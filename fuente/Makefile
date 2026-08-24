# Namibia 2026 · el dossier
#
#   make            los cuatro PDF, con lo que ya haya descargado
#   make imagenes   descarga las fotos del catalogo (Wikimedia Commons) a img/
#   make geo        descarga y cachea la geometria de los mapas a fuente/geo/
#   make avistam    recuentos de GBIF y porcentajes por campamento a fuente/geo/
#   make charcas    reescribe aparte/charcas-de-los-campamentos-de-etosha.md
#   make mapas      exporta los mapas a img/mapas/ (SVG y PNG; el de la ruta va en el README)
#   make mymaps     reescribe los CSV y el KML de aparte/ para Google My Maps
#   make dossier    solo dossier-namibia-2026.pdf
#   make fauna      solo guia-fauna-etosha.pdf
#   make lamina     mapa-ruta-namibia-2026.pdf, la lamina A2 para imprimir
#   make agenda     agenda-namibia-2026.pdf, el dia a dia del `01` y nada mas, un A4 por dia
#   make todo       de cero: imagenes + geo + avistamientos + mapas + los cuatro PDF
#   make comprueba  imagenes, licencias, geometria, avistamientos, escala y README
#   make limpia     borra el HTML intermedio
#
# Solo hace falta Python 3 (pip install -r requirements.txt), Google Chrome y poppler-utils.
# Las comprobaciones corren tambien solas en cada push: .github/workflows/comprueba.yml.

# Si hay un entorno virtual al lado, se usa. En macOS el Python de Homebrew rechaza
# cualquier `pip install` (PEP 668), asi que ahi las dependencias SOLO caben en un venv:
#   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# En Linux y en el runner de CI no hay .venv y sigue valiendo el python3 del sistema.
PY      := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
RAIZ    := $(abspath ..)
IMG     := $(RAIZ)/img
GEO     := geo

.PHONY: all todo imagenes geo avistam mapas charcas mymaps dossier fauna lamina agenda gps limpia comprueba

all: dossier fauna lamina agenda gps

todo: imagenes geo avistam mapas mymaps dossier fauna lamina agenda gps

imagenes:
	$(PY) descargar.py

geo:
	$(PY) geodatos.py

avistam: | $(GEO)/ruta.json
	$(PY) avistamientos.py

mapas: | $(GEO)/ruta.json
	$(PY) mapa.py

# El estudio de las charcas sale entero de los partes ya cacheados: ni red ni Chrome.
charcas: | $(GEO)/avistamientos.json
	$(PY) estudio_charcas.py

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

# La agenda es el `01` recortado a sus quince dias: solo pide la geometria, para la portada.
agenda: | $(GEO)/ruta.json
	$(PY) agenda.py

# Las paradas y el trazado que se importan en Google My Maps, en aparte/. Misma
# geometria otra vez: se derivan, no se escriben.
mymaps: | $(GEO)/ruta.json
	$(PY) mapas_google.py

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
	rm -f dossier.html guia-fauna.html lamina.html agenda.html
