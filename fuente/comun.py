# -*- coding: utf-8 -*-
"""Lo que comparten el dossier y la guia de fauna: Markdown, imagenes y marcas.

El grueso de este modulo es la conversion de emoji a tipografia. En pantalla los
emoji funcionan; en un PDF de cien paginas no: el navegador los mete como mapas de
bits en color, descuadran la linea base, engordan el fichero y en blanco y negro no
se distinguen. Aqui se traducen a tres cosas:

  · las cuatro marcas de fiabilidad (primaria, secundaria, practica comun, sin
    verificar) pasan a discos dibujados con CSS, que se leen igual en color y en gris;
  · los avisos (OJO, OBRAS, PROHIBIDO) pasan a etiquetas de texto;
  · los iconos que en el dia a dia encabezan una linea (sol, temperatura, cama,
    gasolina...) pasan a rotulos en versalita;
  · el resto, decorativo, se quita.
"""
import base64
import json
import os
import re

from markdown_it import MarkdownIt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, "img")

md = (MarkdownIt("commonmark", {"html": True, "linkify": False, "typographer": True})
      .enable("table").enable("strikethrough").enable("smartquotes"))

# ---------------------------------------------------------------------------
# Marcas de fiabilidad — el sistema de notacion del dossier
# ---------------------------------------------------------------------------

MARCAS = {
    "✅": ('<span class="marca m-si" title="fuente primaria"></span>', "fuente primaria"),
    "◐": ('<span class="marca m-med" title="secundaria concordante"></span>', "secundaria concordante"),
    "○": ('<span class="marca m-no" title="práctica común, sin fuente"></span>', "práctica común, sin fuente"),
    "❌": ('<span class="marca m-mal" title="sin verificar"></span>', "sin verificar"),
    "✔️": ('<span class="marca m-si"></span>', ""),
    "✓": ('<span class="marca m-si"></span>', ""),
}

AVISOS = {
    "⚠️": '<span class="et et-no">OJO</span>',
    "⚠": '<span class="et et-no">OJO</span>',
    "🚧": '<span class="et et-duda">OBRAS</span>',
    "🚫": '<span class="et et-no">PROHIBIDO</span>',
    "⛔": '<span class="et et-no">PROHIBIDO</span>',
    "🛑": '<span class="et et-no">ALTO</span>',
    "🚨": '<span class="et et-no">URGENTE</span>',
    "🔑": '<span class="et et-ok">CLAVE</span>',
}

# Iconos que en el dia a dia hacen de encabezado de linea.
ROTULOS = {
    "🌡️": "temperatura", "🌡": "temperatura",
    "☀️": "sol", "☀": "sol",
    "🌅": "amanecer", "🌇": "atardecer", "🌙": "noche",
    "🛏️": "dónde se duerme", "🛏": "dónde se duerme",
    "⛺": "camping", "🏕️": "camping", "🏕": "camping",
    "⛽": "gasolina",
    "🎫": "tasa", "🎟️": "tasa",
    "⏰": "horario",
    "🌧️": "lluvia", "🌧": "lluvia",
    "💱": "cambio",
    "📞": "teléfono",
}

FLECHAS = {"👉": "▸", "➡️": "→"}

# Todo lo demas es decoracion: fuera.
RE_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\u2190-\u21FF\u2300-\u23FF\u25A0-\u27BF"
    "\u2B00-\u2BFF\u2100-\u214F\u2600-\u26FF\uFE0F\u20E3"
    "\U0001F1E6-\U0001F1FF]\uFE0F?\u20E3?")

_CONSERVAR = {"→", "←", "↔", "—", "–", "·", "±", "≈", "×", "→"}


_UNIDADES = ["cero", "una", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
             "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
             "dieciocho", "diecinueve", "veinte", "veintiuna", "veintidós", "veintitrés",
             "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
_DECENAS = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta",
            80: "ochenta", 90: "noventa"}


