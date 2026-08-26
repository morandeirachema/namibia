#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La agenda: el día a día del `01`, y nada más — un A4 por día, para la guantera.

No es el dossier recortado a mano: es el MISMO markdown del `01`, cortado entre `### D1` y
el final del `### D15`, con las digresiones de investigación fuera. Todo lo que aquí se
imprime sale del `01`, así que cambiar una noche en el `01` cambia la agenda sola.

Lo que se quita, y por qué:
  · las notas entre paréntesis en cursiva que citan fuentes, decisiones y fechas
    —«(decidido 08/08)», «(OSRM 128,8)», «(ver `13`)»— son historia del dossier, no del día;
  · las líneas de temperatura y de fauna alrededor del campamento viven en el dossier;
  · las referencias a otros documentos se desenvuelven: aquí no hay a dónde saltar.
Lo que se queda: horas, kilómetros, qué hacer, qué reservar, qué preguntar, el sol, la
luna, las casillas y las opciones ya decididas o abiertas.

    python3 agenda.py            el PDF
    python3 agenda.py --html     solo el HTML, para mirarlo en el navegador
"""
import os
import re
import sys

import comun
import imprimir
import trazado
from comun import RAIZ, marca_texto, md

HERE = os.path.dirname(os.path.abspath(__file__))
FECHA = "25 de agosto de 2026"
FUENTE = os.path.join(RAIZ, "01-itinerarios-dia-a-dia.md")
MARGEN = (14, 12, 16, 12)                        # los del dossier, para que se parezcan

# Bullets del `01` que son del dossier y no de la agenda: empiezan por este emoji.
FUERA = ("🌡️", "🐾")


def dias():
    """Los quince bloques `### Dn · …` del `01`, en orden, con su markdown."""
    texto = open(FUENTE, encoding="utf-8").read()
    ini = texto.index("\n### D1 ·")
    fin = texto.index("\n### 💰 Coste real")
    cuerpo = texto[ini:fin]
    trozos = re.split(r"\n(?=### D\d+ ·)", cuerpo)
    salida = []
    for t in trozos:
        m = re.match(r"### (D\d+) · ([^\n]*)\n", t)
        if not m:
            continue
        salida.append((m.group(1), m.group(2).strip(), t[m.end():]))
    return salida


def poda(mdtexto):
    """Fuera lo que es del dossier y no del día."""
    lineas, out, saltando = mdtexto.split("\n"), [], False
    for ln in lineas:
        es_bullet = re.match(r"^- ", ln)
        if es_bullet:
            saltando = any(ln.startswith(f"- {e}") for e in FUERA)
        elif not ln.startswith("  ") and ln.strip():
            saltando = False
        if not saltando:
            out.append(ln)
    t = "\n".join(out)
    # las notas de fuente/decisión en cursiva entre paréntesis, que van por bloques
    t = re.sub(r"\s*\*\((?:OSRM|decidido|ver |cambio del|act\. |el análisis|detalle en|"
               r"cálculo|adelantado|rehecho|verificado|confirmado|añadido|[Cc]orregido|"
               r"secundarias|tabla de 20)[^)]*\)\*", "", t)
    t = re.sub(r"\s*\*\([^)]*`\d\d`[^)]*\)\*", "", t)         # «(… `13` …)»
    # las remisiones a `aparte/` son del repo, no del dia: en la guantera no hay a donde ir.
    # Van como parrafo propio en cursiva, a veces a dos lineas y a veces citadas con «> ».
    t = re.sub(r"\n(?:>\s*)?\*[^*]*aparte/[^*]*\*\s*(?=\n|$)", "", t)
    # los enlaces a otros documentos, a texto plano
    t = re.sub(r"\[`(\d\d)`\]\(\d\d-[a-z-]+\.md\)", r"`\1`", t)
    t = re.sub(r"\[([^\]]+)\]\((?:\d\d-[a-z-]+\.md|aparte/[^)]+|README\.md|guia-fauna[^)]*)\)",
               r"\1", t)
    return t


def cabecera_dia(dia, titulo, breve=False):
    """«D3 · lun 2 — Spreetshoogte → Sesriem · ~129 km · ~2h» partido en sus piezas."""
    fecha, _, resto = titulo.partition(" — ")
    que, _, cifra = resto.partition(" · **")
    cifra = cifra.rstrip("*").replace("**", "")
    que = re.sub(r"\s*\*\([^)]*\)\*\s*$", "", que).strip()
    etapa = next(e for e in trazado.ETAPAS if e["id"] == dia)
    color = trazado.COLOR_BLOQUE[etapa["bloque"]]
    duerme = (trazado.PUNTOS[etapa["duerme"]][2].split(" · ")[0].replace("Paso de ", "")
              if etapa["duerme"] else "vuelo")
    return f"""<header class="dia{' breve' if breve else ''}" style="--c:{color}">
  <div class="num">{dia}</div>
  <div class="t">
    <div class="fecha">{fecha}</div>
    <h1>{marca_texto(md.renderInline(que))}</h1>
    <div class="cifra">{marca_texto(md.renderInline(cifra)) if cifra else ""}</div>
  </div>
  <div class="duerme"><span>duerme</span><b>{duerme}</b></div>
