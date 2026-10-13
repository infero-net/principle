import sys, json, re, math, os, numpy as np
sys.path.insert(0,'/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj')
from PIL import Image, ImageDraw
from seq import master
from targets import T
sys.path.insert(0,'/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/v8')
from detect import load
D='/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/'
SF=float(os.environ.get('SF','0.62'))
# per page: column centers (top x at yA, bottom x at yB), text top/bottom functions of x
P={
 'P1':dict(photo='111235',yA=800,yB=3600,
   top=[400,558,700,833,967,1100,1250,1400,1542,1683,1825,1967,2100,2233,2367][::-1],
   bot=[375,525,658,800,942,1092,1242,1392,1533,1675,1825,1967,2108,2242,2392][::-1],
   ttop=lambda x: 635+(x-400)*(668-635)/(2367-400), tbot=lambda x: 3748+(x-375)*(3728-3748)/(2392-375)),
 'P2':dict(photo='111231',yA=850,yB=3700,
   top=[817,967,1108,1250,1417,1592,1758,1925,2083,2233,2392,2550,2700,2850][::-1],
   bot=[808,950,1092,1250,1408,1567,1733,1883,2042,2192,2342,2500,2650,2800][::-1],
   ttop=lambda x: 748+(x-817)*(798-748)/(2850-817),
   tbot=lambda x: float(np.polyval(np.polyfit([808,1883,2800],[3815,3850,3825],2),x))),
 'P3':dict(photo='111225',yA=900,yB=3650,
   top=[2425,2281,2137,1994,1856,1719,1569,1431],
   bot=[2481,2337,2200,2050,1906,1756,1600,1460],
   ttop=lambda x: 852, tbot=lambda x: 3800),
}
COLS=[('P1',5,''),('P1',6,'亂天'),('P1',7,'義師'),('P1',8,'𦍑獵'),('P1',9,'懸男'),('P1',10,'爛腐'),('P1',11,'間輒'),('P1',12,'或便'),('P1',13,'生無'),('P1',14,'多霜'),('P1',15,'窮已'),
 ('P2',1,'願骨'),('P2',2,'存亡'),('P2',3,'復有'),('P2',4,'崩五'),('P2',5,'離別'),('P2',6,'欷行'),('P2',7,'念我'),('P2',8,'宇生'),('P2',9,'對孤'),('P2',10,'寬大'),('P2',11,'賤常'),('P2',12,'患宗'),('P2',13,'路曼'),('P2',14,'常流'),
 ('P3',1,'陽精'),('P3',2,'人似'),('P3',3,'悠長'),('P3',4,'星北'),('P3',5,'彈琴'),('P3',6,'兮涕'),('P3',7,'掩耳'),('P3',8,'情心')]
def colgeom(pg,c):
    g=P[pg]; xt=g['top'][c-1]; xb=g['bot'][c-1]
    fx=lambda y: xt+(y-g['yA'])*(xb-xt)/(g['yB']-g['yA'])
    y0=g['ttop'](xt); y1=g['tbot'](xb)
    return fx,y0,y1
def layout():
    seqm=master(); s=''.join(c for c,_ in seqm)
    starts=[];p=0
    for k,(pg,c,a) in enumerate(COLS):
        if a=='': starts.append(0); continue
        m=re.compile(a).search(s,p); assert m,(pg,c,a); starts.append(m.start()); p=m.start()+1
    starts.append(len(s)); pos=[None]*len(seqm)
    for k,(pg,c,a) in enumerate(COLS):
        i0,i1=starts[k],starts[k+1]; fx,y0,y1=colgeom(pg,c)
        items=[];i=i0
        while i<i1:
            if seqm[i][1]==1: items.append(('B',i,1.0)); i+=1
            else:
                j=i
                while j<i1 and seqm[j][1]==0.5: j+=1
                items.append(('S',i,j,math.ceil((j-i)/2)*SF)); i=j
        nu=sum(it[-1] for it in items)
        if k==0: u0=19; tot=26            # P1 col5: 漢 is the 20th of 26 chars
        elif (pg,c)==('P3',8): u0=0; tot=nu+0.0; y1=y0+(nu)*((P['P3']['tbot'](0)-852)/ (22.0))  # short last column
        else: u0=0; tot=nu
        uh=(y1-y0)/tot; u=u0
        for it in items:
            if it[0]=='B':
                yy=y0+u*uh; pos[it[1]]=(pg,fx(yy+uh/2),yy,yy+uh,None)
            else:
                _,i,j,ht=it; n=j-i; half=math.ceil(n/2)
                for q in range(n):
                    sub=0 if q<half else 1; rq=q if q<half else q-half
                    yy=y0+(u+rq*SF)*uh; pos[i+q]=(pg,fx(yy),yy,yy+SF*uh,sub)
            u+=it[-1]
    return pos,s,uh
