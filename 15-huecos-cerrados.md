# 15 · Cómo se verificó esto

> **Namibia · 30 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](README.md)
>
> Los datos duros del dossier con su fuente y su método: temperaturas de estación, viento, tasas,
> vuelos y lodges. Y al final, **la lista de lo que sigue sin cerrar**.
>
> **~N$20 = €1** *(rango 19,5–20,5)* · **✅** fuente primaria · **◐** secundaria concordante ·
> **○** práctica común, sin fuente · **❌** sin verificar, dicho en blanco
>
> *Investigación cerrada el 17/07/2026 · formato y contenido revisados el 09/08/2026*

> ### La regla de la casa
> **Todas** las temperaturas que circulaban por webs de safaris fueron **refutadas 0–3**. Las de aquí
> son **cálculo propio sobre ficheros de observación descargados** —NOAA GHCN-Daily y GSOD, y el
> reanálisis ERA5— no cifras copiadas. Donde no hay medición, **se dice en blanco**.
>
> *Aparecen estaciones del sur —Keetmanshoop, Karios— aunque el sur ya no esté en la ruta: son las
> series largas contra las que se comprueba si el reanálisis miente. Son instrumento de medida, no
> destino.*

---

## 🌡️ Temperatura — el hallazgo que invalida las webs de safaris

> ### El *«suicide month»* depende de la latitud. En Etosha octubre SÍ es el pico. En la costa, no.

```mermaid
flowchart LR
    T["Media de maximas de noviembre<br/>donde duermes · grados C"]
    n0["Costa · Walvis Bay<br/>25,0 dia / 12,7 noche"]
    n1["Windhoek<br/>31,2 / 16,3"]
    n2["Sesriem · desierto<br/>32,5 (ERA5)"]
    n3["Etosha · Okaukuejo<br/>37,1 / 18,9"]
    T ~~~ n0
    n0 ~~~ n1
    n1 ~~~ n2
    n2 ~~~ n3
    style T fill:#7a3a22,color:#fff,stroke:#7a3a22
```

**Etosha (Okaukuejo)** ✅ — estación `WA010517310`, serie **1975–2022**: octubre **37,8** · noviembre
**37,1** · diciembre **35,6 °C** de media de máximas; **mínimas de noviembre 18,9 °C**. Recalculado
dos veces de forma independiente, coinciden en 0,2 °C. **Octubre es el pico del norte, y bajando.**

**La costa (Walvis Bay)** ✅ — estación del aeropuerto `WAM00068098`, serie **1990–2025**. Es la
primaria más cercana a Swakopmund, a 30 km bajo la misma corriente de Benguela:

- sep **22,7** → oct **23,8** → **nov 25,0** → dic **25,4** → ene **26,1 °C**
- **mínimas de noviembre 12,7 °C** *(la madrugada más fría del viaje)*
- récord de noviembre 38,9 °C (2010), un *berg wind* aislado — manda la media

**Windhoek** ✅ — estación `68110`, 1.700 m, serie **1957–2025**: oct **30,5** · **nov 31,2** · dic
**32,1 °C**; mínimas de noviembre **16,3 °C**. Cálido de día, pero a 1.700 m refresca de noche.

**Sesriem** ◐ — **no existe estación que lo mida**, y eso está verificado, no supuesto: descargado el
inventario completo de GHCN, **Namibia tiene 11 estaciones con serie de máximas** y ninguna cae
cerca *(la más próxima, Gobabeb, está a 128 km y a 600 m menos de altitud)*. El **reanálisis ERA5**
le pone **~32,5 °C**, y el dato ◐ de NWR daba **34,1 / 15,5** — **coinciden en el entorno de
32–34 °C**.

> **La conclusión que importa:** «octubre es el peor mes» **solo vale para el interior norte**. En la
> costa el calor sube despacio de septiembre a enero. Por eso este dossier no usa medias nacionales.

**Fuente:** NOAA GHCN-Daily en AWS S3 —
`https://noaa-ghcn-pds.s3.amazonaws.com/csv/by_station/{ESTACION}.csv`— más `ghcnd-stations.txt` y
`ghcnd-inventory.txt`. Descargado y recalculado el 26/07/2026.

### 🛰️ Validado con un segundo dataset independiente ✅

**GSOD** (NOAA, partes de aeropuerto) es una red distinta de GHCN-Daily. En **Keetmanshoop**, que
existe en ambas, dan **exactamente lo mismo: 34,7 °C** de media de máximas de noviembre (2000–2024,
n≈620 días cada uno). Dos construcciones independientes, cero diferencia.

