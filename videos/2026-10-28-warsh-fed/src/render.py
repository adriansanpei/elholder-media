import sys, json
from playwright.sync_api import sync_playwright
base=sys.argv[1]; out=base+'/../capas/'
chk="""()=>[...document.querySelectorAll('.chk')].map(e=>{const r=e.getBoundingClientRect();return {t:e.textContent.slice(0,40),x0:Math.round(r.left),x1:Math.round(r.right),y0:Math.round(r.top),y1:Math.round(r.bottom),ovX:e.scrollWidth>e.clientWidth+1}})"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for f in ['titulo','fijo','marca']:
        pg.goto(f'file://{base}/{f}.html'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        print(f, pg.evaluate(chk)); pg.screenshot(path=out+f+'.png',omit_background=True)
    subs=json.load(open(base+'/subs.json'))
    pg.goto(f'file://{base}/sub.html'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i,(a,z,t) in enumerate(subs):
        pg.evaluate("t=>document.getElementById('t').innerHTML=t",t); pg.wait_for_timeout(50)
        r=pg.evaluate(chk)[0]; flag='' if (r['x0']>=48 and r['x1']<=930 and not r['ovX']) else '  <<< REVISAR'
        print(i,r['y0'],r['y1'],r['x0'],r['x1'],flag)
        pg.screenshot(path=out+f'sub-{i:02d}.png',omit_background=True)
    b.close()
