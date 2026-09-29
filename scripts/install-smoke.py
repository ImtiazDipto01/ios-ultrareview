#!/usr/bin/env python3
"""Install into an owned disposable project; never change user/global skills."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default=str(ROOT), help='Local checkout or remote repository/tree URL')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='ios-ultrareview-install-') as scratch:
        project = Path(scratch)
        env = {**os.environ, 'npm_config_cache': str(project / 'npm-cache'), 'DISABLE_TELEMETRY': '1', 'CI': 'true'}
        command = ['npx', '--yes', 'skills@1.7.0', 'add', args.source, '--skill', 'ios-ultrareview', '--agent', 'codex', 'claude-code', 'cursor', '--copy', '--yes']
        result = subprocess.run(command, cwd=project, env=env, text=True, capture_output=True)
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        expected = {p.relative_to(ROOT / 'skills/ios-ultrareview'): p.read_bytes() for p in (ROOT / 'skills/ios-ultrareview').rglob('*') if p.is_file()}
        for agent, directory in [('codex', '.agents/skills'), ('claude-code', '.claude/skills'), ('cursor', '.agents/skills')]:
            installed = project / directory / 'ios-ultrareview'
            for relative, data in expected.items():
                if not (installed / relative).is_file() or (installed / relative).read_bytes() != data:
                    raise SystemExit(f'Installed content mismatch: {agent}: {relative}')
            if (installed / 'evals').exists():
                raise SystemExit('Maintainer evaluations were installed with runtime')
            print(f'PASS: {agent}, {len(expected)} complete skill files match source')
        print('PASS: isolated project installation; no global installation requested')

if __name__ == '__main__':
    main()
