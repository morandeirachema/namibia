# 01 · Los itinerarios, día a día

> **Namibia · 31 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](README.md)
>
> La la ruta desarrollada día por día —con sol, temperatura, horarios y precios— y las variantes descartadas, como referencia.
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
> SU temporada baja**: el coche está **cerrado — Budget, €1.800 (~N$36.000) por 12 días, disponible**
> *(la estimación previa de ~€1.755 quedó a un 2,5 % del precio real)*. **Adelantar hasta 2 días a
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
> aquí solo hay estación o secundaria que cite estación — **y donde no la hay, dice «sin dato»**.
>
> ```mermaid
> flowchart TD
> T["Noviembre donde duermes<br/>media de máxima / mínima, en °C"]
> n0["Walvis Bay · la costa<br/>25,0 día / 12,7 noche"]
> n1["Windhoek<br/>31,2 día / 16,3 noche"]
> n2["Sesriem · el desierto<br/>32,5 día / 15,5 noche"]
> n3["Okaukuejo · Etosha<br/>37,1 día / 18,9 noche"]
> T ~~~ n0
> n0 ~~~ n1
> n1 ~~~ n2
> n2 ~~~ n3
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
>     D["POR ELEGIR CAMPING · 3 noches<br/>D1 Windhoek y D5-D6 Walvis Bay: SI hay coche,<br/>asi que se puede dormir arriba — falta elegir sitio"]
>     P["LA PISTA QUE LO CAMBIA · D7 Terrace Bay<br/>la tabla de tarifas de NWR lista camping a N$460/persona<br/>pero su descripcion solo habla de chalets: PREGUNTAR"]
>     N["NO SE PUEDE · D13 Windhoek<br/>el coche se entrega ese dia, asi que toca habitacion<br/>salvo que se anada el dia 13 de alquiler (~150 EUR)"]
>     T ~~~ D ~~~ P ~~~ N
>     style T fill:#2d6a4f,color:#fff
>     style P fill:#e85d04,color:#000
>     style N fill:#9d0208,color:#fff
> ```
>
> **El recuento, que suma 13:** **8** ya resueltas en tienda · **3** en las que se puede dormir
> arriba pero falta elegir camping *(D1 y D5–D6)* · **1** que depende de una llamada *(D7 Terrace
> Bay)* · **1** imposible *(D13, sin coche)*.
>
> 👉 **Si Terrace Bay confirma el camping y se añade el día 13 de alquiler, se puede dormir arriba
> las 13 noches.** Sin tocar nada, ya son 12 de 13.
>
> ### 🚗 ¿Y cuántos días estáis en Windhoek sin coche? **Uno.**
>
> El alquiler va del **1 al 13 de noviembre** —12 días—, así que:
>
> - **D1, 1 de noviembre**: aterrizáis a las 13:20 y **recogéis el coche ese mismo día**. Esa noche
>   **sí** hay 4x4: se puede acampar.
> - **De D2 a D12**: coche todos los días.
> - **D13, viernes 13**: se **entrega** el coche. Esa noche, y solo esa, dormís **sin 4x4** →
>   habitación en Windhoek y **traslado al aeropuerto** al día siguiente.
> - **D14, sábado 14**: el vuelo sale a las 14:30 y ya no hay coche.
>
> 💡 **La alternativa que lo evita:** añadir el **día 13 de alquiler (~€150 · ~N$3.000)** y devolver
> el coche el 14 camino del aeropuerto. Te ahorras el hotel y **dos traslados**, así que puede salir
> igual o más barato — y duermes arriba también la última noche.

### D1 · dom 1 nov — Llegada a Windhoek
- 🌡️ **Windhoek, medias de noviembre: 31,2 °C máx / 16,3 °C mín** ✅ *(NOAA GHCN, estación 68110,
  1.700 m, serie 1957–2025; ver `15`)* — cálido de día, pero a 1.700 m **refresca de noche**
- ☀️ amanecer **06:07** · anochecer **19:04**
- ⚠️ **Es domingo: las bottle stores y las secciones de alcohol cierran por ley** (ver `04`) — la
  compra de cervezas para el braai espera al lunes
