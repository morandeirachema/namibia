# -*- coding: utf-8 -*-
"""Los puntos y las etapas de la ruta: la geometria del viaje, en un solo sitio.

Las coordenadas salen de OpenStreetMap (geocodificadas con Nominatim y Overpass,
04/08/2026) y no de estimaciones a ojo. Con ellas, `geodatos.py` le pide a OSRM el
trazado real de carretera de cada dia — lo que ademas sirve de control cruzado de los
kilometros del dossier, que se midieron con otras herramientas.

PUNTOS: clave -> (lat, lon, rotulo, clase). La clase manda en como se pinta:
    parada  · donde se duerme
    hito    · lo que se visita
    puerta  · puerta de parque con horario
    paso    · puerto de montana
    ciudad  · nucleo de referencia
    combu   · gasolinera que el dossier marca como obligatoria
"""

PUNTOS = {
    # --- Windhoek y el eje central ---
    "windhoek":      (-22.57761, 17.07727, "Windhoek", "ciudad"),
    "aeropuerto":    (-22.48220, 17.47205, "Aeropuerto Hosea Kutako", "hito"),
    "rehoboth":      (-23.31510, 17.08170, "Rehoboth", "ciudad"),
    "okahandja":     (-21.97923, 16.91282, "Okahandja", "ciudad"),
    "otjiwarongo":   (-20.46093, 16.65121, "Otjiwarongo", "combu"),
    "tsumeb":        (-19.24672, 17.71622, "Tsumeb", "ciudad"),

    # --- el desierto ---
    "spreetshoogte": (-23.65792, 16.18549, "Paso de Spreetshoogte", "paso"),
    "solitaire":     (-23.89429, 16.00553, "Solitaire", "combu"),
    "sesriem":       (-24.48713, 15.79849, "Sesriem", "parada"),
    "duna45":        (-24.72952, 15.47192, "Duna 45", "hito"),
    "sossusvlei":    (-24.73953, 15.29236, "Sossusvlei", "hito"),
    "deadvlei":      (-24.76299, 15.29440, "Deadvlei", "hito"),

    # --- la costa ---
    "walvisbay":     (-22.95576, 14.50711, "Walvis Bay", "parada"),
    "swakopmund":    (-22.67684, 14.52897, "Swakopmund", "ciudad"),
    "hentiesbay":    (-22.11597, 14.28266, "Henties Bay", "combu"),
    "capecross":     (-21.77145, 13.95196, "Cape Cross", "hito"),
    "ugabmund":      (-21.17270, 13.66950, "Puerta de Ugabmund", "puerta"),
    "torrabay":      (-20.32287, 13.23804, "Torra Bay", "hito"),
    "terracebay":    (-19.98772, 13.03254, "Terrace Bay", "parada"),

    # --- solo en la variante del `aparte/decision-del-ccf`: la vuelta por el CCF en vez de Onguma ---
    "ccf":           (-20.48387, 17.03154, "Cheetah Conservation Fund", "parada"),

    # --- Damaraland ---
    "springbokwasser": (-20.31055, 13.64769, "Puerta de Springbokwasser", "puerta"),
    "twyfelfontein": (-20.54842, 14.41099, "Twyfelfontein", "parada"),
    "khorixas":      (-20.37384, 14.96042, "Khorixas", "ciudad"),
    "palmwag":       (-19.88436, 13.94799, "Palmwag", "hito"),
    "grootberg":     (-19.84295, 14.12820, "Paso de Grootberg", "paso"),
    "hoada":         (-19.73222, 14.30791, "Hoada", "parada"),
    "kamanjab":      (-19.62841, 14.84336, "Kamanjab", "combu"),

    # --- Etosha ---
    "outjo":         (-20.11186, 16.15669, "Outjo", "combu"),
    "andersson":     (-19.33130, 15.94010, "Puerta de Andersson", "puerta"),
    "galton":        (-19.31470, 14.48160, "Puerta de Galton", "puerta"),
    "okaukuejo":     (-19.18080, 15.91790, "Okaukuejo", "parada"),
    "halali":        (-19.03560, 16.47220, "Halali", "parada"),
    "namutoni":      (-18.80590, 16.94050, "Namutoni", "parada"),
    "lindequist":    (-18.80340, 17.04330, "Puerta de Von Lindequist", "puerta"),
    "onguma":        (-18.78191, 17.05919, "Onguma · Tamboti", "parada"),
    "tweepalms":     (-18.76560, 17.02990, "Twee Palms · Fischer's Pan", "hito"),
    "chudob":        (-18.85820, 16.92490, "Chudob", "hito"),
    "gemsbokvlakte": (-19.21340, 16.05830, "Gemsbokvlakte", "hito"),
    "salvadora":     (-19.03460, 16.26970, "Salvadora", "hito"),
    "goas":          (-18.98900, 16.55840, "Goas", "hito"),
}

