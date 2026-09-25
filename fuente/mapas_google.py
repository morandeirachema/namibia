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
import io
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
    for clave, (dia, tras) in trazado.A_MANO.items():
        pasa[clave] = [dia]
        orden.insert(orden.index(tras) + 1, clave)
    return pasa, duerme, orden


def _csv(filas):
    f = io.StringIO()
    csv.writer(f).writerows(filas)
    return f.getvalue()


def paradas():
    """Los dos CSV: las paradas con su dia, y los puntos que ningun dia situa."""
    pasa, duerme, orden = _dias()
    con, sin = [], []
    for clave, (lat, lon, rotulo, clase) in trazado.puntos_oficiales().items():
        fila = [rotulo, CATEGORIA[clase], lat, lon]
        if clave in pasa:
            con.append((orden.index(clave), fila + [", ".join(pasa[clave]),
                                                    ", ".join(duerme.get(clave, []))]))
        else:
            sin.append(fila)
    cabeza = ["Nombre", "Categoría", "Latitud", "Longitud"]
    return (_csv([cabeza + ["Días de la ruta", "Noche aquí"]] + [f for _, f in sorted(con)]),
            _csv([cabeza] + sin))


def trazado_kml():
    etapas = json.load(open(os.path.join(HERE, "geo", "ruta.json")))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<kml xmlns="http://www.opengis.net/kml/2.2">', "<Document>",
           "  <name>Namibia 2026 — trazado real por carretera</name>"]
    for bloque, color in trazado.COLOR_BLOQUE.items():
        out.append(f'  <Style id="bloque-{bloque}"><LineStyle>'
                   f"<color>{trazado.color_kml(color)}</color><width>5</width></LineStyle></Style>")
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
    out += ["</Document>", "</kml>", ""]
    return "\n".join(out)


PARADAS = os.path.join(APARTE, "namibia-paradas-google-maps.csv")
SIN_DIA = os.path.join(APARTE, "namibia-puntos-sin-dia-confirmado.csv")
KML = os.path.join(APARTE, "namibia-trazado-carreteras.kml")


def textos():
    """Fichero -> contenido. `comprobar.revisa_derivados` los compara con lo que hay en disco."""
    con, sin = paradas()
    return {PARADAS: con, SIN_DIA: sin, KML: trazado_kml()}


def main():
    print("Google My Maps · paradas y trazado, desde trazado.ETAPAS y geo/ruta.json")
    for ruta, texto in textos().items():
        with open(ruta, "w", newline="") as f:
            f.write(texto)
        print(f"   -> {os.path.relpath(ruta, RAIZ)} ({len(texto.splitlines()) - 1} filas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
