import os
from playwright.sync_api import sync_playwright
H='file://'+os.path.abspath('src/slide.html')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i in range(1,9):
        pg.goto(H+f'#{i}'); pg.reload(); pg.wait_for_timeout(400)
        top=pg.evaluate("document.querySelector('#s%d .t').getBoundingClientRect().top"%i); print(i,round(top))
        pg.screenshot(path=f'slide-{i}.jpg',type='jpeg',quality=93)
    b.close()
