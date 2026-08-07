#!/usr/bin/env python3
"""Descarga y cachea la geometria de los mapas. Se ejecuta una vez; el resultado se versiona.

Tres fuentes, todas libres:
  · Natural Earth 1:10M (dominio publico) -> contorno de Namibia y de los paises vecinos.
  · OSRM publico sobre OpenStreetMap      -> el trazado real de carretera de la ruta.
  · Overpass sobre OpenStreetMap (ODbL)   -> Etosha: la depresion, las pistas, las charcas,
                                             los campamentos y las puertas.

Todo se guarda en fuente/geo/*.json. `mapa.py` solo lee de ahi, asi que el build del PDF
no necesita red. Uso:

    python3 fuente/geodatos.py           # solo lo que falte
    python3 fuente/geodatos.py --forzar  # todo otra vez
"""
import json
import os
import sys
import time
import urllib.parse

import red

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "geo")

NE = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
      "ne_10m_admin_0_countries.geojson")
PAISES = {"Namibia", "Angola", "Botswana", "South Africa", "Zambia", "Zimbabwe"}

OVERPASS = ["https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter"]

# Caja de Etosha, generosa: el parque va de ~14,2 a ~17,4 E y de ~18,3 a ~19,6 S.
CAJA_ETOSHA = "(-19.65,14.15,-18.30,17.45)"


def pide(url, datos=None, timeout=180, intentos=4):
    """Descargas grandes y servidores comunitarios: timeout largo, pocos intentos."""
    return red.pide(url, datos=datos, timeout=timeout, intentos=intentos)


def overpass(consulta, timeout=180):
    """Lanza una consulta a Overpass, probando servidores hasta que uno responda."""
    datos = urllib.parse.urlencode({"data": consulta}).encode()
    ultimo = None
    for srv in OVERPASS:
        try:
            return json.loads(pide(srv, datos, timeout=timeout, intentos=2))
        except Exception as e:                                    # noqa: BLE001
            ultimo = e
            print(f"   {srv.split('/')[2]}: {e}")
    raise RuntimeError(f"Overpass no responde: {ultimo}")


def guarda(nombre, obj):
    os.makedirs(GEO, exist_ok=True)
    ruta = os.path.join(GEO, nombre)
    with open(ruta, "w") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(f"   -> geo/{nombre} ({os.path.getsize(ruta) // 1024} KB)")


def hecho(nombre):
    return os.path.exists(os.path.join(GEO, nombre))


def anillos(rel, rol="outer"):
    """Une los miembros de una relacion de Overpass en anillos cerrados de (lat, lon).

    Quien escribe el formato sabe leerlo: esta funcion vive aqui porque tanto los
    mapas (`mapa.py`) como el poligono de GBIF (`avistamientos.py`) parten de las
    mismas relaciones que descarga este modulo. Los extremos se comparan con
    tolerancia y no con igualdad exacta: las coordenadas guardadas van redondeadas
    y dos tramos contiguos pueden no casar al bit.
    """
    trozos = [[(p["lat"], p["lon"]) for p in m["geometry"]]
              for m in rel.get("members", [])
              if m.get("role") == rol and m.get("geometry")]
    anillos, pendientes = [], list(trozos)
    while pendientes:
        actual = pendientes.pop(0)
        cambio = True
        while cambio and actual[0] != actual[-1]:
            cambio = False
            for i, t in enumerate(pendientes):
                if abs(t[0][0] - actual[-1][0]) < 1e-6 and abs(t[0][1] - actual[-1][1]) < 1e-6:
                    actual += t[1:]
                    pendientes.pop(i)
                    cambio = True
                    break
                if abs(t[-1][0] - actual[-1][0]) < 1e-6 and abs(t[-1][1] - actual[-1][1]) < 1e-6:
                    actual += t[::-1][1:]
                    pendientes.pop(i)
                    cambio = True
                    break
        anillos.append(actual)
    return anillos


# ---------------------------------------------------------------------------
# 1 · Contornos de los paises (Natural Earth)
# ---------------------------------------------------------------------------

def redondea(geom, dec=3):
    """Recorta la precision de las coordenadas: 3 decimales son ~100 m, de sobra
    para un mapa de pais, y deja el fichero en una decima parte."""
    if isinstance(geom, list):
        if geom and isinstance(geom[0], (int, float)):
            return [round(c, dec) for c in geom]
        return [redondea(g, dec) for g in geom]
    return geom


def paises():
    print("Natural Earth · contornos de paises")
    d = json.loads(pide(NE, timeout=180))
    feats = []
    for f in d["features"]:
        nom = f["properties"].get("NAME")
        if nom not in PAISES:
            continue
        feats.append({"type": "Feature",
                      "properties": {"nombre": nom},
                      "geometry": {"type": f["geometry"]["type"],
                                   "coordinates": redondea(f["geometry"]["coordinates"])}})
    guarda("paises.json", {"type": "FeatureCollection", "features": feats})


