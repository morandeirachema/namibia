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
import comun                                                       # noqa: E402
import imprimir                                                    # noqa: E402
from comun import RAIZ, marca_texto                                # noqa: E402
from textos_especies import ID                                     # noqa: E402
from textos_poblacion import CUANTOS, FUENTES_POBLACION            # noqa: E402
from textos_safari import CONSEJOS                                 # noqa: E402

try:
    from textos_etosha import DONDE, FUENTES_ETOSHA, INTRO_EXTRA
except ImportError:                                                # aun sin el informe
    DONDE, INTRO_EXTRA, FUENTES_ETOSHA = {}, "", []


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
    return f"""
  <p><strong>La línea de arriba de cada ficha dice qué posibilidades hay.</strong> Cuando
  pone <em>«82&nbsp;% lo vio»</em> es literal: viajeros que declararon <strong>una o más
  observaciones durante su estancia en el campamento</strong> (partes de Expert Africa —
  {trozos}). <strong>La unidad es la estancia, no el día ni el viaje</strong>: una o dos
  noches. La cifra grande junta los tres campamentos y detrás va cada uno. Y como aquí se
  duerme en los tres <em>(Okaukuejo 1 noche, Halali 1, Namutoni 2)</em> son <strong>tres
  tiradas</strong>: en las cuatro noches la posibilidad real es más alta que cualquiera de
  estos números. Cuánto más, no lo dicen estos datos, así que no se dice.</p>
  <p>Eso solo existe para catorce especies. Para las otras setenta y siete va un
  <strong>índice de registros de GBIF</strong>: cuánto pesa la especie dentro de los
  registros de su grupo en la zona <strong>en octubre y noviembre</strong> —{mam} de
  mamífero y {aves} de ave solo en Etosha—. Mide <em>lo que se registra</em>, no <em>lo
  que se ve</em>: por eso dice <strong>frecuente</strong> o <strong>escasa</strong>, nunca
  «lo vas a ver».</p>
  <p><strong>Los dos sesgos, por delante:</strong> los partes los rellenan viajeros y hay
  confusiones —un 14&nbsp;% declara antílope sable en Okaukuejo, y en Etosha no hay
  sable—; y a GBIF nadie sube el chacal número doscientos ni casi nada nocturno, así que
  la liebre saltadora sale con cero registros y se ve todas las noches. Cada cifra lleva
  detrás su muestra: con cuatro registros no se afirma nada.</p>
"""


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
  rasgos que distinguen a la especie <em>en el campo</em>. Debajo, dónde y cuándo verla, y
  cuántas quedan cuando hay una cifra publicada que citar.</p>
  {metodo()}
  <h2>Cómo funciona el parque</h2>
  {INTRO_EXTRA}
  {CONSEJOS}
