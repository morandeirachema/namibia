# 13 · Itinerario y viabilidad

> **Namibia · 31 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](README.md)
>
> Distancias, firme y tiempos calculados a velocidad de seguro: la comprobación, etapa por etapa, de que la ruta elegida cabe de verdad en catorce días.
>
> **~N$20 = €1** *(rango 19,5–20,5)* · **✅** fuente primaria · **◐** secundaria concordante ·
> **○** práctica común, sin fuente · **❌** sin verificar, dicho en blanco
>
> *Investigación cerrada el 17/07/2026 · formato y contenido revisados el 03/08/2026*

> ## 📐 Para qué sirve este documento
> Es la **aritmética de la ruta**: a qué velocidad se puede planificar de verdad en Namibia, cuánto
> mide cada etapa y cuánto se tarda en ella. No propone rutas —esa decisión ya está tomada, y está
> en `01`—: **comprueba que la elegida cabe**. Y **no infla nada para complacer**: donde un número
> es una estimación lo dice, y donde una etapa no cabría, también.
>
> *El análisis del sur y de las variantes descartadas se retiró el 03/08/2026 para dejar solo la
> ruta del viaje. Queda en el historial de git.*

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
    F --> G["LLEGAR ANTES DE LAS 18:00<br/>anochece 19:03-19:20 en 1-15 nov<br/>segun dia y lugar - detalle en 01"]
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

Guía independiente de operadores, que coincide: *«plan your daily routing to be no further than
400 km per day»* y, mejor, *«aim to drive no more than 4 to 6 hours per day»* (Expert Africa). Un
viajero cita un tramo de *«288 km that took over 4 hours»* y que después **acortó todos los días**.
👉 **Trabajo con un techo de ~300–350 km/día de tránsito**, y menos si el día tiene grava dura o
actividad (Sossusvlei, safari).

⚠️ *Los 80 km/h con caja negra están documentados en los contratos de **Asco/Savanna** (ver `06`);
la cláusula del contrato vigente —**Namibia2Go Budget**— sigue sin verificar: pídela al reservar.
Los tiempos de este documento se mantienen a 80 igualmente.*

Fuentes de la regla: `12` y `06` (contratos Asco/Savanna, ya descargados) ·
https://www.expertafrica.com/namibia/info/self-drive-driving-tips-and-techniques ·
https://www.safaribookings.com/blog/guide-to-driving-in-namibia-10-useful-self-drive-tips

---

## 2. La ruta etapa a etapa, con la aritmética a la vista

**Ojo a la base**: las distancias son las de §3, casi todas ◐, así que esto es **cálculo
transparente sobre datos marcados**, no medición. Método: asfalto a 100 · grava al techo de 80 con
**media real 60–70** · parque a 60 · **+30–60 min de paradas** por día de tránsito · un pinchazo =
+1 h que no está en ninguna cifra.

- **D2 · Windhoek → Spreetshoogte (~180–200 km ◐)** — 87 km asfalto (~50 min) + ~95–115 km de
  grava (a 60–70: 1h25–1h55) → **mínimo ~2h15 · realista 3h–3h30 con paradas** ✓ *(coincide con `01`)*
- **D3 · Spreetshoogte → Solitaire → Sesriem (~150–170 km ◐)** — grava entera (a 60–70:
  2h10–2h50) + parada en Solitaire → **realista ~2h30–3h** ✓
- **D4 · Sossusvlei (130 km, dentro del parque ✅)** — ~120 km a 60 = 2h de volante repartidas en
  el día + arena + dunas a pie → **día completo, y por eso se madruga a las ~05:10**
- **D5 · Sesriem → Walvis Bay (~270 km ✅)** — grava y paso del Kuiseb (a 60–70: 3h50–4h30) +
  paradas → **realista ~4h30–5h30** ✓ *(el «~5h30» de `01` es el honesto)*
- **D7 · Walvis Bay → Cape Cross → Terrace Bay (~380 km ◐, verificado 03/08)** — el día con hora
  límite: a 70–80 de media son **~5h–5h30 SOLO de volante**, más Cape Cross (~1 h) y el trámite de
  Ugabmund. **Cuenta atrás desde las 15:00 de la puerta: salir de Walvis a las 7:30 deja ~6h30 de
  margen — justo.** Un pinchazo aquí se come el margen entero: sal a las 7:00.
- **D8 · Terrace Bay → Twyfelfontein → Hoada (~300 km)** — grava entera. El grueso, **Terrace Bay →
  Twyfelfontein, son ~216 km ◐** *(96 a la puerta de Springbokwasser + 120)*: a 60–70, **~3h10–3h35
  de volante**; + grabados (~1 h) + la cola a Hoada *(~85 km, aún ○)* → **realista ~5h de volante
  más la visita** ✓
