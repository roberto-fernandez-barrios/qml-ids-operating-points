from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'results/ANALYSIS_V2.json').read_text(encoding='utf8'));S=json.loads((R/'data/SOURCE_REGISTRY.json').read_text(encoding='utf8'));N=json.loads((R/'data/study_notes_en.json').read_text(encoding='utf8'));esc=html.escape
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Derived QML-IDS extraction v2</title><style>body{font:16px/1.5 system-ui;max-width:1200px;margin:2em;color:#172333}details{padding:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1,h2{color:#174a68}input{width:95%;padding:12px}</style><h1>Derived extraction: closed Kaissar corpus</h1><p>21 included articles, 20 documentary families, substantive methodology consulted for 15, 24 descriptive points from five articles. The 466 records are not independent studies. Source copies are intentionally excluded. Human review remains pending.</p><input id="q" placeholder="Filter by study, detector, dataset or count">']
for s in S:
    sid=s['id'];parts.append('<section><h2>'+sid+' '+esc(s['title'])+'</h2><p><a href="'+esc(s['url'])+'">'+esc(s['doi'])+'</a></p><p>'+esc(s['location_and_version'])+'</p>')
    for k,v in N[sid].items():parts.append('<p><b>'+esc(k)+': </b>'+esc(v)+'</p>')
    for p in [p for p in P if p['study']==sid]:parts.append('<details><summary>'+esc(p['id']+' | '+p['detector']+' | '+p['operating_point'])+'</summary><pre>'+esc(json.dumps(p,indent=2,ensure_ascii=False))+'</pre></details>')
    parts.append('</section>')
parts.append('<script>document.getElementById("q").addEventListener("input",e=>document.querySelectorAll("section").forEach(s=>s.hidden=!s.textContent.toLowerCase().includes(e.target.value.toLowerCase())));</script></html>')
(R/'results/extraction_browser.html').write_text('\n'.join(parts),encoding='utf8');print('Offline browser generated.')
