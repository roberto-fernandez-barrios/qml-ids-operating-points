from pathlib import Path
import json,math,re,shutil,unicodedata
from collections import Counter
import numpy as np
from scipy.stats import beta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'data/PUNTOS_OPERACION.json').read_text(encoding='utf8'))
S=json.loads((R/'data/BASE_ESTUDIOS.json').read_text(encoding='utf8'))
N=json.loads((R/'data/study_notes_en.json').read_text(encoding='utf8'))
LOC=json.loads((R/'data/source_locations_en.json').read_text(encoding='utf8'))
for folder in ['results','figures','tables']:(R/folder).mkdir(exist_ok=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def tex(s):
    s=str(s).replace('ș','s').replace('ı','i').replace('−','-').replace('–','--').replace('—','---').replace('‐','-').replace('→',' to ').replace('≤','<=').replace('≈','~').replace('×','x').replace('\u202f',' ').replace('\u00a0',' ')
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(c,c) for c in s)
def num(x,d=3):return f'{100*x:.{d}f}'
def ci(x,n):return [0 if x==0 else float(beta.ppf(.025,x,n-x+1)),1 if x==n else float(beta.ppf(.975,x+1,n-x))]
def upper(x,n):return 1 if x==n else float(beta.ppf(.95,x+1,n-x))
def label(p):
    s=p['detector'].replace(' (submodelo simulado)','').replace('QNN IBM simulator','IBM sim. QNN').replace('QNN Local','Local QNN').replace('Aria1 simulación1000shots','Aria-1 sim., 1000 shots').replace('Aria1 QPU200shots','Aria-1 QPU, 200 shots').replace('Harmony120shots','Harmony, 120 shots').replace('Harmony200shots','Harmony, 200 shots')
    if p['study']=='K11':s+=' / '+format(p['nominal_size'],',')
    return s
count_types=('conteos','conteos_parciales','suplemento_codigo','conteos_mapeo_condicionado')
for p in P:
    p['provenance_en']=N[p['study']]['provenance']
    p['source_training_results']=p['study']=='K11'
    p['main_interval_display']=p['principal'] and p['tipo'] in ('conteos','conteos_parciales') and p['study']!='K11'
    if p['tipo'] in count_types:
        p['fpr_ci95_cond']=ci(p['fp'],p['n0']);p['fpr_U95_cond']=upper(p['fp'],p['n0'])
        p['resolution_fpr']=1/p['n0']
        p['tpr_ci95_cond']=[1-x for x in reversed(ci(p['fn'],p['n1']))]
        p['interval_status_en']='Hypothetical only; source describes training results' if p['study']=='K11' else 'Conditional calculation; population guarantee not verified'
        p['reference_support_cond']={str(t):p['fpr_U95_cond']<=t for t in [.01,.001,.0001]}
    if p['study']=='K11':
        p['inferencia']='Descriptive training results as described in source section3.3; independent evaluation not established. Hypothetical intervals restricted to supplement.'
        p['source_caveat']=p['inferencia']
dump(R/'results/ANALYSIS_V2.json',P)
main=[p for sid in ['K03','K10','K11','K17','K07'] for p in P if p['study']==sid and p['principal']]
primary_ci=[p for p in main if p['main_interval_display']]
complete_ci=[p for p in primary_ci if p['tipo']=='conteos']
summary=dict(articles_included=21,documentary_families=20,methodology_consulted=15,
    main_articles=5,main_points=len(main),complete_matrix_points=19,partial_matrix_points=1,normalized_points=4,
    source_training_points=10,main_conditional_calculation_points=len(primary_ci),complete_matrix_sensitivity_points=len(complete_ci),
    primary_fpr_support={str(t):[p['id'] for p in primary_ci if p['fpr_U95_cond']<=t] for t in [.01,.001,.0001]},
    complete_matrix_sensitivity={str(t):[p['id'] for p in complete_ci if p['fpr_U95_cond']<=t] for t in [.01,.001,.0001]},
    supported_population_guarantees_verified=0,guarantee_denominator=15,
    n0_descriptive_range=[153,9251],n0_main_conditional_range=[442,9251],human_review='PENDING',
    comparison_assumption='Matching denominators do not establish identical instances; no paired inference.',
    k10='FP12/n06000 remains in FPR analysis. TPR needs additional Table2-3 and FN-exhaustiveness assumptions.')
dump(R/'results/SUMMARY_V2.json',summary)

