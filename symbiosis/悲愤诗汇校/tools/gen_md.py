import os
from build import EDS, NOTE, ctx
from targets import T
R=os.path.expanduser('~/Projects/principle/symbiosis/悲愤诗汇校/')
def head():
    cells=[]
    for k,name,date,desc,url,where,fmt in EDS:
        n=f'[{name}]({url})' if url else name
        cells.append(f'{n}<br><sub>{date}<br>{fmt}</sub>')
    return '| 字 | '+' | '.join(cells)+' |\n|'+'---|'*(len(EDS)+1)+'\n'
def row(tid,find,off,ln):
    pre,tg,post=ctx(find,off,ln); note=NOTE.get(tid,'')
    c0=f'{pre}**{tg}**{post}'+(f'<br><sub>{note}</sub>' if note else '')+f'<br><sub>{tid}</sub>'
    cs=[f'<a href="images/crops/{tid}_{e[0]}.jpg"><img src="images/crops_mk/{tid}_{e[0]}.jpg" height="110" alt="{e[1]}截圖 {tid}"></a>' for e in EDS]
    return '| '+c0+' | '+' | '.join(cs)+' |\n'
out='''# 《悲憤詩》八本對照

《後漢書·列女傳·董祀妻》蔡琰《悲憤詩》關鍵字，八個本子的影印截圖逐字對照。每行一個字，每列一個本子，從左到右大致按刊刻年代排，年代未定的京大藏本排在最後。紅框是要看的字，上下各留一字。點圖看不帶紅框的大圖。表頭點本子名去原書。

結論、判據和做法見 [README](README.md)；09333 同卷目旁與耳旁的比對見 README 第三節，京大藏本的同本比對見 README 第四節。

## 其一（五言）

'''+head()+''.join(row(t,f,o,l) for t,_,f,o,l in T if t[0]=='a')+'''
## 其二（騷體）

'''+head()+''.join(row(t,f,o,l) for t,_,f,o,l in T if t[0]=='b')+'''
---

截圖方法、定位誤差與各本出處見 [README](README.md)。國圖三本取自中華古籍資源庫，百衲本、北監本、汲古閣本、五洲同文本取自識典古籍，京大藏本是袁行遠拍的影印本書頁。
'''
open(R+'八本對照.md','w').write(out); print(len(out))
