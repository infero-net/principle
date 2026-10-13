import json
from PIL import Image, ImageDraw, ImageFont
from layout import layout_cols, cellbox
from seq import master
m=master(); s=''.join(c for c,_ in m)
cfg=json.load(open('cfg_09333.json')); p=layout_cols(cfg,m)
def poem(i):
    q=p[i]; f,x0,y0,x1,y1=cellbox(cfg,q[0],q[1],q[2],q[4] if len(q)>4 else 1.0); return f,(x0,y0,x1,y1)
items=[  # (label, sub, file, box)
 ('聎','悲憤詩 登高遠聎望',*poem(488)),
 ('眇','悲憤詩 山谷眇兮',*poem(579)),
 ('盱','曹娥傳 父盱能絃歌','hv39p44.png',(712,1050,792,1119)),
 ('目','女誡 目無邪視','hv39p39.png',(1488,305,1572,369)),
 ('耳','女誡 耳無塗聽','hv39p39.png',(1573,1098,1657,1162)),
 ('聽','女誡 耳無塗聽','hv39p39.png',(1488,236,1572,303)),
 ('聊','周郁妻 亦何聊哉','hv39p32.png',(1508,903,1572,985)),
 ('聊','悲憤詩 何聊賴',*poem(513)),
 ('恥','曹世叔妻 有恥動靜','hv39p38.png',(1508,1098,1567,1167)),
]
CW=230; pad=0.18
F=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',30); f2=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',17)
cells=[]
for lab,sub,f,(x0,y0,x1,y1) in items:
    im=Image.open(f).convert('RGB'); w=x1-x0; h=y1-y0
    cr=im.crop((int(x0-pad*w),int(y0-pad*h),int(x1+pad*w),int(y1+pad*h)))
    k=CW/cr.width; cells.append((lab,sub,cr.resize((CW,int(cr.height*k)),Image.LANCZOS)))
H=max(c[2].height for c in cells)
n=len(cells); per=5; rows=(n+per-1)//per
out=Image.new('RGB',(per*(CW+16)+16,rows*(H+80)+10),'white'); d=ImageDraw.Draw(out)
for k,(lab,sub,im) in enumerate(cells):
    r,c=divmod(k,per); x=16+c*(CW+16); y=10+r*(H+80)
    col=(180,20,20) if lab=='聎' else ((20,90,170) if k in (1,2,3) else (40,120,40))
    d.text((x,y),lab,font=F,fill=col); d.text((x+40,y+10),sub,font=f2,fill=(90,90,90))
    out.paste(im,(x,y+42))
out.save('cmp9333.png'); print(out.size)
