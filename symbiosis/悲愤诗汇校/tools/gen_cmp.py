import base64,io,json,re
from PIL import Image
exec(open('cmp9333.py').read().split('CW=')[0])   # gives items
pg=lambda f:int(re.search(r'p(\d+)',f).group(1))
groups=[('本句','zhu',[0]),('同卷確定的目旁','mu',[1,2,3]),('同卷確定的耳旁','er',[6,7,5,8,4])]
def uri(f,box,pad=0.15,H=360):
    x0,y0,x1,y1=box; w=x1-x0; h=y1-y0
    im=Image.open(f).convert('L').crop((int(x0-pad*w),int(y0-pad*h),int(x1+pad*w),int(y1+pad*h)))
    im=im.resize((int(im.width*H/im.height),H),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,'JPEG',quality=82); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
out=[]
for title,cls,idx in groups:
    figs=[]
    for k in idx:
        lab,sub,f,box=items[k]
        src,ctx=sub.split(' ',1)
        figs.append(f'<figure class="{cls}"><img src="{uri(f,box)}" alt="09333 {ctx} 之「{'眺' if k==0 else lab}」"><figcaption><b>{'眺' if k==0 else lab}</b><span>{src}「{ctx}」</span><span class="pg">第39冊 第{pg(f)}頁</span></figcaption></figure>')
    out.append(f'<div class="grp"><h3>{title}</h3><div class="figs">{"".join(figs)}</div></div>')
open('page/cmp_snippet.html','w').write('\n'.join(out)); print(sum(len(x) for x in out)/1e3,'KB')
