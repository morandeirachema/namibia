#!/usr/bin/env python3
"""Monta TODO el repo en un solo HTML listo para imprimir a PDF, con fotos y diagramas."""
import base64, json, os, re, sys
from markdown_it import MarkdownIt

REPO = "/home/chema/code/Namibia"
HERE = os.path.dirname(os.path.abspath(__file__))
FAUNA = "/tmp/claude-1000/-home-chema-code-Namibia/e5fad87c-7d80-4b7a-9662-2ea2b9cf7cae/scratchpad/fauna"
sys.path.insert(0, FAUNA)
from especies import ID as FAUNA_ID
from etosha import DONDE as FAUNA_DONDE

md = MarkdownIt("commonmark", {"html": True, "linkify": False}).enable("table").enable("strikethrough")

fotos = {f["slug"]: f for f in json.load(open(os.path.join(HERE, "fotos.json")))}
fauna_man = json.load(open(os.path.join(FAUNA, "manifest.json")))

def b64(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

def foto_html(slug, clase="ancha"):
    f = fotos.get(slug)
    if not f:
        return ""
    src = b64(os.path.join(HERE, "img", f["local"]))
    return (f'<figure class="{clase}"><img src="{src}" alt="{f["pie"]}">'
            f'<figcaption>{f["pie"]}<span class="cr">{f["artist"]} · {f["license"]}</span>'
            f'</figcaption></figure>')

# doc -> fotos que lo abren o lo salpican
FOTOS_DOC = {
 "01-itinerarios-dia-a-dia.md": ["sossusvlei", "deadvlei", "walvisbay", "skeleton", "twyfelfontein", "okaukuejo"],
 "02-presupuesto.md":           ["hilux"],
 "03-alojamiento-y-tasas.md":   ["sesriem"],
 "04-guia-preparacion.md":      ["grava"],
 "05-equipaje.md":              [],
 "06-conduccion.md":            ["grava", "duna45"],
 "07-logistica.md":             ["solitaire"],
 "08-comida-compras-y-regalos.md": ["swakopmund"],
 "09-fauna-etosha.md":          ["etosha-pan"],
 "10-joyas-ocultas.md":         ["damaraland", "cielo"],
 "11-lista-google-maps.md":     ["capecross"],
 "12-hallazgos-verificados.md": [],
 "13-itinerario.md":            ["spreetshoogte"],
 "14-lluvias-historico.md":     ["termitero"],
 "15-huecos-cerrados.md":       [],
}

ORDEN = ["README.md"] + [f for f in sorted(os.listdir(REPO))
                         if re.match(r"\d\d-.*\.md$", f)]

GRUPOS = {
 "01-itinerarios-dia-a-dia.md": ("La ruta y el dinero", "Para decidir y reservar"),
 "04-guia-preparacion.md":      ("Preparar", "Antes de salir de casa"),
 "06-conduccion.md":            ("En ruta", "Lo que se consulta con el coche en marcha"),
 "12-hallazgos-verificados.md": ("El respaldo", "Por qué te puedes fiar de estos números"),
}

def a_html(texto):
    h = md.render(texto)
    # los bloques mermaid los pinta el navegador
    h = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',
               lambda m: '<pre class="mermaid">' + m.group(1)
                          .replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                          .replace("&quot;", '"') + "</pre>", h, flags=re.S)
    # enlaces internos entre documentos -> anclas del propio PDF
    h = re.sub(r'href="(\d\d-[a-z-]+)\.md"', r'href="#doc-\1"', h)
    h = h.replace('href="README.md"', 'href="#portada"')
    h = re.sub(r'href="guia-fauna-etosha\.pdf"', 'href="#fauna"', h)
    return h

