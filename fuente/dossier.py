#!/usr/bin/env python3
"""Arma el dossier completo: HTML de una pieza y, de ahi, el PDF.

Dos pasadas: la primera para maquetar y averiguar en que pagina cae cada documento,
la segunda para escribir esos numeros en el indice. Es la unica forma honesta de tener
un indice con paginas — donde cae cada salto lo decide el maquetador, no nosotros.

Uso:
    python3 fuente/dossier.py            # HTML + PDF (dos pasadas)
    python3 fuente/dossier.py --html     # solo el HTML, para mirarlo en el navegador
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import comun                                                       # noqa: E402
import imprimir                                                    # noqa: E402
import mapa                                                        # noqa: E402
import trazado                                                     # noqa: E402
from comun import RAIZ, marca_texto, md                            # noqa: E402

FECHA = "5 de agosto de 2026"

# ---------------------------------------------------------------------------
# Estructura del volumen
# ---------------------------------------------------------------------------

BLOQUES = [
    {"desde": "01", "titulo": "La ruta y el dinero", "epi": "Bloque uno",
     "lema": "Para decidir y reservar: el día a día, lo que cuesta y dónde se duerme.",
     "foto": "sossusvlei"},
    {"desde": "04", "titulo": "Preparar", "epi": "Bloque dos",
     "lema": "Lo que hay que resolver antes de salir de casa, con sus plazos.",
     "foto": "hilux"},
    {"desde": "06", "titulo": "En ruta", "epi": "Bloque tres",
     "lema": "Lo que se consulta con el coche en marcha: conducir, repostar, comer, mirar.",
     "foto": "grava"},
    {"desde": "12", "titulo": "El respaldo", "epi": "Bloque cuatro",
     "lema": "Por qué te puedes fiar de estos números: las fuentes, una por una.",
     "foto": "etosha-pan-satelite"},
]

# Fotos que salpican cada documento, en orden de aparicion.
FOTOS = {
    "01": ["namib-paisaje", "deadvlei", "walvisbay", "skeleton", "twyfelfontein", "okaukuejo"],
    "02": ["hilux"],
    "03": ["sesriem", "terracebay"],
    "04": ["windhoek"],
    "05": [],
    "06": ["grava", "saltroad"],
    "07": ["solitaire"],
    "08": ["swakopmund", "joes"],
    "09": ["etosha-elefantes", "etosha-rino"],
    "10": ["circulos", "cielo", "welwitschia"],
    "11": ["capecross"],
    "12": [],
    "13": ["spreetshoogte", "grootberg"],
    "14": ["termitero"],
    "15": [],
}

# Fotos a pagina completa, antes del documento que abren.
PLENAS = {
    "01": ("duna45", "Duna 45 al amanecer. El D4 empieza una hora antes que para todos "
                     "los demás: la puerta interior de Sesriem abre solo para quien duerme dentro."),
    "09": ("etosha-jirafas", "Etosha al atardecer. Cuatro noches dentro del parque, "
                             "tres campamentos y una charca iluminada en cada uno."),
}

RESUMEN = {
    "01": "La ruta desarrollada día por día: qué se conduce, a qué hora sale y se pone el sol, "
          "qué temperatura hace donde se duerme y qué cuesta cada noche.",
    "02": "El total partida a partida, lo que ya está cerrado con precio real y lo que sigue "
          "siendo estimación.",
    "03": "Tarifas oficiales de NWR para el año tarifario 2026/2027 y tasas de parque.",
    "04": "La cuenta atrás: el e-visa, las vacunas, el permiso de conducir y los plazos que vencen.",
    "05": "El petate que dictan los datos: qué llevar, qué dejar y los tres micro-kits.",
    "06": "El vuelco, el contrato, las presiones, la arena y las puertas de Sesriem.",
    "07": "Gasolineras, dinero, cobertura y emergencias.",
    "08": "El súper parada a parada, la ley del alcohol, dónde comer y la aduana.",
    "09": "Cómo funciona el safari en seco, y la guía de campo de 83 especies.",
    "10": "Los Lone Stone Men, la cascada del Uniab, los círculos de hadas.",
    "11": "Lo que cuesta entrar en cada sitio, y qué quedó fuera de la lista de pines.",
    "12": "Lo que superó la verificación a tres votos, y lo que quedó refutado.",
    "13": "Distancias, firme y viabilidad — con el contraste de OSRM.",
    "14": "Cinco temporadas de lluvia en Etosha, milímetro a milímetro.",
    "15": "El cuaderno de bitácora: temperaturas de estación, viento, luz, vuelos, tasas y lodges.",
}


def documentos():
    return sorted(f for f in os.listdir(RAIZ) if re.match(r"\d\d-.*\.md$", f))


def num(fich):
    return fich[:2]


def titulo_de(texto):
    return texto.split("\n", 1)[0].lstrip("# ").strip()


# ---------------------------------------------------------------------------
# Markdown -> HTML del dossier
# ---------------------------------------------------------------------------

def a_html(texto, doc=None):
    h = md.render(texto)

    # los bloques mermaid los pinta el navegador: se devuelve el codigo sin escapar
    def desescapa(m):
        c = (m.group(1).replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"'))
        return '<pre class="mermaid">' + c + "</pre>"

    h = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', desescapa, h, flags=re.S)

    # enlaces entre documentos -> anclas internas del propio PDF
    h = re.sub(r'href="(\d\d)-[a-z-]+\.md"', r'href="#doc-\1"', h)
    h = h.replace('href="README.md"', 'href="#presentacion"')
    h = re.sub(r'href="guia-fauna-etosha\.pdf"', 'href="#fauna"', h)
    h = re.sub(r'href="dossier-namibia-2026\.pdf"', 'href="#portada"', h)

    h = marca_texto(h)

    # las referencias sueltas a otro documento («ver `13`») se hacen enlace
    if doc:
        h = re.sub(r"<code>(\d\d)</code>",
                   lambda m: f'<a href="#doc-{m.group(1)}"><code>{m.group(1)}</code></a>', h)
    return h


def reparte_fotos(cuerpo, slugs):
    """Mete las fotos delante de los <h2>, repartidas de forma pareja por el documento.

    Cada foto va en un hueco distinto: si dos cayeran en el mismo se solaparian las
    etiquetas y saldria HTML invalido, y con HTML invalido el navegador ensancha la
    pagina y encoge el documento entero al imprimirlo.
    """
    if not slugs:
        return cuerpo
    partes = cuerpo.split("<h2")
    huecos = len(partes) - 1
    if huecos == 0:
        return cuerpo + "".join(comun.figura(s, "media") for s in slugs)

    slugs = slugs[:huecos]
    paso = huecos / len(slugs)
    destino = {min(huecos, 1 + int(i * paso)): s for i, s in enumerate(slugs)}

    salida = [partes[0]]
    primero = min(destino)
    for i, p in enumerate(partes[1:], start=1):
        if i in destino:
            salida.append(comun.figura(destino[i], "media" if i == primero else "baja"))
        salida.append("<h2" + p)
    return "".join(salida)


# ---------------------------------------------------------------------------
# Piezas del volumen
# ---------------------------------------------------------------------------

def portada(total_paginas=None):
    cr = comun.creditos()["lugares/portada"]
    pie_izq = f"{len(documentos())} documentos · 83 especies con foto · 2 mapas"
    pie_der = f"Fotografía de portada: {cr['autor']} · {cr['licencia']}"
    return f"""
