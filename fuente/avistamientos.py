#!/usr/bin/env python3
"""Que posibilidades hay de ver cada bicho, medidas y no inventadas.

Dos fuentes independientes, las dos publicas y las dos con su denominador:

**1 · Expert Africa** publica el porcentaje de sus viajeros que vio cada especie
grande en cada campamento, con el numero de partes de avistamiento detras. Es la
respuesta directa a la pregunta —«el 87 % de los que durmieron en Okaukuejo vio
rinoceronte negro»— y cubre las catorce especies que la gente va buscando. Se baja
de los tres campamentos del viaje: Okaukuejo, Halali y Namutoni.

**2 · GBIF**, el agregador mundial de registros de biodiversidad (museos,
anillamientos, eBird, iNaturalist, atlas de aves), cubre las 148. De ahi sale algo
honesto y reproducible: de cada 100 registros de mamifero dentro de Etosha en octubre
y noviembre, cuantos son de esta especie.

Lo de GBIF NO es una probabilidad de avistamiento y aqui no se le llama asi. Es un
indice de frecuencia relativa, y arrastra los sesgos del observador: en Etosha las aves
llevan ~276.000 registros y los mamiferos ~17.000 (esta consulta), un leon llama mas la
atencion que un steenbok, y nadie sube a GBIF el chacal numero doscientos. Por eso se compara
**dentro de la misma clase y dentro de la misma zona**, nunca un ave contra un
mamifero, y por eso la cifra va siempre con el numero de registros detras: con 12
registros no se afirma nada.

Lo de Expert Africa tampoco es perfecto: lo rellenan los propios viajeros y hay
identificaciones malas —el 14 % que dice haber visto un antilope sable en Okaukuejo
lo delata: en Etosha no hay sable—. Pero la pregunta que responde es exactamente la
que se hace uno antes de ir, y viene con su muestra.

Cuatro zonas, las del viaje:

  · etosha     el poligono real del parque (OSM, via fuente/geo/parques.json)
  · costa      Cape Cross, Swakopmund, Walvis Bay y Sandwich Harbour (D5-D7)
  · namib      Sesriem, Sossusvlei y el Namib-Naukluft (D3-D4)
  · damaraland Twyfelfontein, Grootberg y Hoada (D8-D9)

Uso:
    python3 fuente/avistamientos.py           # solo lo que falte (especies nuevas)
    python3 fuente/avistamientos.py --forzar  # lo rehace todo desde GBIF

El resultado se versiona en fuente/geo/avistamientos.json y el build del PDF lo lee
de ahi: `guia_fauna.py` no toca la red.
"""
import json
import os
import re
import sys
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "geo")
sys.path.insert(0, HERE)

import catalogo                                                    # noqa: E402
import geodatos                                                    # noqa: E402
import red                                                         # noqa: E402
from comun import mil as _mil                                      # noqa: E402

API = "https://api.gbif.org/v1/"
SALIDA = "avistamientos.json"

# Los meses del viaje. La ventana es 30 oct - 14 nov: se piden los dos meses enteros
# porque GBIF no filtra por dia y recortar mas dejaria muestras de dos cifras.
MESES = "10,11"

# Cajas de las otras tres zonas: (oeste, sur, este, norte).
CAJAS = {
    "costa": (13.85, -23.45, 14.85, -21.60),
    "namib": (15.15, -25.15, 16.30, -24.10),
    "damaraland": (13.90, -21.05, 15.30, -19.60),
}
NOMBRES = {
    "etosha": "Etosha",
    "costa": "la costa",
    "namib": "el Namib",
    "damaraland": "Damaraland",
}

# Registros de la clase en la zona por debajo de los cuales no se afirma nada del
# reparto: con 30 registros de milpies en todo el parque, un porcentaje no significa.
MUESTRA_MINIMA = 120

# Y registros DE LA ESPECIE por debajo de los cuales tampoco: 7 registros de cebra de
# montana en Damaraland dan un 3 % que suena a «la vais a ver» y no lo es.
MINIMO_ESPECIE = 10

