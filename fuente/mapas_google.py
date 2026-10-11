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
import os

import gps
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
    """Para cada punto: en que dias se pisa, en cuales se duerme alli, y el orden de la ruta.

    Los dias salen de `trazado.dias_del_punto`, que es lo que usa el GPX: hasta el 09/10
    esto llevaba su propia copia y trataba `A_MANO` de otra manera (lo sobrescribia en vez
    de anadirlo). Daba lo mismo mientras Deadvlei y Torra Bay no estuvieran en ningun `por`,
    pero eran dos reglas para la misma pregunta. Aqui solo queda el ORDEN, que es de My Maps:
    cada punto, donde la ruta lo pisa por primera vez, y los de `A_MANO` tras su punto.
    """
    duerme, orden = {}, []
    for etapa in trazado.ETAPAS:
        for p in etapa["por"] + ([etapa["duerme"]] if etapa.get("duerme") else []):
            if p not in orden:
                orden.append(p)
        if etapa.get("duerme"):
            duerme.setdefault(etapa["duerme"], []).append(etapa["id"])
    for clave, (_dia, tras) in trazado.A_MANO.items():
        orden.insert(orden.index(tras) + 1, clave)
    pasa = {p: trazado.dias_del_punto(p) for p in orden}
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
    """El trazado para My Maps: el mismo KML del GPS sin la carpeta de puntos, que aqui van en
    los CSV. Hasta el 11/10 era un segundo generador de la misma ruta, con otros estilos."""
    return gps.texto_kml(gps.etapas(), nombre="Namibia 2026 — trazado real por carretera",
                         con_puntos=False)


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
