# -*- coding: utf-8 -*-
"""Dibuja los mapas del dossier en SVG, a partir de la geometria cacheada en geo/.

No usa red ni dependencias: lee los JSON que dejo `geodatos.py` y devuelve cadenas SVG
que `dossier.py` incrusta en el HTML. Al ser vectorial, el mapa sale nitido en el PDF a
cualquier tamano y pesa unos pocos KB.

Proyeccion: equirectangular con el eje X corregido por el coseno de la latitud media.
A la escala de Namibia (unos 1.300 km) la deformacion es despreciable y a cambio el
codigo es trivial de auditar — que es lo que pide un dossier que presume de fuentes.
"""
import json
import math
import os

import trazado
from geodatos import anillos

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "geo")

# ---------------------------------------------------------------------------
# Paleta — la misma del sitio y del PDF
# ---------------------------------------------------------------------------
C = {
    "tinta":     "#16130F",
    "tinta2":    "#56514A",
    "tinta3":    "#7D776E",
    "papel":     "#F4F1EA",
    "tierra":    "#EAE5DA",
    "vecino":    "#DCD8CF",
    "borde":     "#B8B3A8",
    "mar":       "#D6DFE2",
    "mar2":      "#B9C7CC",
    "sal":       "#FBFAF7",
    "parque":    "#E3E7DA",
    "parqueb":   "#9CAA83",
    "oxido":     "#C2542F",
    # Tinte calido para las regiones que pisa la ruta en el mapa de la guia de fauna:
    # es el oxido de la ruta rebajado, para que se lean como «lo de este viaje» sin
    # competir con la linea del trazado, que va encima.
    "region":    "#EFDACD",
    "verde":     "#5F7043",
    "oro":       "#8A6210",
    "rojo":      "#A32E28",
}


def carga(nombre):
    with open(os.path.join(GEO, nombre)) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Lienzo: convierte (lat, lon) en coordenadas de dibujo
# ---------------------------------------------------------------------------

class Lienzo:
    def __init__(self, sur, oeste, norte, este, ancho, margen=0):
        self.sur, self.oeste, self.norte, self.este = sur, oeste, norte, este
        self.k = math.cos(math.radians((sur + norte) / 2))       # correccion de meridianos
        self.margen = margen
        util = ancho - 2 * margen
        self.esc = util / ((este - oeste) * self.k)
        self.ancho = ancho
        self.alto = (norte - sur) * self.esc + 2 * margen

    def xy(self, lat, lon):
        return (self.margen + (lon - self.oeste) * self.k * self.esc,
                self.margen + (self.norte - lat) * self.esc)

    # El dibujo se recorta EXACTAMENTE al marco: cualquier holgura la sigue contando
    # el navegador como ancho de pagina.
    HOLGURA = 0

    def d(self, puntos, cerrar=False, dec=1):
        """Path SVG a partir de [(lat, lon), ...], con las coordenadas acotadas al marco.

        El acotado importa mas de lo que parece: los contornos de Natural Earth abarcan
        paises enteros y se salen del encuadre por miles de unidades. Esa geometria no
        se ve —queda fuera del viewBox— pero al incrustar el SVG en el HTML del dossier
        ensancha la caja, y con la caja ancha Chrome encoge el documento ENTERO al
        imprimirlo. Recortando aqui, el dibujo es el mismo y la pagina no se mueve.
        """
        if not puntos:
            return ""
        lim_x = (-self.HOLGURA, self.ancho + self.HOLGURA)
        lim_y = (-self.HOLGURA, self.alto + self.HOLGURA)
        trozos = []
        for i, (lat, lon) in enumerate(puntos):
            x, y = self.xy(lat, lon)
            x = min(max(x, lim_x[0]), lim_x[1])
            y = min(max(y, lim_y[0]), lim_y[1])
            trozos.append(f"{'M' if i == 0 else 'L'}{x:.{dec}f} {y:.{dec}f}")
        return "".join(trozos) + ("Z" if cerrar else "")

    def km_por_unidad(self):
        return 1 / (self.esc / 111.32)


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------------------
# Capas reutilizables
# ---------------------------------------------------------------------------

def capa_paises(L, resaltar="Namibia"):
    out = []
    for f in carga("paises.json")["features"]:
        nom = f["properties"]["nombre"]
        geom = f["geometry"]
        # GeoJSON: Polygon son anillos; MultiPolygon, una lista de poligonos.
        # Se normaliza a lista de poligonos para recorrerlo todo igual.
        poligonos = ([geom["coordinates"]] if geom["type"] == "Polygon"
                     else geom["coordinates"])
        d = ""
        for poly in poligonos:
            for anillo in poly:
                if len(anillo) < 3:
                    continue
                d += L.d([(p[1], p[0]) for p in anillo], cerrar=True)
        if not d:
            continue
        relleno = C["tierra"] if nom == resaltar else C["vecino"]
        trazo = C["tinta3"] if nom == resaltar else C["borde"]
        grosor = 1.6 if nom == resaltar else 0.7
        out.append(f'<path d="{d}" fill="{relleno}" stroke="{trazo}" fill-rule="evenodd" '
                   f'stroke-width="{grosor}" stroke-linejoin="round"/>')
    return "".join(out)


def capa_parques(L, nombres=None, relleno=None, trazo=None, ancho=0.9, guion="2.5 2"):
    out = []
    for e in carga("parques.json")["elements"]:
        nom = e["tags"].get("name", "")
        if nombres and not any(n.lower() in nom.lower() for n in nombres):
            continue
        d = "".join(L.d(a, cerrar=True) for a in anillos(e) if len(a) > 2)
        if not d:
            continue
        out.append(f'<path d="{d}" fill="{relleno or C["parque"]}" '
                   f'stroke="{trazo or C["parqueb"]}" stroke-width="{ancho}" '
                   f'stroke-dasharray="{guion}" fill-rule="evenodd"/>')
    return "".join(out)


def capa_pan(L, borde=0.8):
    """La depresion de Etosha: relleno de sal, con las islas recortadas."""
    for e in carga("etosha_pan.json")["elements"]:
        if e["tags"].get("natural") != "water":
            continue
        d = "".join(L.d(a, cerrar=True) for a in anillos(e, "outer") if len(a) > 2)
        d += "".join(L.d(a, cerrar=True) for a in anillos(e, "inner") if len(a) > 2)
        return (f'<path d="{d}" fill="{C["sal"]}" stroke="{C["borde"]}" '
                f'stroke-width="{borde}" fill-rule="evenodd"/>')
    return ""


def capa_ruta(L, etapas=None, ancho=3.4, halo=True, fichero="ruta.json"):
    """La polilinea de carretera, un trazo por dia, con el color de su bloque."""
    out = []
    datos = carga(fichero)
    for e in datos:
        if etapas and e["id"] not in etapas:
            continue
        if not e.get("geometria"):
            continue
        d = L.d([(p[1], p[0]) for p in e["geometria"]])
        if halo:
            out.append(f'<path d="{d}" fill="none" stroke="{C["papel"]}" '
                       f'stroke-width="{ancho + 2.2}" stroke-linecap="round" '
                       f'stroke-linejoin="round" opacity=".85"/>')
        col = trazado.COLOR_BLOQUE[e["bloque"]]
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{ancho}" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Adornos
# ---------------------------------------------------------------------------

def escala(L, x, y, km=200, ancho_texto=7):
    u = km / L.km_por_unidad()
    return (f'<g font-size="{ancho_texto}" fill="{C["tinta2"]}" font-weight="600">'
            f'<line x1="{x}" y1="{y}" x2="{x + u}" y2="{y}" stroke="{C["tinta"]}" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{y - 2.6}" x2="{x}" y2="{y + 2.6}" stroke="{C["tinta"]}" stroke-width="1.6"/>'
            f'<line x1="{x + u}" y1="{y - 2.6}" x2="{x + u}" y2="{y + 2.6}" stroke="{C["tinta"]}" stroke-width="1.6"/>'
            f'<line x1="{x + u / 2}" y1="{y - 1.8}" x2="{x + u / 2}" y2="{y + 1.8}" stroke="{C["tinta"]}" stroke-width="1"/>'
            f'<text x="{x}" y="{y + 9.5}" text-anchor="middle">0</text>'
            f'<text x="{x + u / 2}" y="{y + 9.5}" text-anchor="middle">{km // 2}</text>'
            f'<text x="{x + u}" y="{y + 9.5}" text-anchor="middle">{km} km</text></g>')


def norte(x, y, r=11):
    return (f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="{C["papel"]}" stroke="{C["borde"]}" '
            f'stroke-width=".8"/>'
            f'<path d="M{x} {y - r + 2.5}L{x + 3.4} {y + r - 4}L{x} {y + r - 6.5}'
            f'L{x - 3.4} {y + r - 4}Z" fill="{C["tinta"]}"/>'
            f'<text x="{x}" y="{y - r - 2.5}" text-anchor="middle" font-size="7.5" '
            f'font-weight="700" fill="{C["tinta"]}">N</text></g>')


def tropico(L, lat=-23.4362):
    """El tropico de Capricornio: la ruta lo cruza el D5, y viene rotulado en la C14."""
    if not (L.sur < lat < L.norte):
        return ""
    _, y = L.xy(lat, L.oeste)
    x0, _ = L.xy(lat, L.oeste)
    x1, _ = L.xy(lat, L.este)
    return (f'<g><line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{C["tinta3"]}" '
            f'stroke-width=".7" stroke-dasharray="6 4" opacity=".7"/>'
            f'<text x="{x1 - 4}" y="{y - 3:.1f}" text-anchor="end" font-size="7" '
            f'fill="{C["tinta3"]}" font-style="italic">trópico de Capricornio</text></g>')


ICONO = {          # radio y forma segun la clase del punto
    "parada": 5.2, "puerta": 4.0, "hito": 3.4, "paso": 3.8, "ciudad": 3.6, "combu": 3.6,
}


