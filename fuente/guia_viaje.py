#!/usr/bin/env python3
"""La guía de viaje: el dossier que se lleva en la mano en Namibia, sin precios ni reservas,
y con la guía de campo de fauna detrás.

El dossier entero son doscientas páginas y la mitad son de antes de salir: el presupuesto,
las tarifas, las reservas, la preparación, el equipaje, la investigación. En la guantera
solo hace falta lo que se consulta con el coche en marcha. Esto es eso:

  · la ruta: el mapa, las quince etapas, el mapa de Etosha y el día a día del `01`;
  · al volante y en el campamento: el `06`, el `18`, el `21`, el `22` y el `23`;
  · por el camino: el `07`, el `08`, el `19` y el `10`;
  · y al final, la guía de campo entera: cómo se usa y las fichas.

Nada se escribe a mano: es el MISMO markdown que el dossier, con las secciones de dinero,
de reservas y de deliberación fuera (`SECCIONES_FUERA`) y, dentro de lo que queda, cada
precio y cada estado de reserva cortados frase a frase por `sin_precios.py`. Lo que se
cambia en un `.md` cambia aquí al regenerar.

    python3 guia_viaje.py            HTML + PDF (dos pasadas, por el índice)
    python3 guia_viaje.py --html     solo el HTML, para mirarlo en el navegador
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import catalogo                                                    # noqa: E402
import comun                                                       # noqa: E402
import dossier                                                     # noqa: E402
import guia_fauna                                                  # noqa: E402
import imprimir                                                    # noqa: E402
import mapa                                                        # noqa: E402
import sin_precios                                                 # noqa: E402
import trazado                                                     # noqa: E402
from comun import RAIZ, marca_texto                                # noqa: E402
from fecha import FECHA, VIAJE                                     # noqa: E402

SALIDA = "guia-de-viaje-namibia-2026.pdf"

# Los documentos que entran, por partes y en orden de lectura.
PARTES = [
    ("La ruta", ["01"]),
    ("Al volante y en el campamento", ["06", "18", "21", "22", "23"]),
    ("Por el camino", ["07", "08", "19", "10"]),
]
DOCS = [n for _, docs in PARTES for n in docs]

# Lo que dice el índice de cada uno. El `RESUMEN` del dossier no vale tal cual: el del `01`
# promete «qué cuesta cada noche».
RESUMEN = {
    "01": "La ruta día por día: qué se conduce, a qué hora sale y se pone el sol, qué "
          "temperatura hace donde se duerme, las gasolineras y los horarios que mandan.",
    "06": "El vuelco, los límites, las presiones, la arena, la noche, los animales, las "
          "puertas de Sesriem, los teléfonos y los pinchazos.",
    "18": "Vivir del coche: la rutina de la tarde, la tienda, el braai, la nevera y los "
          "vecinos del campamento.",
    "21": "Okaukuejo, Halali, Namutoni y Onguma por dentro: la parcela, la charca, los "
          "servicios y la gasolina.",
    "22": "Si pica un escorpión: quién es quién, qué va a pasar, qué hacer y adónde ir.",
    "23": "Lo que no hay que hacer al volante, con la policía, en Etosha, en el campamento, "
          "en la costa y en Windhoek.",
    "07": "Gasolineras y tramos sin surtidor, la línea roja veterinaria, cobertura, dinero, "
          "controles de carretera, emergencias y hospitales.",
    "08": "La ley del alcohol, el súper parada a parada, las gasolineras, dónde comer, los "
          "regalos y la aduana.",
    "19": "Los pueblos, las lenguas, la historia que se ve por la ventanilla y la etiqueta "
          "del trato.",
    "10": "Lo que la ruta pisa y el itinerario no nombra, día a día y con su desvío.",
}

# Secciones que no entran, por un trozo de su encabezado. Se llevan el encabezado y todo
# lo que cuelga de él hasta el siguiente del mismo nivel —o, si el encabezado va dentro de
# una cita («> ### …»), hasta el siguiente de la cita o hasta que la cita acaba—.
FUERA_SIEMPRE = [r"🕳️", r"^Fuentes\b", r"^Cómo se regenera"]
SECCIONES_FUERA = {
    # la deliberación y el estado de las reservas del principio, el coste y lo pendiente
    "01": [r"Esta es LA ruta del viaje", r"Las cuatro noches de Etosha, RESERVADAS",
           r"El 1 de noviembre sigue siendo", r"¿Etosha al principio o al final",
           r"Dónde se duerme: ", r"El coche: ", r"Coste real", r"Lo que falta para cerrar"],
    "06": [r"Hasta dónde llega esta evidencia"],
    "07": [r"El precio, y por qué", r"Cuánto efectivo"],
    "10": [r"Cómo se lee este documento", r"Las que se quedan fuera"],
    "21": [r"^El precio$"],
}
# Líneas sueltas que sobran: el subtítulo del `01` es de la comparación con el blog.
LINEAS_FUERA = {"01": [r"^### Como la del blog de referencia"]}


# ---------------------------------------------------------------------------
# El markdown, recortado
# ---------------------------------------------------------------------------

def _cabecera(ln):
    """(profundidad de cita, nivel, texto) si la línea es un encabezado; si no, None."""
    m = re.match(r"^((?:>\s?)*)(#{1,6})\s+(.*)$", ln)
    return (m.group(1).count(">"), len(m.group(2)), m.group(3).strip()) if m else None


def _cita(ln):
    return re.match(r"^((?:>\s?)*)", ln).group(1).count(">")


def quita_secciones(texto, patrones):
    """Quita las secciones cuyo encabezado case con alguno de `patrones`."""
    out, saltando = [], None
    for ln in texto.split("\n"):
        c = _cabecera(ln)
        if saltando:
            prof, nivel = saltando
            if prof:
                acaba = (not ln.strip() or _cita(ln) < prof
                         or (c and c[0] == prof and c[1] <= nivel))
            else:
                acaba = bool(c and c[0] == 0 and c[1] <= nivel)
            if not acaba:
                continue
            saltando = None
        if c and any(re.search(p, re.sub(r"[*_`]", "", c[2])) for p in patrones):
            saltando = (c[0], c[1])
            continue
        out.append(ln)
    return "\n".join(out)


def sin_cabecera(texto):
    """Fuera la cita de cabecera de cada documento: la remisión al índice, el cambio N$/€,
    la leyenda de las marcas y las fechas de investigación. El índice ya lleva su resumen."""
    lineas = texto.split("\n")
    i = 1
    while i < len(lineas) and not lineas[i].strip():
        i += 1
    j = i
    while j < len(lineas) and lineas[j].startswith(">"):
        j += 1
    return "\n".join(lineas[:1] + lineas[j:]) if j > i else texto


def markdown(n):
    fich = next(f for f in os.listdir(RAIZ) if f.startswith(n + "-") and f.endswith(".md"))
    texto = open(os.path.join(RAIZ, fich), encoding="utf-8").read()
    texto = sin_cabecera(texto)
    texto = quita_secciones(texto, FUERA_SIEMPRE + SECCIONES_FUERA.get(n, []))
    for patron in LINEAS_FUERA.get(n, []):
        texto = "\n".join(ln for ln in texto.split("\n") if not re.search(patron, ln))
    return texto


# ---------------------------------------------------------------------------
# El HTML, sin precios
# ---------------------------------------------------------------------------

def marca_fuera(h):
    """Las remisiones a lo que la guía no lleva, cambiadas por el testigo de `sin_precios`:
    un documento del dossier que no entra, el material de `aparte/` o el README. El filtro
    quita la frase o el paréntesis que las lleva, igual que un precio."""
    t = sin_precios.TESTIGO
    fuera = r"(?!(?:%s)\b)\d\d" % "|".join(DOCS)
    h = re.sub(r"<a href=[\"']#doc-%s[\"']>.*?</a>" % fuera, t, h, flags=re.S)
    h = re.sub(r"<code>%s</code>" % fuera, t, h)
    h = re.sub(r"<a href=[\"'](?:aparte/[^\"']*|#presentacion)[\"']>.*?</a>", t, h, flags=re.S)
    return h


def filtra(h):
    return sin_precios.limpia(marca_fuera(h))


def ancla(clave):
    return dossier.ancla(clave)


def documento(n):
    html = dossier.a_html(markdown(n), doc=n, antes_de_marcar=filtra)
    # las sustituciones del dossier (Asco, la referencia descartada, como «un contrato del sector»)
    for patron, nuevo in dossier.REEMPLAZOS:
        html = re.sub(patron, nuevo, html)
    html = re.sub(r"<h1>(.*?)</h1>",
                  lambda m: f'<h1 class="titulo">{m.group(1)}{ancla(n)}</h1>', html, count=1)
    return f'<section class="doc" id="doc-{n}">{html}</section>'


def titulo(n):
    fich = next(f for f in os.listdir(RAIZ) if f.startswith(n + "-") and f.endswith(".md"))
    return dossier.titulo_de(open(os.path.join(RAIZ, fich), encoding="utf-8").read())


# ---------------------------------------------------------------------------
# Las piezas
# ---------------------------------------------------------------------------

def km_total():
    return comun.mil(sum(e.get("km") or 0 for e in mapa.carga("ruta.json")))


def portada():
    cr = comun.creditos()["lugares/portada"]
    noches = trazado.noches()
    return f"""