- **D9 · Hoada → Okaukuejo (~315–340 km ◐, ver §3)** — grava hasta Kamanjab, asfalto después (firme de la C38
  por confirmar, `01`) → **mínimo ~3h30 · realista ~4h–4h45** ✓ — y dentro del parque ya a 60
- **D10–D12 · Etosha (60–90 km/día ✅)** — a 60 km/h y parando en cada charca: **el día entero ES
  el trayecto** — no son horas de tránsito, son horas de safari
- **D13 · Namutoni → Windhoek (~555–575 km ◐, verificado 03/08)** — asfalto a ~100 → **mínimo ~5h30 ·
  realista 6h–6h30 con comida en Otjiwarongo**. Saliendo al amanecer (~06:10), en Windhoek a media
  tarde ✓

> **Lectura de conjunto:** ningún día se sale de las reglas. El único que exige disciplina de reloj
> es el **D7** —la puerta de Ugabmund cierra a las 15:00— y el único largo de verdad es el **D13**,
> que es asfalto. Lo único que aún hereda incertidumbre de kilómetros es la **cola Twyfelfontein →
> Hoada** *(~85 km ○)*. **Tracks4Africa antes de apurar horarios.**

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
- **Sesriem → Solitaire**: **90 km** ◐ · **Sesriem → Swakopmund** *(por la C14, pasos de Gaub y
  Kuiseb)*: **300 km** de grava ◐ — la etapa real es a **Walvis Bay**, 30 km antes por la costa

### Eje costa y Damaraland

- **Swakopmund → Walvis Bay**: **~30 km**, **asfalto B2** ✅ *(convergente: «30 km of straight tarmac»)*
- **Costa (C34) — desglose del D7** ◐ *(verificado 03/08)*: **Swakopmund → Henties Bay ~70 km**
  *(asfaltado en 2019; Wikipedia C34 / geodatos)* → **Henties Bay → Cape Cross ~70 km** →
  **Cape Cross → Terrace Bay ~200 km** *(guías de la Costa de los Esqueletos)*. La **C34 mide
  300 km Swakopmund → Torra Bay** (Wikipedia) y **Torra Bay → Terrace Bay son ~50 km**, así que
  **Walvis Bay → Terrace Bay ≈ 30 + 300 + 50 = ~380 km**, y el cruce por Cape Cross (que está sobre
  la propia C34, no es desvío) da ~370–380 km. **Cuadra con el ~390 estimado.**
- **Salida de la costa (D8) — Terrace Bay → Twyfelfontein ~216 km** ◐ *(verificado 03/08)*: es la ruta
  **directa por Springbokwasser** (no la vuelta por Khorixas). Desglose: **Terrace Bay → puerta de
  Springbokwasser ~96 km** (por la costa hasta Torra Bay ~50 + tierra adentro ~40–46 a la puerta) →
  **Springbokwasser → Twyfelfontein ~120 km** por la D3245/D2612. *(El routeplanner lo da en 216 km;
  cuadra con el negativo: la puerta de Springbokwasser está a 40 km al este de Torra Bay y a 170 km al
  oeste de Khorixas por la C39 —Wikipedia—, así que ir por Khorixas serían ~360 km; la ruta directa se
  ahorra esa vuelta.)* La **cola Twyfelfontein → Hoada (~85 km ○)** sigue sin fuente propia — Hoada
  está a 75 km al oeste de Kamanjab por la C40, 25 km al este de Grootberg.
- **Twyfelfontein → Palmwag**: **~110 km** ◐ *(operadores namibios convergentes: padlangsnamibia y
  foro 4x4community lo dan en «~2,5 h» de grava)*. **No está en la ruta**, pero se apunta porque
  **Palmwag es el surtidor de respaldo** del tramo si el de Terrace Bay falla *(ver `07`)*.

### Eje Etosha y vuelta

- **Hoada → Okaukuejo (D9)**: aquí hay que avisar de una **discrepancia sin resolver**. `01` da
  **~315 km ◐**; la aritmética sobre la matriz da **~340 km** *(Hoada está «75 km al oeste de
  Kamanjab por la C40» según el propio campamento, y la matriz pone Kamanjab → Okaukuejo en 265)*.
  **Son 25 km de diferencia** — nada que rompa el día, pero **cuenta con los 340** al calcular
  combustible y hora de puerta. Firme: grava hasta Kamanjab, asfalto después *(la C38 sin confirmar)*.
