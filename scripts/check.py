#!/usr/bin/env python3
"""Check distributable structure, local references, syntax and public-data hygiene."""
import ast
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/ios-ultrareview'

def main():
    errors = []
    text = (SKILL / 'SKILL.md').read_text()
    if not text.startswith('---\n'):
        errors.append('Missing skill frontmatter')
    frontmatter = text.split('---', 2)[1]
    for pattern in [r'(?m)^name: ios-ultrareview$', r'(?m)^description: .+', r'(?m)^  version: "1\.0\.1"$']:
        if not re.search(pattern, frontmatter):
            errors.append('Invalid required skill metadata: ' + pattern)
    for name in ['LICENSE', 'THIRD_PARTY_NOTICES.md']:
        if (ROOT / name).read_bytes() != (SKILL / name).read_bytes():
            errors.append('Installed notice differs: ' + name)
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
            continue
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=str(path))
        elif path.suffix == '.json':
            json.loads(path.read_text())
        if path.suffix not in {'.md', '.json', '.yaml', '.yml', '.svg', '.py'}:
            continue
        content = path.read_text()
        if ('/' + 'Users/') in content or ('BEGIN ' + 'PRIVATE KEY') in content:
            errors.append('Private host path/key marker: ' + str(path.relative_to(ROOT)))
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', content):
                target = target.strip().split('#', 1)[0]
                if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                    continue
                if not (path.parent / target).exists():
                    errors.append(f'Broken local link in {path.relative_to(ROOT)}: {target}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: skill structure, local links, Python/JSON syntax, license copies, public-data hygiene')

if __name__ == '__main__':
    main()
