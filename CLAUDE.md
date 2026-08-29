# Cómo está montado esto

Los `.md` numerados son la fuente de verdad. El PDF se genera desde ellos con `fuente/`; nada se
escribe a mano en el PDF. Todo en castellano, precios siempre en **N$ y €** a la vez, y cada dato
con su marca: **✅** fuente primaria · **◐** secundaria concordante · **○** práctica común, sin
fuente · **❌** sin verificar. Un hueco reconocido vale más que un número plausible.

## El build

```
cd fuente
make            los cuatro PDF
make dossier    solo el dossier
make fauna      solo la guía de campo
make lamina     solo la lámina de ruta (A2, una hoja)
make agenda     solo la agenda (el día a día del `01`, dos A4 por día: mapa y explicación)
make avistam    recuentos de GBIF y porcentajes por campamento (las 4 zonas de la ruta)
make mymaps     los CSV y el KML de `aparte/` para Google My Maps
make comprueba  las comprobaciones de abajo
make todo       de cero: imágenes, geometría, avistamientos, mapas y los cuatro PDF
```

La **lámina** (`lamina.py` → `mapa-ruta-namibia-2026.pdf`) es una hoja A2 suelta para imprimir: el
mapa de ruta grande, las quince etapas y una banda de reglas. No lleva ni un dato a mano — las
etapas salen de `trazado.ETAPAS` y los kilómetros de `geo/ruta.json`, igual que el mapa—, así que
cambiar una noche la actualiza sola. `imprimir.a_pdf` acepta `papel="A2"` para esto.

Desde el 28/08 su mapa es `mapa.mapa_lamina()`, no el `mapa_ruta()` del README: **la línea va por
firme, no por bloque del viaje** *(el bloque ya lo dice el color de la tira de etapas)*, con la
misma paleta que el mapa del día de la agenda y **una capa más, la arena**: los ~5 km del
aparcamiento 2WD a Sossusvlei y Deadvlei, que OSRM no enruta, se trazan rectos desde el final del
asfalto del D4 (`mapa.arena_sossusvlei`) — el único firme del viaje que no sale del enrutado.
Encima van **los escudos de carretera** *(`rotulos_carreteras`: un escudo por tramo largo con el
mismo `ref`, uno cada ~150 km en los muy largos, nunca dos del mismo número a menos de 60 km y
ninguno dentro de Etosha, donde es pista)*, **las distancias entre paradas** *(`tramos_entre_paradas`:
medidas sobre la geometría de OSRM entre los puntos de `por`, sin cortar en los puertos de montaña
—Palmwag → Hoada son 52, no 26 + 26— y sin rotular la vuelta de la excursión de Sossusvlei, que iría
sobre la ida)* y **las gasolineras** de `trazado.GASOLINERAS`, que son **las del `01` §gasolineras y
solo esas**, en tres estados: obligatoria (surtidor lleno), opcional (vacío) y «no cuentes con
ella» (tachado). Los escudos van al 50 % de su carretera y las distancias al 33 % de su tramo para
no pisarse; lo que aun así choca se aparta a mano en `DESVIO_DISTANCIA`, `DESVIO_ESCUDO` y
`POS_GASOLINERA`. La tira de abajo lleva, bajo cada etapa, sus carreteras y sus km por firme
(`lamina.carreteras_del_dia`, `firme_texto`); para que cupiera, el mapa bajó de 384 a 372 mm.

Hace falta Python 3 con `markdown-it-py` y `Pillow` —`pip install -r fuente/requirements.txt`—,
Google Chrome y `poppler-utils`. Chrome lo localiza `navegador.py`, que mira el PATH y **después
los `.app` de macOS**, donde Chrome nunca queda en el PATH: sin eso, en un Mac `mapa.py` escribía
los SVG y se saltaba los PNG sin decir por qué. El PDF lo imprime Chrome por CDP desde
`imprimir.py` —no `--print-to-pdf`, que no sabe poner números de página— en **dos pasadas**: la
primera maqueta para averiguar en qué página cae cada documento y la segunda escribe esos números
en el índice.

