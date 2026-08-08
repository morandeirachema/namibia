# Namibia 2026 · el dossier
#
#   make            los dos PDF, con lo que ya haya descargado
#   make imagenes   descarga las 128 fotos de Wikimedia Commons a img/
#   make geo        descarga y cachea la geometria de los mapas a fuente/geo/
#   make avistam    recuentos de GBIF y porcentajes por campamento a fuente/geo/
#   make mapas      exporta los mapas a img/mapas/ (SVG y PNG; el de la ruta va en el README)
#   make dossier    solo dossier-namibia-2026.pdf
#   make fauna      solo guia-fauna-etosha.pdf
#   make todo       de cero: imagenes + geo + avistamientos + mapas + los dos PDF
#   make comprueba  imagenes, licencias, geometria, avistamientos, escala y README
#   make limpia     borra el HTML intermedio
#
# Solo hace falta Python 3 con markdown-it-py y Pillow, Google Chrome y poppler-utils.

PY      := python3
RAIZ    := $(abspath ..)
IMG     := $(RAIZ)/img
GEO     := geo

.PHONY: all todo imagenes geo avistam mapas dossier fauna limpia comprueba

all: dossier fauna

todo: imagenes geo avistam mapas dossier fauna

imagenes:
	$(PY) descargar.py

geo:
	$(PY) geodatos.py

avistam: | $(GEO)/ruta.json
	$(PY) avistamientos.py

mapas: | $(GEO)/ruta.json
	$(PY) mapa.py

dossier: | $(IMG)/creditos.json $(GEO)/ruta.json
	$(PY) dossier.py

fauna: | $(IMG)/creditos.json $(GEO)/avistamientos.json
	$(PY) guia_fauna.py

$(IMG)/creditos.json:
	$(PY) descargar.py

# El testigo de que `geodatos.py` ya corrio es un fichero suyo, no el directorio:
# antes el objetivo se llamaba igual que el target phony `geo` (make avisaba de
# instrucciones anuladas) y, al ser phony, relanzaba la descarga aunque el cache
# estuviera completo.
$(GEO)/ruta.json:
	$(PY) geodatos.py

# La guia de fauna se puede montar sin esto —las fichas salen sin la linea de
# posibilidades—, pero el `make` completo lo pide para no publicarla a medias.
$(GEO)/avistamientos.json: | $(GEO)/ruta.json
	$(PY) avistamientos.py

# Comprobaciones baratas antes de dar un PDF por bueno.
comprueba:
	@$(PY) comprobar.py

limpia:
	rm -f dossier.html guia-fauna.html
