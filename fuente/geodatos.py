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
    _traza(trazado.ETAPAS, "ruta.json", "la ruta")


def ruta_alt():
    """Lo mismo para la variante del `aparte/decision-del-ccf`, que tiene sus propias quince etapas.

    Va a un fichero aparte y no toca `ruta.json`: la ruta que imprime el volumen sigue
    siendo la de `01`, y el `aparte/decision-del-ccf` solo necesita su mapa y sus kilometros.
    """
    import trazado
    _traza(trazado.ETAPAS_ALT, "ruta-alt.json", "la variante del `aparte/decision-del-ccf`")


def _traza(etapas, fichero, que):
    import trazado
    print(f"OSRM · trazado de carretera de {que}, tramo a tramo")
    salida = []
    for etapa in etapas:
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
    guarda(fichero, salida)
    total = sum(e["km"] for e in salida if e["km"])
    print(f"   TOTAL OSRM: {total:.0f} km")


def tramos():
    """Los tramos con nombre de carretera de cada etapa, para el firme y los mapas por dia.

    OSRM publico no expone el `surface` de OSM, pero si el `ref` de cada paso (B1, C24,
    D1261…), y en Namibia con la letra basta —ver `trazado.FIRME`—. Se pide con
    `steps=true`, que devuelve la geometria de cada paso por separado: eso permite pintar
    cada tramo del color de su firme en vez de un porcentaje del dia.
    """
    import trazado
    print("OSRM · tramos con nombre de carretera, para el firme")
    salida = []
    for etapa in trazado.ETAPAS:
        puntos = [trazado.PUNTOS[p][:2] for p in etapa["por"]]
        if len(puntos) < 2:
            salida.append(dict(id=etapa["id"], tramos=[]))
            continue
        coords = ";".join(f"{lon},{lat}" for lat, lon in puntos)
        url = (f"https://router.project-osrm.org/route/v1/driving/{coords}"
               "?overview=false&steps=true&geometries=geojson&annotations=false")
        d = json.loads(pide(url, timeout=120))
        tr = []
        for leg in d["routes"][0]["legs"]:
            for st in leg["steps"]:
                if st["distance"] < 30:
                    continue
                g = st["geometry"]["coordinates"]
                lat, lon = g[len(g) // 2][1], g[len(g) // 2][0]
                tr.append({"ref": st.get("ref") or "", "nombre": st.get("name") or "",
                           "km": round(st["distance"] / 1000, 2),
                           "firme": trazado.firme_de(st.get("ref"), lat, lon, st.get("name")),
                           "geometria": redondea(g, 4)})
        sin = sorted({t["ref"] or t["nombre"] or "(sin nombre)" for t in tr if t["firme"] is None})
        km_sin = sum(t["km"] for t in tr if t["firme"] is None)
        salida.append(dict(id=etapa["id"], tramos=tr))
        print(f"   {etapa['id']:4s} {len(tr):3d} tramos" +
              (f"  · SIN FIRME {km_sin:.0f} km: {sin}" if km_sin > 2 else ""))
        time.sleep(1.2)
    guarda("tramos.json", salida)


# Los puntos de interes de la agenda: donde comer y las joyas del `10`, con el dia en que
# se pasa por ellos. Son los que el dossier ya nombra; aqui solo se les pone coordenada,
# con Nominatim y NUNCA a ojo. Si Nominatim no lo encuentra, no entra al mapa — y se
# dice en la salida, para que conste que falta.
#   (consulta a Nominatim, rotulo del mapa, clase, dias)
#   clase: comer · joya · compra
INTERES = [
    ("Joe's Beerhouse, Windhoek", "Joe's Beerhouse", "comer", ["D1", "D14"]),
    ("Namibia Craft Centre, Windhoek", "Craft Centre", "compra", ["D15"]),
    ("Maerua Mall, Windhoek", "Maerua Mall · SuperSpar", "compra", ["D1"]),
    ("Solitaire Bakery", "Tarta de McGregor", "comer", ["D3", "D5"]),
    ("The Raft, Walvis Bay", "The Raft · ostras", "comer", ["D5", "D6"]),
    ("Anchors at the Jetty, Walvis Bay", "Anchors @ the Jetty", "comer", ["D5", "D6"]),
    ("Café Anton, Swakopmund", "Café Anton", "comer", ["D6", "D7"]),
    ("The Tug, Swakopmund", "The Tug", "comer", ["D6", "D7"]),
    ("Jetty 1905, Swakopmund", "Jetty 1905", "comer", ["D6", "D7"]),
    ("Kücki's Pub, Swakopmund", "Kücki's Pub", "comer", ["D6", "D7"]),
    ("Brewer & Butcher, Swakopmund", "Brewer & Butcher", "comer", ["D6", "D7"]),
    ("Dune 7, Walvis Bay", "Dune 7", "joya", ["D5"]),
    ("Pelican Point, Walvis Bay", "Pelican Point", "joya", ["D6"]),
    ("Welwitschia Drive, Swakopmund", "Welwitschia Drive", "joya", ["D6"]),
    ("Moon Landscape, Swakopmund", "Moon Landscape", "joya", ["D6"]),
    ("Wlotzkasbaken", "Wlotzkasbaken", "joya", ["D7"]),
    ("Zeila Shipwreck", "Pecio Zeila", "joya", ["D7"]),
    ("Kuiseb Pass", "Paso del Kuiseb · Henno Martin", "joya", ["D5"]),
    ("Organ Pipes, Kunene", "Organ Pipes", "joya", ["D8"]),
    ("Burnt Mountain, Kunene", "Burnt Mountain", "joya", ["D8"]),
    ("Petrified Forest, Khorixas", "Petrified Forest", "joya", ["D8", "D9"]),
    ("Lake Otjikoto", "Lago Otjikoto", "joya", ["D14"]),
    ("Sesriem Canyon", "Sesriem Canyon", "joya", ["D3"]),
    ("Elim Dune, Sesriem", "Elim Dune", "joya", ["D3"]),
    ("Grootberg Lodge", "Grootberg Lodge · rastreos", "joya", ["D9"]),
    ("Hoba Meteorite", "Meteorito de Hoba", "joya", ["D14"]),
]


def interes():
    """Geocodifica INTERES con Nominatim y lo guarda en geo/interes.json."""
    print("Nominatim · puntos de interes de la agenda")
    salida, faltan = [], []
    for consulta, rotulo, clase, dias in INTERES:
        url = ("https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
            {"q": consulta, "format": "json", "limit": 1, "countrycodes": "na"}))
        try:
            r = json.loads(pide(url, timeout=40, intentos=2))
        except Exception as e:                                    # noqa: BLE001
            r = []
            print(f"   !! {consulta}: {e}")
        if not r:
            faltan.append(consulta)
            print(f"   —  {rotulo:32s} sin resultado")
        else:
            salida.append({"consulta": consulta, "rotulo": rotulo, "clase": clase, "dias": dias,
                           "lat": round(float(r[0]["lat"]), 5), "lon": round(float(r[0]["lon"]), 5),
                           "osm": r[0].get("display_name", "")[:90]})
            print(f"   ok {rotulo:32s} {r[0]['display_name'][:60]}")
        time.sleep(1.1)                                            # la politica de Nominatim
    guarda("interes.json", {"puntos": salida, "sin_resultado": faltan})
    if faltan:
        print(f"   {len(faltan)} sin coordenada — quedan FUERA del mapa, no se inventan")


PASOS = [("paises.json", paises),
         ("parques.json", parques),
         ("etosha_pan.json", etosha_pan),
         ("etosha_pistas.json", etosha_pistas),
         ("etosha_puntos.json", etosha_puntos),
         ("ruta.json", ruta),
         ("ruta-alt.json", ruta_alt),
         ("tramos.json", tramos),
         ("interes.json", interes)]


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
