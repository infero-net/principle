import sys, json, math, os, re
import numpy as np
from PIL import Image, ImageDraw
from seq import master
from targets import T
D='/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/'
def layout(cfg, seqm):
    halves=cfg['halves']; nc=cfg['ncols']; nr=cfg['nrows']
    h,c,r=cfg['start']  # half idx, col (1=rightmost), row (1=top)
    pos=[None]*len(seqm); i=0
    def adv():
        nonlocal h,c,r
        r+=1
        if r>nr:
            r=1; c+=1
            if c>nc: c=1; h+=1
    skip={tuple(x) for x in cfg.get('skip',[])}  # {(h,c,r):n} cells to skip (blank)
    while i<len(seqm):
        while (h,c,r) in skip: adv()
        ch,sz=seqm[i]
        if sz==1:
            pos[i]=(h,c,r,None); i+=1; adv()
        else:
            j=i
            while j<len(seqm) and seqm[j][1]==0.5: j+=1
            k=i
            while k<j:
                while (h,c,r) in skip: adv()
                R=nr-r+1; n=j-k; cells=min(math.ceil(n/2),R); take=min(n,2*cells)
                for t in range(take):
                    sub=0 if t<cells else 1
                    rr=t if t<cells else t-cells
                    pos[k+t]=('S',h,c,r+rr,sub)
                for _ in range(cells): adv()
                k+=take
            i=j
    return pos

def layout_cols(cfg, seqm):
    """column-anchored layout: cfg['cols']=[[h,c,anchor],...]; first entry may have row start (cfg['start'])"""
    s=''.join(ch for ch,_ in seqm); nr=cfg['nrows']
    cols=cfg['cols']; starts=[]; p=0
    for k,(h,c,a) in enumerate(cols):
        if k==0 and a=='': starts.append(0); continue
        mm=re.compile(a).search(s,p if k else 0); assert mm,(h,c,a,p); i=mm.start(); starts.append(i); p=i+1
    starts.append(len(s))
    pos=[None]*len(seqm)
    for k,(h,c,a) in enumerate(cols):
        i0,i1=starts[k],starts[k+1]
        r0=cfg['start'][2] if k==0 else 1
        # units (float): big char = 1; a note run of n small chars = ceil(n/2)*sf (sf = small-char height in cells)
        sf=cfg.get('small_h',1.0)
        items=[];i=i0
        while i<i1:
            if seqm[i][1]==1: items.append(('B',i,1.0)); i+=1
            else:
                j=i
                while j<i1 and seqm[j][1]==0.5: j+=1
                n=j-i; items.append(('S',i,j,math.ceil(n/2)*sf)); i=j
        nu=sum(it[-1] for it in items); avail=nr-r0+1
        scale = avail/nu if (k<len(cols)-1 and nu>=avail-2) or nu>avail else 1.0
        u=0.0
        for it in items:
            rr=r0+u*scale
            if it[0]=='B': pos[it[1]]=(h,c,rr,None,scale)
            else:
                _,i,j,ht=it; n=j-i; half=math.ceil(n/2)
                for q in range(n):
                    sub=0 if q<half else 1; rq=q if q<half else q-half
                    pos[i+q]=('S',h,c,rr+rq*sf*scale,sub,sf*scale)
            u+=it[-1]
    return pos
def cellbox(cfg,h,c,r,span=1.0):
    hv=cfg['halves'][h]; f,x0,y0,x1,y1=hv[:5]; nc=cfg['ncols']; nr=cfg['nrows']
    cw=(x1-x0)/nc; rh=(y1-y0)/nr
    if len(hv)>5:
        xc=hv[5]; xs=sorted(xc); cw=float(np.median(np.diff(xs[::-1]) if False else np.abs(np.diff(xs))))
        return f, xc[c-1]-cw/2, y0+(r-1)*rh, xc[c-1]+cw/2, y0+(r-1+span)*rh
    return f, x1-c*cw, y0+(r-1)*rh, x1-(c-1)*cw, y0+(r-1+span)*rh

