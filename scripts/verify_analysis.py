"""Technical cross-check; no claim of independent human review.
Reads immutable second-transcription data and independently inverts binomial tails.
"""
from pathlib import Path
import json,hashlib,math
from collections import Counter
from html.parser import HTMLParser
from scipy.stats import binom
from scipy.optimize import brentq
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'results/ANALYSIS_V2.json').read_text(encoding='utf8'))
S=json.loads((R/'data/BASE_ESTUDIOS.json').read_text(encoding='utf8'))
B=json.loads((R/'data/SECOND_TECHNICAL_TRANSCRIPTION.json').read_text(encoding='utf8'))
checks=[]
def ck(name,ok,detail=None):checks.append(dict(field=name,ok=bool(ok),detail=detail))
def get(sid,det,op=None):
    a=[p for p in P if p['study']==sid and p['detector']==det and (op is None or op==p['operating_point'])]
    assert len(a)==1,(sid,det,op);return a[0]
def matrix(p,cm,attack_first=False):
    a,b=cm[0];c,d=cm[1];tn,fp,fn,tp=(d,c,b,a) if attack_first else (a,b,c,d)
    expected=dict(tn=tn,fp=fp,fn=fn,tp=tp,n0=tn+fp,n1=fn+tp)
    ck(p['id']+' cells,axes,denominators',all(p[k]==v for k,v in expected.items()),expected)
    ck(p['id']+' rates',abs(p['fpr']-fp/(tn+fp))<1e-13 and abs(p['tpr']-tp/(fn+tp))<1e-13)
for sid in ['K03','K15']:
    for det,cm in B[sid]['matrices'].items():matrix(get(sid,det),cm)
for group,det in [('local','QNN Local'),('ibm','QNN IBM simulator')]:
    for j,(size,cm) in enumerate(zip(B['K11']['nominales'],B['K11'][group])):
        p=get('K11',det,f'subset nominal={size}');matrix(p,cm,True)
        ck(p['id']+' descriptive training only',p['source_training_results'] and not p['main_interval_display'])
        tp,fn=cm[0];fp,tn=cm[1]
        ck(p['id']+' precision/recall correspondence',abs(100*tp/(tp+fn)-B['K11'][f'table3_{group}_precision'][j])<=.00501 and abs(100*tp/(tp+fp)-B['K11'][f'table3_{group}_recall'][j])<=.00501)
for group in ['test','train']:
    for det,cm in B['K17'][group].items():
        p=get('K17',det,'Fig7 '+group.title());matrix(p,cm)
        ck(p['id']+' correct set role',(p['principal'] and p['main_interval_display']) if group=='test' else (not p['principal'] and not p['main_interval_display']))
for det,d in B['K07']['normal_diagonal'].items():
    p=get('K07',det);a=B['K07']['ataques_predichos_normal'][det]
    ck(p['id']+' normalized reconstruction',abs(p['fpr']-(1-d))<1e-14 and p['tpr_range']==[1-max(a),1-min(a)])
    ck(p['id']+' no invented denominators',p['n0'] is None and p['n1'] is None and 'fpr_ci95_cond' not in p)
# Frozen derived second transcription; not a new source-document review.
raw=B['K10']['table3']
p=get('K10','QIDS-OA')
ck('K10 benign row retained',sum(raw[0])==p['n0']==6000 and sum(raw[0][1:])==p['fp']==12 and p['main_interval_display'])
ck('K10 no invented TP',p['tp'] is None and sum(v for row in raw[1:] for v in row if v is not None)==3985 and sum(row[0] for row in raw[1:])==p['fn']==8)
def up(x,n,a):return 1. if x==n else brentq(lambda z:binom.cdf(x,n,z)-a,0.,1.,xtol=1e-14)
def lo(x,n,a):return 0. if x==0 else brentq(lambda z:binom.sf(x-1,n,z)-a,0.,1.,xtol=1e-14)
errors=[]
for p in P:
    if 'fpr_U95_cond' not in p:continue
    x,n=p['fp'],p['n0'];u=up(x,n,.05)
    err=max(abs(u-p['fpr_U95_cond']),abs(lo(x,n,.025)-p['fpr_ci95_cond'][0]),abs(up(x,n,.025)-p['fpr_ci95_cond'][1]))
    errors.append(err);ck(p['id']+' independent FPR inversion',err<1e-10)
    x,n=p['n1']-p['fn'],p['n1'];err=max(abs(lo(x,n,.025)-p['tpr_ci95_cond'][0]),abs(up(x,n,.025)-p['tpr_ci95_cond'][1]))
    errors.append(err);ck(p['id']+' independent TPR inversion',err<1e-10)
