# elholder-media

Assets y flujo para los carruseles de Instagram de **El Holder** (@elholder_).

## Estructura
- `brand/` — logo (horizontal y cuadrado) y mascotas sin fondo: `doggy`, `doggy-lentes`, `perrillo`, `chubby`.
- `fonts/` — Inter Tight 700/800/900.
- `fondos/` — banco de fotos de fondo por tema. Ver `fondos/INDICE.md`.
- `plantilla/base.css` — estilos de la línea de diseño (azul marino, blanco, acento amarillo, letra gigante en minúsculas).
- `plantilla/render.py` — convierte `carruseles/<slug>/src/slide-*.html` en `slide-NN.jpg` + `preview.jpg`.
- `carruseles/_ejemplo/` — 5 tipos de slide de referencia (portada, frase, dato+lista, cifra+mascota, CTA).
- `carruseles/<AAAA-MM-DD>-<slug>/` — un carrusel por post del newsletter.

## Flujo de un carrusel
1. Crear `carruseles/<fecha>-<slug>/src/` copiando los slides de `_ejemplo` que apliquen.
2. Editar textos (1 idea por slide, mínimo texto), elegir fondos del banco, mascota a veces.
3. `python3 plantilla/render.py carruseles/<fecha>-<slug>`
4. Revisar `preview.jpg`, hacer commit y push.
5. Las imágenes quedan públicas en:
   `https://raw.githubusercontent.com/adriansanpei/elholder-media/main/carruseles/<fecha>-<slug>/slide-NN.jpg`
   Esas URLs son las que se mandan a Metricool.

Reglas de contenido y diseño: ver los docs del proyecto de Claude "EL HOLDER" (`claude/guia-diseno-carruseles.md`, `claude/koemmandments-resumen.md`).