Y añade estaciones del eje norte: **Outjo 35,6 °C** *(camino de la puerta de Andersson)* ·
**Windhoek Eros 32,9** y **Hosea Kutako 32,1**.

> 💡 **Un matiz de método que conviene saber:** los 33,4 °C que el dossier tenía para Keetmanshoop
> eran la **normal de 68 años**; recortando la misma serie a 2000–2024 sube a **34,7**. La década
> reciente corre ~1,3 °C más caliente porque las décadas frías de mediados de siglo tiran de la media
> larga. **Ojo: no se puede generalizar** — en Okaukuejo ese salto no existe, porque su serie empieza
> en 1983 y ya es «reciente». Es un efecto de longitud de serie, no un calentamiento uniforme.

**Fuente:** NOAA GSOD en S3 — `https://noaa-gsod-pds.s3.amazonaws.com/{AÑO}/{ID}099999.csv`. Filtro
de calidad: se descartan máximas >45 °C por implausibles *(afectó a 5 días de 440 en una sola
estación, y mueve la media 0,1 °C)*.

### 🌍 ERA5 — el reanálisis, y cuánto se puede fiar uno ◐

Donde no hay estación, la única fuente que cubre cualquier punto del planeta es el **reanálisis**:
ARCO-ERA5 (ECMWF), rejilla de 0,25° ≈ 28 km. **No es una observación: es un modelo**, por eso va en
◐. Método: máximo de las horas 10–17 UTC de cada día, promediado sobre **9 noviembres (2013–2021)**,
n=270 días por punto.

**Contrastado contra estaciones reales**, el error no es uniforme:

- **Windhoek** — ERA5 31,0 vs GHCN 31,2 → **−0,2 °C**, casi idéntico
- **Keetmanshoop** — ERA5 33,9 vs 33,4/34,7 → **dentro de ±0,8 °C**
- **Walvis Bay** — ERA5 25,8 vs 25,0 → **+0,8 °C**, algo cálido *(la celda mezcla mar y tierra)*
- **Okaukuejo** — ERA5 35,2 vs 37,1 → **−1,9 °C**, aquí sí se queda corto

> **Lectura honesta:** ERA5 clava la meseta interior, va ~1 °C cálido en la costa y ~2 °C frío en la
> sabana seca. **El sesgo no se puede corregir con una constante**, así que las cifras se publican
> tal cual, avisando de hacia dónde tira el error en cada terreno.

### 🆕 Cerrados dos de los tres puntos sin estación: Spreetshoogte y Hoada ◐

**Método idéntico al de arriba, y validado antes de fiarse de él.** Se recalculó ERA5 con la misma
receta —máximo diario de las horas **10–17 UTC**, mínimo de las **00–07 UTC**, promediado sobre los
**9 noviembres 2013–2021 (n=270 días)** del mismo fichero ARCO-ERA5— y **primero se comprobó que el
cálculo reproduce los números ya publicados** en las celdas conocidas:

- **Windhoek** — recalculado **31,0** vs el 31,0 de arriba → **Δ +0,03 °C**
- **Okaukuejo** — recalculado **35,2** vs 35,2 → **Δ +0,04 °C**
- **Sesriem** — recalculado **32,5** vs 32,5 → **Δ −0,01 °C**

Tres regímenes distintos (meseta, sabana, desierto) clavados a **±0,04 °C**: el mismo tubo de
cálculo aplicado a los puntos sin medir es fiable. Con eso:

- 🏔️ **Spreetshoogte** *(campamento del D1–D2, borde de la escarpa ~1.700 m)* — **media de máximas de
  noviembre 31,5 °C / mínima 17,1 °C** ◐ *(ERA5, celda −24,00 / 16,00)*. **Corrobora el proxy de
  Windhoek** que ya usaba `01`: misma altitud, mismo clima de meseta. Días extremos de la serie
  entre 22,5 y **38,0 °C**. Como es meseta —el terreno donde ERA5 apenas tiene sesgo— el número se
  puede tomar casi tal cual.
- 🔥 **Hoada / Grootberg** *(campamento del D8, Damaraland)* — **media de máximas 33,1 °C / mínima
  18,4 °C** ◐ *(ERA5, celda −20,00 / 14,00)*. Días extremos hasta **39,2 °C**. **Ojo al sesgo:**
  Damaraland es «sabana seca», el terreno donde ERA5 se quedó **~2 °C corto** en Okaukuejo, así que
  **el mediodía real de Hoada probablemente ronda 34–35 °C**, no 33. Trátese 33,1 como suelo, no como
  techo. Encaja con lo que decía `01`: entre la meseta (~31) y el norte caluroso, y con Twyfelfontein
  —en el valle, más abajo— aún más caliente a mediodía.

