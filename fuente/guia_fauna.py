#!/usr/bin/env python3
"""La guia de campo de fauna: va suelta en PDF (para la guantera) y embebida en el dossier.

Uso:
    python3 fuente/guia_fauna.py          # HTML + PDF suelto
    python3 fuente/guia_fauna.py --html   # solo el HTML
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import avistamientos                                               # noqa: E402
import catalogo                                                    # noqa: E402
import mapa                                                        # noqa: E402
import pais                                                        # noqa: E402
import comun                                                       # noqa: E402
import imprimir                                                    # noqa: E402
from comun import RAIZ, marca_texto                                # noqa: E402
from textos_especies import ID                                     # noqa: E402
from textos_poblacion import CUANTOS, FUENTES_POBLACION            # noqa: E402
from textos_safari import CONSEJOS                                 # noqa: E402

try:
    from textos_etosha import DONDE, FUENTES_ETOSHA, INTRO_EXTRA, NOCTURNO
except ImportError:                                                # aun sin el informe
    DONDE, INTRO_EXTRA, FUENTES_ETOSHA, NOCTURNO = {}, "", [], ""


def metodo():
    """El bloque que explica de donde sale el porcentaje de cada ficha.

    Sin esto la cifra es un numero suelto que invita a creersela mas de lo que vale.
    Va con los denominadores de verdad, sacados del propio fichero de datos.
    """
    d = avistamientos.datos()
    if not d:
        return ""
    camps = d.get("campamentos") or {}
    trozos = " · ".join(f"<b>{c['nombre']}</b> {c['viajeros']}" for c in camps.values()
                        if c.get("viajeros"))
    et = d.get("zonas", {}).get("etosha", {}).get("por_clase", {})
    mam = comun.mil(et.get("359", {}).get("oct_nov", 0))
    aves = comun.mil(et.get("212", {}).get("oct_nov", 0))
    slugs = [s for _, _, l in catalogo.GRUPOS_FAUNA for s, *_ in l]
    con_partes = comun.en_letras(sum(1 for s in slugs if avistamientos.porcentajes(s)))
    sin_partes = comun.en_letras(sum(1 for s in slugs if not avistamientos.porcentajes(s)))
    return f"""
  <p><strong>La línea de arriba de cada ficha dice qué posibilidades hay.</strong> Cuando
  pone <em>«82&nbsp;% lo vio»</em> es literal: viajeros que declararon <strong>una o más
  observaciones durante su estancia en el campamento</strong> (partes de Expert Africa —
  {trozos}). <strong>La unidad es la estancia, no el día ni el viaje</strong>: una o dos
  noches. La cifra grande junta los tres campamentos de NWR y detrás va cada uno. Aquí se
  duerme en dos de ellos <em>(Okaukuejo y Halali; las dos últimas noches, en Onguma, ya fuera de la
  puerta)</em> y el tercero, Namutoni, se cruza de paso — son <strong>dos tiradas y media</strong>:
  en las cuatro noches la posibilidad real es más alta que cualquiera de estos números. Cuánto más, no lo dicen estos datos, así que no se dice.</p>
  <p>Eso solo existe para {con_partes} especies. Para las otras {sin_partes} va un
  <strong>índice de registros de GBIF</strong>: cuánto pesa la especie dentro de los
  registros de su grupo en la zona <strong>en octubre y noviembre</strong> —{mam} de
  mamífero y {aves} de ave solo en Etosha—. Mide <em>lo que se registra</em>, no <em>lo
  que se ve</em>: por eso dice <strong>frecuente</strong> o <strong>escasa</strong>, nunca
  «lo vas a ver».</p>
  <p><strong>Los dos sesgos, por delante:</strong> los partes los rellenan viajeros y hay
  confusiones —un 14&nbsp;% declara antílope sable en Okaukuejo, y en Etosha no hay
  sable—; y a GBIF nadie sube el chacal número doscientos ni casi nada nocturno, así que
  la liebre saltadora sale con cero registros siendo de lo que más enseñan los guías en el
  nocturno. Cada cifra lleva detrás su muestra: con cuatro registros no se afirma nada.</p>
