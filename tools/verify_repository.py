"""Check documentation links/schema/map and preservation of the frozen analysis."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
checks = []


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf8'))


def check(name, condition, detail=None):
    checks.append({'check': name, 'pass': bool(condition), 'detail': detail})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = read('docs/verification/artifact_v2_2.json')
for group in ['core_sha256', 'preview_sha256']:
    for name, expected in baseline[group].items():
        path = ROOT / name
        check('preserved: ' + name, path.is_file() and sha(path) == expected)

manifest = read('INPUT_SHA256.json')['sha256']
for name, expected in manifest.items():
    path = (ROOT / name).resolve()
    check('current snapshot: ' + name,
          path.is_relative_to(ROOT) and path.is_file() and sha(path) == expected)

markdown = sorted(ROOT.glob('*.md')) + sorted((ROOT / 'docs').rglob('*.md'))
link_count = 0
for doc in markdown:
    content = re.sub(r'```.*?```', '', doc.read_text(encoding='utf8'), flags=re.S)
    for target in re.findall(r'\]\(([^\s)]+)\)', content):
        if urlsplit(target).scheme or target.startswith('#'):
            continue
        relative = unquote(target.split('#', 1)[0])
        path = (doc.parent / relative).resolve()
        link_count += 1
        check(f'local link: {doc.relative_to(ROOT).as_posix()} -> {target}',
              path.is_relative_to(ROOT) and path.exists())
check('documentation links were inspected', link_count >= 30, link_count)

dictionary = read('docs/data_dictionary.json')
for group, filename in [('study', 'BASE_ESTUDIOS.json'),
                        ('point', 'PUNTOS_OPERACION.json'),
                        ('source_registry', 'SOURCE_REGISTRY.json')]:
    keys = set().union(*(row.keys() for row in read('data/' + filename)))
    check('dictionary coverage: ' + group, keys == set(dictionary[group]),
          {'undocumented': sorted(keys - set(dictionary[group]))})

analysis = read('results/ANALYSIS_V2.json')
raw_keys = set().union(*(row.keys() for row in read('data/PUNTOS_OPERACION.json')))
derived_keys = set().union(*(row.keys() for row in analysis)) - raw_keys
check('derived dictionary coverage', derived_keys == set(dictionary['derived']))
record_ids = {row['id'] for row in read('data/BASE_ESTUDIOS.json')}
for item in read('docs/artifact_map.json'):
    check('artifact map: ' + item['article_object'],
          all((ROOT / name).is_file() for name in item['outputs'])
          and set(item['source_ids']) <= record_ids)

report = read('results/TECHNICAL_VERIFICATION_V2.json')
check('archived numerical checks pass', report['status'] == 'PASS' and report['n_checks'] == 180)
check('citation still identifies the archived artifact',
      '10.5281/zenodo.23642804' in (ROOT / 'CITATION.cff').read_text(encoding='utf8')
      and (ROOT / 'VERSION').read_text(encoding='utf8').strip() == '2.2.0')
check('current licensing heading is version-neutral',
      'v2.1.0' not in (ROOT / 'LICENSING.txt').read_text(encoding='utf8').splitlines()[0])

out = {'status': 'PASS' if all(c['pass'] for c in checks) else 'FAIL',
       'checks': checks, 'n_checks': len(checks), 'local_links_checked': link_count,
       'scope': 'Documentation/integrity and preserved-analysis checks, not independent source review or statistical-assumption validation.'}
(ROOT / 'results/REPOSITORY_VERIFICATION.json').write_text(json.dumps(out, indent=2), encoding='utf8')
print({k: out[k] for k in ['status', 'n_checks', 'local_links_checked']})
for result in checks:
    if not result['pass']:
        print(result)
if out['status'] != 'PASS':
    raise SystemExit(1)