def punto(L, clave, texto=None, dx=7, dy=2.6, anclaje="start", tam=8.4, clase=None,
          negrita=True, color=None):
    lat, lon, rotulo, cl = trazado.PUNTOS[clave]
    cl = clase or cl
    x, y = L.xy(lat, lon)
    r = ICONO.get(cl, 3.4)
    col = color or {"parada": C["oxido"], "puerta": C["rojo"], "paso": C["oro"],
                    "combu": C["verde"]}.get(cl, C["tinta"])
    g = []
    if cl == "parada":
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 2.4}" fill="{C["papel"]}" opacity=".9"/>')
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="{C["papel"]}" stroke-width="1.6"/>')
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 2.4}" fill="{C["papel"]}"/>')
    elif cl == "puerta":
        g.append(f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" '
                 f'fill="{col}" stroke="{C["papel"]}" stroke-width="1.4" transform="rotate(45 {x:.1f} {y:.1f})"/>')
    else:
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="{C["papel"]}" stroke-width="1.3"/>')
    t = esc(texto if texto is not None else rotulo)
    if t:
        peso = "700" if negrita and cl in ("parada", "ciudad") else "500"
        g.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anclaje}" '
                 f'font-size="{tam}" font-weight="{peso}" fill="{C["tinta"]}" '
                 f'paint-order="stroke" stroke="{C["papel"]}" stroke-width="2.6" '
                 f'stroke-linejoin="round">{t}</text>')
    return "".join(g)


_ENVOLTORIOS = [0]


def envoltorio(ancho, alto, cuerpo, fondo=None):
    """Cierra el SVG, con TODO el dibujo recortado al marco.

    El recorte no es cosmetico. Los contornos de Natural Earth abarcan paises enteros y
    se salen del encuadre por miles de unidades; al incrustar el SVG en el HTML del
    dossier, esa geometria desbordada ensancha la pagina y Chrome, al imprimir, encoge
    el documento ENTERO para que quepa — la portada y los mapas salian a tres cuartos
    de su tamano. Con un clipPath explicito no se escapa nada.
    """
    _ENVOLTORIOS[0] += 1
    marco = f"marco{_ENVOLTORIOS[0]}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" '
            f'role="img" overflow="hidden" style="display:block;overflow:hidden">'
            f'<defs><clipPath id="{marco}">'
            f'<rect width="{ancho:.0f}" height="{alto:.0f}"/></clipPath></defs>'
            f'<g clip-path="url(#{marco})">'
            f'<rect width="{ancho:.0f}" height="{alto:.0f}" fill="{fondo or C["mar"]}"/>'
            f'{cuerpo}</g></svg>')


# ---------------------------------------------------------------------------
# Mapa por dia · la etapa sola, con su firme
# ---------------------------------------------------------------------------

# El color de cada firme en el mapa del dia. Lo urbano (calles con nombre, sin ref) es
# ruido de pocos kilometros y se pinta como asfalto sin contarlo aparte.
COLOR_FIRME = {"asfalto": "#3A3632", "grava": "#C2542F", "sal": "#8A6210",
               "parque": "#5F7043", "urbano": "#3A3632"}
NOMBRE_FIRME = {"asfalto": "asfalto", "grava": "grava", "sal": "sal compactada",
                "parque": "pista de parque"}
VEL = {"asfalto": 100.0, "urbano": 100.0, "grava": 80.0, "sal": 80.0, "parque": 60.0}


def _tramos(dia):
    for e in carga("tramos.json"):
        if e["id"] == dia:
            return e["tramos"]
    return []


def firme_del_dia(dia):
    """Kilometros por firme, y el tiempo minimo a las velocidades de planificacion del `13`.

    Devuelve (km_por_firme, horas_minimo). El urbano se suma al asfalto: son calles de
    Windhoek o de la costa, y contarlas aparte solo anadiria una fila de 4 km.
    """
    km = {}
    for t in _tramos(dia):
        f = t["firme"] or "urbano"
        f = "asfalto" if f == "urbano" else f
        km[f] = km.get(f, 0.0) + t["km"]
    # un firme de menos de un kilometro es un cruce, no una fila de la ficha
    km = {f: v for f, v in km.items() if v >= 1}
    horas = sum(v / VEL[f] for f, v in km.items())
    return km, horas


def mapa_dia(dia, ancho=1000, alto=None):
    """El mapa de UNA etapa: su recorrido pintado por firme, los puntos por los que pasa
    y, de gris, lo que la ruta hace los demas dias, para que se vea de donde se viene."""
    etapa = next(e for e in trazado.ETAPAS if e["id"] == dia)
    tramos = _tramos(dia)
    puntos = etapa["por"]
    if not tramos:                                       # dia sin traslado
        puntos = [etapa["duerme"]]
    lats = [trazado.PUNTOS[p][0] for p in puntos]
    lons = [trazado.PUNTOS[p][1] for p in puntos]
    for t in tramos:
        for lon, lat in t["geometria"]:
            lats.append(lat); lons.append(lon)
    # los puntos de interes del dia tambien entran en el encuadre: en un dia sin traslado
    # son el mapa entero (Walvis Bay con Pelican Point, Dune 7 y el Welwitschia Drive)
    interes = carga("interes.json")["puntos"] if os.path.exists(
        os.path.join(GEO, "interes.json")) else []
    for pi in interes:
        if dia in pi["dias"]:
            lats.append(pi["lat"]); lons.append(pi["lon"])
    # encuadre: la etapa con aire alrededor, y nunca mas apaisado de lo que pide la caja.
    # El minimo de 0,25 grados (~28 km) es lo que hace que un dia de 70 km de safari o
    # un dia de descanso llenen la pagina en vez de salir como un punto en un desierto.
    holg = 0.14
    dlat, dlon = max(lats) - min(lats), max(lons) - min(lons)
    dlat, dlon = max(dlat, 0.25), max(dlon, 0.25)
    k = math.cos(math.radians((max(lats) + min(lats)) / 2))
    prop = (alto / ancho) if alto else 0.62
    # ajustar para que la caja tenga la proporcion pedida
    if dlat / (dlon * k) < prop:
        dlat = dlon * k * prop
    else:
        dlon = dlat / (k * prop)
    clat, clon = (max(lats) + min(lats)) / 2, (max(lons) + min(lons)) / 2
    L = Lienzo(sur=clat - dlat * (0.5 + holg), oeste=clon - dlon * (0.5 + holg),
               norte=clat + dlat * (0.5 + holg), este=clon + dlon * (0.5 + holg),
               ancho=ancho)
    cuerpo = [capa_paises(L)]
    cuerpo.append(capa_parques(L, ["Namib-Naukluft", "Skeleton Coast", "Dorob", "Etosha"]))
    cuerpo.append(capa_pan(L))
    cuerpo.append(tropico(L))
    # el resto de la ruta, de gris fino
    for e in carga("ruta.json"):
        if e["id"] != dia and e.get("geometria"):
            d = L.d([(p[1], p[0]) for p in e["geometria"]])
            cuerpo.append(f'<path d="{d}" fill="none" stroke="{C["borde"]}" '
                          f'stroke-width="2.2" stroke-linecap="round" opacity=".7"/>')
    # la etapa, por firme
    for t in tramos:
        d = L.d([(p[1], p[0]) for p in t["geometria"]])
        col = COLOR_FIRME[t["firme"] or "urbano"]
        cuerpo.append(f'<path d="{d}" fill="none" stroke="{C["papel"]}" stroke-width="7" '
                      f'stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
        cuerpo.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4.2" '
                      f'stroke-linecap="round" stroke-linejoin="round"/>')
    # puntos de paso: los del dia grandes y rotulados, los de alrededor pequenos
    vistos = set()
    for clave in puntos:
        if clave in vistos:
            continue
        vistos.add(clave)
        dx, dy, anc = ROTULOS_RUTA.get(clave, (8, 4, "start"))
        cuerpo.append(punto(L, clave, None, dx, dy, anc, tam=13))
    for clave, (lat, lon, rot, cl) in trazado.puntos_oficiales().items():
        if clave in vistos:
            continue
        x, y = L.xy(lat, lon)
        if 12 < x < L.ancho - 12 and 12 < y < L.alto - 12:
            cuerpo.append(punto(L, clave, rot, 6, 3, "start", tam=9.6, negrita=False,
                                color=C["tinta3"]))
    # los puntos de interes del dia: donde comer, joyas y compras (geo/interes.json)
    for pi in interes:
        if dia not in pi["dias"]:
            continue
        x, y = L.xy(pi["lat"], pi["lon"])
        if not (10 < x < L.ancho - 10 and 10 < y < L.alto - 10):
            continue
        col = COLOR_INTERES[pi["clase"]]
        cuerpo.append(f'<rect x="{x - 4.2:.1f}" y="{y - 4.2:.1f}" width="8.4" height="8.4" '
                      f'rx="1.6" fill="{col}" stroke="{C["papel"]}" stroke-width="1.4"/>')
        cuerpo.append(f'<text x="{x + 7:.1f}" y="{y + 3.6:.1f}" font-size="10.6" '
                      f'font-weight="600" fill="{col}" paint-order="stroke" '
                      f'stroke="{C["papel"]}" stroke-width="2.6" stroke-linejoin="round">'
                      f'{esc(pi["rotulo"])}</text>')
    # escala acorde al encuadre
    km_esc = 50 if L.km_por_unidad() * L.ancho < 400 else 100
    if L.km_por_unidad() * L.ancho < 120:
        km_esc = 20
    cuerpo.append(escala(L, 30, L.alto - 30, km_esc, ancho_texto=9))
    cuerpo.append(norte(L.ancho - 36, 40, r=12))
    cuerpo.append(leyenda_dia(L, [t["firme"] or "urbano" for t in tramos],
                              {pi["clase"] for pi in interes if dia in pi["dias"]},
                              {trazado.PUNTOS[p][3] for p in puntos}))
    return envoltorio(L.ancho, L.alto, "".join(cuerpo))


COLOR_INTERES = {"comer": "#8A3B8E", "joya": "#2F6E8E", "compra": "#5F7043",
                 "dormir": "#C2542F"}