"""


def _lider():
    """La region con mas fichas y su cuenta, para no escribir el numero a mano."""
    cuenta = mapa._fichas_por_region()
    gid, n = max(cuenta.items(), key=lambda x: x[1])
    return dict((g, nom) for g, nom, _a in pais.REGIONES)[gid], n


def mapa_del_pais():
    """El mapa de las trece regiones, en linea y cruzando las dos columnas.

    Va DENTRO del documento y como SVG en linea, igual que el mapa de la variante en el
    dossier: sale vectorial, no depende de que el PNG este generado y no hay que decidir
    a que ancho se imprime. Sin este mapa, la linea «En Namibia» de cada ficha es una
    lista de nombres propios que no situan nada.
    """
    return f"""
  <h2>Dónde vive cada bicho, y por dónde pasáis vosotros</h2>
  <div class="mapa-doc">{mapa.mapa_regiones(1180)}</div>
  <p class="pie-mapa"><strong>La última línea de cada ficha —«En Namibia»— dice en qué
  regiones se ha registrado la especie y con cuántos registros.</strong> Este mapa es
  dónde caen esas regiones. En naranja, las siete que pisa la ruta; en gris, las seis que
  no — y ahí es donde vive entera la <strong>parte 2</strong> de la guía. El número de
  cada región es cuántas de estas {total()} fichas tienen ahí <em>el grueso</em> de sus
  registros: <strong>{_lider()[0]}</strong> se lleva {_lider()[1]} porque el este de Etosha es donde más
  mira todo el mundo, y eso también es un sesgo del dato y no un ranking de riqueza.</p>"""


def portadilla():
    """El documento de entrada, maquetado como los del dossier: dos columnas y titular.

    Antes todo esto —el metodo, como funciona el parque— iba metido en la cajita de
    introduccion de los mamiferos, que crecio hasta comerse media pagina y dejar la
    primera fila de fichas sin sitio. Como documento propio se lee mejor, cabe la
    seccion de consejos y las fichas empiezan en pagina limpia.
    """
    return marca_texto(f"""
<section class="doc portadilla">
  <h1 class="titulo">Cómo se usa esta guía</h1>
  <p><strong>Cada ficha</strong> lleva el nombre en castellano, el científico y el inglés
  —el de los carteles del parque—, la foto <strong>sin recortar</strong> <em>(los cuernos,
  el cuello y la cola se ven enteros, que es lo que sirve para identificar)</em> y los
  rasgos que distinguen a la especie <em>en el campo</em>. Debajo, dónde y cuándo verla,
  cuántas quedan cuando hay una cifra publicada que citar, y <strong>en qué regiones de
  Namibia vive</strong>.</p>
  <p><strong>Y la guía va en dos partes, que no miden lo mismo.</strong> La
  <strong>parte 1</strong> son las {de_la_ruta()} especies que caen en los 2.798 km de este
  viaje, cada una con su posibilidad de avistamiento medida. La <strong>parte 2</strong> son
  {del_resto()} que existen en Namibia y que <strong>este itinerario no pisa</strong> —el norte
  mojado del Zambeze y el Okavango, y lo del Kalahari que sale de noche—: están para saber qué
  tiene el país y qué haría falta para verlo, no para esperarlas en una charca de Etosha.</p>
  {metodo()}
  {mapa_del_pais()}
  <h2>Cómo funciona el parque</h2>
  {INTRO_EXTRA}
  {NOCTURNO}
  {CONSEJOS}
