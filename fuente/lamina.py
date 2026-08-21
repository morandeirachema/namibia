#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La lamina de ruta: un A2 para imprimir y colgar, con el recorrido entero.

No es una pagina del dossier recortada. Es una hoja sola, pensada para leerse de pie y
a un metro: el mapa a 372 mm de ancho —con lo que los roqulos del SVG, que van en
unidades del viewBox, salen a ~9 pt— y debajo las quince etapas con sus kilometros y
donde se duerme cada noche.

Todo sale de las mismas fuentes que el resto del repo: `trazado.ETAPAS` para el orden y
`geo/ruta.json` para los kilometros reales del enrutado. Aqui no se escribe a mano ni
una cifra; si cambia una noche, cambia la lamina sola.

    python3 lamina.py            el PDF
    python3 lamina.py --html     solo el HTML, para mirarlo en el navegador

Sale en A2 (420x594 mm). En una impresora de casa se manda a A3 o A4 con «ajustar a
pagina»: al ser vectorial no pierde nitidez, solo tamano de letra.
"""
import os
import sys

import comun
import imprimir
import mapa
import trazado

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
FECHA = "21 de agosto de 2026"

# --- La geometria de la hoja, en mm. Todo lo demas se calcula de aqui. -----------
HOJA_ANCHO, HOJA_ALTO = 420, 594
MARGEN = (10, 10, 12, 10)                      # arriba, derecha, abajo, izquierda
UTIL_ANCHO = HOJA_ANCHO - MARGEN[1] - MARGEN[3]
MAPA_ANCHO = 384                               # ~9 pt de rotulo; ver la cabecera
MAPA_ALTO = MAPA_ANCHO * 1373.5 / 1100         # la proporcion del encuadre de mapa.py


def etapas():
    """Las quince etapas con su kilometraje real y donde se duerme esa noche."""
    km = {e["id"]: e.get("km") for e in mapa.carga("ruta.json")}
    filas = []
    for e in trazado.ETAPAS:
        duerme = trazado.PUNTOS[e["duerme"]][2] if e["duerme"] else "—"
        d = km.get(e["id"]) or 0
        filas.append({
            "id": e["id"], "fecha": e["fecha"], "titulo": e["titulo"],
            "km": f"{d:.0f} km" if d else "sin traslado",
            "duerme": duerme, "bloque": e["bloque"],
        })
    return filas


def total_km():
    return sum(e.get("km") or 0 for e in mapa.carga("ruta.json"))


CSS = """
@page {{ size: {ancho}mm {alto}mm; margin: {m0}mm {m1}mm {m2}mm {m3}mm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Source Sans 3', system-ui, sans-serif; color: #1D1A15;
       background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

/* --- cabecera ---------------------------------------------------------- */
.cab {{ display: flex; align-items: flex-end; justify-content: space-between;
       gap: 10mm; border-bottom: .8mm solid #16130F; padding-bottom: 2.5mm; }}
.cab h1 {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 34pt;
          font-weight: 700; line-height: .95; letter-spacing: -.01em; }}
.cab h1 span {{ color: #C2542F; }}
.cab .sub {{ font-size: 12pt; color: #56514A; margin-top: 1.5mm;
            font-family: 'Source Serif 4', Georgia, serif; font-style: italic; }}
.cab .datos {{ text-align: right; font-size: 10pt; line-height: 1.45; color: #56514A; }}
.cab .datos b {{ color: #1D1A15; }}
.cab .datos .grande {{ font-size: 15pt; font-weight: 700; color: #16130F;
                      display: block; letter-spacing: -.01em; }}

/* --- el mapa ----------------------------------------------------------- */
.mapa {{ width: {mapa_ancho}mm; height: {mapa_alto:.1f}mm; margin: 4mm auto 0;
        border: .4mm solid #C6C1B4; }}
.mapa svg {{ width: 100%; height: 100%; }}

/* --- la tira de etapas ------------------------------------------------- */
.tira {{ margin-top: 4.5mm; border-top: .5mm solid #16130F; padding-top: 2.5mm; }}
.tira h2 {{ font-size: 8.5pt; text-transform: uppercase; letter-spacing: .12em;
           color: #7D776E; font-weight: 700; margin-bottom: 2mm; }}
ol.etapas {{ list-style: none; display: grid; grid-template-columns: repeat(3, 1fr);
            gap: 0 7mm; }}
ol.etapas li {{ display: grid; grid-template-columns: 19mm 1fr auto;
               gap: 0 2.5mm; align-items: baseline; font-size: 8.2pt; line-height: 1.25;
               padding: .9mm 0 .9mm 2mm; border-top: .2mm solid #DAD5C9;
               border-left: .9mm solid var(--c); }}
ol.etapas .dia {{ font-weight: 700; font-size: 8.2pt; white-space: nowrap; }}
ol.etapas .dia i {{ font-style: normal; font-weight: 400; color: #7D776E; }}
ol.etapas .que {{ font-family: 'Source Serif 4', Georgia, serif; }}
ol.etapas .que i {{ font-style: normal; color: #7D776E; }}
ol.etapas .que i b {{ font-weight: 700; color: #1D1A15; }}
ol.etapas .km {{ text-align: right; font-family: 'IBM Plex Mono', monospace;
                font-size: 7.6pt; color: #56514A; white-space: nowrap; }}

/* --- la banda de reglas ------------------------------------------------ */
.reglas {{ margin-top: 3.5mm; display: grid; grid-template-columns: repeat(4, 1fr);
          gap: 0 6mm; font-size: 8pt; line-height: 1.3; }}
.reglas div {{ border-left: .9mm solid #C6C1B4; padding-left: 2.5mm; }}
.reglas .rot {{ display: block; font-size: 7.2pt; text-transform: uppercase;
              letter-spacing: .08em; color: #7D776E; margin-bottom: .5mm;
              font-weight: 700; }}
.reglas b {{ font-weight: 700; color: #16130F; }}
.reglas .rojo {{ border-left-color: #A32E28; }}
.reglas .rojo .rot {{ color: #A32E28; }}
"""


def cabecera(km):
    return f"""<header class="cab">
  <div>
    <h1>NAMIBIA <span>2026</span></h1>
    <div class="sub">El gran roadtrip del norte · Chema Morandeira y Miguel Rivera</div>
  </div>
  <div class="datos">
    <span class="grande">~{comun.mil(km)} km en 15 días</span>
    <b>30 de octubre – 15 de noviembre</b> · un 4×4 con tienda de techo<br>
    14 noches, 13 de ellas arriba · cuatro en Etosha, tres dentro del parque
  </div>
</header>"""


def tira():
    li = []
    for e in etapas():
        color = trazado.COLOR_BLOQUE[e["bloque"]]
        li.append(
            f'<li style="--c:{color}">'
            f'<span class="dia">{e["id"]} <i>{e["fecha"]}</i></span>'
            f'<span class="que">{mapa.esc(e["titulo"])} '
            f'<i>· duerme <b>{e["duerme"]}</b></i></span>'
            f'<span class="km">{e["km"]}</span></li>')
    return ('<section class="tira"><h2>Las quince etapas · kilómetros del enrutado '
            'propio sobre OpenStreetMap</h2>'
            f'<ol class="etapas">{"".join(li)}</ol></section>')


REGLAS = [
    ("", "Velocidad de planificación",
     "Asfalto <b>100</b> · grava <b>80</b>, que es el techo del contrato y no la "
     "media · parque <b>60</b>."),
    ("rojo", "La regla de oro",
     "<b>En el campamento a las 18:00</b>. La franja 16:00–20:00 concentra el "
     "<b>29 %</b> de los muertos del país."),
    ("", "Puertas de Etosha",
     "<b>3–9 nov 06:13–19:06</b> · <b>10–16 nov 06:10–19:10</b>. Ugabmund, "
     "última entrada <b>15:00</b>."),
    ("rojo", "Emergencias",
     "E-Med <b>924</b> · LifeLink <b>999</b> · venenos <b>+264 81 127 5109</b> · "
     "policía <b>+264 61 10111</b> (pide prefijo)."),
]


def reglas():
    d = "".join(f'<div class="{c}"><span class="rot">{t}</span>{x}</div>'
                for c, t, x in REGLAS)
    return f'<section class="reglas">{d}</section>'


def html_completo():
    css = CSS.format(ancho=HOJA_ANCHO, alto=HOJA_ALTO, m0=MARGEN[0], m1=MARGEN[1],
                     m2=MARGEN[2], m3=MARGEN[3],
                     mapa_ancho=MAPA_ANCHO, mapa_alto=MAPA_ALTO)
    tipos = comun.tipografias(os.path.join(HERE, "tipos"))
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Namibia 2026 — la lámina de ruta</title>
<style>{tipos}</style><style>{css}</style></head><body>
{cabecera(total_km())}
<div class="mapa">{mapa.mapa_ruta(1100)}</div>
{tira()}
{reglas()}
</body></html>"""


def main():
    salida_html = os.path.join(HERE, "lamina.html")
    salida_pdf = os.path.join(RAIZ, "mapa-ruta-namibia-2026.pdf")

    open(salida_html, "w").write(html_completo())
    print(f"HTML: {os.path.getsize(salida_html) // 1024} KB")
    if "--html" in sys.argv:
        return 0

    imprimir.a_pdf(salida_html, salida_pdf, papel="A2", margenes=MARGEN, espera=3,
                   izquierda="Namibia 2026 · lámina de ruta · A2",
                   derecha=FECHA)
    n = imprimir.paginas(salida_pdf)
    print(f"\n{os.path.relpath(salida_pdf, RAIZ)} · {HOJA_ANCHO}×{HOJA_ALTO} mm · "
          f"{n} página · {os.path.getsize(salida_pdf) // 1024} KB")
    if n != 1:
        print("   aviso: la lámina debería ser UNA página; algo se desborda",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
