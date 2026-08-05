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

    # --- Damaraland ---
    "springbokwasser": (-20.31055, 13.64769, "Puerta de Springbokwasser", "puerta"),
    "twyfelfontein": (-20.54842, 14.41099, "Twyfelfontein", "hito"),
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
    "tweepalms":     (-18.76560, 17.02990, "Twee Palms · Fischer's Pan", "hito"),
    "chudob":        (-18.85820, 16.92490, "Chudob", "hito"),
    "gemsbokvlakte": (-19.21340, 16.05830, "Gemsbokvlakte", "hito"),
    "salvadora":     (-19.03460, 16.26970, "Salvadora", "hito"),
    "goas":          (-18.98900, 16.55840, "Goas", "hito"),
}

# Cada etapa es un dia. `por` son los puntos por los que OSRM tiene que pasar, en orden.
# `bloque` agrupa por tramo del viaje y decide el color de la linea en el mapa.
ETAPAS = [
    {"id": "D1", "fecha": "1 nov", "bloque": "llegada",
     "titulo": "Llegada a Windhoek", "duerme": "windhoek",
     "por": ["aeropuerto", "windhoek"]},
    {"id": "D2", "fecha": "2 nov", "bloque": "desierto",
     "titulo": "Windhoek → paso de Spreetshoogte", "duerme": "spreetshoogte",
     "por": ["windhoek", "rehoboth", "spreetshoogte"]},
    {"id": "D3", "fecha": "3 nov", "bloque": "desierto",
     "titulo": "Spreetshoogte → Solitaire → Sesriem", "duerme": "sesriem",
     "por": ["spreetshoogte", "solitaire", "sesriem"]},
    {"id": "D4", "fecha": "4 nov", "bloque": "desierto",
     "titulo": "Sossusvlei, Deadvlei y Duna 45", "duerme": "sesriem",
     "por": ["sesriem", "sossusvlei", "duna45", "sesriem"]},
    {"id": "D5", "fecha": "5 nov", "bloque": "costa",
     "titulo": "Sesriem → Walvis Bay", "duerme": "walvisbay",
     "por": ["sesriem", "solitaire", "walvisbay"]},
    {"id": "D6", "fecha": "6 nov", "bloque": "costa",
     "titulo": "Walvis Bay: flamencos y descanso", "duerme": "walvisbay",
     "por": []},
    {"id": "D7", "fecha": "7 nov", "bloque": "costa",
     "titulo": "Cape Cross → Terrace Bay", "duerme": "terracebay",
     "por": ["walvisbay", "swakopmund", "hentiesbay", "capecross", "ugabmund", "terracebay"]},
    {"id": "D8", "fecha": "8 nov", "bloque": "damaraland",
     "titulo": "Skeleton Coast → Twyfelfontein → Hoada", "duerme": "hoada",
     "por": ["terracebay", "springbokwasser", "twyfelfontein", "hoada"]},
    {"id": "D9", "fecha": "9 nov", "bloque": "etosha",
     "titulo": "Hoada → Etosha (Okaukuejo)", "duerme": "okaukuejo",
     "por": ["hoada", "kamanjab", "outjo", "andersson", "okaukuejo"]},
    {"id": "D10", "fecha": "10 nov", "bloque": "etosha",
     "titulo": "Safari Okaukuejo → Halali", "duerme": "halali",
     "por": ["okaukuejo", "gemsbokvlakte", "salvadora", "halali"]},
    {"id": "D11", "fecha": "11 nov", "bloque": "etosha",
     "titulo": "Safari Halali → Namutoni", "duerme": "namutoni",
     "por": ["halali", "goas", "chudob", "namutoni"]},
    {"id": "D12", "fecha": "12 nov", "bloque": "etosha",
     "titulo": "Etosha este: Fischer's Pan y Chudob", "duerme": "namutoni",
     "por": ["namutoni", "tweepalms", "chudob", "namutoni"]},
    {"id": "D13", "fecha": "13 nov", "bloque": "vuelta",
     "titulo": "Etosha → Windhoek", "duerme": "windhoek",
     "por": ["namutoni", "lindequist", "tsumeb", "otjiwarongo", "okahandja", "windhoek"]},
    {"id": "D14", "fecha": "14 nov", "bloque": "vuelta",
     "titulo": "Vuelo de vuelta", "duerme": None,
     "por": ["windhoek", "aeropuerto"]},
]

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
