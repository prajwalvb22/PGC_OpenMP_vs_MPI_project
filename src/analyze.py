import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d=pd.read_csv('results/local_results.csv')
d=d.rename(columns={'compute_s':'t'})   # MPI: total (scatter+compute+reduce); seq/omp: compute
g=d.groupby(['mode','N','model','p']).agg(t=('t','mean'),sd=('t','std'),comm=('comm_s','mean'),io=('io_s','mean')).reset_index()
seq=g[g.model=='sequential'].set_index(['mode','N']).t
g['seq']=[seq[(m,n)] for m,n in zip(g['mode'],g['N'])]
g['speedup']=g.seq/g.t; g['eff']=g.speedup/g.p
g['localcomp']=np.where(g.model=='mpi',g.t-g.comm,g.t)
g.to_csv('results/summary_stats.csv',index=False)
FULL=47248723
BLUE,ORG,AQ,INK,GRID='#2a78d6','#eb6834','#1baf7a','#0b0b0b','#e6e5e1'
plt.rcParams.update({'font.size':12,'axes.edgecolor':'#9a9890','axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':GRID,'axes.axisbelow':True,'figure.facecolor':'white','font.family':'DejaVu Sans'})
mn={0:'Mode 0: light (stats + histogram)',1:'Mode 1: heavy (adds log statistics)'}
P=[1,2,4,8,12]
def sub(m,model,N=FULL): return g[(g['mode']==m)&(g.model==model)&(g.N==N)].sort_values('p')
def two(fn,name,ylabel,ideal=None,log=False):
    f,ax=plt.subplots(1,2,figsize=(11,4.4))
    for m,a in zip([0,1],ax):
        o,mp=sub(m,'openmp'),sub(m,'mpi')
        a.errorbar(o.p,fn(o),yerr=o.sd/(1 if fn is None else 1) if False else None,marker='o',color=BLUE,lw=2,label='OpenMP')
        a.plot(mp.p,fn(mp),marker='s',color=ORG,lw=2,label='MPI')
        if ideal=='speed': a.plot(P,P,'--',color='#9a9890',lw=1.5,label='Ideal')
        if ideal=='eff': a.axhline(1,ls='--',color='#9a9890',lw=1.5,label='Ideal')
        if ideal=='seq': a.axhline(seq[(m,FULL)],ls='--',color='#9a9890',lw=1.5,label='Sequential')
        a.set_xticks(P); a.set_xlabel('Threads / processes'); a.set_title(mn[m],fontsize=12,loc='left'); a.set_ylabel(ylabel)
        if log: a.set_yscale('log')
    ax[0].legend(frameon=False); f.tight_layout(); f.savefig(f'graphs/{name}.png',dpi=200); plt.close(f)
two(lambda x:x.t,'g1_time','Time (s), N = 47.2 M',ideal='seq')
two(lambda x:x.speedup,'g2_speedup','Speedup vs sequential',ideal='speed')
two(lambda x:x.eff,'g3_efficiency','Efficiency (speedup / workers)',ideal='eff')
# 4 MPI compute vs comm stacked
f,ax=plt.subplots(1,2,figsize=(11,4.4))
for m,a in zip([0,1],ax):
    mp=sub(m,'mpi'); x=np.arange(len(P))
    a.bar(x,mp.localcomp,0.6,color=BLUE,label='Local compute',edgecolor='white',linewidth=2)
    a.bar(x,mp.comm,0.6,bottom=mp.localcomp,color=ORG,label='Communication',edgecolor='white',linewidth=2)
    a.axhline(seq[(m,FULL)],ls='--',color='#9a9890',lw=1.5,label='Sequential')
    a.set_xticks(x); a.set_xticklabels(P); a.set_xlabel('MPI processes'); a.set_ylabel('Time (s)'); a.set_title(mn[m],fontsize=12,loc='left')
ax[0].legend(frameon=False); f.tight_layout(); f.savefig('graphs/g4_mpi_breakdown.png',dpi=200); plt.close(f)
# 5 time vs N at p=8
f,ax=plt.subplots(1,2,figsize=(11,4.4))
Ns=sorted(g.N.unique())
for m,a in zip([0,1],ax):
    for model,p,c,lab,mk in [('sequential',1,AQ,'Sequential','^'),('openmp',8,BLUE,'OpenMP (8 threads)','o'),('mpi',8,ORG,'MPI (8 processes)','s')]:
        s=g[(g['mode']==m)&(g.model==model)&(g.p==p)].sort_values('N'); a.plot(s.N/1e6,s.t,marker=mk,color=c,lw=2,label=lab)
    a.set_xscale('log'); a.set_yscale('log'); a.set_xlabel('Dataset size (million records)'); a.set_ylabel('Time (s)'); a.set_title(mn[m],fontsize=12,loc='left')
    a.set_xticks([1,5,10,25,47.2]); a.set_xticklabels(['1','5','10','25','47.2'])
ax[0].legend(frameon=False); f.tight_layout(); f.savefig('graphs/g5_time_vs_size.png',dpi=200); plt.close(f)
# 6 speedup vs N at p=8
f,ax=plt.subplots(1,2,figsize=(11,4.4))
for m,a in zip([0,1],ax):
    for model,c,lab,mk in [('openmp',BLUE,'OpenMP (8 threads)','o'),('mpi',ORG,'MPI (8 processes)','s')]:
        s=g[(g['mode']==m)&(g.model==model)&(g.p==8)].sort_values('N'); a.plot(s.N/1e6,s.speedup,marker=mk,color=c,lw=2,label=lab)
    a.axhline(1,ls='--',color='#9a9890',lw=1.5,label='Break-even (1x)'); a.set_xscale('log'); a.set_xticks([1,5,10,25,47.2]); a.set_xticklabels(['1','5','10','25','47.2'])
    a.set_xlabel('Dataset size (million records)'); a.set_ylabel('Speedup vs sequential'); a.set_title(mn[m],fontsize=12,loc='left')
ax[0].legend(frameon=False); f.tight_layout(); f.savefig('graphs/g6_speedup_vs_size.png',dpi=200); plt.close(f)
pd.set_option('display.width',200)
F=g[g.N==FULL]
print(F.pivot_table(index=['mode','model','p'],values=['t','sd','comm','localcomp','speedup','eff']).round(3))
print(g[(g.p.isin([1,8]))&(g.N<FULL)&(g.model!='sequential')][['mode','N','model','p','t','speedup']].round(3).to_string())
