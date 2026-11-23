# Genera src/slide-NN.html para el carrusel de Riemann
import os
CSS = """
@font-face{font-family:'IT';font-weight:700;src:url('../../../fonts/inter-tight-latin-700-normal.woff2')}
@font-face{font-family:'IT';font-weight:800;src:url('../../../fonts/inter-tight-latin-800-normal.woff2')}
@font-face{font-family:'IT';font-weight:900;src:url('../../../fonts/inter-tight-latin-900-normal.woff2')}
html,body{margin:0}*{box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:'IT';color:#fff;background:#0E2238}
#bg{position:absolute;inset:0;background-size:cover;background-position:center}
#ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,34,56,.25) 0%,rgba(14,34,56,.10) 30%,rgba(14,34,56,.82) 50%,#0E2238 68%)}
.in{position:absolute;left:72px;right:72px;top:80px}
.bt{position:absolute;left:72px;right:72px;top:660px}
.k{font-weight:800;font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:#FF6B74;margin-bottom:16px}
h1{margin:0;font-weight:900;font-size:100px;line-height:.98;letter-spacing:-.03em}
.a{color:#4FC3F7}
p{margin:30px 0 0;font-weight:700;font-size:44px;line-height:1.22;color:#DCE6EF;max-width:930px}
.big{font-weight:900;font-size:300px;line-height:.85;letter-spacing:-.05em;filter:drop-shadow(0 6px 26px rgba(0,0,0,.75))}
.neon-v{color:#5EE0A8;text-shadow:0 0 30px rgba(94,224,168,.75),0 0 80px rgba(94,224,168,.45)}
.neon-r{color:#FF4D6D;text-shadow:0 0 30px rgba(255,77,109,.75),0 0 80px rgba(255,77,109,.45)}
.neon-a{color:#4FC3F7;text-shadow:0 0 30px rgba(79,195,247,.75),0 0 80px rgba(79,195,247,.45)}
#pie{position:absolute;left:72px;bottom:56px}
#pie img{height:46px;display:block}
.cue{display:inline-block;margin-top:40px;background:#fff;color:#0E2238;font-weight:900;font-size:34px;padding:16px 30px;border-radius:999px}
.tag{display:inline-block;background:#FF3B47;color:#fff;font-weight:900;font-size:30px;letter-spacing:.08em;padding:10px 22px;border-radius:12px}
"""
def page(body, bg=None, pie=True, extra=""):
    bgh = f'<div id="bg" style="background-image:url(../../../fondos/{bg}.jpg)"></div><div id="ov"></div>' if bg else ''
    pieh = '<div id="pie"><img src="../../../brand/logo-horizontal-transparente.png"></div>' if pie else ''
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}{extra}</style></head><body>{bgh}{body}{pieh}</body></html>'

ANTH = '<svg viewBox="0 0 24 24" style="height:64px;display:block"><path fill="#fff" d="M17.3041 3.541h-3.6718l6.696 16.918H24Zm-10.6082 0L0 20.459h3.7442l1.3693-3.5527h7.0052l1.3693 3.5528h3.7442L10.5363 3.5409Zm-.3712 10.2232 2.2914-5.9456 2.2914 5.9456Z"/></svg>'

slides = []
# 1 portada
slides.append(page(f'''
<div class="in" style="top:64px;display:flex;justify-content:space-between;align-items:center">
 <img src="../../../brand/logo-horizontal-transparente.png" style="height:58px">{ANTH}</div>
<div class="zeta">ζ(s) = 0</div>
<div class="bt" style="top:360px">
 <span class="tag">ESTA SEMANA</span>
 <div class="big neon-v" style="margin-top:22px;white-space:nowrap">166<span style="font-size:150px;letter-spacing:-.03em"> años</span></div>
 <h1 style="font-size:96px;margin-top:26px">La IA de <span class="a">ANTHROPIC</span> ayudó a resolver el problema más famoso de las matemáticas.</h1>
 <div class="cue">Desliza →</div></div>''', bg='ia-chip-01', pie=False,
 extra="#ov{background:linear-gradient(180deg,rgba(14,34,56,.45) 0%,rgba(14,34,56,.35) 25%,rgba(14,34,56,.85) 45%,#0E2238 62%)} .zeta{position:absolute;right:60px;top:170px;font-family:Georgia,serif;font-style:italic;font-size:120px;color:rgba(79,195,247,.85);text-shadow:0 0 40px rgba(79,195,247,.8);transform:rotate(-6deg)}"))