## La agenda, que es el `01` y nada más

`agenda.py` → `agenda-namibia-2026.pdf`: portada y **cada día en su página, con su mapa**, para la
guantera. No se escribe nada a mano: corta el `01` entre `### D1` y el final del `### D15`, quita
lo que es del dossier y no del día —las líneas de temperatura y de fauna del campamento, las notas
de fuente y decisión entre paréntesis, las remisiones a `aparte/`— y desenvuelve los enlaces,
porque en papel no hay a dónde saltar.

**El mapa del día** (`mapa.mapa_dia`) pinta el recorrido **por firme** —asfalto, grava, sal
compactada o pista de parque— a partir de `geo/tramos.json`: es otra descarga de OSRM sobre las
mismas etapas, pedida con `steps=true`, que devuelve el `ref` de cada tramo (B1, C24, D1261…). OSRM
público no expone el `surface` de OSM, pero **en Namibia la letra manda** —B asfalto, C y D grava—
y las excepciones son las que el dossier ya documentaba una a una: van todas en `trazado.FIRME`
*(C34 asfaltada hasta Henties Bay y sal después, C40 asfaltada solo Outjo–Kamanjab, la carretera
de Sossusvlei asfaltada hasta el 2WD…)*. La ficha del mapa da los kilómetros por firme y el tiempo
**mínimo a las velocidades del `13`** (100/80/60) y el **realista como banda** —grava a 60–70 de
media real y 30–60 min de paradas—, que es el convenio del `13` tal cual, aplicado tramo a tramo:
así la ficha envuelve el «~4h30» del `01` en vez de dar otra cifra. Un firme de menos de 1 km no
hace fila, y el D4 avisa de los ~5 km de arena de Sossusvlei que OSRM no enruta. `make comprueba` exige que
`tramos.json` cubra los mismos días y kilómetros que `ruta.json` —si se mueve una noche y no se
regenera, el mapa pinta el recorrido de antes— y que **ningún tramo de más de 8 km quede sin firme
en la tabla**.

**Cada día son DOS páginas, exactamente**: la primera el mapa con, debajo, **lo opcional del día**,
y la segunda la explicación a dos columnas. `make comprueba` exige las páginas que dice
`agenda.paginas_esperadas()` —portada, dos por día y las de más de `agenda.PAGINAS_EXTRA`, que hoy
es solo el D4 con una tercera, ampliado el 28/08 a petición del viajero— y, si un día se desborda
más allá de eso, dice cuál. La lista de viñetas puede partirse entre páginas (`.cuerpo > ul`); si
no, la del D4, que va detrás de su diagrama, saltaba entera a la página siguiente y dejaba la
anterior en blanco.

**Lo opcional del día sale del `10`** *(desde el 27/08)*: `agenda.opcionales()` corta el `10` por
sus `### Dn` —el `10` tiene una sección por día, las quince, con el mismo encabezado que el `01`—
y se queda **solo con las viñetas**: cada viñeta es una joya con dónde cae, qué cuesta y cuánto
desvío añade. Los párrafos sueltos y las líneas «Fuentes:» del `10` son del dossier y no pasan.
Por eso en el `10` las viñetas son cortas y los porqués van en párrafo aparte. **El mapa cede
altura al bloque**: 800 px de alto para un día de dos joyas, 700 para uno de cuatro y 600 para el
D7, que lleva nueve (`agenda.alto_mapa`); si no, la lista saltaba entera a una tercera página, que es
lo que pasó la primera vez con el D5, el D7, el D8 y el D14.

