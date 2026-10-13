# master sequence from 09333 transcription: list of (char, size) size 1=big, 0.5=small note
import re
B='/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/wspage/bf_now.wiki'
def master(note_after_poem=True, notes=True):
    s=open(B).read(); s=re.sub(r'-\{zh:([^;]*);[^}]*\}-',r'\1',s)
    poems=re.findall(r'<poem>(.*?)</poem>',s,re.S)
    out=[]
    def add(txt):
        for part in re.split(r'(<ref[^>]*>.*?</ref>)',txt,flags=re.S):
            m=re.match(r'<ref group="([^"]+)">(.*?)</ref>',part,re.S)
            if m:
                if m.group(1)=='李賢注' and notes:
                    for c in m.group(2):
                        if '㐀'<=c<='鿿' or ord(c)>0x20000: out.append((c,0.5))
                continue
            for c in part:
                if '㐀'<=c<='鿿' or ord(c)>0x20000: out.append((c,1))
    add(poems[0]); 
    for c in '其二章曰': out.append((c,1))
    add(poems[1])
    return out
if __name__=='__main__':
    m=master(); print(len(m), ''.join(c for c,_ in m)[:80])
