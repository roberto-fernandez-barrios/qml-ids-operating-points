"""Verify included immutable files by relative paths; no workspace access."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def verify():
    manifest=R/'INPUT_SHA256.json'
    if not manifest.exists():raise SystemExit('INPUT_SHA256.json missing; package integrity cannot be checked.')
    expected=json.loads(manifest.read_text(encoding='utf8'))['sha256'];missing=[];changed=[]
    for name,digest in expected.items():
        p=(R/name).resolve()
        if not p.is_relative_to(R):raise SystemExit('Unsafe manifest path: '+name)
        if not p.is_file():missing.append(name)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=digest:changed.append(name)
    out={'status':'PASS' if not missing and not changed else 'FAIL','included_files_checked':len(expected),'missing_in_package':missing,'hash_mismatches_in_package':changed,'original_workspace':'NOT_REQUESTED; separate optional audit','excluded_primary_sources':'Intentionally absent; not an integrity error.'}
    (R/'results').mkdir(exist_ok=True);(R/'results/PACKAGE_INTEGRITY.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
    if out['status']!='PASS':raise SystemExit(1)
    return out
if __name__=='__main__':verify()
