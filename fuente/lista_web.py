"""El `17` como página para marcar: lista-de-equipaje.html.

La lista de equipaje se tacha a boli en el PDF; esto es lo mismo para el móvil. Sale del `17`
tal cual —nada se escribe a mano aquí—: cada `- [ ]` es una casilla, con su nombre a la vista
(lo que va antes de la primera raya) y el resto plegado; lo que no es casilla va como nota.

La página la publica Claude como Artifact: las marcas se guardan en su base de datos y las ven
los dos viajeros. Sin ella —o en la copia que la propia página deja descargar para usarla sin
conexión— se guardan en el navegador. La clave de cada casilla es el nombre del ítem, no su
posición: cambiar el detalle de un ítem no le quita la marca; cambiarle el nombre, sí.

Lo mismo vale para la compra grande del D1, que es la lista con casillas del `08`
(§«La lista de la compra grande del D1»): se corta desde su encabezado hasta el siguiente `###`
y sale como otra página, con su propio Artifact y su propia base de datos.

    python3 lista_web.py            -> las dos, en fuente/ (ignoradas por git)
    python3 lista_web.py equipaje   -> fuente/lista-de-equipaje.html
    python3 lista_web.py compra     -> fuente/lista-de-la-compra.html
"""
import html
import json
import os
import re
import sys
import unicodedata

from comun import RAIZ, md, marca_texto
import fecha

AQUI = os.path.dirname(os.path.abspath(__file__))
LISTAS = {
    "equipaje": {
        "fuente": "17-lista-de-equipaje.md",
        "salida": os.path.join(AQUI, "lista-de-equipaje.html"),
        "titulo_pagina": "Equipaje Namibia 2026",
        "clave": "lista17",
        "cuenta": "en su bulto",
        "descarga": "lista-de-equipaje-namibia-2026.html",
        "corte": None,                      # el documento entero
    },
    "compra": {
        "fuente": "08-comida-compras-y-regalos.md",
        "salida": os.path.join(AQUI, "lista-de-la-compra.html"),
        "titulo_pagina": "Compra D1 Namibia",
        "titulo": "La compra grande del D1",
        "clave": "compra08",
        "cuenta": "en el carro",
        "descarga": "lista-de-la-compra-namibia-2026.html",
        "corte": "#### ✅ La lista de la compra grande del D1",
    },
}
# La línea que enlaza el documento con su propia página: en la página sobra.
RE_ENLACE_PROPIO = re.compile(r"claude\.ai/artifact/")
SANGRIA = "      "   # la continuación de una casilla en el `17`


def slug(texto, largo=60):
    t = re.sub(r"\]\([^)]*\)", "]", texto)            # fuera las URL de los enlaces
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    return t[:largo].rstrip("-") or "item"


LARGO_TITULO = 110


def _corte(src, seps, desde=0):
    """La primera de `seps` que no caiga dentro de un enlace, un paréntesis o una negrita."""
    hondo, negrita, i = 0, False, 0
    while i < len(src):
        if src.startswith("**", i):
            negrita = not negrita
            i += 2
            continue
        if hondo == 0 and not negrita and i >= desde:
            for sep, salto in seps:
                if src.startswith(sep, i):
                    return i, salto
        c = src[i]
        if c in "([":
            hondo += 1
        elif c in ")]":
            hondo = max(0, hondo - 1)
        i += 1
    return None, 0


def parte_titulo(src):
    """El nombre del ítem: hasta la primera « — ». Si eso deja un título de párrafo, hasta el
    primer inciso o el primer punto."""
    def largo(t):
        return len(re.sub(r"\]\([^)]*\)|[*_`\[]", "", t))
    busca = src.replace("\n", " ")      # mismo largo: las posiciones valen para `src`
    i, salto = _corte(busca, [(" — ", 3)])
    if i is not None and largo(src[:i]) <= LARGO_TITULO:
        return src[:i].strip(), src[i + salto:].strip()
    i, salto = _corte(busca, [(" *(", 1), (". ", 1), (": ", 1)], desde=14)
    if i is not None and largo(src[:i]) <= LARGO_TITULO + 50:
        return src[:i].strip().rstrip(".:"), src[i + salto:].strip()
    return src.strip(), ""


def mermaid(h):
    def cambia(m):
        codigo = html.unescape(m.group(1))
        codigo = re.sub(r"^\s*%%\s*ancho\s*\n", "", codigo, flags=re.M)
        return f'<pre class="mermaid">{html.escape(codigo)}</pre>'
    return re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', cambia, h, flags=re.S)