<section class="portada" id="portada">
  <img src="{comun.img_lugar('portada')}" alt="{cr['pie']}">
  <div class="velo"></div>
  <div class="marca">Dossier de viaje<span>Actualizado el {FECHA}</span></div>
  <div class="txt">
    <h1>Namibia<em>2026</em></h1>
    <div class="regla"></div>
    <p class="lema">El gran roadtrip del norte: las dunas más altas del mundo al amanecer,
    la Costa de los Esqueletos y cuatro noches dentro de Etosha.</p>
    <div class="datos">
      Dos personas · un 4×4 con tienda de techo · <b>31 de octubre – 15 de noviembre</b><br>
      Desierto → costa → Damaraland → <b>cuatro noches dentro de Etosha</b><br>
      ~2.700 km · <b>~€3.306 por persona</b>, todo incluido
    </div>
    <div class="pie"><span>{pie_izq}</span><span>{pie_der}</span></div>
  </div>
</section>"""


def separador(b):
    cr = comun.creditos()["lugares/" + b["foto"]]
    return f"""
<section class="separador">
  <img src="{comun.img_lugar(b['foto'])}" alt="{cr['pie']}">
  <div class="velo"></div>
  <div class="txt">
    <div class="epi">{b['epi']}</div>
    <h1>{b['titulo']}</h1>
    <p>{b['lema']}</p>
  </div>