# Puntos que SOLO existen en la variante del `aparte/decision-del-ccf`. Viven en la misma tabla —para que el
# mapa de la variante los rotule con el mismo codigo— pero NO entran en el GPX ni en el
# KML: esos son de la ruta que se va a conducir, y un waypoint del CCF en el GPS del
# viaje es una invitacion a salir de Etosha por donde no toca.
SOLO_VARIANTE = ("ccf",)


def puntos_oficiales():
    """La tabla de puntos sin los de la variante: lo que llevan el GPS y la lamina."""
    return {k: v for k, v in PUNTOS.items() if k not in SOLO_VARIANTE}


# Cada etapa es un dia. `por` son los puntos por los que OSRM tiene que pasar, en orden.
# `bloque` agrupa por tramo del viaje y decide el color de la linea en el mapa.
ETAPAS = [
    {"id": "D1", "fecha": "31 oct", "bloque": "llegada",
     "titulo": "Llegada, coche y compra en Windhoek", "duerme": "windhoek",
     "por": ["aeropuerto", "windhoek"]},
    {"id": "D2", "fecha": "1 nov", "bloque": "desierto",
     "titulo": "Windhoek → paso de Spreetshoogte", "duerme": "spreetshoogte",
     "por": ["windhoek", "rehoboth", "spreetshoogte"]},
    {"id": "D3", "fecha": "2 nov", "bloque": "desierto",
     "titulo": "Spreetshoogte → Solitaire → Sesriem", "duerme": "sesriem",
     "por": ["spreetshoogte", "solitaire", "sesriem"]},
    {"id": "D4", "fecha": "3 nov", "bloque": "desierto",
     "titulo": "Sossusvlei, Deadvlei y Duna 45", "duerme": "sesriem",
     "por": ["sesriem", "sossusvlei", "duna45", "sesriem"]},
    {"id": "D5", "fecha": "4 nov", "bloque": "costa",
     "titulo": "Sesriem → Walvis Bay", "duerme": "walvisbay",
     "por": ["sesriem", "solitaire", "walvisbay"]},
    {"id": "D6", "fecha": "5 nov", "bloque": "costa",
     "titulo": "Walvis Bay: flamencos y descanso", "duerme": "walvisbay",
     "por": []},
    {"id": "D7", "fecha": "6 nov", "bloque": "costa",
     "titulo": "Cape Cross → Terrace Bay", "duerme": "terracebay",
     "por": ["walvisbay", "swakopmund", "hentiesbay", "capecross", "ugabmund", "terracebay"]},
    {"id": "D8", "fecha": "7 nov", "bloque": "damaraland",
     "titulo": "Skeleton Coast → Twyfelfontein", "duerme": "twyfelfontein",
     "por": ["terracebay", "springbokwasser", "twyfelfontein"]},
    {"id": "D9", "fecha": "8 nov", "bloque": "damaraland",
     "titulo": "Twyfelfontein → Palmwag → Hoada", "duerme": "hoada",
     "por": ["twyfelfontein", "palmwag", "grootberg", "hoada"]},
    {"id": "D10", "fecha": "9 nov", "bloque": "etosha",
     "titulo": "Hoada → Etosha (Okaukuejo)", "duerme": "okaukuejo",
     "por": ["hoada", "kamanjab", "outjo", "andersson", "okaukuejo"]},
    {"id": "D11", "fecha": "10 nov", "bloque": "etosha",
     "titulo": "Safari Okaukuejo → Halali", "duerme": "halali",
     "por": ["okaukuejo", "gemsbokvlakte", "salvadora", "halali"]},
    {"id": "D12", "fecha": "11 nov", "bloque": "etosha",
     "titulo": "Safari Halali → Namutoni → Onguma", "duerme": "onguma",
     "por": ["halali", "goas", "chudob", "namutoni", "lindequist", "onguma"]},
    {"id": "D13", "fecha": "12 nov", "bloque": "etosha",
     "titulo": "Etosha este desde Onguma: Fischer's Pan", "duerme": "onguma",
     "por": ["onguma", "lindequist", "tweepalms", "chudob", "namutoni", "lindequist", "onguma"]},
    {"id": "D14", "fecha": "13 nov", "bloque": "vuelta",
     "titulo": "Onguma → Windhoek", "duerme": "windhoek",
     "por": ["onguma", "lindequist", "tsumeb", "otjiwarongo", "okahandja", "windhoek"]},
    {"id": "D15", "fecha": "14 nov", "bloque": "vuelta",
     "titulo": "Vuelo de vuelta", "duerme": None,
     "por": ["windhoek", "aeropuerto"]},
]