</header>"""


def banda_mapa(dia):
    """El mapa del dia con, encima, su ficha: kilometros por firme, tiempos y lugares de paso.

    Los kilometros por firme salen de `geo/tramos.json` (OSRM, con el ref de cada tramo y
    la tabla `trazado.FIRME`); el tiempo minimo, de las velocidades de planificacion del
    `13` —asfalto 100, grava 80, parque 60—, y el realista anade lo que el `13` anade:
    grava a 60–70 de media real y 30–60 min de paradas. No es un dato de fuente: es el
    mismo convenio del dossier, aplicado tramo a tramo.
    """
    import mapa
    etapa = next(e for e in trazado.ETAPAS if e["id"] == dia)
    km, h_min = mapa.firme_del_dia(dia)
    total = sum(km.values())
    if not total:
        # dia sin traslado: el mapa es lo que hay alrededor de donde se duerme
        svg = mapa.mapa_dia(dia, 1000, 1080)
        donde = trazado.PUNTOS[etapa["duerme"]][2].split(" · ")[0]
        return f"""<section class="mapa-dia">
  <div class="ficha"><span class="tot"><b>sin traslado</b></span>
    <span class="t">día de descanso en <b>{donde}</b></span></div>
  <div class="svg">{svg}</div>
  <div class="paso">{donde}: lo que hay alrededor, sin mover el coche de sitio</div>
</section>"""
    # realista, con el convenio del `13` tal cual: grava y sal a 60–70 de media real, y
    # 30–60 min de paradas y repostaje — una banda, no un numero, porque asi es como lo
    # da el dossier y asi no salen dos cifras distintas para el mismo dia en el mismo PDF
    def con(vel_grava, paradas):
        return sum(v / (vel_grava if f in ("grava", "sal") else mapa.VEL[f])
                   for f, v in km.items()) + paradas
    h_r0, h_r1 = con(70.0, 0.5), con(60.0, 1.0)
    def hm(h):
        return f"{int(h)} h {int(round(h % 1 * 60)):02d}"
    orden = ["asfalto", "grava", "sal", "parque"]
    firmes = "".join(
        f'<span class="f"><i style="background:{mapa.COLOR_FIRME[f]}"></i>'
        f'{mapa.NOMBRE_FIRME[f]} <b>{km[f]:.0f} km</b></span>'
        for f in orden if km.get(f, 0) >= 1)
    aviso = ""
    if "sossusvlei" in etapa["por"]:
        aviso = ('<span class="f aviso">+ los <b>últimos ~5 km de arena blanda</b> hasta '
                 'Sossusvlei/Deadvlei, que OSRM no enruta: 4H y desinflar, o la lanzadera</span>')
    paso = [trazado.PUNTOS[p][2].split(" · ")[0] for p in etapa["por"]]
    # sin repetir el punto de partida cuando el dia vuelve al mismo sitio
    compact = [p for i, p in enumerate(paso) if i == 0 or p != paso[i - 1]]
    lugares = " → ".join(compact)
    svg = mapa.mapa_dia(dia, 1000, 1080)
    return f"""<section class="mapa-dia">
  <div class="ficha">
    <span class="tot"><b>{total:.0f} km</b></span>
    {firmes}{aviso}
    <span class="t">mínimo <b>{hm(h_min)}</b> · realista <b>{hm(h_r0)}–{hm(h_r1)}</b></span>
  </div>
  <div class="svg">{svg}</div>
  <div class="paso">{lugares}</div>
