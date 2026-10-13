# tops.py ed : strip of column tops (first ~2.3 rows) for each half, labeled h:c
import sys, json
from PIL import Image, ImageDraw
from layout import cellbox
D='/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/'
ed=sys.argv[1]; cfg=json.load(open(D+f'cfg_{ed}.json'))
hs=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else range(len(cfg['halves']))
tiles=[]
for h in hs:
    f=cfg['halves'][h][0]; im=Image.open(D+f).convert('RGB')
    for c in range(1,cfg['ncols']+1):
        _,x0,y0,x1,y1=cellbox(cfg,h,c,1); rh=y1-y0
        t=im.crop((int(x0-4),int(y0-rh*0.2),int(x1+4),int(y0+rh*2.4)))
        t=t.resize((int(t.width*0.6),int(t.height*0.6))); tiles.append((f'{h}:{c}',t))
tw=max(t.width for _,t in tiles); th=max(t.height for _,t in tiles)+18
per=16; rows=(len(tiles)+per-1)//per
out=Image.new('RGB',(per*(tw+6),rows*th),'white'); d=ImageDraw.Draw(out)
for i,(lab,t) in enumerate(tiles):
    r,k=divmod(i,per); x=(per-1-k)*(tw+6); y=r*th
    out.paste(t,(x,y+18)); d.text((x+2,y+2),lab,fill='red')
out.save(D+'tops.png'); print(out.size)