CW={'P1':142,'P2':150,'P3':142}
def crop(pos,a,b):
    pg=pos[a][0]; im=load(P[pg]['photo']).convert('RGB'); cw=CW[pg]
    boxes=[]
    for k in range(a,b+1):
        _,xc,y0,y1,sub=pos[k]
        if sub is None: boxes.append((xc-cw*0.45,y0,xc+cw*0.45,y1))
        else:
            w=cw*0.45
            boxes.append((xc-w if sub==1 else xc-0.05*w, y0, xc+0.05*w if sub==1 else xc+w, y1))
    tx0=min(b_[0] for b_ in boxes); ty0=min(b_[1] for b_ in boxes); tx1=max(b_[2] for b_ in boxes); ty1=max(b_[3] for b_ in boxes)
    rh=(ty1-ty0)/(b-a+1) if pos[a][4] is None else cw
    xc=(tx0+tx1)/2
    cx0=xc-cw*0.62; cx1=xc+cw*0.62; cy0=max(0,ty0-1.15*cw); cy1=ty1+1.15*cw
    cr=im.crop((int(cx0),int(cy0),int(cx1),int(cy1)))
    return cr,(tx0-cx0,ty0-cy0,tx1-cx0,ty1-cy0),[P[pg]['photo'],int(cx0),int(cy0),int(cx1),int(cy1)]
if __name__=='__main__':
    pos,s,_=layout(); ADJ=json.load(open(D+'v8/adj.json')) if os.path.exists(D+'v8/adj.json') else {}
    sheet=[]
    for tid,label,find,off,ln in T:
        idx=s.find(find.replace('聎','聎')); assert idx>=0,(tid,find)
        a=idx+off; b=a+ln-1
        if tid in ADJ:   # manual: [dx,dy] shift in px applied to all chars
            dx,dy=ADJ[tid][:2]
            for k in range(a,b+1):
                q=list(pos[k]); q[1]+=dx; q[2]+=dy; q[3]+=dy; pos[k]=tuple(q)
        cr,t,src=crop(pos,a,b)
        # scale to ~ the size of other editions' crops (column width ~ 140px)
        sc=140/ (CW[pos[a][0]]*1.24)
        mk=cr.copy(); ImageDraw.Draw(mk).rectangle(t,outline=(220,30,30),width=3)
        cr.save(D+f'crops/v8_{tid}.png'); mk.save(D+f'crops/v8_{tid}_mk.png')
        json.dump({'src':[src]},open(D+f'crops/v8_{tid}.json','w'))
        sheet.append((tid,mk))
    W=1600; x=0; rows=[[]]
    for it in sheet:
        if x+it[1].width+8>W: rows.append([]); x=0
        rows[-1].append(it); x+=it[1].width+8
    rh=max(m.height for _,m in sheet)+24
    out=Image.new('RGB',(W,rh*len(rows)),'white'); d=ImageDraw.Draw(out)
    for ri,row in enumerate(rows):
        x=0
        for tid,m in row: out.paste(m,(x,ri*rh+24)); d.text((x+2,ri*rh+4),tid,fill='red'); x+=m.width+8
    out.save(D+'v8/sheet_v8.png'); print(out.size)
