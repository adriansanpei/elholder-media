import sys, json, math, os
from playwright.sync_api import sync_playwright
base=sys.argv[1]; out=sys.argv[2]; os.makedirs(out,exist_ok=True)
data=json.load(open(base+'/series.json'))
FPS=30; T_MAIN=15.5; START=0.4; END=12.4
only=[float(x) for x in sys.argv[3:]]
def prog(t):
    if t<=START: return 0.0
    if t>=END: return 31.0
    u=(t-START)/(END-START); u=0.5-0.5*math.cos(math.pi*u); return 31.0*u
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto(f'file://{base}/cierre.html'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300); pg.screenshot(path=out+'/cierre.png')
    pg.goto(f'file://{base}/anim.html'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    pg.evaluate("d=>{DATA=d}",data)
    frames=[int(t*FPS) for t in only] if only else range(int(T_MAIN*FPS))
    for i in frames:
        d=prog(i/FPS); pg.evaluate("d=>draw(d)",d)
        pg.screenshot(path=f'{out}/{i:04d}.png')
    b.close()
