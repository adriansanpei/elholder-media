import sys, json
from playwright.sync_api import sync_playwright
jobs=[('parches.html',1180,1606,True),('marco.html',1080,1920,True),('cierre.html',1080,1920,False)]
chk="""()=>{const out=[];document.querySelectorAll('.txt,#titulo,#bloque,#dog,#logo,.p').forEach(e=>{const r=e.getBoundingClientRect();const p=e.parentElement.getBoundingClientRect();
out.push({el:(e.id||e.className||e.tagName)+':'+(e.textContent||'').slice(0,30),x0:Math.round(r.left),x1:Math.round(r.right),y0:Math.round(r.top),y1:Math.round(r.bottom),ovX:e.scrollWidth>e.clientWidth+1,ovY:e.scrollHeight>e.clientHeight+1,pr:Math.round(p.right)})});return out}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for f,w,h,tr in jobs:
        pg=b.new_page(viewport={'width':w,'height':h})
        pg.goto('file://'+sys.argv[1]+'/'+f); pg.wait_for_timeout(500)
        pg.evaluate("document.fonts.ready")
        print(f); [print('  ',r) for r in pg.evaluate(chk)]
        pg.screenshot(path=sys.argv[1]+'/../'+f.replace('.html','.png'),omit_background=tr)
    b.close()