for r,e in [(.01,299),(.001,2995),(.0001,29956)]:ck('zero-FP size '+str(r),math.ceil(math.log(.05)/math.log1p(-r))==e)
main=[p for p in P if p['principal']];conditional=[p for p in P if p['main_interval_display']]
ck('main 24 points / 5 articles',len(main)==24 and len({p['study'] for p in main})==5)
ck('conditional 10 points / 3 articles',len(conditional)==10 and len({p['study'] for p in conditional})==3)
ck('complete sensitivity 9',len([p for p in conditional if p['tipo']=='conteos'])==9)
for t,ids in [(.01,['K10-P001']),(.001,[]),(.0001,[])]:ck('conditional reference '+str(t),[p['id'] for p in conditional if p['fpr_U95_cond']<=t]==ids)
ck('selection 21/2/2',Counter(s['inclusion'] for s in S)=={'incluir':21,'excluir':2,'pendiente':2})
ck('families 20',len({s['familia_informe'] for s in S if s['inclusion']=='incluir'})==20)
ck('466 unique records',len(P)==len({p['id'] for p in P})==466)
registry=json.loads((R/'data/SOURCE_REGISTRY.json').read_text(encoding='utf8'))
ck('all25 external source locators',len(registry)==25 and all(x['doi'] and x['location_and_version'] for x in registry))
q=get('K17','QSVM-IGWO','Fig7 Test');rf=get('K17','RF','Fig7 Test')
ck('K17 difference values',abs(100*(q['fpr']-rf['fpr'])+3.5455626418765545)<1e-10 and abs(100*(q['tpr']-rf['tpr'])+.273561595481827)<1e-10)
# Confirm numerical preservation against v1; no absolute-path checks.
reference={p['id']:p for p in json.loads((R/'data/REFERENCE_RESULTS_V1.json').read_text(encoding='utf8'))}
preserved=True
for p in P:
    for key in ['tn','fp','fn','tp','n0','n1','fpr','tpr','fpr_U95_cond','fpr_ci95_cond','tpr_ci95_cond']:
        if key not in p:continue
        old=reference[p['id']].get(key);new=p[key]
        if isinstance(new,list):ok=len(old)==len(new) and all(abs(a-b)<1e-12 for a,b in zip(old,new))
        elif isinstance(new,(int,float)) and old is not None:ok=abs(new-old)<1e-12
        else:ok=new==old
        preserved=preserved and ok
        if not ok:ck(p['id']+' numerical preservation '+key,False,{'old':old,'new':new})
ck('all numerical fields preserved from v1',preserved)
out={'date_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if all(x['ok'] for x in checks) else 'FAIL','n_checks':len(checks),'max_interval_difference':max(errors),'checks':checks,'limits':'Portable numerical check of derived records and frozen transcription. Source copies intentionally absent. No new primary-source review, independent human review, verification of sampling independence, shared instances, label truth or transport. Original workspace audit is separate and optional.'}
(R/'results/TECHNICAL_VERIFICATION_V2.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
print({k:out[k] for k in ['status','n_checks','max_interval_difference']})
for c in checks:
    if not c['ok']:print(c)
if out['status']!='PASS':raise SystemExit(1)
