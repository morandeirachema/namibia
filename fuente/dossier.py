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

FECHA = "24 de agosto de 2026"

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
    "01": ["spreetshoogte", "namib-paisaje", "grava", "deadvlei", "walvisbay", "saltroad",
           "skeleton", "grootberg", "twyfelfontein", "okaukuejo"],
    "02": ["hilux", "sandwich"],
    "03": ["sesriem", "terracebay"],
    "04": ["windhoek"],
    "05": [],
    "06": ["grava", "saltroad", "bigdaddy"],
    "07": ["solitaire"],
    "08": ["swakopmund", "joes"],
    "09": ["etosha-elefantes", "etosha-rino", "halali", "namutoni"],
    "10": ["circulos", "cielo", "welwitschia"],
    "11": ["capecross"],
    "12": [],
    "13": ["spreetshoogte", "grootberg", "damaraland"],
    "14": ["termitero", "etosha-pan"],
    "15": [],
    "17": ["hiddenvlei"],
    "18": ["hoada"],
    "21": ["okaukuejo-torre", "okaukuejo-charca-dia", "okaukuejo-charca-noche", "halali",
           "halali-moringa", "halali-piscina", "namutoni", "namutoni-atardecer",
           "namutoni-charca"],
}

# Fotos a pagina completa, antes del documento que abren.
PLENAS = {
    "01": ("duna45", "Duna 45 al amanecer. El D4 empieza una hora antes que para todos "
                     "los demás: la puerta interior de Sesriem abre solo para quien duerme dentro."),
    "09": ("etosha-jirafas", "Etosha al atardecer. Cuatro noches dentro del parque, "
                             "tres campamentos y una charca iluminada en cada uno."),
}

# ---------------------------------------------------------------------------
# Que NO entra en el PDF
# ---------------------------------------------------------------------------
# El PDF es el documento del viaje: solo lleva datos de la ruta que se va a hacer.
# La deliberacion —por que esta ruta y no otra, por que el sur se queda fuera, que
# variantes se estudiaron— es material de trabajo: sigue entera en los .md del repo
# y en el historial de git, pero no en el volumen que se imprime y se lleva en el
# coche. Ahi solo estorba.

FUERA_DEL_PDF = {"16"}    # documentos completos que no entran: las variantes archivadas

# Secciones que se caen, por un trozo de su titulo. Se lleva por delante la seccion
# entera: el encabezado y todo lo que cuelga de el hasta el siguiente del mismo nivel.
SECCIONES_FUERA = {}
# Vacío desde el 12/08: los bloques de deliberación que este mecanismo recortaba del PDF
# (la duda de Etosha al principio o al final, la comparación con el blog, los descartes
# de ruta, los drones) se quitaron directamente de los .md — no hacía falta filtrarlos
# en cada build si ya no viven en la fuente. El mecanismo se queda por si vuelve a hacer falta.

# Frases sueltas que remiten al material de trabajo (las variantes descartadas) y que
# no justifican tirar el bloque entero donde viven.
# En el PDF el coche es Savanna y punto: fuera las comparativas de precio con
# otras companias. OJO: en `06` los nombres se quedan a proposito — esas clausulas
# salen del contrato PUBLICADO de otra empresa porque el de Savanna no es publico,
# y borrar la atribucion las haria parecer verificadas contra tu propio contrato.
# Son expresiones regulares porque el texto llega ya en HTML, con sus <em> y <strong>.
# Comprobado el 13/08/2026: 5 de las 9 reglas de entonces ya no casaban con nada en los
# .md actuales (citaban "34 pines de Google Maps", ya fuera del dossier, y una forma de
# nombrar a Asco que se reescribió en su sitio) — se quitaron. Las 4 que quedan SÍ siguen
# disparando hoy: antes de tocar esta lista, comprueba con grep contra el .md real, no
# de memoria — así fue como se detectaron las 5 muertas.
REEMPLAZOS = [
    (r"niveles bajos de <strong>Asco</strong> \(la referencia descartada\)",
     "los niveles bajos de un contrato de referencia del sector"),
    (r"contratos Asco/Savanna, ya descargados", "contratos de alquiler ya descargados"),
    (r"Asco/Savanna ya descargados", "contratos de alquiler ya descargados"),
    (r"no se investiga si Asco autoriza el cruce",
     "no se investiga si el contrato autoriza el cruce"),
]

