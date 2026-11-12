import sys, re
src=open('shot.py').read()
JS=re.search(r"JS=r'''(.*?)'''",src,re.S).group(1)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':480,'height':900},device_scale_factor=2.25)
    pg.goto('file://'+sys.argv[1],wait_until='networkidle'); pg.evaluate(JS)
    r=pg.evaluate(r'''()=>{let a=[...document.querySelectorAll('a')].find(x=>x.textContent.trim()==='Leer completo'); let t=a.closest('table'); const h=t.getBoundingClientRect().height; t.remove();
      let best=null;for(const e of document.querySelectorAll('table,div,tr,td')){if(e.textContent.includes('EL MARCADOR')){if(!best||best.contains(e))best=e}}
      return [h,(best.getBoundingClientRect().top+scrollY)]}''')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(800); print(r)
    pg.screenshot(path='cover-full.png',full_page=True); b.close()
