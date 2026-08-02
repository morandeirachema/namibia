#!/usr/bin/env python3
"""Descarga fotos de especies desde Wikimedia Commons con su licencia y autoria verificadas."""
import json, os, re, sys, time, urllib.parse, urllib.request

UA = "NamibiaTripDossier/1.0 (josemorandeira@gmail.com) python-urllib"
OUT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(OUT, "img")
os.makedirs(IMG, exist_ok=True)

# (slug, nombre_es, nombre_en, cientifico, titulo_wikipedia_en, override_commons_file)
MAMIFEROS = [
    ("elefante", "Elefante africano de sabana", "African bush elephant", "Loxodonta africana", "African bush elephant", None),
    ("rino-negro", "Rinoceronte negro", "Black rhinoceros", "Diceros bicornis", "Black rhinoceros", None),
    ("rino-blanco", "Rinoceronte blanco", "White rhinoceros", "Ceratotherium simum", "White rhinoceros", None),
    ("leon", "León", "Lion", "Panthera leo", "Lion", None),
    ("leopardo", "Leopardo", "Leopard", "Panthera pardus", "Leopard", None),
    ("guepardo", "Guepardo", "Cheetah", "Acinonyx jubatus", "Cheetah", None),
    ("jirafa", "Jirafa angoleña", "Angolan giraffe", "Giraffa giraffa angolensis", "Angolan giraffe", None),
    ("cebra-burchell", "Cebra de Burchell", "Burchell's zebra", "Equus quagga burchellii", "Burchell's zebra", None),
    ("cebra-hartmann", "Cebra de montaña de Hartmann", "Hartmann's mountain zebra", "Equus zebra hartmannae", "Hartmann's mountain zebra", None),
    ("orix", "Órix o gemsbok", "Gemsbok", "Oryx gazella", "Gemsbok", None),
    ("springbok", "Springbok", "Springbok", "Antidorcas marsupialis", "Springbok", None),
    ("kudu", "Gran kudú", "Greater kudu", "Tragelaphus strepsiceros", "Greater kudu", None),
    ("eland", "Eland común", "Common eland", "Taurotragus oryx", "Common eland", None),
    ("nu", "Ñu azul", "Blue wildebeest", "Connochaetes taurinus", "Blue wildebeest", None),
    ("impala-cara-negra", "Impala de cara negra", "Black-faced impala", "Aepyceros melampus petersi", "Black-faced impala", None),
    ("dikdik", "Dik-dik de Damara", "Damara dik-dik", "Madoqua damarensis", "Damara dik-dik", None),
    ("hiena-manchada", "Hiena manchada", "Spotted hyena", "Crocuta crocuta", "Spotted hyena", None),
    ("hiena-parda", "Hiena parda", "Brown hyena", "Parahyaena brunnea", "Brown hyena", None),
    ("chacal", "Chacal de lomo negro", "Black-backed jackal", "Lupulella mesomelas", "Black-backed jackal", None),
    ("ratel", "Ratel o tejón de la miel", "Honey badger", "Mellivora capensis", "Honey badger", None),
    ("facocero", "Facóquero", "Common warthog", "Phacochoerus africanus", "Warthog", None),
    ("suricata", "Suricata", "Meerkat", "Suricata suricatta", "Meerkat", None),
    ("hartebeest", "Alcélafo rojo", "Red hartebeest", "Alcelaphus buselaphus caama", "Red hartebeest", None),
    ("steenbok", "Steenbok", "Steenbok", "Raphicerus campestris", "Steenbok", None),
]