# Las quince etapas de la VARIANTE del `aparte/decision-del-ccf`. Desde el 24/08 la variante ya NO es otra ruta:
# es UN cambio, el del final. La ruta oficial y ésta son la misma línea hasta la noche del
# D12 en Onguma; lo que cambia es que aquí NO se duerme la segunda noche de Onguma, sino
# que el D13 se emplea en bajar al Cheetah Conservation Fund por la B1 y el D14 sale de
# allí. Es una decisión que se toma DENTRO de Etosha, según la fauna que haya salido.
# Misma forma que ETAPAS para que `geodatos.ruta_alt()` y `mapa.mapa_ruta_alt()` la
# traten igual — y para que el dia a dia del `aparte/decision-del-ccf` no se escriba a mano en ningun sitio.
ETAPAS_ALT = [
    {"id": "D1", "fecha": "31 oct", "bloque": "llegada",
     "titulo": "Llegada, coche y compra en Windhoek", "duerme": "windhoek",
     "por": ["aeropuerto", "windhoek"]},
    {"id": "D2", "fecha": "1 nov", "bloque": "desierto",
     "titulo": "Windhoek → paso de Spreetshoogte", "duerme": "spreetshoogte",
     "por": ["windhoek", "rehoboth", "spreetshoogte"]},
    {"id": "D3", "fecha": "2 nov", "bloque": "desierto",
     "titulo": "Spreetshoogte → Solitaire → Sesriem", "duerme": "sesriem",
     "por": ["spreetshoogte", "solitaire", "sesriem"]},
    {"id": "D4", "fecha": "3 nov", "bloque": "desierto",
     "titulo": "Sossusvlei, Deadvlei y Duna 45", "duerme": "sesriem",
     "por": ["sesriem", "sossusvlei", "duna45", "sesriem"]},
    {"id": "D5", "fecha": "4 nov", "bloque": "costa",
     "titulo": "Sesriem → Walvis Bay", "duerme": "walvisbay",
     "por": ["sesriem", "solitaire", "walvisbay"]},
    {"id": "D6", "fecha": "5 nov", "bloque": "costa",
     "titulo": "Walvis Bay: flamencos y descanso", "duerme": "walvisbay",
     "por": []},
    {"id": "D7", "fecha": "6 nov", "bloque": "costa",
     "titulo": "Cape Cross → Terrace Bay", "duerme": "terracebay",
     "por": ["walvisbay", "swakopmund", "hentiesbay", "capecross", "ugabmund", "terracebay"]},
    {"id": "D8", "fecha": "7 nov", "bloque": "damaraland",
     "titulo": "Skeleton Coast → Twyfelfontein", "duerme": "twyfelfontein",
     "por": ["terracebay", "springbokwasser", "twyfelfontein"]},
    {"id": "D9", "fecha": "8 nov", "bloque": "damaraland",
     "titulo": "Twyfelfontein → Palmwag → Hoada", "duerme": "hoada",
     "por": ["twyfelfontein", "palmwag", "grootberg", "hoada"]},
    {"id": "D10", "fecha": "9 nov", "bloque": "etosha",
     "titulo": "Hoada → Etosha (Okaukuejo)", "duerme": "okaukuejo",
     "por": ["hoada", "kamanjab", "outjo", "andersson", "okaukuejo"]},
    {"id": "D11", "fecha": "10 nov", "bloque": "etosha",
     "titulo": "Safari Okaukuejo → Halali", "duerme": "halali",
     "por": ["okaukuejo", "gemsbokvlakte", "salvadora", "halali"]},
    {"id": "D12", "fecha": "11 nov", "bloque": "etosha",
     "titulo": "Safari Halali → Namutoni → Onguma", "duerme": "onguma",
     "por": ["halali", "goas", "chudob", "namutoni", "lindequist", "onguma"]},
    {"id": "D13", "fecha": "12 nov", "bloque": "vuelta",
     "titulo": "Onguma → Tsumeb → Otjiwarongo → CCF", "duerme": "ccf",
     "por": ["onguma", "tsumeb", "otjiwarongo", "ccf"]},
    {"id": "D14", "fecha": "13 nov", "bloque": "vuelta",
     "titulo": "Cheetah Run y bajada a Windhoek", "duerme": "windhoek",
     "por": ["ccf", "windhoek"]},
    {"id": "D15", "fecha": "14 nov", "bloque": "vuelta",
     "titulo": "Vuelo de vuelta", "duerme": None,
     "por": ["windhoek", "aeropuerto"]},
]

