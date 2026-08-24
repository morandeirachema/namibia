# -*- coding: utf-8 -*-
"""Donde esta Chrome. Un solo sitio, sin dependencias.

Lo necesitan dos programas que por lo demas no se parecen en nada —`mapa.py`, para
sacar el PNG de cada mapa de una captura headless, e `imprimir.py`, para maquetar los
PDF por CDP—, y `mapa.py` presume de no arrastrar dependencias: por eso esto no vive
en `comun.py`, que importa markdown-it.

Se busca primero en el PATH —que es lo que hay en Linux y en el runner de CI— y
despues en los sitios fijos de macOS, donde Chrome se instala como paquete `.app` y
nunca queda en el PATH. Sin esta segunda parte, en un Mac `mapa.py` escribia los SVG
y se saltaba los PNG en silencio, e `imprimir.py` no sacaba ningun PDF.
"""
import os
import shutil

EN_PATH = ("google-chrome", "chromium", "chromium-browser", "chrome")

EN_MACOS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)


def chrome():
    """La ruta al binario de Chrome o Chromium, o None si no hay ninguno."""
    for nombre in EN_PATH:
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    for ruta in EN_MACOS:
        ruta = os.path.expanduser(ruta)
        if os.path.exists(ruta):
            return ruta
    return None
