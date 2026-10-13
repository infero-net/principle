# colcenters.py ed : detect per-column x centers for each half and store as 6th element of halves
import sys, json, numpy as np
from PIL import Image
from scipy.signal import find_peaks
D='/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/'
ed=sys.argv[1]; cfg=json.load(open(D+f'cfg_{ed}.json')); nc=cfg['ncols']
for hv in cfg['halves']:
    f,x0,y0,x1,y1=hv[:5]; cw=(x1-x0)/nc
    a=np.array(Image.open(D+f).convert('L')).astype(float)
    xa=int(x0+cw*0.25); xb=int(x1-cw*0.25)
    ink=(a[int(y0):int(y1),xa:xb]<110).mean(0)
    sm=np.convolve(ink,np.ones(int(cw*0.35))/int(cw*0.35),'same')
    pk,_=find_peaks(sm,distance=int(cw*0.75),prominence=0.015); pk=pk+xa
    # assign peaks to columns via model centers; fit offset+scale
    model=np.array([x1-(c-0.5)*cw for c in range(1,nc+1)])
    best=None
    for dx in np.arange(-cw*0.5,cw*0.5,1):
        for sc in np.arange(0.95,1.05,0.005):
            m=x1+dx-(np.arange(1,nc+1)-0.5)*cw*sc
            d=np.min(np.abs(pk[:,None]-m[None,:]),axis=1) if len(pk) else np.array([0])
            err=np.sum(np.minimum(d,cw*0.3)**2)
            if best is None or err<best[0]: best=(err,m)
    m=best[1]; xc=[]
    for c in range(nc):
        near=[p for p in pk if abs(p-m[c])<cw*0.22]
        xc.append(float(near[0]) if near else float(m[c]))
    if len(hv)>5: hv[5]=xc
    else: hv.append(xc)
    print(f,[int(v) for v in xc])
json.dump(cfg,open(D+f'cfg_{ed}.json','w'),ensure_ascii=False)