NOMBRE_INTERES = {"comer": "dónde comer", "joya": "qué ver de paso", "compra": "compra",
                  "dormir": "el camping"}


def leyenda_dia(L, firmes, clases_interes, clases_punto):
    """La leyenda del mapa del dia, arriba a la izquierda: firmes que pisa y simbolos."""
    filas = []
    for f in ("asfalto", "grava", "sal", "parque"):
        if f in firmes:
            filas.append(("linea", COLOR_FIRME[f], NOMBRE_FIRME[f]))
    simb = [("parada", "donde se duerme"), ("combu", "gasolinera obligatoria"),
            ("puerta", "puerta de parque con horario"), ("paso", "puerto de montaña"),
            ("hito", "lo que se visita")]
    for cl, nom in simb:
        if cl in clases_punto:
            filas.append((cl, None, nom))
    for cl in ("dormir", "comer", "joya", "compra"):
        if cl in clases_interes:
            filas.append(("cuadro", COLOR_INTERES[cl], NOMBRE_INTERES[cl]))
    if not filas:
        return ""
    x0, y0, paso = 22, 22, 17
    alto = 14 + paso * len(filas)
    out = [f'<rect x="{x0 - 10}" y="{y0 - 10}" width="212" height="{alto}" rx="5" '
           f'fill="{C["papel"]}" stroke="{C["borde"]}" stroke-width=".9" opacity=".95"/>']
    for i, (tipo, col, nom) in enumerate(filas):
        y = y0 + 8 + paso * i
        if tipo == "linea":
            out.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + 26}" y2="{y}" stroke="{col}" '
                       f'stroke-width="4.2" stroke-linecap="round"/>')
        elif tipo == "cuadro":
            out.append(f'<rect x="{x0 + 9}" y="{y - 4.2}" width="8.4" height="8.4" rx="1.6" '
                       f'fill="{col}" stroke="{C["papel"]}" stroke-width="1.2"/>')
        else:
            r = ICONO[tipo]
            colp = {"parada": C["oxido"], "puerta": C["rojo"], "paso": C["oro"],
                    "combu": C["verde"]}.get(tipo, C["tinta"])
            cx = x0 + 13
            if tipo == "parada":
                out.append(f'<circle cx="{cx}" cy="{y}" r="{r}" fill="{colp}" stroke="{C["papel"]}" stroke-width="1.6"/>'
                           f'<circle cx="{cx}" cy="{y}" r="{r - 2.4}" fill="{C["papel"]}"/>')
            elif tipo == "puerta":
                out.append(f'<rect x="{cx - r}" y="{y - r}" width="{2 * r}" height="{2 * r}" fill="{colp}" '
                           f'stroke="{C["papel"]}" stroke-width="1.2" transform="rotate(45 {cx} {y})"/>')
            else:
                out.append(f'<circle cx="{cx}" cy="{y}" r="{r}" fill="{colp}" stroke="{C["papel"]}" stroke-width="1.2"/>')
        out.append(f'<text x="{x0 + 34}" y="{y + 3.4}" font-size="9.4" fill="{C["tinta"]}">'
                   f'{esc(nom)}</text>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Mapa 1 · la ruta entera
# ---------------------------------------------------------------------------

# clave -> (dx, dy, anclaje). Colocados a mano: en un mapa de veinte rotulos sale
# mejor y mas rapido que cualquier algoritmo de reparto.
ROTULOS_RUTA = {
    "windhoek":        (9, 4, "start"),
    "aeropuerto":      (7, -6, "start"),
    "okahandja":       (8, 3, "start"),
    "otjiwarongo":     (8, 3, "start"),
    "tsumeb":          (8, 3, "start"),
    "outjo":           (8, 3, "start"),
    "rehoboth":        (8, 3, "start"),
    "spreetshoogte":   (-8, 3, "end"),
    "solitaire":       (-8, 3, "end"),
    "sesriem":         (-9, 4, "end"),
    "sossusvlei":      (-8, 3, "end"),
    "walvisbay":       (-9, 4, "end"),
    "swakopmund":      (-8, 3, "end"),
    "hentiesbay":      (-8, 3, "end"),
    "capecross":       (-8, 3, "end"),
    "ugabmund":        (-8, 3, "end"),
    "terracebay":      (-9, 4, "end"),
    "springbokwasser": (-8, -5, "end"),
    "twyfelfontein":   (9, 3, "start"),
    "hoada":           (-9, 1, "end"),
    "kamanjab":        (0, 12, "middle"),
    "andersson":       (-8, 2, "end"),
    "okaukuejo":       (-9, 4, "end"),
    "halali":          (0, -10, "middle"),
    "namutoni":        (-9, -6, "end"),
    "onguma":          (10, 3, "start"),
    "lindequist":      (2, 15, "start"),
    "palmwag":         (-8, -5, "end"),
    # --- solo en el mapa de la variante archivada del `aparte/decision-del-ccf` ---
    "ccf":             (9, 4, "start"),
}

# El CCF cae 40 km al ESTE de Otjiwarongo y su rotulo es largo: con las posiciones de
# siempre se montaba encima del pueblo. En la variante los dos se separan a mano.
ROTULOS_ALT = {
    "otjiwarongo":     (0, -9, "middle"),
}

EN_MAPA_RUTA = ["windhoek", "aeropuerto", "okahandja", "otjiwarongo", "tsumeb", "outjo", "rehoboth",
                "spreetshoogte", "solitaire", "sesriem", "sossusvlei", "walvisbay",
                "swakopmund", "hentiesbay", "capecross", "ugabmund", "terracebay",
                "springbokwasser", "twyfelfontein", "palmwag", "hoada", "kamanjab",
                "andersson", "okaukuejo", "halali", "namutoni", "lindequist", "onguma"]

# El nombre con el que sale cada parada en el mapa, cuando no vale el rotulo de
# `trazado.PUNTOS`. Los DIAS no se escriben aqui: se calculan de las etapas —ver
# `_rotulos()`—, porque escritos a mano se quedaron contando la ruta de agosto
# cuando el itinerario cambio, y el mapa decia «Sesriem D4·D5» con Sesriem ya en D3.
NOMBRE_PARADA = {
    "sossusvlei": "Sossusvlei · Deadvlei",
    "spreetshoogte": "Spreetshoogte",
    "windhoek": "WINDHOEK",
    "onguma": "Onguma Tamboti",
    "ugabmund": "Ugabmund",
    "springbokwasser": "Springbokwasser",
    "andersson": "Andersson",
    "lindequist": "Von Lindequist",
}


def _dias_seguidos(ids):
    """«D2, D3, D4» -> «D2–D4»; los tramos sueltos se separan con un punto medio."""
    nums = sorted(int(i[1:]) for i in ids)
    tramos, ini, prev = [], nums[0], nums[0]
    for n in nums[1:] + [None]:
        if n == prev + 1:
            prev = n
            continue
        tramos.append(f"D{ini}" if ini == prev else f"D{ini}–D{prev}")
        if n is None:
            break
        ini = prev = n
    return " · ".join(tramos)


def _rotulos(etapas):
    """El texto de cada parada, con las noches que se duermen alli pegadas detras."""
    noches = {}
    for e in etapas:
        if e.get("duerme"):
            noches.setdefault(e["duerme"], []).append(e["id"])
    textos = {c: NOMBRE_PARADA.get(c, trazado.PUNTOS[c][2]) for c in trazado.PUNTOS}
    for clave, dias in noches.items():
        textos[clave] = f"{textos[clave]}  {'·'.join(dias)}"
    return textos


def _leyenda(etapas, titulos):
    """Los bloques del viaje con sus dias, sacados de las propias etapas."""
    dias = {}
    for e in etapas:
        dias.setdefault(e["bloque"], []).append(e["id"])
    filas = []
    for bloques, nombre in titulos:
        ids = [i for b in bloques for i in dias.get(b, [])]
        if ids:
            filas.append((bloques[-1], nombre, _dias_seguidos(ids)))
    return filas


def _noches(clave, etapas=None):
    """Los dias que se duerme en una parada, «D12·D13» — para los rotulos sueltos."""
    ids = [e["id"] for e in (etapas or trazado.ETAPAS) if e.get("duerme") == clave]
    return "·".join(ids)


TITULOS_LEYENDA = [
    (("desierto",), "El desierto"),
    (("costa",), "La costa"),
    (("damaraland",), "Damaraland"),
    (("etosha",), "Etosha"),
    (("llegada", "vuelta"), "Ida y vuelta a Windhoek"),
]

TEXTO_ROTULO = _rotulos(trazado.ETAPAS)
BLOQUES_LEYENDA = _leyenda(trazado.ETAPAS, TITULOS_LEYENDA)

# --- la variante del `aparte/decision-del-ccf` -------------------------------------------------
# Variante DESCARTADA el 26/08; el mapa se conserva como registro. Misma ruta que la
# oficial hasta el D12 y solo cambia el final: en vez de la segunda noche de Onguma, el D13
# baja al CCF por la B1 y el D14 sale de alli.
EN_MAPA_ALT = ["windhoek", "aeropuerto", "okahandja", "otjiwarongo", "tsumeb", "outjo",
               "rehoboth", "spreetshoogte", "solitaire", "sesriem", "sossusvlei",
               "walvisbay", "swakopmund", "hentiesbay", "capecross", "ugabmund",
               "terracebay", "springbokwasser", "twyfelfontein", "palmwag", "hoada",
               "kamanjab", "andersson", "okaukuejo", "halali", "namutoni",
               "lindequist", "onguma", "ccf"]

TITULOS_LEYENDA_ALT = [
    (("desierto",), "El desierto"),
    (("costa",), "La costa y el Skeleton Coast"),
    (("damaraland",), "Damaraland"),
    (("etosha",), "Etosha"),
    (("llegada", "vuelta"), "El CCF y la vuelta a Windhoek"),
]

TEXTO_ROTULO_ALT = _rotulos(trazado.ETAPAS_ALT)
BLOQUES_LEYENDA_ALT = _leyenda(trazado.ETAPAS_ALT, TITULOS_LEYENDA_ALT)


def situacion(L, x, y, ancho):
    """Mapa de situacion: Namibia entera y, encima, el recuadro de lo que se esta viendo.

    El mapa grande esta recortado al norte, que es por donde va la ruta. Sin esta
    esquina no se ve que el viaje ocupa media Namibia y deja el sur fuera.
    """
    m = Lienzo(sur=-29.0, oeste=11.6, norte=-16.9, este=25.4, ancho=ancho)
    piezas = [f'<g transform="translate({x:.0f} {y:.0f})">',
              f'<rect x="-6" y="-6" width="{ancho + 12:.0f}" height="{m.alto + 26:.0f}" rx="5" '
              f'fill="{C["papel"]}" opacity=".93" stroke="{C["borde"]}" stroke-width=".8"/>',
              f'<rect width="{ancho:.0f}" height="{m.alto:.0f}" fill="{C["mar"]}"/>',
              capa_paises(m)]
    # el recuadro de lo que se ve en el mapa grande
    x0, y0 = m.xy(L.norte, L.oeste)
    x1, y1 = m.xy(L.sur, L.este)
    piezas.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" '
                  f'fill="none" stroke="{C["oxido"]}" stroke-width="1.8"/>')
    piezas.append(capa_ruta(m, ancho=1.4, halo=False))
    piezas.append(f'<text x="{ancho / 2:.0f}" y="{m.alto + 16:.0f}" text-anchor="middle" '
                  f'font-size="8" fill="{C["tinta2"]}" font-weight="600">'
                  f'El viaje, sobre Namibia entera</text>')
    piezas.append("</g>")
    return "".join(piezas)


