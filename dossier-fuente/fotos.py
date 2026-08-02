#!/usr/bin/env python3
"""Fotos de los lugares de la ruta, desde Wikimedia Commons, con licencia y autoria."""
import json, os, re, time, urllib.parse, urllib.request

UA = "NamibiaTripDossier/1.0 (josemorandeira@gmail.com)"
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img"); os.makedirs(IMG, exist_ok=True)

# (slug, pie de foto, busqueda en Commons)
LUGARES = [
 ("portada",       "Deadvlei al amanecer — el motivo del viaje",            "Deadvlei sunrise Namibia"),
 ("windhoek",      "Windhoek, punto de entrada y de salida",                "Windhoek Namibia city view"),
 ("spreetshoogte", "El paso de Spreetshoogte, con el Namib mil metros abajo","Spreetshoogte Pass Namibia"),
 ("solitaire",     "Solitaire: gasolina, tarta de manzana y coches oxidados","Solitaire Namibia"),
 ("sossusvlei",    "Las dunas de Sossusvlei",                                "Sossusvlei dunes Namibia"),
 ("deadvlei",      "Los árboles muertos de Deadvlei",                        "Deadvlei Namibia trees"),
 ("duna45",        "Duna 45, en la carretera de Sossusvlei",                 "Dune 45 Sossusvlei"),
 ("sesriem",       "El cañón de Sesriem",                                    "Sesriem Canyon Namibia"),
 ("walvisbay",     "Flamencos en la laguna de Walvis Bay",                   "Walvis Bay lagoon flamingos"),
 ("swakopmund",    "Swakopmund, la costa alemana",                           "Swakopmund Namibia jetty"),
 ("capecross",     "La colonia de lobos marinos de Cape Cross",              "Cape Cross seal colony Namibia"),
 ("skeleton",      "La Costa de los Esqueletos",                             "Skeleton Coast Namibia shipwreck"),
 ("twyfelfontein", "Los grabados rupestres de Twyfelfontein",                "Twyfelfontein engravings"),
 ("damaraland",    "Damaraland, camino de Grootberg",                        "Damaraland Namibia landscape"),
 ("etosha-pan",    "La depresión de Etosha",                                 "Etosha Pan Namibia"),
 ("okaukuejo",     "La charca de Okaukuejo",                                 "Okaukuejo waterhole Etosha"),
 ("grava",         "La pista de grava: donde vive el riesgo del viaje",      "Namibia gravel road C road"),
 ("cielo",         "El cielo del desierto namibio",                          "Namib desert night sky stars"),
 ("termitero",     "Termitero en la sabana",                                 "termite mound Namibia"),
 ("hilux",         "Un 4x4 con tienda de techo, como el vuestro",            "Toyota Hilux roof tent Namibia camping"),
]

def api(params):
    params = dict(params); params["format"] = "json"
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=30))

def limpia(v):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", v)).strip()

manifest = []
for slug, pie, busqueda in LUGARES:
    try:
        d = api({"action": "query", "generator": "search", "gsrsearch": busqueda,
                 "gsrnamespace": "6", "gsrlimit": "14", "prop": "imageinfo",
                 "iiprop": "url|extmetadata|mime|size", "iiurlwidth": "1100"})
        mejor = None
        for _, p in d.get("query", {}).get("pages", {}).items():
            ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
            lic = limpia(em.get("LicenseShortName", {}).get("value", ""))
            if ii.get("mime") != "image/jpeg":            continue
            if not lic.startswith(("CC BY", "CC0", "Public")):  continue
            if ii.get("width", 0) < 1100:                 continue
            if ii["width"] / ii["height"] < 1.2:          continue   # apaisadas
            puntos = ii["width"] * ii["height"]
            if not mejor or puntos > mejor[0]:
                mejor = (puntos, p, ii, em, lic)
        if not mejor:
            print(f"!! sin foto util: {slug}"); continue
        _, p, ii, em, lic = mejor
        dest = os.path.join(IMG, slug + ".jpg")
        req = urllib.request.Request(ii["thumburl"], headers={"User-Agent": UA})
        open(dest, "wb").write(urllib.request.urlopen(req, timeout=60).read())
        manifest.append({"slug": slug, "pie": pie, "file": p["title"], "local": slug + ".jpg",
                         "license": lic, "artist": limpia(em.get("Artist", {}).get("value", "")),
                         "descurl": ii.get("descriptionurl")})
        print(f"OK {slug:15s} {lic:16s} {manifest[-1]['artist'][:34]:36s}")
        time.sleep(0.2)
    except Exception as e:
        print(f"!! {slug}: {e}")

json.dump(manifest, open(os.path.join(HERE, "fotos.json"), "w"), indent=1, ensure_ascii=False)
print(f"\n{len(manifest)}/{len(LUGARES)} fotos de lugares")
