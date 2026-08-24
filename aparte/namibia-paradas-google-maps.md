# Paradas de la ruta, para Google My Maps

*Documento de consulta aparte — sin enlazar todavía desde el README ni desde ninguno de los dos
PDF.*

📍 **[El mapa ya montado, en Google My Maps](https://www.google.com/maps/d/u/0/edit?mid=1MQI8k4r_mCZwAcnhjcCBGndU-yHECHI&usp=sharing)**
— ábrelo directamente, o entra desde la app Google Maps del móvil en "Tus lugares" → "Mapas".

🔴 **24/08 — LA RUTA CAMBIÓ Y ESTOS TRES FICHEROS ESTÁN REGENERADOS: hay que reimportarlos
enteros.** Los días se movieron: **Spreetshoogte pasa de dos noches a una**, aparece **noche propia
en Twyfelfontein (D8)** y **Namutoni deja de ser noche** —sus dos últimas las hace **Onguma
Tamboti**—. En la práctica, **todo lo que va del D3 al D9 lleva un número de día distinto** y hay
un tramo más en el KML. *(El itinerario nuevo, en [`01`](../01-itinerarios-dia-a-dia.md); el porqué,
en [la decisión del CCF](decision-del-ccf.md).)*

✅ **Y desde el 24/08 ya no se escriben a mano**: los tres salen de `fuente/mapas_google.py`, que los
deriva de `trazado.ETAPAS` y de `geo/ruta.json` — los mismos datos que dibujan el mapa del dossier y
el GPX. Antes se mantenían a mano y al mover una noche se quedaban contando la ruta de antes sin que
nada avisara.

*Correcciones anteriores que siguen vigentes:* el orden de las filas del CSV principal es el real de
paso por la ruta, no el bloque del catálogo interno; **los puntos sin día confirmado van en un
fichero aparte** *(si el mapa conecta los puntos con una línea, ponerlos al final los dibujaba como
si se visitaran después de volver a Windhoek)*; y el trazado va **por carretera real**, no en líneas
rectas entre chinchetas.

**Google My Maps no se actualiza solo cuando cambia el fichero de origen — hay que volver a
importar los tres ficheros de abajo si ya tenías una versión anterior.**

## Los tres ficheros

- **[namibia-paradas-google-maps.csv](namibia-paradas-google-maps.csv)** — 37 puntos con día
  confirmado, **en el orden real en que se pasa por ellos**: dónde se duerme cada noche, lo que se
  visita, las puertas de parque con horario, los puertos de montaña y las gasolineras que el
  dossier marca como obligatorias.
- **[namibia-puntos-sin-dia-confirmado.csv](namibia-puntos-sin-dia-confirmado.csv)** — 2 puntos
  reales (coordenadas correctas) que **ninguna fuente sitúa en un día concreto**:
  Khorixas y la puerta de Galton. Impórtalos como **capa separada**, sin conectarlos con una línea
  ni mezclarlos con la secuencia de arriba — son de consulta suelta, no paradas ordenadas.
- **[namibia-trazado-carreteras.kml](namibia-trazado-carreteras.kml)** — el camino en sí, **por la
  carretera o pista real, no la línea recta entre dos chinchetas** que dibujaría My Maps si le
  pides "direcciones en coche" entre puntos sueltos *(Google ni siquiera tiene datos fiables de
  muchas pistas de grava namibias — la línea recta habría sido peor que nada)*. Son **14 tramos**
  —uno por día de conducción, coloreados por bloque del viaje (desierto, costa, Damaraland, Etosha,
  vuelta)—, cada uno con su fecha, sus km y sus horas de conducción al pulsarlo. **Solo el D6 no
  lleva tramo propio**, porque es el día de descanso en Walvis Bay y no hay conducción. *(Eran 13:
  el día suelto de la escarpa desapareció y en su lugar entraron dos etapas de Damaraland.)*

## Cómo importar

1. Entra en [mymaps.google.com](https://mymaps.google.com) y crea un mapa nuevo (o abre el que ya
   tengas del viaje).
2. **Añadir capa** → **Importar** → sube `namibia-paradas-google-maps.csv`. Cuando pregunte qué
   columnas son la posición, marca **Latitud** y **Longitud**; para el título de cada chincheta,
   marca **Nombre**.
3. **Añadir capa** otra vez → **Importar** → sube `namibia-puntos-sin-dia-confirmado.csv`, en su
   propia capa.
4. **Añadir capa** una tercera vez → **Importar** → sube `namibia-trazado-carreteras.kml`. Este
   entra ya con sus 14 líneas, sus nombres y sus colores — no hace falta mapear columnas.
5. Opcional, en las dos capas de puntos: **Estilo de capa** → "Estilo uniforme" → "Agrupar lugares
   por columna" → **Categoría**. Google My Maps le pone automáticamente un color e icono distinto a
   cada grupo (dónde se duerme, lo que se visita, puertas, puertos, ciudades, gasolineras), sin
   tocar nada a mano.
6. La app **Google Maps** del móvil sincroniza sola los mapas guardados en My Maps — no hace falta
   enlace nuevo ni exportar otra vez: abre "Tus lugares" → "Mapas" en el móvil y ahí está.

## De dónde salen los datos — cero fabricación

Las 39 coordenadas de los puntos, y los 18.398 puntos de la geometría de las 14 líneas, son las que
ya usa este mismo repo para dibujar sus propios mapas y calcular la ruta real por carretera:
`fuente/trazado.py` para los puntos —geocodificados con OpenStreetMap (Nominatim y Overpass) el
04/08/2026—, y `fuente/geo/ruta.json` para el trazado, que es el resultado real de pedirle a OSRM
(el mismo motor de rutas que usa OpenStreetMap) el camino día a día entre esos puntos — no una
estimación nueva ni una línea recta.

**El orden de las filas del CSV principal es el orden real de paso**, no alfabético ni de bloque
del catálogo: lo calcula `mapas_google.py` recorriendo `ETAPAS` día a día y anotando la primera vez
que se pisa cada punto. **Dos de esos 37 —Deadvlei y Torra Bay— no son ancla de enrutado OSRM** (el
camino pasa por ellos sin necesitar un punto de paso aparte para que la ruta salga bien), así que
el cruce automático los dejaría sin día: van en la tabla `A_MANO` del propio script, con su día
escrito y el punto tras el que se insertan —**Deadvlei justo tras Duna 45 en el D4**, y **Torra Bay
tras la puerta de Ugabmund en el D7**, que es la C34 de la costa, cerrada y sin parada pero de
paso—. *(Palmwag y el paso de Grootberg también iban a mano hasta el 24/08; ahora son puntos de
paso reales del D9 y salen solos.)*

**Los dos puntos del segundo fichero no tienen día ni orden asignado, a propósito** ❌ — ni la
geometría de la ruta ni el itinerario narrado sitúan a Khorixas o la puerta de Galton en un momento
concreto del viaje *(Galton, de hecho, ni siquiera se usa en la ruta final: exige reserva propia y
es un rodeo más largo hacia Okaukuejo, `13`)*. Sus coordenadas son reales; su fecha, no — mejor un
hueco reconocido, y aparte, que un día o un orden inventados.