def _kms(fichero="ruta.json"):
    return {e["id"]: e.get("km") for e in carga(fichero)}


def mapa_ruta(ancho=1000):
    """La ruta oficial, la del `01`."""
    return _mapa_ruta(ancho, "ruta.json", EN_MAPA_RUTA, TEXTO_ROTULO, BLOQUES_LEYENDA)


def mapa_ruta_alt(ancho=1000):
    """La variante del `aparte/decision-del-ccf`. Mismo encuadre que el oficial a proposito: los dos mapas se
    comparan poniendolos uno al lado del otro, y para eso tienen que estar a la misma
    escala y con el mismo recorte."""
    return _mapa_ruta(ancho, "ruta-alt.json", EN_MAPA_ALT, TEXTO_ROTULO_ALT,
                      BLOQUES_LEYENDA_ALT, ROTULOS_ALT)


def _mapa_ruta(ancho, fichero, en_mapa, textos, bloques, mueve=None):
    # El encuadre esta elegido para que el mapa quepa a ancho de caja en una pagina
    # A4 junto con el titular y el pie: proporcion alto/ancho ~1,25.
    L = Lienzo(sur=-25.05, oeste=12.62, norte=-18.32, este=18.42, ancho=ancho, margen=0)
    km = _kms(fichero)
    total = sum(v for v in km.values() if v)

    cuerpo = [capa_paises(L)]
    cuerpo.append(capa_parques(L, ["Namib-Naukluft", "Skeleton Coast", "Dorob", "Etosha"]))
    cuerpo.append(capa_pan(L))
    cuerpo.append(tropico(L))
    cuerpo.append(capa_ruta(L, ancho=3.6, fichero=fichero))

    # rotulos de los paises vecinos, en gris y en versalita
    for nom, lat, lon in [("ANGOLA", -17.15, 15.6), ("BOTSUANA", -20.4, 21.6),
                          ("SUDÁFRICA", -25.15, 19.6), ("ZAMBIA", -17.35, 24.2)]:
        x, y = L.xy(lat, lon)
        if 0 < x < L.ancho and 0 < y < L.alto:
            cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="11" fill="{C["tinta3"]}" '
                          f'letter-spacing="2.2" font-weight="600" opacity=".8">{nom}</text>')
    x, y = L.xy(-22.4, 13.05)
    cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12" fill="{C["mar2"]}" '
                  f'letter-spacing="3" font-style="italic" font-weight="600" '
                  f'transform="rotate(-90 {x:.0f} {y:.0f})">OCÉANO ATLÁNTICO</text>')

    # nombres de los parques
    for texto, lat, lon, rot in [("Parque Nacional de Etosha", -19.44, 16.55, 0),
                                 ("Namib-Naukluft", -24.15, 15.05, -62),
                                 ("Costa de los Esqueletos", -20.75, 13.15, -68)]:
        x, y = L.xy(lat, lon)
        cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="8.6" fill="{C["parqueb"]}" '
                      f'font-weight="700" letter-spacing=".6" text-anchor="middle" '
                      f'transform="rotate({rot} {x:.0f} {y:.0f})">{esc(texto)}</text>')
    x, y = L.xy(-18.83, 16.32)
    cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="8" fill="{C["tinta3"]}" '
                  f'font-style="italic" text-anchor="middle">depresión de Etosha</text>')

    sitios = dict(ROTULOS_RUTA, **(mueve or {}))
    for clave in en_mapa:
        dx, dy, anc = sitios[clave]
        cuerpo.append(punto(L, clave, textos.get(clave), dx, dy, anc,
                            tam=9.6 if clave in textos else 8.4))

    cuerpo.append(escala(L, 42, L.alto - 42, 200))
    cuerpo.append(norte(L.ancho - 46, 52))

    # ---- leyenda ----
    lx, ly = 40, 46
    ln = [f'<rect x="{lx - 12}" y="{ly - 26}" width="290" height="{34 + 21 * len(bloques)}" '
          f'rx="6" fill="{C["papel"]}" opacity=".93" stroke="{C["borde"]}" stroke-width=".8"/>',
          f'<text x="{lx}" y="{ly - 8}" font-size="12.5" font-weight="800" fill="{C["tinta"]}">'
          f'~{total:,.0f}'.replace(",", ".") + ' km en 15 días</text>']
    for i, (bloque, nombre, dias) in enumerate(bloques):
        y0 = ly + 14 + i * 21
        ln.append(f'<line x1="{lx}" y1="{y0}" x2="{lx + 26}" y2="{y0}" '
                  f'stroke="{trazado.COLOR_BLOQUE[bloque]}" stroke-width="4" stroke-linecap="round"/>')
        ln.append(f'<text x="{lx + 34}" y="{y0 + 3.6}" font-size="9.6" fill="{C["tinta"]}" '
                  f'font-weight="600">{esc(nombre)}</text>')
        ln.append(f'<text x="{lx + 266}" y="{y0 + 3.6}" font-size="9" fill="{C["tinta3"]}" '
                  f'text-anchor="end">{dias}</text>')
    cuerpo.append("".join(ln))

    # ---- simbolos ----
    sx, sy = 40, ly + 26 + 21 * len(bloques)
    sim = [f'<rect x="{sx - 12}" y="{sy - 14}" width="290" height="76" rx="6" '
           f'fill="{C["papel"]}" opacity=".93" stroke="{C["borde"]}" stroke-width=".8"/>']
    for i, (col, forma, txt) in enumerate([
            (C["oxido"], "anillo", "Donde se duerme"),
            (C["rojo"], "rombo", "Puerta de parque con horario"),
            (C["verde"], "punto", "Gasolinera de parada obligada"),
    ]):
        y0 = sy + 4 + i * 20
        if forma == "anillo":
            sim.append(f'<circle cx="{sx + 8}" cy="{y0}" r="5.2" fill="{col}"/>'
                       f'<circle cx="{sx + 8}" cy="{y0}" r="2.8" fill="{C["papel"]}"/>')
        elif forma == "rombo":
            sim.append(f'<rect x="{sx + 4}" y="{y0 - 4}" width="8" height="8" fill="{col}" '
                       f'transform="rotate(45 {sx + 8} {y0})"/>')
        else:
            sim.append(f'<circle cx="{sx + 8}" cy="{y0}" r="3.6" fill="{col}"/>')
        sim.append(f'<text x="{sx + 26}" y="{y0 + 3.4}" font-size="9.4" fill="{C["tinta"]}">{esc(txt)}</text>')
    cuerpo.append("".join(sim))

    cuerpo.append(situacion(L, L.ancho - 178, L.alto - 208, 158))
    cuerpo.append(f'<text x="{L.ancho - 14}" y="{L.alto - 12}" text-anchor="end" font-size="7.6" '
                  f'fill="{C["tinta3"]}">Contornos: Natural Earth (dominio público) · '
                  f'trazado de carretera: OSRM sobre OpenStreetMap (ODbL)</text>')

    return envoltorio(L.ancho, L.alto, "".join(cuerpo))


# ---------------------------------------------------------------------------
# Mapa 1b · la lámina: la ruta entera POR FIRME, con carreteras, distancias y gasolineras
# ---------------------------------------------------------------------------
#
# Mismo encuadre y mismos puntos que el mapa de la ruta, pero la linea no dice en que
# bloque del viaje estas —eso ya lo dice la tira de etapas de la lamina— sino sobre que
# ruedas: asfalto, grava (tierra), sal compactada, pista de parque y los ~5 km de arena
# de Sossusvlei. Encima, el numero de cada carretera en escudo, la distancia entre
# paradas medida sobre la propia geometria de OSRM, y las gasolineras del `01` con su
# estado. Nada se escribe a mano: si cambia una noche, cambia la lamina.

COLOR_FIRME["arena"] = "#D9A441"
NOMBRE_FIRME["arena"] = "arena"


def _hav(a, b):
    """Kilometros entre dos (lat, lon)."""
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def _acumulado(pts):
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + _hav(pts[i - 1], pts[i]))
    return cum


def _indice_a(cum, km, desde=0, hasta=None):
    """El vertice de la polilinea que cae mas cerca del kilometro `km`."""
    hasta = len(cum) if hasta is None else hasta
    return min(range(desde, hasta), key=lambda k: abs(cum[k] - km))