# Las dos fichas donde el indice diria una cosa y la fuente dice la contraria. La
# suricata no vive en esta ruta (es del Kalahari y del sur) y la cebra de Hartmann
# esta dentro del poligono de Etosha pero solo en las lomas del extremo oeste, a
# doscientos kilometros del eje Okaukuejo-Namutoni. GBIF no distingue eso; la ficha si.
# Vacio desde el 09/08: las especies que la fuente situaba fuera de la ruta (suricata,
# cebra de Hartmann) salieron del catalogo con la regla nueva — la guia no lleva
# animales que nadie va a ver. El mecanismo se queda por si vuelve a hacer falta.
FUERA_DE_RUTA = set()


def pide(path, **kw):
    """GET a GBIF que devuelve el JSON ya cargado.

    La manía de GBIF: suelta 503 esporadicos sin motivo, y a veces disfrazados de
    HTTP 200 con una LISTA JSON donde tocaba un objeto — por eso el `valida`.
    """
    url = API + path + "?" + urllib.parse.urlencode(kw)
    return json.loads(red.pide(url, timeout=120, intentos=5,
                               valida=lambda b: isinstance(json.loads(b), dict)))


# ---------------------------------------------------------------------------
# 1 · Las zonas, en WKT
# ---------------------------------------------------------------------------

def _simplifica(pts, tol):
    """Douglas-Peucker. GBIF rechaza los poligonos con miles de vertices."""
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    norma = (dx * dx + dy * dy) ** .5 or 1e-12
    peor, idx = 0, 0
    for i, (x, y) in enumerate(pts[1:-1], 1):
        d = abs(dy * x - dx * y + x1 * y0 - y1 * x0) / norma
        if d > peor:
            peor, idx = d, i
    if peor <= tol:
        return [pts[0], pts[-1]]
    return _simplifica(pts[:idx + 1], tol)[:-1] + _simplifica(pts[idx:], tol)


def _antihorario(anillo):
    """GBIF exige el poligono en sentido antihorario."""
    area = sum((anillo[i][0] - anillo[i - 1][0]) * (anillo[i][1] + anillo[i - 1][1])
               for i in range(len(anillo)))
    return anillo if area < 0 else anillo[::-1]


def poligono_etosha():
    with open(os.path.join(GEO, "parques.json")) as f:
        d = json.load(f)
    rel = next(e for e in d["elements"]
               if e.get("tags", {}).get("name", "").startswith("Etosha"))
    # geodatos.anillos devuelve (lat, lon); aqui todo trabaja en (x, y) = (lon, lat).
    anillo = [(lon, lat) for lat, lon in max(geodatos.anillos(rel), key=len)]
    if anillo[0] == anillo[-1]:                     # se simplifica el anillo ABIERTO:
        anillo = anillo[:-1]                        # con el primer punto igual al ultimo,
    tol = 0.005                                     # Douglas-Peucker se colapsa a dos puntos
    while len(anillo) > 250 and tol < 1:            # ~500 m de tolerancia, y subiendo
        anillo, tol = _simplifica(anillo, tol), tol * 1.6
    return _antihorario(anillo + [anillo[0]])


def wkt(zona):
    if zona == "etosha":
        pts = poligono_etosha()
    else:
        o, s, e, n = CAJAS[zona]
        pts = [(o, s), (e, s), (e, n), (o, n), (o, s)]
    return "POLYGON((" + ",".join(f"{x:.4f} {y:.4f}" for x, y in pts) + "))"


# ---------------------------------------------------------------------------
# 2 · Los taxones del catalogo, resueltos contra la taxonomia de GBIF
# ---------------------------------------------------------------------------

def taxones():
    """slug -> {clave, clase, rango}. Se cuenta a nivel de ESPECIE a proposito.

    Media docena de fichas son subespecies (la jirafa angolena, la cebra de Burchell,
    la impala de cara negra). Contar la subespecie daria casi cero: casi nadie
    determina hasta ahi. Y no hace falta: en Etosha toda impala es de cara negra y
    toda cebra de llanura es de Burchell, asi que la especie ya responde la pregunta.
    """
    out = {}
    for _, _, lista in catalogo.GRUPOS_FAUNA:
        for slug, es, _en, sci, _f in lista:
            m = pide("species/match", name=sci, strict="false")
            clave = m.get("speciesKey") or m.get("usageKey")
            if not clave or m.get("matchType") == "NONE":
                print(f"   !! sin taxon en GBIF: {es} ({sci})")
                continue
            out[slug] = {"clave": clave,
                         "sci": m.get("canonicalName") or sci,
                         "clase": m.get("class") or m.get("phylum") or "?",
                         "clase_clave": m.get("classKey"),
                         "rango": m.get("rank", "")}
            time.sleep(.15)
    return out


