# Paradas de la ruta, para Google My Maps

*Documento de consulta aparte — sin enlazar todavía desde el README ni desde ninguno de los dos
PDF.*

📍 **[El mapa ya montado, en Google My Maps](https://www.google.com/maps/d/u/0/edit?mid=1MQI8k4r_mCZwAcnhjcCBGndU-yHECHI&usp=sharing)**
— ábrelo directamente, o entra desde la app Google Maps del móvil en "Tus lugares" → "Mapas".

⚠️ **12/08, dos correcciones sobre la primera versión — hay que reimportar**:

1. El orden de las filas ahora es el real de paso por la ruta, no el bloque del catálogo interno.
2. **Los tres puntos sin día confirmado se sacaron a un fichero aparte.** Iban al final del CSV
   único, y si el mapa tiene una línea que conecta los puntos en orden, eso los dibujaba como si
   fueran la parada nº36-38 — justo después de Okahandja, que es la vuelta a Windhoek el D13: habría
   hecho parecer que Torra Bay (costa) se visita *después* de terminar el viaje entero, cosa que no
   es verdad. Separarlos evita esa lectura falsa sin tener que inventarles un día.

**Google My Maps no se actualiza solo cuando cambia el fichero de origen — hay que volver a
importar los dos CSV de abajo si ya tenías la versión anterior.**

## Los dos ficheros

- **[namibia-paradas-google-maps.csv](namibia-paradas-google-maps.csv)** — 35 puntos con día
  confirmado, **en el orden real en que se pasa por ellos**: dónde se duerme cada noche, lo que se
  visita, las puertas de parque con horario, los puertos de montaña y las gasolineras que el
  dossier marca como obligatorias. Es el que sirve para trazar una línea/ruta en My Maps, porque su
  orden es el orden de verdad.
- **[namibia-puntos-sin-dia-confirmado.csv](namibia-puntos-sin-dia-confirmado.csv)** — 3 puntos
  reales (coordenadas correctas) que **ninguna fuente sitúa en un día concreto**: Torra Bay,
  Khorixas y la puerta de Galton. Impórtalos como **capa separada**, sin conectarlos con una línea
  ni mezclarlos con la secuencia de arriba — son de consulta suelta, no paradas ordenadas.

## Cómo importar

1. Entra en [mymaps.google.com](https://mymaps.google.com) y crea un mapa nuevo (o abre el que ya
   tengas del viaje).
2. **Añadir capa** → **Importar** → sube `namibia-paradas-google-maps.csv`. Con este sí puedes usar
   luego "Añadir línea o forma" → "Direcciones en coche" apoyándote en el orden de las filas, si
   quieres dibujar el itinerario completo.
3. Cuando pregunte qué columnas son la posición, marca **Latitud** y **Longitud**; para el título
   de cada chincheta, marca **Nombre**.
4. **Añadir capa** otra vez → **Importar** → sube ahora
   `namibia-puntos-sin-dia-confirmado.csv`, en su propia capa, sin línea que la conecte.
5. Opcional, en cada capa: **Estilo de capa** → "Estilo uniforme" → "Agrupar lugares por columna" →
   **Categoría**. Google My Maps le pone automáticamente un color e icono distinto a cada grupo
   (dónde se duerme, lo que se visita, puertas, puertos, ciudades, gasolineras), sin tocar nada a
   mano.
6. La app **Google Maps** del móvil sincroniza sola los mapas guardados en My Maps — no hace falta
   enlace nuevo ni exportar otra vez: abre "Tus lugares" → "Mapas" en el móvil y ahí está.

## De dónde salen los datos — cero fabricación

Las 38 coordenadas base son las que ya usa este mismo repo para dibujar sus propios mapas y
calcular la ruta real por carretera: `fuente/trazado.py`, geocodificadas con OpenStreetMap
(Nominatim y Overpass) el 04/08/2026 — no son una estimación nueva ni aproximada. Las columnas
**Días de la ruta** y **Noche aquí** del fichero principal salen de cruzar esas coordenadas con
`fuente/trazado.py` → `ETAPAS`, el itinerario día a día que ya usa `geodatos.py` para pedirle a
OSRM el trazado real de cada etapa.

**El orden de las filas del fichero principal es el orden real de paso**, no alfabético ni de
bloque del catálogo: se calcula recorriendo `ETAPAS` día a día y anotando la primera vez que se
pisa cada punto. Tres de esos 35 —**Deadvlei**, **Palmwag** y el **paso de Grootberg**— no son
ancla de enrutado OSRM (el camino pasa por ellos sin necesitar un punto de paso aparte para que la
ruta salga bien), así que el cruce automático los dejaba sin día ni posición: se completaron a mano
contra [`01-itinerarios-dia-a-dia.md`](01-itinerarios-dia-a-dia.md) e insertaron en su hueco real
(Deadvlei justo tras Duna 45 en el D4; Palmwag y Grootberg entre Twyfelfontein y Hoada en el D8, en
ese orden geográfico).

**Los tres puntos del segundo fichero no tienen día ni orden asignado, a propósito** ❌ — ni la
geometría de la ruta ni el itinerario narrado sitúan a Torra Bay, Khorixas o la puerta de Galton en
un momento concreto del viaje *(Galton, de hecho, ni siquiera se usa en la ruta final: no conecta
con la red principal del parque hacia Okaukuejo, `13`)*. Sus coordenadas son reales; su fecha, no —
mejor un hueco reconocido, y aparte, que un día o un orden inventados.
