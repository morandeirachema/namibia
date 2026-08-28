# 13 · Itinerario y viabilidad

> **Namibia · 30 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](README.md)
>
> Distancias, firme y tiempos calculados a velocidad de seguro: la comprobación, etapa por etapa, de que la ruta elegida cabe de verdad en quince días (14 noches).
>
> **~N$20 = €1**, de bolsillo *(el cambio real de 2026 va por **18,5–19,4** — BCE, 28/08: el euro de estas páginas se queda ~7 % corto)* · **✅** fuente primaria · **◐** secundaria concordante ·
> **○** práctica común, sin fuente · **❌** sin verificar, dicho en blanco
>
> *Investigación cerrada el 17/07/2026 · formato y contenido revisados el 09/08/2026 — añadido el
> contraste etapa a etapa con el enrutado OSRM propio (§5)*

> ## 📐 Para qué sirve este documento
> Es la **aritmética de la ruta**: a qué velocidad se puede planificar de verdad en Namibia, cuánto
> mide cada etapa y cuánto se tarda en ella. Comprueba que la ruta del norte cabe, y **no infla nada
> para complacer**: donde un número es una estimación lo dice, y donde una etapa no cabría, también.
>
> ✅ **La ruta del norte está confirmada** por el viajero el 06/08/2026, con las fechas del vuelo de
> Lufthansa. Las variantes que respetaban el sur se retiraron de aquí el 03/08 y **siguen en el
> historial de git** *(`git show d0320c3^:13-itinerario.md`)*; el análisis que las comparaba está
> archivado en [`16`](16-punto-de-decision.md). Aquí ya solo se mide la ruta que se va a conducir.
> *Último retoque (24/08): **Spreetshoogte se queda en UNA noche** y la liberada se va a
> **Damaraland**, partiendo en dos el día más largo de grava del viaje *(D8 Twyfelfontein + D9
> Hoada, 211 + 159 km donde había 367)*; **Namutoni desaparece** y sus noches de Etosha pasan a
> **Onguma ×2**, lo que suma **+30 km** de entrar y salir por Von Lindequist dos días seguidos.
> Total: **~2.798 km**, 34 más que en agosto. El argumento del cambio, en `aparte/decision-del-ccf`.*

---

## 1. Las reglas del cálculo — por qué NO valen los tiempos de Google Maps

Google Maps asume velocidades que **anulan tu seguro** (ver `12` y `06`: 80 km/h contractuales en
grava, caja negra, límite de 60 km/h en parques). Todos los tiempos de este documento se calculan
con **tus** reglas, no las de Google:

```mermaid
flowchart TD
    A["Distancia por carretera"] --> B{"Tipo de firme"}
    B -->|"Asfalto B/algunas C"| C["100 km/h de planificacion<br/>el limite es 120, pero con<br/>fauna, viento y camiones"]
    B -->|"Grava C/D"| D["80 km/h MAXIMO<br/>contractual · caja negra<br/>realista 60-70 con corrugado"]
    B -->|"Dentro de parque"| E["60 km/h MAXIMO<br/>y mas lento buscando fauna"]
    C --> F["+ paradas foto, repostaje,<br/>pinchazo posible +1 h"]
    D --> F
    E --> F
    F --> G["LLEGAR ANTES DE LAS 18:00<br/>anochece 19:03-19:20 en 31 oct - 14 nov<br/>segun dia y lugar - detalle en 01"]
    style D fill:#e85d04,color:#000
    style E fill:#e85d04,color:#000
    style G fill:#9d0208,color:#fff
```

- **Asfalto**: planifico a **100 km/h** (el límite es 120, pero cargados, con viento lateral y
  camiones no se sostiene de media).
- **Grava**: **80 km/h es el TECHO contractual**, no la media. Con corrugado, curvas y polvo, la
  media real cae a **60–70**. Calculo el *tiempo mínimo* a 80 y aviso de que el real es mayor.
- **Parque**: **60 km/h**, y en la práctica mucho menos porque vas parando a mirar.
- **Sumo** una franja de paradas/repostaje a cada etapa y recuerdo que **un solo pinchazo suma ~1 h**.
- **Regla de oro (de `06`)**: apuntar a **llegar a las 18:00**, una hora antes del ocaso. La franja
  16:00–20:00 concentra el **29 % de los muertos** del país. Si vas tarde, **te paras y llegas mañana**.