# Avisos sueltos que son deliberacion, no dato. Se busca el trozo dentro del bloque.
# (Vacío desde el 12/08: las dos frases que filtraba ya no existen en ningún .md — se
# quitaron de raíz junto con las secciones de SECCIONES_FUERA.)
AVISOS_FUERA = []

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
    "09": "Cómo funciona el safari en seco, y la guía de campo con las posibilidades "
          "medidas de ver cada especie.",
    "10": "Los Lone Stone Men, la cascada del Uniab, los círculos de hadas.",
    "11": "Lo que cuesta entrar en cada sitio de la ruta, los permisos y la norma de drones.",
    "12": "Lo que superó la verificación a tres votos, y lo que quedó refutado.",
    "13": "Distancias, firme y viabilidad — con el contraste de OSRM.",
    "14": "Cinco temporadas de lluvia en Etosha, milímetro a milímetro.",
    "15": "El cuaderno de bitácora: temperaturas de estación, viento, luz, vuelos, tasas y lodges.",
    "17": "La lista de la víspera, ítem a ítem y con casilla: ropa, neceser, botiquín y kits.",
    "18": "Vivir del coche: la rutina de la tarde, la tienda, el braai, la nevera y los "
          "vecinos del campamento.",
    "19": "Los pueblos, las lenguas, la historia que explica lo que se ve por la ventanilla "
          "y la etiqueta del trato — atado a los días de la ruta.",
    "20": "El cuaderno de llamadas: cada reserva con su canal, su contacto y su fuente — "
          "el orden en que se cierran y lo que se deja para recepción.",
    "21": "Las cuatro noches de Etosha por dentro —Okaukuejo, Halali y Onguma Tamboti ×2, "
          "más Namutoni, que se visita pero ya no se duerme—: la parcela, la charca y los "
          "servicios, con los avisos de los viajeros recientes.",
    "22": "Si te pica un escorpión: quién es quién, qué va a pasar, qué hacer y qué no, a "
          "quién llamar y adónde ir — etapa a etapa.",
    "23": "El guepardo, prioridad del viaje: dónde se ve de verdad y de qué noche sale el "
          "día. Y las joyas de FUERA de la ruta, con los kilómetros medidos.",
    "24": "La decisión del D12, que se toma dentro de Etosha: saltarse la segunda noche "
          "de Onguma y bajar al Cheetah Conservation Fund si el guepardo no ha salido. "
          "Medida, con su mapa, y con lo que hay que preguntar antes de salir de casa.",
}


def miles(n, sufijo=" km"):
    """2728 -> «2.728 km»."""
    return comun.mil(n) + sufijo


# El numero de un documento manda su sitio en el volumen, salvo aqui: la lista de
# equipaje (`17`) se escribio la ultima pero se lee pegada al `05`, que es de lo que
# sale; el manual de campamento (`18`) va pegado al `06`, porque el dia de ruta se lee
# del tiron: conducir y acampar; los campamentos de Etosha (`21`) van pegados al `18`,
# que es su manual de uso; la picadura de escorpion (`22`) detras del `21`, porque es del
# campamento; la cultura (`19`) pegada al `08`, que ya lleva la mesa y los mercados; y los
# desvios de fuera de la ruta (`23`) detras del `10`, que cataloga las joyas de dentro:
# son las dos caras de la misma pregunta y se leen seguidas.
# Renumerar el repo entero seria peor: hay referencias cruzadas por todos lados.
ORDEN = {"20": "04a", "17": "05a", "18": "06a", "21": "06b", "22": "06c", "19": "08a",
         "23": "10a", "24": "10b"}