**Los puntos de interés del mapa** —dónde comer, qué ver de paso, compras— son los que el `08` y el
`10` ya nombran; `geodatos.py interes` les pone coordenada **con Nominatim, nunca a ojo**, y los
cachea en `geo/interes.json` con el día en que se pasa. Lo que Nominatim no encuentra **queda fuera
del mapa y consta en el JSON**. Para
añadir uno, se añade a `INTERES` en `geodatos.py` y se regenera. Desde el 27/08 la tabla lleva las
joyas del `10` una a una y en su día *(Heroes' Acre, Vogelfederberg, Bird Rock, el Zeila, la torre
del Toscanini, Wondergat, el Damara Living Museum, Peet Alberts, el museo de Outjo, el de Tsumeb, la
Crocodile Farm, los meteoritos de Gibeon…)*; **sin coordenada, y por tanto fuera del mapa, quedan
seis**: el Urban Camp, Anchors @ the Jetty, el delta del Uniab, el lago Otjikoto, el memorial de
Khorab y el Telephone Man. Los desvíos que el `10` cita *(Petrified Forest +60 km, Hoba +93,
Peet Alberts +4)* se midieron metiendo el punto en la etapa de OSRM y restando.

## Convenciones que no se ven en el markdown

- **`%% ancho`** en un bloque Mermaid hace que el diagrama cruce las dos columnas del PDF. Mermaid
  lo lee como comentario y GitHub lo pinta igual. Va **en la segunda línea**, después de
  `flowchart …`, porque el tipo de diagrama se saca de la primera. Los `gantt`, `pie` y `timeline`
  ya cruzan solos: no caben en 89 mm.
- **`- [ ] item`** se dibuja como una casilla de verdad en el PDF, para marcarla a boli. Es lo que
  usa la lista de equipaje del `17`.
- **Nada de tablas.** Lo tabular se maqueta en rejilla (`<ol class="etapas">` en `dossier.py`) y lo
  visual va en Mermaid. Los diagramas verticales largos se comen media página: mejor `flowchart LR`.
- **El orden del volumen es el del número del fichero**, salvo lo que diga `ORDEN` en `dossier.py`
  —hoy el `20`, que se lee pegado al `04`; el `17`, pegado al `05`; el `18`, pegado al `06`; el
  `21`, pegado al `18`; el `22`, pegado al `21`, y el `19`, pegado al `08`—. Y lo que no entra en el PDF está en
  `FUERA_DEL_PDF` —hoy solo el `16`— **o directamente en `aparte/`**, que es donde viven los
  documentos que dejan de ser del volumen *(el 25/08 se fueron ahí los desvíos y la decisión del
  CCF, que eran el `23` y el `24`)*: el PDF lleva la ruta que se va a hacer, no la deliberación de
  por qué es ésa ni las alternativas que se descartaron.

## La variante del CCF — `aparte/decision-del-ccf.md`, **archivada** desde el 26/08

⚠️ **El desvío al CCF se descartó el 26/08** *(el guepardo caza de día, y bajar allí gastaba el D13,
que es el único día del viaje sin traslado en su mejor terreno — `aparte/plan-del-guepardo.md`)*. El
documento y su maquinaria **se conservan como registro**, no como plan: si algún día vuelve, está
todo montado y comprobado. Lo que sigue describe cómo funciona esa maquinaria.

Ese documento no es prosa: tiene **sus propias quince etapas** en `trazado.ETAPAS_ALT`, su geometría en
`geo/ruta-alt.json` —`python3 geodatos.py ruta-alt`— y **su propio mapa a escala de país**,
`mapa.mapa_ruta_alt()` → `img/mapas/ruta-alternativa.svg` y `.png`. El mapa va **con el mismo
encuadre y la misma escala que el oficial** a propósito: los dos se comparan poniéndolos uno al
lado del otro, y si el recorte no coincide la comparación miente.

⚠️ **La variante ya no es otra ruta: es UN cambio, el del final.** Hasta el 24/08 proponía además
Spreetshoogte con una noche y la suelta en Damaraland — **eso se adoptó y es la ruta oficial**. Lo
que queda en `ETAPAS_ALT` es idéntico a `ETAPAS` hasta el D12 y solo cambia el D13 y el D14: en vez
de la segunda noche de Onguma, se baja al CCF. Por eso las dos listas comparten sus primeras doce
etapas — si se toca una, hay que tocar la otra.