AVES = [
    ("avestruz", "Avestruz común", "Common ostrich", "Struthio camelus", "Common ostrich", None),
    ("avutarda-kori", "Avutarda kori", "Kori bustard", "Ardeotis kori", "Kori bustard", None),
    ("secretario", "Secretario", "Secretarybird", "Sagittarius serpentarius", "Secretarybird", None),
    ("carraca-lila", "Carraca lila", "Lilac-breasted roller", "Coracias caudatus", "Lilac-breasted roller", None),
    ("calao-amarillo", "Cálao de pico amarillo sureño", "Southern yellow-billed hornbill", "Tockus leucomelas", "Southern yellow-billed hornbill", None),
    ("calao-rojo", "Cálao de pico rojo sureño", "Southern red-billed hornbill", "Tockus rufirostris", "Southern red-billed hornbill", None),
    ("tejedor-republicano", "Tejedor republicano", "Sociable weaver", "Philetairus socius", "Sociable weaver", None),
    ("aguila-marcial", "Águila marcial", "Martial eagle", "Polemaetus bellicosus", "Martial eagle", None),
    ("buitre-dorsiblanco", "Buitre dorsiblanco africano", "White-backed vulture", "Gyps africanus", "White-backed vulture", None),
    ("flamenco-enano", "Flamenco enano", "Lesser flamingo", "Phoeniconaias minor", "Lesser flamingo", None),
    ("grulla-azul", "Grulla azul", "Blue crane", "Grus paradisea", "Blue crane", None),
    ("ganga-namaqua", "Ganga namaqua", "Namaqua sandgrouse", "Pterocles namaqua", "Namaqua sandgrouse", None),
    ("sison-negro", "Sisón negro norteño", "Northern black korhaan", "Afrotis afraoides", "Northern black korhaan", None),
    ("azor-lagartijero", "Azor lagartijero claro", "Pale chanting goshawk", "Melierax canorus", "Pale chanting goshawk", None),
    ("alcaudon-carmesi", "Alcaudón de pecho carmesí", "Crimson-breasted shrike", "Laniarius atrococcineus", "Crimson-breasted shrike", None),
    ("buho-lacteo", "Búho lácteo de Verreaux", "Verreaux's eagle-owl", "Bubo lacteus", "Verreaux's eagle-owl", None),
    ("abejaruco-carmin", "Abejaruco carmesí sureño", "Southern carmine bee-eater", "Merops nubicoides", "Southern carmine bee-eater", None),
    ("ciguena-abdim", "Cigüeña de Abdim", "Abdim's stork", "Ciconia abdimii", "Abdim's stork", None),
    ("estornino-cabo", "Estornino brillante del Cabo", "Cape starling", "Lamprotornis nitens", "Cape starling", None),
    ("pigargo-vocinglero", "Pigargo vocinglero", "African fish eagle", "Icthyophaga vocifer", "African fish eagle", None),
]


def api(base, params):
    params = dict(params)
    params["format"] = "json"
    url = base + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def lead_image(title):
    """Nombre del fichero de la imagen principal del articulo de Wikipedia."""
    d = api("https://en.wikipedia.org/w/api.php",
            {"action": "query", "prop": "pageimages", "piprop": "name",
             "titles": title, "redirects": 1})
    pages = d.get("query", {}).get("pages", {})
    for _, p in pages.items():
        if "pageimage" in p:
            return p["pageimage"], p.get("title", title)
    return None, title


def commons_info(filename, width=900):
    d = api("https://commons.wikimedia.org/w/api.php",
            {"action": "query", "prop": "imageinfo", "titles": "File:" + filename,
             "iiprop": "url|extmetadata|mime", "iiurlwidth": width})
    pages = d.get("query", {}).get("pages", {})
    for pid, p in pages.items():
        if pid == "-1" or "imageinfo" not in p:
            return None
        ii = p["imageinfo"][0]
        em = ii.get("extmetadata", {})

        def g(k):
            v = em.get(k, {}).get("value", "")
            v = re.sub(r"<[^>]+>", "", v)          # quitar HTML
            v = re.sub(r"\s+", " ", v).strip()
            return v
        return {
            "file": p["title"],
            "thumb": ii.get("thumburl") or ii.get("url"),
            "descurl": ii.get("descriptionurl"),
            "mime": ii.get("mime"),
            "license": g("LicenseShortName"),
            "license_url": em.get("LicenseUrl", {}).get("value", ""),
            "artist": g("Artist"),
            "credit": g("Credit"),
            "usage": g("UsageTerms"),
            "restrictions": g("Restrictions"),
        }
    return None


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())
    return os.path.getsize(dest)


manifest = []
for grupo, lista in (("mamifero", MAMIFEROS), ("ave", AVES)):
    for slug, es, en, sci, wtitle, override in lista:
        try:
            if override:
                fname, resolved = override, wtitle
            else:
                fname, resolved = lead_image(wtitle)
            if not fname:
                print(f"!! SIN IMAGEN  {slug} ({wtitle})")
                manifest.append({"slug": slug, "grupo": grupo, "es": es, "en": en,
                                 "sci": sci, "wiki": wtitle, "error": "sin pageimage"})
                continue
            info = commons_info(fname)
            if not info:
                print(f"!! SIN META    {slug} -> {fname}")
                manifest.append({"slug": slug, "grupo": grupo, "es": es, "en": en,
                                 "sci": sci, "wiki": wtitle, "error": "sin metadatos commons"})
                continue
            ext = ".jpg" if "jpeg" in (info["mime"] or "") else os.path.splitext(fname)[1].lower()
            dest = os.path.join(IMG, slug + ext)
            size = download(info["thumb"], dest)
            info.update({"slug": slug, "grupo": grupo, "es": es, "en": en, "sci": sci,
                         "wiki": resolved, "local": os.path.basename(dest), "bytes": size})
            manifest.append(info)
            print(f"OK {slug:22s} {info['license']:18s} {info['artist'][:38]:40s} {size//1024}KB")
            time.sleep(0.25)
        except Exception as e:
            print(f"!! ERROR {slug}: {e}")
            manifest.append({"slug": slug, "grupo": grupo, "es": es, "en": en,
                             "sci": sci, "wiki": wtitle, "error": str(e)})

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1, ensure_ascii=False)
print(f"\n{len([m for m in manifest if 'local' in m])}/{len(manifest)} con foto")
