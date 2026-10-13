# usage: nshot.py <fid> <vol> <prefix> <page>...   (vol 1-based in detail rows order)
import asyncio, sys, json, base64
sys.path.insert(0, "/Users/xingyuanyuan/.cache/pandi-work")
from cdp import Tab
D="/Users/xingyuanyuan/.claude/jobs/b0034877/tmp/hj/"
import os
CX,CY,CW,CH=[int(v) for v in os.environ.get("CLIP","290,105,860,700").split(",")]
async def main():
    fid, vol, pre = sys.argv[1], int(sys.argv[2]), sys.argv[3]; pages=[int(x) for x in sys.argv[4:]]
    rows=[r for r in json.load(open(D+f"d_{fid}.json"))['rows'] if r[0].startswith('第')]
    url=rows[vol-1][1]
    t = await Tab().open("about:blank")
    await t.cmd("Emulation.setDeviceMetricsOverride", width=1400, height=1000, deviceScaleFactor=2, mobile=False)
    await t.goto(url); await asyncio.sleep(14)
    fr = await t.cmd("Page.getFrameTree")
    child = fr["frameTree"]["childFrames"][0]["frame"]["id"]
    w = await t.cmd("Page.createIsolatedWorld", frameId=child); ctx = w["executionContextId"]
    async def fjs(e):
        r = await t.cmd("Runtime.evaluate", expression=e, contextId=ctx, returnByValue=True, awaitPromise=True)
        return r.get("result", {}).get("value")
    print(rows[vol-1][0], "total", await fjs("(document.body.innerText.match(/\\/\\s*\\d+/)||[''])[0]"))
    for p in pages:
        await fjs(f"(()=>{{const i=document.querySelector('input#pageNumber')||document.querySelector('input'); i.value='{p}'; i.dispatchEvent(new KeyboardEvent('keydown',{{key:'Enter',keyCode:13,bubbles:true}})); i.dispatchEvent(new Event('change',{{bubbles:true}})); return i.id}})()"); await asyncio.sleep(4)
        r = await t.cmd("Page.captureScreenshot", format="png", clip={"x":CX,"y":CY,"width":CW,"height":CH,"scale":1})
        open(D + f"{pre}p{p}.png", "wb").write(base64.b64decode(r["data"])); print("shot", p)
    await t.close()
asyncio.run(main())
