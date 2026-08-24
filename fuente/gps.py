#!/usr/bin/env python3
"""El GPS del viaje: la ruta entera en GPX y en KML, para llevarla en el trasto.

Sale de la MISMA geometria que el mapa del dossier y que la lamina —`geo/ruta.json`,
enrutado con OSRM sobre OpenStreetMap— y de la misma tabla de puntos
(`trazado.puntos_oficiales()`: `PUNTOS` menos los que solo existen en la variante
del `24`, que no se van a conducir).
Es decir: si se cambia una noche, el GPX cambia solo. Nada escrito a mano.

Se generan dos ficheros porque no los come el mismo sitio:

  · **GPX** — el formato de los GPS de verdad (Garmin) y de casi toda app de navegacion
    offline (OsmAnd, Locus, Organic Maps, Gaia). Lleva los 40 puntos como *waypoints*,
    con simbolo segun lo que sean, y las 15 etapas como *tracks* separados, para poder
    encender y apagar los dias uno a uno.
  · **KML** — el que importa Google My Maps y Google Earth, con las etapas ya coloreadas
    por bloque de viaje (desierto, costa, Damaraland, Etosha), como en el mapa del PDF.

⚠️ **Tracks4Africa NO importa ninguno de los dos, y conviene saberlo antes de intentarlo**:
su planificador online exporta GPX y KML pero *importar* sigue siendo una funcion
pendiente —«the function to import points from a KML or GPX file will be added over time
as well», su propio blog— y la app Overland tampoco admite GPX: alli las rutas se montan
dentro. Estos ficheros valen para todo lo demas.
"""
import json
import os
import sys
import xml.sax.saxutils as x

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import trazado                                                     # noqa: E402

GPX = os.path.join(RAIZ, "ruta-namibia-2026.gpx")
KML = os.path.join(RAIZ, "ruta-namibia-2026.kml")

# Que dibuja el GPS en cada punto. Los nombres son los del catalogo de simbolos de
# Garmin: si el trasto no conoce uno, cae a un icono generico y no rompe nada.
SIMBOLO = {
    "parada":  ("Campground",      "donde se duerme"),
    "combu":   ("Gas Station",     "gasolinera de las obligatorias"),
    "puerta":  ("Flag, Red",       "puerta de parque, con horario"),
    "paso":    ("Summit",          "puerto de montana"),
    "ciudad":  ("City (Medium)",   "nucleo de referencia"),
    "hito":    ("Flag, Blue",      "lo que se visita"),
}


def etapas():
    ruta = os.path.join(HERE, "geo", "ruta.json")
    if not os.path.exists(ruta):
        raise SystemExit("falta geo/ruta.json — ejecuta `python3 fuente/geodatos.py`")
    return json.load(open(ruta))


def donde_sale(clave, tramos):
    """Los dias en que se pisa un punto, para que el waypoint diga a que etapa es."""
    dias = [e["id"] for e in tramos if clave in e.get("por", []) or e.get("duerme") == clave]
    return ", ".join(dias)


def escribe_gpx(tramos):
    p = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gpx version="1.1" creator="Namibia 2026 · fuente/gps.py"',
         '     xmlns="http://www.topografix.com/GPX/1/1">',
         '  <metadata>',
         '    <name>Namibia 2026 · la clasica del norte</name>',
         '    <desc>15 etapas, 14 noches, ~{:.0f} km. Trazado con OSRM sobre OpenStreetMap.</desc>'
         .format(sum(e["km"] or 0 for e in tramos)),
         '  </metadata>']

    for clave, (lat, lon, rotulo, clase) in trazado.puntos_oficiales().items():
        simbolo, que_es = SIMBOLO.get(clase, ("Flag, Blue", clase))
        dias = donde_sale(clave, tramos)
        desc = f"{que_es}{' · ' + dias if dias else ''}"
        p += [f'  <wpt lat="{lat}" lon="{lon}">',
              f'    <name>{x.escape(rotulo)}</name>',
              f'    <desc>{x.escape(desc)}</desc>',
              f'    <sym>{x.escape(simbolo)}</sym>',
              f'    <type>{x.escape(clase)}</type>',
              '  </wpt>']

    for e in tramos:
        if not e.get("geometria"):
            continue                       # el D2 y el D4 no mueven el coche de sitio
        horas = e.get("horas")
        desc = f'{e["fecha"]} · {e["km"]:.0f} km' + (f' · ~{horas:.1f} h' if horas else "")
        p += ['  <trk>',
              f'    <name>{x.escape(e["id"] + " · " + e["titulo"])}</name>',
              f'    <desc>{x.escape(desc)}</desc>',
              '    <trkseg>']
        p += [f'      <trkpt lat="{lat}" lon="{lon}"/>' for lon, lat in e["geometria"]]
        p += ['    </trkseg>', '  </trk>']

    p.append('</gpx>')
    open(GPX, "w").write("\n".join(p) + "\n")
    return len(trazado.puntos_oficiales()), sum(1 for e in tramos if e.get("geometria"))


def _kml_color(hexa):
    """#RRGGBB -> aabbggrr, que es como KML pide el color (y al reves)."""
    r, g, b = hexa[1:3], hexa[3:5], hexa[5:7]
    return f"ff{b}{g}{r}".lower()


def escribe_kml(tramos):
    p = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
         '  <name>Namibia 2026 · la clasica del norte</name>']

    for bloque, color in trazado.COLOR_BLOQUE.items():
        p += [f'  <Style id="{bloque}"><LineStyle>',
              f'    <color>{_kml_color(color)}</color><width>4</width>',
              '  </LineStyle></Style>']

    p.append('  <Folder><name>Etapas</name>')
    for e in tramos:
        if not e.get("geometria"):
            continue
        coords = " ".join(f"{lon},{lat},0" for lon, lat in e["geometria"])
        p += ['    <Placemark>',
              f'      <name>{x.escape(e["id"] + " · " + e["titulo"])}</name>',
              f'      <description>{x.escape(e["fecha"])} · {e["km"]:.0f} km</description>',
              f'      <styleUrl>#{e["bloque"]}</styleUrl>',
              f'      <LineString><tessellate>1</tessellate><coordinates>{coords}</coordinates>'
              '</LineString>',
              '    </Placemark>']
    p.append('  </Folder>')

    p.append('  <Folder><name>Puntos</name>')
    for clave, (lat, lon, rotulo, clase) in trazado.puntos_oficiales().items():
        dias = donde_sale(clave, tramos)
        desc = SIMBOLO.get(clase, ("", clase))[1] + (f" · {dias}" if dias else "")
        p += ['    <Placemark>',
              f'      <name>{x.escape(rotulo)}</name>',
              f'      <description>{x.escape(desc)}</description>',
              f'      <Point><coordinates>{lon},{lat},0</coordinates></Point>',
              '    </Placemark>']
    p.append('  </Folder>')

    p.append('</Document></kml>')
    open(KML, "w").write("\n".join(p) + "\n")


def main():
    tramos = etapas()
    puntos, pistas = escribe_gpx(tramos)
    escribe_kml(tramos)
    for f in (GPX, KML):
        print(f"{os.path.basename(f)} · {os.path.getsize(f) / 1024:.0f} KB")
    print(f"  {puntos} puntos · {pistas} etapas con trazado · "
          f"{sum(e['km'] or 0 for e in tramos):.0f} km")


if __name__ == "__main__":
    main()