def _rumbo(pts, j, paso=3):
    """Vector unitario de avance en el vertice j, promediando unos vertices a cada lado."""
    a = pts[max(0, j - paso)]
    b = pts[min(len(pts) - 1, j + paso)]
    dx, dy = (b[1] - a[1]) * math.cos(math.radians(a[0])), -(b[0] - a[0])
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n


def capa_ruta_firme(L, ancho=3.6):
    """La ruta entera pintada por firme, tramo a tramo, desde geo/tramos.json.

    Todos los halos van primero y todos los colores despues: si no, el halo de un tramo
    tapa el color del anterior en cada empalme.
    """
    tramos = [t for e in carga("tramos.json") for t in e["tramos"] if len(t["geometria"]) > 1]
    out = []
    for t in tramos:
        d = L.d([(p[1], p[0]) for p in t["geometria"]])
        out.append(f'<path d="{d}" fill="none" stroke="{C["papel"]}" '
                   f'stroke-width="{ancho + 2.2}" stroke-linecap="round" '
                   f'stroke-linejoin="round" opacity=".85"/>')
    for t in tramos:
        d = L.d([(p[1], p[0]) for p in t["geometria"]])
        col = COLOR_FIRME[t["firme"] or "urbano"]
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{ancho}" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)


def arena_sossusvlei():
    """Los ~5 km de arena blanda que OSRM no enruta: del aparcamiento 2WD —donde acaba
    el asfalto del D4— a Sossusvlei y a Deadvlei. Es el unico firme del viaje que no sale
    del enrutado, y por eso es el unico que se traza recto entre dos puntos conocidos."""
    d4 = next((e for e in carga("tramos.json") if e["id"] == "D4"), None)
    if not d4 or not d4["tramos"]:
        return []
    asfalto = max(d4["tramos"], key=lambda t: t["km"])
    lon, lat = asfalto["geometria"][-1]
    fin = (lat, lon)
    return [[fin, trazado.PUNTOS["sossusvlei"][:2]], [fin, trazado.PUNTOS["deadvlei"][:2]]]


def capa_arena(L, ancho=3.6):
    out = []
    for seg in arena_sossusvlei():
        d = L.d(seg)
        out.append(f'<path d="{d}" fill="none" stroke="{C["papel"]}" stroke-width="{ancho + 2.2}" '
                   f'stroke-linecap="round" opacity=".85"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{COLOR_FIRME["arena"]}" '
                   f'stroke-width="{ancho}" stroke-linecap="round" stroke-dasharray="4 3"/>')
    return "".join(out)


# El numero de carretera que se rotula: la B1 dentro de Windhoek va como A1 en OSM y la
# C24 lleva tambien M47. Lo que no tiene numero (pistas de parque, la carretera de
# Sossusvlei) no lleva escudo: ya lo dicen el color y el nombre de la parada.
REF_ROTULO = {"A1": "B1", "M47": "C24"}


def _carreteras(min_km=20):
    """Tramos seguidos con el mismo numero de carretera, por dia: [{ref, km, pts}]."""
    runs = []
    for e in carga("tramos.json"):
        for t in e["tramos"]:
            ref = (t["ref"] or "").split(";")[0].strip()
            ref = REF_ROTULO.get(ref, ref)
            pts = [(p[1], p[0]) for p in t["geometria"]]
            if runs and runs[-1]["ref"] == ref and runs[-1]["dia"] == e["id"]:
                runs[-1]["km"] += t["km"]
                runs[-1]["pts"].extend(pts)
            else:
                runs.append({"dia": e["id"], "ref": ref, "km": t["km"], "pts": pts})
    return [r for r in runs if r["ref"] and r["km"] >= min_km]


# Escudo por letra: las B (asfalto) en negativo, las C y D en claro.
ESCUDO = {"B": (C["tinta"], C["papel"], C["tinta"]),
          "C": (C["papel"], C["tinta"], C["tinta"]),
          "D": (C["papel"], C["tinta2"], C["tinta3"])}

# Escudos que hay que apartar a mano para que no pisen un rotulo: (ref, indice) -> (dx, dy).
DESVIO_ESCUDO = {}


def escudo(L, ref, lat, lon, dx=0, dy=0, tam=8.2):
    fondo, texto, borde = ESCUDO.get(ref[:1], ESCUDO["C"])
    x, y = L.xy(lat, lon)
    x, y = x + dx, y + dy
    w, h = 6 + 5.2 * len(ref), 11.4
    return (f'<g><rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h}" '
            f'rx="2.2" fill="{fondo}" stroke="{borde}" stroke-width=".9"/>'
            f'<text x="{x:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-size="{tam}" '
            f'font-weight="700" fill="{texto}">{esc(ref)}</text></g>')


def rotulos_carreteras(L, cada_km=150, separa_km=60):
    """Un escudo por carretera, en mitad de cada tramo largo; en los muy largos, uno cada
    ~150 km. La misma carretera no se rotula dos veces a menos de 60 km: la C19 y la
    C14 se pisan dos dias, y el escudo es el mismo."""
    puestos = []
    out = []
    for r in _carreteras():
        cum = _acumulado(r["pts"])
        n = max(1, round(cum[-1] / cada_km))
        for i in range(n):
            j = _indice_a(cum, cum[-1] * (i + 0.5) / n)
            lat, lon = r["pts"][j]
            if lat > -19.5 and 15.5 < lon < 17.2:          # dentro de Etosha: sin escudo
                continue
            if any(p[0] == r["ref"] and _hav((lat, lon), p[1:]) < separa_km for p in puestos):
                continue
            puestos.append((r["ref"], lat, lon))
            dx, dy = DESVIO_ESCUDO.get((r["ref"], len([p for p in puestos if p[0] == r["ref"]]) - 1), (0, 0))
            out.append(escudo(L, r["ref"], lat, lon, dx, dy))
    return "".join(out)


def tramos_entre_paradas(fichero="ruta.json", min_km=25):
    """La distancia entre puntos de paso consecutivos, medida sobre la geometria de OSRM.

    Devuelve [(a, b, km, (lat, lon), (ux, uy))]: el par, los kilometros, el punto de la
    polilinea donde poner el rotulo y el rumbo alli. Cada par se rotula una vez aunque
    se pise dos dias (Solitaire–Sesriem, Chudob–Namutoni), y en un dia que vuelve a
    donde salio (la excursion de Sossusvlei) el tramo de vuelta no se rotula: iria
    encima del de ida.
    """
    vistos, salida = set(), []
    for e in carga(fichero):
        g = e.get("geometria") or []
        if len(g) < 2 or len(e["por"]) < 2:
            continue
        pts = [(p[1], p[0]) for p in g]
        cum = _acumulado(pts)
        idx, prev = [], 0
        for clave in e["por"]:
            lat, lon = trazado.PUNTOS[clave][:2]
            j = min(range(prev, len(pts)), key=lambda k: _hav(pts[k], (lat, lon)))
            idx.append(j)
            prev = j
        # un puerto de montana (clase «paso») no corta la distancia si no se duerme en el:
        # Palmwag → Hoada son 52 km, no «26 + 26» con el escudo del C40 en medio
        paradas = [(c, idx[k]) for k, c in enumerate(e["por"])
                   if trazado.PUNTOS[c][3] != "paso" or c == e.get("duerme")]
        for i in range(len(paradas) - 1):
            (a, ja), (b, jb) = paradas[i], paradas[i + 1]
            km = cum[jb] - cum[ja]
            par = tuple(sorted((a, b)))
            vuelta = b == e["por"][0] and e.get("duerme") == b
            if par in vistos or km < min_km or vuelta:
                continue
            vistos.add(par)
            # al 33 % del tramo, para no caer sobre el escudo, que va al 50 % de su carretera
            j = _indice_a(cum, cum[ja] + km * 0.33, ja, jb + 1)
            salida.append((a, b, km, pts[j], _rumbo(pts, j)))
    return salida


# Rotulos de distancia que hay que mover a mano: (a, b) -> (dx, dy) extra.
DESVIO_DISTANCIA = {("walvisbay", "swakopmund"): (26, 4),
                    ("spreetshoogte", "solitaire"): (30, 10),
                    ("twyfelfontein", "palmwag"): (14, 14),
                    ("terracebay", "springbokwasser"): (-8, 16)}


def rotulos_distancias(L, aparta=10, tam=7.8):
    out = []
    for a, b, km, (lat, lon), (ux, uy) in tramos_entre_paradas():
        x, y = L.xy(lat, lon)
        # a la izquierda del sentido de la marcha, apartado de la linea
        nx, ny = -uy, ux
        dx, dy = DESVIO_DISTANCIA.get((a, b), (0, 0))
        x, y = x + nx * aparta + dx, y + ny * aparta + dy
        out.append(f'<text x="{x:.1f}" y="{y + 2.6:.1f}" text-anchor="middle" font-size="{tam}" '
                   f'font-family="IBM Plex Mono, monospace" font-weight="600" fill="{C["tinta2"]}" '
                   f'paint-order="stroke" stroke="{C["papel"]}" stroke-width="2.6" '
                   f'stroke-linejoin="round">{km:.0f} km</text>')
    return "".join(out)


# Donde va el surtidor respecto al punto, para no pisar el rotulo del pueblo
# (los rotulos van a un lado; el surtidor, al otro). clave -> (dx, dy).
POS_GASOLINERA = {
    "windhoek": (-12, -12), "solitaire": (10, -10), "sesriem": (10, -11),
    "walvisbay": (10, -11), "swakopmund": (10, -11), "hentiesbay": (10, -11),
    "terracebay": (10, -11), "twyfelfontein": (-10, -12), "palmwag": (-12, 9),
    "kamanjab": (10, -11), "outjo": (-11, -11), "okaukuejo": (10, -11),
    "halali": (12, -3), "namutoni": (-10, 12), "tsumeb": (-10, -11),
    "otjiwarongo": (-11, -11),
}