- 4x4 + briefing (1–2 h): **presiones en frío apuntadas, las DOS ruedas de repuesto, gato y
  compresor a la vista** antes de salir del patio (`06`)
- Efectivo (~N$6.000–8.000) · **SIM de MTC** con pasaporte *(el kiosco cierra ~21:00)*
- 🍺 **Joe's Beerhouse** · 🛏️ Windhoek

### D2 · lun 2 — Windhoek → paso de Spreetshoogte · **~180–200 km · ~3h–3h30** ◐
- 🌡️ **Spreetshoogte: sin dato de estación.** El proxy razonable es **Windhoek (31,2/16,3 ✅)**:
  misma altitud (~1.700 m) en el borde de la escarpa. Arriba corre viento y refresca al caer el
  sol ○
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
- Tarde: **Sesriem Canyon** y atardecer en **Elim Dune** *(o el guiado de NWR, N$300/persona)*
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
  N$180/persona)*
- 🛏️ Sesriem, segunda noche

### D5 · jue 5 — Sesriem → Walvis Bay · **~270 km · ~5h30** ✅
- 🌡️ **Walvis Bay, medias de noviembre: 25,0 °C máx / 12,7 °C mín** ✅ *(NOAA GHCN, estación del
  aeropuerto WMO 68098, serie 1990–2025; ver `15`)* — **la costa es el respiro térmico del viaje**:
  la corriente de Benguela. Pero ojo a la madrugada: **12–14 °C**, y viento. Cortavientos a mano
- ☀️ amanecer **06:15** · anochecer **19:17** (Walvis Bay)
- C14 por los pasos de **Gaub y Kuiseb** + Trópico de Capricornio
- ⛽ **Solitaire otra vez, sí o sí** — después, **210 km sin nada**
- 🛏️ **Walvis Bay** ⚠️ *precio sin verificar (el blog usó Lagoon Chalets)*

### D6 · vie 6 — Walvis Bay: flamencos y descanso ✅
- 🌡️ **Walvis Bay 25,0 / 12,7** ✅ — el día fresco del viaje: aprovecha para el Welwitschia Drive
- ☀️ amanecer **06:14** · anochecer **19:17** — *flamencos con la primera luz, ~06:15–07:30*
- 🦩 **Y tu mes es de los buenos**: en Walvis Bay los flamencos tienen su **máximo de junio a
  noviembre** ✅ *(SABAP1)*. Aquí sí los hay en cantidad — en Etosha, en cambio, **no**: la depresión está
  seca en noviembre *(ver `09`)*
- 🦩 **Flamencos y pelícanos en la laguna** al amanecer y al atardecer — las mejores luces
- Día libre: paseo marítimo, ostras, o la excursión guiada a **Sandwich Harbour**
  *(🚫 con tu coche está prohibida por contrato — el tour es la forma correcta y mejor)*
- 🛏️ Walvis Bay, segunda noche

### D7 · sáb 7 — Cape Cross → Terrace Bay (Skeleton Coast) · **~390 km · día logístico** ✅
- 🌡️ **Terrace Bay: sin dato de estación** — no hay serie pública ni en Möwe Bay ni en Terrace
  Bay. Proxy honesto: **la costa ronda los 25,0 °C de Walvis Bay ✅**, 400 km más al sur — cuenta
  con **niebla, viento y menos calor que tierra adentro** ○
- ☀️ amanecer **06:18** (Cape Cross) · anochecer **19:20** (Terrace Bay) — *pero aquí el sol no es
  el límite: lo es la puerta de las 15:00*
- ⏰ **Salida temprana — este día tiene una hora límite.** C34 costera (sal compactada):
  Swakopmund → Henties Bay → 🦭 **Cape Cross** (miles de lobos marinos; pañuelo para el olor)
- 🛑 **Puerta de Ugabmund: última entrada 15:00.** Para pernoctar dentro hace falta **reserva
  confirmada de Terrace Bay** — sin ella no se entra (el permiso de tránsito obliga a salir el
  mismo día)