# ---------------------------------------------------------------------------
# 3 · Los recuentos
# ---------------------------------------------------------------------------

def facetas(geometria, clase_clave, meses=None):
    """Un solo tiro por clase y zona: GBIF devuelve el recuento de TODAS las especies."""
    kw = dict(geometry=geometria, taxonKey=clase_clave, facet="speciesKey",
              facetLimit=1500, limit=0)
    if meses:
        kw["month"] = meses
    d = pide("occurrence/search", **kw)
    cuentas = {int(c["name"]): c["count"] for c in d["facets"][0]["counts"]} if d["facets"] else {}
    return d["count"], cuentas


def sueltos(geometria, clave, meses=None):
    """Para los taxones que no son especie (el solifugo es un orden; el anofeles, un genero)."""
    kw = dict(geometry=geometria, taxonKey=clave, limit=0)
    if meses:
        kw["month"] = meses
    return pide("occurrence/search", **kw)["count"]


def recuenta(tx):
    zonas = {}
    for zona in ("etosha", "costa", "namib", "damaraland"):
        g = wkt(zona)
        print(f"GBIF · {NOMBRES[zona]}")
        claves = sorted({t["clase_clave"] for t in tx.values() if t["clase_clave"]})
        todo, ventana, total_clase, total_ventana = {}, {}, {}, {}
        for ck in claves:
            n, c = facetas(g, ck)
            nv, cv = facetas(g, ck, MESES)
            todo.update(c)
            ventana.update(cv)
            total_clase[ck], total_ventana[ck] = n, nv
            print(f"   clase {ck:>10}: {n:>7} registros · {nv:>6} en oct-nov")
        zonas[zona] = {"nombre": NOMBRES[zona], "wkt": g,
                       "por_clase": {str(k): {"registros": total_clase[k],
                                              "oct_nov": total_ventana[k]} for k in claves},
                       "_todo": todo, "_ventana": ventana}

    especies = {}
    for slug, t in tx.items():
        fila = {"sci": t["sci"], "clase": t["clase"], "clase_clave": t["clase_clave"],
                "rango": t["rango"], "zonas": {}}
        for zona, z in zonas.items():
            if t["rango"] in ("SPECIES", "SUBSPECIES", "VARIETY", "FORM"):
                n = z["_todo"].get(t["clave"], 0)
                nv = z["_ventana"].get(t["clave"], 0)
            else:                                   # orden o genero: no sale en las facetas
                n = sueltos(z["wkt"], t["clave"])
                nv = sueltos(z["wkt"], t["clave"], MESES)
            fila["zonas"][zona] = {"registros": n, "oct_nov": nv}
        especies[slug] = fila
        print(f"   {slug:<22} " + " ".join(
            f"{z}:{fila['zonas'][z]['oct_nov']}/{fila['zonas'][z]['registros']}"
            for z in ("etosha", "costa", "namib", "damaraland")))

    for z in zonas.values():
        z.pop("_todo"), z.pop("_ventana")
    return {"zonas": zonas, "especies": especies}


# ---------------------------------------------------------------------------
# 4 · Los partes de avistamiento de los viajeros (Expert Africa)
# ---------------------------------------------------------------------------

# Los tres campamentos de NWR con partes, en el orden del viaje: en los dos primeros se
# duerme; Namutoni se cruza de dia el D12 (su noche se cambio por Onguma el 24/08).
CAMPAMENTOS = [("okaukuejo", "Okaukuejo", "okaukuejo-camp"),
               ("halali", "Halali", "halali-camp"),
               ("namutoni", "Namutoni", "namutoni-camp")]