def surtidor(x, y, estado, escala=1.0):
    """El icono de gasolinera: lleno (obligatoria), vacio (opcional) o tachado (no fiable)."""
    verde = C["verde"]
    if estado == "obligatoria":
        fondo, borde, ventana = verde, verde, C["papel"]
    elif estado == "opcional":
        fondo, borde, ventana = C["papel"], verde, verde
    else:
        fondo, borde, ventana = C["papel"], C["tinta3"], C["tinta3"]
    g = [f'<g transform="translate({x:.1f} {y:.1f}) scale({escala})">',
         f'<rect x="-4.8" y="-5.6" width="7.4" height="11.2" rx="1.4" fill="{fondo}" '
         f'stroke="{borde}" stroke-width="1.3"/>',
         f'<rect x="-3.3" y="-4" width="4.4" height="3.3" rx=".5" fill="{ventana}" opacity=".9"/>',
         f'<path d="M3 -2.2 h1.7 v6 a1.6 1.6 0 0 1 -3.2 0 v-1.4" fill="none" stroke="{borde}" '
         f'stroke-width="1.2" stroke-linecap="round"/>']
    if estado == "no":
        g.append(f'<line x1="-6.5" y1="7" x2="6.5" y2="-7" stroke="{C["rojo"]}" '
                 f'stroke-width="1.7" stroke-linecap="round"/>')
    g.append("</g>")
    return "".join(g)


def capa_gasolineras(L, escala=1.05):
    out = []
    for clave, estado, _nota in trazado.GASOLINERAS:
        lat, lon = trazado.PUNTOS[clave][:2]
        x, y = L.xy(lat, lon)
        dx, dy = POS_GASOLINERA.get(clave, (10, -11))
        out.append(surtidor(x + dx, y + dy, estado, escala))
    return "".join(out)


def leyenda_lamina(L, total, lx=40, fondo=None):
    """La leyenda de la lamina: el firme, los simbolos y las gasolineras por estado.
    Va ABAJO a la izquierda, sobre el mar y encima de la barra de escala: arriba tapaba
    Hoada, Palmwag y el paso de Grootberg."""
    paso = 19
    filas = [("linea", COLOR_FIRME["asfalto"], "Asfalto · 100 km/h de planificación", None),
             ("linea", COLOR_FIRME["grava"], "Tierra (grava) · 80, techo del contrato", None),
             ("linea", COLOR_FIRME["sal"], "Sal compactada · como grava", None),
             ("linea", COLOR_FIRME["parque"], "Pista de parque · 60", None),
             ("arena", COLOR_FIRME["arena"], "Arena · los ~5 km finales a Sossusvlei y Deadvlei", None),
             ("escudo", None, "Número de carretera (B asfalto · C y D tierra)", None),
             ("km", None, "Distancia entre paradas, sobre el enrutado", None),
             ("anillo", C["oxido"], "Donde se duerme, con sus días", None),
             ("rombo", C["rojo"], "Puerta de parque con horario", None),
             ("surtidor", "obligatoria", "Gasolinera OBLIGATORIA: se llena, marque lo que marque", None),
             ("surtidor", "opcional", "Gasolinera opcional: conviene, no hace falta", None),
             ("surtidor", "no", "Surtidor sin garantía: no cuentes con él", None)]
    alto = 40 + paso * len(filas)
    ly = L.alto - 64 - alto + 26                 # la caja acaba 64 unidades sobre el borde
    out = [f'<rect x="{lx - 12}" y="{ly - 26}" width="330" height="{alto}" rx="6" '
           f'fill="{C["papel"]}" opacity=".94" stroke="{C["borde"]}" stroke-width=".8"/>',
           f'<text x="{lx}" y="{ly - 8}" font-size="12.5" font-weight="800" fill="{C["tinta"]}">'
           f'~{total:,.0f}'.replace(",", ".") + ' km en 15 días · por firme</text>']
    for i, (tipo, col, txt, _) in enumerate(filas):
        y0 = ly + 14 + i * paso
        cx = lx + 13
        if tipo == "linea":
            out.append(f'<line x1="{lx}" y1="{y0}" x2="{lx + 26}" y2="{y0}" stroke="{col}" '
                       f'stroke-width="4" stroke-linecap="round"/>')
        elif tipo == "arena":
            out.append(f'<line x1="{lx}" y1="{y0}" x2="{lx + 26}" y2="{y0}" stroke="{col}" '
                       f'stroke-width="4" stroke-linecap="round" stroke-dasharray="4 3"/>')
        elif tipo == "escudo":
            fondo, texto, borde = ESCUDO["C"]
            out.append(f'<rect x="{cx - 10.5}" y="{y0 - 5.7}" width="21" height="11.4" rx="2.2" '
                       f'fill="{fondo}" stroke="{borde}" stroke-width=".9"/>'
                       f'<text x="{cx}" y="{y0 + 3}" text-anchor="middle" font-size="8.2" '
                       f'font-weight="700" fill="{texto}">C14</text>')
        elif tipo == "km":
            out.append(f'<text x="{cx}" y="{y0 + 2.6}" text-anchor="middle" font-size="7.8" '
                       f'font-family="IBM Plex Mono, monospace" font-weight="600" '
                       f'fill="{C["tinta2"]}">84 km</text>')
        elif tipo == "anillo":
            out.append(f'<circle cx="{cx}" cy="{y0}" r="5.2" fill="{col}"/>'
                       f'<circle cx="{cx}" cy="{y0}" r="2.8" fill="{C["papel"]}"/>')
        elif tipo == "rombo":
            out.append(f'<rect x="{cx - 4}" y="{y0 - 4}" width="8" height="8" fill="{col}" '
                       f'transform="rotate(45 {cx} {y0})"/>')
        else:
            out.append(surtidor(cx, y0, col, 0.95))
        out.append(f'<text x="{lx + 34}" y="{y0 + 3.4}" font-size="9.2" fill="{C["tinta"]}">'
                   f'{esc(txt)}</text>')
    return "".join(out)


def mapa_lamina(ancho=1100):
    """El mapa de la lamina A2: la ruta oficial por firme, con carreteras, distancias y
    gasolineras. Mismo encuadre que `mapa_ruta`."""
    L = Lienzo(sur=-25.05, oeste=12.62, norte=-18.32, este=18.42, ancho=ancho, margen=0)
    km = _kms("ruta.json")
    total = sum(v for v in km.values() if v)

    cuerpo = [capa_paises(L)]
    cuerpo.append(capa_parques(L, ["Namib-Naukluft", "Skeleton Coast", "Dorob", "Etosha"]))
    cuerpo.append(capa_pan(L))
    cuerpo.append(tropico(L))
    cuerpo.append(capa_ruta_firme(L, ancho=3.8))
    cuerpo.append(capa_arena(L, ancho=3.8))

    for nom, lat, lon in [("ANGOLA", -17.15, 15.6), ("BOTSUANA", -20.4, 21.6),
                          ("SUDÁFRICA", -25.15, 19.6), ("ZAMBIA", -17.35, 24.2)]:
        x, y = L.xy(lat, lon)
        if 0 < x < L.ancho and 0 < y < L.alto:
            cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="11" fill="{C["tinta3"]}" '
                          f'letter-spacing="2.2" font-weight="600" opacity=".8">{nom}</text>')
    x, y = L.xy(-22.4, 13.05)
    cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12" fill="{C["mar2"]}" '
                  f'letter-spacing="3" font-style="italic" font-weight="600" '
                  f'transform="rotate(-90 {x:.0f} {y:.0f})">OCÉANO ATLÁNTICO</text>')
    for texto, lat, lon, rot in [("Parque Nacional de Etosha", -19.44, 16.55, 0),
                                 ("Namib-Naukluft", -24.15, 15.05, -62),
                                 ("Costa de los Esqueletos", -20.75, 13.15, -68)]:
        x, y = L.xy(lat, lon)
        cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="8.6" fill="{C["parqueb"]}" '
                      f'font-weight="700" letter-spacing=".6" text-anchor="middle" '
                      f'transform="rotate({rot} {x:.0f} {y:.0f})">{esc(texto)}</text>')
    x, y = L.xy(-18.83, 16.32)
    cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="8" fill="{C["tinta3"]}" '
                  f'font-style="italic" text-anchor="middle">depresión de Etosha</text>')

    cuerpo.append(rotulos_carreteras(L))
    cuerpo.append(rotulos_distancias(L))
    # las gasolineras dejan de ser una clase de punto: el surtidor las cuenta aparte
    for clave in EN_MAPA_RUTA:
        dx, dy, anc = ROTULOS_RUTA[clave]
        cl = "ciudad" if trazado.PUNTOS[clave][3] == "combu" else None
        cuerpo.append(punto(L, clave, TEXTO_ROTULO.get(clave), dx, dy, anc,
                            tam=9.6 if clave in TEXTO_ROTULO else 8.4, clase=cl))
    cuerpo.append(capa_gasolineras(L))

    cuerpo.append(escala(L, 42, L.alto - 42, 200))
    cuerpo.append(norte(L.ancho - 46, 52))
    cuerpo.append(leyenda_lamina(L, total))
    cuerpo.append(situacion(L, L.ancho - 178, L.alto - 208, 158))
    cuerpo.append(f'<text x="{L.ancho - 14}" y="{L.alto - 12}" text-anchor="end" font-size="7.6" '
                  f'fill="{C["tinta3"]}">Contornos: Natural Earth (dominio público) · '
                  f'trazado, carreteras y distancias: OSRM sobre OpenStreetMap (ODbL) · '
                  f'firme: `trazado.FIRME` · gasolineras: `01` §gasolineras</text>')
    return envoltorio(L.ancho, L.alto, "".join(cuerpo))


# ---------------------------------------------------------------------------
# Mapa 2 · Etosha, charca a charca
# ---------------------------------------------------------------------------

import re as _re


