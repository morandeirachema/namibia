# 01 · Los itinerarios, día a día

> **Namibia · 30 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](README.md)
>
> La ruta desarrollada día por día: qué se conduce, a qué hora sale y se pone el sol, qué temperatura hace donde se duerme y qué cuesta cada noche.
>
> **~N$20 = €1** *(rango 19,5–20,5)* · **✅** fuente primaria · **◐** secundaria concordante ·
> **○** práctica común, sin fuente · **❌** sin verificar, dicho en blanco
>
> *Investigación cerrada el 17/07/2026 · formato y contenido revisados el 03/08/2026*

> ## 🗺️ Esta es LA ruta del viaje
>
> Decisiones del viajero, en orden: **primera quincena de noviembre**, **Sossusvlei y Etosha los
> dos**, y **el sur fuera entero**. El resultado es la ruta de abajo: la clásica del norte a ritmo
> lento, la misma familia que el itinerario de
> [lugaresincertos.com](https://www.lugaresincertos.com/en/travel-inspiration/two-week-trip-to-namibia/)
> que sirvió de referencia, pero montada con datos verificados.
>
> *Las variantes que se estudiaron y se descartaron (con el sur, sin Etosha, o todo comprimido) ya
> no están en el dossier: se quitaron el 03/08/2026 para dejar solo lo que se va a hacer. Quedan en
> el historial de git.*

---

<div align="center">

## ⭐ LA RUTA — la clásica del norte, a ritmo lento
### Como la del blog de referencia, pero con nuestros datos verificados

</div>

**~2.600 km · 12 días de coche contratados (1–13 nov) · ningún día por encima de ~390 km · dos
noches en Sesriem, dos en la costa y CUATRO en Etosha · fechas reales del vuelo: llegada el domingo
1 de noviembre de 2026, vuelta el sábado 14**

> ### 📅 El 1 de noviembre sigue siendo la fecha mágica
> **NWR entra en tramo barato** (Sesriem, Halali, Okaukuejo, Terrace Bay) y **Namibia2Go entra en
> SU temporada baja**: el coche está **cotizado — Budget N$35.100 (~€1.755) o Comfort N$39.000
> (~€1.950) por 13 días, las dos disponibles**. **Adelantar hasta 2 días a
> octubre es gratis** (Windhoek y Spreetshoogte no son NWR).

> ### ❓ ¿Etosha al principio o al final? → **AL FINAL.** Tres razones con datos:
> 1. **Dinero**: con el desierto primero, si adelantáis la salida a octubre, **todas las noches NWR
>    caen después del 1 de noviembre** (tarifa baja). Etosha primero + salida en octubre = tarifa
>    vieja **y** el pico de calor del parque (38,0 °C de media de máximas en octubre).
> 2. **Termómetro**: Etosha se enfría según avanza noviembre (38,0 oct → 37,1 media nov).
> 3. **Rodaje y crescendo**: asfalto y grava fácil primero; el safari como clímax, no aperitivo.
>
> *El contra, honesto: el riesgo de primeras tormentas sube mínimamente hacia el día 15 (en 2 de 5
> temporadas cayó algún chubasco suelto en la primera quincena — aislado, no la temporada
> asentada). Marginal frente a lo anterior.*

```mermaid
gantt
    title la ruta · la clasica del norte · 1-14 nov 2026
    dateFormat YYYY-MM-DD
    axisFormat %d-%m
    section Llegada
    D1 Windhoek :e1, 2026-11-01, 1d
    section Desierto
    D2 Paso de Spreetshoogte :e2, after e1, 1d
    D3 Solitaire-Sesriem :e3, after e2, 1d
    D4 Sossusvlei y Deadvlei :e4, after e3, 1d
    section Costa
    D5 Sesriem-Walvis Bay :e5, after e4, 1d
    D6 Flamencos y descanso :e6, after e5, 1d
    D7 Cape Cross-Terrace Bay :e7, after e6, 1d
    section Damaraland
    D8 Skeleton-Twyfelfontein-Hoada :e8, after e7, 1d
    section Safari
    D9 Hoada-Okaukuejo :e9, after e8, 1d
    D10 Safari a Halali :e10, after e9, 1d
    D11 Safari a Namutoni :e11, after e10, 1d
    D12 Etosha este :e12, after e11, 1d
    section Vuelta
    D13 Regreso a Windhoek :e13, after e12, 1d
    D14 Vuelo :e14, after e13, 1d
```

> ### ☀️ El sol de tu viaje *(cálculo astronómico NOAA, hora local UTC+2, coordenadas aproximadas — margen ±5 min; cuadra con el ~19:15 de fin de noviembre que da NWR ◐)*
> Cada día lleva abajo su amanecer y anochecer. El patrón que importa: **en Etosha anochece antes
> (~19:05, está al este) y en la costa después (~19:20)** — la regla de «en el campamento a las
> 18:00» vale igual en toda la ruta.

> ### 🌡️ Y la temperatura donde duermes — medias de NOVIEMBRE
> Cada noche lleva su **máxima media / mínima media** del mes. **Son medias mensuales, no la
> previsión de tu día**: el récord de noviembre en el sur llega a 41–42 °C (`15`).
> **Regla de fuentes de este repo:** las webs de safaris fueron **refutadas 0–3** (`15`), así que
> aquí solo hay **estación ✅** (o secundaria que la cite) y, donde no hay estación, **reanálisis
> ERA5 ◐** validado a ±0,04 °C contra las estaciones (`15` §ERA5). Terrace Bay se queda en «sin
> dato» a propósito: su celda ERA5 es mar.
>
> ```mermaid
> flowchart LR
> T["Noviembre donde duermes<br/>media de máxima / mínima, en °C"]
> n0["Walvis Bay · la costa<br/>25,0 día / 12,7 noche"]
> n1["Windhoek<br/>31,2 día / 16,3 noche"]
> n1b["Spreetshoogte · escarpa<br/>31,5 / 17,1 · ERA5"]
> n2["Sesriem · el desierto<br/>32,5 día / 15,5 noche"]
> n2b["Hoada · Damaraland<br/>33,1 / 18,4 · ERA5"]
> n3["Okaukuejo · Etosha<br/>37,1 día / 18,9 noche"]
> T ~~~ n0
> n0 ~~~ n1
> n1 ~~~ n1b
> n1b ~~~ n2
> n2 ~~~ n2b
> n2b ~~~ n3
> style T fill:#7a3a22,color:#fff,stroke:#7a3a22
> style n0 fill:#2d6a4f,color:#fff,stroke:#2d6a4f
> style n3 fill:#9d0208,color:#fff,stroke:#9d0208
>```
>
> **El viaje entero cabe en una frase: la costa fresca (25 °C), el desierto y la meseta calurosos
> (31–33 °C) y Etosha duro (37 °C) — y TODAS las noches entre 12 y 19 °C.** Por eso el equipaje
> lleva forro polar y no plumas (`05`).

> ### 🏕️ Dónde se duerme: **en la tienda de techo siempre que se pueda**
>
> El plan es dormir arriba las 13 noches y **meterse en campings**, incluidos los tres de dentro de
> Etosha. Estado noche a noche:
>
> ```mermaid
> flowchart TD
>     T["TIENDA DE TECHO · 8 noches ya resueltas<br/>D2 Spreetshoogte · D3-D4 Sesriem dentro de la puerta<br/>D8 Hoada · D9 Okaukuejo · D10 Halali · D11-D12 Namutoni"]
>     D["POR ELEGIR CAMPING · 3 noches<br/>D1 Windhoek: Urban Camp o Arebbusch<br/>D5-D6 Walvis Bay: Lagoon Chalets<br/>existen y tienen camping, pero NO publican precio"]
>     P["HABITACION, NO TIENDA · D7 Terrace Bay<br/>el tarifario oficial de NWR no tiene camping aqui:<br/>doble en media pension, N$3.480 (~EUR 174) los dos"]
>     N["TAMPOCO · D13 Windhoek<br/>el coche se entrega ese dia: habitacion<br/>salvo que se anada el dia 13 (~150 EUR)"]
>     T ~~~ D ~~~ P ~~~ N
>     style T fill:#2d6a4f,color:#fff
>     style P fill:#e85d04,color:#000
>     style N fill:#9d0208,color:#fff
> ```
>
> **El recuento, que suma 13:** **8** ya resueltas en tienda · **3** en las que se puede dormir
> arriba pero falta elegir camping *(D1 y D5–D6)* · **2 imposibles**: *D7 Terrace Bay* (no tiene
> camping) y *D13* (sin coche).
>
> 👉 **El techo real son 11 de 13 noches arriba** (12 si añadís el día 13 de alquiler). Las dos que
> no pueden ser: Terrace Bay, que solo tiene habitaciones, y la última, sin coche.
>
> ### 🚗 ¿Y cuántos días estáis en Windhoek sin coche? **Dos, con la cotización actual.**
>
> El coche está cotizado del **1 nov 08:00 al 13 nov 17:00** —13 días— y el vuelo va del **31 de
> octubre al 14 de noviembre**. No cuadra por las dos puntas:
>
> - **D0, 31 de octubre**: aterrizáis a las **09:25** y **el alquiler no ha empezado** → noche de
>   hotel en Windhoek y traslado desde el aeropuerto *(~45 km)*.
> - **De D1 a D13**: coche todos los días. La noche del 13 ya es **sin 4x4**.
> - **D14, sábado 14**: el vuelo sale a las **20:45** — un día entero en Windhoek, otra vez a pie.
>
> 💡 **La alternativa que lo evita:** recotizar el alquiler **del 31 oct 11:00 al 14 nov 18:00**
> —15 días—. Son **~N$5.400 (~€270)** más la pareja con la Budget, y te ahorras **dos noches de
> hotel y tres traslados**, además de dormir arriba la última noche. ⚠️ **Ojo: el 31 de octubre cae
> fuera de la temporada baja de Namibia2Go** — pide ese día por separado *(ver
> [`02`](02-presupuesto.md) §2)*.

### D0 · sáb 31 oct — **Aterrizas, y este día es nuevo** ⚠️
- ✈️ **Llegada a Windhoek a las 09:25** con el vuelo de Oporto *(ver [`02`](02-presupuesto.md) §8)*
- ⚠️ **Este día NO estaba en el plan y todavía no tiene contenido.** El vuelo aterriza un día antes
  de lo que asumía la ruta, así que **hay una jornada entera de regalo en Windhoek** — y una noche
  más que resolver. **Dos cosas que decidir**: si se adelanta la recogida del coche al 31
  *(recotizar, [`02`](02-presupuesto.md) §2)* y si ese día se usa para **descansar del vuelo** o
  para **adelantar etapa** hacia Spreetshoogte.
- 🛏️ **Windhoek, noche extra** — sin resolver ❌

### D1 · dom 1 nov — Windhoek, el día que ya estaba planificado
- 🌡️ **Windhoek, medias de noviembre: 31,2 °C máx / 16,3 °C mín** ✅ *(NOAA GHCN, estación 68110,
  1.700 m, serie 1957–2025; ver `15`)* — cálido de día, pero a 1.700 m **refresca de noche**
- ☀️ amanecer **06:07** · anochecer **19:04**
- ⚠️ **Es domingo: las bottle stores y las secciones de alcohol cierran por ley** (ver `04`) — la
  compra de cervezas para el braai espera al lunes
- 4x4 + briefing (1–2 h): **presiones en frío apuntadas, las DOS ruedas de repuesto, gato y
  compresor a la vista** antes de salir del patio (`06`)
- Efectivo (~N$6.000–8.000 · ~€300–400) · **SIM de MTC** con pasaporte *(el kiosco cierra ~21:00)*
- 🍺 **Joe's Beerhouse** · 🛏️ **Windhoek — y aquí ya se puede dormir arriba**, porque el coche se
  recoge hoy. Candidatos con camping verificado *(precio ❌, no lo publican)*: **Urban Camp**
  *(Schanzen Road, en la ciudad; piscina, bar, wifi, cajero)* y **Arebbusch Travel Lodge**

### D2 · lun 2 — Windhoek → paso de Spreetshoogte · **~180–200 km · ~3h–3h30** ◐
- 🌡️ **Spreetshoogte: medias de noviembre ~31,5 °C máx / ~17,1 °C mín** ◐ *(reanálisis ERA5,
  celda del borde de la escarpa; el cálculo reproduce Windhoek/Sesriem a ±0,04 °C — ver `15` §ERA5)*.
  **Confirma el proxy de Windhoek** (31,2/16,3 ✅): misma altitud (~1.700 m), mismo clima de meseta.
  Arriba corre viento y refresca al caer el sol ○
- ☀️ amanecer **06:09** · anochecer **19:10** — *el atardecer en el paso es el plan del día: en
  posición hacia las 18:40*
- B1 a Rehoboth (87 asfalto) → C24 → D1261 → **D1275: el paso**. ⚠️ **Muy empinado**, tramos de
  hormigón para tracción, prohibido a caravanas — se baja despacio y es espectacular
- 🌇 **Atardecer desde el mirador del paso**: el Namib a 1.000 m bajo tus pies
- 🛏️ **Spreetshoogte Campsite** ⚠️ *precio sin verificar (el blog citaba 150–300 ZAR/persona,
  vigencia desconocida)*

### D3 · mar 3 — Spreetshoogte → Solitaire → Sesriem · **~150–170 km · ~2h30–3h** ◐
- 🌡️ **Sesriem, media de máximas de noviembre: ~32,5 °C** ◐ *(reanálisis ERA5, celda a 4 km de la
  puerta; con el sesgo frío del interior la real ronda **33–34 °C**, que es justo el 34,1 ◐ de NWR —
  dos fuentes independientes, mismo entorno; ver `15` §ERA5)*. Mínima **~15,5 °C** ◐ (NWR)
- ☀️ amanecer **06:09** · anochecer **19:12** — *la puerta exterior de Sesriem funciona de
  amanecer a ocaso: dentro antes de ~19:10*
- Bajada del paso → C14 → 🥧 **Solitaire** (tarta + depósito lleno) → D826/C19 a Sesriem
- Tarde: **Sesriem Canyon** y atardecer en **Elim Dune** *(o el guiado de NWR, N$300 ≈ €15/persona)*
- 🎫 Namib-Naukluft ~N$620/24 h
- 🛏️ **🔑 DENTRO de la puerta: Sesriem Campsite — N$1.340 (~€67)** ✅ *(44 parcelas: reservar YA)*

### D4 · mié 4 — Sossusvlei y Deadvlei · **130 km · día completo** ✅
- 🌡️ **Sesriem ~32,5–34 / 15,5 ◐** — y en la duna, a mediodía, la arena está muy por encima de eso:
  **Big Daddy se sube al amanecer o no se sube** ○
- ☀️ amanecer **06:10** (Deadvlei) · anochecer **19:16** — **la puerta interior abre 1 h antes del
  amanecer: ~05:10.** Son ~60 km de asfalto + arena hasta el aparcamiento: saliendo al abrirse,
  llegas con la duna encendiéndose *(horas de puerta: confírmalas en recepción al llegar, se
  mueven con el orto real — ver `06`)*
- 🌅 **Puerta interior 1 h antes del amanecer** — Deadvlei casi en solitario
- Con día entero: **Big Daddy** (la subida) + **Hidden Vlei** + **Duna 45** a la vuelta
- Arena final: 4H antes de entrar, desinflar en el 2WD, reinflar en Sesriem *(o lanzadera
  N$180 ≈ €9/persona)*
- 🛏️ Sesriem, segunda noche

### D5 · jue 5 — Sesriem → Walvis Bay · **~270 km · ~5h30** ✅
- 🌡️ **Walvis Bay, medias de noviembre: 25,0 °C máx / 12,7 °C mín** ✅ *(NOAA GHCN, estación del
  aeropuerto WMO 68098, serie 1990–2025; ver `15`)* — **la costa es el respiro térmico del viaje**:
  la corriente de Benguela. Pero ojo a la madrugada: **12–14 °C**, y viento. Cortavientos a mano
- ☀️ amanecer **06:15** · anochecer **19:17** (Walvis Bay)
- C14 por los pasos de **Gaub y Kuiseb** + Trópico de Capricornio
- ⛽ **Solitaire otra vez, sí o sí** — después, **210 km sin nada**
- 🛏️ **Walvis Bay — también en tienda.** El único sitio con camping que aparece listado en la
  ciudad es **Lagoon Chalets**, que es además el que usó el blog de referencia ◐. **Precio ❌: no
  lo publica.** *(Si no cuadra, Swakopmund a 30 km tiene más oferta de camping.)*

### D6 · vie 6 — Walvis Bay: flamencos y descanso ✅
- 🌡️ **Walvis Bay 25,0 / 12,7** ✅ — el día fresco del viaje: aprovecha para el Welwitschia Drive
- ☀️ amanecer **06:14** · anochecer **19:17** — *flamencos con la primera luz, ~06:15–07:30*
- 🦩 **Y tu mes es de los buenos**: en Walvis Bay los flamencos tienen su **máximo de junio a
  noviembre** ✅ *(SABAP1)*. Aquí sí los hay en cantidad — en Etosha, en cambio, **no**: la depresión está
  seca en noviembre *(ver `09`)*
- 🦩 **Flamencos y pelícanos en la laguna** al amanecer y al atardecer — las mejores luces
- Día libre: paseo marítimo, ostras, el **crucero de delfines y lobos** *(~N$1.400–1.990, ~€70–100 pp
  ◐)* o la excursión guiada a **Sandwich Harbour** *(~N$2.600–3.220, ~€130–161 pp ◐)*
  *(🚫 con tu coche Sandwich Harbour está prohibida por contrato — el tour es la forma correcta y mejor;
  precios y fuentes en [`02`](02-presupuesto.md), §9)*
- 🛏️ Walvis Bay, segunda noche

### D7 · sáb 7 — Cape Cross → Terrace Bay (Skeleton Coast) · **~390 km · día logístico** ✅
- 🌡️ **Terrace Bay: sin dato de estación** — no hay serie pública ni en Möwe Bay ni en Terrace
  Bay, y **ERA5 tampoco sirve aquí**: su celda más cercana cae sobre el mar *(da aire marino ~19 °C,
  no tierra; ver `15` §ERA5)*. Proxy honesto: **la costa ronda los 25,0 °C de Walvis Bay ✅**, 400 km
  más al sur — con **niebla, viento y menos calor que tierra adentro** ○
- ☀️ amanecer **06:18** (Cape Cross) · anochecer **19:20** (Terrace Bay) — *pero aquí el sol no es
  el límite: lo es la puerta de las 15:00*
- ⏰ **Salida temprana — este día tiene una hora límite.** C34 costera (sal compactada):
  Swakopmund → Henties Bay → 🦭 **Cape Cross** (miles de lobos marinos; pañuelo para el olor)
- 🎫 **Cape Cross cobra entrada propia, aparte del permiso de Skeleton Coast:** **N$150 (~€8)/extranjero
  + N$50 (~€3)/coche** (≤10 plazas) = **~N$350 (~€18) los dos** ◐, en **efectivo**, se paga en recepción
  al entrar (reserva dentro del Dorob NP; tarifa menor que el baremo premium, **no** son las 7 unidades
  de `02` §5 — súmalo). Horario ◐: **abre a las 08:00 solo del 16 nov al 30 jun; el resto del año, a
  las 10:00** *(confirmado por búsqueda; la ficha del MEFT sigue en 403)*. **Ojo: vuestro D7 es el 7 nov,
  antes del 16 → Cape Cross abre a las 10:00, NO a las 08:00.** No hay entrada a primera hora: apuntad
  el alto de los lobos a las 10:00 en punto y salid seguidos. De Cape Cross a Ugabmund quedan ~110 km:
  cruzáis de sobra antes de las 15:00, pero sin la holgura que daría un 08:00 — no os entretengáis
- 🛑 **Puerta de Ugabmund: última entrada 15:00.** Para pernoctar dentro hace falta **reserva
  confirmada de Terrace Bay** — sin ella no se entra (el permiso de tránsito obliga a salir el
  mismo día)
- Dentro del parque: **60 km/h** · 🎫 Skeleton Coast ~N$620 (~€31)/24 h
- 🛏️ **Terrace Bay (NWR)** — dormir en la Costa de los Esqueletos, con la niebla y el
  Atlántico rugiendo. **Ojo: es un resort con media pensión (DBB), no un camping.** Suelo publicado
  (doméstico/SADC, temporada baja): **N$1.440–1.920/persona DBB (~€72–96)**; como extranjeros en
  noviembre, **más** ◐ — la noche más cara de la ruta *(tarifa internacional nov 2026 aún ❌; ver `15`)*
- 💰 **Precio cerrado (03/08) ✅:** el PDF oficial de tarifas de NWR 2026/2027 da para Terrace Bay
  **habitación doble en media pensión a N$1.740/persona → N$3.480 (~€174) los dos**, en tu ventana.
  **No hay camping**: la ficha web listaba una fila de «Campsite» que **no existe en el tarifario**
  — es un error de su web. Es **la noche más cara del viaje**, pero incluye **cena y desayuno**.
- *Variante fácil: saltarse Terrace Bay, dormir en Henties/Swakopmund y entrar a Damaraland al día
  siguiente por Springbokwasser en tránsito — un día mucho más corto*

### D8 · dom 8 — Skeleton Coast → Twyfelfontein → Hoada · **~370 km · ~5h30–6h de volante** ◐
- 🌡️ **Hoada/Grootberg: medias de noviembre ~33,1 °C máx / ~18,4 °C mín** ◐ *(reanálisis ERA5,
  ninguna estación GHCN cae cerca; ver `15` §ERA5)*. **Es un suelo, no un techo**: en sabana seca
  ERA5 se queda ~2 °C corto, así que el mediodía real ronda **34–35 °C**. Está entre la meseta (~31)
  y el norte caluroso; Twyfelfontein, en el valle, es **aún más caluroso a mediodía** ○
- ☀️ amanecer **06:17** (Twyfelfontein) · anochecer **19:15** (Hoada) — *y es domingo otra vez:
  sin alcohol a la venta*
- Salida por **Springbokwasser** → C39/D3245 → **Twyfelfontein** (grabados rupestres UNESCO; Google
  lo lista como cerrado: **es un fallo del listado**). **Terrace Bay → Twyfelfontein son ~216 km ◐**
  *(verificado 03/08: 96 a la puerta de Springbokwasser + 120 a Twyfelfontein; ver `13` y `15`)*; y la
  cola **Twyfelfontein → Hoada son ~155 km ◐** *(verificado 03/08 — vía Palmwag o vía Grootberg, ambas
  convergen; «~2,5 h» del operador)*. **Es un día largo (~370 km de grava): sal temprano de Terrace
  Bay.** El ~85 km que se manejaba antes quedó **refutado** —era menor que la línea recta (~95 km).
- ⚠️ **Damaraland: los bajos son el punto delicado del seguro** — la referencia de Asco los
  excluía aquí, y **cómo los trata el Premium Cover de tu Namibia2Go Budget sigue SIN confirmar:
  pregúntalo por escrito al reservar**. Despacio en las piedras.
- 🛏️ **Hoada Campsite** (zona Grootberg) — el blog lo llama su campamento más bonito del viaje:
  rocas de granito, duchas entre peñas, cielo estrellado. **N$271–366/persona según temporada
  (~€14–18 pp) → N$542–732/noche la pareja (~€27–37)** ◐ *(la temporada de noviembre sin fijar; ver `15`)*

### D9 · lun 9 — Hoada → Etosha (Okaukuejo) · **~340 km · ~4h30** ◐
- 🌡️ **Okaukuejo, medias de noviembre: 37,1 °C máx / 18,9 °C mín** ✅ *(NOAA GHCN, serie completa
  1975–2022, recomputada en `15` en dos extracciones independientes)* — y **baja según avanza el
  mes**: 37,8 en octubre → 37,1 en noviembre → 35,6 en diciembre
- ☀️ amanecer **06:18** (Hoada) · anochecer **19:08** (Okaukuejo) — *las puertas de Etosha cierran
  al ocaso: pasa Andersson con margen de sobra*
- C40 a Kamanjab → C38 a la puerta de **Andersson** (asfalto desde Kamanjab... ⚠️ firme por
  confirmar) → **Okaukuejo a 17 km** de la puerta
- ✅ **Son ~340 km (verificado 04/08, antes se manejaba ~315)**: Hoada → Kamanjab **75 km** + Kamanjab
  → Okaukuejo por Outjo **~265–271 km** *(distancesto: Kamanjab–Outjo 156 km; CityMeter: Kamanjab–Okaukuejo
  271 km; la matriz de 2010 daba 265, convergen)*. **El ~315 queda refutado.** Cuenta ~340 para el
  depósito y la hora de puerta. Ver [`13`](13-itinerario.md), §3.
- 🎫 Etosha ~N$620 (~€31)/24 h × 4 días · trámite de puerta 20–30 min · **60 km/h dentro**
- 🌙 **Noche en la charca iluminada de Okaukuejo** — rinocerontes negros
- 🛏️ **Camping Okaukuejo — N$920 (~€46)** ✅ · *capricho: chalet del charco N$4.760 (~€238)*

### D10 · mar 10 — Safari Okaukuejo → Halali · **~90 km de safari lento** ✅
- 🌡️ **Etosha, medias de noviembre: 37,1 °C máx / 18,9 °C mín** ✅ *(GHCN Okaukuejo, la estación
  del parque)* — la cifra más alta del viaje. **A mediodía no se hace safari: piscina** ○
- ☀️ amanecer **06:12** · anochecer **19:06** (Halali) — *dentro del campamento, del ocaso al
  amanecer: la charca iluminada ES el plan de la noche*
- 🚧 **Obras Okaukuejo–Halali–Namutoni — CONFIRMADO que te afectan (act. 03/08, ◐)**: el MEFT
  reconstruye la pista central para asfaltarla, y ya hay **nota oficial de 2026** —«Traffic deviation
  via Gemsbokvlakte road from Okaukuejo to Halali» *(meft.gov.na/news/335)*, con aviso paralelo de
  NWR— que fija un **desvío OBLIGATORIO desde el 2 de junio de 2026 y hasta julio de 2027**. Tu
  ventana de la primera quincena de noviembre **cae de lleno dentro**: da por hecho que la carretera directa
  Okaukuejo→Halali estará **cerrada** y que irás por el bypass — no lo dejes como un «quizá».
  *(No se pudo abrir la página oficial (403); las fechas las dan cinco fuentes secundarias que
  concuerdan, por eso va en ◐. Confírmalo con NWR Okaukuejo **+264 67 229 800** por si hubiera
  cambio de última hora.)*
- 🚗 **El desvío en la práctica ◐**: desde Okaukuejo se sigue por grava hasta **~km 47** y ahí se
  toma el **bypass nuevo y el Rhino Drive** hacia Halali. Las charcas accesibles en ese tramo se
  reducen a **Gemsbokvlakte, Sueda y Salvadora**; **Nebrownii y Kapupuhedi quedan fuera** por la
  obra. Recomiendan vehículo alto —tu Hilux cumple—. **No hay cifra oficial del sobrecoste en tiempo**:
  cuéntalo despacio.
- ✅ **Y el desvío no es un castigo**: **Gemsbokvlakte–Sueda–Salvadora** es de los mejores tramos de
  borde de la depresión para **guepardo y león**
- Charcas del camino · siesta en la piscina de Halali · charca de Halali al anochecer
- 🛏️ **Camping Halali — N$920 (~€46)** ✅

### D11 · mié 11 — Safari Halali → Namutoni · **~80 km de safari** ✅
- 🌡️ **Etosha 37,1 / 18,9 ✅** — la noche más cálida del viaje: casi 19 °C de mínima
- ☀️ amanecer **06:08** · anochecer **19:05** — *el safari bueno es 06:10–09:00 y 16:30–19:00;
  al mediodía, piscina y siesta*
- Charcas **Goas, Nuamses, Springbokfontein, Batia, Chudop** — el corazón del safari
- **Se duerme DENTRO, como todo Etosha en esta ruta**: sin horas de puerta, con la charca al lado
- 🛏️ **Camping Namutoni — N$920 (~€46)** ✅ *(el fuerte alemán, y Chudop a un paso)*
- *Capricho opcional: **Onguma** (tu pin, reserva privada justo al otro lado de la puerta de Von
  Lindequist) ⚠️ precio sin verificar; puede ser gama alta — a cambio pierdes estar dentro*

### D12 · jue 12 — Etosha este · **~60–80 km de safari** ✅
- 🌡️ **Etosha 37,1 / 18,9 ✅**
- ☀️ amanecer **06:08** · anochecer **19:05**
- **Fischer's Pan**, Chudop, Klein Namutoni — la esquina que casi nadie hace. *Ojo: Fischer's Pan
  es el mejor sitio de aves acuáticas del parque **cuando hay agua**, y en noviembre está seco —
  lo que va bien es Chudop (león fiable) y el **Dik-dik Drive** de Klein Namutoni* ◐
- 🛏️ **Namutoni, segunda noche — N$920 (~€46)** ✅

### D13 · vie 13 — Etosha → Windhoek · **~550 km asfalto · ~5h30–6h** ○
- 🌡️ De **Etosha (37,1 ✅)** a **Windhoek (31,2 ✅)**: el día de bajar 6 grados y 550 km
- ☀️ amanecer **06:08** (Namutoni) · anochecer **19:11** (Windhoek) — *la puerta de Von Lindequist
  abre al amanecer: saliendo a las 06:10 llegas a Windhoek con la tarde entera*
- Von Lindequist → Tsumeb → Otjiwarongo → B1 · salida al alba, comida en Otjiwarongo
- 🥩 **Línea Roja**: la carne cruda no baja del norte — el braai se come en Etosha
- 🛏️ Windhoek — **entrega del coche HOY**: el contrato de 12 días acaba el 13. *(Alternativa
  pendiente de decidir: añadir el día 13, ~€150 · ~N$3.000, y devolverlo el 14 camino del
  aeropuerto)*
- *Parada opcional de camino: **Okonjima/AfriCat** (leopardos) o el meteorito de **Hoba** (desvío
  por Grootfontein)*

### D14 · sáb 14 — Vuelo
- ✈️ **Despegue a las 20:45** *(vuelo de Oporto, [`02`](02-presupuesto.md) §8)* — no es una mañana
  de aeropuerto: es **un día entero en Windhoek** antes de embarcar
- ☀️ amanecer **06:01**
- ⚠️ **Y ese día no tienes coche** con la cotización actual, que lo devuelve el 13 a las 17:00.
  **O se alarga el alquiler al 14 por la tarde, o hay que llenar el día a pie y con traslado al
  aeropuerto** *(~45 km)* — ver [`02`](02-presupuesto.md) §2
- 💱 **Gasta o cambia los N$ antes de embarcar**: fuera de Namibia no valen nada

### 💰 Coste real de E *(1–15 nov · el detalle completo, en `02-presupuesto.md`)*
- **Alquiler 13 días (1 nov 08:00 – 13 nov 17:00)**: **Namibia2Go Budget N$35.100 (~€1.755)** ✅
  — o **Comfort N$39.000 (~€1.950)**; las dos disponibles. ⚠️ **Hay que recotizarlo a 15 días** para
  que cubra el vuelo (ver `02` §2), con Premium Insurance Cover (franquicia cero) y km ilimitados *(Asco, descartada:
  €2.652 en su banda alta)*
- **Noches NWR verificadas**: Sesriem 2×1.340 + Okaukuejo 920 + Halali 920 + Namutoni 2×920 =
  **N$6.360 (~€318)** ✅ — **las 4 noches de Etosha, dentro del parque**
  *(+ Terrace Bay, Spreetshoogte, Walvis, Hoada: sin verificar)*
- **Tasas de parque**: Namib 2 + Skeleton 1 + Etosha 4 = 7 unidades × N$620 ≈ **N$4.340 (~€217)** ◐
- **Combustible ~2.728 km**: ~310–340 l ≈ **N$8.000–9.200 (~€400–460)** ○
- **Visado**: N$3.200 (~€160) los dos ✅
- **Total tierra en camping ≈ ~€3.610 (~N$72.200)** la pareja ○, banda ~€3.310–3.910 — *el coche es
  cifra cerrada. Sumando vuelos (**€2.900**) y seguro IATI Estrella (€226,04):
  **~€6.736 (~N$134.700) la pareja · ~€3.368 por persona** (ver `02`)*

### ⏰ Los horarios que mandan *(✅/◐ = con fuente en el dossier · ☀️ = cálculo astronómico ±5 min)*

- **Sesriem** ✅: puerta exterior de amanecer a ocaso; la interior, **1 h antes del amanecer y 1 h
  después del ocaso**. Para tus noches del 3–4 nov ☀️: interior **~05:10–20:10**, exterior
  **~06:10–19:10**. *Confírmalo en recepción al llegar: se mueve con el orto real (`06`).*
- **Skeleton Coast** ◐: para pernoctar en Terrace Bay hay que cruzar Ugabmund **antes de las
  15:00** y con **reserva confirmada** (`11`). Horarios de puerta: las fuentes bailan — NWR/foros
  daban 07:30–19:00; guías recientes, Ugab 07:30–15:00 y Springbokwasser 07:30–17:00 (`08`). **En
  la práctica manda el 15:00.**
- **Etosha** ✅ — **horarios oficiales de puerta**, de la tabla que publica el parque *(cambian cada
  semana siguiendo al sol, y están puestas en cada puerta)*: **3–9 nov: 06:13–19:06** ·
  **10–16 nov: 06:10–19:10**. Son **trece horas de parque al día**, casi dos más que en invierno.
  *(Cuadra al minuto con el cálculo astronómico de arriba.)* Dentro: **60 km/h**, **20 en los
  campamentos**, y **solo se puede bajar del coche dentro de los campamentos** — la única excepción
  es el *koppie* de dolomita de **Halali**, que sí se puede pasear. De noche te quedas dentro: la
  charca iluminada es el plan.
- **Kiosco SIM de MTC en el aeropuerto** ◐: cierra **~21:00** — aterrizas a las **09:25**, de sobra.
- **Alcohol** ✅: bottle stores y secciones de licores **cierran domingos y festivos**. Tus
  domingos de viaje: **1 nov (el día que llegas) y 8 nov** — compra el sábado.
- **Otjitotongwe (guepardos)** ◐ — C40, a 24 km de Kamanjab, de camino el D9 (lunes):
  alimentación **~15:00**; si no te alojas, avisa antes. *(Una fuente dice que cierra los fines
  de semana — tu paso es lunes.)*
- **Gasolinera en Etosha** ✅⚠️: los tres campamentos **listan «Filling Station» en la web oficial
  de NWR**, pero con historial de cortes en 2025 — entra lleno desde Outjo; respaldo: la Etosha
  Trading Post a 6,5 km de Andersson (`08`).
- **❌ Sin verificar — pídelo al reservar con NWR:** horarios de desayuno/restaurante de los
  campamentos (importa para salir al alba: pide desayuno para llevar o hazlo tú) y el horario de
  Joe's Beerhouse.

### 🦁 En los parques: ¿tu 4x4 o el vehículo del parque?

**Regla general de esta ruta: tu 4x4 vale para TODO el safari diurno — lo guiado se compra solo
donde añade algo que por libre es imposible o está prohibido.**

- **Etosha → tu 4x4, self-drive** ✅. Las pistas principales son aptas para tu Hilux (60 km/h,
  parando en cada charca); **no hace falta ningún vehículo del parque para el safari de día**, y
  además tenéis **13 horas de puerta a puerta**. Lo que **sí** merece pagarse: el **safari nocturno
  guiado de NWR (N$750 · ~€38/persona)** ✅ — de noche está **prohibido circular por libre**, así que
  es literalmente la única forma de estar en el parque a oscuras. Buen plan: una noche en Okaukuejo
  (D9). *(La charca iluminada del campamento es gratis y no necesita vehículo: andando desde tu
  parcela.)* Tips ○: en las charcas apaga el motor y dale 15–20 min — la fauna llega por turnos;
  los coches parados en racimo delatan un avistamiento; lleva los prismáticos EN el asiento.

#### 🎟️ Las excursiones que se pueden contratar

Los **tres campamentos donde dormís venden lo mismo** ✅ *(fichas de NWR, 03/08)*: safari guiado de
**mañana N$650**, de **tarde N$650** y **nocturno N$750** *(≈ €33 · €33 · €38)*, por persona. ❌ **Los horarios de salida
no los publican en ninguna parte**: pregúntalos en recepción al llegar.

**De día no compensa** en vuestro caso: ya tenéis 4x4, trece horas de puerta a puerta y libertad para
quedaros en una charca el rato que queráis. Lo que compra el guiado son los ojos del guía y un
vehículo alto — legítimo, pero no cambia el viaje.

**El nocturno sí**, porque de noche está **prohibido circular por libre**: es la única forma de estar
en el parque a oscuras y ver oricteropo, puercoespín, liebre saltadora o leones cazando. **N$1.500
(~€75) los dos.**

> ### 👉 Y hazlo desde NAMUTONI, no desde Okaukuejo
> Sale de cruzar dos datos: la charca iluminada de **Okaukuejo es probablemente el mejor sitio de
> África para ver rinoceronte negro de noche**, y la de **Halali es famosa por el leopardo y el
> puercoespín** — las dos **gratis y andando desde la parcela**. La de **Namutoni es la más floja**.
> **Gasta el nocturno la noche en que menos pierdes.**
>
> ⚠️ Pregunta al reservar si **se puede dejar cerrado desde España**: la tarifa de NWR avisa de que
> no acepta reservas anticipadas de actividades en temporada de lluvias. 📞 +264 67 229 800.
> 💶 Y ojo: el nocturno **se come entero** el margen de actividades del presupuesto (~€38 p.p.).

**Fuera de Etosha**, ya en el dossier: la **lanzadera de Deadvlei N$180** ✅, el safari guiado de
mañana de Sesriem N$600–700 (~€30–35), Elim Dune N$300 (~€15) y el cañón N$200 (~€10) *(ver [`03`](03-alojamiento-y-tasas.md))*.

**Y las reservas privadas —Ongava, Okonjima, Onguma— no son una mejora del plan**: una sola noche en
Ongava cuesta **~N$34.600 (~€1.730) los dos**, el triple que las trece noches de camping de todo el viaje. Son
otro producto. *(Okonjima, por sus leopardos habituados, es el único capricho con argumento — como
parada del D13.)*

### 🔍 En qué se diferencia del blog *(y por qué)*
- **Ellos, 2 noches en Spreetshoogte; nosotros, 1** — la segunda se va a Etosha, que con tu ventana
  seca merece 4 noches
- **Ellos duermen en Onguma (fuera); nosotros las 4 noches DENTRO del parque** (Okaukuejo, Halali,
  Namutoni ×2 — verificado, N$920 ≈ €46/noche) — dormir dentro es lo que da las charcas nocturnas
  iluminadas y los amaneceres sin esperar puerta. Onguma queda como capricho opcional
- **Mismo espíritu**: Terrace Bay, Hoada, dos noches en la costa, y el sur para otro viaje
- ⚠️ Sus precios (Spreetshoogte 150–300 ZAR) son de la fecha de su post: **no presupuestar con ellos**

### ⛔ Lo que queda fuera *(y dónde está documentado por si vuelve)*
**Fish River Canyon** · **kokerbooms** · **caballos de Garub** · **D707** · **Lüderitz/Kolmanskop**
· **Spitzkoppe** *(tampoco está en la ruta del blog; si os duele,
cabe como parada larga la mañana del D13 alternativo vía Usakos — pero alarga el día)*

---

<div align="center">

## 🧭 Por qué esta ruta y no otra

Con **Sossusvlei y Etosha fijos**, lo que competía por los días era el sur — Fish River, Lüderitz,
Kolmanskop. Medido en kilómetros y horas, **no cabía**: el sur profundo y Etosha están en extremos
opuestos del país y cada uno pide varios días. Intentar las dos coronas convierte el viaje en
catorce días **conduciendo por delante de los sitios en vez de estar en ellos** — y la fatiga en
grava es justo el ingrediente del vuelco (ver `06`).

**Así que el sur se quitó entero**, y sus días se fueron a donde más rinden: **dos noches en
Sesriem** para el amanecer de Deadvlei sin prisa, **dos en la costa** para descansar a mitad de
viaje, y **cuatro dentro de Etosha**. El resultado son ~2.600 km, ningún día por encima de ~390 km,
y el safari como clímax final.

<div align="center">

## 🕳️ Lo que falta para cerrar LA RUTA DEL VIAJE

- ✅ **Vuelos** — precio final: €1.450 (~N$29.000) p.p., **Oporto → Windhoek, 30 oct – 14 nov**. *Pendiente
  solo de emitir el billete*
- ❌ **Tres noches sin precio** — Terrace Bay, Spreetshoogte *(candidato: Camp Gecko, banda
  contradictoria)* y Walvis Bay ×2, más el hotel del D13. **Hoada ya tiene precio** ◐ (arriba), y
  los lodges privados siguen sin rack/noche (Gondwana y las webs propias, en 403). ⛺ También
  cerrado el **camping de Spitzkoppe: N$270/persona → N$540/noche (~€27), entrada incluida** ◐
  *(fuera de la ruta)*
- ◐ **Km del D7 y del D13 ya cerrados (03/08)** — la costa **Walvis Bay → Terrace Bay ≈ ~380 km**
  (C34 300 km Swakopmund→Torra Bay + 50 a Terrace Bay + 30 de Walvis, fuentes convergentes) y el
  **Namutoni → Windhoek ≈ ~555–575 km** (web de Etosha NP y rome2rio). Detalle y fuentes en `13`.
- ◐ **Km del D8 ya cerrados (03/08)** — **Terrace Bay → Twyfelfontein ≈ ~216 km** por la ruta directa
  de Springbokwasser (96 a la puerta + 120 a Twyfelfontein; routeplanner + negativo de la C39) **y la
  cola Twyfelfontein → Hoada ≈ ~155 km** (Palmwag ~110 + ~50, o Grootberg ~130 + 25; «~2,5 h» del
  operador), fuentes convergentes. El **D8 sube así a ~370 km**: es un día largo. El ~85 km anterior
  quedó **refutado** (menor que la línea recta de ~95 km). Detalle y fuentes en `13`.
- 🚧 **Las obras de Etosha** — **desvío obligatorio Okaukuejo→Halali en vigor hasta julio de 2027**
  *(afecta al D10; detalle y fuente en ese día)*. Confírmalo con NWR al reservar.