def bloque(texto):
    return marca_texto(mermaid(md.render(texto)))


def sin_enlace_propio(lineas):
    """Quita la línea que apunta al Artifact, y el `>` vacío que la separaba, si lo hay."""
    fuera = []
    for n, l in enumerate(lineas):
        if RE_ENLACE_PROPIO.search(l):
            fuera.append(n)
            if n + 1 < len(lineas) and lineas[n + 1].strip() in (">", ""):
                fuera.append(n + 1)
    return [l for n, l in enumerate(lineas) if n not in fuera]


def lee(lista):
    nombre = lista["fuente"]
    lineas = open(os.path.join(RAIZ, nombre), encoding="utf-8").read().split("\n")
    # La cabecera: el título y la cita que la sigue.
    assert lineas[0].startswith("# "), f"el `{nombre[:2]}` ha perdido su título"
    cab, i = [], 1
    while i < len(lineas) and not lineas[i].startswith("---"):
        cab.append(lineas[i])
        i += 1
    cab = sin_enlace_propio(cab)
    if lista["corte"] is None:
        # La historia de la lista: lo que va tras el último `---`.
        ult = max(n for n, l in enumerate(lineas) if l.strip() == "---")
        historia = "\n".join(lineas[ult + 1:]).strip()
        cuerpo = lineas[i:ult]
    else:
        # Un trozo del documento: de su encabezado al siguiente `###` (o `##`, o `---`).
        desde = [n for n, l in enumerate(lineas) if l.startswith(lista["corte"])]
        assert len(desde) == 1, f"el `{nombre[:2]}` ha perdido «{lista['corte']}»: la lista se queda ciega"
        hasta = next(n for n in range(desde[0] + 1, len(lineas))
                     if re.match(r"^(#{2,3} |---\s*$)", lineas[n]))
        historia = ""
        cuerpo = lineas[desde[0]:hasta]
    cuerpo = sin_enlace_propio(cuerpo)

    secciones, sec, nota, vistos = [], None, [], {}

    def cierra_nota():
        if sec is not None and "\n".join(nota).strip():
            sec["bloques"].append(("nota", bloque("\n".join(nota))))
        nota.clear()

    n = 0
    while n < len(cuerpo):
        l = cuerpo[n]
        m = re.match(r"^(##+) (.*)", l)
        if m:
            cierra_nota()
            titulo = re.sub(r"^[^\wÀ-ÿ¿¡]+", "", m.group(2)).strip()
            sec = {"nivel": len(m.group(1)), "titulo": titulo, "id": slug(titulo, 40), "bloques": []}
            secciones.append(sec)
            n += 1
            continue
        # Una negrita sola en su párrafo es un subtítulo («Kit Deadvlei», «Lo que viene con
        # receta»): se queda a la vista aunque se oculten las notas.
        if (re.match(r"^\*\*[^*]+\*\*", l) and (n + 1 == len(cuerpo) or not cuerpo[n + 1].strip())
                and (not nota or not nota[-1].strip()) and len(l) < 220):
            cierra_nota()
            sec["bloques"].append(("sub", marca_texto(md.renderInline(l))))
            n += 1
            continue
        if l.strip() == "---":
            n += 1
            continue
        if l.startswith("- [ ] ") or l.startswith("- [x] "):
            cierra_nota()
            trozo = [l[6:]]
            n += 1
            while n < len(cuerpo):
                s = cuerpo[n]
                if s.startswith(SANGRIA) or (not s.strip() and n + 1 < len(cuerpo)
                                             and cuerpo[n + 1].startswith(SANGRIA)):
                    trozo.append(s[len(SANGRIA):] if s.startswith(SANGRIA) else "")
                    n += 1
                else:
                    break
            titulo, detalle = parte_titulo("\n".join(trozo))
            titulo = re.sub(r"\s*\n\s*", " ", titulo)
            clave = slug(re.sub(r"[*_`]", "", titulo))
            vistos[clave] = vistos.get(clave, 0) + 1
            if vistos[clave] > 1:
                clave += f"-{vistos[clave]}"
            sec["bloques"].append(("item", {
                "id": clave,
                "titulo": marca_texto(md.renderInline(titulo)),
                "detalle": bloque(detalle) if detalle else "",
            }))
            continue
        nota.append(l)
        n += 1
    cierra_nota()
    titulo_doc = lista.get("titulo") or re.sub(r"^#\s*\d+\s*·\s*", "", lineas[0]).strip()
    intro = bloque("\n".join(re.sub(r"^>\s?", "", x) for x in cab))
    return titulo_doc, intro, secciones, bloque(historia) if historia else ""


