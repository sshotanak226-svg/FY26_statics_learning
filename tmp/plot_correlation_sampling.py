from pathlib import Path
import sys
sys.path.insert(0,str(Path('tmp/statistics-plot-deps').resolve()))
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.ndimage import gaussian_filter1d
from scipy.stats import t,kstest,skew

out=Path('tmp/correlation-sampling');out.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(20261025)
n=20;reps=100000
a=rng.normal(size=(reps,n));b=rng.normal(size=(reps,n))
a-=a.mean(axis=1,keepdims=True);b-=b.mean(axis=1,keepdims=True)
font=FontProperties(fname='C:/Windows/Fonts/meiryo.ttc')
plt.rcParams.update({'font.size':18,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#142d39','xtick.color':'#52636b','ytick.color':'#52636b','axes.edgecolor':'#aabac8'})
fig,ax=plt.subplots(figsize=(8.0,4.8),dpi=180)
report=[]
for rho,color in [(0.0,'#1467b3'),(0.5,'#bd6827'),(0.8,'#087f78')]:
 y=rho*a+np.sqrt(1-rho*rho)*b
 r=(a*y).sum(axis=1)/np.sqrt((a*a).sum(axis=1)*(y*y).sum(axis=1))
 hist,edges=np.histogram(r,bins=160,range=(-1,1),density=True)
 density=gaussian_filter1d(hist,1.4,mode='constant');x=(edges[:-1]+edges[1:])/2
 ax.plot(x,density,color=color,lw=2.6,label=rf'$\rho={rho:.1f}$')
 report.append({'rho':rho,'mean_r':float(r.mean()),'sd_r':float(r.std()),'skewness_r':float(skew(r))})
 if rho==0:
  null_t=np.sqrt(n-2)*r/np.sqrt(1-r*r)
  ks=kstest(null_t,t(n-2).cdf).statistic
  assert ks<0.01
  report[-1]['null_t_ks_distance']=float(ks)
ax.set_xlim(-1,1);ax.set_ylim(0,6.5)
ax.set_xticks([-1,-.5,0,.5,1]);ax.set_yticks([0,2,4,6])
ax.set_xlabel('標本相関 r',fontproperties=font,fontsize=18)
ax.set_ylabel('確率密度',fontproperties=font,fontsize=18)
ax.grid(axis='y',color='#dde5ed',linewidth=.7)
ax.legend(frameon=False,loc='upper left',fontsize=18)
fig.tight_layout(pad=.7)
fig.savefig(out/'r-distributions.png',facecolor='white')
plt.close(fig)
(out/'simulation.json').write_text(json.dumps({'n':n,'samples_per_rho':reps,'seed':20261025,'results':report},indent=2),encoding='utf-8')
print(json.dumps({'chart':str(out/'r-distributions.png'),'n':n,'samples_per_rho':reps,'results':report}))