# 2 qué pasó
slides.append(page('''
<div class="bt" style="top:600px"><div class="k">Qué pasó</div>
 <h1>“Creo que la resolví, <span class="a">trabajando con Claude.</span>”</h1>
 <p>Eso escribió Levent Alpöge, matemático de Anthropic, el 20 de noviembre. Hablaba de la Hipótesis de Riemann: planteada en 1859 y con un premio de $1 millón de dólares.</p></div>''', bg='cafe-escritorio-01'))
# 3 qué es
slides.append(page('''
<div class="in"><div class="big neon-a" style="font-size:150px;letter-spacing:-.02em">2, 3, 5, 7, 11…</div></div>
<div class="bt" style="top:620px"><div class="k">¿Y eso qué es?</div>
 <h1>El mapa secreto de los <span class="a">números primos.</span></h1>
 <p>Los primos parecen salir al azar. Riemann propuso que siguen un patrón oculto. En más de 160 años, nadie lo había podido demostrar.</p></div>''', bg='lupa-datos-01'))
# 4 17M
slides.append(page('''
<div class="in"><div class="big neon-v">17M</div></div>
<div class="bt" style="top:620px"><div class="k">La prueba</div>
 <h1>Líneas de código para <span class="a">comprobarla.</span></h1>
 <p>Está escrita en Lean, un lenguaje donde la computadora revisa cada paso. Las comunidades de Lean y Mathlib ya la certificaron como correcta.</p></div>''', bg='ia-chip-02'))
# 5 nadie la ha leído
slides.append(page('''
<div class="in"><div class="big neon-r">0</div></div>
<div class="bt" style="top:620px"><div class="k">El detalle inquietante</div>
 <h1>Humanos la han leído <span class="a">completa.</span></h1>
 <p>La máquina dice que es correcta, pero todavía no entendemos por qué funciona. Descifrarla podría tomar años.</p></div>''', bg='multitud-01'))
# 6 qué viene
slides.append(page('''
<div class="bt" style="top:600px"><div class="k">¿Y esto qué significa?</div>
 <h1>Si la IA pudo con esto, <span class="a">¿qué sigue?</span></h1>
 <p>Gente de la industria advierte que podría acelerar la ciencia, la medicina y la propia IA más rápido de lo que podemos vigilar. El debate ya no es si llega, sino cómo.</p></div>''', bg='cohete-01'))
# 7 CTA
slides.append(page('''
<img src="../../../brand/mascotas/doggy-lentes.png" style="position:absolute;right:-40px;bottom:0;width:470px">
<div class="in" style="top:120px"><img src="../../../brand/logo-horizontal-transparente.png" style="height:80px;display:block">
 <h1 style="font-size:104px;margin-top:60px">La IA ya no solo escribe. <span class="a">Descubre.</span></h1>
 <p style="max-width:620px">Te explicamos qué significa para ti y para tu dinero, sin rollo. Gratis en tu correo.</p>
 <div class="cue" style="background:#4FC3F7">Link en la bio</div>
 <p style="font-size:38px;max-width:560px;margin-top:50px">¿Emocionante o da miedo? Comenta.</p></div>''', pie=False))
for i, h in enumerate(slides, 1):
    open(f'src/slide-{i:02d}.html', 'w').write(h)
print(len(slides))