<section class="portada" id="portada">
  <img src="{comun.img_lugar('portada')}" alt="{cr['pie']}">
  <div class="velo"></div>
  <div class="capa">
  <div class="marca"><span>Guía de viaje</span><span>Actualizada el {FECHA}</span></div>
  <div class="txt">
    <h1>Namibia<em>2026</em></h1>
    <div class="regla"></div>
    <p class="lema">Para llevar en la mano: la ruta día a día, el coche, el campamento, el
    camino y la fauna. Sin precios ni reservas.</p>
    <p class="viajan"><b>Chema Morandeira</b> y <b>Miguel Rivera</b></p>
    <div class="datos">
      Un 4×4 con tienda de techo · <b>{VIAJE[:-8]}</b><br>
      Desierto → costa → Damaraland → <b>Etosha</b><br>
      ~{km_total()} km · {comun.en_letras(len(trazado.ETAPAS))} etapas · {len(noches)} noches
    </div>
    <div class="pie"><span>{len(DOCS)} documentos del dossier · {guia_fauna.total()} fichas de fauna</span>
    <span>Fotografía de portada: {cr['autor']} · {cr['licencia']}</span></div>
  </div>
  </div>
</section>"""


def indice(paginas):
    filas = []
    for nombre, docs in PARTES:
        filas.append(f'<div class="grupo">{nombre}</div><ol>')
        for n in docs:
            t = re.sub(r"^\d\d\s*·\s*", "", marca_texto(titulo(n)))
            filas.append(
                f'<li><span class="n">{n}</span>'
                f'<span class="t">{t}<small>{RESUMEN[n]}</small></span>'
                f'<span class="puntos"></span><span class="p">{paginas.get("doc" + n, "")}</span></li>')
        filas.append("</ol>")
    cuentas = " · ".join(f"{len(l)} {g.lower()}" for _, g, l in catalogo.GRUPOS_FAUNA)

    def fila(clave, nombre, resumen=""):
        pie = f"<small>{resumen}</small>" if resumen else ""
        return (f'<li><span class="n"></span><span class="t">{nombre}{pie}</span>'
                f'<span class="puntos"></span><span class="p">{paginas.get(clave, "")}</span></li>')
    return f"""