# ---------------------------------------------------------------------------
# 2 · Etosha (Overpass)
# ---------------------------------------------------------------------------

def etosha_pan():
    print("Overpass · la depresion de Etosha y el limite del parque")
    q = f"""[out:json][timeout:180];
(
  relation["natural"="water"]["name"~"Etosha",i]{CAJA_ETOSHA};
  way["natural"="water"]["name"~"Etosha Pan",i]{CAJA_ETOSHA};
  relation["boundary"="protected_area"]["name"~"Etosha",i]{CAJA_ETOSHA};
);
out geom;"""
    guarda("etosha_pan.json", overpass(q))


def parques():
    print("Overpass · limites de los parques de la ruta")
    q = """[out:json][timeout:240];
(
  relation["boundary"="protected_area"]["name"~"^(Etosha|Namib-Naukluft|Skeleton Coast|Dorob)",i](-29.5,11.0,-16.5,26.0);
  relation["boundary"="national_park"]["name"~"^(Etosha|Namib-Naukluft|Skeleton Coast|Dorob)",i](-29.5,11.0,-16.5,26.0);
);
out geom;"""
    d = overpass(q, timeout=300)
    # Solo hace falta el contorno: se tiran los miembros interiores y se recorta precision.
    for e in d.get("elements", []):
        for m in e.get("members", []):
            if "geometry" in m:
                m["geometry"] = [{"lat": round(p["lat"], 3), "lon": round(p["lon"], 3)}
                                 for p in m["geometry"]]
    guarda("parques.json", d)


def etosha_pistas():
    print("Overpass · pistas de Etosha")
    q = f"""[out:json][timeout:180];
way["highway"~"^(trunk|primary|secondary|tertiary|unclassified|residential)$"]{CAJA_ETOSHA};
out geom;"""
    guarda("etosha_pistas.json", overpass(q))


def etosha_puntos():
    print("Overpass · charcas, campamentos y puertas de Etosha")
    q = f"""[out:json][timeout:180];
(
  node["tourism"]["name"]{CAJA_ETOSHA};
  way["tourism"]["name"]{CAJA_ETOSHA};
  node["barrier"="gate"]["name"]{CAJA_ETOSHA};
  node["place"]["name"]{CAJA_ETOSHA};
);
out center tags;"""
    guarda("etosha_puntos.json", overpass(q))


# ---------------------------------------------------------------------------
# 3 · El trazado de la ruta (OSRM sobre OSM)
# ---------------------------------------------------------------------------

def osrm(puntos, perfil="driving"):
    coords = ";".join(f"{lon},{lat}" for lat, lon in puntos)
    url = (f"https://router.project-osrm.org/route/v1/{perfil}/{coords}"
           "?overview=full&geometries=geojson&steps=false&annotations=false")
    return json.loads(pide(url, timeout=120))


def ruta():
    """Un tramo por dia, para poder pintar cada etapa de su color y medirla aparte."""
    import trazado
    print("OSRM · trazado de carretera de la ruta, tramo a tramo")
    salida = []
    for etapa in trazado.ETAPAS:
        puntos = [trazado.PUNTOS[p][:2] for p in etapa["por"]]
        if len(puntos) < 2:                       # dia de descanso: no hay traslado
            salida.append(dict(etapa, geometria=None, km=0.0, horas=0.0))
            print(f"   {etapa['id']:4s}     —      sin traslado")
            continue
        d = osrm(puntos)
        if d.get("code") != "Ok":
            print(f"   !! {etapa['id']}: OSRM dice {d.get('code')}")
            salida.append(dict(etapa, geometria=None, km=None, horas=None))
            continue
        r = d["routes"][0]
        salida.append(dict(etapa,
                           geometria=redondea(r["geometry"]["coordinates"], 4),
                           km=round(r["distance"] / 1000, 1),
                           horas=round(r["duration"] / 3600, 2)))
        print(f"   {etapa['id']:4s} {r['distance'] / 1000:7.1f} km  "
              f"{r['duration'] / 3600:5.2f} h  ({' → '.join(etapa['por'])})")
        time.sleep(1.2)
    guarda("ruta.json", salida)
    total = sum(e["km"] for e in salida if e["km"])
    print(f"   TOTAL OSRM: {total:.0f} km")


PASOS = [("paises.json", paises),
         ("parques.json", parques),
         ("etosha_pan.json", etosha_pan),
         ("etosha_pistas.json", etosha_pistas),
         ("etosha_puntos.json", etosha_puntos),
         ("ruta.json", ruta)]


def main():
    forzar = "--forzar" in sys.argv
    solo = [a for a in sys.argv[1:] if not a.startswith("--")]
    for nombre, fn in PASOS:
        if solo and nombre.split(".")[0] not in solo:
            continue
        if hecho(nombre) and not forzar:
            print(f"ya esta: geo/{nombre}")
            continue
        fn()
    return 0


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    raise SystemExit(main())
