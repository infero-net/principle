import asyncio,sys
sys.path.insert(0,"/Users/xingyuanyuan/.cache/pandi-work")
from cdp import Tab
async def main():
    t=await Tab().open("about:blank")
    await t.goto(sys.argv[1]); await asyncio.sleep(10)
    txt=await t.js("document.body.innerText")
    open(sys.argv[2],'w').write(txt); print(len(txt))
    await t.close()
asyncio.run(main())
