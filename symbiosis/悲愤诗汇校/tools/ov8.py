import sys
from PIL import Image, ImageDraw, ImageFont
EDS=['bn','09333','08656','08657','bj','jg','wz','ky']
ids=sys.argv[1].split(','); out=sys.argv[2]; Wc=int(sys.argv[3]) if len(sys.argv)>3 else 130
f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18)
rows=[]
for t in ids:
    ims=[]
    for e in EDS:
        im=Image.open(f'crops/{e}_{t}_mk.png').convert('RGB'); im=im.resize((Wc,int(Wc*im.height/im.width)),Image.LANCZOS); ims.append(im)
    rows.append((t,ims))
H=[max(i.height for i in ims) for _,ims in rows]
o=Image.new('RGB',(60+8*(Wc+10),sum(h+26 for h in H)+10),'white'); d=ImageDraw.Draw(o); y=0
for (t,ims),h in zip(rows,H):
    d.text((4,y+40),t,fill='red',font=f)
    for k,(e,im) in enumerate(zip(EDS,ims)): d.text((60+k*(Wc+10),y+2),e,fill='blue',font=f); o.paste(im,(60+k*(Wc+10),y+24))
    y+=h+26
o.save(out); print(o.size)
