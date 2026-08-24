#!/usr/bin/env python3
"""Reescribe los ficheros de `aparte/` que se importan en Google My Maps.

Son datos DERIVADOS de `trazado.ETAPAS` y de `geo/ruta.json`, igual que el mapa, la
lamina y el GPX — pero hasta el 24/08 se escribian a mano, y al mover una noche se
quedaban contando la ruta de antes sin que nada avisara. Aqui se generan:

  aparte/namibia-paradas-google-maps.csv        las paradas, con su dia y donde se duerme
  aparte/namibia-puntos-sin-dia-confirmado.csv  los puntos reales que NINGUN dia situa
  aparte/namibia-trazado-carreteras.kml         un tramo por dia, coloreado por bloque

    python3 fuente/mapas_google.py
"""
import csv
import json
import os

import trazado

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
APARTE = os.path.join(RAIZ, "aparte")

CATEGORIA = {
    "parada": "Donde se duerme",
    "hito":   "Lo que se visita",
    "puerta": "Puerta de parque",
    "paso":   "Puerto de montaña",
    "ciudad": "Núcleo de referencia",
    "combu":  "Gasolinera obligatoria",
}

# Puntos que la ruta visita de verdad pero que NO son ancla de enrutado: OSRM pasa por
# ellos sin necesitar un punto de paso, asi que no aparecen en ningun `por`. Se situan a
# mano contra el `01`, y va aqui —y no en el CSV— para que quede dicho de donde sale.
A_MANO = {"deadvlei":  ("D3", "duna45"),      # clave -> (dia, punto tras el que va)
          "torrabay":  ("D6", "ugabmund")}   # la C34 pasa por el; cerrado y sin parada


def _dias():
    """Para cada punto: en que dias se pasa por el y en cuales se duerme alli."""
    pasa, duerme, orden = {}, {}, []
    for etapa in trazado.ETAPAS:
        for p in etapa["por"]:
            if p not in pasa:
                pasa[p], _ = [], orden.append(p)
            if etapa["id"] not in pasa[p]:
                pasa[p].append(etapa["id"])
        d = etapa.get("duerme")
        if d:
            duerme.setdefault(d, []).append(etapa["id"])
            if d not in pasa:
                pasa[d], _ = [], orden.append(d)
    for clave, (dia, tras) in A_MANO.items():
        pasa[clave] = [dia]
        orden.insert(orden.index(tras) + 1, clave)
    return pasa, duerme, orden


def paradas():
    pasa, duerme, orden = _dias()
    oficiales = trazado.puntos_oficiales()
    con, sin = [], []
    for clave, (lat, lon, rotulo, clase) in oficiales.items():
        fila = [rotulo, CATEGORIA[clase], lat, lon]
        if clave in pasa:
            con.append((orden.index(clave), fila + [", ".join(pasa[clave]),
                                                    ", ".join(duerme.get(clave, []))]))
        else:
            sin.append(fila)

    ruta = os.path.join(APARTE, "namibia-paradas-google-maps.csv")
    with open(ruta, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Nombre", "Categoría", "Latitud", "Longitud",
                    "Días de la ruta", "Noche aquí"])
        for _, fila in sorted(con):
            w.writerow(fila)
    print(f"   -> aparte/namibia-paradas-google-maps.csv ({len(con)} paradas)")

    ruta = os.path.join(APARTE, "namibia-puntos-sin-dia-confirmado.csv")
    with open(ruta, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Nombre", "Categoría", "Latitud", "Longitud"])
        w.writerows(sin)
    print(f"   -> aparte/namibia-puntos-sin-dia-confirmado.csv ({len(sin)} puntos)")
    return len(con), len(sin)


def _abgr(hexrgb):
    """KML pide el color al reves y con alfa delante: #RRGGBB -> ffBBGGRR."""
    r, g, b = hexrgb[1:3], hexrgb[3:5], hexrgb[5:7]
    return f"ff{b}{g}{r}".lower()


def trazado_kml():
    ruta_json = os.path.join(HERE, "geo", "ruta.json")
    etapas = json.load(open(ruta_json))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<kml xmlns="http://www.opengis.net/kml/2.2">', "<Document>",
           "  <name>Namibia 2026 — trazado real por carretera</name>"]
    for bloque, color in trazado.COLOR_BLOQUE.items():
        out.append(f'  <Style id="bloque-{bloque}"><LineStyle>'
                   f"<color>{_abgr(color)}</color><width>5</width></LineStyle></Style>")
    tramos = 0
    for e in etapas:
        if not e.get("geometria"):
            continue
        coords = " ".join(f"{lon},{lat},0" for lon, lat in e["geometria"])
        out += ["  <Placemark>",
                f"    <name>{e['id']} · {e['titulo']}</name>",
                f"    <description>{e['fecha']} · {e['km']:.0f} km · "
                f"{e['horas']:.1f} h de conducción · duerme en "
                f"{e['duerme'] or '—'}</description>",
                f"    <styleUrl>#bloque-{e['bloque']}</styleUrl>",
                "    <LineString>", "      <tessellate>1</tessellate>",
                f"      <coordinates>{coords}</coordinates>",
                "    </LineString>", "  </Placemark>"]
        tramos += 1
    out += ["</Document>", "</kml>", ""]
    dest = os.path.join(APARTE, "namibia-trazado-carreteras.kml")
    open(dest, "w").write("\n".join(out))
    print(f"   -> aparte/namibia-trazado-carreteras.kml ({tramos} tramos, "
          f"{os.path.getsize(dest) // 1024} KB)")
    return tramos


def main():
    print("Google My Maps · paradas y trazado, desde trazado.ETAPAS y geo/ruta.json")
    paradas()
    trazado_kml()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