**El tercer punto, Terrace Bay, NO se puede cerrar así, y es un hallazgo en sí mismo.** Su celda ERA5
más cercana (−20,00 / **13,00**) cae **sobre el océano**: devuelve **~19,3 °C**, que es aire marino
sobre la corriente fría de Benguela, **no la temperatura en tierra del campamento**. Lo confirma el
control: la misma celda-más-cercana para **Walvis Bay dio 18,5 °C**, un absurdo frente a los **25,0
✅** de su estación —la celda es mar, no tierra—. Por eso, para la costa **sigue mandando el proxy de
estación real (Walvis Bay 25,0 ✅)** y no el reanálisis. Lo que ERA5 sí confirma de Terrace Bay es
que la capa marina la mantiene fría y estable *(máximos de la serie que no pasan de ~25 °C)*, en
línea con la niebla y el viento que ya se anotaban.

---

## 🌬️ Viento en la costa — y no es lo que su fama sugiere ✅

**Walvis Bay en noviembre promedia ~13 km/h** (GSOD, misma metodología). Es viento suave de media:
lo que molesta en la costa es la **niebla y el frío de madrugada**, no el vendaval. *(La fama ventosa
de esta costa viene de Lüderitz, 400 km al sur y fuera de la ruta.)*

## 🌅 Luz — superado por una fuente mejor

La ventana de luz se calculó por longitud para las fechas reales, y luego apareció algo mejor: **la
tabla oficial de horarios de puerta del parque**, que va con el orto y el ocaso. Para vuestras
fechas: **3–9 nov 06:13–19:06** y **10–16 nov 06:10–19:10**. El desglose día a día, con el sol de
cada parada, está en [`01`](01-itinerarios-dia-a-dia.md).

---

## 🎫 Tasas de parque 2026 — el precio subió, y mucho ◐

**Baremo del MEFT vigente desde el 1/04/2026**, localizado en el **Government Gazette nº 8877,
Government Notice nº 115**:

- **Adulto internacional: N$280 (~€14) por persona y día** = N$140 de entrada + N$140 de conservación
- Adulto SADC N$180 · namibio N$60 · **niño <8 gratis** en todas las nacionalidades
- **Vehículo hasta 10 plazas: N$60 (~€3)**

**Los tres parques de la ruta son «premium»** *(la tarifa alta)*: **Etosha, Namib-Naukluft** y
**Skeleton Coast**. Se cobra **por parque y por cada 24 h**, así que la ruta suma **7 unidades**.

> ⚠️ **Por qué esto sigue en ◐ y no en ✅:** la gaceta está localizada y las secundarias concuerdan,
> pero **el PDF primario del MEFT no se ha podido abrir** para verificar la tabla fina. Y ojo: una
> cifra de «N$75–150» que devolvió un buscador **está confabulada** — contradice a todas las demás.

---

## ✈️ Vuelos — cerrado en €1.450 (Oporto), y con qué se comparó

El billete del viaje está en [`02`](02-presupuesto.md) §8. Lo que sigue es el **contexto de mercado**
con el que se juzgó si ese precio era razonable, y la lógica de la fiebre amarilla:

- **Lufthansa vía Fráncfort y Múnich** — **la ruta elegida**, saliendo de **Oporto**. Una escala por
  sentido, **sin fiebre amarilla** *(ninguno de los dos hubs es zona de riesgo)*, y el largo radio
  parcialmente operado por **Discover Airlines**. Muestras de agregador anteriores la situaban en
  **~€673–715** ida y vuelta ◐ — el precio real del viaje, con equipaje y cargos, es **€1.450 p.p.**
- **Qatar vía Doha** ◐ — sin fiebre amarilla; rango gancho de agregador **desde ~€631** ida y vuelta.
- **Airlink (JNB–WDH)** y **TAAG (Luanda–WDH)** ◐ — son solo el **conector regional**: hay que sumar
  el largo radio desde Europa. TAAG es la única que hace Luanda–Windhoek sin escala (2 h 30).
- ⚠️ **Los hubs que sí obligan a vacunarse** son los que están en zona de fiebre amarilla. La ruta
  elegida los evita por completo, así que **el certificado no hace falta** *(el árbol de decisión,
  en [`04`](04-guia-preparacion.md))*.

