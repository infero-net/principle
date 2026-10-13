import json,sys
from PIL import Image, ImageDraw
from layout import layout, layout_cols, cellbox
from seq import master
from targets import T
m=master(); s=''.join(c for c,_ in m)
EDS=['bn','08657','09333','08656','bj','jg','wz']
want=sys.argv[1].split(','); outf=sys.argv[2]
pos={}
for e in EDS:
    cfg=json.load(open(f'cfg_{e}.json')); pos[e]=(cfg,layout_cols(cfg,m) if 'cols' in cfg else layout(cfg,m))
def hcrs(q):
    if q[0]=='S': return q[1],q[2],q[3],(q[5] if len(q)>5 else 1.0)
    return q[0],q[1],q[2],(q[4] if len(q)>4 else 1.0)
rows=[]
for tid,label,find,off,ln in T:
    if tid not in want: continue
    a=s.find(find)+off; b=a+ln-1
    ims=[]
    for e in EDS:
        cfg,p=pos[e]; h,c,r,sp=hcrs(p[a]); hb,cb,rb,spb=hcrs(p[b])
        f,x0,y0,x1,y1=cellbox(cfg,h,c,r,sp)
        if (hb,cb)==(h,c): _,_,_,_,y1=cellbox(cfg,h,c,rb,spb)
        im=Image.open(f).convert('RGB'); pad=(x1-x0)*0.1
        cr=im.crop((int(x0-pad),int(y0-pad),int(x1+pad),int(y1+pad)))
        cr=cr.resize((260,int(260*cr.height/cr.width))); ims.append(cr)
    rows.append((tid,ims))
H=max(max(i.height for i in ims) for _,ims in rows)
out=Image.new('RGB',(50+7*270,len(rows)*(H+20)),'white'); d=ImageDraw.Draw(out)
for r,(tid,ims) in enumerate(rows):
    d.text((2,r*(H+20)+40),tid,fill='red')
    for k,(e,im) in enumerate(zip(EDS,ims)): d.text((50+k*270,r*(H+20)),e,fill='blue'); out.paste(im,(50+k*270,r*(H+20)+14))
out.save(outf); print(out.size)