CSS = r"""
:root {
  /* Diseño: el del dossier (fuente/estilo/comun.css) llevado a pantalla — papel crema, tinta,
     óxido de acento, verde de las marcas. Una columna; cada casilla es una fila táctil. */
  --fondo: #F7F4ED; --papel: #FFFFFF; --tinta: #1D1A15; --tinta-2: #56514A; --tinta-3: #7D776E;
  --regla: #DAD5C9; --oxido: #9A3F20; --oxido-claro: #C2542F; --verde: #5F7043; --verde-bg: #EDF1E4;
  --rojo: #A32E28; --rojo-bg: #FBEDEB; --ambar: #8A6210; --ambar-bg: #FAF1DC; --azul: #2F6E8E;
  --azul-bg: #EAF1F5; --hecho: #9A958B;
  --serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --sans: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --fondo: #17150F; --papel: #211E18; --tinta: #ECE6D9; --tinta-2: #BDB6A8; --tinta-3: #8F887B;
  --regla: #3A352C; --oxido: #E08A62; --oxido-claro: #E08A62; --verde: #A9BC86; --verde-bg: #263020;
  --rojo: #EE8B82; --rojo-bg: #3A1F1C; --ambar: #E0B75E; --ambar-bg: #362B14; --azul: #8DC3DE;
  --azul-bg: #1A2A33; --hecho: #6F695E; color-scheme: dark } }
:root[data-theme="dark"] {
  --fondo: #17150F; --papel: #211E18; --tinta: #ECE6D9; --tinta-2: #BDB6A8; --tinta-3: #8F887B;
  --regla: #3A352C; --oxido: #E08A62; --oxido-claro: #E08A62; --verde: #A9BC86; --verde-bg: #263020;
  --rojo: #EE8B82; --rojo-bg: #3A1F1C; --ambar: #E0B75E; --ambar-bg: #362B14; --azul: #8DC3DE;
  --azul-bg: #1A2A33; --hecho: #6F695E; color-scheme: dark }

* { box-sizing: border-box; }
body { background: var(--fondo); color: var(--tinta); font-family: var(--serif); font-size: 16px;
  line-height: 1.5; margin: 0; }
.envoltura { max-width: 46rem; margin: 0 auto; padding-inline: 16px; padding-block: 1.5rem 4rem; }
a { color: var(--oxido); text-underline-offset: 2px; overflow-wrap: anywhere; }
a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible {
  outline: 2px solid var(--oxido-claro); outline-offset: 2px; }

header.cab .viaje { font-family: var(--sans); font-size: .78rem; font-weight: 700;
  letter-spacing: .14em; text-transform: uppercase; color: var(--oxido); margin: 0; }
header.cab h1 { font-family: var(--sans); font-weight: 700; font-size: clamp(1.9rem, 6vw, 2.6rem);
  line-height: 1.05; letter-spacing: -.02em; margin: .35rem 0 .9rem; text-wrap: balance; }
.intro { font-size: .95rem; color: var(--tinta-2); }
.intro p { margin: 0 0 .6rem; }
.intro details summary, .historia summary { font-family: var(--sans); font-size: .85rem;
  font-weight: 600; color: var(--tinta-2); cursor: pointer; }

.barra { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--fondo);
  border-bottom: 1px solid var(--regla); margin: 1.2rem -16px 0; padding: .7rem 16px .6rem; }
.cuenta { display: flex; align-items: baseline; gap: .6rem; flex-wrap: wrap; font-family: var(--sans); }
.cuenta .num { font-family: var(--mono); font-size: 1.35rem; font-weight: 600;
  font-variant-numeric: tabular-nums; }
.cuenta .de { color: var(--tinta-2); font-size: .9rem; }
.cuenta .modo { margin-left: auto; font-size: .78rem; color: var(--tinta-3); }
.cuenta .modo.compartido { color: var(--verde); }
.cuenta .modo.error { color: var(--rojo); }
.progreso { height: 6px; background: var(--regla); border-radius: 3px; overflow: hidden; margin: .45rem 0 .6rem; }
.progreso i { display: block; height: 100%; width: 0; background: var(--verde); transition: width .25s; }
.mandos { display: flex; gap: .5rem; flex-wrap: wrap; }
.mandos button { font-family: var(--sans); font-size: .85rem; font-weight: 600; padding: .4rem .75rem;
  border-radius: 999px; border: 1px solid var(--regla); background: var(--papel); color: var(--tinta);
  cursor: pointer; min-height: 2.25rem; }
.mandos button[aria-pressed="true"] { background: var(--tinta); color: var(--fondo); border-color: var(--tinta); }
.mandos .descarga { margin-left: auto; border-color: var(--oxido); color: var(--oxido); }
.aviso { font-family: var(--sans); font-size: .82rem; color: var(--tinta-2); margin: .5rem 0 0; }
.aviso:empty { display: none; }

nav.indice { display: flex; gap: .35rem; flex-wrap: wrap; margin: 1rem 0 .5rem; }
nav.indice a { font-family: var(--sans); font-size: .8rem; text-decoration: none; color: var(--tinta-2);
  padding: .2rem .55rem; border: 1px solid var(--regla); border-radius: 4px;
  font-variant-numeric: tabular-nums; }
nav.indice a b { color: var(--tinta); font-weight: 600; }
nav.indice a.llena { border-color: var(--verde); color: var(--verde); }

section.sec { margin-top: 2.2rem; scroll-margin-top: 9rem; }
section.sec > h2, section.sec > h3 { font-family: var(--sans); display: flex; align-items: baseline;
  gap: .6rem; margin: 0 0 .6rem; text-wrap: balance; }
section.sec > h2 { font-size: 1.35rem; border-bottom: 2px solid var(--tinta); padding-bottom: .3rem; }
section.sec > h3 { font-size: 1.1rem; border-bottom: 1px solid var(--regla); padding-bottom: .25rem; }
section.sec .parcial { margin-left: auto; font-family: var(--mono); font-size: .8rem; font-weight: 400;
  color: var(--tinta-3); font-variant-numeric: tabular-nums; white-space: nowrap; }

.nota { font-size: .93rem; color: var(--tinta-2); }
.nota p, .nota ul, .nota ol, .nota blockquote { margin: .5rem 0; }
.nota ul { padding-left: 1.2rem; }
.nota > p > strong:only-child { display: block; font-family: var(--sans); color: var(--tinta);
  font-size: 1rem; margin-top: 1.2rem; }
h4.sub { font-family: var(--sans); font-size: 1rem; font-weight: 400; color: var(--tinta-2);
  margin: 1.4rem 0 .3rem; }
h4.sub strong { color: var(--tinta); font-weight: 700; }
pre.mermaid { overflow-x: auto; background: var(--papel); border: 1px solid var(--regla);
  border-radius: 6px; padding: .6rem; font-size: .75rem; }
blockquote { margin: .6rem 0; padding: .1rem 0 .1rem .9rem; border-left: 3px solid var(--ambar);
  color: var(--tinta-2); }

ul.casillas { list-style: none; margin: .4rem 0; padding: 0; border-top: 1px solid var(--regla); }
li.item { display: grid; grid-template-columns: 2.75rem minmax(0, 1fr); align-items: start;
  border-bottom: 1px solid var(--regla); padding: .55rem 0; }
li.item input { appearance: none; -webkit-appearance: none; width: 1.6rem; height: 1.6rem; margin: .1rem 0 0 .2rem;
  border: 2px solid var(--tinta-2); border-radius: 4px; background: var(--papel); cursor: pointer;
  display: grid; place-content: center; }
li.item input::after { content: ""; width: .5rem; height: .9rem; border: solid var(--fondo);
  border-width: 0 3px 3px 0; transform: rotate(45deg) translate(-1px, -2px); opacity: 0; }
li.item input:checked { background: var(--verde); border-color: var(--verde); }
li.item input:checked::after { opacity: 1; }
li.item input:disabled { cursor: not-allowed; opacity: .6; }
li.item .tit { cursor: pointer; padding-top: .1rem; }
li.item.hecho .tit { color: var(--hecho); text-decoration: line-through;
  text-decoration-color: var(--tinta-3); }
li.item.hecho .tit a { color: var(--hecho); }
li.item details { grid-column: 2; margin-top: .25rem; }
li.item details summary { font-family: var(--sans); font-size: .8rem; color: var(--tinta-3);
  cursor: pointer; width: max-content; }
li.item details[open] summary { margin-bottom: .2rem; }
li.item .det { font-size: .9rem; color: var(--tinta-2); }
li.item .det p { margin: .35rem 0; }

ul.extras:empty { display: none; }
ul.extras { border-top: 0; }
li.item.extra { grid-template-columns: 2.75rem minmax(0, 1fr) auto; }
li.item .anadido { font-family: var(--sans); font-size: .68rem; font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; color: var(--azul); background: var(--azul-bg); border-radius: 3px;
  padding: .05rem .35rem; margin-left: .5rem; vertical-align: .1em; text-decoration: none; display: inline-block; }
button.quitar { font-family: var(--sans); font-size: .78rem; color: var(--tinta-3); background: none;
  border: 1px solid transparent; border-radius: 4px; padding: .25rem .5rem; cursor: pointer; align-self: start; }
button.quitar:hover { border-color: var(--regla); }
button.quitar.seguro { color: var(--rojo); border-color: var(--rojo); }
form.anadir { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: .4rem; margin: .7rem 0 0; }
form.anadir label { grid-column: 1 / -1; font-family: var(--sans); font-size: .78rem; color: var(--tinta-3); }
form.anadir input { font: inherit; font-size: .95rem; padding: .5rem .65rem; border: 1px solid var(--regla);
  border-radius: 6px; background: var(--papel); color: var(--tinta); min-width: 0; }
form.anadir button { font-family: var(--sans); font-weight: 600; font-size: .88rem; padding: .5rem .9rem;
  border-radius: 6px; border: 1px solid var(--oxido); background: var(--oxido); color: var(--papel); cursor: pointer; }
body.lectura form.anadir, body.lectura button.quitar { display: none; }
body.solo-lista .nota, body.solo-lista .intro .resto { display: none; }
body.pendiente li.item.hecho { display: none; }
body.pendiente section.sec.completa { display: none; }

.marca { display: inline-block; width: .62em; height: .62em; border-radius: 50%; vertical-align: .02em;
  margin: 0 .12em; border: 1.5px solid; }
.m-si  { background: var(--verde); border-color: var(--verde); }
.m-med { background: linear-gradient(90deg, var(--ambar) 50%, transparent 50%); border-color: var(--ambar); }
.m-no  { background: transparent; border-color: var(--tinta-3); }
.m-mal { background: transparent; border-color: var(--rojo); position: relative; }
.m-mal::after { content: ""; position: absolute; left: -.05em; top: .22em; width: .7em; height: 1.5px;
  background: var(--rojo); transform: rotate(-45deg); }
.et { font-family: var(--sans); font-size: .68rem; font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; padding: .05rem .35rem; border-radius: 3px; white-space: nowrap; }
.et-ok { background: var(--verde-bg); color: var(--verde); }
.et-no { background: var(--rojo-bg); color: var(--rojo); }
.et-duda { background: var(--ambar-bg); color: var(--ambar); }
.rot { font-family: var(--sans); font-size: .7rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .06em; color: var(--azul); margin-right: .3rem; }
.historia { margin-top: 3rem; font-size: .85rem; color: var(--tinta-3); }
@media (prefers-reduced-motion: reduce) { .progreso i { transition: none; } }
"""

