# Paradas de la ruta, para Google My Maps

*Documento de consulta aparte — sin enlazar todavía desde el README ni desde ninguno de los dos
PDF.*

📍 **[El mapa ya montado, en Google My Maps](https://www.google.com/maps/d/u/0/edit?mid=1MQI8k4r_mCZwAcnhjcCBGndU-yHECHI&usp=sharing)**
— ábrelo directamente, o entra desde la app Google Maps del móvil en "Tus lugares" → "Mapas".

⚠️ **12/08, tres correcciones/añadidos sobre la primera versión — hay que reimportar**:

1. El orden de las filas del CSV principal ahora es el real de paso por la ruta, no el bloque del
   catálogo interno.
2. **Los tres puntos sin día confirmado se sacaron a un fichero aparte.** Iban al final del CSV
   único, y si el mapa tiene una línea que conecta los puntos en orden, eso los dibujaba como si
   fueran la parada nº36-38 — justo después de Okahandja, que es la vuelta a Windhoek el D13:
   habría hecho parecer que Torra Bay (costa) se visita *después* de terminar el viaje entero, cosa
   que no es verdad. Separarlos evita esa lectura falsa sin tener que inventarles un día.
3. **Nuevo: el trazado real por carretera**, no líneas rectas entre chinchetas — ver más abajo.

**Google My Maps no se actualiza solo cuando cambia el fichero de origen — hay que volver a
importar los tres ficheros de abajo si ya tenías una versión anterior.**

## Los tres ficheros

- **[namibia-paradas-google-maps.csv](namibia-paradas-google-maps.csv)** — 35 puntos con día
  confirmado, **en el orden real en que se pasa por ellos**: dónde se duerme cada noche, lo que se
  visita, las puertas de parque con horario, los puertos de montaña y las gasolineras que el
  dossier marca como obligatorias.
- **[namibia-puntos-sin-dia-confirmado.csv](namibia-puntos-sin-dia-confirmado.csv)** — 3 puntos
  reales (coordenadas correctas) que **ninguna fuente sitúa en un día concreto**: Torra Bay,
  Khorixas y la puerta de Galton. Impórtalos como **capa separada**, sin conectarlos con una línea
  ni mezclarlos con la secuencia de arriba — son de consulta suelta, no paradas ordenadas.
- **[namibia-trazado-carreteras.kml](namibia-trazado-carreteras.kml)** — el camino en sí, **por la
  carretera o pista real, no la línea recta entre dos chinchetas** que dibujaría My Maps si le
  pides "direcciones en coche" entre puntos sueltos *(Google ni siquiera tiene datos fiables de
  muchas pistas de grava namibias — la línea recta habría sido peor que nada)*. Son 13 tramos —uno
  por día de conducción, coloreados por bloque del viaje (desierto, costa, Damaraland, Etosha,
  vuelta)—, cada uno con su fecha, sus km y sus horas de conducción al pulsarlo. D2 y D6 no llevan
  tramo propio porque ese día no hay conducción — se está en el mismo sitio que el día anterior.

## Cómo importar

1. Entra en [mymaps.google.com](https://mymaps.google.com) y crea un mapa nuevo (o abre el que ya
   tengas del viaje).
2. **Añadir capa** → **Importar** → sube `namibia-paradas-google-maps.csv`. Cuando pregunte qué
   columnas son la posición, marca **Latitud** y **Longitud**; para el título de cada chincheta,
   marca **Nombre**.
3. **Añadir capa** otra vez → **Importar** → sube `namibia-puntos-sin-dia-confirmado.csv`, en su
   propia capa.
4. **Añadir capa** una tercera vez → **Importar** → sube `namibia-trazado-carreteras.kml`. Este
   entra ya con sus 13 líneas, sus nombres y sus colores — no hace falta mapear columnas.
5. Opcional, en las dos capas de puntos: **Estilo de capa** → "Estilo uniforme" → "Agrupar lugares
   por columna" → **Categoría**. Google My Maps le pone automáticamente un color e icono distinto a
   cada grupo (dónde se duerme, lo que se visita, puertas, puertos, ciudades, gasolineras), sin
   tocar nada a mano.
6. La app **Google Maps** del móvil sincroniza sola los mapas guardados en My Maps — no hace falta
   enlace nuevo ni exportar otra vez: abre "Tus lugares" → "Mapas" en el móvil y ahí está.

## De dónde salen los datos — cero fabricación

Las 38 coordenadas de los puntos, y los 18.432 puntos de la geometría de las 13 líneas, son las que
ya usa este mismo repo para dibujar sus propios mapas y calcular la ruta real por carretera:
`fuente/trazado.py` para los puntos —geocodificados con OpenStreetMap (Nominatim y Overpass) el
04/08/2026—, y `fuente/geo/ruta.json` para el trazado, que es el resultado real de pedirle a OSRM
(el mismo motor de rutas que usa OpenStreetMap) el camino día a día entre esos puntos — no una
estimación nueva ni una línea recta.

**El orden de las filas del CSV principal es el orden real de paso**, no alfabético ni de bloque
del catálogo: se calcula recorriendo `ETAPAS` día a día y anotando la primera vez que se pisa cada
punto. Tres de esos 35 —**Deadvlei**, **Palmwag** y el **paso de Grootberg**— no son ancla de
enrutado OSRM (el camino pasa por ellos sin necesitar un punto de paso aparte para que la ruta
salga bien), así que el cruce automático los dejaba sin día ni posición: se completaron a mano
contra [`01-itinerarios-dia-a-dia.md`](01-itinerarios-dia-a-dia.md) e insertaron en su hueco real
(Deadvlei justo tras Duna 45 en el D4; Palmwag y Grootberg entre Twyfelfontein y Hoada en el D8, en
ese orden geográfico).

**Los tres puntos del segundo fichero no tienen día ni orden asignado, a propósito** ❌ — ni la
geometría de la ruta ni el itinerario narrado sitúan a Torra Bay, Khorixas o la puerta de Galton en
un momento concreto del viaje *(Galton, de hecho, ni siquiera se usa en la ruta final: no conecta
con la red principal del parque hacia Okaukuejo, `13`)*. Sus coordenadas son reales; su fecha, no —
mejor un hueco reconocido, y aparte, que un día o un orden inventados.
