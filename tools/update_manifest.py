"""Maintainer utility: hash intentionally staged/tracked files, never the archive."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf8').split('\0')
names = sorted(n for n in names if n and n != 'INPUT_SHA256.json')
if not names:
    raise SystemExit('No tracked files. Stage intended changes before updating the manifest.')
hashes = {}
for name in names:
    path = ROOT / name
    if not path.is_file():
        raise SystemExit('Tracked file missing: ' + name)
    hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
manifest = {
    'analysis_version': '2.2.0',
    'scope': 'Current main-branch documentation snapshot; includes tracked inputs, guides, previews and CI. The published v2.2.0 artifact has its own unchanged manifest.',
    'sha256': hashes,
}
(ROOT / 'INPUT_SHA256.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
print(f'Updated current-checkout manifest: {len(hashes)} files. Review and stage it explicitly.')