Tres cosas que no se ven:

- **El mapa entra DENTRO del documento**, no en las páginas de mapas del principio. En el markdown
  va como `<img>` —para que GitHub lo pinte— y `dossier.MAPAS_EN_DOC` lo cambia por el **SVG en
  línea** al montar el PDF, que sale vectorial y no depende de que el PNG esté generado. La clase
  `.mapa-doc` cruza las dos columnas: a 89 mm la leyenda es ilegible.
- **Los puntos de la variante no van al GPS.** `ccf` vive en la misma tabla `PUNTOS` —para que el
  mapa lo rotule con el mismo código— pero `trazado.SOLO_VARIANTE` lo saca del GPX y del KML: esos
  son de la ruta que se va a conducir, y un waypoint del CCF en el GPS es una invitación a salir de
  Etosha por donde no toca.
- **Su día a día se comprueba contra su geometría** *(abajo)*, igual que el del `01`. Es el mismo error que ya
  costó una tarde con las tartas: dos sitios contando la misma ruta y nada obligándolos a coincidir.

## Lo que se importa en Google My Maps

Los tres ficheros de `aparte/` que se suben a My Maps —`namibia-paradas-google-maps.csv`,
`namibia-puntos-sin-dia-confirmado.csv` y `namibia-trazado-carreteras.kml`— **son derivados, no
fuente**: los escribe `mapas_google.py` (`make mymaps`) desde `trazado.ETAPAS` y `geo/ruta.json`.
Se mantenían a mano hasta el 24/08 y al mover una noche se quedaban contando la ruta de antes sin
que nada avisara. Los puntos que la ruta pisa pero que **no son ancla de enrutado OSRM** —hoy
Deadvlei y Torra Bay— no aparecen en ningún `por`, así que llevan su día escrito en la tabla
`A_MANO` del propio script; es el único sitio donde se dice a mano en qué día cae un punto.

## La guía de fauna es SOLO de los sitios a los que se va

`guia-fauna-namibia.pdf` —antes `guia-fauna-etosha.pdf`, que mentía: cubre cuatro zonas, no un
parque— lleva **159 fichas y todas caen en la ruta**. La regla del 09/08 *(sin avistamientos, sin
ficha)* manda entera, y **desde el 29/08 está comprobada y no solo escrita**: `comprobar.revisa_ruta`
exige que **cada ficha tenga al menos un registro de GBIF dentro de alguna de las cuatro zonas del
viaje**, y lo que no lo tenga va en `catalogo.EXCEPCIONES_RUTA` **con su motivo escrito** *(hoy una
sola: el shongololo, que no está en GBIF porque nadie sube milpiés)*.

⚠️ **Esto se aprendió el 29/08 haciéndolo mal.** Ese día entraron **24 fichas del Zambeze, el
Okavango y el Kalahari** —hipopótamo, licaón, sable, búfalo, suricata, pangolín— en una «parte 2»
rotulada «lo que este viaje no pisa». **Se deshizo el mismo día, y el motivo es la regla**:
rotularlo no arregla nada, porque en la guantera ocupa sitio una guía de un viaje que no se hace.
Con ellas se fueron tres que tampoco llegaban al umbral de la ruta *(gecko gigante del suelo, 1
registro de oct-nov; duiker común, 5; ballena franca austral, 3 y se va antes de noviembre)*.

Lo que sí se quedó de aquel barrido son **once fichas que faltaban y son de la ruta**: la cebra de
Hartmann *(23 registros de oct-nov en Etosha, 8 en el Namib, 7 en Damaraland — cierra el hueco que
la auditoría del 28/08 dejó reconocido)*, cinco casi endémicos del oeste que caen en Damaraland
*(alcaudón de cola blanca 74, carbonero de Carp 83, papamoscas herero 27, cantor de roca 24,
francolín de Hartlaub 19)*, la alondra de Gray *(192 en la costa)*, tres bichos de mar que estaban
en la caja de Walvis Bay *(alcatraz 228, cormorán de las bancas 65, pingüino 65)* y la grulla
carunculada *(18 dentro de Etosha, aunque su casa sea el Okavango)*.

