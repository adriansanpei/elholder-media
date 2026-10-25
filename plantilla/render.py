"""Renderiza los slides HTML de un carrusel a JPG 1080x1350.

Uso:  python3 plantilla/render.py carruseles/<slug>
Lee   carruseles/<slug>/src/slide-*.html  (ordenados por nombre)
Crea  carruseles/<slug>/slide-NN.jpg       (listos para Metricool)
      carruseles/<slug>/preview.jpg        (hoja de contacto 3x3 para revisar)
Requiere playwright (Chromium) y Pillow.
"""
import sys, os, glob, asyncio
from PIL import Image
from playwright.async_api import async_playwright

async def main(folder):
    folder = os.path.abspath(folder)
    srcs = sorted(glob.glob(os.path.join(folder, 'src', 'slide-*.html')))
    if not srcs:
        sys.exit(f'No hay slides en {folder}/src')
    outs = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, s in enumerate(srcs, 1):
            await pg.goto('file://' + s)
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(250)
            png = os.path.join(folder, f'.tmp-{i:02d}.png')
            await pg.screenshot(path=png, clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
            jpg = os.path.join(folder, f'slide-{i:02d}.jpg')
            Image.open(png).convert('RGB').save(jpg, quality=92)
            os.remove(png)
            outs.append(jpg)
            print('ok', os.path.basename(jpg))
        await b.close()
    # hoja de contacto
    n = len(outs); cols = 3; rows = (n + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 370 + 10, rows * 460 + 10), 'white')
    for i, p in enumerate(outs):
        im = Image.open(p).resize((360, 450))
        sheet.paste(im, (10 + (i % cols) * 370, 10 + (i // cols) * 460))
    sheet.save(os.path.join(folder, 'preview.jpg'), quality=85)
    print('preview.jpg')

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1]))