> Todas las cifras de arriba son **ganchos «desde» de agregador, sin fecha concreta** ◐ — sirven para
> situar el orden de magnitud, no para reservar. El precio real del viaje se cotizó aparte.

---

## 🏨 Lodges privados y antelación de reserva

**Novedad (03/08/2026): el año tarifario que cubre el viaje YA está publicado.** El hallazgo
anterior decía que noviembre caía en un año tarifario nuevo «sin publicar»; **eso ha caducado**.
Gondwana Collection publica ya su tarifa **1 nov 2026 – 31 oct 2027** —el año exacto del viaje— en
las páginas de cada alojamiento. Confirmado el rango de fechas en **cinco búsquedas independientes**
sobre sus propias URL *(gondwana-collection.com/accommodation/…)*.

> ⚠️ **Pero la extracción NO está verificada, y por eso todo esto va en ◐, no en ✅.** Las páginas
> de Gondwana siguen devolviendo **`403`** al abrirlas directamente desde este entorno; los números
> de abajo vienen de **fragmentos («snippets») del índice del buscador**, resumidos por un modelo,
> **sin poder abrir la ficha para comprobar la extracción**. Y ese riesgo es real: una pasada devolvió
> «Etosha Safari Lodge N$445 pp» —un disparate— que otra pasada corrigió a ~N$3.790–6.060/noche.
> **Trátalos como pistas con URL, no como precios cerrados. Confírmalos por email o teléfono antes de
> presupuestar.**

**Tarifas candidatas para 1 nov 2026 – 31 oct 2027** *(◐ extracción sin verificar, página en 403)*:

- 🛖 **Damara Mopane Lodge** *(Damaraland, cerca de la ruta D8)* — **B&B ~N$2.970 por persona en
  habitación compartida (~€149)**. Fuente: página propia de Gondwana vía snippet. *(Es tarifa de
  alojamiento, distinta de sus actividades: rastreo de elefante N$3.300 pp, sendero autoguiado
  N$250 pp — que el buscador tiende a devolver primero.)*
- 🦁 **Etosha Safari Camp** *(chalets junto a la puerta de Andersson, EN la ruta)* — **~N$2.220–3.550
  por noche (~€111–178)**. Fuente: agregador `south-african-lodges.com`, no la web propia → ◐ más
  débil; lo da como «media», sin distinguir por persona vs por unidad.
- 🏨 **Etosha Safari Lodge** *(el hermano de gama alta, misma zona)* — **~N$3.790–6.060 por noche
  (~€190–303)**. Mismo agregador, misma cautela.
- ⛺ **Camping de los Roadhouse de Gondwana** — **N$300 por persona (~€15)** para 1 nov 2026 – 31 oct
  2027, dato de la página propia *(medido en Canyon Roadhouse; el sur ya no está en la ruta, pero
  fija el nivel del camping Gondwana para el año nuevo)*.

**Lo que sigue sin cerrarse:** la tarifa **DBB por noche de la web propia** de los lodges de la ruta
*(Sesriem: Desert Camp, Desert Quiver, The Desert Grace; Swakopmund; Twyfelfontein Country Lodge —
que NO es de Gondwana; puertas de Etosha: Taleni, Toshari)*. El buscador devuelve sus **actividades**
antes que el alojamiento, y el `403` impide leer la ficha. Como referencia de gama media namibia
sigue valiendo **~€75–170 por noche para dos ◐** (rango de agregador). *(Twyfelfontein Country Lodge:
un agregador da «desde ~$223 pp DBB» para may–oct 2026 ◐; sin cifra limpia para noviembre.)*

**Antelación** ◐: la temporada alta namibia es **julio–octubre**, y **noviembre es hombro**. El
cuello de botella no es la temporada: es **estructural**, porque **Sesriem tiene 44 parcelas** y es
la única forma de estar en Deadvlei al amanecer.

---

## 🦁 El safari de Etosha — decidido GUIADO ✅ *(08/08/2026)*

Criterio del viajero: *«el safari es un 90 % un buen guía»*. **3 salidas de mañana** (una por
campamento, N$650 pp ✅) + **el nocturno de Namutoni** (N$750 pp ✅) = **N$5.400 (~€270) la
pareja** — un extra de ~€97,50 p.p. sobre el plan anterior, que solo compraba el nocturno. Tarifa NWR verificada, **sin reservar**: horarios
de salida ❌ no publicados y pre-reserva incierta en temporada de lluvias — se cierra en
recepción (la pregunta a NWR está en el README, punto 7). Los traslados entre campamentos siguen
siendo con el 4x4. El análisis descartado, en `16` §7.

