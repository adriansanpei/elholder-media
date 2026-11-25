import os
from playwright.sync_api import sync_playwright
H='file://'+os.path.abspath('src/slide.html')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i in range(1,13):
        pg.goto(H+f'#{i}'); pg.reload(); pg.wait_for_timeout(400)
        r=pg.evaluate("(()=>{const t=document.querySelector('#s%d .t').getBoundingClientRect();const im=document.querySelector('#s%d .img');return [Math.round(t.top),Math.round(t.bottom),im?Math.round(im.getBoundingClientRect().bottom):0]})()"%(i,i)); print(i,r)
        pg.screenshot(path=f'slide-{i}.jpg',type='jpeg',quality=92)
    b.close()