# Como se llama alli cada bicho de nuestro catalogo. Lo que no esta en el catalogo
# —pangolin, sable, roan— se guarda igualmente en "otros": el sable es la prueba de
# que estos partes los rellena gente y no un biologo, y esa prueba no se tira.
EA_ESPECIE = {
    "Lion": "leon", "Leopard": "leopardo", "Cheetah": "guepardo",
    "Elephant": "elefante", "Giraffe": "jirafa", "Zebra": "cebra-burchell",
    "Oryx": "orix", "Wildebeest": "nu", "Eland": "eland",
    "Black Rhino": "rino-negro", "White Rhino": "rino-blanco",
    "Spotted Hyena": "hiena-manchada", "Brown Hyena": "hiena-parda",
    "Aardvark": "oricteropo",
}

NAVEGADOR = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/126.0 Safari/537.36")


def viajeros():
    """Baja los porcentajes de avistamiento de los tres campamentos.

    Una peticion por campamento y a cachear: el fichero se versiona y el build no
    vuelve a tocar la web. Los datos van en el atributo data-tooltip de cada bloque.
    """
    import html as _html
    out = {}
    for clave, nombre, slug in CAMPAMENTOS:
        url = f"https://www.expertafrica.com/namibia/etosha-national-park/{slug}/reviews/1"
        try:
            pag = red.pide(url, timeout=90, cabeceras={
                "User-Agent": NAVEGADOR,
                "Accept-Language": "en-GB,en;q=0.9"}).decode("utf-8", "replace")
        except Exception as e:                                    # noqa: BLE001
            print(f"   !! {nombre}: {e} — se queda sin porcentajes")
            continue
        cab = re.search(r"Starting in ([A-Za-z]+-\d{4}), <strong>(\d+) of our travellers</strong>",
                        pag)
        especies, otros = {}, {}
        for t in re.findall(r'data-tooltip="(\{&quot;titleText.*?\})"', pag):
            d = json.loads(_html.unescape(t))
            pct = re.match(r"(\d+)%", d["subtitleText"])
            n = re.findall(r"\[b\](\d+)\[/b\]", d["descriptionText"])
            if not pct or len(n) < 2:
                continue
            en = d["titleText"].replace("sightings", "").strip()
            fila = {"pct": int(pct.group(1)), "partes": int(n[0]), "lo_vieron": int(n[1])}
            (especies if en in EA_ESPECIE else otros)[EA_ESPECIE.get(en, en)] = fila
        out[clave] = {"nombre": nombre, "url": url,
                      "desde": cab.group(1) if cab else None,
                      "viajeros": int(cab.group(2)) if cab else None,
                      "especies": especies, "otros": otros}
        print(f"   {nombre:<10} {out[clave]['viajeros']} viajeros desde "
              f"{out[clave]['desde']} · {len(especies)} especies del catalogo")
        time.sleep(2)
    return out


# ---------------------------------------------------------------------------
# 5 · Lo que lee el build
# ---------------------------------------------------------------------------

_cache = None


def datos():
    """Devuelve el JSON cacheado, o {} si nadie lo ha generado todavia."""
    global _cache
    if _cache is None:
        ruta = os.path.join(GEO, SALIDA)
        _cache = json.load(open(ruta)) if os.path.exists(ruta) else {}
    return _cache


# La banda dice lo que el dato dice de verdad —cuanto se REGISTRA la especie— y no lo
# que a uno le gustaria que dijera —si la va a ver—. Se corta por el porcentaje que
# supone dentro de los registros de SU clase y SU zona en octubre-noviembre.
BANDAS = [(3.0, "seguro", "Muy frecuente"),
          (1.0, "facil", "Frecuente"),
          (0.3, "probable", "Regular"),
          (0.08, "buscar", "Escasa"),
          (0.0, "raro", "Muy escasa")]


