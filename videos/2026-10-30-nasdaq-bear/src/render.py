import sys,json
from playwright.sync_api import sync_playwright
base=sys.argv[1]; s=json.load(open(sys.argv[2]))
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1080,'height':1350}); pg.goto(f'file://{base}/cierre.html'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300); pg.screenshot(path=base+'/../capas/cierre.png')
    pg=b.new_page(viewport={'width':1080,'height':330}); pg.goto(f'file://{base}/header.html'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    r=pg.evaluate("()=>[...document.querySelectorAll('.st span,#s')].map(e=>({t:e.textContent,ov:e.scrollWidth>e.clientWidth+1,w:e.getBoundingClientRect().width}))"); print(r)
    last=None
    for i in range(len(s['cnt'])):
        vals=(s['cnt'][i],s['med'][i],s['wip'][i])
        if vals!=last:
            pg.evaluate("v=>{document.getElementById('v1').textContent=v[0];document.getElementById('v2').textContent='−'+v[1].toFixed(1)+'%';document.getElementById('v3').textContent='$'+v[2].toFixed(1)+'T'}",vals)
            pg.screenshot(path=base+f'/../capas/h-{i:04d}.png',omit_background=True); last=vals; lastfile=f'h-{i:04d}.png'
        else:
            import shutil; shutil.copy(base+'/../capas/'+lastfile, base+f'/../capas/h-{i:04d}.png')
    b.close()