# El firme de cada carretera, por su nombre. En Namibia la letra manda: B es asfalto, C y D
# son grava — y luego estan las excepciones, que son justo las que el dossier ya tenia
# documentadas una a una. Aqui van TODAS las carreteras que pisa la ruta, para que un
# tramo sin clasificar salte a la vista en vez de pintarse de cualquier cosa. Las claves
# «parque» son pistas de dentro de Etosha y del Skeleton Coast, que van a 60.
#
#   asfalto  · B1, B2, B6, C38 Otjiwarongo–Okaukuejo (Wikipedia, `13` §3), C40 Outjo–Kamanjab
#              (Wikipedia, `13` §3), C34 Swakopmund–Henties Bay (asfaltada en 2019, `13` §3)
#   grava    · el resto de C y D
#   sal      · C34 al norte de Henties Bay: salt road, se conduce como grava
FIRME = {
    "B1": "asfalto", "B2": "asfalto", "B6": "asfalto", "B8": "asfalto",
    "M47": "grava",                      # es el nombre alternativo de la C24 en OSM
    "C14": "grava", "C19": "grava", "C24": "grava", "C26": "grava", "C28": "grava",
    "C34": "sal",                        # se afina por latitud en firme_de(): al sur de
    "C35": "grava", "C36": "grava",      # Henties Bay es asfalto
    "C38": "asfalto", "C39": "grava", "C40": "asfalto",   # C40: asfalto solo Outjo–Kamanjab
    "C43": "grava", "C45": "grava",
    "D826": "grava", "D1261": "grava", "D1275": "grava", "D1982": "grava",
    "D2612": "grava", "D3254": "grava", "D2743": "grava", "D3706": "grava",
    "D3245": "grava", "C27": "grava",
    "A1": "asfalto",                     # la B1 dentro de Windhoek lleva ese ref en OSM
    "M44": "asfalto",                    # la salida de Walvis Bay a la B2
    "D2302": "parque",                   # Springbokwasser–Torra Bay, dentro del Skeleton Coast
}

# Carreteras que OSM nombra pero no numera. La de Sossusvlei es asfalto hasta el
# aparcamiento 2WD (`06` §5, `01` §D4); los ultimos 5 km de arena no los enruta OSRM.
FIRME_POR_NOMBRE = {"Sossusvlei Road": "asfalto", "Sesriem Road": "grava"}


def firme_de(ref, lat=None, lon=None, nombre=None):
    """Asfalto, grava, sal o parque para un tramo de OSRM, con las excepciones geograficas.

    Devuelve None si la carretera no esta en la tabla: el que dibuja decide que hacer,
    pero nunca se inventa un firme. Sin nombre y dentro de Etosha o del Skeleton Coast
    es pista de parque.
    """
    if not ref and nombre in FIRME_POR_NOMBRE:
        return FIRME_POR_NOMBRE[nombre]
    if not ref:
        if lat is not None and -19.7 < lat < -18.3 and 14.2 < lon < 17.5:
            return "parque"                                    # Etosha
        if lat is not None and lat > -21.3 and lon < 13.75:
            return "parque"                                    # Skeleton Coast
        return None
    ref = ref.split(";")[0].strip()
    f = FIRME.get(ref)
    if ref == "C34" and lat is not None and lat < -22.1:
        return "asfalto"                                       # Swakopmund–Henties Bay
    if ref == "C40" and lat is not None and lon < 14.85:
        return "grava"                                         # al oeste de Kamanjab
    return f


# Color por bloque. Sale de la paleta del sitio: basalto, hueso y oxido, mas los
# acentos de estado que ya usan los diagramas del dossier.
COLOR_BLOQUE = {
    "llegada":    "#7D776E",
    "desierto":   "#C2542F",
    "costa":      "#2F6E8E",
    "damaraland": "#8A6210",
    "etosha":     "#5F7043",
    "vuelta":     "#7D776E",
}
