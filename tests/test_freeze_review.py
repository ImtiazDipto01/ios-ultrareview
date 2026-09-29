"""Exercise publication metadata failures and frozen artifact preservation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class FreezeReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = 'a' * 40
        self.head = 'b' * 40
        self.model = 'test-provider/recorded-model'
        self.settings = {'reasoning_effort': 'high', 'temperature': None}
        (self.root / 'input.md').write_text(f'Base: `{self.base}`\nHead: `{self.head}`\n')
        (self.root / 'review.md').write_text('Test-only prediction artifact.\n')
        self.write('settings.json', self.settings)
        self.write('tools.json', {'git': 'recorded-version', 'hidden_access': False})
        self.write('host.json', {'model': self.model, 'settings': self.settings, 'kind': 'synthetic test metadata'})
        self.provenance = {'model': self.model, 'settings': self.settings, 'source': {'kind': 'host-recorded', 'label': 'Synthetic host metadata for tool testing only', 'artifact': 'host.json', 'sha256': hashlib.sha256((self.root / 'host.json').read_bytes()).hexdigest()}}
        self.write('provenance.json', self.provenance)

    def write(self, name, data):
        (self.root / name).write_text(json.dumps(data))

    def run_freeze(self, extra=(), model=None, public=True):
        command = [sys.executable, str(ROOT / 'evals/freeze-review.py'), '--input', str(self.root / 'input.md'), '--review', str(self.root / 'review.md'), '--skill', str(ROOT / 'skills/ios-ultrareview'), '--base', self.base, '--head', self.head, '--model', self.model if model is None else model, '--settings-json', str(self.root / 'settings.json'), '--tools-json', str(self.root / 'tools.json'), '--output', str(self.root / 'frozen')]
        if public:
            command += ['--public-benchmark', '--provenance-json', str(self.root / 'provenance.json')]
        return subprocess.run(command + list(extra), text=True, capture_output=True)

    def assert_refused(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse((self.root / 'frozen').exists(), result.stderr)

    def test_public_freeze_preserves_hash_bound_artifacts_and_refuses_overwrite(self):
        result = self.run_freeze()
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.root / 'frozen/record.json').read_text())
        self.assertTrue(record['publication']['metadata_complete'])
        self.assertIsNone(record['tokens'])
        for name, digest in record['artifacts'].items():
            self.assertEqual(hashlib.sha256((self.root / 'frozen' / name).read_bytes()).hexdigest(), digest)
        self.assertEqual((self.root / 'frozen/provenance-source.json').read_bytes(), (self.root / 'host.json').read_bytes())
        prior = (self.root / 'frozen/record.json').read_bytes()
        self.assertNotEqual(self.run_freeze().returncode, 0)
        self.assertEqual((self.root / 'frozen/record.json').read_bytes(), prior)

    def test_unknown_model_rejected_for_public_but_allowed_for_historical(self):
        self.assert_refused(self.run_freeze(model='unknown'))
        self.assertEqual(self.run_freeze(model='unknown', public=False).returncode, 0)

    def test_all_unknown_settings_rejected(self):
        self.write('settings.json', {'temperature': None, 'reasoning_effort': 'unknown'})
        self.assert_refused(self.run_freeze())

    def test_missing_provenance_rejected(self):
        (self.root / 'provenance.json').unlink()
        self.assert_refused(self.run_freeze())

    def test_metadata_mismatch_rejected(self):
        self.provenance['model'] = 'another-model'
        self.write('provenance.json', self.provenance)
        self.assert_refused(self.run_freeze())

    def test_tampered_source_rejected(self):
        self.write('host.json', {'tampered': True})
        self.assert_refused(self.run_freeze())

    def test_unscoped_token_claim_rejected(self):
        self.assert_refused(self.run_freeze(['--tokens', '100']))

    def test_scoped_zero_tokens_are_preserved(self):
        self.provenance['usage'] = {'total_tokens': 0, 'scope': 'Synthetic empty test session; not a model measurement'}
        self.write('provenance.json', self.provenance)
        result = self.run_freeze(['--tokens', '0'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.root / 'frozen/record.json').read_text())['tokens'], 0)

    def test_negative_counter_rejected(self):
        self.assert_refused(self.run_freeze(['--tokens', '-1']))

    def test_target_mismatch_rejected(self):
        (self.root / 'input.md').write_text(f'Base: `{self.base}`\nHead: `{"c" * 40}`\n')
        self.assert_refused(self.run_freeze())

if __name__ == '__main__':
    unittest.main()