def indice(slug):
    """(clase_css, banda, detalle) segun GBIF, o None si no hay ni muestra que citar.

    Se elige la zona del viaje donde MAS REGISTROS tiene la especie —no donde saca el
    porcentaje mas alto, que era premiar a las zonas con cuatro registros—. Asi el
    facocero cuenta por Etosha y el lobo marino por Cape Cross, que es lo suyo.
    """
    d = datos()
    sp = d.get("especies", {}).get(slug)
    if not sp:
        return None
    if slug in FUERA_DE_RUTA:
        return ("fuera", "Fuera de la ruta", "no cae en el recorrido de este viaje")
    ck = str(sp["clase_clave"])
    minimo = d.get("muestra_minima", MUESTRA_MINIMA)
    valida = [(z, sp["zonas"][z]["oct_nov"], base)
              for z in ("etosha", "costa", "namib", "damaraland")
              for base in [d["zonas"][z]["por_clase"].get(ck, {}).get("oct_nov", 0)]
              if base >= minimo]
    if not valida:
        return None                             # su grupo casi no se registra: nada que decir
    zona, n, base = max(valida, key=lambda v: v[1])
    donde = d["zonas"][zona]["nombre"]
    if n == 0:
        return ("cero", "Sin registros",
                f"ninguno de los {_mil(base)} registros de su grupo en {donde} "
                f"en oct-nov es suyo")
    if n < MINIMO_ESPECIE:
        return ("pocos", "Apenas registrada",
                f"{n} registro{'s' if n > 1 else ''} en {donde} en oct-nov: "
                f"muestra corta para decir más")
    pct = 100 * n / base
    clase_css, banda = next((c, t) for lim, c, t in BANDAS if pct >= lim)
    cifra = (f"{pct:.1f} %" if pct >= 0.1 else f"{pct:.2f} %").replace(".", ",")
    return (clase_css, banda,
            f"{cifra} de los registros de su grupo en {donde} en oct-nov "
            f"({n} de {_mil(base)})")


# Las mismas bandas, pero para un porcentaje que SI es una probabilidad de avistamiento.
BANDAS_VIAJEROS = [(90, "seguro"), (60, "facil"), (30, "probable"),
                   (10, "buscar"), (0, "raro")]


def porcentajes(slug):
    """(clase_css, '82 %', 'Okaukuejo 87 % · Halali 73 % · Namutoni 55 %', partes).

    El porcentaje que se destaca es el de los TRES campamentos juntos, no el del
    campamento donde mas se ve. Coger el maximo suena mejor y enganaba: el maximo
    salia casi siempre de Namutoni, que es la muestra pequena —16 viajeros—, y asi el
    eland pasaba de un 45 % real a un 73 % de casualidad. Aqui se pasa por los tres —se
    duerme en dos—, de modo que lo que corresponde es sumar partes y avistamientos.

    Detras van igualmente los tres por separado, porque ahi esta lo util: que el
    leopardo es de Halali y el rinoceronte negro, de Okaukuejo.
    """
    camps = datos().get("campamentos") or {}
    filas = [(c["nombre"], c["especies"][slug]) for c in camps.values()
             if slug in c.get("especies", {})]
    if not filas:
        return None
    partes = sum(f["partes"] for _, f in filas)
    vieron = sum(f["lo_vieron"] for _, f in filas)
    if not partes:
        return None
    pct = round(100 * vieron / partes)
    clase_css = next(c for lim, c in BANDAS_VIAJEROS if pct >= lim)
    detalle = " · ".join(f"{n} {f['pct']} %" for n, f in filas)
    return clase_css, f"{pct} %", detalle, partes


def fuente_html():
    """Las dos fuentes de la linea de posibilidades, para los creditos del PDF."""
    d = datos()
    if not d:
        return ""
    camps = (d.get("campamentos") or {}).values()
    detalle = " · ".join(f"{c['nombre']} ({c['viajeros']} viajeros desde {c['desde']})"
                         for c in camps if c.get("viajeros"))
    zonas = d.get("zonas", {})
    return (
        "<li><b>Porcentaje de viajeros que vio cada especie:</b> partes de avistamiento "
        f"publicados por <i>Expert Africa</i> para los tres campamentos — {detalle}. "
        "<span class='u'>expertafrica.com/namibia/etosha-national-park</span>. La unidad "
        "es <b>una estancia en ese campamento</b> con una o más observaciones, no un día "
        "ni un viaje. Los rellenan los propios viajeros: el 14 % que declara antílope "
        "sable en Okaukuejo es la medida del ruido que traen.</li>"
        "<li><b>Índice de registros:</b> <i>GBIF</i>, recuento de ocurrencias dentro del "
        "polígono de cada zona y filtrado a octubre y noviembre "
        "<span class='u'>api.gbif.org/v1/occurrence/search</span>. El polígono de Etosha "
        "es el límite real del parque en OpenStreetMap; las otras tres zonas son cajas "
        "sobre la costa, el Namib y Damaraland. Lo baja y lo cachea "
        "<code>fuente/avistamientos.py</code>, y las cifras de este PDF salen de ese "
        f"fichero: {len(zonas)} zonas, {len(d.get('especies', {}))} especies.</li>")


