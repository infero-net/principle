exec(open('cmp9333.py').read().split('CW=')[0])
from PIL import Image, ImageDraw, ImageFont
F=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',26)
sel=[(0,'眺'),(1,'眇'),(2,'盱'),(6,'聊'),(7,'聊'),(5,'聽'),(8,'恥')]
H=300; cells=[]
for k,lab in sel:
    _,_,f,(x0,y0,x1,y1)=items[k]; w=x1-x0; h=y1-y0
    im=Image.open(f).convert('L')
    cr=im.crop((int(x0-0.08*w),int(y0-0.12*h),int(x0+0.6*w),int(y0+0.6*h)))
    cr=cr.resize((int(cr.width*H/cr.height),H),Image.LANCZOS); cells.append((lab,cr))
W=sum(c[1].width+16 for c in cells)+16
out=Image.new('L',(W,H+50),255); d=ImageDraw.Draw(out); x=16
for lab,cr in cells: d.text((x,6),lab,font=F,fill=0); out.paste(cr,(x,44)); x+=cr.width+16
out.save('topright.png'); print(out.size)