## La línea «En la ruta» de cada ficha, y su mapa

La línea que cierra cada ficha reparte sus registros de GBIF entre **las cuatro zonas del viaje** y
pone **el día al lado** — *«Damaraland (D8–D9) 83 · Etosha (D10–D13) 24…»*. La de arriba da **una**
cifra y la de **una** zona, la mejor; ésta abre el reparto, que es lo que contesta la pregunta del
que conduce: **en qué día toca buscar esto**. Sale de `guia_fauna.en_la_ruta()` y del mismo
`geo/avistamientos.json` que la de arriba: **ni una consulta más ni un fichero más**.

El mapa que la sitúa es `mapa.mapa_zonas()` → `img/mapas/zonas-fauna.svg` y `.png`: las cuatro
zonas con la ruta encima y cuántas fichas tienen su grueso en cada una *(Etosha 97, la costa 31,
Damaraland 18, el Namib 6)*. **Se dibuja desde el WKT que `avistamientos.py` cacheó**, no desde una
geometría aparte: si la caja cambia, el mapa cambia con ella y la ficha no puede separarse del
dibujo. Va dentro de la guía *(SVG en línea)* y dentro del `09` *(vía `dossier.MAPAS_EN_DOC`)*.

## Las posibilidades de avistamiento

La línea de «qué posibilidades hay» de la guía de fauna **no se escribe a mano**: sale de
`avistamientos.py`, que baja dos cosas y las cachea en `geo/avistamientos.json` —los partes de
avistamiento por campamento de Expert Africa, que son una probabilidad de verdad, y los recuentos
de GBIF dentro del polígono de cada zona filtrados a octubre y noviembre, que **no lo son**—. Las
dos van con etiquetas distintas a propósito: la primera dice «82 % lo vio», la segunda dice
«frecuente» o «escasa» y nunca «lo vas a ver».

Tres reglas que ya costaron una recalibración: la zona se elige por **registros absolutos**, no
por porcentaje *(si no, siete registros en Damaraland se convertían en «lo vais a ver»)*; por
debajo de 10 registros de la especie o 120 de su clase **no se afirma nada**; y desde el 09/08,
**la guía no lleva animales que nadie vio**: lo que la fuente sitúa fuera de la ruta o con 0 %
medido de avistamiento sale del catálogo *(el mecanismo `FUERA_DE_RUTA` de banda forzada queda
vacío, por si algún día vuelve a hacer falta)*. **Una sola excepción consciente, desde el 15/08**:
el gato de patas negras entra con banda «Sin registros» porque el viajero pidió *todos* los
felinos y la ficha sirve para no confundirlo con el gato montés — está escrito en la intro de
Felinos y en el `09`; no es precedente para otras.

De ese mismo cache sale, sin tocar la red, **el estudio de las charcas de
`aparte/charcas-de-los-campamentos-de-etosha.md`** —`make charcas`, `estudio_charcas.py`—: los siete
campamentos de Etosha que nombra el repo, con **el intervalo de Wilson al 95 % detrás de cada
porcentaje**, porque los tres campamentos medidos tienen 149, 48 y 16 viajeros y comparar los
porcentajes pelados hace decir tonterías. *(Puestos los intervalos, de catorce especies **solo
sobreviven tres diferencias**: el leopardo de Moringa, el guepardo de Namutoni y el rinoceronte
negro de Okaukuejo. El resto es ruido, el león incluido.)* No se escribe a mano: se regenera.

