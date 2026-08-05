# Namibia 2026 · el dossier
#
#   make            los dos PDF, con lo que ya haya descargado
#   make imagenes   descarga las 120 fotos de Wikimedia Commons a img/
#   make geo        descarga y cachea la geometria de los mapas a fuente/geo/
#   make mapas      exporta los mapas a img/mapas/ (SVG y PNG, para el README)
#   make dossier    solo dossier-namibia-2026.pdf
#   make fauna      solo guia-fauna-etosha.pdf
#   make todo       de cero: imagenes + geo + mapas + los dos PDF
#   make limpia     borra el HTML intermedio
#
# Solo hace falta Python 3 con markdown-it-py y Pillow, Google Chrome y poppler-utils.

PY      := python3
RAIZ    := $(abspath ..)
IMG     := $(RAIZ)/img
GEO     := geo

.PHONY: all todo imagenes geo mapas dossier fauna limpia comprueba

all: dossier fauna

todo: imagenes geo mapas dossier fauna

imagenes:
	$(PY) descargar.py

geo:
	$(PY) geodatos.py

mapas: | $(GEO)
	$(PY) mapa.py

dossier: | $(IMG)/creditos.json $(GEO)
	$(PY) dossier.py

fauna: | $(IMG)/creditos.json
	$(PY) guia_fauna.py

$(IMG)/creditos.json:
	$(PY) descargar.py

$(GEO):
	$(PY) geodatos.py

# Comprobaciones baratas antes de dar un PDF por bueno.
comprueba:
	@$(PY) comprobar.py

limpia:
	rm -f dossier.html guia-fauna.html