# Main joint operating-point figure: no K11 hypothetical uncertainty or U95 labels.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','pdf.fonttype':42})
fig=plt.figure(figsize=(7.05,7.6))
gs=fig.add_gridspec(1,3,width_ratios=[1.0,1.0,.9],left=.30,right=.995,top=.94,bottom=.10,wspace=.12)
axf=fig.add_subplot(gs[0]);axt=fig.add_subplot(gs[1],sharey=axf);axn=fig.add_subplot(gs[2],sharey=axf)
colors={'K03':'#0072B2','K10':'#D55E00','K11':'#555555','K17':'#009E73','K07':'#8a6599'}
labels=[]
for y,p in enumerate(main):
    sid=p['study'];c=colors[sid];labels.append(sid+' '+label(p)+(' *' if sid=='K10' else ''))
    if p['main_interval_display']:
        for ax,v,intv in [(axf,p['fpr'],p['fpr_ci95_cond']),(axt,p['tpr'],p['tpr_ci95_cond'])]:
            ax.errorbar(100*v,y,xerr=[[100*(v-intv[0])],[100*(intv[1]-v)]],fmt='D' if sid=='K10' else 'o',color=c,ms=4,capsize=2,lw=.9,markerfacecolor='white' if sid=='K10' else c)
        axn.text(0,y,f"{p['fp']}/{p['n0']} | {p['fn']}/{p['n1']}",va='center',fontsize=6.6,color=c)
    elif sid=='K11':
        axf.plot(100*p['fpr'],y,'o',color=c,ms=4,markerfacecolor='white');axt.plot(100*p['tpr'],y,'o',color=c,ms=4,markerfacecolor='white')
        axn.text(0,y,f"{p['fp']}/{p['n0']} | {p['fn']}/{p['n1']}",va='center',fontsize=6.6,color=c)
    else:
        axf.plot(100*p['fpr'],y,'s',color=c,ms=4)
        lo,hi=p['tpr_range'];lo=max(0,lo-.005);hi=min(1,hi+.005)
        axt.hlines(y,100*lo,100*hi,color=c,ls='--',lw=1.5);axt.plot([100*lo,100*hi],[y,y],'|',color=c)
        axn.text(0,y,'Normalized; n unknown',va='center',fontsize=6.6,color=c)
    if y and main[y-1]['study']!=sid:
        for ax in [axf,axt,axn]:ax.axhline(y-.5,color='.78',lw=.65)
axf.set_xscale('log');axf.set_xlim(.007,105);axf.set_xticks([.01,.1,1,10,100],labels=['0.01','0.1','1','10','100'])
for x in [.01,.1,1]:axf.axvline(x,color='.7',ls=':',lw=.7,zorder=0)
axt.set_xlim(60,100.5);axt.set_xticks([60,80,100])
axf.set_yticks(range(len(main)),labels=labels,fontsize=7.4);axf.set_ylim(len(main)-.35,-.75)
for ax,title in [(axf,'FPR (%)'),(axt,'Attack TPR (%)')]:
    ax.set_title(title,fontsize=9);ax.grid(axis='x',alpha=.12);ax.tick_params(axis='y',length=0);ax.tick_params(axis='x',labelsize=7);ax.spines[['top','right','left']].set_visible(False)
axt.tick_params(labelleft=False);axn.axis('off');axn.set_title('FP / n0 | FN / n1',fontsize=9)
fig.text(.30,.036,'Bars: conditional 95% intervals. K11: training descriptions, no intervals.\nDashed ranges: unknown attack weights and rounding, not sampling uncertainty.',fontsize=6.6)
for ext in ['pdf','svg','png']:fig.savefig(R/f'figures/figure1_operating_points.{ext}',dpi=300)
plt.close(fig)

# All five K17 test-labelled points, no connecting ROC and no paired uncertainty.
k17=[p for p in P if p['study']=='K17' and p['operating_point']=='Fig7 Test']
fig,ax=plt.subplots(figsize=(6.2,3.7));fig.subplots_adjust(left=.12,right=.95,top=.93,bottom=.18)
for p in k17:
    col='#0072B2' if p['detector']=='QSVM-IGWO' else '#D55E00' if p['detector']=='RF' else '#6a6a6a'
    ax.scatter(100*p['fpr'],100*p['tpr'],s=45,c=col,zorder=3)
    dx,dy=(-1.5,-.75) if p['detector']=='QSVM-IGWO' else (.15,.18)
    ax.annotate(p['detector'],(100*p['fpr'],100*p['tpr']),xytext=(100*p['fpr']+dx,100*p['tpr']+dy),fontsize=9,color=col)
ax.set(xlabel='Observed FPR (%)',ylabel='Observed attack TPR (%)',xlim=(1.5,14.5),ylim=(85.5,95.5));ax.grid(alpha=.2)
ax.spines[['top','right']].set_visible(False)
for ext in ['pdf','svg','png']:fig.savefig(R/f'figures/figure2_k17_tradeoff.{ext}',dpi=300)
plt.close(fig)