JS = r"""
(function () {
  // Dos cosas se guardan: las marcas de las casillas (por su clave) y los ítems que
  // se añaden desde la página. Con la base de datos del Artifact, compartidas; sin ella —o en
  // la copia descargada—, en este navegador.
  var CLAVE = "@CLAVE@-marcas", CLAVE_EXTRA = "@CLAVE@-extras";
  var inicial = {};
  try { inicial = JSON.parse(document.getElementById("estado-inicial").textContent) || {}; } catch (e) {}
  var esCopia = document.documentElement.hasAttribute("data-copia");
  var marcas = {}, extras = {};
  var db = null;
  var modo = document.getElementById("modo"), aviso = document.getElementById("aviso");

  function lee(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function guarda() {
    try {
      localStorage.setItem(CLAVE, JSON.stringify(marcas));
      localStorage.setItem(CLAVE_EXTRA, JSON.stringify(extras));
    } catch (e) {}
  }
  marcas = lee(CLAVE) || inicial.marcas || {};
  extras = lee(CLAVE_EXTRA) || inicial.extras || {};

  function nuevoId() { return "x" + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

  function pintaExtras() {
    document.querySelectorAll("ul.extras").forEach(function (ul) { ul.textContent = ""; });
    Object.keys(extras).sort(function (a, b) {
      return (extras[a].cuando || "").localeCompare(extras[b].cuando || "");
    }).forEach(function (id) {
      var x = extras[id];
      var ul = document.querySelector('ul.extras[data-sec="' + x.sec + '"]') ||
               document.querySelector("ul.extras");
      if (!ul) return;
      var li = document.createElement("li");
      li.className = "item extra";
      var c = document.createElement("input");
      c.type = "checkbox"; c.className = "casilla"; c.dataset.extra = id;
      c.id = "c-" + id; c.setAttribute("aria-labelledby", "t-" + id);
      var t = document.createElement("div");
      t.className = "tit"; t.id = "t-" + id; t.textContent = x.texto;
      var q = document.createElement("button");
      q.type = "button"; q.className = "quitar"; q.dataset.extra = id; q.textContent = "Quitar";
      q.setAttribute("aria-label", "Quitar " + x.texto);
      var et = document.createElement("span");
      et.className = "anadido"; et.textContent = "añadido";
      t.appendChild(et);
      li.appendChild(c); li.appendChild(t); li.appendChild(q);
      ul.appendChild(li);
    });
  }

  function pinta() {
    var cajas = document.querySelectorAll("input.casilla"), hechas = 0;
    cajas.forEach(function (c) {
      var si = c.dataset.extra ? !!(extras[c.dataset.extra] || {}).hecho : !!marcas[c.dataset.id];
      c.checked = si;
      c.closest("li.item").classList.toggle("hecho", si);
      if (si) hechas++;
    });
    document.getElementById("num").textContent = hechas;
    document.getElementById("total").textContent = cajas.length;
    document.getElementById("barra-i").style.width = (cajas.length ? 100 * hechas / cajas.length : 0) + "%";
    document.querySelectorAll("section.sec").forEach(function (s) {
      var cs = s.querySelectorAll("input.casilla"), h = 0;
      cs.forEach(function (c) { if (c.checked) h++; });
      var p = s.querySelector(".parcial");
      if (p) p.textContent = cs.length ? h + "/" + cs.length : "";
      s.classList.toggle("completa", cs.length > 0 && h === cs.length);
      var a = document.querySelector('nav.indice a[href="#' + s.id + '"]');
      if (a && cs.length) {
        a.querySelector("b").textContent = h + "/" + cs.length;
        a.classList.toggle("llena", h === cs.length);
      }
    });
  }

  function todo() { pintaExtras(); pinta(); }

  function falla(e, deshaz) {
    deshaz(); todo();
    if (e && (e.code === "not_granted" || e.code === "permission_denied")) {
      document.body.classList.add("lectura");
      document.querySelectorAll("input.casilla").forEach(function (c) { c.disabled = true; });
      modo.textContent = "Solo lectura";
      aviso.textContent = "Puedes ver la lista pero no cambiarla: pide a quien la compartió permiso para editarla.";
    } else {
      aviso.textContent = "No se pudo guardar el cambio. Comprueba la conexión y vuelve a intentarlo.";
    }
  }

  function marca(c, si) {
    aviso.textContent = "";
    var ahora = new Date().toISOString();
    if (c.dataset.extra) {
      var id = c.dataset.extra, x = extras[id];
      if (!x) return;
      var antes = x.hecho;
      x.hecho = si; pinta();
      if (db) db.collection("extras").doc(id).update({ hecho: si, cuando_marca: ahora })
        .catch(function (e) { falla(e, function () { x.hecho = antes; }); });
      else guarda();
      return;
    }
    var k = c.dataset.id;
    if (si) marcas[k] = true; else delete marcas[k];
    pinta();
    if (db) db.collection("marcas").doc(k).set({ hecho: si, cuando: ahora })
      .catch(function (e) { falla(e, function () { if (si) delete marcas[k]; else marcas[k] = true; }); });
    else guarda();
  }

  document.addEventListener("change", function (ev) {
    var c = ev.target;
    if (c.matches && c.matches("input.casilla")) marca(c, c.checked);
  });
  document.addEventListener("click", function (ev) {
    var q = ev.target.closest && ev.target.closest("button.quitar");
    if (q) {
      // Primer toque: pide confirmación en el propio botón. Segundo: quita.
      if (q.dataset.seguro !== "1") {
        q.dataset.seguro = "1"; q.textContent = "¿Seguro?"; q.classList.add("seguro");
        setTimeout(function () { if (q.isConnected) { q.dataset.seguro = ""; q.textContent = "Quitar"; q.classList.remove("seguro"); } }, 4000);
        return;
      }
      var id = q.dataset.extra, guardado = extras[id];
      delete extras[id]; todo();
      if (db) db.collection("extras").doc(id).delete()
        .catch(function (e) { falla(e, function () { extras[id] = guardado; }); });
      else guarda();
      return;
    }
    var t = ev.target.closest && ev.target.closest("li.item .tit");
    if (t && !ev.target.closest("a")) {
      var c = t.closest("li.item").querySelector("input.casilla");
      if (c.disabled) return;
      c.checked = !c.checked;
      marca(c, c.checked);
    }
  });

  document.querySelectorAll("form.anadir").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var inp = f.querySelector("input"), texto = inp.value.trim();
      if (!texto) { inp.focus(); return; }
      var id = nuevoId(), x = { sec: f.dataset.sec, texto: texto.slice(0, 300), hecho: false,
                               cuando: new Date().toISOString() };
      extras[id] = x; inp.value = ""; todo();
      aviso.textContent = "Añadido a «" + f.dataset.nombre + "».";
      if (db) db.collection("extras").doc(id).set(x)
        .catch(function (e) { falla(e, function () { delete extras[id]; }); });
      else guarda();
    });
  });

  function interruptor(id, clase) {
    var b = document.getElementById(id);
    b.addEventListener("click", function () {
      var on = b.getAttribute("aria-pressed") !== "true";
      b.setAttribute("aria-pressed", on ? "true" : "false");
      document.body.classList.toggle(clase, on);
      try { localStorage.setItem(CLAVE + "-" + id, on ? "1" : ""); } catch (e) {}
    });
    try { if (localStorage.getItem(CLAVE + "-" + id)) b.click(); } catch (e) {}
  }
  interruptor("ver-pendiente", "pendiente");
  interruptor("ver-solo-lista", "solo-lista");

  modo.textContent = esCopia ? "Copia sin conexión · se guarda en este navegador"
                             : "Se guarda en este dispositivo";
  todo();

  if (esCopia || !window.claude || !window.claude.use) return;

  window.claude.use("db").then(function (d) {
    if (!d) return;
    db = d;
    modo.textContent = "Compartida · los dos veis lo mismo";
    modo.classList.add("compartido");
    function caida() {
      modo.textContent = "Sin conexión con la lista compartida";
      modo.classList.remove("compartido"); modo.classList.add("error");
    }
    db.collection("marcas").onSnapshot(function (snap) {
      marcas = {};
      snap.docs.forEach(function (doc) { var v = doc.data(); if (v && v.hecho) marcas[doc.id] = true; });
      pinta();
    }, caida);
    db.collection("extras").onSnapshot(function (snap) {
      extras = {};
      snap.docs.forEach(function (doc) { var v = doc.data(); if (v && v.texto) extras[doc.id] = Object.assign({}, v); });
      todo();
    }, caida);
  });

  window.claude.use("downloads").then(function (dl) {
    if (!dl) return;
    var b = document.getElementById("descarga");
    b.hidden = false;
    b.addEventListener("click", function () {
      var clon = document.documentElement.cloneNode(true);
      clon.setAttribute("data-copia", "");
      clon.querySelectorAll("script").forEach(function (s) {
        if (s.id !== "app" && s.id !== "estado-inicial") s.remove();
      });
      clon.querySelector("#estado-inicial").textContent = JSON.stringify({ marcas: marcas, extras: extras });
      clon.querySelectorAll("ul.extras").forEach(function (ul) { ul.textContent = ""; });
      clon.querySelectorAll("input.casilla").forEach(function (c) { c.removeAttribute("disabled"); });
      clon.querySelector("body").classList.remove("lectura");
      var bc = clon.querySelector("#descarga"); if (bc) bc.remove();
      dl.save({ filename: "@DESCARGA@",
                data: "<!doctype html>\n" + clon.outerHTML })
        .then(function () { aviso.textContent = "Copia guardada. Ábrela en el navegador del móvil: funciona sin conexión y guarda los cambios ahí."; })
        .catch(function (e) {
          if (e && e.code === "declined") return;
          aviso.textContent = "No se pudo descargar la copia (" + ((e && e.code) || "error") + ").";
        });
    });
  });
})();
"""


