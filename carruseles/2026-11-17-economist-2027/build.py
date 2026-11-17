# Genera crops, HTML y renderiza. Uso: python3 build.py [n ...]
import os, sys
from PIL import Image, ImageFilter, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
src=Image.open('fondos/portada-economist.jpg').convert('RGB')
CIRC=(70,395,1115,1440)  # recorte cuadrado del círculo
T=[ # (titulo html, crop, texto)
("Empieza la era <span class='a'>post-Trump</span>",(385,400,835,790),
 "Tras las elecciones intermedias arranca la carrera por sucederlo. Pero no se irá en silencio: se esperan más decretos, litigios, megaobras e intervenciones militares."),
("Irán: la guerra que <span class='a'>sigue moviendo todo</span>",(700,1015,1100,1255),
 "Sin solución a la vista. El conflicto puede seguir alterando el flujo de energía, las alianzas de la región y el suministro de fertilizantes, o sea, la comida de millones."),
("El año <span class='a'>más caluroso</span>, otra vez",(85,810,345,1010),
 "2027 podría romper el récord de calor por un posible súper El Niño: sequías, incendios y olas de calor. La otra cara: las energías renovables ganan terreno."),
("IA: aceleración, riesgos y <span class='a'>rechazo</span>",(228,765,690,1012),
 "Deuda corporativa al alza y financiamiento opaco elevan el riesgo de un crash en el sector. Se suman ciberataques y el debate por empleo, energía y agua."),
("Francia vota: <span class='a'>¿Le Pen presidenta?</span>",(662,768,1068,1032),
 "Las presidenciales francesas son la cita política del año en Europa. Un triunfo de Marine Le Pen tensaría el eje Francia-Alemania y las finanzas públicas del país."),
("La deuda se pone <span class='a'>más cara</span>",(578,636,850,866),
 "Gobiernos más endeudados y bonos que pagan más interés: el costo del dinero aprieta a las economías desarrolladas y pone en duda sus finanzas públicas."),
("China y Taiwán: <span class='a'>el año marcado</span>",(395,1040,760,1200),
 "Xi Jinping habría pedido un ejército listo para tomar Taiwán en 2027. Eso no significa invasión anunciada, y los drones ya permiten a los países chicos resistir más."),
("Ozempic <span class='a'>cambia el consumo</span>",(405,850,768,1078),
 "Los medicamentos para bajar de peso mueven el gasto hacia ropa, cosméticos y fitness. Y las farmacéuticas vuelven a apostar por tratamientos de longevidad."),
("El espacio ya es <span class='a'>negocio</span>",(150,490,470,800),
 "Starship de SpaceX empezaría lanzamientos regulares de satélites. Viene la primera estación espacial privada y los centros de datos en órbita suenan más reales."),
("Hollywood busca <span class='a'>a su público</span>",(215,1165,475,1295),
 "Regresan Star Wars, Avengers y James Bond, pero hay fatiga de franquicias. Y los youtubers, con producciones baratas, ya compiten con los grandes estudios."),
]
def crop(box,name,maxw=1800):
    c=src.crop(box); s=maxw/c.width
    c=c.resize((maxw,int(c.height*s)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(3,70,2))
    c.save('fondos/'+name,quality=92)
def mini(box,name):
    c=src.crop(CIRC).resize((300,300),Image.LANCZOS).convert('RGBA')
    k=300/(CIRC[2]-CIRC[0]); d=ImageDraw.Draw(c)
    r=[(box[0]-CIRC[0])*k,(box[1]-CIRC[1])*k,(box[2]-CIRC[0])*k,(box[3]-CIRC[1])*k]
    d.rectangle(r,outline=(229,72,77,255),width=7)
    c.save('fondos/'+name)
crop(CIRC,'circulo.jpg',2000)
CSS="""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'IT';font-weight:700;src:url('../../../fonts/inter-tight-latin-700-normal.woff2')}
@font-face{font-family:'IT';font-weight:800;src:url('../../../fonts/inter-tight-latin-800-normal.woff2')}
@font-face{font-family:'IT';font-weight:900;src:url('../../../fonts/inter-tight-latin-900-normal.woff2')}
html,body{margin:0}*{box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#152F46;font-family:'IT';color:#fff}
.a{color:#4FC3F7}
#pie{position:absolute;left:64px;right:64px;bottom:52px;display:flex;align-items:center;justify-content:space-between}
#pie img{width:190px}#pie span{font-size:23px;font-weight:700;color:#9FB4C7}
"""
PIE="<div id='pie'><img src='../../../brand/logo-horizontal-transparente.png'><span>Ilustración: Cleon Peterson / The Economist</span></div>"
def trend(i,t,box,txt):
    crop(box,f'z{i:02d}.jpg'); mini(box,f'm{i:02d}.png')
    return CSS+f"""
#n{{position:absolute;left:64px;top:64px;display:flex;align-items:center;gap:18px}}
#n b{{background:#4FC3F7;color:#152F46;font-weight:900;font-size:34px;padding:10px 22px;border-radius:10px;letter-spacing:.02em}}
#n i{{font-style:normal;font-weight:800;font-size:24px;letter-spacing:.14em;color:#9FB4C7}}
#mini{{position:absolute;right:64px;top:54px;width:150px;height:150px;border-radius:50%;background:#F5F5F5 url(../fondos/m{i:02d}.png) center/88% no-repeat;box-shadow:0 0 0 5px #4FC3F7}}
h1{{position:absolute;left:64px;right:250px;top:150px;margin:0;font-weight:900;font-size:66px;line-height:1;letter-spacing:-.025em;text-transform:uppercase}}
h1 .a{{white-space:nowrap}}
#z{{position:absolute;left:64px;top:330px;width:952px;height:590px;border-radius:28px;background:#F5F5F5 url(../fondos/z{i:02d}.jpg) center/contain no-repeat;box-shadow:0 20px 50px rgba(0,0,0,.35);border:6px solid #F5F5F5}}
p{{position:absolute;left:64px;right:64px;top:962px;margin:0;font-weight:700;font-size:38px;line-height:1.26;color:#DCE6EF}}
</style></head><body>
<div id='n'><b>{i:02d} / 10</b><i>THE WORLD AHEAD 2027</i></div><div id='mini'></div>
<h1 class='chk'>{t}</h1><div id='z'></div><p class='chk'>{txt}</p>{PIE}</body></html>"""
pages={}
pages[1]=CSS+"""
#disc{position:absolute;left:225px;top:52px;width:630px;height:630px;border-radius:50%;background:#F5F5F5 url(../fondos/circulo.jpg) center/97% no-repeat;box-shadow:0 0 0 10px #4FC3F7,0 30px 80px rgba(0,0,0,.5)}
#pill{position:absolute;left:64px;top:722px;display:flex;height:60px;border-radius:6px;overflow:hidden}
#pill .l{display:flex;align-items:center;background:#E5484D;font-weight:900;font-size:25px;letter-spacing:.1em;padding:0 20px}
#pill .r{display:flex;align-items:center;background:#fff;color:#152F46;font-weight:900;font-size:25px;letter-spacing:.06em;padding:0 20px}
h1{position:absolute;left:64px;right:64px;top:806px;margin:0;font-weight:900;font-size:86px;line-height:.95;letter-spacing:-.03em;text-transform:uppercase}
p{position:absolute;left:64px;right:64px;top:1092px;margin:0;font-weight:700;font-size:38px;line-height:1.22;color:#DCE6EF}
</style></head><body><div id='disc'></div>
<div id='pill'><span class='l'>THE ECONOMIST</span><span class='r'>PORTADA 2027</span></div>
<h1 class='chk'>Así viene el <span class='a'>2027</span>, según The Economist</h1>
<p class='chk'>Las 10 señales de su famosa portada, con zoom a cada una. Desliza →</p>"""+PIE+"</body></html>"
for i,(t,box,txt) in enumerate(T,1): pages[i+1]=trend(i,t,box,txt)
pages[12]=CSS+"""
h1{position:absolute;left:64px;right:64px;top:90px;margin:0;font-weight:900;font-size:88px;line-height:.96;letter-spacing:-.03em;text-transform:uppercase}
#c{position:absolute;left:64px;right:64px;top:400px;display:flex;flex-direction:column;gap:26px}
.k{background:#1D3E5C;border-left:10px solid #4FC3F7;border-radius:18px;padding:30px 34px}
.k b{display:block;font-weight:900;font-size:40px;letter-spacing:-.01em;margin-bottom:8px}
.k span{font-weight:700;font-size:32px;line-height:1.25;color:#DCE6EF}
#d{position:absolute;left:64px;right:64px;top:1135px;font-size:25px;font-weight:700;color:#9FB4C7}
</style></head><body>
<h1>¿Y esto qué <span class='a'>significa para ti?</span></h1>
<div id='c' class='chk'>
<div class='k'><b>1. El costo del dinero</b><span>Deuda y tasas altas pegan en créditos, bonos y bolsas. Vigila las tasas de interés.</span></div>
<div class='k'><b>2. La IA manda en el mercado</b><span>Es el motor de Wall Street y también su mayor riesgo. Ojo con la concentración.</span></div>
<div class='k'><b>3. La geopolítica mueve precios</b><span>Irán y Taiwán impactan petróleo, dólar y activos de riesgo como cripto.</span></div>
</div><div id='d'>Contenido informativo. No es asesoría financiera.</div>"""+PIE+"</body></html>"
pages[13]=CSS+"""
#logo{position:absolute;left:72px;top:84px;width:300px}
#dog{position:absolute;right:-30px;bottom:150px;width:470px;filter:drop-shadow(0 20px 50px rgba(0,0,0,.45))}
#b{position:absolute;left:72px;top:300px;width:760px;display:flex;flex-direction:column;gap:34px;align-items:flex-start}
h2{margin:0;font-weight:900;font-size:90px;line-height:.95;letter-spacing:-.04em}
p{margin:0;font-weight:700;font-size:40px;line-height:1.25;color:#DCE6EF;width:560px}
.btn{background:#4FC3F7;color:#152F46;font-weight:900;font-size:40px;padding:24px 38px;border-radius:999px;letter-spacing:-.02em;margin-top:10px}
#d{position:absolute;left:72px;right:72px;bottom:64px;font-size:25px;font-weight:700;color:#9FB4C7}
</style></head><body><img id='logo' src='../../../brand/logo-horizontal-transparente.png'>
<div id='b'><h2>Entiende el 2027 <span class='a'>antes que los demás</span></h2><p>Cripto y mercados, explicados fácil. Directo a tu correo y gratis.</p><span class='btn'>Suscríbete · link en la bio</span></div>
<img id='dog' src='../../../brand/mascotas/doggy-lentes.png'>
<div id='d'>Contenido informativo, no es asesoría financiera.</div></body></html>"""
for n,h in pages.items(): open(f'src/slide-{n:02d}.html','w').write(h)
from playwright.sync_api import sync_playwright
want=[int(x) for x in sys.argv[1:]] or sorted(pages)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for n in want:
        pg.goto('file://'+os.path.abspath(f'src/slide-{n:02d}.html')); pg.wait_for_timeout(500)
        r=pg.evaluate("[...document.querySelectorAll('.chk')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]})")
        print(n,r)
        pg.screenshot(path=f'slide-{n:02d}.jpg',type='jpeg',quality=92)
    b.close()
