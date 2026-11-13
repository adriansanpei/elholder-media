import asyncio,glob,os,sys
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1350})
        for f in sorted(glob.glob(D+'/src/slide-*.html')):
            n=os.path.basename(f)[:-5]
            if len(sys.argv)>1 and n[-2:] not in sys.argv[1:]: continue
            await pg.goto('file://'+f);await pg.wait_for_timeout(600)
            await pg.screenshot(path=f'{D}/{n}.jpg',type='jpeg',quality=92)
        await b.close()
asyncio.run(m())
