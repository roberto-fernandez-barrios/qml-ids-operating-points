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
    p['source_training_results']=p['study']=='K11' or (p['study']=='K17' and p['operating_point']=='Fig7 Train')
    p['source_test_adjustments']=p['study']=='K03'
    p['provenance_class']='training_described' if p['source_training_results'] else 'test_adjustments_described' if p['source_test_adjustments'] else 'normalized_unknown_weights' if p['study']=='K07' else 'evaluation_independence_unverified' if p['principal'] else 'supplementary_or_other'
    p['main_interval_display']=p['principal'] and p['tipo'] in ('conteos','conteos_parciales') and not (p['source_training_results'] or p['source_test_adjustments'])
    if p['tipo'] in count_types:
        p['fpr_ci95_cond']=ci(p['fp'],p['n0']);p['fpr_U95_cond']=upper(p['fp'],p['n0'])
        p['resolution_fpr']=1/p['n0']
        p['tpr_ci95_cond']=[1-x for x in reversed(ci(p['fn'],p['n1']))]
        p['interval_status_en']='Hypothetical only; source describes training results' if p['source_training_results'] else 'Hypothetical only; source describes adjustments after test inspection' if p['source_test_adjustments'] else 'Conditional calculation; independence and population guarantee not verified'
        p['reference_support_cond']={str(t):p['fpr_U95_cond']<=t for t in [.01,.001,.0001]}
    if p['study']=='K07' and p['principal']:
        p['fpr_rounding_range']=[max(0,p['fpr']-.005),min(1,p['fpr']+.005)]
        p['tpr_identification_rounding_range']=[max(0,p['tpr_range'][0]-.005),min(1,p['tpr_range'][1]+.005)]
    if p['study']=='K03':
        p['inferencia']='Descriptive rates; source describes post-test adjustments. Hypothetical intervals restricted to supplement.'
        p['source_caveat']=p['inferencia']
    if p['study']=='K11':
        p['inferencia']='Descriptive training results as described in source section3.3; independent evaluation not established. Hypothetical intervals restricted to supplement.'
        p['source_caveat']=p['inferencia']
dump(R/'results/ANALYSIS_V2.json',P)
main=[p for sid in ['K03','K10','K11','K17','K07'] for p in P if p['study']==sid and p['principal']]
primary_ci=[p for p in main if p['main_interval_display']]
complete_ci=[p for p in primary_ci if p['tipo']=='conteos']
legacy_ci=[p for p in main if p['tipo'] in ('conteos','conteos_parciales') and p['study']!='K11']
k03_hyp=[p for p in main if p['study']=='K03']
summary=dict(articles_included=21,documentary_families=20,methodology_consulted=15,
    main_articles=5,main_points=len(main),complete_matrix_points=19,partial_matrix_points=1,normalized_points=4,
    source_training_points=10,test_adjustment_points=4,legacy_conditional_points=10,legacy_conditional_articles=3,main_conditional_articles=2,main_conditional_calculation_points=len(primary_ci),complete_matrix_sensitivity_points=len(complete_ci),
    primary_fpr_support={str(t):[p['id'] for p in primary_ci if p['fpr_U95_cond']<=t] for t in [.01,.001,.0001]},
    complete_matrix_sensitivity={str(t):[p['id'] for p in complete_ci if p['fpr_U95_cond']<=t] for t in [.01,.001,.0001]},
    supported_population_guarantees_verified=0,guarantee_denominator=15,
    n0_descriptive_range=[153,9251],n0_main_conditional_range=[6000,9251],human_review='CLOSED_AUTHOR_CONFIRMED',
    legacy_fpr_support={str(t):[p['id'] for p in legacy_ci if p['fpr_U95_cond']<=t] for t in [.01,.001,.0001]},
    zero_error_upper_at_max_n0=upper(0,9251),min_n0_zero_error_0_01pct=math.ceil(math.log(.05)/math.log1p(-.0001)),
    provenance_rule='All identifiable rates remain descriptive. Training-described or post-test-adjusted counts receive hypothetical intervals only. Other eligible count points remain conditional on unverified independence.',
    comparison_assumption='Matching denominators do not establish identical instances; no paired inference.',
    k10='FP12/n06000 remains in FPR analysis. TPR needs additional Table2-3 and FN-exhaustiveness assumptions.')
dump(R/'results/SUMMARY_V2.json',summary)