</section>"""


def a_html(texto):
    h = md.render(texto)

    def desescapa(m):
        c = (m.group(1).replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"'))
        return '<pre class="mermaid">' + c + "</pre>"
    h = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', desescapa, h, flags=re.S)
    h = re.sub(r'<li>\[ \]\s*', '<li class="tarea"><span class="casilla"></span>', h)
    h = re.sub(r'<code>(\d\d)</code>', r'<span class="doc">\1</span>', h)
    return marca_texto(h)


CSS = """
@page { size: A4; margin: 14mm 12mm 16mm 12mm; }
* { box-sizing: border-box; }
html { font-size: 9.6pt; }
body { margin: 0; font-family: var(--sans); color: var(--tinta); background: #fff;
       line-height: 1.38; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
:root { --serif: "Source Serif 4", Georgia, serif; --sans: "Source Sans 3", Arial, sans-serif;
        --mono: "IBM Plex Mono", monospace; --tinta: #1D1A15; --tinta-2: #56514A;
        --tinta-3: #7D776E; --regla: #DAD5C9; --oxido: #C2542F; --crema: #F7F4ED; }

/* --- portada ------------------------------------------------------------ */
.portada { height: 267mm; display: flex; flex-direction: column; justify-content: space-between;
           page-break-after: always; }
.portada h1 { font-family: var(--serif); font-size: 44pt; line-height: .95; margin: 0;
              letter-spacing: -.01em; }
.portada h1 span { color: var(--oxido); }
.portada .sub { font-family: var(--serif); font-style: italic; font-size: 15pt;
                color: var(--tinta-2); margin-top: 3mm; }
.portada .que { margin-top: 12mm; font-size: 11pt; max-width: 130mm; color: var(--tinta-2); }
ol.indice { list-style: none; padding: 0; margin: 10mm 0 0; column-count: 2; column-gap: 8mm;
            font-size: 9.6pt; }
ol.indice li { display: grid; grid-template-columns: 11mm 1fr auto; gap: 0 2mm;
               padding: 1mm 0 1mm 2mm; border-left: .9mm solid var(--c);
               border-top: .2mm solid var(--regla); break-inside: avoid; }
ol.indice .d { font-weight: 700; }
ol.indice .f { color: var(--tinta-3); }
ol.indice .k { font-family: var(--mono); font-size: 8.4pt; color: var(--tinta-2); }
.portada .pie { font-size: 8.6pt; color: var(--tinta-3); border-top: .5mm solid var(--tinta); padding-top: 2mm; }

/* --- el mapa del día ------------------------------------------------------ */
.mapa-dia { margin: 0; break-inside: avoid; }
.mapa-dia .svg { border: .35mm solid var(--regla); }
.mapa-dia .ficha { margin: 2.5mm 0 1.5mm; font-size: 9.6pt; gap: 1mm 6mm; }
.mapa-dia .ficha .tot { font-size: 14pt; }
.mapa-dia .ficha .t { margin-left: auto; font-size: 9pt; }
.mapa-dia .ficha .aviso { color: var(--oxido); font-size: 8.6pt; flex-basis: 100%; }
.mapa-dia .paso { font-size: 9.4pt; margin-top: 1.5mm; }
section.d.texto .cuerpo { column-count: 2; column-gap: 6mm; }
header.dia.breve { margin-bottom: 3mm; padding-bottom: 1.5mm; }
header.dia.breve .num { font-size: 22pt; }
header.dia.breve h1 { font-size: 13pt; }
header.dia.breve .cifra, header.dia.breve .duerme { display: none; }
.mapa-dia .svg svg { display: block; width: 100%; height: auto; }
.mapa-dia .ficha { display: flex; flex-wrap: wrap; gap: 1mm 5mm; align-items: baseline;
                   font-size: 8.8pt; color: var(--tinta-2); margin-bottom: 1.5mm; }
.mapa-dia .ficha .tot { font-family: var(--serif); font-size: 12pt; color: var(--tinta); }
.mapa-dia .ficha .f i { display: inline-block; width: 6mm; height: 1.4mm; border-radius: .7mm;
                        vertical-align: middle; margin-right: 1.4mm; }
.mapa-dia .ficha .t { margin-left: auto; font-family: var(--mono); font-size: 8.2pt; }
.mapa-dia .paso { font-size: 8.2pt; color: var(--tinta-3); margin-top: 1.2mm;
                  font-family: var(--serif); font-style: italic; }
.cuerpo { column-count: 2; column-gap: 6mm; column-fill: auto; }
.cuerpo > * { break-inside: avoid; }
.cuerpo pre.mermaid { column-span: all; }

/* --- cada día ----------------------------------------------------------- */
section.d { page-break-before: always; }
header.dia { display: grid; grid-template-columns: 22mm 1fr auto; gap: 0 4mm; align-items: end;
             border-bottom: .8mm solid var(--c); padding-bottom: 2.5mm; margin-bottom: 4mm; }
header.dia .num { font-family: var(--serif); font-size: 34pt; font-weight: 700; color: var(--c);
                  line-height: .9; }
header.dia .fecha { font-size: 9.5pt; text-transform: uppercase; letter-spacing: .1em;
                    color: var(--tinta-3); font-weight: 700; }
header.dia h1 { font-family: var(--serif); font-size: 17pt; line-height: 1.1; margin: .5mm 0 0;
                font-weight: 700; }
header.dia .cifra { font-family: var(--mono); font-size: 8.8pt; color: var(--tinta-2); margin-top: 1mm; }
header.dia .duerme { text-align: right; font-size: 8.4pt; color: var(--tinta-3);
                     text-transform: uppercase; letter-spacing: .08em; }
header.dia .duerme b { display: block; font-family: var(--serif); font-size: 12pt;
                       text-transform: none; letter-spacing: 0; color: var(--tinta); }

.cuerpo ul { padding-left: 5.5mm; margin: 0 0 2mm; }
.cuerpo li { margin: 0 0 1.6mm; }
.cuerpo li.tarea { list-style: none; position: relative; }
.cuerpo .casilla { position: absolute; left: -5.5mm; top: .9mm; width: 3.4mm; height: 3.4mm;
                   border: .35mm solid var(--tinta); border-radius: .5mm; }
.cuerpo blockquote { margin: 3mm 0; padding: 3mm 4mm; background: var(--crema);
                     border-left: .9mm solid var(--oxido); }
.cuerpo blockquote li, .cuerpo blockquote h3 { break-inside: avoid; }
.cuerpo blockquote h3 { margin: 0 0 1.5mm; font-family: var(--serif); font-size: 12pt; }
.cuerpo blockquote p { margin: 0 0 1.5mm; }
.cuerpo h3 { font-family: var(--serif); font-size: 12.5pt; margin: 4mm 0 1.5mm; }
.cuerpo h4 { font-size: 10pt; margin: 3mm 0 1mm; text-transform: uppercase; letter-spacing: .06em;
             color: var(--tinta-3); }
.cuerpo code { font-family: var(--mono); font-size: .9em; }
.cuerpo .doc { font-family: var(--mono); font-size: .8em; color: var(--tinta-3);
               border: .2mm solid var(--regla); border-radius: .6mm; padding: 0 .8mm; }
.cuerpo strong { font-weight: 700; }
.cuerpo em { color: var(--tinta-2); }
.cuerpo a { color: inherit; text-decoration: none; }
.cuerpo p { margin: 0 0 2mm; }
.cuerpo pre.mermaid { margin: 2mm 0 3mm; text-align: center; break-inside: avoid; }
.cuerpo pre.mermaid svg { max-width: 100%; height: auto; }
.marca { white-space: nowrap; }
/* Los rotulos que marca_texto saca de los emoji (sol, teléfono, dónde se duerme…): sin
   este margen se pegan a la palabra siguiente y se lee «teléfonoLas dos llamadas». */
.rot { font-size: 7.6pt; text-transform: uppercase; letter-spacing: .07em; color: var(--tinta-3);
       font-weight: 700; margin-right: 1.6mm; white-space: nowrap; }
/* El D13 es el mas largo y se salia por dos viñetas: la
   ultima lista de cada dia no necesita aire debajo, que ahi acaba la pagina. */
.cuerpo > :last-child, .cuerpo blockquote > :last-child { margin-bottom: 0; }
.cuerpo blockquote li { margin-bottom: 1mm; }
.cuerpo blockquote { line-height: 1.32; }
"""


def portada():
    from mapa import carga
    km = {e["id"]: e.get("km") or 0 for e in carga("ruta.json")}
    li = []
    for e in trazado.ETAPAS:
        c = trazado.COLOR_BLOQUE[e["bloque"]]
        k = km[e["id"]]
        li.append(f'<li style="--c:{c}"><span class="d">{e["id"]}</span>'
                  f'<span><b>{e["titulo"]}</b> <span class="f">· {e["fecha"]}</span></span>'
                  f'<span class="k">{f"{k:.0f} km" if k else "—"}</span></li>')
    total = sum(km.values())
    return f"""<section class="portada">
  <div>
    <h1>NAMIBIA <span>2026</span><br>la agenda</h1>
    <div class="sub">El día a día, y nada más — cada día con su mapa, para la guantera</div>
    <p class="que">Dos páginas por día. La primera, el mapa del recorrido pintado por
    firme —asfalto, grava, sal, pista de parque—, con los lugares de paso, las gasolineras
    obligatorias, dónde comer y qué ver de paso, y los kilómetros y el tiempo de cada
    firme. La segunda, lo mismo que cuenta el itinerario del dossier sin la investigación
    detrás: horas, qué hacer, qué reservar, qué preguntar, el sol y la luna, y las opciones
    que ya están decididas o abiertas. Cada casilla se marca a boli.</p>
    <ol class="indice">{"".join(li)}</ol>
  </div>
  <div class="pie">~{comun.mil(total)} km en 15 días · 30 de octubre – 15 de noviembre ·
  Chema Morandeira y Miguel Rivera · generado del documento <code>01</code> el {FECHA}</div>
</section>"""


def html_completo():
    # El mismo Mermaid, la misma configuracion y la misma senal de «diagramas listos» que
    # el dossier: `imprimir.a_pdf` espera a `dataset.diagramas` antes de imprimir, y la
    # configuracion de dossier.py es la que ya costo afinar para que los rotulos no se
    # salgan de las cajas.
    import dossier
    tipos = comun.tipografias(os.path.join(HERE, "tipos"))
    secciones = []
    for dia, titulo, cuerpo in dias():
        secciones.append(f'<section class="d mapa">{cabecera_dia(dia, titulo)}{banda_mapa(dia)}</section>'
                         f'<section class="d texto">{cabecera_dia(dia, titulo, breve=True)}'
                         f'<div class="cuerpo">{a_html(poda(cuerpo))}</div></section>')
    completo = dossier.html_completo()
    script = completo[completo.index('<script src="'):completo.rindex("</body>")]
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Namibia 2026 — la agenda</title>
<style>{tipos}</style><style>{CSS}</style></head><body>
{portada()}
{"".join(secciones)}
{script}
</body></html>"""


def main():
    salida_html = os.path.join(HERE, "agenda.html")
    salida_pdf = os.path.join(RAIZ, "agenda-namibia-2026.pdf")
    open(salida_html, "w", encoding="utf-8").write(html_completo())
    print(f"HTML: {os.path.getsize(salida_html) // 1024} KB · {len(dias())} días")
    if "--html" in sys.argv:
        return 0
    imprimir.a_pdf(salida_html, salida_pdf, margenes=MARGEN, espera=6,
                   izquierda="Namibia 2026 · la agenda, día a día", derecha=FECHA)
    n = imprimir.paginas(salida_pdf)
    print(f"\n{os.path.relpath(salida_pdf, RAIZ)} · {n} páginas · "
          f"{os.path.getsize(salida_pdf) // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