def longtable(header,cols,rows,caption):
    return '\\begin{longtable}{'+cols+'}\n\\caption{'+caption+'}\\\\\n\\toprule\n'+header+'\\\\\n\\midrule\n\\endfirsthead\n\\toprule\n'+header+'\\\\\n\\midrule\n\\endhead\n'+ '\n'.join(rows)+'\n\\bottomrule\n\\end{longtable}\n'
# All count-based numerical values, with hypothetical training calculations separate.
for name,points in [('conditional_points',primary_ci),('k11_hypothetical',[p for p in main if p['study']=='K11']),('supplementary_counts',[p for p in P if p['tipo'] in ('suplemento_codigo','conteos_mapeo_condicionado')])]:
    rows=[]
    for p in points:
        rows.append(tex(p['id']+' '+label(p))+' & '+str(p['fp'])+'/'+str(p['n0'])+' & '+str(p['fn'])+'/'+str(p['n1'])+' & '+num(p['fpr'])+' & '+num(p['tpr'])+' & '+num(p['fpr_U95_cond'])+r' \\')
    out=longtable(r'Point / detector & FP/$n_0$ & FN/$n_1$ & FPR & TPR & $U_{.95}$',r'p{5.2cm}rrrrr',rows,{'conditional_points':'Conditional pointwise calculations retained in the main FPR analysis. Rates in percent; K10 TPR requires extra reconstruction assumptions.','k11_hypothetical':'Hypothetical calculations for K11 training-described results. These intervals are excluded from the main figure and are not evidence of independent evaluation. Rates in percent.','supplementary_counts':'Supplementary code/mapping-conditional results. No result in this table is promoted to an unambiguous primary published point. Rates in percent.'}[name])
    (R/f'tables/{name}.tex').write_text(out,encoding='utf8')
rows=[]
for p in primary_ci:
    rows.append(tex(p['id']+' '+label(p))+' & '+f"[{num(p['fpr_ci95_cond'][0])}, {num(p['fpr_ci95_cond'][1])}]"+' & '+f"[{num(p['tpr_ci95_cond'][0])}, {num(p['tpr_ci95_cond'][1])}]"+r' \\')
(R/'tables/intervals.tex').write_text(longtable(r'Point / detector & FPR 95\% interval & TPR 95\% interval',r'p{6cm}rr',rows,r'Marginal, pointwise conditional intervals used in Figure 1; not a joint 95\% region.'),encoding='utf8')
rows=[]
for p in [p for p in main if p['study']=='K11']:
    rows.append(tex(p['id']+' '+label(p))+' & '+f"[{num(p['fpr_ci95_cond'][0])}, {num(p['fpr_ci95_cond'][1])}]"+' & '+f"[{num(p['tpr_ci95_cond'][0])}, {num(p['tpr_ci95_cond'][1])}]"+r' \\')
(R/'tables/k11_intervals.tex').write_text(longtable(r'Point / detector & Hypothetical FPR CI & Hypothetical TPR CI',r'p{6cm}rr',rows,'K11 hypothetical intervals only; the fixed-detector, independent-test interpretation is not established.'),encoding='utf8')
rows=[]
for s in S:
    sid=s['id'];n=N[sid]
    rows.append(sid+' & '+tex(s['autores'].replace(' y ',' and '))+' & '+tex(n['selection'])+' & '+tex(n['access'])+r' \\')
(R/'tables/selection.tex').write_text(longtable('ID & Report & Eligibility & Access',r'p{.8cm}p{4.4cm}p{2.3cm}p{6.1cm}',rows,'All 25 entries in the original order of the Kaissar frame. Access is not an eligibility criterion.'),encoding='utf8')
# Readable source dossiers, English interpretation alongside frozen original extraction.
pages=[]
for s in S:
    sid=s['id'];n=N[sid]
    pages.extend([r'\subsection{'+sid+': '+tex(s['autores'].replace(' y ',' and '))+'}',r'\textbf{'+tex(s['title'])+r'.} \cite{'+sid+r'} \url{'+s['url']+'}.',
      r'\textbf{Selection/access:} '+tex(n['selection']+'; '+n['access'])+'.',
      r'\textbf{Location/version:} '+tex(LOC[sid])+'.',
      r'\textbf{Authors\textquotesingle{} claim:} '+tex(n['claim']),
      r'\textbf{Decision rule:} '+tex(n['rule']),
      r'\textbf{Recoverable evidence:} '+tex(n['finding']),
      r'\textbf{Provenance/limit:} '+tex(n['provenance'])+'\n'])
(R/'tables/source_dossiers.tex').write_text('\n\n'.join(pages),encoding='utf8')
print(json.dumps(summary,indent=2))
