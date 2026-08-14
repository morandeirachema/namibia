# Auditoría de mat-travel.com como fuente de Etosha (14/08/2026)

> **Veredicto: prosa verosímil, geografía inventada.** Se auditaron las 24 páginas de la sección
> de Etosha —las guías de charca una a una, los circuitos, los campamentos, las puertas y las
> tarifas— contra las coordenadas del trazado propio (`fuente/trazado.py` ✅) y OSM. El patrón es
> el de texto generado: los consejos genéricos son razonables, pero **los datos concretos que se
> pueden comprobar fallan de forma sistemática**. Regla para este repo: **no citar mat-travel
> para geografía, distancias ni «dónde ver» especies**. Su única página aprovechable es la de
> tarifas (abajo).

## Los errores probados ❌

- **Chudob está en la punta equivocada del parque, y en 5 páginas distintas.** La
  [guía del león](https://mat-travel.com/namibia/etosha/lion/), la
  [de Chudob](https://mat-travel.com/namibia/etosha/waterholes/chudob/), el
  [circuito](https://mat-travel.com/namibia/etosha/waterholes/circuit-guide/), el
  [ranking de león](https://mat-travel.com/namibia/etosha/waterholes/best-for-lion/) y la
  [matriz de especies](https://mat-travel.com/namibia/etosha/wildlife-by-waterhole/) la sitúan
  «a 15 km al este de Okaukuejo», «territorio de león del Etosha occidental». Chudob está a
  **~6 km de Namutoni** y a **~112 km en línea recta de Okaukuejo** *(coordenadas propias ✅ y
  OSM: -18.8582, 16.9249)*. Describen la posición de Nebrownii con el nombre de Chudob.
- **Su circuito estrella es imposible.** «Desde Okaukuejo: Chudob (15 km) → Goas → Rietfontein →
  Salvadora → vuelta, ~120 km en total»: el primer tramo real ya son ~112 km en línea recta; el
  circuito completo pasa de 230 km. Del mismo palo: el «circuito oriental» desde Halali empieza
  en Charitsaub *(que está 22 km al **oeste** de Halali)*, y desde Salvadora mandan «al norte a
  Rietfontein» *(está al este)* «volviendo por Gemsbokvlakte» *(que está pegada a Okaukuejo, a
  ~48 km de Halali — nuestro D10 la hace saliendo de Okaukuejo, no de Halali)*.
- **Nebrownii «accesible desde Halali», «sección central»**: está a 10-15 km de **Okaukuejo**
  (el intercambio simétrico del error de Chudob). Y además `01` la tiene **cerrada por obras en
  nuestras fechas** ◐ — la web ni lo sabe.
- **Una «Eastern Extension» que no existe donde la ponen.** Batia y Aus, sus charcas «de la
  extensión oriental» para ruano, eland y perro salvaje, están en el tramo **Halali–Namutoni**
  del borde del pan *(Batia: -18.9514, 16.7098, OSM)* — es el camino de vuelta, no ninguna
  extensión.
- **El ruano «fiable en Gemsbokvlakte», «población centro-oriental»**: los ruanos de Etosha
  viven en el **oeste** — translocados a la zona de cría de Otjovasandu (esquina SO) en 1968-71 y
  «raros de ver salvo en el oeste» ◐
  *([Travel News Namibia](https://www.travelnewsnamibia.com/etoshas-special-species/))*. Por eso
  la guía de fauna ni lo lleva: nadie de la ruta lo ve.
- **El rino blanco «Medium-High en Dolomite, grupos pastando con regularidad»**: contra el dato
  verificado de la ficha —**una docena escasa** desde la reintroducción de 1995, citado de vez en
  cuando en Springbokfontein, y el aviso de que la mayoría de los «avistamientos» son negros mal
  identificados—, eso es fantasía.
- **El fuerte de Namutoni, «destruido por un ataque herero en 1904»** ❌: lo asaltaron los
  **ovambos de Nehale lya Mpingana** (28/01/1904) — el rey que da nombre a la puerta norte que la
  propia web lista dos párrafos después. El «Ludwig Fischer» del Fischer's Pan tampoco cuadra
  *(las fuentes históricas dan al teniente **Adolf** Fischer)* ❌.
- **Distancias a voleo**: Okaukuejo «a 10 km de la puerta de Andersson» *(reales ~17)* y con
  coordenada «19°01'S» *(real 19°11'S — 18 km de error)*; Tsumeb→Von Lindequist «70 km, 1 h»
  *(reales ~100)*; Klein Namutoni «a 10 km del campamento» *(reales ~2,6 en línea recta)*;
  Rietfontein a 15, 30 o 50 km según qué página suya se lea.
- **Contradicciones internas**: las tasas «se pagan en los campamentos»
  ([entry-fees](https://mat-travel.com/namibia/etosha/entry-fees/)) y «se cobran en la puerta»
  ([gates-guide](https://mat-travel.com/namibia/etosha/gates-guide/)); el perro salvaje
  «raramente visto» ([wild-dog](https://mat-travel.com/namibia/etosha/wild-dog/)) pero «Medium
  en Batia y Aus» (la matriz). Y una **«Ombika Gate, previously called Anderson Gate»** de la
  que no aparece rastro oficial ❌ *(las fuentes siguen diciendo
  [Andersson](https://www.etoshanationalparknamibia.com/etosha-gates/); Ombika es la charca de
  al lado)*.
- **«Los campamentos están vallados; la fauna no puede entrar»**: que se lo digan al tejón
  mielero de Halali y a los chacales de `21`.
- Y el detalle revelador: su guía del león **no menciona Okondeka** — la charca con manada
  residente que la fuente con datos (Expert Africa ✅) da como LA charca de león del parque — y
  su sección «Etosha's Lion Population» **no trae ni un número** *(los reales: 335 en 2018,
  estable en 300-400 —
  [Conservation Namibia](https://conservationnamibia.com/blog/etosha-lions-2023.php) sobre
  Heydinger, Packer & Funston 2022)*.

## Lo que concuerda (y ya estaba, con mejor fuente)

La mecánica de las charcas iluminadas *(24 h, ventana de rino 21:00-02:00, frío, silencio)*, el
reglamento *(60 km/h, no bajarse, puertas al ocaso, dron en la puerta — `09` y `11` ✅)*, **la
gasolinera del parque sin combustible** *(cuadra con los cortes 2025-26 verificados en `05`)*,
el guepardo en Salvadora ◐, la fama leonera de Rietfontein ◐, el impala de cara negra en Klein
Namutoni ✅, los flamencos de Fischer's Pan solo en años de inundación ✅ y los nocturnos de
Ongava. Nada de esto necesita citarles.

## La única página aprovechable: las tarifas 2026

La [guía de tarifas](https://mat-travel.com/namibia/etosha/entry-fees/) reproduce **exactamente
el baremo de la Government Gazette nº 8877** que `15` §Tasas tiene localizado pero sin poder
abrir: **N$280 (~€14)/adulto internacional/día, SADC N$180 (~€9), namibio N$60 (~€3), menor de
8 gratis, vehículo ≤10 plazas N$60 (~€3)** — y completa la tabla fina *(niño 8-16: N$180 ~€9
internacional / N$100 ~€5 SADC; vehículos 11-25 plazas N$150 ~€7,5)*. Sigue siendo secundaria
—**el ◐ no sube a ✅**— y vale como concordancia, no como confirmación: la web acierta copiando
una tabla y falla imaginando un mapa. Ojo: dice tasa por **día natural**, no por bloque de 24 h
como registró `12` §7 — una razón más para confirmar en recepción.

## Consecuencia para las citas existentes

- `aparte/reservas-privadas-vs-etosha.md` usaba su página del perro salvaje como contrapeso del
  «ausente de Etosha 20 años» de New Era. Visto que la web **inventa la geografía de esa misma
  «Eastern Extension»**, el contrapeso queda degradado: la balanza se inclina hacia New Era
  *(anotado allí)*.
- El enlace de `10` *(atracciones de Damaraland, solo apoya un precio ya sostenido por Windhoek
  Express)* ya estaba en ○ y ahí se queda: sección distinta de la web, sin auditar, y sin peso
  propio.