- Dentro del parque: **60 km/h** · 🎫 Skeleton Coast ~N$620/24 h
- 🛏️ **Terrace Bay (NWR)** — dormir en la Costa de los Esqueletos, con la niebla y el
  Atlántico rugiendo. **Ojo: es un resort con media pensión (DBB), no un camping.** Suelo publicado
  (doméstico/SADC, temporada baja): **N$1.440–1.920/persona DBB (~€72–96)**; como extranjeros en
  noviembre, **más** ◐ — la noche más cara de la ruta *(tarifa internacional nov 2026 aún ❌; ver `15`)*
- 💡 **Y una pista que puede cambiar la noche (03/08):** la **tabla de tarifas de NWR para Terrace
  Bay lista «Campsite (Max 5 People) — N$460/persona»**, el mismo precio que los campings de
  Etosha, para las dos temporadas. Pero **la descripción del sitio solo habla de 3 beach chalets y
  20 habitaciones dobles**, así que es ambiguo. 👉 **Pregúntalo al reservar**: si hay camping, esta
  noche pasa de ser **la más cara del viaje (~€144–192 los dos, media pensión)** a **N$920 (~€46)**
  — y de habitación a tienda de techo.
- *Variante fácil: saltarse Terrace Bay, dormir en Henties/Swakopmund y entrar a Damaraland al día
  siguiente por Springbokwasser en tránsito — un día mucho más corto*

### D8 · dom 8 — Skeleton Coast → Twyfelfontein → Hoada · **~300 km · ~5h** ◐
- 🌡️ **Hoada/Grootberg: sin dato de estación** *(ninguna de las 11 estaciones GHCN de Namibia cae
  cerca — ver `15`)*. Está entre la meseta (~31 °C) y el norte caluroso; Twyfelfontein, en el
  valle, es **notablemente más caluroso a mediodía** ○
- ☀️ amanecer **06:17** (Twyfelfontein) · anochecer **19:15** (Hoada) — *y es domingo otra vez:
  sin alcohol a la venta*
- Salida por **Springbokwasser** → C39 a Bergsig → **desvío opcional a Twyfelfontein**
  (grabados rupestres UNESCO; Google lo lista como cerrado: **es un fallo del listado**)
- ⚠️ **Damaraland: los bajos son el punto delicado del seguro** — la referencia de Asco los
  excluía aquí, y **cómo los trata el Premium Cover de tu Namibia2Go Budget sigue SIN confirmar:
  pregúntalo por escrito al reservar**. Despacio en las piedras.
- 🛏️ **Hoada Campsite** (zona Grootberg) — el blog lo llama su campamento más bonito del viaje:
  rocas de granito, duchas entre peñas, cielo estrellado. **N$271–366/persona según temporada
  (~€14–18 pp) → N$542–732/noche la pareja (~€27–37)** ◐ *(la temporada de noviembre sin fijar; ver `15`)*

### D9 · lun 9 — Hoada → Etosha (Okaukuejo) · **~315 km · ~4h** ◐
- 🌡️ **Okaukuejo, medias de noviembre: 37,1 °C máx / 18,9 °C mín** ✅ *(NOAA GHCN, serie completa
  1975–2022, recomputada en `15` en dos extracciones independientes)* — y **baja según avanza el
  mes**: 37,8 en octubre → 37,1 en noviembre → 35,6 en diciembre
- ☀️ amanecer **06:18** (Hoada) · anochecer **19:08** (Okaukuejo) — *las puertas de Etosha cierran
  al ocaso: pasa Andersson con margen de sobra*
- C40 a Kamanjab → C38 a la puerta de **Andersson** (asfalto desde Kamanjab... ⚠️ firme por
  confirmar) → **Okaukuejo a 17 km** de la puerta
- 🎫 Etosha ~N$620/24 h × 4 días · trámite de puerta 20–30 min · **60 km/h dentro**
- 🌙 **Noche en la charca iluminada de Okaukuejo** — rinocerontes negros
- 🛏️ **Camping Okaukuejo — N$920 (~€46)** ✅ · *capricho: chalet del charco N$4.760 (~€238)*

