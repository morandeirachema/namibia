#!/usr/bin/env python3
"""Comprobaciones baratas antes de dar un PDF por bueno.

No valida el contenido del viaje —eso lo hace la verificacion a tres votos del propio
dossier—, sino que el build no se ha roto por debajo: que estan todas las imagenes, que
ninguna se ha colado con licencia no libre, que el catalogo y los creditos cuadran y que
los PDF existen y tienen paginas.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import catalogo                                                    # noqa: E402

LICENCIAS_OK = ("CC BY", "CC0", "Public domain", "FAL")
FALLOS = []


def mal(msg):
    FALLOS.append(msg)
    print("  FALLO  " + msg)


def bien(msg):
    print("  ok     " + msg)


def revisa_imagenes():
    ruta = os.path.join(RAIZ, "img", "creditos.json")
    if not os.path.exists(ruta):
        return mal("no existe img/creditos.json — ejecuta `python3 fuente/descargar.py`")
    cr = json.load(open(ruta))

    esperadas = {f"lugares/{s}" for s, _, _ in catalogo.LUGARES}
    esperadas |= {f"fauna/{e[0]}" for _, _, l in catalogo.GRUPOS_FAUNA for e in l}
    faltan = esperadas - set(cr)
    if faltan:
        mal(f"{len(faltan)} imagenes del catalogo sin descargar: {sorted(faltan)[:4]}…")
    sobran = set(cr) - esperadas
    if sobran:
        mal(f"{len(sobran)} imagenes descargadas que ya no estan en el catalogo: {sorted(sobran)[:4]}…")

    sin_fichero = [k for k, v in cr.items()
                   if not os.path.exists(os.path.join(RAIZ, "img", v["carpeta"], v["local"]))]
    if sin_fichero:
        mal(f"{len(sin_fichero)} entradas de creditos sin fichero en disco")

    no_libres = [f'{k} ({v["licencia"]})' for k, v in cr.items()
                 if not v["licencia"].startswith(LICENCIAS_OK)]
    if no_libres:
        mal(f"licencia no libre en: {no_libres}")

    sin_autor = [k for k, v in cr.items() if not v.get("autor")]
    if sin_autor:
        mal(f"{len(sin_autor)} imagenes sin autor — la licencia obliga a citarlo")

    if not (faltan or sobran or sin_fichero or no_libres or sin_autor):
        bien(f"{len(cr)} imagenes, todas con fichero, licencia libre y autor")


def revisa_geo():
    faltan = [n for n in ("paises.json", "parques.json", "etosha_pan.json",
                          "etosha_pistas.json", "etosha_puntos.json", "ruta.json")
              if not os.path.exists(os.path.join(HERE, "geo", n))]
    if faltan:
        return mal(f"faltan geodatos: {faltan} — ejecuta `python3 fuente/geodatos.py`")
    ruta = json.load(open(os.path.join(HERE, "geo", "ruta.json")))
    sin_traza = [e["id"] for e in ruta if e["km"] is None]
    if sin_traza:
        mal(f"etapas sin trazado: {sin_traza}")
    total = sum(e["km"] or 0 for e in ruta)
    if not 2200 < total < 3200:
        mal(f"la ruta suma {total:.0f} km, fuera de lo razonable para este viaje")
    else:
        bien(f"ruta completa: {len(ruta)} etapas, {total:.0f} km")


def revisa_pdf(nombre, minimo):
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return mal(f"no existe {nombre}")
    salida = subprocess.run(["pdfinfo", ruta], capture_output=True, text=True).stdout
    paginas = next((int(l.split()[1]) for l in salida.splitlines()
                    if l.startswith("Pages:")), 0)
    mb = os.path.getsize(ruta) / 1024 / 1024
    if paginas < minimo:
        mal(f"{nombre} tiene {paginas} paginas, esperaba al menos {minimo}")
    else:
        bien(f"{nombre}: {paginas} paginas, {mb:.1f} MB")


def revisa_escala(nombre, alto=267, tolerancia=3):
    """Vigila que Chrome no haya encogido el PDF entero.

    Si algo no cabe a lo ancho —una URL larga en una columna de 89 mm, sin ir mas
    lejos— el navegador ensancha la caja, abre una tercera columna y reduce TODAS
    las paginas para que quepan: el documento sale a dos tercios sin avisar. El
    ancho no lo delata (la portada es `width:100%` y se encoge con el resto, asi
    que sigue llenando la caja); el alto si, porque esta en milimetros: la
    portada pide 267 mm y en un PDF sano mide eso.

    Se mide la PRIMERA mancha continua de la pagina 1 —la foto de portada—, no de
    la primera a la ultima fila con tinta: si no, el filete del pie de pagina
    entra en la cuenta y disimula un encogido suave.
    """
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "p")
        r = subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "72", "-png", ruta, base],
                           capture_output=True)
        png = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
        if r.returncode or not png:
            return bien(f"{nombre}: sin pdftoppm, no se mide la escala")
        try:
            from PIL import Image
        except ImportError:
            return bien(f"{nombre}: sin Pillow, no se mide la escala")
        im = Image.open(os.path.join(tmp, png[0])).convert("L")
        w, h = im.size
        px = im.load()
        tinta = [sum(1 for x in range(w) if px[x, y] < 200) > w * .5 for y in range(h)]
        try:
            a = tinta.index(True)
            b = tinta.index(False, a) - 1
        except ValueError:
            a, b = 0, -1
        mm = (b - a + 1) / 72 * 25.4 if b >= a else 0
    if abs(mm - alto) > tolerancia:
        mal(f"{nombre}: la portada mide {mm:.0f} mm de alto y deberia medir {alto}. "
            f"Si es menos, Chrome ha encogido el PDF entero porque algo no cabe a lo ancho: "
            f"busca una URL sin partir o un diagrama que se salga de la columna")
    else:
        bien(f"{nombre}: escala correcta, la portada mide sus {mm:.0f} mm")


def revisa_paginas_readme():
    """El README anuncia cuantas paginas tiene cada PDF: que no se quede desfasado."""
    import re
    texto = open(os.path.join(RAIZ, "README.md")).read()
    for nombre in ("dossier-namibia-2026.pdf", "guia-fauna-etosha.pdf"):
        ruta = os.path.join(RAIZ, nombre)
        if not os.path.exists(ruta):
            continue
        salida = subprocess.run(["pdfinfo", ruta], capture_output=True, text=True).stdout
        real = next((int(l.split()[1]) for l in salida.splitlines()
                     if l.startswith("Pages:")), 0)
        dichas = {int(n) for n in re.findall(
            re.escape(nombre) + r"[^\n]*?(\d+)\s+páginas", texto)}
        dichas |= {int(n) for n in re.findall(
            r"\((\d+)\s+páginas[^\n]*?\)", texto)} if "guia-fauna" in nombre else set()
        malas = {n for n in dichas if n != real}
        if malas:
            mal(f"el README dice {sorted(malas)} paginas de {nombre}, y tiene {real}")
        else:
            bien(f"{nombre}: el README dice las paginas que son ({real})")


def revisa_indice_readme():
    """El indice del README se numera a mano: que no se descuadre ni pierda un documento."""
    import re
    texto = open(os.path.join(RAIZ, "README.md")).read()
    listados = re.findall(r"^(\d+)\. .*?\[\*\*`(\d\d)-[a-z-]+`\*\*\]", texto, re.M)
    numeros = [int(n) for n, _ in listados]
    docs = {d for _, d in listados}
    if numeros != list(range(1, len(numeros) + 1)):
        return mal(f"el indice del README va numerado {numeros}, y deberia ir 1..{len(numeros)}")
    en_disco = {f[:2] for f in os.listdir(RAIZ) if re.match(r"\d\d-.*\.md$", f)}
    if en_disco - docs:
        return mal(f"el indice del README no lista {sorted(en_disco - docs)}")
    bien(f"el indice del README: {len(numeros)} documentos, numerados y completos")


def revisa_documentos():
    import re
    docs = sorted(f for f in os.listdir(RAIZ) if re.match(r"\d\d-.*\.md$", f))
    huecos = [f for f in docs if not open(os.path.join(RAIZ, f)).read().startswith("# ")]
    if huecos:
        mal(f"documentos sin titulo de primer nivel: {huecos}")
    else:
        bien(f"{len(docs)} documentos, todos con su titulo")


def main():
    print("Comprobando el build…")
    revisa_documentos()
    revisa_imagenes()
    revisa_geo()
    revisa_pdf("dossier-namibia-2026.pdf", 40)
    revisa_pdf("guia-fauna-etosha.pdf", 8)
    revisa_escala("dossier-namibia-2026.pdf")
    revisa_paginas_readme()
    revisa_indice_readme()
    print(f"\n{'TODO EN ORDEN' if not FALLOS else str(len(FALLOS)) + ' FALLOS'}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    raise SystemExit(main())