</section>""")


INTROS = {
    "felino": "<p><strong>Namibia tiene siete felinos y aquí van seis</strong> — el séptimo, el "
              "serval, no toca esta ruta: cero registros en las cuatro zonas. Los tres grandes "
              "llevan el porcentaje de viajeros que los vio; los tres pequeños son nocturnos y la "
              "banda dice lo que hay. El <strong>gato de patas negras</strong> va con un solo "
              "registro en toda la historia del polígono: está para saber distinguirlo del gato "
              "montés en el nocturno, no porque contéis con verlo.</p>",
    "mamifero": "<p>Treinta y tres fichas, de lo que se ve en todas las charcas a lo que "
                "hay que tener suerte para cruzarse — los felinos van aparte, justo antes. "
                "<strong>El orden no es alfabético: es el de siempre</strong> — primero los "
                "grandes.</p>"
                "<p><strong>Las dos últimas entraron el 29/08 con el barrido de todo el "
                "país.</strong> La <strong>cebra de Hartmann</strong> había salido del catálogo "
                "el 09/08 por vivir en las lomas del extremo oeste de Etosha, lejos del eje; "
                "pero la ruta cambió y ahora pisa dos sitios donde sí está —la escarpa de "
                "Spreetshoogte, donde la propia finca la anuncia, y Damaraland—. Y el "
                "<strong>duiker común</strong>, que es el antílope pequeño que más se cruza de "
                "noche en el bosque del norte.</p>",
    "rapaz": "<p><strong>Cuarenta rapaces, diurnas y nocturnas, y el criterio es el del "
             "método:</strong> entra toda la que GBIF registra <strong>diez veces o más en "
             "octubre-noviembre en alguna zona de la ruta</strong>. Las que se quedan por "
             "debajo, para que no las echéis en falta: azor lagartijero oscuro (9, en el "
             "este de Etosha), gavilán ovambo (8), búho del Cabo (7), buitre del Cabo (6, su "
             "casa es Waterberg), cernícalo primilla (5), águila esteparia (4), mochuelo de "
             "El Cabo (4), cernícalo patirrojo (3), alimoche (3), buitre encapuchado (2) y el "
             "<strong>halcón del Amur</strong> (2): sus bandadas llegan a Etosha en diciembre y "
             "el grueso pasa en febrero-marzo <em>(1 registro en noviembre, 9 en diciembre, "
             "34 en marzo)</em> — justo después de vosotros.</p>"
             "<p><strong>Cómo se separan, en corto:</strong> las <strong>águilas</strong> "
             "grandes por la silueta y el pecho (marcial: capucha y pecho blanco moteado; "
             "rapaz: parda lisa; cafre: negra con V blanca, solo en roca; bateleur: sin cola); "
             "las <strong>culebreras</strong> por los ojos amarillos enormes y las patas "
             "desnudas; los <strong>buitres</strong> por la cabeza (dorsiblanco: negra y "
             "delgada, en piña; orejudo: rosada y enorme; cabeciblanco: blanca, solitario); los "
             "<strong>azores y gavilanes</strong> por las patas rojas o amarillas y el "
             "obispillo; los <strong>aguiluchos</strong> por el vuelo bajo y bamboleante; los "
             "<strong>halcones</strong> por las alas puntiagudas y el vuelo directo; los "
             "<strong>búhos</strong> por el ojo (amarillo, naranja u oscuro) y el tamaño. "
             "<strong>Y mirad la fecha:</strong> el ratonero, los aguiluchos, la calzada y la "
             "pomerana son europeos que llegan en octubre-noviembre <em>(en Etosha sus "
             "registros arrancan en noviembre)</em>; la de Wahlberg es africana y llega en "
             "agosto-septiembre a criar; los milanos llegan con las lluvias, de noviembre en "
             "adelante.</p>",
    "ave": "<p>Con el coche parado en una charca, las aves llenan las esperas. Estas son las "
           "que <strong>se ven sin ser ornitólogo</strong>: grandes, ruidosas o de color "
           "imposible.</p>"
           "<p><strong>Y seis que se añadieron el 29/08 y que son la razón por la que vienen "
           "ornitólogos a Namibia:</strong> pájaros que <strong>casi solo existen aquí y en el "
           "suroeste de Angola</strong> —el cantor de roca, el papamoscas herero, el alcaudón de "
           "cola blanca, el francolín de Hartlaub, el carbonero de Carp— y la <strong>alondra de "
           "Gray</strong>, del color exacto de la gravilla del Namib. No son rarezas de otro "
           "sitio: los cinco primeros caen en <strong>Damaraland</strong> y la alondra, en la "
           "<strong>costa de Swakopmund</strong>, y sus cifras lo dicen.</p>"
           "<p><strong>Y la grulla carunculada entró por la puerta de atrás.</strong> Se metió "
           "en la guía como fauna del Zambeze —es la grulla del norte mojado— y al medirla "
           "resultó tener <strong>18 registros de octubre-noviembre dentro de Etosha</strong>, "
           "más que muchas fichas que nadie discute. Así que está aquí, al lado de la grulla "
           "azul, que es la otra: <em>azul</em>, gris entera con la cabeza abultada; "
           "<em>carunculada</em>, más grande, con el cuello blanco y dos carúnculas colgando.</p>",
    "reptil": "<p><strong>Las tres primeras son seguridad, no coleccionismo.</strong> Dormís "
              "trece noches en tienda y andáis por Sossusvlei y Damaraland: lo útil no es "
              "distinguirlas de lejos, es <strong>saber qué NO hacer</strong>. Nunca metas la "
              "mano donde no ves, <strong>mira dónde pisas al anochecer</strong> —que es cuando "
              "salen a la pista tibia—, linterna para ir al baño, y si te encuentras una, "
              "<strong>quédate quieto y retrocede</strong>: casi todas las mordeduras pasan al "
              "intentar matarlas o cogerlas.</p>"
              "<p>Las otras catorce son de las que apetece ver: el <strong>camaleón que "
              "corre</strong>, el <strong>gecko translúcido</strong> de las dunas, el "
              "<strong>agama naranja</strong> de las rocas de Damaraland, los tres "
              "del campamento de Etosha —el <strong>escinco</strong> de los recintos, el "
              "<strong>gecko</strong> de las noches de Okaukuejo y el <strong>galápago</strong> "
              "que caza quéleas— y los dos diurnos del 11/08: el <strong>gecko que cambió "
              "la noche por el día</strong> en la costa de la niebla y el <strong>lagarto de "
              "nariz de cuña</strong> de la base de las dunas. Desde el 29/08, también el "
              "<strong>gecko gigante del suelo</strong>, que no trepa: vive en la arena y de "
              "día está bajo tierra.</p>",
    "costa": "<p>Etosha no es toda la fauna del viaje. Esto es lo que veréis <strong>fuera del "
             "parque</strong>: en <strong>Cape Cross</strong> (D7), en la laguna de "
             "<strong>Walvis Bay</strong> (D5–D6), en los roquedos de Damaraland y en la arena "
             "del Namib. La laguna, por cierto, no es una charca cualquiera: <strong>sitio "
             "Ramsar desde 1995</strong> y descrita como el humedal costero más importante del "
             "África austral en número de aves — el conteo récord, 242.000 en un solo verano. "
             "La <strong>ardilla terrestre</strong> es la excepción a caballo: campa "
             "igual por dentro de Etosha —de ahí sale su banda— que por los campamentos "
             "del oeste.</p>"
             "<p><strong>Los cuatro últimos son del 29/08 y estaban donde nadie los buscaba: en "
             "vuestra propia costa.</strong> Se metieron en la guía como fauna del sur —las "
             "islas de Lüderitz— y GBIF los devolvió a la caja de Walvis Bay y Swakopmund: "
             "<strong>alcatraz del Cabo</strong> (228 registros de octubre-noviembre ahí), "
             "<strong>cormorán de las bancas</strong> (65), <strong>pingüino africano</strong> "
             "(65) y la <strong>ballena franca austral</strong>, que es la excepción — cuatro "
             "registros y se va antes de que lleguéis. Se quedan en la parte de la ruta porque "
             "el dato dice que están, no porque apetezca.</p>",
    "bicho": "<p>Los vecinos de cada braai — en un viaje de camping <strong>se dejan ver más "
             "que el leopardo</strong>, aunque en los registros ni salgan: a GBIF nadie sube "
             "termitas, y la banda de abajo mide registros, no presencia. "
             "Van aquí por tres motivos distintos: los que hay que "
             "<strong>respetar</strong> (escorpión), los que dan un susto y son "
             "<strong>inofensivos</strong> (solífugo, shongololo), y los que explican cómo "
             "funciona este desierto (el escarabajo que bebe niebla, la termita que construye).</p>"
             "<p><strong>Y uno que no es anécdota:</strong> el mosquito. Es, de largo, el animal "
             "más peligroso de la ruta — la profilaxis está en "
             "<a href='#doc-04'><code>04</code></a>.</p>",
    "norte": "<p><strong>Aquí empieza la Namibia que este viaje no ve.</strong> Todo lo de "
             "abajo vive donde hay <strong>agua todo el año</strong>: la Franja de Caprivi, el "
             "Okavango, el Kwando, el Chobe y el Zambeze, más el Kunene en la frontera con "
             "Angola. Son 400 km al noreste de Etosha y otro viaje: la diferencia entre este "
             "país y el de al lado <strong>no la marcan los animales, la marca el agua</strong> "
             "<em>(el reparto entero, en <code>aparte/fauna-namibia-okavango-zambia.md</code>)</em>.</p>"
             "<p><strong>Ninguna de estas fichas lleva porcentaje de avistamiento de vuestro "
             "viaje, y no es un olvido:</strong> la línea de arriba mide las cuatro zonas de la "
             "ruta y en casi todas da cero. Lo que hay que mirar aquí es la línea "
             "<strong>«En Namibia»</strong>, que dice en qué región del país está cada una y "
             "con cuántos registros. Dos avisos que da el propio dato: el "
             "<strong>puku</strong> tiene <strong>catorce</strong> registros en todo el país "
             "—trece en el Zambezi— y el <strong>sitatunga</strong>, catorce; no son animales "
             "difíciles de ver, son animales que en Namibia casi no hay.</p>",
    "kalahari": "<p>Y cuatro que no son de una región sino de una <strong>manera de vivir</strong>: "
                "de noche, bajo tierra o en la arena roja del este. La <strong>suricata</strong> "
                "es del Kalahari y por eso salió del catálogo el 09/08 — vuelve aquí, en su "
                "sitio. El <strong>oricteropo</strong> y el <strong>pangolín</strong> son los "
                "dos animales que todo guía africano quiere enseñar y casi ninguno enseña: "
                "73 y 43 registros en todo el país, y de noche. Y la <strong>pitón de "
                "Anchieta</strong>, con 26 registros, es de las serpientes menos vistas de "
                "África y vive precisamente en el noroeste, cerca de por donde pasáis.</p>",
}

PELIGRO = {"reptil"}


def _negrita(t):
    t = marca_texto(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"(?<![\w*])\*(?!\*)(.+?)(?<!\*)\*(?![\w*])", r"<em>\1</em>", t)


def verlo(slug):
    """La linea de «qué posibilidades hay», con las dos fuentes por orden de calidad.

    Si Expert Africa publica el porcentaje de sus viajeros que lo vio en alguno de los
    tres campamentos, ese numero manda: es una probabilidad de avistamiento de verdad.
    Si no, va el indice de registros de GBIF, que cubre el catalogo entero pero mide
    otra cosa —lo que se registra, no lo que se ve— y por eso lleva otra etiqueta.
    """
    p = avistamientos.porcentajes(slug)
    if p:
        css, pico, detalle, partes = p
        return (f'<p class="verlo v-{css}"><span class="banda">{pico} lo vio</span>'
                f'{detalle} · <span class="fino">{partes} estancias</span></p>')
    i = avistamientos.indice(slug)
    if not i:
        return ""
    css, banda, detalle = i
    return (f'<p class="verlo v-{css}"><span class="banda">{banda}</span>'
            f'<span class="fino">{detalle}</span></p>')


def en_namibia(slug):
    """La linea de «donde vive en Namibia», que es la que hace de esta una guia del pais.

    La de arriba (`verlo`) contesta si se va a ver EN ESTE VIAJE, con las cuatro zonas de
    la ruta y filtrada a octubre y noviembre. Esta contesta donde vive, con las trece
    regiones y sin filtrar por mes. Son preguntas distintas y por eso van en dos lineas
    distintas: mezclarlas es como sumar el mapa y el calendario.
    """
    d = pais.donde(slug)
    if not d:
        return ""
    texto, _region = d
    return (f'<p class="pais"><span class="marca-et">En Namibia</span>{texto}</p>')


def ficha(slug, es, en, sci):
    cr = comun.creditos().get("fauna/" + slug, {})
    donde = DONDE.get(slug, "")
    bloque = (f'<p class="donde"><span class="marca-et">Dónde</span>{_negrita(donde)}</p>'
              if donde else "")
    cuantos = CUANTOS.get(slug, "")
    if cuantos:
        bloque += (f'<p class="cuantos"><span class="marca-et">Cuántos</span>'
                   f'{_negrita(cuantos)}</p>')
    return (f'<article class="sp"><div class="foto">'
            f'<img src="{comun.img_fauna(slug)}" alt="{es}"></div>'
            f'<div class="txt"><h3>{es}</h3>'
            f'<p class="nom"><em>{sci}</em> · {en}</p>'
            f'{verlo(slug)}'
            f'<p class="id">{_negrita(ID.get(slug, ""))}</p>{bloque}'
            f'{en_namibia(slug)}</div>'
            f'<p class="cred">Foto: {cr.get("autor", "autor no indicado")} · '
            f'{cr.get("licencia", "")}</p></article>')


# Los grupos que NO son de la ruta: la parte 2 de la guia. El corte no es de estilo, es
# de honestidad — lo de la parte 1 lleva un porcentaje de avistamiento que significa algo
# y lo de la parte 2, no: son animales que con este itinerario no se van a ver.
FUERA_DE_LA_RUTA = ("norte", "kalahari")

PARTES = {
    "felino": ("Parte 1 · La fauna de vuestra ruta",
               "Lo que cae en los 2.798 km de este viaje: el Namib, la costa, Damaraland y "
               "Etosha. Cada ficha lleva <strong>qué posibilidades hay de verla</strong>, "
               "medida en las cuatro zonas de la ruta y en octubre y noviembre."),
    "norte": ("Parte 2 · El resto de Namibia",
              "Y esto es lo que el país tiene y <strong>este viaje no pisa</strong>. Ni una "
              "ficha de aquí es una expectativa: van con el sitio al que habría que ir a "
              "buscarlas, que casi siempre es el norte mojado o el Kalahari. La línea "
              "<strong>«En Namibia»</strong> de cada ficha es la que manda en esta parte."),
}


def secciones():
    out = []
    for clave, nombre, lista in catalogo.GRUPOS_FAUNA:
        if clave in PARTES:
            titulo, entradilla = PARTES[clave]
            out.append(f'<div class="parte"><h2>{titulo}</h2>'
                       f'<p>{marca_texto(entradilla)}</p></div>')
        fichas = "".join(ficha(s, es, en, sci) for s, es, en, sci, _f in lista)
        peligro = " peligro" if clave in PELIGRO else ""
        # titulo e intro juntos en una caja que no se parte: si no, el titulo se queda
        # huerfano al pie de una pagina y la intro arranca en la siguiente
        out.append(f'<div class="cabecera"><h2>{nombre}<span class="cuenta">{len(lista)} especies</span></h2>'
                   f'<div class="intro{peligro}">{marca_texto(INTROS.get(clave, ""))}</div></div>'
                   f'<div class="rejilla">{fichas}</div>')
    return "".join(out)


def total():
    return sum(len(l) for _, _, l in catalogo.GRUPOS_FAUNA)


def de_la_ruta():
    return sum(len(l) for c, _, l in catalogo.GRUPOS_FAUNA if c not in FUERA_DE_LA_RUTA)


def del_resto():
    return sum(len(l) for c, _, l in catalogo.GRUPOS_FAUNA if c in FUERA_DE_LA_RUTA)


def remite_desde_dossier(ancla=""):
    """El dossier NO lleva las fichas dentro: solo remite a la guia suelta.

    Meter las 148 fotos de fauna dentro del dossier lo engordaba en unas veinte paginas y
    varios megas, y duplicaba un documento que ya existe aparte y que ademas se imprime
    solo para llevarlo en la guantera. Aqui queda el enlace y el resumen de lo que hay.
    """
    cuentas = " · ".join(f"<b>{len(l)}</b> {n.lower()}" for _, n, l in catalogo.GRUPOS_FAUNA)
    return f"""