- **Etosha, travesía interior**: **Okaukuejo → Halali ~70 km → Namutoni ~70 km** (a 60 km/h y parando
  a mirar: **es un día entero de safari**, no un traslado) ◐
- **Namutoni → Windhoek** *(por Tsumeb–Otjiwarongo–Okahandja, asfalto B1/B8)*: **~555–575 km** ◐
  *(convergente: «553 km» por la web de Etosha NP y ~575 km por rome2rio; Namutoni queda más al este
  que Okaukuejo, de ahí que sea más que los 440 km desde Okaukuejo)*
- **Otjiwarongo → Outjo**: 75 km ◐ — Otjiwarongo es la parada de comida del D13

> ⚠️ **Aviso de fuente:** el bloque del eje central se apoya en una matriz con **copyright de 2010**.
> Las distancias por carretera cambian poco, pero **verifícalas con Tracks4Africa o un GPS actual
> antes de reservar alojamientos con horarios ajustados.**

---

## 4. Lo que este documento NO pudo verificar — dicho claro

- **Varias distancias del eje central** salen de una **matriz de 2010** (◐): Windhoek–Sesriem,
  Sesriem–Swakopmund, travesía de Etosha. Cambian poco, pero **no salen de un GPS 2026**.
  Verifícalas con **Tracks4Africa** antes de fijar reservas con hora.
- **Ninguna cifra de este documento es una medición propia.** Las tres que se reverificaron —el
  desglose del D7 por la C34, el D8 por Springbokwasser y el D13 Namutoni → Windhoek— **dejaron de
  ser triangulaciones**: las apoyan varias fuentes secundarias independientes que convergen en el
  rango (◐, ver §3 y Fuentes). Siguen sin ser un GPS.
- **La cola Twyfelfontein → Hoada (~85 km) sigue ○**: es el último tramo de la ruta sin fuente propia.
- **Ni la web de NWR ni las de los lodges se dejaron descargar** (**HTTP 403** desde este entorno):
  lo que hay son descripciones de operadores cruzadas entre sí, no la web oficial. **Confírmalo al
  reservar.**
- **Estado real del firme en noviembre de 2026**: el corrugado y los baches cambian mes a mes; los
  reportes de foros (4x4community, roadtripster) son de años anteriores.
- **La discrepancia del D9** (~315 vs ~340 km hasta Okaukuejo) **no está resuelta** — ver §3.

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
- **Costa (D7) — C34, verificado 03/08:** https://en.wikipedia.org/wiki/C34_road_(Namibia)
  *(«C34 is 300 km long, Swakopmund → Torra Bay»; Swakopmund → Henties Bay asfaltado en 2019)* ·
  https://www.geodatos.net/en/distances/from-swakopmund-to-hentiesbaai · Cape Cross → Terrace Bay ~200 km
  y Torra Bay → Terrace Bay ~50 km vía guías de la Costa de los Esqueletos (mistersafari, wild-wings-safaris)
  *(páginas no descargadas; datos de los extractos de búsqueda)*
- **Namutoni → Windhoek — verificado 03/08:** web de Etosha NP («553 km north of Windhoek via
  Otjiwarongo and Tsumeb») y rome2rio (~575 km) *(vía extractos de búsqueda; páginas devuelven 403 al descargar)*
- **Twyfelfontein → Palmwag — verificado 03/08:** https://padlangsnamibia.com/padlangs-namibia/the-palmwag-experience
  y foro 4x4community *(«~2,5 h» de grava; ~110 km)*
- **Salida de la costa (D8) Terrace Bay → Twyfelfontein — verificado 03/08 (◐):**
  https://www.distancesfrom.com/na/Twyfelfontein-to-Terrace-bay-Namibia-Route/RouteplannerHistory/6599689.aspx
  *(216 km vía Springbokwasser: 96 + 120)* · puerta de Springbokwasser «40 km east of Torra Bay»
  (https://skeletoncoastparkspringbokwassergate.wheretostay.na/) y «170 km west of Khorixas» +
  C39 de 494 km Torra Bay→Khorixas→Outjo→Otavi (https://en.wikipedia.org/wiki/C39_road_(Namibia)) ·
  Hoada «75 km west of Kamanjab on the C40, 25 km east of Grootberg» (https://grootberg.com/hoada-campsite/)
  *(páginas no descargadas; datos de los extractos de búsqueda, convergentes)*
- Matriz de distancias del eje central: Namibia Tours & Safaris (2010), recogida en `07-logistica.md`