Los felinos y las rapaces van en **secciones propias** del catálogo (`FELINOS`, `RAPACES`) desde
el 15/08. Al añadir especies al catálogo, `python3 avistamientos.py` **solo baja lo que falte**
(`completa()`), sin rehacer el resto ni volver a raspar Expert Africa; los denominadores por clase
y zona se quedan como estaban a propósito, para que todas las fichas compartan la misma foto de
GBIF. `--forzar` lo rehace todo.

## La trampa que costó una tarde

Si **cualquier cosa** se sale del ancho de la columna —una URL larga sin partir, un diagrama
demasiado ancho— Chrome ensancha la caja para que quepa, abre una tercera columna en la página y
después **encoge el PDF entero** para meterlo en el A4. El documento sale a dos tercios de tamaño y
no avisa de nada: parece un problema de diseño de la portada. Por eso `.doc` lleva
`overflow-wrap: break-word` y por eso `make comprueba` mide el alto de la portada.

## Qué comprueba `comprobar.py`

Que estén las 208 imágenes con licencia libre y autor, que el catálogo y los créditos cuadren, que
la geometría de la ruta esté completa, **que ningún porcentaje de avistamiento se quede sin su
muestra detrás**, que las 159 especies tengan recuento y **que ninguna sea de fuera de la ruta**, que los PDF tengan las páginas que
deben, **que la portada mida sus 267 mm** —si mide menos, Chrome ha encogido el documento— y que el
README no mienta ni en el número de páginas ni en el índice de documentos.

Y **que el presupuesto cuadre consigo mismo**, que es lo que se coló tres días seguidos: las dos
tartas —la del README va **por persona** y la del `02` §1 **por pareja**— tienen que **sumar el
total que su propio documento anuncia**, ser **una el doble de la otra**, coincidir con la línea de
texto del desglose, y cuadrar con los **cuatro cubos de solidez del `02` §11** y con la resta de
«todo lo demás junto». *(Al cambiar una noche de Namutoni por Onguma se actualizó la prosa y no las
tartas: el README repartía €3.982 bajo un titular de €3.990 y los dos desgloses parecían correctos
de un vistazo. Cerrar algo obliga a subirlo de cubo **y** bajarlo del suyo.)*

Y que el **día a día de `aparte/decision-del-ccf.md` cuadre con la geometría de su variante** —cada etapa con 1 km de
tolerancia, porque cada una se redondea por su cuenta; el titular contra la suma de verdad; la
resta contra la oficial; y que el mapa que el documento enlaza exista en disco—. *(Ese documento escribe
las quince etapas a mano y dibuja el mapa desde `ruta-alt.json`: sin esto, tocar `ETAPAS_ALT` movía
el mapa y dejaba la prosa contando los kilómetros de antes.)*

Y **que sus tiempos salgan de su propio desglose de firme**: toda etapa que declare un
tiempo tiene que decir sus kilómetros de **asfalto, grava y parque**, el reparto tiene que sumar los
km de la etapa, y el mínimo tiene que ser exactamente el que dan las velocidades del `13` *(100, 80
y 60)*. *(Daba «289 km · ~3 h 35» y «294 km · ~3 h 40»: la misma velocidad para una etapa
que arranca dentro del parque y otra que es B1 entera, sin salir ni de OSRM ni del convenio. Una
comprobación de banda no lo caza —80 km/h cae dentro de todo—; lo único que lo caza es exigir que el
tiempo cuadre con el firme.)*

Y que **la chapa de reservas del README cuadre con las casillas tachadas del `20` §9**, cuyo
reparto vive en `RESERVAS_CONTADAS` de `comprobar.py` *(la casilla de Etosha vale por cuatro
noches)*: al reservar o anular algo hay que tocar **la casilla y la chapa**, y si cambia el conjunto
de reservas que hacen el viaje, también esa tabla.

Y que la **agenda tenga exactamente las páginas que dice `agenda.paginas_esperadas()`** —portada,
dos por día y una más para el D4, hoy 32— y, si sale una más, que diga qué día se ha desbordado
*(el D7 fue el que se desbordó el 25/08)*.