<section class="doc sin-columnas remite" id="fauna">
  <h1 class="titulo">La guía de campo va aparte{ancla}</h1>
  <blockquote>
    <h2>{total()} especies con foto, en su propio PDF</h2>
    <p>La fauna <strong>no está dentro de este dossier a propósito</strong>: son
    {total()} fichas con fotografía que engordarían el volumen en más de veinte páginas y
    varios megas, y que se usan en otro momento y de otra forma — en el coche, con el motor
    apagado en una charca, no leyendo del tirón en casa.</p>
    <p><strong>Y desde el 29/08 no es solo la fauna de la ruta:</strong> son
    {de_la_ruta()} especies de este viaje más {del_resto()} del resto del país, y
    <strong>cada ficha dice en qué regiones de Namibia vive</strong> la especie, medido en
    GBIF sobre las trece divisiones administrativas.</p>
    <p><strong>Está en <code>guia-fauna-namibia.pdf</code></strong>, en la raíz del repo:
    {cuentas}. Cada ficha lleva el nombre en castellano, el científico y el inglés —el de
    los carteles del parque—, cómo reconocer la especie, <strong>qué posibilidades hay de
    verla</strong> —medidas, no dichas a ojo—, <strong>en qué región del país vive</strong>
    y, donde hay fuente, dónde y cuándo verla y cuántas quedan.</p>
    <p>Delante de las fichas va lo que no cabe aquí: <strong>cómo se hace un safari</strong>
    —la ropa, lo que tiene que ir a mano dentro del coche, la táctica de la charca y lo
    que es reglamento y no consejo—.</p>
    <p><strong>Imprímela aparte y déjala en la guantera.</strong> Se consulta con una mano
    y con el motor parado, que es cuando sirve.</p>
  </blockquote>
