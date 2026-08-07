#!/usr/bin/env python3
"""Descarga de Wikimedia Commons las imagenes del catalogo, con licencia y autoria.

Resuelve cada fichero de `catalogo.py` contra la API de Commons, baja una version
reducida (el original de algunas fotos pasa de 30 MP y no cabe en un PDF), y escribe:

    img/lugares/<slug>.jpg
    img/fauna/<slug>.jpg
    img/creditos.json        <- autoria + licencia + URL de cada foto

Idempotente: si el JPEG ya esta y no se pide --forzar, no vuelve a bajarlo, pero si
refresca los creditos. Uso:

    python3 fuente/descargar.py            # solo lo que falte
    python3 fuente/descargar.py --forzar   # todo otra vez
"""
import json
import os
import re
import sys
import time
import urllib.parse

import catalogo
import red

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, "img")

# Ancho de descarga y ancho final, por carpeta. El original de algunas fotos pasa de
# 30 MP: se pide miniatura a Commons y luego se reescala aqui al tamano de uso real.
#   lugares -> foto a ancho de columna (186 mm). 1400 px son ~190 ppp: de sobra en papel.
#   fauna   -> ficha en rejilla de 3 columnas (~57 mm de ancho). 700 px son ~310 ppp.
# El objetivo es que el PDF entero quepa en unos pocos MB sin que se note en papel.
ANCHO_DESCARGA = 1800
ANCHO_FINAL = {"lugares": 1400, "fauna": 700}
CALIDAD = 78

LICENCIAS_OK = ("CC BY", "CC0", "Public domain", "FAL")


def pide(url, timeout=60):
    """Commons devuelve 429 con facilidad y manda Retry-After: seis intentos."""
    return red.pide(url, timeout=timeout, intentos=6)


def api(params, base="https://commons.wikimedia.org/w/api.php"):
    params = dict(params, format="json", formatversion="2")
    return json.loads(pide(base + "?" + urllib.parse.urlencode(params)))


def limpia(v):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", v or "")).strip()


def fichas(ficheros):
    """Metadatos de N ficheros de Commons en lotes de 50 — una llamada por lote."""
    out = {}
    lote = 50
    for i in range(0, len(ficheros), lote):
        trozo = ficheros[i:i + lote]
        d = api({"action": "query", "prop": "imageinfo",
                 "titles": "|".join("File:" + f for f in trozo),
                 "iiprop": "url|extmetadata|mime|size", "iiurlwidth": str(ANCHO_DESCARGA)})
        # Commons normaliza los titulos (guion bajo, mayuscula inicial): hay que
        # deshacer esa normalizacion para poder volver al nombre del catalogo.
        norm = {n["to"]: n["from"] for n in d.get("query", {}).get("normalized", [])}
        for pg in d.get("query", {}).get("pages", []):
            pedido = norm.get(pg["title"], pg["title"])[5:]
            if pg.get("missing") or "imageinfo" not in pg:
                out[pedido] = None
                continue
            ii = pg["imageinfo"][0]
            em = ii.get("extmetadata", {})
            g = lambda k: limpia(em.get(k, {}).get("value", ""))     # noqa: E731
            out[pedido] = {
                "fichero": pg["title"],
                "url": ii.get("thumburl") or ii.get("url"),
                "pagina": ii.get("descriptionurl"),
                "licencia": g("LicenseShortName"),
                "licencia_url": em.get("LicenseUrl", {}).get("value", ""),
                "autor": g("Artist") or "autor no indicado",
                "ancho": ii.get("width"),
                "alto": ii.get("height"),
            }
        time.sleep(1)
    return out


def baja(url, destino, ancho):
    """Baja, reescala al ancho de uso y reescribe como JPEG progresivo sin metadatos."""
    from io import BytesIO

    from PIL import Image

    im = Image.open(BytesIO(pide(url, timeout=120)))
    im = im.convert("RGB")
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    im.save(destino, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
    return os.path.getsize(destino)


def entradas():
    """(grupo_carpeta, slug, fichero, extra) de todo el catalogo."""
    for slug, pie, fichero in catalogo.LUGARES:
        yield "lugares", slug, fichero, {"pie": pie}
    for clave, _nombre, lista in catalogo.GRUPOS_FAUNA:
        for slug, es, en, sci, fichero in lista:
            yield "fauna", slug, fichero, {"grupo": clave, "es": es, "en": en, "sci": sci}


def main():
    forzar = "--forzar" in sys.argv
    todo = list(entradas())
    print(f"Resolviendo {len(todo)} ficheros en Commons…")
    meta = fichas(sorted({e[2] for e in todo}))

    creditos, fallos = {}, []
    for carpeta, slug, fichero, extra in todo:
        destino_dir = os.path.join(IMG, carpeta)
        os.makedirs(destino_dir, exist_ok=True)
        destino = os.path.join(destino_dir, slug + ".jpg")
        clave = f"{carpeta}/{slug}"
        try:
            info = meta.get(fichero)
            if not info:
                fallos.append(f"{clave}: no existe «{fichero}» en Commons")
                continue
            if not info["licencia"].startswith(LICENCIAS_OK):
                fallos.append(f"{clave}: licencia no libre «{info['licencia']}»")
                continue
            if forzar or not os.path.exists(destino):
                tam = baja(info["url"], destino, ANCHO_FINAL[carpeta])
                time.sleep(0.4)
            else:
                tam = os.path.getsize(destino)
            creditos[clave] = dict(info, slug=slug, carpeta=carpeta, local=slug + ".jpg",
                                   bytes=tam, **extra)
            print(f"OK  {clave:34s} {info['licencia']:16s} {info['autor'][:34]:36s} {tam // 1024:5d} KB")
        except Exception as e:                                   # noqa: BLE001
            fallos.append(f"{clave}: {e}")
            print(f"!!  {clave}: {e}")

    with open(os.path.join(IMG, "creditos.json"), "w") as f:
        json.dump(creditos, f, indent=1, ensure_ascii=False, sort_keys=True)

    print(f"\n{len(creditos)} imagenes en img/ · creditos en img/creditos.json")
    if fallos:
        print(f"\n{len(fallos)} FALLOS:")
        for x in fallos:
            print("   ", x)
        return 1
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(main())