</section>"""


def ancla(doc):
    """Testigo invisible para localizar la pagina del documento en el PDF ya maquetado."""
    return f'<span class="ancla">xqpagina{doc}</span>'


def indice(paginas):
    grupos, actual = [], None
    for f in documentos():
        n = num(f)
        for b in BLOQUES:
            if b["desde"] == n:
                actual = b["titulo"]
                grupos.append((actual, []))
        grupos[-1][1].append((n, titulo_de(open(os.path.join(RAIZ, f)).read())))

    filas = []
    for nombre, docs in grupos:
        filas.append(f'<div class="grupo">{nombre}</div><ol>')
        for n, t in docs:
            t = marca_texto(t)
            t = re.sub(r"^\d\d\s*·\s*", "", t)
            p = paginas.get("doc" + n, "")
            filas.append(
                f'<li><span class="n">{n}</span>'
                f'<span class="t">{t}<small>{RESUMEN.get(n, "")}</small></span>'
                f'<span class="puntos"></span><span class="p">{p}</span></li>')
        filas.append("</ol>")

    extra = []
    for clave, nombre in [("mapas", "Los mapas: la ruta y las charcas de Etosha"),
                          ("presentacion", "El viaje de un vistazo"),
                          ("fauna", "Guía de campo — 83 especies con foto"),
                          ("creditos", "Créditos de las fotografías")]:
        p = paginas.get(clave, "")
        extra.append(f'<li><span class="n"></span><span class="t">{nombre}</span>'
                     f'<span class="puntos"></span><span class="p">{p}</span></li>')

    return f"""
<section class="indice" id="indice">
  <h1>Qué hay aquí dentro</h1>
  <div class="grupo">Antes de empezar</div><ol>{"".join(extra[:2])}</ol>
  {"".join(filas)}
  <div class="grupo">Al final</div><ol>{"".join(extra[2:])}</ol>
  <p class="nota">Los documentos van numerados por <b>el momento en que se usan</b>, no por el
  orden en que se investigaron: primero la ruta y el dinero, luego lo que hay que preparar en
  casa, después lo que se consulta con el coche en marcha, y al final el respaldo de por qué
  estos números son fiables. <b>Las cuatro marcas</b> que verás por todo el dossier:
  <span class="marca m-si"></span> fuente primaria ·
  <span class="marca m-med"></span> secundaria concordante ·
  <span class="marca m-no"></span> práctica común, sin fuente ·
  <span class="marca m-mal"></span> sin verificar, dicho en blanco.</p>
</section>"""


def paginas_de_mapas():
    datos = {e["id"]: e for e in mapa.carga("ruta.json")}
    filas = []
    for e in trazado.ETAPAS:
        d = datos.get(e["id"], {})
        km = d.get("km")
        duerme = trazado.PUNTOS[e["duerme"]][2] if e["duerme"] else "—"
        color = trazado.COLOR_BLOQUE[e["bloque"]]
        filas.append(
            f'<tr><td class="dia"><span class="pip" style="background:{color}"></span>'
            f'{e["id"]}</td><td class="fec">{e["fecha"]}</td><td>{e["titulo"]}</td>'
            f'<td class="km">{"—" if not km else f"{km:.0f} km"}</td>'
            f'<td class="dor">{duerme}</td></tr>')
    total = sum(d.get("km") or 0 for d in datos.values())

    return f"""
<section class="mapa-plena" id="mapas">
  <h1 class="titulo">La ruta, en el mapa</h1>
  <div class="mapa">{mapa.mapa_ruta()}
    <figcaption>Trazado real de carretera, calculado con <b>OSRM</b> sobre OpenStreetMap a
    partir de las coordenadas de cada parada. Los contornos son de <b>Natural Earth</b>
    (dominio público). La suma de las catorce etapas da <b>{total:.0f} km</b>, que cuadra con
    los ~2.600 km medidos aparte en <a href="#doc-13"><code>13</code></a>.</figcaption>
  </div>
</section>