Y que la **lámina de ruta sea UNA hoja A2** *(si se desborda salen dos y la segunda va medio
vacía; el margen es de pocos milímetros, así que cualquier línea de más en la banda de abajo lo
rompe)*. Y que **cada documento del PDF tenga su resumen en `RESUMEN`** de `dossier.py` *(el índice sale
mudo si falta y nada avisaba)*. Más las tres convenciones de arriba, que antes solo estaban
escritas: **ninguna tabla de markdown**, **el `%% ancho` en la segunda línea** del bloque Mermaid,
y **todo precio en N$ con su € al lado**.
Lo del euro se comprueba solo en los documentos que se leen sobre el terreno —`01`, `03`, `13`,
`18`, `21` y `22`— y en el cuaderno de reservas —`20`, que se lee con la tarjeta en la mano—, porque los de
investigación citan cifras para desmentirlas *(«N$150 es lo que repiten los blogs»)* y tarifas que
no nos aplican: exigirles el euro llenaría la comprobación de avisos falsos, y una comprobación
que grita sin motivo se acaba ignorando.

Y cuatro más que estaban sin escribir aquí: que **el día a día del `01` cuadre con OSRM**
*(`revisa_dia_a_dia`: cada `### Dn` con kilómetros contra `geo/ruta.json` — la gemela de la de la
variante)*; que **el GPX y el KML lleven la misma ruta** que `ruta.json` **y que el README cuente sus puntos y
sus pistas bien** *(decía «las 13 etapas» con 14 dentro desde que el día de llegada pasó a ser el D1:
los PDF tenían su comprobación de páginas y esto no)*; que **la cuenta atrás del
README cuadre con la fecha que él mismo declara, y que esa fecha sea la que imprimen los tres PDF**
—vive en `fuente/fecha.py` y de ahí la leen `dossier.py`, `agenda.py` y `lamina.py`, porque el
26/08 cada uno llevaba la suya y salieron con tres fechas—; que **el `01` conserve los dos
encabezados entre los que `agenda.py` recorta el día a día**; y que **los 22 documentos tengan
título**.

Y **que el sol y la luna del `01` salgan del cálculo y no de la memoria** *(desde el 28/08)*: los
quince amaneceres, los quince ocasos y la fracción iluminada de cada noche se recalculan en
`fuente/astro.py` —**algoritmo solar de la NOAA** con cenit 90,833° y **series de Meeus** para la
fase, sin red ni dependencias— y `revisa_sol_y_luna` los cotea línea a línea contra el markdown,
sacando el sitio del propio texto *(«amanecer **06:18** (Cape Cross)»)* y, cuando no lo nombra, de
donde se duerme esa noche. Tolerancia de 4 minutos y de 2 puntos de luna. **Si el formato cambia y
el patrón deja de encontrar horas, falla en vez de callar.** *(Las horas ya estaban bien —las
veintisiete cuadran—; la luna no: iba con «conjunción de referencia + mes sinódico» y se quedaba
3–7 puntos alta en toda la menguante, así que las noches del viaje son más oscuras de lo que decía
el dossier.)*

**Y la regla que se aprendió el 26/08: una comprobación que no puede correr FALLA, no calla.** Sin
`pdftoppm` o sin Pillow, la de la escala devolvía `ok`; la de las páginas del README daba `ok` cuando
su patrón no encontraba nada *(le pasaba con la lámina, que no dice «páginas» sino «una sola hoja»)*;
dos cuadres del presupuesto se saltaban si su literal desaparecía. Todas gritan ahora. Si una
comprobación depende de un literal del markdown y el literal cambia, tiene que avisar de que se ha
quedado ciega — un tick verde sin haber medido es peor que ninguna comprobación.

Las mismas comprobaciones corren solas en cada push (`.github/workflows/comprueba.yml`). No
regeneran los PDF —eso pide Chrome y red—: vigilan que lo commiteado sea coherente.