<section class="indice" id="indice">
  <h1>Qué hay aquí dentro</h1>
  <div class="grupo">Antes de empezar</div><ol>
  {fila("mapas", "La ruta en el mapa, las quince etapas y Etosha charca a charca")}</ol>
  {"".join(filas)}
  <div class="grupo">La fauna</div><ol>
  {fila("fauna", f"Guía de campo — {guia_fauna.total()} especies con foto", cuentas)}</ol>
  <p class="nota">Es el dossier del viaje recortado a lo que se consulta sobre el terreno:
  <b>sin precios, sin tarifas y sin el estado de las reservas</b>, que siguen en el dossier
  completo. Los números de documento son los del dossier, para que las remisiones
  —«ver <code>06</code>»— sigan valiendo. <b>Las cuatro marcas</b>:
  <span class="marca m-si"></span> fuente primaria ·
  <span class="marca m-med"></span> secundaria concordante ·
  <span class="marca m-no"></span> práctica común, sin fuente ·
  <span class="marca m-mal"></span> sin verificar. Las fotografías son de Wikimedia
  Commons, con autor y licencia bajo cada una; los mapas, de © los colaboradores de
  OpenStreetMap (ODbL) y Natural Earth.</p>
</section>"""


def mapas():
    """Las tres páginas de mapas del dossier —la ruta, las etapas y Etosha—, filtradas: la
    leyenda de la ruta remite al `13`, que aquí no está."""
    return filtra(dossier.paginas_de_mapas())


def fauna():
    """La guía de campo entera: cómo se usa y las fichas, sin la portada ni los créditos
    finales —el crédito de cada foto va debajo de ella—."""
    intro = filtra(guia_fauna.portadilla(filtro=filtra))
    intro = intro.replace('<h1 class="titulo">Cómo se usa esta guía',
                          f'<h1 class="titulo">Fauna · cómo se usa esta guía{ancla("FA")}', 1)
    fichas = filtra(guia_fauna.secciones())
    return (f'<div id="fauna">{intro}</div>'
            f'<section class="doc sin-columnas fauna">{fichas}</section>')


MARCAS_PAGINA = dict({"doc" + n: f"xqpagina{n}" for n in DOCS},
                     fauna="xqpaginaFA", mapas="La ruta, en el mapa")


def contenido():
    """Lo que sale del dossier y de la guía de fauna: todo menos la portada y el índice,
    que son de aquí y dicen «sin precios» a propósito."""
    return mapas() + "".join(documento(n) for n in DOCS) + fauna()


def html_completo(paginas=None, cuerpo=None):
    css = "".join(open(os.path.join(HERE, "estilo", f), encoding="utf-8").read()
                  for f in ("comun.css", "dossier.css", "fauna.css"))
    tipos = comun.tipografias(os.path.join(HERE, "tipos"))
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Namibia 2026 — guía de viaje</title>
<style>{tipos}</style><style>{css}</style></head><body>
{portada()}
{indice(paginas or {})}
{cuerpo or contenido()}
{dossier.script_mermaid()}
</body></html>"""


