import sys, json
from playwright.sync_api import sync_playwright
W=480; S=2.25
JS=r'''
()=>{
 const st=document.createElement('style'); st.textContent="@font-face{font-family:'Inter';font-weight:100 900;src:url('../../../fonts/inter-variable-latin.woff2')}"; document.head.appendChild(st);
 const has=(e,t)=>e.textContent.includes(t);
 const smallest=(t1,t2)=>{let best=null;for(const e of document.querySelectorAll('table,div,tr,td')){if(has(e,t1)&&(!t2||has(e,t2))){if(!best||best.contains(e))best=e}}return best};
 const rm=(e)=>{let p=e.parentElement; e.remove(); while(p&&p!==document.body&&p.textContent.trim()===''&&!p.querySelector('img')){const q=p.parentElement;p.remove();p=q}};
 const ad=smallest('PATROCINIO','Kalshi.com/hedging'); if(ad) rm(ad);
 const ip=smallest('In partnership with'); if(ip) rm(ip);
 for(const i of [...document.images]) if(/kalshi/i.test(i.src)) rm(i);
 const ro=smallest('Read online'); if(ro&&ro.getBoundingClientRect().height<80) rm(ro);
}
'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':900},device_scale_factor=S)
    pg.goto('file://'+sys.argv[1],wait_until='networkidle'); pg.evaluate(JS); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(1500)
    info=pg.evaluate(r'''()=>{const y=t=>{let best=null;for(const e of document.querySelectorAll('table,div,tr,td,p,h1,h2,h3')){if(e.textContent.includes(t)){if(!best||best.contains(e))best=e}}return best?best.getBoundingClientRect():null};
      const r=o=>o?[o.top+scrollY,o.bottom+scrollY]:null;
      return {imgs:[...document.images].map(i=>{const b=i.getBoundingClientRect();return [b.top+scrollY,b.bottom+scrollY]}).filter(b=>b[1]-b[0]>60), poll:r(y('DINOS QUÉ PIENSAS')), criterio:r(y('decide con tu propio criterio')), marcador:r(y('EL MARCADOR')), gm:r(y('Gm Holder')), leer:r(y('Leer completo')), fonts:[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family)}}''')
    print(json.dumps(info)); json.dump(info,open('info.json','w'))
    pg.screenshot(path='full.png',full_page=True); b.close()