### D10 · mar 10 — Safari Okaukuejo → Halali · **~90 km de safari lento** ✅
- 🌡️ **Etosha, medias de noviembre: 37,1 °C máx / 18,9 °C mín** ✅ *(GHCN Okaukuejo, la estación
  del parque)* — la cifra más alta del viaje. **A mediodía no se hace safari: piscina** ○
- ☀️ amanecer **06:12** · anochecer **19:06** (Halali) — *dentro del campamento, del ocaso al
  amanecer: la charca iluminada ES el plan de la noche*
- 🚧 **Obras — el detalle, actualizado 03/08**: están **asfaltando la pista Okaukuejo–Halali–
  Namutoni**. En 2025 el MEFT desvió el tráfico **por la carretera de Gemsbokvlakte** y cerró la
  salida de Okaukuejo hacia Halali; en 2026 seguía habiendo bypass. Las charcas de **Nebrownii y
  Kapupuhedi quedaron inaccesibles** por la obra. ⚠️ **No hay nota oficial posterior a 2025:
  llama a NWR Okaukuejo (+264 67 229 800) antes de ir.**
- ✅ **Y el desvío no es un castigo**: pasa por **Gemsbokvlakte y luego Sueda–Salvadora–Charitsaub**,
  que es el mejor tramo de borde de la depresión para **guepardo y león**
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
- ☀️ amanecer **06:01** · *(despegue 14:30 — mañana tranquila)*
- 💱 **Gasta o cambia los N$ antes de embarcar**: fuera de Namibia no valen nada

### 💰 Coste real de E *(1–15 nov · el detalle completo, en `02-presupuesto.md`)*
- **Alquiler 12 días (1–13 nov)**: **Namibia2Go Budget €1.800 (~N$36.000)** ✅ **cerrado y
  disponible**, con Premium Insurance Cover (franquicia cero) y km ilimitados *(Asco, descartada:
  €2.652 en su banda alta)*
- **Noches NWR verificadas**: Sesriem 2×1.340 + Okaukuejo 920 + Halali 920 + Namutoni 2×920 =
  **N$6.360 (~€318)** ✅ — **las 4 noches de Etosha, dentro del parque**
  *(+ Terrace Bay, Spreetshoogte, Walvis, Hoada: sin verificar)*
- **Tasas de parque**: Namib 2 + Skeleton 1 + Etosha 4 = 7 unidades × N$620 ≈ **N$4.340 (~€217)** ◐
- **Combustible ~2.600 km**: ~310–340 l ≈ **N$8.000–9.200 (~€400–460)** ○
- **Visado**: N$3.200 (~€160) los dos ✅
- **Total tierra en camping ≈ ~€3.650 (~N$73.000)** la pareja ○, banda ~€3.350–3.950 — *ya sin
  rango de compañía: el coche es cifra cerrada. Sumando vuelos (€2.732) y seguro IATI Estrella
  (€226,04): **~€6.612 (~N$132.000) la pareja · ~€3.306 por persona** (ver `02`)*

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
- **Kiosco SIM de MTC en el aeropuerto** ◐: cierra **~21:00** — aterrizas a las 13:20, de sobra.
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

#### 🎟️ Las excursiones que se pueden contratar, con precio ✅

**Verificado el 03/08/2026 en las fichas de los propios campamentos de NWR** — y **los tres donde
dormís venden lo mismo**, por persona:

- 🌅 **Safari guiado de mañana — N$650 (~€33)**
- 🌇 **Safari guiado de tarde — N$650 (~€33)**
- 🌙 **Safari NOCTURNO guiado — N$750 (~€38)**