<section class="mapa-plena">
  <h1 class="titulo">Las catorce etapas</h1>
  <table class="etapas">
    <thead><tr><th>Día</th><th>Fecha</th><th>Etapa</th><th class="km">Carretera</th>
    <th>Dónde se duerme</th></tr></thead>
    <tbody>{"".join(filas)}</tbody>
    <tfoot><tr><td colspan="3">Total conducido</td><td class="km">{total:.0f} km</td>
    <td>13 noches</td></tr></tfoot>
  </table>
  <p class="nota-tabla">Los kilómetros de esta tabla son <b>de carretera, puerta a puerta</b>,
  medidos con OSRM sobre el trazado de OpenStreetMap el 4 de agosto de 2026. No incluyen los
  desvíos a charcas dentro de Etosha ni las vueltas del día de descanso.</p>

  <div class="mapa">{mapa.mapa_etosha()}
    <figcaption><b>Etosha, charca a charca.</b> En seca la fauna no está repartida por el
    parque: está en el agua. Las charcas, las pistas y el límite del parque salen de
    OpenStreetMap; el relleno blanco es la depresión, que en noviembre está seca —y por eso
    el safari funciona. Los círculos huecos son sondeos con bomba: los que aguantan cuando
    las charcas naturales se secan.</figcaption>
  </div>
</section>"""


def cuerpo_documentos():
    partes = []
    for f in documentos():
        n = num(f)
        texto = open(os.path.join(RAIZ, f)).read()

        for b in BLOQUES:
            if b["desde"] == n:
                partes.append(separador(b))

        if n in PLENAS:
            slug, pie = PLENAS[n]
            partes.append(comun.foto_plena(slug, pie))

        html = a_html(texto, doc=n)
        # el primer <h1> se convierte en titulo de documento
        html = re.sub(r"<h1>(.*?)</h1>",
                      lambda m: f'<h1 class="titulo">{m.group(1)}{ancla(n)}</h1>', html, count=1)
        html = reparte_fotos(html, FOTOS.get(n, []))
        partes.append(f'<section class="doc" id="doc-{n}">{html}</section>')
    return "".join(partes)


def presentacion():
    texto = open(os.path.join(RAIZ, "README.md")).read()
    # el titulo y el bloque de descarga del PDF no pintan nada dentro del propio PDF
    texto = re.sub(r'^<div align="center">\n\n# 🇳🇦 NAMIBIA 2026\n', '<div align="center">\n', texto)
    texto = re.sub(r"### 📕 \[\*\*Descargar.*?\n\n.*?\n\n", "", texto, flags=re.S)
    h = a_html(texto)
    h = re.sub(r"<h2>", '<h2 class="pres">', h)
    return (f'<section class="doc" id="presentacion">'
            f'<h1 class="titulo">El viaje de un vistazo{ancla("RM")}</h1>{h}</section>')


def fauna():
    import guia_fauna
    return guia_fauna.seccion_embebida(ancla("FA"))


def creditos_seccion():
    cr = comun.creditos()
    lug = "".join(f'<li><b>{v["pie"]}</b> — {v["autor"]}, <i>{v["licencia"]}</i></li>'
                  for k, v in sorted(cr.items()) if k.startswith("lugares/"))
    fau = "".join(f'<li><b>{v["es"]}</b> — {v["autor"]}, <i>{v["licencia"]}</i></li>'
                  for k, v in sorted(cr.items(), key=lambda x: x[1].get("es", ""))
                  if k.startswith("fauna/"))
    return f"""
<section class="doc sin-columnas creditos" id="creditos">
  <h1 class="titulo">Créditos de las fotografías{ancla('CR')}</h1>
  <p class="nota">Las {len(cr)} fotografías de este dossier proceden de <b>Wikimedia
  Commons</b> y están bajo licencia libre (CC BY, CC BY-SA, CC0 o dominio público), que exige
  citar autor y licencia — es lo que hace esta lista. El fichero exacto de cada una está en
  <code>fuente/catalogo.py</code>, y <code>fuente/descargar.py</code> rechaza cualquier imagen
  cuya licencia no sea libre.</p>
  <h2>Los lugares y los mapas</h2><ul class="dos">{lug}</ul>
  <h2>La fauna</h2><ul class="dos">{fau}</ul>
  <h2>Los mapas</h2>
  <ul class="dos">
    <li><b>Contornos de países</b> — Natural Earth 1:10M, <i>dominio público</i></li>
    <li><b>Límites de parques, pistas, charcas y campamentos</b> — OpenStreetMap,
        <i>ODbL</i> © colaboradores de OpenStreetMap</li>
    <li><b>Trazado de carretera de la ruta</b> — OSRM sobre datos de OpenStreetMap, <i>ODbL</i></li>
  </ul>