# Provenance-aware main figure: six conditional, four adjusted-test descriptive,
# four normalized-range points, and ten training descriptions on a separate panel.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','pdf.fonttype':42})
fig=plt.figure(figsize=(7.2,8.0))
gs=fig.add_gridspec(2,3,width_ratios=[1,1,.92],height_ratios=[14,5.5],left=.255,right=.985,top=.91,bottom=.12,hspace=.52,wspace=.14)
axf=fig.add_subplot(gs[0,0]);axt=fig.add_subplot(gs[0,1],sharey=axf);axn=fig.add_subplot(gs[0,2],sharey=axf)
colors={'K03':'#0072B2','K10':'#D55E00','K17':'#009E73','K07':'#80538c'}
upper_points=[p for sid in ['K10','K17','K03','K07'] for p in main if p['study']==sid]
labels=[]
for y,p in enumerate(upper_points):
    sid=p['study'];c=colors[sid];labels.append(sid+' '+label(p)+(' *' if sid=='K10' else ''))
    if p['main_interval_display']:
        for ax,v,intv in [(axf,p['fpr'],p['fpr_ci95_cond']),(axt,p['tpr'],p['tpr_ci95_cond'])]:
            ax.errorbar(100*v,y,xerr=[[100*(v-intv[0])],[100*(intv[1]-v)]],fmt='D' if sid=='K10' else 'o',color=c,ms=4,capsize=2,lw=.9,markerfacecolor='white' if sid=='K10' else c)
    elif sid=='K03':
        axf.plot(100*p['fpr'],y,'^',color=c,ms=4.5,markerfacecolor='white');axt.plot(100*p['tpr'],y,'^',color=c,ms=4.5,markerfacecolor='white')
    else:
        lo,hi=p['fpr_rounding_range'];axf.hlines(y,100*lo,100*hi,color=c,ls='--',lw=1.3);axf.plot([100*lo,100*hi],[y,y],'|',color=c);axf.plot(100*p['fpr'],y,'s',color=c,ms=3)
        lo,hi=p['tpr_identification_rounding_range'];axt.hlines(y,100*lo,100*hi,color=c,ls='--',lw=1.3);axt.plot([100*lo,100*hi],[y,y],'|',color=c)
    axn.text(0,y,f"{p['fp']}/{p['n0']} | {p['fn']}/{p['n1']}" if sid!='K07' else 'Normalized; n unknown',va='center',fontsize=7,color=c)
    if y in [6,10]:
        for ax in [axf,axt,axn]:ax.axhline(y-.5,color='.70',lw=.8)
axf.set_xscale('log');axf.set_xlim(.007,110);axf.set_xticks([.01,.1,1,10,100],labels=['0.01','0.1','1','10','100'])
for x in [.01,.1,1]:axf.axvline(x,color='.7',ls=':',lw=.7,zorder=0)
axt.set_xlim(75,100.8);axt.set_xticks([80,90,100]);axf.set_yticks(range(len(upper_points)),labels=labels,fontsize=7.7);axf.set_ylim(len(upper_points)-.4,-.8)
for ax,title in [(axf,'FPR (%) - log scale'),(axt,'Attack TPR (%)')]:
    ax.set_title(title,fontsize=8.5);ax.grid(axis='x',alpha=.12);ax.tick_params(axis='y',length=0);ax.tick_params(axis='x',labelsize=7);ax.spines[['top','right','left']].set_visible(False)
axt.tick_params(labelleft=False);axn.axis('off');axn.set_title('FP / n0 | FN / n1',fontsize=8.2)
fig.text(.025,.977,'A. Count and normalized points (14)',fontsize=10,weight='bold')
fig.text(.025,.952,'Solid bars: conditional, independence unverified. Triangles: test adjustments, no intervals.',fontsize=7.5)
fig.text(.025,.36,'B. K11 training-described simulation results (10)',fontsize=10,weight='bold')
bf=fig.add_subplot(gs[1,0]);bt=fig.add_subplot(gs[1,1],sharey=bf);bn=fig.add_subplot(gs[1,2]);bn.axis('off')
for j,size in enumerate([1000,2000,4000,8000,16000]):
    for det,dy,marker,c in [('QNN Local',-.13,'o','#555555'),('QNN IBM simulator',.13,'s','#0072B2')]:
        p=next(p for p in main if p['study']=='K11' and p['nominal_size']==size and p['detector']==det)
        bf.plot(100*p['fpr'],j+dy,marker=marker,color=c,ms=4.5,markerfacecolor='white',linestyle='none');bt.plot(100*p['tpr'],j+dy,marker=marker,color=c,ms=4.5,markerfacecolor='white',linestyle='none')
bf.set_yticks(range(5),labels=[f'Nominal {n:,}' for n in [1000,2000,4000,8000,16000]],fontsize=8);bf.set_ylim(4.6,-.6);bf.set_xlim(0,35);bf.set_xticks([0,10,20,30]);bt.set_xlim(65,100);bt.set_xticks([70,80,90,100]);bt.tick_params(labelleft=False)
for ax,title in [(bf,'FPR (%) - linear scale'),(bt,'Attack TPR (%)')]:
    ax.set_title(title,fontsize=8.5);ax.grid(axis='x',alpha=.15);ax.tick_params(axis='y',length=0);ax.spines[['top','right','left']].set_visible(False)