*(Fuentes: fichas de [Okaukuejo](https://www.nwr.com.na/resorts/okaukuejo-resort/),
[Halali](https://www.nwr.com.na/resorts/halali-resort/) y
[Namutoni](https://www.nwr.com.na/resorts/namutoni-resort/) en nwr.com.na.)*

#### 🕐 Los horarios de salida: **NWR no los publica** ❌

Buscado el 03/08/2026 y no aparecen en ninguna parte: **ni en las fichas de los tres campamentos,
ni en la [página de actividades](https://www.nwr.com.na/activities/) de NWR** —que solo dice que
podrás hacer *«an early, afternoon or late evening Game Drive»*, sin una sola hora—, **ni en su
motor de reservas**, que exige registro. **No hay horario oficial que copiar, así que no se
inventa.**

**Lo que sí se puede deducir**, porque los guiados van atados al sol igual que las puertas ○:

- **El de mañana** sale con la apertura o poco antes → hacia las **06:00–06:15** en vuestros días
- **El de tarde** sale a media tarde y aprovecha la última luz → vuelta hacia el **cierre, ~19:10**
- **El nocturno** empieza **cuando ya es de noche**, después de cenar → **a partir de ~19:30–20:00**

👉 **Confírmalos en recepción el día que llegues** y apunta la hora: es lo que decide si el D9 lo
dedicas a la charca o al vehículo. 📞 Okaukuejo **+264 67 229 800** · reservas centrales NWR
**+264 61 285 7200**.

*Nota sobre «las empresas que operan»: durmiendo **dentro**, tu operador es **NWR** y punto. Los
lodges privados de las puertas (Ongava, Onguma, Etosha Safari Lodge, Mokuti) hacen sus propios
game drives, pero **son para sus huéspedes** y están sujetos a las mismas horas de puerta — no
puedes contratarles una salida desde el camping.*

Y fuera de Etosha, ya en el dossier: **lanzadera de Deadvlei N$180 (~€9)** ✅, safari guiado de
mañana en Sesriem N$600–700, Elim Dune N$300, cañón N$200 *(ver `03`)*.

#### 🌙 El nocturno: el único que compra algo imposible por libre

**De día, pagar N$650/persona no tiene mucho sentido en vuestro caso**: ya tenéis 4x4, trece horas
de puerta a puerta y libertad para quedaros en una charca el rato que queráis. Lo que compra el
guiado de día son **los ojos del guía** y un vehículo alto y abierto — legítimo, pero no cambia el
viaje.

**El nocturno sí**: de noche está prohibido circular por libre, así que es **la única forma de estar
en el parque a oscuras** y ver lo que solo sale entonces — oricteropo, puercoespín, liebre saltadora,
leones cazando. **N$1.500 (~€75) los dos.**

> ### 👉 Hazlo desde NAMUTONI, no desde Okaukuejo
> Suena raro, pero sale de cruzar dos datos verificados: **la charca iluminada de Okaukuejo es
> probablemente el mejor sitio de África para ver rinoceronte negro de noche**, y la de **Halali es
> famosa por el leopardo y el puercoespín** — las dos son **gratis y sin coche, andando desde la
> parcela**. En cambio la de **Namutoni (King Nehale) es la más floja de las tres**: «se ven animales
> ocasionalmente».
>
> **Conclusión: gasta el nocturno la noche en que menos pierdes** — el **D11 o el D12, en
> Namutoni** —, y deja intactas las noches de Okaukuejo (D9) y Halali (D10) para sentarte en sus
> charcas, que es gratis y de las mejores cosas del viaje.

> ⚠️ **Dos cosas que preguntar al reservar:** los **horarios de salida** (no están publicados) y si
> el nocturno **se puede dejar cerrado desde España** — la tarifa de NWR avisa de que *«no se
> aceptan reservas anticipadas de actividades en temporada de lluvias»*, y vuestra quincena es el
> hombro justo antes. 📞 Okaukuejo **+264 67 229 800**.
>
> 💶 **Y ojo al presupuesto:** el nocturno **se come entero** el margen de actividades (~€38 p.p. en
> `02`). Con la lanzadera de Deadvlei son **~€47 p.p.**: cuenta ~€10 más por cabeza.
- **Sossusvlei → tu 4x4 hasta el final** *(estado a 16/07: self-drive permitido — reconfirma en
  octubre, ver `06`)*. Los últimos ~5 km de arena son 4H de verdad; si no te apetece la arena, la
  **lanzadera del concesionario (N$180 · ~€9/persona)** ✅ hace exactamente ese tramo. Big Daddy y
  Deadvlei son a pie de todas formas.
- **Sandwich Harbour → SOLO tour guiado.** Con tu coche está vetado por contrato (referencia Asco;
  asume lo mismo en Namibia2Go hasta leer el tuyo, `06`) — y el tour es mejor plan de todas formas.
  Precio ❌ sin verificar: pregúntalo en Walvis Bay.
- **Skeleton Coast → tu 4x4** con permiso de la puerta (tránsito gratis ◐; pernocta = reserva de
  Terrace Bay). El **sector norte** del parque es solo por concesión aérea/guiada — no aplica a
  esta ruta.
- **Cape Cross → tu 4x4** hasta el aparcamiento y pasarelas a pie.

**¿Y las reservas PRIVADAS — valen la pena frente a Etosha?** Con precios verificados, el
veredicto es fácil para este viaje:

- **Ongava** (puerta de Andersson) — **~N$17.300 (~€865)/persona/noche** ◐ pensión completa.
  **Una sola noche para dos ≈ N$34.600 — el TRIPLE de lo que cuestan las 13 noches de camping
  de todo el viaje (~N$11.400).** Es otro producto (lodge de lujo con game drives), no un upgrade.
- **Okonjima/AfriCat** (eje Windhoek–Etosha) — desde **~N$12.700 (~€630)/persona/noche** ◐. Su
  argumento real son los **leopardos habituados** — lo único que Etosha casi nunca da. Si algún
  día cae un capricho, es este, como **parada del D13**; como sustituto de Etosha, no.
- **Onguma** (puerta este) — precio ❌ sin verificar, «puede ser gama alta». Lo que pierdes seguro:
  dormir DENTRO y las charcas iluminadas.

> 👉 **Veredicto:** a **N$460/persona el camping dentro** ✅ + **N$750 el safari nocturno** ✅,
> Etosha por libre da más horas de safari por menos dinero que cualquier privado. Los privados son
> un capricho legítimo (Okonjima por los leopardos), **no una mejora del plan**.

### 🔍 En qué se diferencia del blog *(y por qué)*
- **Ellos, 2 noches en Spreetshoogte; nosotros, 1** — la segunda se va a Etosha, que con tu ventana
  seca merece 4 noches
- **Ellos duermen en Onguma (fuera); nosotros las 4 noches DENTRO del parque** (Okaukuejo, Halali,
  Namutoni ×2 — verificado, N$920/noche) — dormir dentro es lo que da las charcas nocturnas
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

- ✅ **Vuelos** — ya hay presupuesto real: €1.366 (~N$27.300) p.p., 31 oct – 14 nov. *Pendiente
  solo de emitir el billete*
- ❌ **Tres noches sin precio** — Terrace Bay, Spreetshoogte *(candidato: Camp Gecko, banda
  contradictoria)* y Walvis Bay ×2, más el hotel del D13. **Hoada ya tiene precio** ◐ (arriba), y
  los lodges privados siguen sin rack/noche (Gondwana y las webs propias, en 403). ⛺ También
  cerrado el **camping de Spitzkoppe: N$270/persona → N$540/noche (~€27), entrada incluida** ◐
  *(fuera de la ruta E)*
- ◐ **Km del D7 y del D13 ya cerrados (03/08)** — la costa **Walvis Bay → Terrace Bay ≈ ~380 km**
  (C34 300 km Swakopmund→Torra Bay + 50 a Terrace Bay + 30 de Walvis, fuentes convergentes) y el
  **Namutoni → Windhoek ≈ ~555–575 km** (web de Etosha NP y rome2rio). Detalle y fuentes en `13`.
- ⚠️ **Sigue sin verificar el D8** — la salida de la costa hacia Twyfelfontein (Terrace Bay →
  interior por la C39) no se pudo cerrar con fuente (`13`)
- 🚧 **Las obras de Etosha** — confirmar con NWR al reservar *(afectan al D10 de la E,
  Okaukuejo → Halali)*
- 🕳️ *Residuos del sur (conflicto Keetmanshoop → Hobas, lodges del cañón): **sin efecto en la E***