def crop_target(cfg,pos,a,b):
    groups={}
    order=[]
    for k in range(a,b+1):
        q=pos[k]
        if q[0]=='S':
            _,h,c,r,sub=q[:5]; sp=q[5] if len(q)>5 else 1.0; f,x0,y0,x1,y1=cellbox(cfg,h,c,r,sp); w=(x1-x0)/2
            box=(x1-w*(sub+1)-(0.1*w if sub==0 else 0),y0,x1-w*sub+(0.1*w if sub==1 else 0),y1)
        else:
            h,c,r=q[:3]; sp=q[4] if len(q)>4 else 1.0; f,*box=cellbox(cfg,h,c,r,sp)
        if (h,c) not in groups: groups[(h,c)]=[]; order.append((h,c))
        groups[(h,c)].append((f,box))
    parts=[];srcs=[]
    for g in order:
        h,c=g; f=groups[g][0][0]
        _,X0,_,X1,_=cellbox(cfg,h,c,1)
        tx0=min(x[1][0] for x in groups[g]); ty0=min(x[1][1] for x in groups[g]); tx1=max(x[1][2] for x in groups[g]); ty1=max(x[1][3] for x in groups[g])
        rh=(cfg['halves'][h][4]-cfg['halves'][h][2])/cfg['nrows']
        im=Image.open(D+f).convert('RGB')
        cx0=X0-0.12*(X1-X0); cx1=X1+0.12*(X1-X0)
        cy0=max(0,ty0-1.15*rh); cy1=min(im.height,ty1+1.15*rh)
        cr=im.crop((int(cx0),int(cy0),int(cx1),int(cy1)))
        parts.append((cr,(tx0-cx0,ty0-cy0,tx1-cx0,ty1-cy0))); srcs.append([f,int(cx0),int(cy0),int(cx1),int(cy1)])
    gap=10
    W=sum(p[0].width for p in parts)+gap*(len(parts)-1); H=max(p[0].height for p in parts)
    clean=Image.new('RGB',(W,H),'white'); mk=Image.new('RGB',(W,H),'white')
    x=W
    for cr,t in parts:   # first part on the right (reading order)
        x-=cr.width; clean.paste(cr,(x,0)); m=cr.copy(); ImageDraw.Draw(m).rectangle(t,outline=(220,30,30),width=2); mk.paste(m,(x,0)); x-=gap
    return clean,mk,srcs
def run(ed):
    cfg=json.load(open(D+f'cfg_{ed}.json'))
    seqm=master(); s=''.join(ch for ch,_ in seqm)
    for k,v in cfg.get('subst',{}).items(): pass
    pos=layout_cols(cfg,seqm) if 'cols' in cfg else layout(cfg,seqm)
    os.makedirs(D+'crops',exist_ok=True)
    sheet=[]
    for tid,label,find,off,ln in T:
        idx=s.find(find); assert idx>=0,(tid,find)
        a=idx+off; b=a+ln-1
        clean,mk,srcs=crop_target(cfg,pos,a,b)
        clean.save(D+f'crops/{ed}_{tid}.png'); mk.save(D+f'crops/{ed}_{tid}_mk.png')
        json.dump({'src':srcs},open(D+f'crops/{ed}_{tid}.json','w'))
        sheet.append((tid,label,mk))
    # contact sheet
    rowh=max(cimg.height for _,_,cimg in sheet)+30; W=1500
    rows=[[]]; x=0
    for it in sheet:
        if x+it[2].width+8>W: rows.append([]); x=0
        rows[-1].append(it); x+=it[2].width+8
    out=Image.new('RGB',(W,rowh*len(rows)),'white'); d=ImageDraw.Draw(out)
    for ri,row in enumerate(rows):
        x=0
        for tid,label,cimg in row: out.paste(cimg,(x,ri*rowh+30)); d.text((x+2,ri*rowh+2),tid,fill='red'); x+=cimg.width+8
    out.save(D+f'sheet_{ed}.png'); print('ok',ed,out.size)
if __name__=='__main__': run(sys.argv[1])
