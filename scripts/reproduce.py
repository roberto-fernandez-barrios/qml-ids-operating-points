"""Offline reconstruction, without detector training or source recovery."""
from pathlib import Path
import subprocess,sys,json,platform,importlib.metadata
R=Path(__file__).resolve().parents[1]
for name in ['verify_package.py','prepare_analysis.py','verify_analysis.py','make_browser.py']:
    result=subprocess.run([sys.executable,'-B',str(R/'scripts'/name)],cwd=R)
    if result.returncode:raise SystemExit(result.returncode)
env={'python':sys.version,'platform':platform.platform(),'packages':{p:importlib.metadata.version(p) for p in ['numpy','scipy','matplotlib']},'scope':'Local reconstruction from derived results. No network, detector training or quantum execution.'}
(R/'results/ENVIRONMENT.json').write_text(json.dumps(env,indent=2),encoding='utf8');print('Reproduction complete. See results/, figures/ and tables/.')