## 🐾 Dos fichas nuevas en la guía — añadidas *(08/08/2026)*

**Babuino chacma** *(56 registros GBIF en el Namib, 58 en Damaraland ✅ — cifras en el JSON
versionado; el «mono» real de esta ruta)* y **ballena jorobada** *(210 en la costa, 55 en
oct–nov ✅)*. La guía pasa de 83 a **85 fichas** y las imágenes de 120 a **122**, con licencia y
autor verificados. **Ampliación de la misma tarde (08/08): +6 fichas por barrido de ausencias
contra GBIF** — mangosta rayada *(400 registros en Etosha ✅ — el gran ausente)*, gaviota de
Hartlaub *(6.334 en la costa ✅)* y avoceta *(3.944 ✅)*, más el trío del nocturno guiado: zorro
del Cabo *(31/10)*, gato montés africano *(39/8)* y lobo de tierra *(10/1 — el caso «liebre
saltadora»: nocturno infrarregistrado, documentado en la propia guía)*. **Quedan fuera con
datos**: duiker *(16/5)* y liebre del Cabo *(3/1)*. Total del 08/08: 91 fichas / 128 imágenes.

**Poda del 09/08 — regla nueva del viajero: la guía no lleva animales que nadie vio.** Fuera el
**oricteropo** *(el 0 % medido en 149 partes — la cifra más honesta del método, y por eso mismo
descalifica la ficha)*, la **suricata** y la **cebra de Hartmann** *(las dos con la banda forzada
«fuera de la ruta»: la propia guía decía que no caían en el eje)*. Los avisos de identificación se
conservan en `09` y en la ficha de la cebra de Burchell; el 0 % del oricteropo se queda contado
como anécdota de método. **Total vigente: 88 fichas / 125 imágenes.**

**El archivo de la consulta puntual del 08/08/2026** *(API de GBIF sobre los polígonos de las
zonas; NO está en el JSON del build —que solo guarda totales y oct–nov— y por eso se deja aquí
mes a mes, ◐)*:

- **Jorobada, costa, por meses (ene→dic): 0 · 0 · 6 · 8 · 8 · 22 · 25 · 42 · 34 · 28 · 27 · 5**
  *(suma 205; los 5 registros restantes hasta los 210 de la zona van sin mes en GBIF)*
  → migración **jun–nov**, pico jul–sep, y noviembre todavía en temporada. El crucero del D6
  (5–6 nov) cae dentro.
- **Heaviside y mular**: registros repartidos por todos los meses — sin estacionalidad que
  planificar ◐.
- **Mono vervet** *(Chlorocebus pygerythrus)*: **sin un solo registro en las cuatro zonas** de la
  ruta → se descartó su ficha a propósito; habría sido el «plausible pero falso» que este repo
  prohíbe. *(No está en el catálogo, así que este cero no se re-genera con `make avistam`: vive
  solo aquí, con su fecha.)*

## 🧳 Franquicia de equipaje — cerrada ✅ *(07/08/2026)*

Era uno de los huecos del README *(«tres aerolíneas en la vuelta»)* y se cierra con fuente
primaria: **en un billete único del grupo Lufthansa, la franquicia es una para todo el itinerario
y la fija la tarifa, no cada operador**. Los tramos largos los opera **Discover Airlines** *(la
filial de largo radio de LH, que vuela Frankfurt/Múnich–Windhoek)* y aplica el reglamento de
equipaje del grupo: **Economy Classic = 1×23 kg (158 cm) por persona; Economy Light = ninguna;
cabina 8 kg + accesorio**. La única decisión real ya estaba avisada: **emitir con tarifa con
maleta**. Detalle y fuentes en [`02`](02-presupuesto.md) §8.

## 🌊 Mareas de Walvis Bay y 🌙 la luna — cerrados el 09/08/2026