def en_letras(n):
    """0-199 en letras (femenino: «ciento treinta y cinco especies»). Fuera de rango, la cifra."""
    if not 0 <= n < 200:
        return str(n)
    if n >= 100:
        resto = n - 100
        return "cien" if not resto else "ciento " + en_letras(resto)
    if n < 30:
        return _UNIDADES[n]
    d, u = divmod(n, 10)
    return _DECENAS[d * 10] + (f" y {_UNIDADES[u]}" if u else "")


def mil(n):
    """2728 -> «2.728»: punto de millar, que es lo que se usa en castellano."""
    return f"{n:,.0f}".replace(",", ".")


def marca_texto(html):
    """Sustituye emoji por tipografia. Trabaja sobre HTML ya renderizado."""
    for e, r in FLECHAS.items():
        html = html.replace(e + " ", r + " ").replace(e, r)
    for e, (r, _) in MARCAS.items():
        html = html.replace(e, r)
    for e, r in AVISOS.items():
        html = html.replace(e + " ", r + " ").replace(e, r)
    for e, r in ROTULOS.items():
        html = html.replace(e + " ", f'<span class="rot">{r}</span>').replace(
            e, f'<span class="rot">{r}</span>')

    def limpia(m):
        return "" if m.group(0)[0] not in _CONSERVAR else m.group(0)

    html = RE_EMOJI.sub(limpia, html)
    # los espacios dobles que deja quitar un emoji
    html = re.sub(r"(<(?:h[1-6]|p|li|strong|em|td|th)[^>]*>)\s+", r"\1", html)
    html = re.sub(r"[ \t]{2,}", " ", html)
    html = re.sub(r"\s+(</(?:h[1-6]|p|li|strong|em)>)", r"\1", html)
    return html


# ---------------------------------------------------------------------------
# Imagenes y creditos
# ---------------------------------------------------------------------------

def creditos():
    with open(os.path.join(IMG, "creditos.json")) as f:
        return json.load(f)


_cache_b64 = {}


def b64(ruta):
    if ruta not in _cache_b64:
        with open(ruta, "rb") as f:
            _cache_b64[ruta] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    return _cache_b64[ruta]


def img_lugar(slug):
    return b64(os.path.join(IMG, "lugares", slug + ".jpg"))


def img_fauna(slug):
    return b64(os.path.join(IMG, "fauna", slug + ".jpg"))


def tipografias(carpeta):
    """Empotra las woff2 de fuente/tipos como @font-face en base64.

    Van dentro del HTML para que el build no dependa de que fuentes tenga instaladas
    la maquina: el PDF sale identico en cualquier sitio.
    """
    fams = {"SourceSerif4": "Source Serif 4", "SourceSans3": "Source Sans 3",
            "IBMPlexMono": "IBM Plex Mono"}
    reglas = []
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".woff2"):
            continue
        base, peso, estilo, _sub = f[:-6].split("-", 3)
        with open(os.path.join(carpeta, f), "rb") as fh:
            d = base64.b64encode(fh.read()).decode()
        reglas.append(
            f"@font-face{{font-family:'{fams[base]}';font-style:{estilo};"
            f"font-weight:{peso};font-display:block;"
            f"src:url(data:font/woff2;base64,{d}) format('woff2')}}")
    return "".join(reglas)


def figura(slug, clase="media", pie=None):
    """<figure> con la foto, su pie y el credito obligatorio de la licencia."""
    cr = creditos().get("lugares/" + slug)
    if not cr:
        return ""
    return (f'<figure class="{clase}"><img src="{img_lugar(slug)}" alt="{cr["pie"]}">'
            f'<figcaption><span>{pie or cr["pie"]}</span>'
            f'<span class="credito">{cr["autor"]} · {cr["licencia"]}</span>'
            f'</figcaption></figure>')


def foto_plena(slug, pie=None):
    cr = creditos().get("lugares/" + slug)
    if not cr:
        return ""
    return (f'<section class="foto-plena"><img src="{img_lugar(slug)}" alt="{cr["pie"]}">'
            f'<figcaption><div class="pie-grande">{pie or cr["pie"]}</div>'
            f'<div class="credito">{cr["autor"]} · {cr["licencia"]} · Wikimedia Commons</div>'
            f'</figcaption></section>')
