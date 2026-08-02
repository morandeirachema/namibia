#!/usr/bin/env python3
"""Genera la guia de fauna de Etosha en HTML listo para imprimir a PDF."""
import base64, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from especies import ID
try:
    from etosha import DONDE, INTRO_EXTRA, FUENTES_ETOSHA
except ImportError:          # aun sin el informe con fuentes
    DONDE, INTRO_EXTRA, FUENTES_ETOSHA = {}, "", []

man = json.load(open(os.path.join(HERE, "manifest.json")))

def negrita(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)   # negrita PRIMERO
    return re.sub(r"(?<![\w*])\*(?!\*)(.+?)(?<!\*)\*(?![\w*])", r"<em>\1</em>", t)

def b64(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

def tarjeta(m):
    img = b64(os.path.join(HERE, "img", m["local"]))
    autor = m["artist"] or "autor no indicado"
    donde = DONDE.get(m["slug"], "")
    bloque_donde = f'<p class="donde"><span class="et">Etosha</span> {negrita(donde)}</p>' if donde else ""
    return f"""
    <article class="sp">
      <div class="foto"><img src="{img}" alt="{m['es']}"></div>
      <div class="txt">
        <h3>{m['es']}</h3>
        <p class="nom"><em>{m['sci']}</em> · {m['en']}</p>
        <p class="id">{negrita(ID.get(m['slug'], ''))}</p>
        {bloque_donde}
      </div>
      <p class="cred">Foto: {autor} · {m['license']}</p>
    </article>"""

mam = [m for m in man if m["grupo"] == "mamifero" and "local" in m]
ave = [m for m in man if m["grupo"] == "ave" and "local" in m]

creditos = "".join(
    f"<li><strong>{m['es']}</strong> — {m['artist'] or 'autor no indicado'}, "
    f"<em>{m['license']}</em> · <span class='u'>{m['descurl']}</span></li>"
    for m in man if "local" in m)

fuentes_extra = "".join(f"<li>{f}</li>" for f in FUENTES_ETOSHA)

HTML = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Fauna de Etosha — guía de campo</title>
<style>
  @page {{ size: A4; margin: 12mm 11mm 14mm 11mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif;
         color: #22201d; margin: 0; font-size: 9.2pt; line-height: 1.34;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

  /* ---------- portada ---------- */
  .portada {{ height: 271mm; display: flex; flex-direction: column; justify-content: center;
              text-align: center; background: #1d2b21; color: #f4efe6; padding: 0 16mm;
              page-break-after: always; }}
  .portada .kicker {{ letter-spacing: .32em; text-transform: uppercase; font-size: 8.5pt;
                      color: #c9b98f; margin-bottom: 7mm; }}
  .portada h1 {{ font-size: 34pt; margin: 0 0 3mm; line-height: 1.05; font-weight: 800; }}
  .portada h2 {{ font-size: 13pt; font-weight: 400; color: #c9b98f; margin: 0 0 12mm; }}
  .portada .datos {{ font-size: 10pt; line-height: 1.9; }}
  .portada .datos b {{ color: #e9dcc0; }}
  .portada .pie {{ margin-top: 14mm; font-size: 7.8pt; color: #93a394; line-height: 1.6; }}

  /* ---------- secciones ---------- */
  h2.sec {{ font-size: 15pt; margin: 0 0 4mm; padding: 2.5mm 4mm; color: #fff;
            background: #7a3a22; border-radius: 2mm; page-break-after: avoid; }}
  h2.sec span {{ float: right; font-weight: 400; font-size: 9.5pt; opacity: .85; }}
  .intro {{ background: #f3ede2; border-left: 3px solid #7a3a22; padding: 3mm 4mm;
            margin: 0 0 4mm; font-size: 8.1pt; border-radius: 0 2mm 2mm 0; }}
  .intro p {{ margin: 0 0 1.2mm; }} .intro p:last-child {{ margin: 0; }}

  /* ---------- rejilla de especies ---------- */
  .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3.5mm; align-items: start; }}
  .sp {{ border: .4pt solid #d8d0c2; border-radius: 2mm; overflow: hidden;
         page-break-inside: avoid; break-inside: avoid; background: #fff; }}
  /* caja 3:2, la proporcion mediana de las fotos · contain = NUNCA recorta */
  .foto {{ height: 39mm; background: #e6e0d4; }}
  .foto img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
  .txt {{ padding: 2mm 2.4mm .8mm; }}
  .sp h3 {{ margin: 0; font-size: 9.6pt; color: #7a3a22; line-height: 1.15; }}
  .nom {{ margin: .3mm 0 1.4mm; font-size: 6.9pt; color: #6d675d; }}
  .id {{ margin: 0; font-size: 7.7pt; text-align: justify; hyphens: auto; }}
  .donde {{ margin: 1.4mm 0 0; font-size: 7.5pt; background: #eaf1ea; border-radius: 1.2mm;
            padding: 1.6mm 2mm; text-align: justify; }}
  .donde .et {{ font-weight: 700; color: #2d6a4f; text-transform: uppercase;
                font-size: 6.8pt; letter-spacing: .09em; margin-right: 1mm; }}
  .cred {{ margin: 1mm 0 0; padding: 0 2.4mm 1.6mm; font-size: 6pt; color: #8d867a; }}

  /* ---------- creditos ---------- */
  .final {{ page-break-before: always; }}
  .final h2 {{ font-size: 13pt; color: #7a3a22; margin: 0 0 3mm; }}
  .final ul {{ columns: 2; column-gap: 7mm; padding-left: 4mm; margin: 0 0 5mm;
               font-size: 7.2pt; line-height: 1.45; }}
  .final li {{ break-inside: avoid; margin-bottom: 1mm; }}
  .final .u {{ color: #8d867a; word-break: break-all; }}
  .nota {{ background: #f3ede2; padding: 3mm 4mm; border-radius: 2mm; font-size: 8pt; }}
</style></head><body>

<section class="portada">
  <div class="kicker">Namibia · 1–14 de noviembre de 2026</div>
  <h1>Fauna de Etosha</h1>
  <h2>Guía de campo · {len(mam)} mamíferos y {len(ave)} aves</h2>
  <div class="datos">
    Cuatro noches <b>dentro del parque</b><br>
    <b>Okaukuejo</b> · 9 nov &nbsp;—&nbsp; <b>Halali</b> · 10 nov &nbsp;—&nbsp; <b>Namutoni</b> · 11 y 12 nov<br>
    Final de la estación seca: la fauna, concentrada en las charcas
  </div>
  <div class="pie">
    Fotografías de Wikimedia Commons, todas con licencia libre (CC BY / CC BY-SA):<br>
    autoría y licencia de cada una, bajo la foto y en los créditos del final.<br>
    Los rasgos de identificación son descriptivos; lo específico de Etosha va con su fuente.
  </div>
</section>

<h2 class="sec">Mamíferos <span>{len(mam)} especies</span></h2>
<div class="intro">
  <p><strong>Cada ficha</strong> lleva el nombre en castellano, el científico y el inglés —el de los
  carteles del parque— y los rasgos que sirven para distinguirla <em>en el campo</em>.</p>
  {INTRO_EXTRA}
</div>
<div class="grid">{''.join(tarjeta(m) for m in mam)}</div>

<h2 class="sec" style="margin-top:6mm">Aves <span>{len(ave)} especies</span></h2>
<div class="intro">
  <p>Con el coche parado en una charca, las aves llenan las esperas. Estas son las que
  <strong>se ven sin ser ornitólogo</strong>: grandes, ruidosas o de color imposible.</p>
</div>
<div class="grid">{''.join(tarjeta(m) for m in ave)}</div>

<section class="final">
  <h2>Créditos de las fotografías</h2>
  <p class="nota">Todas las imágenes proceden de <strong>Wikimedia Commons</strong> y se reproducen
  bajo licencia libre <strong>CC BY</strong> o <strong>CC BY-SA</strong>, que exigen citar autor y
  licencia — es lo que hace esta lista. Los textos de licencia:
  <span class="u">creativecommons.org/licenses/by/2.0</span> ·
  <span class="u">creativecommons.org/licenses/by-sa/2.0</span> ·
  <span class="u">creativecommons.org/licenses/by-sa/3.0</span> ·
  <span class="u">creativecommons.org/licenses/by-sa/4.0</span></p>
  <ul>{creditos}</ul>
  {'<h2>Fuentes de lo específico de Etosha</h2><ul>' + fuentes_extra + '</ul>' if fuentes_extra else ''}
</section>

</body></html>"""

out = os.path.join(HERE, "guia.html")
open(out, "w").write(HTML)
print(f"HTML escrito: {out} ({len(HTML)//1024} KB) · {len(mam)} mamíferos + {len(ave)} aves"
      f" · fichas con dato de Etosha: {sum(1 for m in man if DONDE.get(m.get('slug')))}")
