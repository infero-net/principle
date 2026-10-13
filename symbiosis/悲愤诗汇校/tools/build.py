import json, base64, io, html
from PIL import Image
from targets import T
from seq import master
D='/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/'
EDS=[
 ('bn','百衲本','影宋紹興本','商務印書館百衲本影印（識典古籍）','https://www.shidianguji.com/book/LS0003/chapter/1j7lpp3blt8ai_251','第45—51頁','九行十六字'),
 ('09333','國圖 09333','嘉定元年（1208）','卷八十四配蔡琪一經堂本（國圖）','http://read.nlc.cn/OutOpenBook/OpenObjectBook?aid=892&bid=304498.0','第39冊 第53—56頁','八行十六字'),
 ('08656','國圖 08656','南宋 白鷺洲書院','白鷺洲書院刻本（國圖）','http://read.nlc.cn/OutOpenBook/OpenObjectBook?aid=892&bid=304783.0','第76冊 第27—30頁','八行十六字'),
 ('08657','國圖 08657','宋刻元修','宋刻元修本（國圖）','http://read.nlc.cn/OutOpenBook/OpenObjectBook?aid=892&bid=306947.0','第38冊 第18—20頁','十行十九字'),
 ('bj','北監本','萬曆（1595—1606）','北京國子監刻本（識典古籍）','https://www.shidianguji.com/book/HY2027/chapter/1knxmsomusumk','卷一百十四','十行二十一字'),
 ('jg','汲古閣本','崇禎（1628—1644）','毛氏汲古閣刻本（識典古籍）','https://www.shidianguji.com/book/HY2998/chapter/1kvp7vwfvos9x','列女傳第七十四','十二行二十五字'),
 ('wz','五洲同文本','光緒（1903）','武英殿本系，五洲同文書局石印（識典古籍）','https://www.shidianguji.com/book/CADAL01027400/chapter/1l45dfz42a69g','卷一百十四','十行二十一字'),
 ('ky','京大藏本','年代待核','《日本京都大學藏珍稀漢籍十一種》冊十六影印（袁行遠拍照）','','第374—376頁','面十四至十五行，行二十六字'),
]
NOTE={
'a01':'𦍑（羊下作人）/ 羌','a02':'𢧵（左雀右戈）/ 截','a03':'牚 / 撐','a04':'懸 / 縣','a05':'逈 / 迥','a06':'㝠 / 冥','a07':'機 / 幾',
'a08':'捶 / 棰','a10':'戹 / 厄','a12':'已 / 己','a14':'匈 / 胸','a15':'從 / 縱','a16':'怚 / 怛','a17':'眺（右上封口是目旁，似聎）',
'a19':'託 / 托','a20':'勗 / 勖，厲 / 勵','b01':'祐 / 祜','b04':'㝠 / 冥','b05':'李賢注：瞑 / 䏃','b07':'歳 / 歲',
'b08':'扄 / 扃','b10':'胡 / 明','b11':'冷泠 / 泠泠','b12':'匈 / 胸','b13':'號 / 啼','b14':'耳 / 目','b15':'徒 / 走',
}
m=master(); s=''.join(c for c,_ in m)
def ctx(find,off,ln):
    i=s.find(find); a=i+off
    return s[max(0,a-2):a], s[a:a+ln], s[a+ln:a+ln+2]
def img64(path,maxh=300):
    im=Image.open(path).convert('RGB')
    if im.height>maxh: im=im.resize((round(im.width*maxh/im.height),maxh),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,'JPEG',quality=82,optimize=True); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
rows=[]
for tid,label,find,off,ln in T:
    pre,tg,post=ctx(find,off,ln)
    cells=[img64(D+f'crops/{e[0]}_{tid}_mk.png') for e in EDS]
    clean=[img64(D+f'crops/{e[0]}_{tid}.png',maxh=600) for e in EDS]
    rows.append(dict(id=tid,pre=pre,tg=tg,post=post,note=NOTE.get(tid,''),poem=1 if tid[0]=='a' else 2,cells=cells,clean=clean))
json.dump(dict(eds=[dict(k=e[0],name=e[1],date=e[2],desc=e[3],url=e[4],where=e[5],fmt=e[6]) for e in EDS],rows=rows),open(D+'page/data.json','w'),ensure_ascii=False)
print(len(rows), sum(len(c) for r in rows for c in r['cells']+r['clean'])/1e6,'MB')