partes = []
toc = []
for fich in ORDEN:
    texto = open(os.path.join(REPO, fich)).read()
    if fich == "README.md":
        # la portada la ponemos nosotros: se quita el titulo grande del README
        texto = re.sub(r"^<div align=\"center\">\n\n# 🇳🇦 NAMIBIA 2026\n", '<div align="center">\n', texto)
        partes.append(f'<section id="portada" class="doc">{a_html(texto)}</section>')
        toc.append(("portada", "Presentación", ""))
        continue

    ident = "doc-" + fich[:-3]
    titulo = texto.split("\n")[0].lstrip("# ").strip()
    toc.append((ident, titulo, ""))

    if fich in GRUPOS:
        g, sub = GRUPOS[fich]
        partes.append(f'<section class="separador"><div><span>{sub}</span><h1>{g}</h1></div></section>')

    fotos_doc = FOTOS_DOC.get(fich, [])
    cuerpo = a_html(texto)
    # la primera foto va tras el titulo; el resto, repartidas entre los <h2>
    if fotos_doc:
        cuerpo = re.sub(r"(</blockquote>)", r"\1" + foto_html(fotos_doc[0]), cuerpo, count=1)
        for i, slug in enumerate(fotos_doc[1:], start=1):
            partidas = cuerpo.split("<h2>")
            pos = min(i * max(len(partidas) // (len(fotos_doc)), 1), len(partidas) - 1)
            if pos > 0:
                partidas[pos] = partidas[pos] + foto_html(slug, "media")
            cuerpo = "<h2>".join(partidas)
    partes.append(f'<section id="{ident}" class="doc">{cuerpo}</section>')

# ---------- la guia de fauna, incrustada ----------
def negrita(t):
    t = t.replace("⚠️ ", '<b class="ojo">OJO</b> ').replace("⚠️", '<b class="ojo">OJO</b> ')
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"(?<![\w*])\*(?!\*)(.+?)(?<!\*)\*(?![\w*])", r"<em>\1</em>", t)

def ficha(m):
    src = b64(os.path.join(FAUNA, "img", m["local"]))
    d = FAUNA_DONDE.get(m["slug"], "")
    bloque = f'<p class="donde"><span class="et">Etosha</span> {negrita(d)}</p>' if d else ""
    return (f'<article class="sp"><div class="foto"><img src="{src}"></div><div class="txt">'
            f'<h3>{m["es"]}</h3><p class="nom"><em>{m["sci"]}</em> · {m["en"]}</p>'
            f'<p class="id">{negrita(FAUNA_ID.get(m["slug"], ""))}</p>{bloque}</div>'
            f'<p class="cred">Foto: {m["artist"] or "autor no indicado"} · {m["license"]}</p></article>')

SECC = [("mamifero", "Mamíferos"), ("ave", "Aves"), ("reptil", "Reptiles"),
        ("costa", "La costa, la roca y la arena"), ("bicho", "Bichos")]
fauna_html = ['<section class="separador"><div><span>Guía de campo</span><h1>Fauna del viaje</h1></div></section>',
              f'<section id="fauna" class="doc"><h1>Fauna — {len(fauna_man)} especies con foto</h1>'
              '<blockquote><p>La guía de campo completa, la misma que va suelta en '
              '<code>guia-fauna-etosha.pdf</code> para imprimir aparte. Cada ficha: nombre en castellano, '
              'científico e inglés, cómo reconocerla y —donde hay fuente— dónde y cuándo verla.</p></blockquote>']
for clave, nombre in SECC:
    grupo = [m for m in fauna_man if m["grupo"] == clave and "local" in m]
    fauna_html.append(f'<h2>{nombre} <span class="cuenta">{len(grupo)} especies</span></h2>')
    fauna_html.append('<div class="grid">' + "".join(ficha(m) for m in grupo) + "</div>")
fauna_html.append("</section>")

# ---------- creditos ----------
cred_lugares = "".join(f"<li><b>{f['pie']}</b> — {f['artist']}, <i>{f['license']}</i></li>"
                       for f in fotos.values())
cred_fauna = "".join(f"<li><b>{m['es']}</b> — {m['artist'] or 'autor no indicado'}, <i>{m['license']}</i></li>"
                     for m in fauna_man if "local" in m)

toc_html = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in toc) + '<li><a href="#fauna">Fauna del viaje — 83 especies</a></li>'

CSS = open(os.path.join(HERE, "estilo.css")).read()
HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Namibia 2026 — el dossier completo</title><style>{CSS}</style></head><body>

<section class="portada">
  <img class="fondo" src="{b64(os.path.join(HERE, 'img', 'deadvlei.jpg'))}">
  <div class="velo"></div>
  <div class="txt">
    <div class="kicker">Dossier de viaje · verificado contra fuentes primarias</div>
    <h1>Namibia<br>2026</h1>
    <h2>El gran roadtrip del norte</h2>
    <div class="datos">
      Dos personas · un 4x4 con tienda de techo · <b>31 de octubre – 15 de noviembre</b><br>
      Desierto → costa → Damaraland → <b>cuatro noches dentro de Etosha</b><br>
      ~2.600 km · ~€3.306 por persona, todo incluido
    </div>
    <div class="pie">{len(ORDEN)} documentos · 72 diagramas · {len(fauna_man)} especies con foto<br>
    Todas las fotografías, de Wikimedia Commons con licencia libre · 03·08·2026</div>
  </div>
</section>

<section class="doc toc">
  <h1>Qué hay aquí dentro</h1>
  <ol>{toc_html}</ol>
  <p class="nota">Los documentos van numerados por <b>el momento en que se usan</b>, no por el orden
  en que se investigaron: primero la ruta y el dinero, luego lo de preparar en casa, después lo que
  se consulta con el coche en marcha, y al final el respaldo de por qué los números son fiables.</p>
</section>

{"".join(partes)}
{"".join(fauna_html)}

<section class="doc creditos">
  <h1>Créditos de las fotografías</h1>
  <p class="nota">Todas de <b>Wikimedia Commons</b>, con licencia libre (CC BY, CC BY-SA, CC0 o
  dominio público), que exige citar autor y licencia — es lo que hace esta lista.</p>
  <h2>Los lugares</h2><ul class="dos">{cred_lugares}</ul>
  <h2>La fauna</h2><ul class="dos">{cred_fauna}</ul>
</section>

<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, securityLevel:'loose', theme:'base',
  themeVariables:{{fontSize:'13px', fontFamily:'DejaVu Sans, Arial, sans-serif'}}, flowchart:{{useMaxWidth:true}}}});</script>
</body></html>"""

out = os.path.join(HERE, "dossier.html")
open(out, "w").write(HTML)
print(f"HTML: {len(HTML)//1024} KB · {len(ORDEN)} documentos · {len(fauna_man)} especies · {len(fotos)} fotos de lugares")
