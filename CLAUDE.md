# Cómo está montado esto

Los `.md` numerados son la fuente de verdad. El PDF se genera desde ellos con `fuente/`; nada se
escribe a mano en el PDF. Todo en castellano, precios siempre en **N$ y €** a la vez, y cada dato
con su marca: **✅** fuente primaria · **◐** secundaria concordante · **○** práctica común, sin
fuente · **❌** sin verificar. Un hueco reconocido vale más que un número plausible.

## El build

```
cd fuente
make            los tres PDF
make dossier    solo el dossier
make fauna      solo la guía de campo
make lamina     solo la lámina de ruta (A2, una hoja)
make avistam    recuentos de GBIF y porcentajes por campamento
make mymaps     los CSV y el KML de `aparte/` para Google My Maps
make comprueba  las comprobaciones de abajo
make todo       de cero: imágenes, geometría, avistamientos, mapas y los tres PDF
```

La **lámina** (`lamina.py` → `mapa-ruta-namibia-2026.pdf`) es una hoja A2 suelta para imprimir: el
mapa de ruta grande, las quince etapas y una banda de reglas. No lleva ni un dato a mano — las
etapas salen de `trazado.ETAPAS` y los kilómetros de `geo/ruta.json`, igual que el mapa—, así que
cambiar una noche la actualiza sola. `imprimir.a_pdf` acepta `papel="A2"` para esto.

Hace falta Python 3 con `markdown-it-py` y `Pillow` —`pip install -r fuente/requirements.txt`—,
Google Chrome y `poppler-utils`. Chrome lo localiza `navegador.py`, que mira el PATH y **después
los `.app` de macOS**, donde Chrome nunca queda en el PATH: sin eso, en un Mac `mapa.py` escribía
los SVG y se saltaba los PNG sin decir por qué. El PDF lo imprime Chrome por CDP desde
`imprimir.py` —no `--print-to-pdf`, que no sabe poner números de página— en **dos pasadas**: la
primera maqueta para averiguar en qué página cae cada documento y la segunda escribe esos números
en el índice.

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
  `21`, pegado al `18`, y el `19`, pegado al `08`—. Y lo que no entra en el PDF está en
  `FUERA_DEL_PDF` —hoy solo el `16`— **o directamente en `aparte/`**, que es donde viven los
  documentos que dejan de ser del volumen *(el 25/08 se fueron ahí los desvíos y la decisión del
  CCF, que eran el `23` y el `24`)*: el PDF lleva la ruta que se va a hacer, no la deliberación de
  por qué es ésa ni las alternativas que se descartaron.

## La variante del CCF — `aparte/decision-del-ccf.md`, fuera del PDF

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

Que estén las 197 imágenes con licencia libre y autor, que el catálogo y los créditos cuadren, que
la geometría de la ruta esté completa, **que ningún porcentaje de avistamiento se quede sin su
muestra detrás** y que las 148 especies tengan recuento, que los dos PDF tengan las páginas que
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

Y que la **lámina de ruta sea UNA hoja A2** *(si se desborda salen dos y la segunda va medio
vacía; el margen es de pocos milímetros, así que cualquier línea de más en la banda de abajo lo
rompe)*. Y que **cada documento del PDF tenga su resumen en `RESUMEN`** de `dossier.py` *(el índice sale
mudo si falta y nada avisaba)*. Más las tres convenciones de arriba, que antes solo estaban
escritas: **ninguna tabla de markdown**, **el `%% ancho` en la segunda línea** del bloque Mermaid,
y **todo precio en N$ con su € al lado**.
Lo del euro se comprueba solo en los documentos que se leen sobre el terreno —`01`, `03`, `13`,
`18` y `21`— y en el cuaderno de reservas —`20`, que se lee con la tarjeta en la mano—, porque los de
investigación citan cifras para desmentirlas *(«N$150 es lo que repiten los blogs»)* y tarifas que
no nos aplican: exigirles el euro llenaría la comprobación de avisos falsos, y una comprobación
que grita sin motivo se acaba ignorando.

Las mismas comprobaciones corren solas en cada push (`.github/workflows/comprueba.yml`). No
regeneran los PDF —eso pide Chrome y red—: vigilan que lo commiteado sea coherente.
