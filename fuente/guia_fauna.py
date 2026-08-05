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

import catalogo                                                    # noqa: E402
import comun                                                       # noqa: E402
import imprimir                                                    # noqa: E402
from comun import RAIZ, marca_texto                                # noqa: E402
from textos_especies import ID                                     # noqa: E402

try:
    from textos_etosha import DONDE, FUENTES_ETOSHA, INTRO_EXTRA
except ImportError:                                                # aun sin el informe
    DONDE, INTRO_EXTRA, FUENTES_ETOSHA = {}, "", []

INTROS = {
    "mamifero": "<p><strong>Cada ficha</strong> lleva el nombre en castellano, el científico y "
                "el inglés —el de los carteles del parque— y los rasgos que sirven para "
                "distinguirla <em>en el campo</em>.</p>" + INTRO_EXTRA,
    "ave": "<p>Con el coche parado en una charca, las aves llenan las esperas. Estas son las "
           "que <strong>se ven sin ser ornitólogo</strong>: grandes, ruidosas o de color "
           "imposible.</p>",
    "reptil": "<p><strong>Las tres primeras son seguridad, no coleccionismo.</strong> Dormís "
              "once noches en tienda y andáis por Sossusvlei y Damaraland: lo útil no es "
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


def ficha(slug, es, en, sci):
    cr = comun.creditos().get("fauna/" + slug, {})
    donde = DONDE.get(slug, "")
    bloque = (f'<p class="donde"><span class="marca-et">Etosha</span>{_negrita(donde)}</p>'
              if donde else "")
    return (f'<article class="sp"><div class="foto">'
            f'<img src="{comun.img_fauna(slug)}" alt="{es}"></div>'
            f'<div class="txt"><h3>{es}</h3>'
            f'<p class="nom"><em>{sci}</em> · {en}</p>'
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

    Meter las 83 fotos de fauna dentro del dossier lo engordaba en unas veinte paginas y
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
    los carteles del parque—, cómo reconocer la especie y, donde hay fuente, dónde y
    cuándo verla en Etosha.</p>
    <p><strong>Imprímela aparte y déjala en la guantera.</strong> Son quince páginas: cabe
    grapada en la puerta del coche y se consulta con una mano.</p>
  </blockquote>
</section>"""


EXTRA_CSS = """
.intro { background: var(--crema); border-left: 2.6pt solid var(--oxido);
         padding: 3mm 4mm; margin: 0 0 3.5mm; font-size: 8.2pt; border-radius: 0 1.5mm 1.5mm 0;
         column-span: all; break-inside: avoid; }
.intro p { margin: 0 0 1.4mm; } .intro p:last-child { margin: 0; }
.intro.peligro { background: var(--rojo-bg); border-left-color: var(--rojo); }
.fauna h2 { margin-top: 7mm; }
.guia-portada { position: relative; width: 100%; height: var(--caja-alto); overflow: hidden;
  page-break-after: always; background: #1D2B21; color: #F4EFE6; border-radius: 2mm;
  display: flex; flex-direction: column; justify-content: center; padding: 0 18mm;
  text-align: center; }
.guia-portada .epi { font-family: var(--sans); letter-spacing: .34em; text-transform: uppercase;
  font-size: 8pt; color: #C9B98F; margin-bottom: 8mm; }
.guia-portada h1 { font-family: var(--sans); font-size: 40pt; font-weight: 700; margin: 0 0 3mm;
  line-height: 1.02; color: #fff; border: 0; }
.guia-portada h2 { font-family: var(--serif); font-style: italic; font-size: 14pt;
  font-weight: 400; color: #C9B98F; margin: 0 0 12mm; border: 0; }
.guia-portada .datos { font-family: var(--sans); font-size: 10pt; line-height: 1.95; }
.guia-portada .datos b { color: #E9DCC0; }
.guia-portada .pie { margin-top: 14mm; font-family: var(--sans); font-size: 7.8pt;
  color: #93A394; line-height: 1.65; }
.final { page-break-before: always; padding: 0; }
.final ul { columns: 2; column-gap: 7mm; padding-left: 0; list-style: none;
            font-size: 7.2pt; line-height: 1.45; }
.final ul li::before { content: none; }
.final li { break-inside: avoid; margin-bottom: 1mm; }
.final .u { color: var(--tinta-3); word-break: break-all; }
"""


def html_suelto():
    css = open(os.path.join(HERE, "estilo", "dossier.css")).read() + EXTRA_CSS
    tipos = comun.tipografias(os.path.join(HERE, "tipos"))
    cuentas = " · ".join(f"<b>{len(l)}</b> {n.lower()}" for _, n, l in catalogo.GRUPOS_FAUNA)
    cr = comun.creditos()
    lista = "".join(
        f'<li><b>{v["es"]}</b> — {v["autor"]}, <i>{v["licencia"]}</i> · '
        f'<span class="u">{v["pagina"]}</span></li>'
        for k, v in sorted(cr.items(), key=lambda x: x[1].get("es", "")) if k.startswith("fauna/"))
    fuentes = "".join(f"<li>{f}</li>" for f in FUENTES_ETOSHA)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Fauna de Etosha — guía de campo</title>
<style>{tipos}</style><style>{css}</style></head><body>
<section class="guia-portada">
  <div class="epi">Namibia · 1–14 de noviembre de 2026</div>
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
<section class="doc sin-columnas fauna">{secciones()}</section>
<section class="final">
  <h1 class="titulo">Créditos de las fotografías</h1>
  <p class="nota">Todas las imágenes proceden de <b>Wikimedia Commons</b> con licencia libre
  (CC BY, CC BY-SA, CC0 o dominio público), que exige citar autor y licencia.</p>
  <ul>{lista}</ul>
  {'<h2>Fuentes de lo específico de Etosha</h2><ul>' + fuentes + '</ul>' if fuentes else ''}
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
