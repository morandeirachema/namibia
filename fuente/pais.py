#!/usr/bin/env python3
"""Donde vive cada bicho DENTRO DE NAMIBIA, region por region y medido en GBIF.

La guia de fauna responde dos preguntas distintas y no conviene mezclarlas:

  1 · **¿lo vamos a ver en este viaje?** — eso lo contesta `avistamientos.py`, con los
      partes de Expert Africa y con los registros de GBIF **dentro de las cuatro zonas
      de la ruta** y **filtrados a octubre y noviembre**, que son las fechas.

  2 · **¿donde vive en Namibia?** — eso lo contesta este modulo, con los registros de
      GBIF **en las catorce regiones del pais** y **sin filtrar por mes**: la pregunta
      es de reparto geografico, no de calendario, y recortar a dos meses solo anadiria
      ruido de muestreo a una region que ya de por si tiene pocos registros.

El reparto se pide a GBIF por `gadmGid`, el codigo de la division administrativa —el
mismo que dibuja el mapa desde `geo/regiones.json`, bajado de OpenStreetMap—. GADM
todavia trae **Kavango entero** (la particion en Este y Oeste es de 2013), asi que las
dos regiones del mapa comparten gid y sus recuentos se suman.

Esto NO es una probabilidad de avistamiento y aqui no se le llama asi, igual que en
`avistamientos.py`: es donde se ha REGISTRADO la especie, con todos los sesgos del
observador —la Franja de Caprivi tiene lodges con ornitologos y el Kaokoveld no—. Por
eso la ficha da siempre el recuento crudo detras del reparto, y por eso no se dice
nada de una region con cuatro registros.

Uso:
    python3 fuente/pais.py            # solo las especies que falten
    python3 fuente/pais.py --forzar   # todo otra vez

Resultado versionado en fuente/geo/fauna-pais.json; el build del PDF no toca la red.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "geo")
sys.path.insert(0, HERE)

import catalogo                                                    # noqa: E402
from avistamientos import pide                                     # noqa: E402
from comun import mil as _mil                                      # noqa: E402

SALIDA = "fauna-pais.json"

# Los catorce nombres del mapa, agrupados por el gid de GADM con el que se cuenta, y
# el apodo con el que los conoce un viajero: «Zambezi» no le dice nada a nadie y «la
# Franja de Caprivi» si. El orden es el del norte al sur, que es como se lee el pais.
REGIONES = [
    ("NAM.13_1", "Zambezi", "la Franja de Caprivi"),
    ("NAM.4_1", "Kavango", "el rio Okavango y Khaudum"),
    ("NAM.7_1", "Ohangwena", "el norte de Owambo"),
    ("NAM.9_1", "Omusati", "el oeste de Owambo"),
    ("NAM.10_1", "Oshana", "el centro de Owambo"),
    ("NAM.11_1", "Oshikoto", "Tsumeb y el este de Etosha"),
    ("NAM.6_1", "Kunene", "el Kaokoveld, Damaraland y el oeste de Etosha"),
    ("NAM.12_1", "Otjozondjupa", "el Waterberg y el bosque del noreste"),
    ("NAM.2_1", "Erongo", "Swakopmund, Walvis Bay y la costa central"),
    ("NAM.8_1", "Omaheke", "el Kalahari del este"),
    ("NAM.5_1", "Khomas", "la meseta de Windhoek"),
    ("NAM.3_1", "Hardap", "Sossusvlei, el Naukluft y el Kalahari del sur"),
    ("NAM.1_1", "ǁKaras", "el sur: Fish River, Lüderitz y el Sperrgebiet"),
]

# Por debajo de esto no se nombra una region en la ficha: con tres registros de leon en
# Oshana no se dice que el leon viva en Oshana.
MINIMO_REGION = 5


def facetas(gid, clase_clave):
    """Un tiro por clase y region: GBIF devuelve el recuento de TODAS sus especies."""
    d = pide("occurrence/search", gadmGid=gid, taxonKey=clase_clave,
             facet="speciesKey", facetLimit=3000, limit=0)
    cuentas = {int(c["name"]): c["count"] for c in d["facets"][0]["counts"]} if d["facets"] else {}
    return d["count"], cuentas


def sueltos(clave, gid=None):
    """Para los taxones que no son especie: el solifugo es un orden y el anofeles, un genero."""
    kw = dict(taxonKey=clave, limit=0)
    kw.update({"gadmGid": gid} if gid else {"country": "NA"})
    return pide("occurrence/search", **kw)["count"]


def del_catalogo():
    """slug -> (sci, clase_clave, rango, clave) reusando los taxones ya resueltos."""
    prev = json.load(open(os.path.join(GEO, "avistamientos.json")))["especies"]
    out = {}
    for _, _, lista in catalogo.GRUPOS_FAUNA:
        for slug, es, _en, sci, _f in lista:
            p = prev.get(slug)
            if p:
                out[slug] = dict(sci=p["sci"], clase=p["clase"], clase_clave=p["clase_clave"],
                                 rango=p["rango"], clave=None)
                continue
            m = pide("species/match", name=sci, strict="false")
            clave = m.get("speciesKey") or m.get("usageKey")
            if not clave or m.get("matchType") == "NONE":
                print(f"   !! sin taxon en GBIF: {es} ({sci})")
                continue
            out[slug] = dict(sci=m.get("canonicalName") or sci,
                             clase=m.get("class") or m.get("phylum") or "?",
                             clase_clave=m.get("classKey"), rango=m.get("rank", ""),
                             clave=clave)
            time.sleep(.15)
    # La clave de especie hace falta para leer las facetas; las del cache no la guardan.
    for slug, t in out.items():
        if t["clave"] is None:
            m = pide("species/match", name=t["sci"], strict="false")
            t["clave"] = m.get("speciesKey") or m.get("usageKey")
            time.sleep(.12)
    return out


# ---------------------------------------------------------------------------
# Lo que lee el PDF: la linea de «donde vive en Namibia» de cada ficha
# ---------------------------------------------------------------------------

_cache = None


def datos():
    global _cache
    if _cache is None:
        ruta = os.path.join(GEO, SALIDA)
        _cache = json.load(open(ruta)) if os.path.exists(ruta) else {}
    return _cache


def apodos():
    return {gid: (nombre, apodo) for gid, nombre, apodo in REGIONES}


def donde(slug, cuantas=4):
    """(texto, en_la_ruta) con el reparto por regiones, o None si no hay nada que decir.

    Se nombran las regiones con MINIMO_REGION registros o mas y se dan las cifras
    crudas: sin el denominador, «Kavango» a secas suena a certeza y es un recuento.
    Lo que GBIF no situa en ninguna region —lo del mar, y lo que llego sin coordenada y
    solo consta «Namibia»— se dice aparte en vez de desaparecer de la resta.
    """
    d = datos()
    sp = (d.get("especies") or {}).get(slug)
    if not sp:
        return None
    nombres = apodos()
    total = sp.get("pais", 0)
    reparto = sorted(((g, n) for g, n in sp.get("regiones", {}).items() if n >= MINIMO_REGION),
                     key=lambda x: -x[1])
    if total < 10 and not reparto:
        return (f"solo {total} registro{'s' if total != 1 else ''} en todo el país: "
                f"la muestra no da para decir dónde", None)
    if not reparto:
        return (f"{_mil(total)} registros en el país y ninguno dentro de una región: "
                f"o son del mar, o llegaron sin coordenada", None)
    fuera = total - sum(n for _, n in sp["regiones"].items())
    cabeza = " · ".join(f"<b>{nombres[g][0]}</b> {_mil(n)}" for g, n in reparto[:cuantas])
    resto = len(reparto) - cuantas
    cola = (f" · y {resto} regiones más" if resto > 1
            else " · y una región más" if resto == 1 else "")
    mar = (f", {_mil(fuera)} sin región —del mar o sin coordenada—"
           if fuera >= max(5, total * .05) else "")
    dominante = nombres[reparto[0][0]][1]
    return (f"{cabeza}{cola} — de {_mil(total)} registros en el país{mar}. "
            f"El grueso, en <i>{dominante}</i>.", reparto[0][0])


def fuente_html():
    """La linea de creditos de este reparto, con sus numeros de verdad."""
    d = datos()
    if not d:
        return ""
    regs = d.get("regiones") or {}
    esp = d.get("especies") or {}
    return ("<li><b>Dónde vive en Namibia:</b> <i>GBIF</i>, recuento de ocurrencias por "
            "división administrativa (<code>gadmGid</code>) "
            "<span class='u'>api.gbif.org/v1/occurrence/search</span> — "
            f"{len(regs)} regiones, {len(esp)} especies, <b>sin filtrar por mes</b>: la "
            "pregunta es dónde vive, no cuándo. El límite de cada región lo dibuja "
            "OpenStreetMap (ODbL). Lo baja y lo cachea <code>fuente/pais.py</code>. Es "
            "<b>dónde se ha registrado</b> la especie, con el sesgo del observador que eso "
            "arrastra: en la Franja de Caprivi hay lodges con ornitólogos y en el Kaokoveld "
            "no.</li>")


def main():
    ruta = os.path.join(GEO, SALIDA)
    forzar = "--forzar" in sys.argv
    d = json.load(open(ruta)) if os.path.exists(ruta) and not forzar else {}
    regiones = d.get("regiones") or {}
    especies = d.get("especies") or {}
    pais = d.get("pais") or {}

    print("GBIF · resolviendo los taxones del catalogo")
    tx = del_catalogo()
    print(f"   {len(tx)} taxones")

    # Que hay que bajar: las clases de las especies que aun no tienen recuento, mas
    # cualquier clase que le falte a una region. Bajar una clase entera cuesta un tiro
    # por region y trae de golpe TODAS sus especies, asi que nunca se pide por especie.
    faltan = [s for s in tx if s not in especies]
    clases = {t["clase_clave"] for s, t in tx.items()
              if t["clase_clave"] and (s in faltan or forzar)}
    for gid, _n, _a in REGIONES:
        clases |= {t["clase_clave"] for t in tx.values() if t["clase_clave"]
                   and str(t["clase_clave"]) not in (regiones.get(gid, {}).get("por_clase") or {})}
    if faltan:
        print(f"   {len(faltan)} especies sin recuento: {', '.join(faltan[:6])}"
              f"{'…' if len(faltan) > 6 else ''}")
    if not clases:
        print("ya esta: el reparto por regiones de todo el catalogo")
    tablas = {}
    for gid, nombre, _apodo in REGIONES:
        if not clases:
            break
        print(f"GBIF · {nombre}")
        fila = regiones.setdefault(gid, {"nombre": nombre, "por_clase": {}})
        fila["nombre"] = nombre
        tabla = {}
        for ck in sorted(clases):
            n, cuentas = facetas(gid, ck)
            fila["por_clase"][str(ck)] = n
            tabla.update(cuentas)
            print(f"   clase {ck:>10}: {n:>7} registros")
        tablas[gid] = tabla
    if clases:
        print("GBIF · Namibia entera")
        tabla_pais = {}
        for ck in sorted(clases):
            r = pide("occurrence/search", country="NA", taxonKey=ck,
                     facet="speciesKey", facetLimit=3000, limit=0)
            pais[str(ck)] = r["count"]
            tabla_pais.update({int(c["name"]): c["count"] for c in r["facets"][0]["counts"]})
            print(f"   clase {ck:>10}: {r['count']:>7} registros")
        tablas["_pais"] = tabla_pais

    for slug, t in tx.items():
        if slug in especies and not forzar and slug not in faltan:
            continue
        fila = especies.get(slug) if not forzar else None
        fila = fila or {"sci": t["sci"], "clase": t["clase"], "clase_clave": t["clase_clave"],
                        "rango": t["rango"], "regiones": {}}
        for gid, tabla in tablas.items():
            if t["rango"] in ("SPECIES", "SUBSPECIES", "VARIETY", "FORM"):
                n = tabla.get(t["clave"], 0)
            else:
                n = sueltos(t["clave"], None if gid == "_pais" else gid)
            if gid == "_pais":
                fila["pais"] = n
            else:
                fila["regiones"][gid] = n
        especies[slug] = fila
        if slug in faltan:
            top = sorted(fila["regiones"].items(), key=lambda x: -x[1])[:3]
            print(f"   {slug:<24} pais {fila.get('pais', 0):>6} · " +
                  " ".join(f"{g.split('.')[1]}:{n}" for g, n in top))

    # Lo que ya no esta en el catalogo tampoco tiene que estar en el cache.
    for slug in set(especies) - set(tx):
        especies.pop(slug)
        print(f"   fuera del catalogo, fuera del cache: {slug}")

    d.update(regiones=regiones, especies=especies, pais=pais,
             fuente="GBIF · api.gbif.org/v1/occurrence/search, reparto por gadmGid",
             limite="sin filtrar por mes: la pregunta es donde vive, no cuando",
             minimo_region=MINIMO_REGION)
    with open(ruta, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(f"-> geo/{SALIDA} ({os.path.getsize(ruta) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