bn.legend(handles=[Line2D([0],[0],marker='o',mfc='white',color='#555555',linestyle='none',label='Local'),Line2D([0],[0],marker='s',mfc='white',color='#0072B2',linestyle='none',label='IBM simulator')],loc='upper left',frameon=False,fontsize=8,handletextpad=.4)
bn.text(.04,.38,'No intervals.\nNominal size is\nnot a test count.\nClass counts differ\nbetween platforms.',transform=bn.transAxes,fontsize=7.5,va='top',linespacing=1.5)
fig.text(.025,.025,'Dashed purple bars: rounding ranges for FPR; unknown attack weights plus rounding for TPR.\nThese are identification ranges, not confidence intervals. * K10 TPR requires extra assumptions.\nAll 24 descriptive points retained; K03 and K11 hypothetical intervals are supplementary only.',fontsize=7.2,linespacing=1.5)
for ext in ['pdf','svg','png']:fig.savefig(R/f'figures/figure1_operating_points.{ext}',dpi=300)
plt.close(fig)
dump(R/'results/FIGURE_MANIFEST_V2_2.json',{
    'descriptive_point_ids':[p['id'] for p in upper_points]+[p['id'] for p in main if p['study']=='K11'],
    'conditional_interval_ids':[p['id'] for p in upper_points if p['main_interval_display']],
    'no_interval_due_provenance_ids':[p['id'] for p in main if p['study'] in ('K03','K11')],
    'rounding_range_ids':[p['id'] for p in upper_points if p['study']=='K07'],
    'k11_layout':'Five nominal sizes, two offset platform markers per row; no connecting lines or intervals',
    'source_counts':'unchanged', 'format':'vector PDF and SVG; PNG for preview'
})

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
for name,points in [('conditional_points',primary_ci),('legacy_conditional_points',legacy_ci),('k03_hypothetical',k03_hyp),('k11_hypothetical',[p for p in main if p['study']=='K11']),('supplementary_counts',[p for p in P if p['tipo'] in ('suplemento_codigo','conteos_mapeo_condicionado')])]:
    rows=[]
    for p in points:
        rows.append(tex(p['id']+' '+label(p))+' & '+str(p['fp'])+'/'+str(p['n0'])+' & '+str(p['fn'])+'/'+str(p['n1'])+' & '+num(p['fpr'])+' & '+num(p['tpr'])+' & '+num(p['fpr_U95_cond'])+r' \\')
    out=longtable(r'Point / detector & FP/$n_0$ & FN/$n_1$ & FPR & TPR & $U_{.95}$',r'p{5.2cm}rrrrr',rows,{'legacy_conditional_points':'Historical v2.1 ten-point calculation retained for comparison only; K03 intervals are hypothetical in the current hierarchy. Rates in percent.', 'k03_hypothetical':'K03 hypothetical fixed-detector calculations; post-test adjustments prevent an independent-test interpretation. Rates in percent.', 'conditional_points':'Conditional pointwise calculations retained in the main FPR analysis. Rates in percent; K10 TPR requires extra reconstruction assumptions.','k11_hypothetical':'Hypothetical calculations for K11 training-described results. These intervals are excluded from the main figure and are not evidence of independent evaluation. Rates in percent.','supplementary_counts':'Supplementary code/mapping-conditional results. No result in this table is promoted to an unambiguous primary published point. Rates in percent.'}[name])
    (R/f'tables/{name}.tex').write_text(out,encoding='utf8')
rows=[]
for p in primary_ci:
    rows.append(tex(p['id']+' '+label(p))+' & '+f"[{num(p['fpr_ci95_cond'][0])}, {num(p['fpr_ci95_cond'][1])}]"+' & '+f"[{num(p['tpr_ci95_cond'][0])}, {num(p['tpr_ci95_cond'][1])}]"+r' \\')
(R/'tables/intervals.tex').write_text(longtable(r'Point / detector & FPR 95\% interval & TPR 95\% interval',r'p{6cm}rr',rows,r'Marginal, pointwise conditional intervals used in Figure 1; not a joint 95\% region.'),encoding='utf8')
rows=[]
for p in [p for p in main if p['study'] in ('K03','K11')]:
    rows.append(tex(p['id']+' '+label(p))+' & '+f"[{num(p['fpr_ci95_cond'][0])}, {num(p['fpr_ci95_cond'][1])}]"+' & '+f"[{num(p['tpr_ci95_cond'][0])}, {num(p['tpr_ci95_cond'][1])}]"+r' \\')
(R/'tables/hypothetical_intervals.tex').write_text(longtable(r'Point / detector & Hypothetical FPR CI & Hypothetical TPR CI',r'p{6cm}rr',rows,'K03 and K11 hypothetical intervals only; test adjustments or training descriptions conflict with an independent-test interpretation.'),encoding='utf8')
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