def documentos():
    """Los documentos que entran en el PDF, en orden de lectura."""
    return sorted((f for f in os.listdir(RAIZ)
                   if re.match(r"\d\d-.*\.md$", f) and num(f) not in FUERA_DEL_PDF),
                  key=lambda f: ORDEN.get(num(f), num(f)))


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
        # Los gantt y los quesos no caben en una columna de 89 mm: esos si cruzan.
        # Cualquier otro diagrama puede pedirlo con una linea `%% ancho`, que
        # Mermaid lee como comentario y GitHub sigue pintando igual.
        tipo = c.strip().split("\n", 1)[0].strip().split()[0].lower()
        ancho = (" ancho" if tipo in ("gantt", "pie", "timeline")
                 or re.search(r'^\s*%%\s*ancho\s*$', c, re.M) else "")
        return f'<pre class="mermaid{ancho}">' + c + "</pre>"

    h = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', desescapa, h, flags=re.S)

    # `- [ ] item` -> casilla dibujada, que en papel se marca a boli.
    h = re.sub(r'<li>\[ \]\s*', '<li class="tarea"><span class="casilla"></span>', h)

    # Cosas que GitHub pinta bonito y en papel no existen:
    #  · los avisos `> [!NOTE]` -> el rotulo tipografico del dossier
    #  · los `<details>` plegables -> abiertos, con su titulo, que en el PDF no
    #    hay donde pulsar y Chrome imprime solo el `<summary>` si se dejan
    #  · las insignias de shields.io -> fuera: el PDF se imprime sin red
    avisos = {"NOTE": ("info", "nota"), "TIP": ("ok", "en corto"),
              "IMPORTANT": ("duda", "importante"), "WARNING": ("no", "ojo"),
              "CAUTION": ("no", "cuidado")}
    h = re.sub(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*",
               lambda m: '<span class="et et-{0}">{1}</span> '.format(*avisos[m.group(1)]), h)
    h = re.sub(r"<details[^>]*>", '<div class="desplegable">', h)
    h = h.replace("</details>", "</div>")
    h = re.sub(r"<summary>(.*?)</summary>", r'<h3 class="desplegable-t">\1</h3>', h, flags=re.S)
    h = re.sub(r'<img [^>]*src="https?://[^"]*"[^>]*>\s*', "", h)

    # enlaces entre documentos -> anclas internas del propio PDF
    h = re.sub(r'href="(\d\d)-[a-z-]+\.md"', r'href="#doc-\1"', h)
    h = h.replace('href="README.md"', 'href="#presentacion"')
    h = re.sub(r'href="guia-fauna-etosha\.pdf"', 'href="#fauna"', h)
    h = re.sub(r'href="dossier-namibia-2026\.pdf"', 'href="#portada"', h)

    h = marca_texto(h)

    # las referencias sueltas a otro documento («ver `13`») se hacen enlace — con guardia:
    # el `NN` de un enlace [`NN`](NN-….md) ya viene dentro de su <a>, y sin la guardia
    # se anidaba un segundo ancla dentro del primero (HTML invalido).
    if doc:
        h = re.sub(r'(?<!#doc-\d\d">)<code>(\d\d)</code>',
                   lambda m: f'<a href="#doc-{m.group(1)}"><code>{m.group(1)}</code></a>', h)
    # los documentos FUERA_DEL_PDF no tienen ancla dentro del volumen: el enlace se
    # desenvuelve a texto plano en vez de dejar un href muerto (#doc-16 no existe).
    # Hasta punto fijo, por si quedara algun anidado de HTML viejo.
    for fuera in FUERA_DEL_PDF:
        patron = rf'<a href="#doc-{fuera}">((?:(?!</a>).)*?)</a>'
        previo = None
        while previo != h:
            previo, h = h, re.sub(patron, r"\1", h, flags=re.S)
    return h