El techo coincide con lo que repiten las guías de operadores —*«no más de 400 km al día»*, y mejor
*«de 4 a 6 horas al volante»*— ○ ⚠️ *(**la atribución a Expert Africa se retira el 28/08**: sus
páginas devuelven 403 desde aquí y las dos frases no aparecen en ninguna suya que se pueda abrir,
así que la regla se queda como práctica común y no como cita — es exactamente el caso que la marca
○ existe para cubrir)*. Lo que sí es de un viajero real, y se sostiene, es el tramo de
*«288 km que le llevaron más de 4 horas»* ◐ *(Spitzkoppe → Vingerklip, relato citado por
naturallynamibia)* y que después **acortó todos los días**.
👉 **Trabajo con un techo de ~300–350 km/día de tránsito**, y menos si el día tiene grava dura o
actividad (Sossusvlei, safari).

✅ *Los 80 km/h con caja negra están en el contrato de **Asco** (ver `06`) **y, verificado el 25/08,
en las condiciones del propio Savanna** ([rental-conditions](https://www.savannacarhire.com.na/rental-conditions)):
«National Parks: 60 km/hour, Gravel roads: 80 km/hour … Tarred Highways: 120 km/hour», «GPS Tracking
System (Black Box)» y «if you exceed this speed limit all insurances and Reduced Excesses lapse».
Los tiempos de este documento van a 80, y ahora con el contrato del coche real detrás.*

Fuentes de la regla: `12` y `06` (contratos Asco/Savanna, ya descargados) ·
https://www.expertafrica.com/namibia/info/self-drive-driving-tips-and-techniques ·
https://www.safaribookings.com/blog/guide-to-driving-in-namibia-10-useful-self-drive-tips

---

## 2. La ruta etapa a etapa, con la aritmética a la vista

**Ojo a la base**: las distancias son las de §3, casi todas ◐, así que esto es **cálculo
transparente sobre datos marcados**, no medición. Método: asfalto a 100 · grava al techo de 80 con
**media real 60–70** · parque a 60 · **+30–60 min de paradas** por día de tránsito · un pinchazo =
+1 h que no está en ninguna cifra.

- **D2 · Windhoek → Spreetshoogte (~205 km ◐, OSRM)** — 87 km asfalto (~50 min) + ~120 km de
  grava (a 60–70: 1h40–2h) → **mínimo ~2h30 · realista 3h–3h30 con paradas** ✓ *(coincide con `01`)*
- **D3 · Spreetshoogte → Solitaire → Sesriem (~129 km ◐, OSRM 128,8)** — grava entera (a 60–70:
  ~2h) + parada en Solitaire → **realista ~2h–2h30** ✓ *(el ~150–170 anterior sobraba)*
- **D4 · Sossusvlei (~122 km, dentro del parque ◐, OSRM 122)** — ~120 km a 60 = 2h de volante
  repartidas en el día + arena + dunas a pie → **día completo, y por eso se madruga a las ~05:10**
- **D5 · Sesriem → Walvis Bay (~316 km ◐, OSRM 315,6)** — grava y paso del Kuiseb (a 60–70:
  4h30–5h15) + paradas → **realista ~5h30–6h** ✓ *(la matriz de 2010 daba ~270 vía «Swakopmund
  −30»: se quedaba 45 km corta)*
- **D7 · Walvis Bay → Cape Cross → Terrace Bay (~412 km ◐, OSRM 411,5 — recalibrado el 09/08)** —
  el día con hora límite. El reloj real lo marca **Cape Cross, que el 6 nov abre a las 10:00**
  (`01`; la raya del horario de verano está en el 16 de noviembre, así que adelantar el día no la
  cruza): Walvis → Cape Cross son ~170 km (~2h15–2h30 · salir a las ~07:30 clava la apertura),
  el alto de los lobos ~1 h, y de ahí **~80 km a Ugabmund** (~1h10) → **en la puerta hacia las
  12:15–12:45, holgadamente antes de las 15:00** — y quedan **~160 km de parque a 60** hasta
  Terrace Bay (~2h30). Un pinchazo se come la mitad del margen: disciplina de reloj.
- **D8 · Terrace Bay → Springbokwasser → Twyfelfontein (~211 km ◐, OSRM 211,5)** — grava entera.
  A 60–70, **~3h–3h30 de volante**; sin puerta con hora, pero **el permiso de Skeleton Coast obliga
  a salir del parque el mismo día**. Llegando a media tarde, los grabados entran hoy o mañana
  temprano ✓ **Es la etapa que nació el 24/08**, de partir en dos el antiguo D9
- **D9 · Twyfelfontein → Palmwag → Hoada (~159 km ◐, OSRM 158,7)** — grava entera *(107 + 51)*: a
  60–70, **~2h15–2h35 de volante**; «~2,5 h» del operador. **Con la mañana libre entera**, que es lo
  que desbloquea el rastreo de rinoceronte de media jornada de Palmwag, que cae a mitad de etapa *(`11`)* ✓
  *(Hasta el 24/08 estos dos días eran **uno solo de ~370 km**, la etapa más dura del viaje, con la
  visita de Twyfelfontein metida en medio. Partirla cuesta **+3 km** y devuelve una mañana.)*
- **D10 · Hoada → Okaukuejo (~343 km ◐, resuelto 04/08 y OSRM 342,6 — ver §3)** — grava hasta Kamanjab, asfalto después (firme de la C38
  por confirmar, `01`) → **mínimo ~3h30 · realista ~4h–4h45** ✓ — y dentro del parque ya a 60
- **D11–D13 · Etosha (~70–108 km/día ◐)** — a 60 km/h y parando en cada charca: **el día entero ES
  el trayecto** — no son horas de tránsito, son horas de safari. *(El D11 es el largo: ~108 km por
  el **desvío obligatorio** de las obras — abajo, §3. El **D12 sube a ~93 km** porque termina
  saliendo por Von Lindequist hasta Onguma, y el **D13 son ~70 km** de entrar y volver a salir por
  la misma puerta: **+30 km entre los dos** frente al plan de agosto, que dormía dentro el D12.)*
- **D14 · Onguma → Windhoek (~539 km ◐ — OSRM propio; desde Namutoni eran 548)** — asfalto a ~100 →
  **mínimo ~5h30 · realista 6h–6h30 con comida en Otjiwarongo**. **Y durmiendo fuera del parque no
  hay que esperar a que la puerta abra a las 06:10**: media hora larga de ventaja ✓

> **Lectura de conjunto, revisada el 24/08:** ningún día rompe las reglas de velocidad, y **ahora
> solo quedan DOS etapas grandes, no tres**: el **D7** exige disciplina de reloj —la puerta de
> Ugabmund cierra a las 15:00— y el **D14** (539 km de asfalto) es el largo de verdad. **La tercera
> desapareció**: el antiguo día de ~370 km de grava con Twyfelfontein en medio **se partió en 211 +
> 159**, y ninguna de las dos mitades llega a cuatro horas de volante. La **cola Twyfelfontein →
> Hoada quedó medida en ~159 km**, lo que **refuta el ~85 km anterior** —era menor que la línea
> recta entre los dos puntos (~95 km por coordenadas), imposible por carretera. **Tracks4Africa
> antes de apurar horarios.**

---

## 3. De dónde sale cada distancia

Números **por carretera**, con su fuente y su confianza. Varios del **eje central** vienen de la
matriz de Namibia Tours & Safaris (**◐, copyright 2010** — las distancias cambian poco, pero es
secundaria y vieja; ver `07`); los de la **costa y la salida al interior** se reverificaron en 2026.

### Eje Windhoek → desierto

- **Windhoek → Sesriem por el paso de Spreetshoogte (D1275)**: **~320–350 km** ◐. Desglose:
  B1 a Rehoboth **87 km (asfalto)** → C24 **39 km** → D1261 a Nauchas **55 km** → **D1275, paso de
  Spreetshoogte** (miradores a 16,4 km, y 34,4 km más hasta la C14) → Solitaire → Sesriem.
  ⚠️ **El paso de Spreetshoogte es MUY empinado**, con tramos de grava y otros de adoquín de hormigón
  para tracción; *«no coaches, caravans or trailers permitted»*. Espectacular, pero es un **descenso
  técnico**, no un atajo cómodo. **Si el primer día con el coche recién cogido se hace cuesta arriba**,
  la alternativa es rodearlo por el **paso de Remhoogte (C24)**: ~365 km, más largo y más llevadero ◐.
- **Sesriem → Sossusvlei / Deadvlei**: **60 km cada trayecto** (120 ida y vuelta) **+ 5 km de arena
  blanda** en reductora al final ◐ *(matriz 2010 + `06`)*
- **Sesriem → Solitaire**: **~85 km** ◐ *(OSRM 83,5; la matriz decía 90)* · **Sesriem → Walvis
  Bay** *(por la C14, pasos de Gaub y Kuiseb)*: **~315 km** ◐ *(OSRM 316: 83,5 a Solitaire +
  232,8 de Solitaire a Walvis)*. ⚠️ La matriz de 2010 daba «Sesriem → Swakopmund 300» y de ahí
  salía un «Walvis a 270»: **se quedaba ~45 km corta** — es la clase de error que el enrutado
  destapa (ver §5).

### Eje costa y Damaraland

- **Swakopmund → Walvis Bay**: **~30 km**, **asfalto B2** ✅ *(convergente: «30 km of straight tarmac»)*
- **Costa (C34) — desglose del D7, recalibrado el 09/08 con el enrutado OSRM propio** ◐:
  **Walvis Bay → Swakopmund 35** → **Swakopmund → Henties Bay 77** *(asfaltado en 2019; Wikipedia
  C34 / geodatos)* → **Henties Bay → Cape Cross 59** → **Cape Cross → Ugabmund 81** →
  **Ugabmund → Terrace Bay 161** *(pasando Torra Bay; Torra → Terrace ~50 sigue cuadrando)* =
  **Walvis Bay → Terrace Bay ≈ 412 km**. ⚠️ **La triangulación secundaria del 03/08 (~380) queda
  refutada por abajo**: su tramo «Cape Cross → Terrace Bay ~200 km» era **menor que la línea
  recta entre los dos puntos (220 km)** — el mismo argumento que tumbó el «~85 km» de
  Twyfelfontein–Hoada. Para el día con hora de puerta, **cuenta ~410**.
- **Salida de la costa (D8) — Terrace Bay → Twyfelfontein ~216 km** ◐ *(verificado 03/08)*: es la ruta
  **directa por Springbokwasser** (no la vuelta por Khorixas). Desglose: **Terrace Bay → puerta de
  Springbokwasser ~96 km** (por la costa hasta Torra Bay ~50 + tierra adentro ~40–46 a la puerta) →
  **Springbokwasser → Twyfelfontein ~120 km** por la C39 y las D2612/**D3254** *(la numeración
  correcta del acceso final; un borrador decía «D3245», con los dígitos bailados)*. *(El routeplanner lo da en 216 km;
  cuadra con el negativo: la puerta de Springbokwasser está a 40 km al este de Torra Bay y a 170 km al
  oeste de Khorixas por la C39 —Wikipedia—, así que ir por Khorixas serían ~360 km; la ruta directa se
  ahorra esa vuelta.)* La **cola Twyfelfontein → Hoada mide ~155 km ◐** *(verificado 03/08)*. Hoada
  está en la **C40, a 25 km al este de Grootberg, ~50 km al este de Palmwag y 75 km al oeste de
  Kamanjab** (GPS S 19°43,9′ E 14°18,4′). Dos rutas convergen: **Twyfelfontein → Palmwag ~110 km +
  Palmwag → Hoada ~50 km ≈ 160 km**, y **Twyfelfontein → Grootberg ~130 km + Hoada 25 km al este ≈
  155 km**; el operador da el trayecto en **«~2,5 h»**. **El ~85 km anterior queda refutado**: es menor
  que la línea recta Twyfelfontein–Hoada (~95 km, por coordenadas), imposible por carretera.
- **Twyfelfontein → Palmwag**: **~110 km** ◐ *(operadores namibios convergentes: padlangsnamibia y
  foro 4x4community lo dan en «~2,5 h» de grava)*. **No está en la ruta**, pero se apunta porque
  **Palmwag es el surtidor de respaldo** del tramo si el de Terrace Bay falla *(ver `07`)*.

### Eje Etosha y vuelta

- **Hoada → Okaukuejo (D10) — DISCREPANCIA RESUELTA (04/08): son ~340 km, y el ~315 queda refutado.**
  Se cierra sumando tramos con fuente propia: **Hoada → Kamanjab 75 km** *(el campamento se sitúa «75 km
  al oeste de Kamanjab por la C40»)* **+ Kamanjab → Okaukuejo por Outjo ~265–271 km**. Esta última pata
  se corroboró con **dos fuentes independientes que convergen con la matriz de 2010**: **distancesto.com
  da Kamanjab → Outjo en 156 km** *(C40, asfaltado Outjo–Kamanjab, coincide con la ficha de Wikipedia del
  C40)* y **CityMeter da Kamanjab → Okaukuejo vía Outjo en 271 km** —a 6 km de los 265 de la matriz—.
  Total **75 + 265…271 = ~340–346 km**, que **confirma el ~340 y descarta el ~315** *(un subconteo de
  `01`)*. No hay ruta más corta: cualquier alternativa a Okaukuejo pasa por Kamanjab y Outjo *(Galton, al
  oeste, exige reserva y es más largo por dentro)*. Firme: grava hasta Kamanjab, asfalto después *(la C38
  sin confirmar)*.
- **Etosha, travesía interior**: **Okaukuejo → Halali, ~70 km por la pista directa — pero en
  vuestras fechas rige el desvío obligatorio de las obras** *(MEFT `news/335`, ver `01` §D11)*:
  **por Gemsbokvlakte–Salvadora son ~108 km (OSRM propio, +38)**. **Halali → Namutoni ~70–77 km**
  *(OSRM 77)*. A 60 km/h y parando a mirar: **es un día entero de safari**, no un traslado ◐
- **Onguma → Windhoek** *(por Tsumeb–Otjiwarongo–Okahandja, todo B1; la variante por
  Grootfontein para Hoba toca la B8)*: **~539 km** ◐ *(enrutado propio; desde Namutoni eran 548, y
  ahí convergían «553 km» por la web de Etosha NP y ~575 km por rome2rio; Namutoni queda más al
  este que Okaukuejo, de ahí que sea más que los 440 km desde Okaukuejo)*. **Onguma → Tsumeb:
  ~105 km** ◐ *(enrutado propio; secundarias 108–110)* — es el primer repostaje del día
- **La pieza nueva del 21/08**, medida con el mismo enrutado que el resto de la ruta ✅: **puerta
  de Von Lindequist → Onguma Tamboti, 3,4 km** *(coordenadas de OpenStreetMap: 18,7819 S
  17,0592 E, `camp_site`)*. Es lo que explica los ~16 km que sube el D12 *(salir por la puerta hasta Onguma)*, los ~14 del
  D13 *(entrar y salir)* y los ~9 que baja el D14
- **Otjiwarongo → Outjo**: 75 km ◐ — Otjiwarongo es la parada de comida del D14

> ⚠️ **Aviso de fuente:** el bloque del eje central se apoya en una matriz con **copyright de 2010**.
> Las distancias por carretera cambian poco, pero **verifícalas con Tracks4Africa o un GPS actual
> antes de reservar alojamientos con horarios ajustados.**

---

## 4. Lo que este documento NO pudo verificar — dicho claro

- **Varias distancias del eje central venían de una matriz de 2010** (◐) y el enrutado OSRM del
  §5 las recalibró: Windhoek–Sesriem aguantó (~334 por Spreetshoogte), **Sesriem–Walvis Bay no**
  (270 → ~315). Cambian poco con los años, pero **no salen de un GPS 2026**: verifícalas con
  **Tracks4Africa** antes de fijar reservas con hora.
- **La única medición propia es el enrutado OSRM del §5** — que es cálculo sobre OpenStreetMap,
  **no un GPS rodado en el terreno**: donde OSM tenga el trazado viejo, OSRM lo hereda. Del resto,
  las cifras reverificadas el 03–04/08 (D8 por Springbokwasser, D10, D14) son secundarias
  convergentes ◐ — y **las tres cuadran con OSRM a ±5 km**, que es justo lo que les faltaba.
  El desglose viejo de la costa (~380) **quedó refutado** el 09/08 *(ver §3)*.
- **La cola Twyfelfontein → Hoada quedó cerrada en ~159 km ◐** *(OSRM 158,7 por Palmwag; el 03/08 se
  midió en ~150 con un enrutado anterior)*: el ~85 km que se
  manejaba antes está **refutado** por ser menor que la línea recta (~95 km). Con esto **la ruta E
  ya no tiene distancias sin medir**, y **la discrepancia del D10 quedó resuelta el 04/08 en ~340 km**
  *(ver §3)*.
- **En la pasada del 17/07, ni la web de NWR ni las de los lodges se dejaban descargar** (HTTP 403
  desde este entorno). ⚠️ **Aviso caducado en parte**: el **PDF de tarifas 2026/27 de NWR sí se
  descargó y leyó el 16/07** *(es la fuente de `03`)* y **las fichas de actividades de nwr.com.na
  se leyeron el 03/08** *(`03` §Actividades)*. Lo que sigue sin abrirse son los **lodges privados**
  *(403, ver `15`)*. **Confírmalo al reservar.**
- **Estado real del firme en noviembre de 2026**: el corrugado y los baches cambian mes a mes; los
  reportes de foros (4x4community, roadtripster) son de años anteriores.
- ~~**La discrepancia del D10** (~315 vs ~340 km hasta Okaukuejo)~~ **RESUELTA el 04/08 en ~340 km**
  con dos fuentes de distancia convergentes — ver §3.

---

## 5. El contraste con OSRM — la ruta entera, enrutada de una pieza *(08–09/08/2026)*

El trazado del dossier no está dibujado a mano: **son las coordenadas reales de cada parada
(geocodificadas el 04/08) enrutadas por carretera con OSRM sobre OpenStreetMap** — el mismo
cálculo que pinta el mapa del PDF y que da el **total de ~2.798 km**. Guardado en
`fuente/geo/ruta.json`; se regenera con `make geo`. Etapa a etapa, en km de carretera
*(rehecho el 24/08 con el itinerario nuevo)*:

**D1 · 46** *(aeropuerto → Windhoek)* · **D2 · 205** · **D3 · 129** · **D4 · 122** · **D5 · 316** ·
**D6 · 0** · **D7 · 412** · **D8 · 211** · **D9 · 159** · **D10 · 343** · **D11 · 108** *(con el
desvío de las obras)* · **D12 · 93** *(safari y **salida a Onguma**)* · **D13 · 70** *(el bucle de
Fischer's Pan, **entrando y saliendo por Von Lindequist**)* · **D14 · 539** *(ya desde Onguma)* ·
**D15 · 46** *(al aeropuerto)* — **total 2.798**.

> **Los 34 km de diferencia con los ~2.764 del 21/08 salen de dos sitios, y conviene separarlos**:
> **+30 km son las noches de Onguma** —el D12 sube de 77 a 93 al salir por la puerta y el D13 de 56
> a 70 al entrar y volver a salir— y **+3 km, partir Damaraland en dos** *(211 + 159 = 370 donde
> había 367: pasar por Twyfelfontein y volver a salir cuesta tres kilómetros)*. El resto de la ruta
> es idéntica; lo que cambió fue **qué día se hace cada cosa**, no el trazado.

**Lectura honesta**: OSRM es una medición **de gabinete** (◐) — depende de que OSM tenga el trazado
al día — pero es **consistente de punta a punta**, y donde discrepó de las triangulaciones de
secundarias ganó dos veces por geometría *(el D8, cuyo tramo «~200 km» era menor que la línea
recta; y el D6, heredero de la matriz de 2010)*. Donde ambas convergen *(D9, D10, D14, D2–D5)*, la
cifra queda doblemente apoyada.

---

## Fuentes

- Reglas de conducción y velocidad: `12-hallazgos-verificados.md`, `06-conduccion.md` (contratos
  Asco/Savanna ya descargados) ·
  https://www.expertafrica.com/namibia/info/self-drive-driving-tips-and-techniques ·
  https://www.safaribookings.com/blog/guide-to-driving-in-namibia-10-useful-self-drive-tips
- Paso de Spreetshoogte vs Remhoogte: descripciones de ruta recogidas vía Travel Namibia y foros
  (travelnam.com, tripadvisor Namibia) *(páginas no descargadas hoy; datos de los extractos de búsqueda)*
- Swakopmund–Walvis Bay: extractos de búsqueda cruzados (siyabona, distancesfrom)
- Etosha, travesía interior y puertas: foro NWR y https://www.etoshanationalpark.org/map
- **Costa (D8) — C34, verificado 03/08:** https://en.wikipedia.org/wiki/C34_road_(Namibia)
  *(«C34 is 300 km long, Swakopmund → Torra Bay»; Swakopmund → Henties Bay asfaltado en 2019)* ·
  https://www.geodatos.net/en/distances/from-swakopmund-to-hentiesbaai · Cape Cross → Terrace Bay ~200 km
  y Torra Bay → Terrace Bay ~50 km vía guías de la Costa de los Esqueletos (mistersafari, wild-wings-safaris)
  *(páginas no descargadas; datos de los extractos de búsqueda)*
- **Namutoni → Windhoek — verificado 03/08:** web de Etosha NP («553 km north of Windhoek via
  Otjiwarongo and Tsumeb») y rome2rio (~575 km) *(vía extractos de búsqueda; páginas devuelven 403 al descargar)*
- **Twyfelfontein → Palmwag — verificado 03/08:** https://padlangsnamibia.com/padlangs-namibia/the-palmwag-experience
  y foro 4x4community *(«~2,5 h» de grava; ~110 km)*
- **Numeración del acceso a Twyfelfontein (C39 → D2612 → D3254):**
  https://www.siyabona.com/twyfelfontein-country-lodge_location.html *(◐; corrige el «D3245» de un
  borrador)*
- **Salida de la costa (D8) Terrace Bay → Twyfelfontein — verificado 03/08 (◐):**
  https://www.distancesfrom.com/na/Twyfelfontein-to-Terrace-bay-Namibia-Route/RouteplannerHistory/6599689.aspx
  *(216 km vía Springbokwasser: 96 + 120)* · puerta de Springbokwasser «40 km east of Torra Bay»
  (https://skeletoncoastparkspringbokwassergate.wheretostay.na/) y «170 km west of Khorixas» +
  C39 de 494 km Torra Bay→Khorixas→Outjo→Otavi (https://en.wikipedia.org/wiki/C39_road_(Namibia))
  *(páginas no descargadas; datos de los extractos de búsqueda, convergentes)*
- **Cola del D9 Twyfelfontein → Hoada ~155 km — verificado 03/08 (◐):** Hoada «75 km west of Kamanjab
  on the C40, 25 km east of Grootberg, ~50 km east of Palmwag», GPS S 19°43,930′ E 14°18,401′
  (https://grootberg.com/ · https://www.namibweb.com/camping-coordinates-namibia.htm ·
  https://www.places.co.za/accommodation/hoada-campsite.html) · Twyfelfontein 20,5906°S 14,3722°E
  (https://en.wikipedia.org/wiki/Twyfelfontein ·
  https://latitude.to/articles-by-country/na/namibia/39007/twyfelfontein) → la línea recta de ~95 km
  que refuta el ~85 km · Twyfelfontein → Grootberg «~130 km, ~2,5 h» y Twyfelfontein → Hoada «about two
  and a half hours» (extractos de distancesfrom y journeysnamibia.com) *(páginas no descargadas por 403)*
- **D10 Hoada → Okaukuejo ~340 km — resuelto 04/08 (◐):** Kamanjab → Outjo **156 km**
  (https://www.distancesto.com/road-map/na/kamanjab-to-outjo/history/1188283.html) · Kamanjab →
  Okaukuejo vía Outjo **271 km** (https://citymeter.net/distance-between-kamanjab-and-okaukuejo-via-Outjo-2016870196)
  · C40 «259 km, Outjo vía Kamanjab a Palmwag, asfaltado Outjo–Kamanjab» y C38 «asfaltado Otjiwarongo–Okaukuejo»
  (https://en.wikipedia.org/wiki/C40_road_(Namibia) · https://en.wikipedia.org/wiki/C38_road_(Namibia))
  · Hoada «75 km al oeste de Kamanjab por la C40» (fichas de grootberg.com y places.co.za, ya citadas arriba)
  *(datos de los extractos de búsqueda; las páginas devuelven 403 al descargar)*
- Matriz de distancias del eje central: Namibia Tours & Safaris (2010), recogida en `07-logistica.md`