def charcas():
    """Las charcas con nombre de Etosha, sacadas de OpenStreetMap.

    Devuelve (nombre, lat, lon, artificial). `artificial` distingue el sondeo con
    bomba de la fuente natural — que en seca es la diferencia entre tener agua o no.
    """
    fuera = set()
    salida = {}
    for e in carga("etosha_puntos.json")["elements"]:
        t = e.get("tags", {})
        n = t.get("name", "")
        if not n:
            continue
        pinta = (t.get("natural") in ("water", "waterhole", "spring")
                 or "waterhole" in n.lower() or "water point" in n.lower()
                 or "wateringhole" in n.lower())
        if not pinta:
            continue
        artificial = bool(_re.search(r"man[- ]?made", n, _re.I))
        limpio = _re.sub(r"\s*\((natural |man[- ]?made )?water\s*(hole|point)?\)", "", n, flags=_re.I)
        limpio = _re.sub(r"\s*\(man[- ]?made\)", "", limpio, flags=_re.I)
        limpio = _re.sub(r"\s*(Waterhole|Wateringhole)\s*$", "", limpio, flags=_re.I).strip()
        if not limpio or limpio.lower() in fuera:
            continue
        lat = e.get("lat") or e.get("center", {}).get("lat")
        lon = e.get("lon") or e.get("center", {}).get("lon")
        if lat is None:
            continue
        salida.setdefault(limpio.lower(), (limpio, lat, lon, artificial))
    return sorted(salida.values(), key=lambda x: x[0])


# Las que el dossier nombra en el dia a dia: van rotuladas y en grande.
CHARCAS_CLAVE = {
    "okaukuejo", "moringa", "chudob", "klein namutoni", "nebrowni", "gemsbokvlakte",
    "olifantsbad", "aus", "homob", "sueda", "salvadora", "charitsaub", "rietfontein",
    "goas", "noniams", "nuamses", "springbokfontein", "okerfontein", "ngobib", "batia",
    "koinachas", "groot okevi", "klein okevi", "kalkheuwel", "twee palms", "tsumcor",
    "andoni", "okondeka", "ondongab", "kapupuhedi", "ombika", "helio",
}

# Rotulos que hay que apartar para que no choquen entre si.
DESVIO_CHARCA = {
    "ombika": (0, 12, "middle"),
    "nebrowni": (8, 7, "start"), "gemsbokvlakte": (0, 12, "middle"),
    "olifantsbad": (7, 3, "start"), "aus": (7, -3, "start"),
    "homob": (-6, 3, "end"), "ondongab": (7, -4, "start"),
    "kapupuhedi": (-7, 1, "end"), "sueda": (-7, -3, "end"),
    "salvadora": (0, -8, "middle"), "charitsaub": (-2, 12, "middle"),
    "rietfontein": (8, -5, "start"), "moringa": (-8, -3, "end"),
    "helio": (7, 5, "start"), "noniams": (7, 3, "start"),
    "goas": (7, 2, "start"), "nuamses": (-6, 3, "end"),
    "springbokfontein": (0, -8, "middle"), "okerfontein": (7, 3, "start"),
    "ngobib": (-6, 3, "end"), "batia": (0, 11, "middle"),
    "kalkheuwel": (0, 12, "middle"), "chudob": (8, 8, "start"),
    "klein namutoni": (-8, 11, "end"), "koinachas": (-8, -4, "end"),
    "groot okevi": (8, 2, "start"), "klein okevi": (8, 9, "start"),
    "twee palms": (7, -4, "start"), "tsumcor": (0, -8, "middle"),
    "andoni": (7, 3, "start"), "okondeka": (7, 3, "start"),
}

# La charca del propio campamento no se rotula: la tapa el nombre del campamento.
SIN_ROTULO = {"okaukuejo", "ombika", "groot okevi", "klein okevi", "koinachas",
              "kalkheuwel", "helio"}


def mapa_etosha(ancho=1000):
    L = Lienzo(sur=-19.47, oeste=15.50, norte=-18.48, este=17.32, ancho=ancho, margen=0)

    cuerpo = [f'<rect width="{L.ancho}" height="{L.alto:.0f}" fill="{C["tierra"]}"/>']
    cuerpo.append(capa_parques(L, ["Etosha"], relleno=C["parque"], ancho=1.4, guion="6 4"))
    cuerpo.append(capa_pan(L, borde=1.0))

    # pistas del parque, finas y en gris: dan contexto sin robar protagonismo
    pistas = []
    for w in carga("etosha_pistas.json")["elements"]:
        g = w.get("geometry")
        if not g or len(g) < 2:
            continue
        pistas.append(L.d([(p["lat"], p["lon"]) for p in g]))
    cuerpo.append(f'<path d="{"".join(pistas)}" fill="none" stroke="{C["borde"]}" '
                  f'stroke-width=".9" stroke-linecap="round" opacity=".85"/>')

    cuerpo.append(capa_ruta(L, etapas=["D10", "D11", "D12", "D13", "D14"], ancho=3.2))

    x, y = L.xy(-18.83, 16.28)
    cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="15" fill="{C["tinta3"]}" '
                  f'text-anchor="middle" letter-spacing="3" font-style="italic">'
                  f'DEPRESIÓN DE ETOSHA</text>')
    x, y = L.xy(-18.90, 16.28)
    cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="9" fill="{C["tinta3"]}" '
                  f'text-anchor="middle" font-style="italic">'
                  f'~4.800 km² de arcilla y sal · seca en noviembre</text>')

    # ---- charcas ----
    for nombre, lat, lon, artificial in charcas():
        clave = nombre.lower()
        px, py = L.xy(lat, lon)
        if not (-20 < px < L.ancho + 20 and -20 < py < L.alto + 20):
            continue
        clave_corta = clave.replace("nebrowni waterhole (man-made)", "nebrowni")
        es_clave = any(k in clave_corta for k in CHARCAS_CLAVE)
        r = 4.0 if es_clave else 2.4
        relleno = "#2F6E8E" if not artificial else C["papel"]
        cuerpo.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{relleno}" '
                      f'stroke="#2F6E8E" stroke-width="1.5"/>')
        if not es_clave or clave_corta in SIN_ROTULO:
            continue
        dx, dy, anc = DESVIO_CHARCA.get(
            next((k for k in DESVIO_CHARCA if k in clave_corta), ""), (6, 3, "start"))
        etiqueta = _re.sub(r"\s*Waterhole.*", "", nombre)
        cuerpo.append(f'<text x="{px + dx:.1f}" y="{py + dy:.1f}" text-anchor="{anc}" '
                      f'font-size="9" font-weight="600" fill="#20536B" paint-order="stroke" '
                      f'stroke="{C["parque"]}" stroke-width="2.4" stroke-linejoin="round">'
                      f'{esc(etiqueta)}</text>')

    # ---- campamentos y puertas ----
    for clave, dx, dy, anc, txt in [
            # los dias salen de las etapas: escritos a mano se quedaron viejos una vez
            ("okaukuejo", 0, -16, "middle", "OKAUKUEJO · " + _noches("okaukuejo")),
            ("halali", 0, -16, "middle", "HALALI · " + _noches("halali")),
            ("namutoni", -40, -6, "end", "NAMUTONI"),          # se visita, no se duerme
            ("onguma", 12, -4, "start", "ONGUMA · " + _noches("onguma")),
            ("andersson", -9, 4, "end", "Puerta de Andersson"),
            ("lindequist", 11, 22, "start", "Von Lindequist"),
    ]:
        cuerpo.append(punto(L, clave, txt, dx, dy, anc, tam=11.5))

    # ---- leyenda ----
    lx, ly = 28, 40
    ln = [f'<rect x="{lx - 10}" y="{ly - 18}" width="272" height="128" rx="6" '
          f'fill="{C["papel"]}" opacity=".95" stroke="{C["borde"]}" stroke-width=".8"/>',
          f'<text x="{lx}" y="{ly}" font-size="12.5" font-weight="800" fill="{C["tinta"]}">'
          f'Las charcas son el safari</text>',
          f'<text x="{lx}" y="{ly + 15}" font-size="8.6" fill="{C["tinta2"]}">'
          f'En seca la fauna va al agua: se elige una y se espera.</text>']
    for i, (tipo, txt) in enumerate([
            ("natural", "Charca natural"),
            ("bomba", "Sondeo con bomba — el que aguanta en seca"),
            ("campa", "Campamento donde se duerme"),
            ("puerta", "Puerta con horario"),
    ]):
        y0 = ly + 34 + i * 18
        if tipo == "natural":
            ln.append(f'<circle cx="{lx + 7}" cy="{y0 - 3}" r="4" fill="#2F6E8E" stroke="#2F6E8E" stroke-width="1.5"/>')
        elif tipo == "bomba":
            ln.append(f'<circle cx="{lx + 7}" cy="{y0 - 3}" r="4" fill="{C["papel"]}" stroke="#2F6E8E" stroke-width="1.5"/>')
        elif tipo == "campa":
            ln.append(f'<circle cx="{lx + 7}" cy="{y0 - 3}" r="5.2" fill="{C["oxido"]}"/>'
                      f'<circle cx="{lx + 7}" cy="{y0 - 3}" r="2.8" fill="{C["papel"]}"/>')
        else:
            ln.append(f'<rect x="{lx + 3}" y="{y0 - 7}" width="8" height="8" fill="{C["rojo"]}" '
                      f'transform="rotate(45 {lx + 7} {y0 - 3})"/>')
        ln.append(f'<text x="{lx + 22}" y="{y0}" font-size="9.2" fill="{C["tinta"]}">{esc(txt)}</text>')
    cuerpo.append("".join(ln))

    # La barra de 50 km mide ~450 px a esta escala: se coloca midiendola, no a ojo
    # (con el offset fijo de antes se salia del lienzo y quedaba cortada).
    cuerpo.append(escala(L, L.ancho - 50 / L.km_por_unidad() - 46, L.alto - 42, 50))
    cuerpo.append(norte(L.ancho - 42, 42))
    cuerpo.append(f'<text x="{L.ancho - 14}" y="{L.alto - 10}" text-anchor="end" font-size="7.4" '
                  f'fill="{C["tinta3"]}">Charcas, pistas y límites: OpenStreetMap (ODbL) · '
                  f'trazado: OSRM</text>')

    return envoltorio(L.ancho, L.alto, "".join(cuerpo), fondo=C["tierra"])


