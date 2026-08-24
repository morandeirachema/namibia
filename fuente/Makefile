# Namibia 2026 · el dossier
#
#   make            los tres PDF, con lo que ya haya descargado
#   make imagenes   descarga las fotos del catalogo (Wikimedia Commons) a img/
#   make geo        descarga y cachea la geometria de los mapas a fuente/geo/
#   make avistam    recuentos de GBIF y porcentajes por campamento a fuente/geo/
#   make mapas      exporta los mapas a img/mapas/ (SVG y PNG; el de la ruta va en el README)
#   make dossier    solo dossier-namibia-2026.pdf
#   make fauna      solo guia-fauna-etosha.pdf
#   make lamina     mapa-ruta-namibia-2026.pdf, la lamina A2 para imprimir
#   make todo       de cero: imagenes + geo + avistamientos + mapas + los tres PDF
#   make comprueba  imagenes, licencias, geometria, avistamientos, escala y README
#   make limpia     borra el HTML intermedio
#
# Solo hace falta Python 3 (pip install -r requirements.txt), Google Chrome y poppler-utils.
# Las comprobaciones corren tambien solas en cada push: .github/workflows/comprueba.yml.

PY      := python3
RAIZ    := $(abspath ..)
IMG     := $(RAIZ)/img
GEO     := geo

.PHONY: all todo imagenes geo avistam mapas dossier fauna lamina gps limpia comprueba

all: dossier fauna lamina gps

todo: imagenes geo avistam mapas dossier fauna lamina gps

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

# La lamina solo necesita la geometria: ni fotos ni avistamientos.
lamina: | $(GEO)/ruta.json
	$(PY) lamina.py

# El GPX y el KML, para el GPS y el movil. Misma geometria que el mapa y la lamina.
gps: | $(GEO)/ruta.json
	$(PY) gps.py

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