</section>"""


def html_suelto():
    css = "".join(open(os.path.join(HERE, "estilo", f)).read()
                  for f in ("comun.css", "fauna.css"))
    tipos = comun.tipografias(os.path.join(HERE, "tipos"))
    cuentas = " · ".join(f"<b>{len(l)}</b> {n.lower()}" for _, n, l in catalogo.GRUPOS_FAUNA)
    cr = comun.creditos()
    lista = "".join(
        f'<li><b>{v["es"]}</b> — {v["autor"]}, <i>{v["licencia"]}</i> · '
        f'<span class="u">{v["pagina"]}</span></li>'
        for k, v in sorted(cr.items(), key=lambda x: x[1].get("es", "")) if k.startswith("fauna/"))
    fuentes = "".join(f"<li>{f}</li>" for f in FUENTES_ETOSHA)
    poblacion = "".join(f"<li>{f}</li>" for f in FUENTES_POBLACION)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Fauna de Namibia — guía de campo</title>
<style>{tipos}</style><style>{css}</style></head><body>
<section class="guia-portada">
  <div class="epi">Namibia · 31 de octubre – 14 de noviembre de 2026</div>
  <h1>Fauna de Namibia</h1>
  <h2>Guía de campo · {total()} especies — {de_la_ruta()} de vuestra ruta y {del_resto()} del resto del país</h2>
  <div class="datos">{cuentas}<br>
    Cada ficha dice <b>dónde vive en Namibia</b>, región por región<br>
    Cuatro noches en Etosha · dos <b>dentro del parque</b><br>
    <b>Okaukuejo</b> · 9 nov &nbsp;—&nbsp; <b>Halali</b> · 10 nov &nbsp;—&nbsp;
    <b>Onguma</b> · 11 y 12 nov<br>
    Final de la estación seca: la fauna, concentrada en las charcas</div>
  <div class="pie">Fotografías de Wikimedia Commons, todas con licencia libre:<br>
  autoría y licencia bajo cada foto y en los créditos del final.<br>
  Los rasgos de identificación son descriptivos; lo específico de Etosha va con su fuente.<br>
  El reparto por regiones sale de GBIF y de los límites de OpenStreetMap: se mide, no se dice a ojo.</div>
</section>
{portadilla()}
<section class="doc sin-columnas fauna">{secciones()}</section>
<section class="final">
  <h1 class="titulo">Créditos de las fotografías</h1>
  <p class="nota">Todas las imágenes proceden de <b>Wikimedia Commons</b> con licencia libre
  (CC BY, CC BY-SA, CC0 o dominio público), que exige citar autor y licencia.</p>
  <ul>{lista}</ul>
  {'<h2>Fuentes del «dónde y cuándo»</h2><ul>' + fuentes + '</ul>' if fuentes else ''}
  <h2>Fuentes de las posibilidades y de los recuentos</h2>
  <ul>{avistamientos.fuente_html()}{pais.fuente_html()}{poblacion}</ul>
</section>
</body></html>"""


def main():
    salida_html = os.path.join(HERE, "guia-fauna.html")
    salida_pdf = os.path.join(RAIZ, "guia-fauna-namibia.pdf")
    open(salida_html, "w").write(html_suelto())
    print(f"HTML: {os.path.getsize(salida_html) // 1024} KB · {total()} especies")
    if "--html" in sys.argv:
        return 0
    imprimir.a_pdf(salida_html, salida_pdf, izquierda="Namibia 2026 · guía de campo",
                   derecha=f"{total()} especies de Namibia", espera=2)
    print(f"{os.path.relpath(salida_pdf, RAIZ)} · {imprimir.paginas(salida_pdf)} páginas · "
          f"{os.path.getsize(salida_pdf) // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