</section>""")


INTROS = {
    "mamifero": "<p>Treinta y una fichas, de lo que se ve en todas las charcas a lo que "
                "hay que tener suerte para cruzarse. <strong>El orden no es alfabético: "
                "es el de siempre</strong> — primero los grandes.</p>",
    "ave": "<p>Con el coche parado en una charca, las aves llenan las esperas. Estas son las "
           "que <strong>se ven sin ser ornitólogo</strong>: grandes, ruidosas o de color "
           "imposible.</p>",
    "reptil": "<p><strong>Las tres primeras son seguridad, no coleccionismo.</strong> Dormís "
              "trece noches en tienda y andáis por Sossusvlei y Damaraland: lo útil no es "
              "distinguirlas de lejos, es <strong>saber qué NO hacer</strong>. Nunca metas la "
              "mano donde no ves, <strong>mira dónde pisas al anochecer</strong> —que es cuando "
              "salen a la pista tibia—, linterna para ir al baño, y si te encuentras una, "
              "<strong>quédate quieto y retrocede</strong>: casi todas las mordeduras pasan al "
              "intentar matarlas o cogerlas.</p>"
              "<p>Las otras ocho son de las que apetece ver: el <strong>camaleón que "
              "corre</strong>, el <strong>gecko translúcido</strong> de las dunas y el "
              "<strong>agama naranja</strong> de las rocas de Damaraland.</p>",
    "costa": "<p>Etosha no es toda la fauna del viaje. Esto es lo que veréis <strong>fuera del "
             "parque</strong>: en <strong>Cape Cross</strong> (D7), en la laguna de "
             "<strong>Walvis Bay</strong> (D5–D6), en los roquedos de Damaraland y en la arena "
             "del Namib.</p>",
    "bicho": "<p>En un viaje de camping, <strong>estos los ves seguro</strong> — más que al "
             "leopardo. Van aquí por tres motivos distintos: los que hay que "
             "<strong>respetar</strong> (escorpión), los que dan un susto y son "
             "<strong>inofensivos</strong> (solífugo, shongololo), y los que explican cómo "
             "funciona este desierto (el escarabajo que bebe niebla, la termita que construye).</p>"
             "<p><strong>Y uno que no es anécdota:</strong> el mosquito. Es, de largo, el animal "
             "más peligroso de la ruta — la profilaxis está en "
             "<a href='#doc-04'><code>04</code></a>.</p>",
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
    Si no, va el indice de registros de GBIF, que cubre las 91 pero mide otra cosa —lo
    que se registra, no lo que se ve— y por eso lleva otra etiqueta.
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
            f'<p class="id">{_negrita(ID.get(slug, ""))}</p>{bloque}</div>'
            f'<p class="cred">Foto: {cr.get("autor", "autor no indicado")} · '
            f'{cr.get("licencia", "")}</p></article>')


def secciones():
    out = []
    for clave, nombre, lista in catalogo.GRUPOS_FAUNA:
        fichas = "".join(ficha(s, es, en, sci) for s, es, en, sci, _f in lista)
        peligro = " peligro" if clave in PELIGRO else ""
        out.append(f'<h2>{nombre}<span class="cuenta">{len(lista)} especies</span></h2>'
                   f'<div class="intro{peligro}">{marca_texto(INTROS.get(clave, ""))}</div>'
                   f'<div class="rejilla">{fichas}</div>')
    return "".join(out)


def total():
    return sum(len(l) for _, _, l in catalogo.GRUPOS_FAUNA)


def remite_desde_dossier(ancla=""):
    """El dossier NO lleva las fichas dentro: solo remite a la guia suelta.

    Meter las 91 fotos de fauna dentro del dossier lo engordaba en unas veinte paginas y
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
    {total()} fichas con fotografía que engordarían el volumen en veinte páginas y varios
    megas, y que se usan en otro momento y de otra forma — en el coche, con el motor
    apagado en una charca, no leyendo del tirón en casa.</p>
    <p><strong>Está en <code>guia-fauna-etosha.pdf</code></strong>, en la raíz del repo:
    {cuentas}. Cada ficha lleva el nombre en castellano, el científico y el inglés —el de
    los carteles del parque—, cómo reconocer la especie, <strong>qué posibilidades hay de
    verla</strong> —medidas, no dichas a ojo— y, donde hay fuente, dónde y cuándo verla y
    cuántas quedan.</p>
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
<title>Fauna de Etosha — guía de campo</title>
<style>{tipos}</style><style>{css}</style></head><body>
<section class="guia-portada">
  <div class="epi">Namibia · 31 de octubre – 14 de noviembre de 2026</div>
  <h1>Fauna del viaje</h1>
  <h2>Guía de campo · {total()} especies de toda la ruta</h2>
  <div class="datos">{cuentas}<br>
    Cuatro noches <b>dentro del parque</b><br>
    <b>Okaukuejo</b> · 9 nov &nbsp;—&nbsp; <b>Halali</b> · 10 nov &nbsp;—&nbsp;
    <b>Namutoni</b> · 11 y 12 nov<br>
    Final de la estación seca: la fauna, concentrada en las charcas</div>
  <div class="pie">Fotografías de Wikimedia Commons, todas con licencia libre:<br>
  autoría y licencia bajo cada foto y en los créditos del final.<br>
  Los rasgos de identificación son descriptivos; lo específico de Etosha va con su fuente.</div>
</section>
{portadilla()}
<section class="doc sin-columnas fauna">{secciones()}</section>
<section class="final">
  <h1 class="titulo">Créditos de las fotografías</h1>
  <p class="nota">Todas las imágenes proceden de <b>Wikimedia Commons</b> con licencia libre
  (CC BY, CC BY-SA, CC0 o dominio público), que exige citar autor y licencia.</p>
  <ul>{lista}</ul>
  {'<h2>Fuentes de lo específico de Etosha</h2><ul>' + fuentes + '</ul>' if fuentes else ''}
  <h2>Fuentes de las posibilidades y de los recuentos</h2>
  <ul>{avistamientos.fuente_html()}{poblacion}</ul>
</section>
</body></html>"""


def main():
    salida_html = os.path.join(HERE, "guia-fauna.html")
    salida_pdf = os.path.join(RAIZ, "guia-fauna-etosha.pdf")
    open(salida_html, "w").write(html_suelto())
    print(f"HTML: {os.path.getsize(salida_html) // 1024} KB · {total()} especies")
    if "--html" in sys.argv:
        return 0
    imprimir.a_pdf(salida_html, salida_pdf, izquierda="Namibia 2026 · guía de campo",
                   derecha=f"{total()} especies", espera=2)
    print(f"{os.path.relpath(salida_pdf, RAIZ)} · {imprimir.paginas(salida_pdf)} páginas · "
          f"{os.path.getsize(salida_pdf) // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