# ---------------------------------------------------------------------------
# Exportar a fichero, para el README y para GitHub
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Mapa de las regiones · para la guia de fauna: donde vive cada bicho
# ---------------------------------------------------------------------------

# Las cuatro regiones de Owambo y las dos del Kavango son franjas estrechas y pegadas:
# escribirles el nombre encima las tapa y los rotulos se pisan entre si. Por eso el mapa
# lleva un DISCO NUMERADO en cada una y la lista va aparte, en el hueco de Botsuana, que
# es espacio que el encuadre tiene que reservar igualmente para que quepa la Franja de
# Caprivi. Un par de discos se apartan a mano de su centroide, que cae en un rio.
DISCO_REGION = {"NAM.7_1": (-17.55, 16.30), "NAM.10_1": (-17.85, 15.55),
                "NAM.4_1": (-18.35, 20.10)}


def _centroide(anillo):
    """Centroide de area de un anillo (lat, lon). El de la media de vertices se va al
    lado donde la frontera tiene mas puntos, que en Namibia es siempre el rio."""
    a = cx = cy = 0.0
    for i in range(len(anillo) - 1):
        y0, x0 = anillo[i]
        y1, x1 = anillo[i + 1]
        f = x0 * y1 - x1 * y0
        a += f
        cx += (x0 + x1) * f
        cy += (y0 + y1) * f
    if abs(a) < 1e-12:
        return anillo[0]
    a *= .5
    return (cy / (6 * a), cx / (6 * a))


def _fichas_por_region():
    """Cuantas fichas de la guia tienen su GRUESO de registros en cada region.

    No es «cuantas especies viven ahi» —casi todas viven en varias— sino donde esta el
    grueso de cada una, que es lo que contesta la pregunta util: si quiero ver esto,
    ¿donde tengo que estar?"""
    import catalogo
    import pais
    cuenta = {}
    for _c, _n, lista in catalogo.GRUPOS_FAUNA:
        for slug, *_ in lista:
            d = pais.donde(slug)
            if d and d[1]:
                cuenta[d[1]] = cuenta.get(d[1], 0) + 1
    return cuenta


# Las regiones que la ruta pisa, por su gid de GADM: Khomas (Windhoek), Hardap
# (Sossusvlei), Erongo (la costa), Kunene (Damaraland y el oeste de Etosha), Oshana y
# Oshikoto (el centro y el este del parque) y Otjozondjupa (la vuelta por Otjiwarongo).
REGIONES_DE_LA_RUTA = {"NAM.5_1", "NAM.3_1", "NAM.2_1", "NAM.6_1",
                       "NAM.10_1", "NAM.11_1", "NAM.12_1"}


def mapa_regiones(ancho=1180):
    """Namibia por regiones, con la ruta encima y el recuento de fichas de cada una.

    Es el mapa que hace legible la linea «En Namibia» de cada ficha: sin el, decir que
    el hipopotamo esta en Kavango y el pinguino en ǁKaras no situa nada. Las regiones
    que la ruta pisa van en color y las demas en gris: de un vistazo se ve que el norte
    mojado —donde vive toda la parte 2 de la guia— se queda entero fuera del viaje.
    """
    import pais
    L = Lienzo(sur=-29.10, oeste=11.62, norte=-16.85, este=25.45, ancho=ancho, margen=0)
    cuenta = _fichas_por_region()
    orden = {gid: i + 1 for i, (gid, _n, _a) in enumerate(pais.REGIONES)}

    cuerpo = [capa_paises(L, resaltar=None)]
    centros = {}
    for r in carga("regiones.json")["regiones"]:
        gid = r["gadm"]
        aros = [[tuple(p) for p in a] for a in r["anillos"]]
        d = "".join(L.d(a, cerrar=True) for a in aros if len(a) > 3)
        if not d:
            continue
        dentro = gid in REGIONES_DE_LA_RUTA
        cuerpo.append(f'<path d="{d}" fill="{C["region"] if dentro else C["vecino"]}" '
                      f'stroke="{C["tinta3"]}" stroke-width="{1.4 if dentro else .8}" '
                      f'fill-rule="evenodd" stroke-linejoin="round"/>')
        grande = max(aros, key=len)
        # Kavango son dos poligonos con un solo gid: se queda el mas grande de los dos.
        if gid not in centros or len(grande) > centros[gid][1]:
            centros[gid] = (_centroide(grande), len(grande), dentro)

    cuerpo.append(capa_parques(L, ["Namib-Naukluft", "Skeleton Coast", "Dorob", "Etosha"]))
    cuerpo.append(capa_pan(L))
    cuerpo.append(capa_ruta(L, ancho=3.0))

    for gid, (cen, _n, dentro) in centros.items():
        lat, lon = DISCO_REGION.get(gid, cen)
        x, y = L.xy(lat, lon)
        col = C["oxido"] if dentro else C["tinta3"]
        cuerpo.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{col}" stroke="{C["papel"]}" '
            f'stroke-width="2"/>'
            f'<text x="{x:.0f}" y="{y + 4:.0f}" font-size="12" font-weight="800" '
            f'fill="{C["papel"]}" text-anchor="middle">{orden[gid]}</text>')

    for nom, lat, lon in [("ANGOLA", -17.05, 14.2), ("BOTSUANA", -20.6, 23.6),
                          ("SUDÁFRICA", -28.75, 20.4), ("ZAMBIA", -17.05, 24.6)]:
        x, y = L.xy(lat, lon)
        cuerpo.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="11" fill="{C["tinta3"]}" '
                      f'letter-spacing="2.2" font-weight="600" opacity=".75" '
                      f'text-anchor="middle">{nom}</text>')

    cuerpo.append(escala(L, 44, L.alto - 44, 200))
    cuerpo.append(norte(L.ancho - 48, 54))

    # ---- la lista, en el hueco de Botsuana ----
    lx = L.xy(-21.6, 20.9)[0]
    ly = 205                       # por debajo de la Franja de Caprivi, que llega arriba
    alto_caja = 46 + 20 * len(pais.REGIONES)
    ln = [f'<rect x="{lx - 14}" y="{ly - 30}" width="332" height="{alto_caja}" rx="7" '
          f'fill="{C["papel"]}" opacity=".95" stroke="{C["borde"]}" stroke-width=".9"/>',
          f'<text x="{lx}" y="{ly - 12}" font-size="13" font-weight="800" '
          f'fill="{C["tinta"]}">Las trece regiones, y cuántas fichas</text>',
          f'<text x="{lx}" y="{ly + 2}" font-size="9.6" fill="{C["tinta3"]}">'
          f'tienen aquí su grueso de registros de GBIF</text>']
    for i, (gid, nombre, apodo) in enumerate(pais.REGIONES):
        y0 = ly + 24 + i * 20
        dentro = gid in REGIONES_DE_LA_RUTA
        col = C["oxido"] if dentro else C["tinta3"]
        ln.append(
            f'<circle cx="{lx + 7}" cy="{y0 - 4}" r="7.5" fill="{col}"/>'
            f'<text x="{lx + 7}" y="{y0 - 1}" font-size="9" font-weight="800" '
            f'fill="{C["papel"]}" text-anchor="middle">{i + 1}</text>'
            f'<text x="{lx + 20}" y="{y0}" font-size="10.5" '
            f'font-weight="{700 if dentro else 400}" fill="{C["tinta"]}">'
            f'{esc(nombre)}</text>'
            f'<text x="{lx + 20 + 7.2 * len(nombre)}" y="{y0}" font-size="9.4" '
            f'fill="{C["tinta3"]}"> · {esc(apodo)}</text>'
            f'<text x="{lx + 300}" y="{y0}" font-size="10.5" font-weight="700" '
            f'fill="{col}" text-anchor="end">{cuenta.get(gid, 0)}</text>')
    y0 = ly + 30 + 20 * len(pais.REGIONES)
    ln.append(f'<text x="{lx}" y="{y0}" font-size="9.6" fill="{C["tinta3"]}">'
              f'En NARANJA, las siete regiones que pisa la ruta.</text>')
    cuerpo.append("".join(ln))

    return envoltorio(L.ancho, L.alto, "".join(cuerpo))


def exporta(destino=None):
    """Escribe los mapas en img/mapas/ como SVG y como PNG.

    El PNG es para el README: GitHub renderiza SVG con reservas y los diagramas de
    Mermaid fallan a ratos («Cannot read properties of undefined»), asi que la ruta
    en la portada del repo va como imagen y no como diagrama.
    """
    import subprocess
    import tempfile

    destino = destino or os.path.join(os.path.dirname(HERE), "img", "mapas")
    os.makedirs(destino, exist_ok=True)
    hechos = []
    for nombre, fn, ancho in (("ruta", mapa_ruta, 1100), ("etosha", mapa_etosha, 1500),
                              ("ruta-alternativa", mapa_ruta_alt, 1100),
                              ("regiones", mapa_regiones, 1180)):
        svg = fn(ancho)
        ruta_svg = os.path.join(destino, nombre + ".svg")
        with open(ruta_svg, "w") as f:
            f.write(svg)
        alto = round(float(_re.search(r'viewBox="0 0 [\d.]+ ([\d.]+)"', svg).group(1)))
        import navegador
        chrome = navegador.chrome()
        ruta_png = os.path.join(destino, nombre + ".png")
        if chrome:
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(
                    [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                     f"--user-data-dir={tmp}", "--hide-scrollbars",
                     f"--screenshot={ruta_png}", f"--window-size={ancho},{alto}",
                     "file://" + os.path.abspath(ruta_svg)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        hechos.append((nombre, ruta_svg, ruta_png if os.path.exists(ruta_png) else None))
    return hechos


if __name__ == "__main__":
    for nombre, svg, png in exporta():
        print(f"{nombre:8s} {os.path.relpath(svg, os.path.dirname(HERE))} "
              f"({os.path.getsize(svg) // 1024} KB)"
              + (f" · {os.path.relpath(png, os.path.dirname(HERE))} "
                 f"({os.path.getsize(png) // 1024} KB)" if png else " · sin PNG"))
