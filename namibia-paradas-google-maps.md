# Paradas de la ruta, para Google My Maps

*Documento de consulta aparte — sin enlazar todavía desde el README ni desde ninguno de los dos
PDF.*

📍 **[El mapa ya montado, en Google My Maps](https://www.google.com/maps/d/u/0/edit?mid=1MQI8k4r_mCZwAcnhjcCBGndU-yHECHI&usp=sharing)**
— ábrelo directamente, o entra desde la app Google Maps del móvil en "Tus lugares" → "Mapas".

**[namibia-paradas-google-maps.csv](namibia-paradas-google-maps.csv)** — el fichero de origen: 38
puntos de la ruta con coordenadas, dónde se duerme cada noche, lo que se visita, las puertas de
parque con horario, los puertos de montaña y las gasolineras que el dossier marca como
obligatorias. Sirve para reimportar si el mapa de arriba se pierde o hace falta rehacerlo.

## Cómo importar

1. Entra en [mymaps.google.com](https://mymaps.google.com) y crea un mapa nuevo (o abre uno que
   ya tengas del viaje).
2. **Importar** → sube `namibia-paradas-google-maps.csv`.
3. Cuando pregunte qué columnas son la posición, marca **Latitud** y **Longitud**.
4. Cuando pregunte qué columna usar como título de cada chincheta, marca **Nombre**.
5. Opcional: en **Estilo de capa**, elige "Estilo uniforme" → "Agrupar lugares por columna" →
   **Categoría**. Google My Maps le pone automáticamente un color e icono distinto a cada grupo
   (dónde se duerme, lo que se visita, puertas, puertos, ciudades y gasolineras), sin tocar nada
   a mano.
6. La app **Google Maps** del móvil sincroniza sola los mapas guardados en My Maps — no hace
   falta enlace nuevo ni exportar otra vez: abre "Tus lugares" → "Mapas" en el móvil y ahí está.

## De dónde salen los datos — cero fabricación

Las 34 coordenadas base son las que ya usa este mismo repo para dibujar sus propios mapas y
calcular la ruta real por carretera: `fuente/trazado.py`, geocodificadas con OpenStreetMap
(Nominatim y Overpass) el 04/08/2026 — no son una estimación nueva ni aproximada. Las columnas
**Días de la ruta** y **Noche aquí** salen de cruzar esas coordenadas con `fuente/trazado.py` →
`ETAPAS`, el itinerario día a día que ya usa `geodatos.py` para pedirle a OSRM el trazado real de
cada etapa.

Tres puntos —**Deadvlei**, **Palmwag** y el **paso de Grootberg**— no son ancla de enrutado OSRM
(el camino pasa por ellos sin necesitar un punto de paso aparte para que la ruta salga bien), así
que el cruce automático los dejaba sin día: se completaron a mano contra
[`01-itinerarios-dia-a-dia.md`](01-itinerarios-dia-a-dia.md) (Deadvlei, D4; Grootberg y Palmwag,
tramo D8 Twyfelfontein→Hoada).

**Tres puntos se quedan sin día asignado, a propósito** ❌ — ni la geometría de la ruta ni el
itinerario narrado los sitúan en un día concreto: **Torra Bay**, **Khorixas** y la **puerta de
Galton** (esta última ni siquiera se usa en la ruta final — Galton no conecta con la red principal
del parque hacia Okaukuejo, `13`). Sus coordenadas son reales y están en el CSV para tenerlas en el
mapa, pero sin fecha porque no hay fuente que la confirme — mejor un hueco que un día inventado.
