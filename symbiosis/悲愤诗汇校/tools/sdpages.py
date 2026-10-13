# sdpages.py <chapter_url> <outprefix> <page>...  : go to pages in 识典 reader, collect signed page-image urls, download them
import asyncio, json, sys, re, urllib.request
sys.path.insert(0, "/Users/xingyuanyuan/.cache/pandi-work")
from cdp import Tab
D="/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/sd/"
async def main():
    url, pre = sys.argv[1], sys.argv[2]; pages=[int(x) for x in sys.argv[3:]]
    t = await Tab().open("about:blank")
    await t.cmd("Emulation.setDeviceMetricsOverride", width=1400, height=1000, deviceScaleFactor=1, mobile=False)
    await t.goto(url); await asyncio.sleep(3)
    await t.js('performance.setResourceTimingBufferSize(20000)'); await asyncio.sleep(9)
    seen=set()
    async def urls():
        return json.loads(await t.js("JSON.stringify(performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('ancientlib-sign')&&n.includes('/page/')))"))
    for u in await urls(): seen.add(u)
    tot=await t.js("(document.body.innerText.match(/\\d+\\s*\\/\\s*(\\d+)/)||['',''])[1]")
    print('total pages', tot)
    out={}
    for p in pages:
        async def curp():
            v=await t.js("(document.body.innerText.match(/(\\d+)\\s*\\/\\s*\\d+/)||['',''])[1]"); return int(v) if v else None
        ok='click'
        for _ in range(200):
            c=await curp()
            if c==p: break
            x = 511 if c<p else 422; Y=907
            for typ in ("mousePressed","mouseReleased"):
                await t.cmd("Input.dispatchMouseEvent", type=typ, x=x, y=Y, button="left", clickCount=1)
            await asyncio.sleep(0.6)
        await asyncio.sleep(5)
        cur=await t.js("(document.body.innerText.match(/(\\d+)\\s*\\/\\s*\\d+/)||['',''])[1]")
        new=[u for u in await urls() if u not in seen]
        for u in new: seen.add(u)
        print(p, ok, 'cur', cur, 'new', [re.search(r'/([^/]+)\.webp',u).group(1) for u in new])
        out[p]=new
    json.dump(out,open(D+pre+'_urls.json','w'))
    await t.close()
    for p,us in out.items():
        for k,u in enumerate(us):
            fn=D+pre+'_'+re.search(r'/([^/]+)\.webp',u).group(1).split('-',1)[-1]+'.webp'
            data=urllib.request.urlopen(urllib.request.Request(u,headers={'Referer':'https://www.shidianguji.com/','User-Agent':'Mozilla/5.0'}),timeout=60).read()
            open(fn,'wb').write(data); print('saved',fn,len(data))
asyncio.run(main())