- **Las mareas del D5–D7** *(Walvis Bay es el puerto patrón de la costa)* ◐ — leídas de la tabla
  de noviembre de 2026 de
  [tidetime.org](https://www.tidetime.org/africa/namibia/walvis-bay-calendar-nov.htm): **D5**
  bajamares 06:37 y 19:01 · **D6 — el día del tour: bajamares 07:18 y 19:38, pleamares 01:21 y
  13:27** · **D7** 07:54 y 20:12; el rango crece hacia las **mareas vivas del novilunio del 9**
  *(coherencia interna que respalda la tabla)*. Es **predicción comercial, no tabla náutica**
  *(las primarias —SANHO, Namport— no se abrieron desde aquí)*: vale para planificar la mañana
  del D6 —**la salida de Sandwich Harbour de las ~08:30 es la de la playa**—, no para navegar,
  y **el operador manda con su propia tabla**.
- **La fase lunar, calculada en casa** *(conjunción de referencia + mes sinódico; ±1 día en el
  instante)* — **luna nueva el 9–10 de noviembre**: las **cuatro noches de Etosha (D9–D12)
  entre el 0 y el 9 % de iluminación**, el amanecer de Deadvlei (D4) con un menguante del ~27 %,
  y la salida (D0–D2) con una menguante del 48–68 % que sale ya de noche. El día a día, en el
  bloque 🌙 de `01`.

## 🕳️ Lo que sigue sin cerrarse — la lista maestra *(al 09/08/2026)*

El inventario de huecos abiertos, para no tener que reconstruirlo leyendo todo el dossier.

**Bloquean algo con fecha:**

- ✈️ **El billete NO consta emitido** *(hay precio real, €1.450 p.p., cotizado el 05/08)*.
  **Sin billete no hay e-visa**, porque exige billete de vuelta.
- 🏕️ **Ninguna reserva consta hecha**: ni coche, ni Sesriem ×2, ni Terrace Bay *(sin ella no se entra
  al parque a pernoctar)*, ni las cuatro de Etosha — **ni las DOS de Spreetshoogte** *(decididas el
  08/08; su hueco doble quedó en sencillo el 09/08: **contacto localizado** —
  spreetshoogte@iway.na · +264 62 572 010 ◐, ver `21`— pero la **tarifa sigue sin verificar** ❌,
  una fuente lo marca «closed down» ◐ y `01` añade un cuarto nombre a la trampa: «Camp Gecko»)*.
- 🚗 **Recotizar el coche con las fechas decididas** *(31 oct 11:00 → 14 nov 18:00, 15 días,
  aeropuerto → aeropuerto; el 31-oct fuera de temporada baja ❌ y la entrega EN el aeropuerto sin
  confirmar ❌ — `02` §2)*.
- 🛡️ **Adelantar el seguro IATI al 30/10** *(la póliza cotizada empieza el 31; el coste del día
  extra ❌ sin cotizar — `02` §7–8)*.
- 💉 **La cita del Centro de Vacunación Internacional** — para salir el 30/10 hay que ser atendidos
  hacia el **19–26 de septiembre**. Se pide en agosto.
- 🪪 **El permiso internacional de conducir**: fuente ◐, y la DGT pide cita.

**Precios sin cerrar — el margen real del presupuesto:**

- 🛏️ **Tres campings sin cotizar**: Windhoek (D0 y D13), Walvis Bay (D5–D6) y Spreetshoogte (D1–D2, dos noches desde el 08/08). Los
  sitios están identificados; **ninguno publica tarifa abrible desde aquí**. **Reintento 05/08 —
  el muro de `403` es total**: no solo las webs propias, también **todos los agregadores y hasta
  ioverlander** *(arebbusch.com, africanreservations.com, madbookings.com, booking.com y
  ioverlander.com devuelven `403`)*, así que **la ficha no se puede abrir para comprobar la
  extracción**. Lo único que asoma son **fragmentos del índice del buscador, de un solo origen cada
  uno y sin verificar** — se anotan como pista **○, NO entran al presupuesto**:
  - **Urban Camp (Windhoek)** — el buscador da «desde ~R660–700 la noche para dos» *(booking.com,
    agregador, precio-gancho «desde»)* ≈ **N$660–700 (~€33–35) la pareja ○**. Encaja en la horquilla
    de práctica común que ya usa `02` (~N$600–1.000), así que **no la mueve**.
  - **Lagoon Chalets (Walvis Bay)** — un fragmento cita «N$600 la parcela para 1 coche + 2 personas»
    *(~€30 ○, origen único)*, pero **africanreservations marca «sin tarifas para 01 mar 2026 – 28 feb
    2027»**: corrobora que **para la ventana del viaje no hay tarifa publicada**. Queda en ○.
  - **Spreetshoogte** — ⚠️ **trampa de nombre viva**: hay al menos **tres** cosas llamadas
    «Spreetshoogte» junto al paso —el camping propio, **Namibgrens Guest Farm** y **Barkhan Dune
    Retreat**—, la misma confusión que ya dio el gancho de N$269,50 (Namibgrens). Los fragmentos dan
    «~N$120–150 por persona» *(~€6–7,50 ○, orígenes que se contradicen entre sí)*. **No se cierra**:
    sin abrir la ficha no se puede saber a cuál de las tres propiedades corresponde cada cifra. En
    `01` (D1–D2, dos noches desde el 08/08) sigue como está: 150–300 ZAR/persona, vigencia desconocida.
  > **Conclusión 05/08:** ninguno pasa el listón de «verifica la extracción, no solo la fuente». Los
  > tres siguen en la estimación de práctica común de `02`; **estos números son pistas con URL para el
  > que llame a reservar, no precios para presupuestar**.

  **Avance del 09/08** *(los contactos, con URL, en `21`)*: **Urban Camp** reserva por NightsBridge
  y su propia web confirma que **no publica número** ✅; **Lagoon Chalets** tiene teléfono y un
  portal le publica **camping «desde R700» ≈ N$700 (~€35) para dos** ◐; y **Spreetshoogte** tiene
  email y teléfono ◐ — con un aviso de «closed down» ◐ por confirmar. **Ninguna tarifa nueva
  verificada: los tres siguen en la estimación.**
- 💳 **La fianza que retiene Namibia2Go** en la tarjeta — **PARCIALMENTE CERRADO ◐ (05/08), con un
  conflicto sin resolver**: la propia Namibia2Go se anuncia como **«No Deposit»** *(sin fianza, a
  diferencia de casi todos los operadores)* y su FAQ dice que **no hay depósito de combustible**;
  pero un revendedor —madbookings— y un directorio —goArid— citan que **se retiene N$2.500 (~€125) de
  depósito de combustible**, liberado si devuelves el depósito lleno. Las dos versiones son de fuentes
  secundarias *(la web propia está en 403)* y **se contradicen**: puede ser un cambio de política o
  depender del canal de reserva. **No lo des por sentado en ningún sentido — pregunta por escrito, al
  reservar, si hay retención en tarjeta y de cuánto.** Aceptan todas las tarjetas salvo Diners y Amex.
- 🛟 La **opción de búsqueda y salvamento del IATI Estrella: ❌ sin cotizar** *(el Mochilero la
  trae de serie; pedirla por escrito está en el README, punto 6)*.
- 🚗 El **traslado A Coruña ↔ Oporto — decidido (09/08): en coche propio**. Sin cotizar ❌: el
  **aparcamiento de larga estancia** del aeropuerto (30 oct – 15 nov) y los peajes *(el bus
  directo, ~€17/persona y trayecto ◐, queda de plan B — `02` §8)*.
- 🛢️ La **capacidad real del depósito del Hilux de Namibia2Go**: **❌ sin confirmar** — y de ella
  cuelga la aritmética del bucle Henties Bay → Kamanjab (~740 km, 81–96 l — `07`). Pregunta de
  una línea al reservar.
- 🚤 *(Cerrado a nivel de mercado ◐: el **crucero de Walvis Bay** ~N$1.400–1.990 pp y el **4x4 a
  Sandwich Harbour** ~N$2.600–3.220 pp tienen rango 2026 en [`02`](02-presupuesto.md) §9 —
  cruzado entre operadores, con la ficha propia en `403`.)*
- 📱 ~~La **SIM de MTC**~~ **CERRADA ◐ (05/08)**: paquete turista **«Leisure» N$349 (~€17) / 14 días /
  10,1 GB** y **«Premium» N$659 (~€33) / 30 días / 20,1 GB**, solo en la tienda MTC del aeropuerto.
  *(Ojo al calendario: activada el 31 de octubre, los 14 días llegan al 13 — el día del vuelo de
  vuelta puede quedar fuera; un bono «Aweh» lo tapa.)* Cifras convergentes entre la web de MTC, su
  PDF de T&C y un blog independiente, internamente coherentes; ◐ porque no se pudo abrir la página.
  Detalle en [`07`](07-logistica.md), §Cobertura.

**Datos que siguen abiertos:**

- 📏 ~~**La discrepancia del D9**: Hoada → Okaukuejo, ~315 vs ~340 km~~ **RESUELTA (04/08): son
  ~340 km.** Kamanjab → Outjo 156 km *(distancesto)* + Kamanjab → Okaukuejo 271 km *(CityMeter, vía
  Outjo)* corroboran los 265 de la matriz, y con los 75 km Hoada → Kamanjab dan **~340–346 km**. El
  ~315 de `01` queda refutado; ya corregido a 340. Detalle en [`13`](13-itinerario.md), §3.
- ⛽ **Diésel en Terrace Bay** — hay **surtidor con gasolina y diésel** junto a la recepción del
  resort *(ioverlander + relatos de viajeros ◐/○)*, pero se secó en 2025 y NWR no lo publicita:
  **la regla operativa de `07`/`08` es tratarlo como que NO hay** — llena en Henties Bay y entra
  con autonomía para salir. Sigue sin cerrar si hay diésel en el bucle Ugabmund–Springbokwasser.
- 🎫 **La tabla fina de tasas del MEFT**: el PDF primario sigue sin abrirse.
- 🚧 **Obras Okaukuejo–Halali — ACTUALIZADO 03/08 (◐, antes «hay que llamar»)**: ya hay **nota
  oficial de 2026** —MEFT `news/335` «Traffic deviation via Gemsbokvlakte road from Okaukuejo to
  Halali», con aviso paralelo de NWR— que fija un **desvío obligatorio del 2 jun 2026 al jul 2027**,
  así que en noviembre de 2026 estará activo con seguridad. La página oficial no se pudo **abrir**
  (403); las fechas convergen en **cinco fuentes secundarias**, por eso queda en ◐. **El sobrecoste
  en KM quedó medido el 09/08 con el enrutado OSRM propio: ~108 km por Gemsbokvlakte–Salvadora
  frente a ~70 de la directa (+38)**. Lo que sigue abierto: el **sobrecoste en TIEMPO** —no lo
  publica nadie: cuéntalo despacio— y reconfirmar que sigue en pie *(NWR Okaukuejo,
  +264 67 229 800)*.
- 🕐 **Los horarios de salida de los safaris guiados de NWR**: no los publican en ninguna parte.
- 🌡️ ~~**Sin estación meteorológica**: Spreetshoogte, Terrace Bay y Hoada/Grootberg.~~ **CERRADOS
  DOS (04/08) con ERA5, validado a ±0,04 °C contra las celdas conocidas** *(ver arriba, §ERA5)*:
  **Spreetshoogte 31,5/17,1** y **Hoada 33,1/18,4** ◐. **Terrace Bay queda abierto a propósito**: su
  celda más cercana es océano (da 19,3 °C de aire marino, no tierra), así que la costa se sigue
  cubriendo con el proxy de estación real de Walvis Bay (25,0 ✅).

**Los flecos menores, doc a doc** *(recogidos aquí el 09/08 para que esta lista sea de verdad el
inventario; ninguno bloquea una reserva — son preguntas de la entrega del coche, de cada recepción
o de un email)*:

- 🧰 **De la entrega del coche** *(`18` §4–5, `05`, `01` §D0)*: si hay **hornillo de gas** ❌ *(no
  consta en la ficha)* · **segunda batería o corte por voltaje** para la nevera ❌ · **con cuánto
  tanque entregan** el coche ❌ · el **teléfono de emergencias 24 h de Namibia2Go** ❌ *(`06` §13)* ·
  el **coste del conductor adicional** ❌ *(`02` §10)*.
- 🏕️ **De cada recepción** *(`18`)*: **enchufe por parcela** campamento a campamento ❌ *(NWR lo
  anuncia en los grandes ◐)* · **precio de la leña** ❌ · **potabilidad del grifo** camping a
  camping ❌ · el **check-out del camping de Windhoek el D14** y si se puede volver por la tarde ❌
  *(`01` §D14)* · los **horarios de desayuno/restaurante** de los campamentos NWR y de Joe's ❌
  *(`01` §horarios)*.
- 📡 **Cobertura móvil en la escarpa de Spreetshoogte y la D1275** (noches D1–D2): **sin dato** ❌
  — trátala como silencio *(`07` §Cobertura)*.
- 📷 **Tarifas 2026/27 de ProHire y Capture Namibia** *(alquiler de cámara en Windhoek)*: la
  publicada caduca el 31 de octubre — pedir por escrito ❌ *(`19`)*.
- 🎈 **El vuelo panorámico** *(Sossusvlei / Skeleton Coast)*: sin cotizar ❌ *(`11` §drones)*.
- 🎫 **El tramo exacto de Cape Cross** *(¿N$150 o el baremo premium de N$280?)*: presupuestado
  N$150+50 ◐ con la banda alta dentro del rango — mismo email del MEFT que la tabla fina de
  tasas *(`11`)*. · **Okonjima Plains** y la **parcela de Waterberg**: cifras finas sin extraer
  *(`11` §huecos)*.

---

*Precios en N$ y € · ~N$20 = €1 · Las tarifas namibias cambian: reconfirma antes de pagar*