def escribe(lista):
    titulo, intro, secciones, historia = lee(lista)
    partes = []
    total = 0
    for s in secciones:
        h = "h2" if s["nivel"] == 2 else "h3"
        partes.append(f'<section class="sec" id="{s["id"]}"><{h}>{html.escape(s["titulo"])}'
                      f'<span class="parcial"></span></{h}>')
        abierto = False
        for tipo, b in s["bloques"]:
            if tipo == "item":
                if not abierto:
                    partes.append('<ul class="casillas">')
                    abierto = True
                total += 1
                det = (f'<details><summary>Detalles</summary><div class="det">{b["detalle"]}</div></details>'
                       if b["detalle"] else "")
                partes.append(
                    f'<li class="item"><input type="checkbox" class="casilla" id="c-{b["id"]}" '
                    f'data-id="{b["id"]}" aria-labelledby="t-{b["id"]}">'
                    f'<div class="tit" id="t-{b["id"]}">{b["titulo"]}</div>{det}</li>')
            else:
                if abierto:
                    partes.append("</ul>")
                    abierto = False
                partes.append(f'<h4 class="sub">{b}</h4>' if tipo == "sub" else f'<div class="nota">{b}</div>')
        if abierto:
            partes.append("</ul>")
        if any(t == "item" for t, _ in s["bloques"]):
            nombre = html.escape(s["titulo"].split(" — ")[0])
            partes.append(
                f'<ul class="casillas extras" data-sec="{s["id"]}"></ul>'
                f'<form class="anadir" data-sec="{s["id"]}" data-nombre="{nombre}">'
                f'<label for="a-{s["id"]}">Añadir a {nombre}</label>'
                f'<input id="a-{s["id"]}" type="text" maxlength="300" autocomplete="off" '
                f'placeholder="Algo que falta en la lista…">'
                f'<button type="submit">Añadir</button></form>')
        partes.append("</section>")
    indice = "".join(
        f'<a href="#{s["id"]}">{html.escape(s["titulo"])} <b></b></a>'
        for s in secciones if any(t == "item" for t, _ in s["bloques"]))
    js = JS.replace("@CLAVE@", lista["clave"]).replace("@DESCARGA@", lista["descarga"])
    pagina = f"""<title>{html.escape(lista["titulo_pagina"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">
<style>{CSS}</style>
<div class="envoltura">
<header class="cab">
  <p class="viaje">Namibia · {html.escape(fecha.VIAJE)}</p>
  <h1>{html.escape(titulo)}</h1>
  <div class="intro">
    <details class="resto"><summary>Cómo se usa esta lista, y las marcas ✅ ◐ ○ ❌</summary>{intro}</details>
  </div>
</header>
<div class="barra">
  <div class="cuenta"><span class="num" id="num">0</span><span class="de">de <span id="total">{total}</span> {html.escape(lista["cuenta"])}</span>
    <span class="modo" id="modo"></span></div>
  <div class="progreso" aria-hidden="true"><i id="barra-i"></i></div>
  <div class="mandos">
    <button type="button" id="ver-pendiente" aria-pressed="false">Solo lo que falta</button>
    <button type="button" id="ver-solo-lista" aria-pressed="false">Sin notas</button>
    <button type="button" id="descarga" class="descarga" hidden>Descargar para usar sin conexión</button>
  </div>
  <p class="aviso" id="aviso" role="status"></p>
</div>
<nav class="indice" aria-label="Secciones">{indice}</nav>
{"".join(partes)}
<details class="historia"><summary>De dónde sale esta lista</summary>{historia}
<p>Generada desde <code>{html.escape(lista["fuente"])}</code> el {html.escape(fecha.FECHA)}.</p></details>
</div>
<script type="application/json" id="estado-inicial">{{}}</script>
<script id="app">{js}</script>
"""
    pagina = marca_texto_seguro(pagina)
    with open(lista["salida"], "w", encoding="utf-8") as f:
        f.write(pagina)
    return lista["salida"], total


def marca_texto_seguro(pagina):
    """El resumen de la cabecera nombra las marcas con su emoji: se dibujan como en el resto."""
    return pagina.replace("las marcas ✅ ◐ ○ ❌", "las marcas " + marca_texto("✅ ◐ ○ ❌"))


if __name__ == "__main__":
    for clave in sys.argv[1:] or LISTAS:
        ruta, n = escribe(LISTAS[clave])
        print(f"{os.path.relpath(ruta)}: {n} casillas")