def restos(h):
    """Lo que aún huele a precio o a reserva, para avisar. Las fotos van fuera: son base64."""
    return sin_precios.restos(re.sub(r'<img [^>]*>', "", h))


def main():
    salida_html = os.path.join(HERE, "guia-de-viaje.html")
    salida_pdf = os.path.join(RAIZ, SALIDA)
    cuerpo = contenido()
    h = html_completo(cuerpo=cuerpo)
    open(salida_html, "w", encoding="utf-8").write(h)
    quedan = restos(cuerpo)
    print(f"HTML: {os.path.getsize(salida_html) // 1024} KB · {len(quedan)} restos de precio o reserva")
    for r in quedan:
        print("   ·", r)
    if "--html" in sys.argv:
        return 0
    if quedan:
        raise SystemExit("guia_viaje: queda algún precio o reserva en el HTML — mira arriba")
    pie = dict(izquierda="Namibia 2026 · guía de viaje", derecha=FECHA, espera=6)
    print("Pasada 1 · maquetando para saber las páginas…")
    imprimir.a_pdf(salida_html, salida_pdf, **pie)
    paginas = imprimir.indice_de_paginas(salida_pdf, MARCAS_PAGINA)
    faltan = [k for k in MARCAS_PAGINA if k not in paginas]
    if faltan:
        raise SystemExit(f"guia_viaje: la primera pasada no encuentra la marca de "
                         f"{', '.join(faltan)} — el índice se quedaría sin su página")
    print("Pasada 2 · escribiendo los números en el índice…")
    open(salida_html, "w", encoding="utf-8").write(html_completo(paginas, cuerpo))
    imprimir.a_pdf(salida_html, salida_pdf, **pie)
    print(f"\n{SALIDA} · {imprimir.paginas(salida_pdf)} páginas · "
          f"{os.path.getsize(salida_pdf) // 1024 // 1024} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