def completa(d):
    """Anade al cache SOLO las especies del catalogo que aun no tienen recuento.

    Cuando el catalogo crece (las 33 rapaces y felinos del 15/08) no hace falta
    rehacer las 115 anteriores ni volver a raspar Expert Africa: se resuelven las
    nuevas y se cuentan contra las mismas zonas. Los totales por clase de cada zona
    se dejan como estan —son el denominador de todas las fichas y conviene que
    todas compartan la misma foto de GBIF—; unos dias de deriva no cambian nada.
    """
    en_cache = set(d.get("especies", {}))
    faltan = [(slug, es, sci) for _, _, lista in catalogo.GRUPOS_FAUNA
              for slug, es, _en, sci, _f in lista if slug not in en_cache]
    sobran = en_cache - {slug for _, _, lista in catalogo.GRUPOS_FAUNA for slug, *_ in lista}
    for slug in sobran:
        d["especies"].pop(slug)
        print(f"   fuera del catalogo, fuera del cache: {slug}")
    if not faltan:
        return False
    print(f"GBIF · {len(faltan)} especies nuevas en el catalogo")
    tx = {}
    for slug, es, sci in faltan:
        m = pide("species/match", name=sci, strict="false")
        clave = m.get("speciesKey") or m.get("usageKey")
        if not clave or m.get("matchType") == "NONE":
            print(f"   !! sin taxon en GBIF: {es} ({sci})")
            continue
        tx[slug] = {"clave": clave, "sci": m.get("canonicalName") or sci,
                    "clase": m.get("class") or m.get("phylum") or "?",
                    "clase_clave": m.get("classKey"), "rango": m.get("rank", "")}
        time.sleep(.15)
    facetas_cache = {}
    for slug, t in tx.items():
        fila = {"sci": t["sci"], "clase": t["clase"], "clase_clave": t["clase_clave"],
                "rango": t["rango"], "zonas": {}}
        for zona in ("etosha", "costa", "namib", "damaraland"):
            g = d["zonas"][zona]["wkt"]
            if t["rango"] in ("SPECIES", "SUBSPECIES", "VARIETY", "FORM"):
                k = (zona, t["clase_clave"])
                if k not in facetas_cache:
                    _, todo = facetas(g, t["clase_clave"])
                    _, ventana = facetas(g, t["clase_clave"], MESES)
                    facetas_cache[k] = (todo, ventana)
                todo, ventana = facetas_cache[k]
                n, nv = todo.get(t["clave"], 0), ventana.get(t["clave"], 0)
            else:
                n, nv = sueltos(g, t["clave"]), sueltos(g, t["clave"], MESES)
            fila["zonas"][zona] = {"registros": n, "oct_nov": nv}
        d["especies"][slug] = fila
        print(f"   {slug:<26} " + " ".join(
            f"{z}:{fila['zonas'][z]['oct_nov']}/{fila['zonas'][z]['registros']}"
            for z in ("etosha", "costa", "namib", "damaraland")))
    return True


def main():
    ruta = os.path.join(GEO, SALIDA)
    forzar = "--forzar" in sys.argv
    d = json.load(open(ruta)) if os.path.exists(ruta) and not forzar else {}
    if not d.get("especies"):
        print("GBIF · resolviendo los taxones del catalogo")
        tx = taxones()
        print(f"   {len(tx)} taxones resueltos")
        d.update(recuenta(tx))
    elif not completa(d):
        print(f"ya esta: los recuentos de GBIF de geo/{SALIDA}")
    if not d.get("campamentos"):
        print("Expert Africa · partes de avistamiento de los tres campamentos")
        d["campamentos"] = viajeros()
    else:
        print("ya esta: los porcentajes por campamento")
    d.update(fuente="GBIF · api.gbif.org/v1/occurrence/search",
             fuente_campamentos="Expert Africa · partes de avistamiento de sus viajeros",
             ventana="octubre y noviembre, todos los anos disponibles",
             muestra_minima=MUESTRA_MINIMA)
    os.makedirs(GEO, exist_ok=True)
    with open(ruta, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(f"-> geo/{SALIDA} ({os.path.getsize(ruta) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