</section>"""


# ---------------------------------------------------------------------------
# Montaje
# ---------------------------------------------------------------------------

EXTRA_CSS = """
/* Testigo invisible para localizar la pagina en el PDF ya maquetado. Va en
   blanco y con el interletraje a cero: con el negativo del titular los glifos
   se solapan y pdftotext los devuelve desordenados. */
.ancla { font-size: 6pt; color: #fff; letter-spacing: 0; font-family: var(--mono);
         font-weight: 400; }
table.etapas { font-size: 8.6pt; margin-top: 2mm; }
table.etapas td.dia { font-family: var(--sans); font-weight: 700; white-space: nowrap; }
table.etapas td.fec { color: var(--tinta-2); white-space: nowrap; }
table.etapas td.km  { text-align: right; font-family: var(--sans); font-weight: 600;
                      white-space: nowrap; }
table.etapas th.km  { text-align: right; }
table.etapas td.dor { font-weight: 600; }
table.etapas tfoot td { border-top: 1pt solid var(--regla-2); border-bottom: 0;
                        font-family: var(--sans); font-weight: 700; padding-top: 2mm; }
table.etapas tfoot td.km { text-align: right; }
.pip { display: inline-block; width: 2mm; height: 2mm; border-radius: 50%;
       margin-right: 1.4mm; vertical-align: -.1mm; }
.nota-tabla { font-size: 8pt; color: var(--tinta-2); margin: 3mm 0 6mm;
              padding-left: 3mm; border-left: 2pt solid var(--regla); }
.mapa-plena h1.titulo { font-size: 19pt; }
"""


def html_completo(paginas=None):
    css = open(os.path.join(HERE, "estilo", "dossier.css")).read() + EXTRA_CSS
    tipos = comun.tipografias(os.path.join(HERE, "tipos"))
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Namibia 2026 — el dossier del viaje</title>
<style>{tipos}</style><style>{css}</style></head><body>
{portada()}
{indice(paginas or {})}
{paginas_de_mapas()}
{presentacion()}
{cuerpo_documentos()}
{fauna()}
{creditos_seccion()}
<script src="{VENDOR}"></script>
<script>
mermaid.initialize({{startOnLoad:true, securityLevel:'loose', theme:'base',
  themeVariables:{{
    fontFamily:'Source Sans 3, Helvetica, Arial, sans-serif', fontSize:'13px',
    primaryColor:'#F7F4ED', primaryTextColor:'#16130F', primaryBorderColor:'#C6C1B4',
    lineColor:'#7D776E', tertiaryColor:'#EFEAE0'
  }},
  flowchart:{{useMaxWidth:true, htmlLabels:true, curve:'basis'}},
  gantt:{{useMaxWidth:true}}, pie:{{useMaxWidth:true}}}});
</script>
</body></html>"""


VENDOR = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"

MARCAS_PAGINA = dict(
    {"doc" + num(f): f"xqpagina{num(f)}" for f in documentos()},
    presentacion="xqpaginaRM", fauna="xqpaginaFA", creditos="xqpaginaCR",
    mapas="La ruta, en el mapa")



def main():
    salida_html = os.path.join(HERE, "dossier.html")
    salida_pdf = os.path.join(RAIZ, "dossier-namibia-2026.pdf")

    open(salida_html, "w").write(html_completo())
    print(f"HTML: {os.path.getsize(salida_html) // 1024} KB")
    if "--html" in sys.argv:
        return 0

    print("Pasada 1 · maquetando para saber las páginas…")
    imprimir.a_pdf(salida_html, salida_pdf, izquierda="Namibia 2026 · el dossier del viaje",
                   derecha=FECHA, espera=6)
    paginas = imprimir.indice_de_paginas(salida_pdf, MARCAS_PAGINA)
    faltan = [k for k in MARCAS_PAGINA if k not in paginas]
    if faltan:
        print(f"   aviso: sin página para {', '.join(faltan)}")
    print("Pasada 2 · escribiendo los números en el índice…")
    open(salida_html, "w").write(html_completo(paginas))
    imprimir.a_pdf(salida_html, salida_pdf, izquierda="Namibia 2026 · el dossier del viaje",
                   derecha=FECHA, espera=6)
    n = imprimir.paginas(salida_pdf)
    print(f"\n{os.path.relpath(salida_pdf, RAIZ)} · {n} páginas · "
          f"{os.path.getsize(salida_pdf) // 1024 // 1024} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