def _texto(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def poda(cuerpo, doc):
    """Quita del HTML las secciones y avisos que no son datos de la ruta.

    Trabaja sobre el HTML ya renderizado y no sobre el Markdown: los documentos del
    repo se quedan enteros —en GitHub la deliberacion si vale—, y es solo el volumen
    impreso el que sale limpio.
    """
    titulos = SECCIONES_FUERA.get(doc, [])

    # 1 · secciones enteras: del encabezado hasta el siguiente del mismo nivel o superior
    if titulos:
        trozos = re.split(r"(<h[1-4]>)", cuerpo)
        salida, i, saltando, nivel_corte = [trozos[0]], 1, False, 9
        while i < len(trozos) - 1:
            etiqueta, contenido = trozos[i], trozos[i + 1]
            nivel = int(etiqueta[2])
            titulo = _texto(contenido.split("</h")[0])
            if saltando and nivel <= nivel_corte:
                saltando = False
            if not saltando and any(t.lower() in titulo.lower() for t in titulos):
                saltando, nivel_corte = True, nivel
            if not saltando:
                salida.append(etiqueta + contenido)
            i += 2
        cuerpo = "".join(salida)

    # 2 · avisos sueltos: el <blockquote> entero si contiene la frase
    for aguja in AVISOS_FUERA:
        cuerpo = re.sub(r"<blockquote>(?:(?!</blockquote>).)*?</blockquote>",
                        lambda m: "" if aguja.lower() in _texto(m.group(0)).lower() else m.group(0),
                        cuerpo, flags=re.S)

    # 3 · la cabecera comun: se repite igual en los quince documentos. En GitHub tiene
    #     sentido (cada fichero se lee suelto); en el PDF son quince copias del mismo
    #     parrafo, y la leyenda de las marcas ya esta en el indice.
    cuerpo = re.sub(r"<p><strong>Namibia · [^<]*</strong>[^<]*<a [^>]*>[^<]*</a></p>\s*", "", cuerpo)
    cuerpo = re.sub(r"<p><strong>~N\$20 = €1</strong>.*?</p>\s*", "", cuerpo, flags=re.S)

    # 4 · frases sueltas que remiten al material de trabajo o a otra compania
    for patron, nuevo in REEMPLAZOS:
        cuerpo = re.sub(patron, nuevo, cuerpo)

    # 5 · los separadores <hr> que se quedan pegados de dos en dos
    return re.sub(r"(?:<hr\s*/?>\s*){2,}", "<hr>", cuerpo)


def reparte_fotos(cuerpo, slugs):
    """Mete las fotos delante de los <h2> y <h3>, repartidas por el documento.

    Cada foto va en un hueco distinto: si dos cayeran en el mismo se solaparian las
    etiquetas y saldria HTML invalido, y con HTML invalido el navegador ensancha la
    pagina y encoge el documento entero al imprimirlo.

    Se reparte tambien en los <h3> (los dias del `01`, p. ej.): solo con <h2>, al
    documento del itinerario le quedaban DOS huecos tras la poda y cuatro de sus seis
    fotos declaradas se caian en silencio — y salian acreditadas sin ensenarse. Solo
    cuentan las etiquetas desnudas: el <h3 class="desplegable-t"> de los plegables no.
    """
    if not slugs:
        return cuerpo
    partes = re.split(r"(?=<h[23]>)", cuerpo)
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
        salida.append(p)
    return "".join(salida)


# ---------------------------------------------------------------------------
# Piezas del volumen
# ---------------------------------------------------------------------------

def portada(total_paginas=None):
    cr = comun.creditos()["lugares/portada"]
    pie_izq = f"{len(documentos())} documentos · 2 mapas · guía de fauna aparte"
    pie_der = f"Fotografía de portada: {cr['autor']} · {cr['licencia']}"
    return f"""
<section class="portada" id="portada">
  <img src="{comun.img_lugar('portada')}" alt="{cr['pie']}">
  <div class="velo"></div>
  <div class="capa">
  <div class="marca"><span>Dossier de viaje</span><span>Actualizado el {FECHA}</span></div>
  <div class="txt">
    <h1>Namibia<em>2026</em></h1>
    <div class="regla"></div>
    <p class="lema">El gran roadtrip del norte: las dunas más altas del mundo al amanecer,
    la Costa de los Esqueletos y cuatro noches de safari en Etosha.</p>
    <p class="viajan"><b>Chema Morandeira</b> y <b>Miguel Rivera</b></p>
    <div class="datos">
      Un 4×4 con tienda de techo · <b>30 de octubre – 15 de noviembre</b><br>
      Desierto → costa → Damaraland → <b>cuatro noches de safari en Etosha</b><br>
      ~2.764 km · <b>~€3.990 por persona</b>, todo incluido
    </div>
    <div class="pie"><span>{pie_izq}</span><span>{pie_der}</span></div>
  </div>
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

    import catalogo
    n_especies = sum(len(l) for _, _, l in catalogo.GRUPOS_FAUNA)
    extra = []
    for clave, nombre in [("mapas", "Los mapas: la ruta y las charcas de Etosha"),
                          ("presentacion", "El viaje de un vistazo"),
                          ("fauna", f"La guía de campo va aparte — {n_especies} especies con foto"),
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


# Los mapas que van DENTRO de un documento, y no en su pagina suelta del principio.
# En el markdown van como <img> —para que GitHub los pinte y el `.md` se lea solo—, y
# aqui se cambian por el SVG en linea: en el PDF sale vectorial, nitido a cualquier
# tamano y sin depender de que el PNG este generado. Clave: nombre en img/mapas/.
MAPAS_EN_DOC = {"24": ("ruta-alternativa", lambda: mapa.mapa_ruta_alt())}


def mete_mapas(html, doc):
    """Cambia el <img> del mapa por el SVG en linea, en los documentos que lo llevan."""
    par = MAPAS_EN_DOC.get(doc)
    if not par:
        return html
    nombre, dibuja = par
    patron = (r'<p>\s*<a href="img/mapas/' + re.escape(nombre) +
              r'\.svg">\s*<img[^>]*>\s*</a>\s*</p>')
    if not re.search(patron, html):
        return html
    return re.sub(patron, lambda _: f'<div class="mapa mapa-doc">{dibuja()}</div>',
                  html, count=1)


def paginas_de_mapas():
    datos = {e["id"]: e for e in mapa.carga("ruta.json")}
    filas = []
    for e in trazado.ETAPAS:
        d = datos.get(e["id"], {})
        km = d.get("km")
        duerme = trazado.PUNTOS[e["duerme"]][2] if e["duerme"] else "—"
        color = trazado.COLOR_BLOQUE[e["bloque"]]
        filas.append(
            f'<li><span class="dia" style="border-color:{color}">{e["id"]}</span>'
            f'<span class="fec">{e["fecha"]}</span>'
            f'<span class="etapa">{e["titulo"]}</span>'
            f'<span class="km">{"—" if not km else miles(km)}</span>'
            f'<span class="dor">{duerme}</span></li>')
    total = sum(d.get("km") or 0 for d in datos.values())

    return f"""
<section class="mapa-plena" id="mapas">
  <h1 class="titulo">La ruta, en el mapa</h1>
  <div class="mapa mapa-ruta">{mapa.mapa_ruta()}
    <figcaption>Trazado real de carretera, calculado con <b>OSRM</b> sobre OpenStreetMap a
    partir de las coordenadas de cada parada. Los contornos son de <b>Natural Earth</b>
    (dominio público). La suma de las quince etapas da <b>{miles(total)}</b>, que cuadra con
    lo medido aparte en <a href="#doc-13"><code>13</code></a>.</figcaption>
  </div>
</section>

<section class="mapa-plena">
  <h1 class="titulo">Las quince etapas</h1>
  <ol class="etapas">
    <li class="cabecera"><span class="dia">Día</span><span class="fec">Fecha</span>
      <span class="etapa">Etapa</span><span class="km">Carretera</span>
      <span class="dor">Dónde se duerme</span></li>
    {"".join(filas)}
    <li class="total"><span class="dia"></span><span class="fec"></span>
      <span class="etapa">Total conducido</span><span class="km">{miles(total)}</span>
      <span class="dor">14 noches — 13 en tienda</span></li>
  </ol>
  <p class="nota-tabla">Los kilómetros de esta tabla son <b>de carretera, puerta a puerta</b>,
  medidos con OSRM sobre el trazado de OpenStreetMap el 8 de agosto de 2026. No incluyen los
  desvíos a charcas dentro de Etosha ni las vueltas del día de descanso.</p>
</section>

<section class="mapa-plena girado">
  <div class="marco">
    <div class="mapa mapa-etosha">{mapa.mapa_etosha()}
      <figcaption><b>Etosha, charca a charca.</b> En seca la fauna no está repartida por el
      parque: está en el agua. Las charcas, las pistas y el límite del parque salen de
      OpenStreetMap; el relleno blanco es la depresión, que en noviembre está seca —y por eso
      el safari funciona. Los círculos huecos son sondeos con bomba: los que aguantan cuando
      las charcas naturales se secan.</figcaption>
    </div>
  </div>
</section>"""


def documento(fich, con_separador=True):
    """Un documento del dossier, con su separador de bloque y sus fotos."""
    n = num(fich)
    texto = open(os.path.join(RAIZ, fich)).read()
    partes = []
    if con_separador:
        for b in BLOQUES:
            if b["desde"] == n:
                partes.append(separador(b))
    if n in PLENAS:
        slug, pie = PLENAS[n]
        partes.append(comun.foto_plena(slug, pie))
    html = poda(a_html(texto, doc=n), n)
    html = re.sub(r"<h1>(.*?)</h1>",
                  lambda m: f'<h1 class="titulo">{m.group(1)}{ancla(n)}</h1>', html, count=1)
    html = mete_mapas(html, n)
    html = reparte_fotos(html, FOTOS.get(n, []))
    partes.append(f'<section class="doc" id="doc-{n}">{html}</section>')
    return "".join(partes)


def cuerpo_documentos():
    partes = []
    for f in documentos():
        partes.append(documento(f))
    return "".join(partes)


def presentacion():
    texto = open(os.path.join(RAIZ, "README.md")).read()
    # el titulo y el bloque de descarga del PDF no pintan nada dentro del propio PDF
    texto = re.sub(r'^<div align="center">\n\n# 🇳🇦 NAMIBIA 2026\n', '<div align="center">\n', texto)
    texto = re.sub(r"### 📕 \[\*\*Descargar.*?\n\n.*?\n\n", "", texto, flags=re.S)
    h = poda(a_html(texto), "RM")
    h = re.sub(r"<h2>", '<h2 class="pres">', h)
    # Las fotos y el mapa del README no entran: el dossier trae los suyos, colocados
    # donde tocan, y aqui saldrian repetidos y del tamano de un sello.
    h = re.sub(r"<img [^>]*>", "", h)
    h = re.sub(r"<a [^>]*>\s*</a>", "", h)
    # En el indice del README los emojis son decoracion, no rotulos: convertidos a
    # palabra se pegan al numero de la lista («8.GASOLINA 07-logistica»). Aqui —y
    # solo aqui, que en los documentos si etiquetan— se caen.
    h = re.sub(r'(<li>)\s*<span class="(?:rot|et et-\w+)">[^<]*</span>\s*(?=<a )', r"\1", h)
    return (f'<section class="doc" id="presentacion">'
            f'<h1 class="titulo">El viaje de un vistazo{ancla("RM")}</h1>{h}</section>')


def fauna():
    import guia_fauna
    return guia_fauna.remite_desde_dossier(ancla("FA"))


def _lugares_usados():
    """Solo se acreditan las fotos de lugar que el dossier ENSEÑA — la nota de la
    seccion promete creditos «donde se usan», y acreditar siete fotos que nunca
    salen la desmentia."""
    usados = {"portada"}
    usados.update(b["foto"] for b in BLOQUES)
    usados.update(s for slugs in FOTOS.values() for s in slugs)
    usados.update(slug for slug, _pie in PLENAS.values())
    return usados


def creditos_seccion():
    cr = comun.creditos()
    usados = _lugares_usados()
    lug = "".join(f'<li><b>{v["pie"]}</b> — {v["autor"]}, <i>{v["licencia"]}</i></li>'
                  for k, v in sorted(cr.items())
                  if k.startswith("lugares/") and k.split("/", 1)[1] in usados)
    n_fauna = sum(1 for k in cr if k.startswith("fauna/"))
    return f"""
<section class="doc sin-columnas creditos" id="creditos">
  <h1 class="titulo">Créditos de las fotografías{ancla('CR')}</h1>
  <p class="nota">Las fotografías de este dossier proceden de <b>Wikimedia Commons</b> y están
  bajo licencia libre (CC BY, CC BY-SA, CC0 o dominio público), que exige citar autor y
  licencia — es lo que hace esta lista. El fichero exacto de cada una está en
  <code>fuente/catalogo.py</code>, y <code>fuente/descargar.py</code> rechaza cualquier imagen
  cuya licencia no sea libre. Los créditos de las <b>{n_fauna} fotografías de fauna</b> van en su
  propio PDF, <code>guia-fauna-etosha.pdf</code>, donde se usan.</p>
  <h2>Los lugares</h2><ul class="dos">{lug}</ul>
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

def html_completo(paginas=None):
    css = "".join(open(os.path.join(HERE, "estilo", f)).read()
                  for f in ("comun.css", "dossier.css"))
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
// startOnLoad va a false y se dibuja DESPUES de que carguen las tipografias: si
// Mermaid mide las etiquetas con la fuente de respaldo, calcula cajas mas pequenas
// que el texto definitivo y los rotulos se salen por abajo.
mermaid.initialize({{startOnLoad:false, securityLevel:'loose', theme:'base',
  themeVariables:{{
    fontFamily:'Source Sans 3, Helvetica, Arial, sans-serif', fontSize:'12px',
    primaryColor:'#F7F4ED', primaryTextColor:'#16130F', primaryBorderColor:'#C6C1B4',
    lineColor:'#7D776E', tertiaryColor:'#EFEAE0'
  }},
  // wrappingWidth manda cuando parte la etiqueta de un nodo: con el valor por
  // defecto (200) las cajas salen estrechas y el texto se sale por abajo.
  // htmlLabels a false: con etiquetas HTML, Mermaid calcula la caja con una medida
  // que no coincide con la del texto final y los rotulos se salen por abajo. Con
  // texto SVG mide lo que luego pinta.
  flowchart:{{useMaxWidth:true, htmlLabels:false, curve:'basis',
              wrappingWidth:420, padding:14, nodeSpacing:32, rankSpacing:42}},
  gantt:{{useMaxWidth:true, fontSize:11, barHeight:15, barGap:4, topPadding:36,
          leftPadding:96, gridLineStartPadding:28}},
  pie:{{useMaxWidth:true, textPosition:0.62}}}});

(document.fonts ? document.fonts.ready : Promise.resolve())
  .then(function () {{ return new Promise(function (r) {{ setTimeout(r, 120); }}); }})
  .then(function () {{ return mermaid.run({{querySelector: 'pre.mermaid'}}); }})
  .then(function () {{ document.documentElement.dataset.diagramas = 'listos'; }})
  .catch(function (e) {{ document.documentElement.dataset.diagramas = 'error'; console.error(e); }});
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
