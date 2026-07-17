# Los itinerarios, día a día

> ## 🔄 ACTUALIZACIÓN 17/07/2026 — dos decisiones del viajero cambian la ruta
>
> 1. **Fechas: primera quincena de noviembre**, pudiéndose adelantar algunos días a finales de
>    octubre. El "salir tras el 15 nov" ya no aplica: el coche irá en banda alta (€179/día).
> 2. **Sossusvlei Y Etosha van los dos en el mismo viaje.** Eso invalida la A (sin Etosha) y la B
>    (sin Sossusvlei) como recomendación, y obliga a recortar el sur.
>
> **La ruta pasa a ser la VARIANTE D**, desarrollada aquí abajo. A y B quedan como referencia.

---

<div align="center">

## ❓ ¿Qué se puede quitar del sur? — la tijera, ordenada

</div>

Con Sossusvlei y Etosha fijos, el sur es lo que compite por los días. Esto es lo que cuesta y lo que
vale cada pieza:

```mermaid
flowchart TD
    S["EL SUR<br/>~4,5-5 dias completo"] --> A1["✂️ 1º · AI-AIS<br/>ahorra ~medio dia<br/>pierdes poco"]
    S --> A2["✂️ 2º · LUDERITZ + KOLMANSKOP<br/>ahorra ~2 dias<br/>LA tijera que hace caber todo"]
    S --> A3["🚫 NO CORTAR · miradores del canon<br/>+ kokerbooms + Garub + D707<br/>cuestan ~2,5 dias y son el alma del sur"]
    A1 --> R["Con 1º y 2º cortados:<br/>Sossusvlei + Etosha + canon<br/>CABEN en 14 dias"]
    A2 --> R
    style A1 fill:#2d6a4f,color:#fff
    style A2 fill:#e85d04,color:#000
    style A3 fill:#9d0208,color:#fff
    style R fill:#2d6a4f,color:#fff
```

**✂️ Primera tijera — Ai-Ais** *(ahorra ~½ día, pierdes casi nada)*
Son las fuentes termales del **fondo** del cañón: 68 km de grava bacheada por trayecto, hace más
calor que en el borde (está cientos de metros más abajo), y el sendero está cerrado en noviembre de
todas formas. **Los miradores —que son el espectáculo— están arriba, en Hobas.**

**✂️ Segunda tijera — Lüderitz y Kolmanskop** *(ahorra ~2 días; es la que decide)*
Lüderitz es un **fondo de saco**: 334 km al oeste por la B4 que hay que deshacer o pagar con la
etapa más dura del viaje. Kolmanskop merece un día entero para hacerlo bien (el permiso de fotógrafo
es de amanecer a atardecer). Juntos cuestan **~2 días** que son exactamente los que necesita Etosha.
*(Elizabeth Bay cae sola con ellos — era un capricho de N$3.630/persona con permiso a 10 días.)*
**Es la pérdida dolorosa**: la ciudad fantasma es única. Pero es la única tijera que cierra el
círculo.

**🚫 Lo que NO hay que cortar** *(porque cuesta poco y es el alma del sur)*
- **Los miradores del Fish River** — el motivo del sur, ~2,5 días desde el eje
- **El bosque de kokerbooms** — 14 km de Keetmanshoop, sale gratis
- **Los caballos de Garub** — pequeño desvío desde Aus, de camino
- **La D707** — no es desvío, ES la carretera hacia Sesriem

> ### El resultado: la Variante D
> **Sossusvlei + Etosha + el cañón + la D707 + Garub + kokerbooms, en 14 días.**
> Lo único que se queda fuera del sur: Ai-Ais y Lüderitz/Kolmanskop.

---

Desarrollo completo de las variantes. **Ventana real: primera quincena de noviembre de 2026.**

**~N$20 = €1** · **✅ verificado** · **◐ secundario** · **○ estimación propia**

> **Reglas aplicadas en todos:** grava a **80 km/h como techo** (media real 60–70) · asfalto ~105 ·
> **60 km/h en parques** · **llegar a las 18:00** (anochece ~19:15) · **nunca de noche**.
> Ver `04` y `05`.

---

<div align="center">

## ⭐ VARIANTE D — Las dos coronas y el cañón
### La ruta del viaje: Sossusvlei + Etosha + Fish River, sin Lüderitz

</div>

**~3.100 km · 13 días de coche · 4 días de conducción fuerte (2 de ellos en asfalto) · fechas
ilustrativas: llegada el domingo 1 de noviembre de 2026**

> ### 📅 Por qué el 1 de noviembre importa
> **NWR cambia a su tramo barato el 1 de noviembre.** Empezando ese día, **todas** las noches de
> NWR (Hobas, Sesriem, Etosha) van en tarifa baja.
>
> **¿Y si adelantáis días a octubre?** Hasta **2 días es gratis**: las primeras noches del plan
> (Windhoek, Keetmanshoop) **no son NWR**. A partir de ahí, cada noche NWR de octubre paga la
> tarifa vieja en su tramo caro (el chalet del charco costaría N$2.200 más, el camping N$200 más).
> 👉 **Si se adelanta, que octubre se lo lleve el sur — que además es su época fresca (~30 °C).**

```mermaid
gantt
    title Variante D · Sossusvlei + Etosha + canon · 1-14 nov 2026
    dateFormat YYYY-MM-DD
    axisFormat %d-%m
    section Llegada
    D1 Llegada Windhoek           :d1, 2026-11-01, 1d
    section Sur esencial
    D2 Windhoek-Keetmanshoop      :d2, after d1, 1d
    D3 Keetmanshoop-Hobas         :d3, after d2, 1d
    D4 Miradores-Garub-Tiras      :d4, after d3, 1d
    section Namib
    D5 D707-Sesriem               :d5, after d4, 1d
    D6 Sossusvlei amanecer        :d6, after d5, 1d
    D7 Sesriem-Swakopmund         :d7, after d6, 1d
    section Costa
    D8 Descanso costa             :d8, after d7, 1d
    D9 Swakopmund-Spitzkoppe      :d9, after d8, 1d
    section Safari
    D10 Spitzkoppe-Etosha         :d10, after d9, 1d
    D11 Safari Okaukuejo          :d11, after d10, 1d
    D12 Safari Halali-Namutoni    :d12, after d11, 1d
    section Vuelta
    D13 Namutoni-Windhoek         :d13, after d12, 1d
    D14 Vuelo                     :d14, after d13, 1d
```

### D1 · dom 1 nov — Llegada a Windhoek
- 4x4 + briefing (1–2 h): **presiones en frío apuntadas, las DOS ruedas de repuesto, gato y
  compresor a la vista** antes de salir del patio (`05`)
- Efectivo (~N$6.000–8.000), **SIM de MTC** con pasaporte *(el kiosco cierra ~21:00)*
- 🍺 **Joe's Beerhouse** · 🛏️ Windhoek — hoy no se conduce al sur

### D2 · lun 2 — Windhoek → Keetmanshoop · **500 km asfalto · 5h30–6h** ✅
- B1: sal al alba, come en Mariental. Fauna en los arcenes al atardecer: llega con luz
- 🌳 **Kokerbooms al atardecer** (14 km, M29) — y si el cielo acompaña, **astrofoto**
- 🛏️ Keetmanshoop / Quivertree Rest Camp ⚠️ *precio sin verificar*

### D3 · mar 3 — Keetmanshoop → Hobas · **150–160 km · 2h30** ✅
- 🛑 **Borde ESTE por la C12** *(el aviso "no tomes la C12" es para el Lodge del borde oeste; no hay
  puente entre bordes)* · **evita la D462** · valora la ruta por la presa de Naute
- ⛽ A tope en Keetmanshoop · 🎫 tasa ~N$620/24 h
- 🌇 **Hell's Bend al atardecer** (10 km de pista de borde, despacio)
- 🛏️ **Camping Hobas — N$960 (~€48)** ✅ *(tarifa baja: ya es noviembre)*

### D4 · mié 4 — Amanecer en el cañón → Garub → Tiras · **~300–330 km · ~4h30–5h** ◐
- 🌅 Amanecer en los miradores (bloque de 2–3 h) — *Ai-Ais se queda fuera: fondo del cañón, más
  calor, sendero cerrado. Media jornada ahorrada que se va al safari*
- Salida por C12/B4 hacia el oeste → 🐎 **desvío corto a Garub: los caballos salvajes** → Aus →
  C13 norte hacia Helmeringhausen
- 🛏️ Zona **Tiras / Namtib** ⚠️ *precio sin verificar*

### D5 · jue 5 — La D707 → Sesriem · **~240 km grava · ~4h** ◐
- 🏆 **La D707 entera**, dunas a un lado y las Tiras al otro — con calma, es de las joyas del viaje
- ✅ *Recuerda: la D707 NO es la D3707 — esta está cubierta por el seguro como cualquier grava*
- 🎫 Namib-Naukluft ~N$620/24 h
- 🛏️ **🔑 DENTRO de la puerta: Sesriem Campsite — N$1.340 (~€67)** ✅ *(44 parcelas: reservar YA)*

### D6 · vie 6 — Sossusvlei y Deadvlei · **130 km · día completo** ✅
- 🌅 **Puerta interior 1 h antes del amanecer** — Deadvlei casi en solitario
- Duna 45 de camino · últimos 5 km de arena: 4H antes de entrar, desinflar en el 2WD, reinflar en
  Sesriem *(o lanzadera N$180/persona)*
- Tarde: Sesriem Canyon · 🛏️ Sesriem, segunda noche

### D7 · sáb 7 — Sesriem → Swakopmund · **345 km · 91 % grava · ~7h** ✅
- **El día grande de grava**: sal al alba. C14, pasos de Gaub y Kuiseb, Trópico de Capricornio
- ⛽ **Solitaire obligatorio** *(y la tarta)* — después, **210 km sin nada**
- 🛏️ Swakopmund ⚠️ *precio sin verificar*

### D8 · dom 8 — Costa: el día de descanso ✅
- 🦩 Flamencos y pelícanos en Walvis Bay (30 km de asfalto) · ostras, café, ciudad alemana
- 🚫 Sandwich Harbour **solo en tour guiado** (el contrato lo prohíbe con tu coche — y el tour es
  mejor plan) · 🛏️ Swakopmund

### D9 · lun 9 — Swakopmund → Spitzkoppe · **140–150 km · ~1h45** ◐
- Día corto a propósito: tarde de arcos de granito y **noche de estrellas**
- 🛏️ Spitzkoppe Community Campsite ⚠️ *precio sin verificar*

### D10 · mar 10 — Spitzkoppe → Etosha (Okaukuejo) · **~430–450 km · ~5h** ○
- Ruta rápida por Usakos–Otjiwarongo–Outjo (mayoría asfalto) → puerta de **Andersson**
- *Alternativa con Damaraland: parar en **Twyfelfontein** (grabados UNESCO) y dormir allí, pasando a
  Etosha el D11 — a cambio de un día menos de safari. Elegir según fauna vs arte rupestre*
- 🎫 Etosha ~N$620/24 h × 3 días · trámite de puerta 20–30 min
- 🌙 **Noche en la charca iluminada de Okaukuejo** — rinocerontes
- 🛏️ **Camping Okaukuejo — N$920 (~€46)** ✅ · *capricho: chalet del charco N$4.760 (~€238)*

### D11 · mié 11 — Safari zona Okaukuejo ✅
- Día entero de charcas alrededor de Okaukuejo, a 60 km/h y parando
- Primera quincena de noviembre = **parque seco casi seguro** (4 de 5 temporadas) = fauna
  concentrada en las charcas · 🛏️ Okaukuejo

### D12 · jue 12 — Safari Okaukuejo → Halali → Namutoni · **~140 km de safari** ✅
- 🚧 **Obras 2026**: el tramo a Halali va por desvíos (~90 km lentos, ~3 h) — confirmar con NWR
- Charcas Goas, Nuamses, Springbokfontein, Batia, Chudop
- 🛏️ **Camping Namutoni — N$920 (~€46)** ✅ *(o Halali si el desvío come el día)*

### D13 · vie 13 — Namutoni → Windhoek · **~550 km asfalto · ~5h30–6h** ○
- Salida por **Von Lindequist** (14 km, la puerta rápida del este)
- 🥩 **Línea Roja**: la carne cruda no baja del norte — el braai se come en Etosha
- 🛏️ Windhoek — entrega del coche hoy o mañana temprano

### D14 · sáb 14 — Vuelo
- 💱 **Gasta o cambia los N$ antes de embarcar**: fuera de Namibia no valen nada

### 💰 Coste orientativo de D *(ventana 1–15 nov: coche en banda alta)*
- **Alquiler 13 días + Super Cover: €2.652 (~N$53.040)** ✅ *(€179+€25/día · la banda baja de €117
  no es accesible con vuestras fechas — la flexibilidad tras el 15 nov habría valido ~€806)*
- **Camping NWR verificado**: Hobas 960 + Sesriem 2×1.340 + Etosha 3×920 = **N$6.400 (~€320)** ✅
- **Tasas de parque**: cañón 1–2 + Namib 2 + Etosha 3 unidades ≈ **N$3.700–4.300 (~€185–215)** ◐
- **Combustible ~3.100 km**: ~370–400 l ≈ **N$9.500–10.500 (~€475–525)** ○
- **Visado**: N$3.200 (~€160) los dos ✅
- **Total tierra en camping ≈ €4.400 (~N$88.000)** la pareja ○ *(recalculado desde `10` con el
  coche en banda alta; hereda sus partidas estimadas)*

---

<div align="center">

## 🟢 VARIANTE A — Sur + Namib + costa · SIN Etosha
### Referencia (superada por la decisión de incluir Etosha)

</div>

**~2.400 km · 12 días de coche · ningún día pasa de ~300 km de grava**

```mermaid
gantt
    title Variante A · la que deja respirar
    dateFormat YYYY-MM-DD
    axisFormat %d-%m
    section Llegada
    D1 Llegada Windhoek           :a1, 2026-11-20, 1d
    section Sur
    D2 Windhoek-Keetmanshoop      :a2, after a1, 1d
    D3 Keetmanshoop-Hobas         :a3, after a2, 1d
    D4 Miradores + Ai-Ais         :a4, after a3, 1d
    D5 Hobas-Luderitz             :a5, after a4, 1d
    D6 Kolmanskop y Luderitz      :a6, after a5, 1d
    section Namib
    D7 Luderitz-Tiras por D707    :a7, after a6, 1d
    D8 Tiras-Sesriem              :a8, after a7, 1d
    D9 Sossusvlei amanecer        :a9, after a8, 1d
    section Costa
    D10 Sesriem-Swakopmund        :a10, after a9, 1d
    D11 Swakopmund descanso       :a11, after a10, 1d
    D12 Swakopmund-Spitzkoppe     :a12, after a11, 1d
    D13 Spitzkoppe-Windhoek       :a13, after a12, 1d
    section Salida
    D14 Vuelo                     :a14, after a13, 1d
```

### D1 · vie 20 — Llegada a Windhoek
- Aterrizas, recoges el 4x4. **Briefing 1–2 h**: que te enseñen **físicamente** gato, llave, **las
  dos ruedas de repuesto**, compresor y herramientas (`05`).
- **Pide la presión en frío para TU vehículo cargado y apúntala.** No la de un foro.
- Saca **efectivo** (~N$6.000–8.000) y compra la **SIM de MTC** *(el kiosco del aeropuerto cierra
  ~21:00)*. Registro obligatorio **con pasaporte** (`07`).
- 🍺 **Joe's Beerhouse** — tu pin. N$200–400 (~€10–20).
- 🛏️ **Windhoek.** ⚠️ **No salgas hoy hacia el sur**: 500 km + briefing = llegas de noche.

### D2 · sáb 21 — Windhoek → Keetmanshoop · **500 km asfalto · 5h30–6h** ✅
- B1 todo el camino. Combustible en Rehoboth, Kalkrand, **Mariental** (come aquí).
- ⚠️ **Ganado y kudú sueltos en los arcenes de la B1 al atardecer** — sal temprano.
- 🌅 **Bosque de kokerbooms al atardecer** — 14 km por la M29, grava buena, 12–15 min. **La luz de
  mediodía lo mata; la del atardecer es el motivo de ir.** ~250 ejemplares.
- 🛏️ **Quivertree Forest Rest Camp** ⚠️ *precio sin verificar*

### D3 · dom 22 — Keetmanshoop → Hobas · **150–160 km · 2h20–2h30** ✅
- B4 (~40 km asfalto) → **C12** (~80 grava) → C37/D601 (~30 grava).
- 🛑 **Vas al borde ESTE.** El aviso de *"no tomes la C12"* que circula es para el **Lodge del borde
  oeste**. **No hay puente entre los dos bordes.** Para Hobas y los miradores: **C12 es correcta**.
- 🛑 **Evita la D462** (lechos de arena profunda). Valora ir por la **presa de Naute** en vez del
  desvío de Seeheim, que puede cortarse con lluvia — y **finales de noviembre ya es inicio de lluvias
  en el sur**.
- ⛽ **Reposta a tope en Keetmanshoop**: en Hobas no hay gasolinera fiable.
- 🎫 **Tasa de parque Ai-Ais/Fish River: ~N$620 (~€31)** la pareja + coche, **por cada 24 h**.
- 🛏️ **Camping Hobas — N$480/persona → N$960 (~€48)** ✅

### D4 · lun 23 — Miradores + Ai-Ais · **~150 km · día de media jornada de coche** ✅
- 🌅 **Amanecer en el Main Viewpoint (Hell's Bend)** — 10 km de Hobas, pista de borde mala
  (*"a horrible dirt road"*), 15–20 min a 40–50 reales.
- Bloque de miradores: **3–4 h**. El cañón: 160 km de largo, 27 de ancho, 550 m de profundidad.
- Tarde: **Ai-Ais** — 68 km, grava bacheada (D324+C10), **1h10–1h20**, con descenso al final.
  ⚠️ **Ai-Ais está en el fondo del cañón: es sistemáticamente más caluroso que el borde** (`08`).
- ❌ **El sendero está CERRADO** (temporada may–sep, y exige mínimo 3 personas). Hoy es mirador.
- 🛏️ **Hobas** o **Ai-Ais** ⚠️ *precio Ai-Ais sin verificar*

### D5 · mar 24 — Hobas → Lüderitz · **410–430 km · 5h45–6h15** ✅
- ~120 km de grava saliendo (D601/C37+C12) + **~293 km de asfalto B4** vía Goageb y Aus.
- 🐎 **Parada obligada: los caballos salvajes del Namib en Garub**, cerca de Aus.
- ⛽ Reposta en **Goageb o Aus**.
- ⚠️ Viento lateral fuerte cerca de la costa.
- 🛏️ **Lüderitz** ⚠️ *Nest Hotel sin precio verificado*

### D6 · mié 25 — Kolmanskop y Lüderitz · **~20 km** ✅
- 🌅 **Kolmanskop con permiso de fotógrafo: N$480/persona (~€24)** → **de amanecer a atardecer**.
  El ticket normal (N$230, ~€11,50) **te encierra en la franja del tour = luz dura de mediodía**,
  justo la que no quieres para las habitaciones llenas de arena.
  ⚠️ **Cómpralo la víspera en Lüderitz** (Desert Deli, esquina Bahnhof/Moltke): una fuente dice que
  no se vende en la puerta el mismo día.
  Horarios: L–V 08:00–15:00 · S/D/festivos 08:00–13:00.
- 10 km de asfalto (B4). Día tranquilo — **el único de descanso del sur**.
- ❌ **Elizabeth Bay**: son **N$3.630/persona (~€181)** con mínimo 4 y **permiso policial 6–10 días
  antes con copia de pasaporte**. **16 veces el precio de Kolmanskop.** Si lo quieres, **se cierra
  desde España**, no se improvisa.
- 🛏️ **Lüderitz**

### D7 · jue 26 — Lüderitz → Tiras/Namtib por la D707 · **~250 km** ◐
- B4 hasta Aus (125 km asfalto) → C13 sur → **D707**.
- 🏆 **La D707: 123 km de grava**, considerada **la carretera más bonita de Namibia**. Dunas del
  Namib a un lado, montañas Tiras al otro.
- ⚠️ **Es grava exigente**: arena blanda, corrugado, piedras. **4x4 obligatorio.**
- ✅ **NO la confundas con la D3707**: la que anula tu seguro de bajos y rescate es la **D3707/D3703
  en Kaokoland/Damaraland** (`05`), **no** la D707.
- **Partir aquí es lo que salva la variante A**: convierte la etapa asesina de 8 h en dos de ~4 h.
- 🛏️ **Zona Tiras / Namtib** ⚠️ *precio sin verificar*

### D8 · vie 27 — Tiras → Sesriem · **~240 km grava** ◐
- Resto de la D707 → C27 norte → Sesriem.
- ⛽ **Reposta donde puedas**: este tramo es de los vacíos.
- 🎫 **Tasa Namib-Naukluft: ~N$620 (~€31)** la pareja + coche.
- 🛏️ **🔑 DUERME DENTRO DE LA PUERTA — Sesriem Campsite, N$670/persona → N$1.340 (~€67)** ✅
  > **Es la única forma de ver el amanecer en Deadvlei.** La puerta interior abre **1 h antes del
  > amanecer solo si duermes dentro**; la exterior abre **al amanecer**, y son **60 km + arena** hasta
  > allí. Dormir fuera = **no llegas** (`05`).
  > ⚠️ **Solo 44 parcelas + 6 de desbordamiento.** Reserva **ya**.

### D9 · sáb 28 — Sossusvlei y Deadvlei · **130 km · día completo 6–8 h** ✅
- 🌅 **Sal con la puerta interior, 1 h antes del amanecer.**
- 60 km de asfalto **de parque: límite 60 km/h**, con órix, avestruces y springbok.
- **Duna 45** de camino *(Google la lista como "cerrada permanentemente": es un fallo del listado)*.
- Últimos **~5 km de arena blanda**: **4H ANTES de entrar**, desinfla **en el aparcamiento 2WD, no
  antes**, métete en las roderas, no pares en subida. **Reinfla en Sesriem** (`05`).
  O usa la **lanzadera de NWR: N$180/persona (~€9)**.
- Tarde: **Sesriem Canyon** (está en la entrada, incluido).
- 🛏️ **Sesriem** *(segunda noche)*

### D10 · dom 29 — Sesriem → Swakopmund · **345 km · 🔴 91 % grava · 6h50–7h** ✅
- **La etapa más grava del viaje.** C19/D826 → **C14**: pasos de **Gaub** y **Kuiseb**, Trópico de
  Capricornio, Walvis Bay.
- ⛽ **REPOSTA EN SOLITAIRE, SÍ O SÍ** (83 km, 1h15). **Después son 210 km sin NADA** hasta Walvis
  Bay (`07`). *(Y la tarta de manzana.)*
- ⚠️ **Solitaire → Kuiseb (~90 km) es el tramo malo**: media real ~55 km/h.
- **Sal al alba.** Es el día más largo de A.
- 🛏️ **Swakopmund** ⚠️ *precio sin verificar*

### D11 · lun 30 — Swakopmund y Walvis Bay · **~70 km** ✅
- **El día de descanso.** Swakopmund → Walvis Bay son 30–35 km de asfalto, 30–35 min.
- **Pelícanos y flamencos** en la laguna de Walvis Bay.
- 🚫 **Sandwich Harbour: prohibido por contrato** (*"strictly prohibited"*, anula la cobertura
  entera). **Si lo quieres, tour guiado** — no con tu coche.
- Ciudad alemana, café, ostras. **Aprovecha: es el único respiro real.**
- 🛏️ **Swakopmund**

### D12 · mar 1 dic — Swakopmund → Spitzkoppe · **140–150 km · ~1h45** ◐
- B2 asfalto hasta el desvío + ~29 km de grava.
- 🏔️ **El "Matterhorn de Namibia"**. Granito, arcos, pinturas rupestres.
- 🌌 **Cielo oscuro espectacular** — es de los mejores sitios del viaje para estrellas.
- Día corto: **llegas con luz de sobra para la tarde de fotos**.
- 🛏️ **Spitzkoppe Community Campsite** ⚠️ *precio sin verificar*

### D13 · mié 2 dic — Spitzkoppe → Windhoek · **~280 km asfalto** ◐
- Vuelta cómoda por Usakos y Karibib.
- 🛏️ **Windhoek** — última noche, entrega el coche mañana o esta tarde.

### D14 · jue 3 dic — Vuelo
- ⚠️ **Gasta o cambia los N$ ANTES de volar**: el **NAD no vale nada fuera de Namibia** (`07`).

### 💰 Coste orientativo de A
- **Alquiler 13 días + Super Cover: ~€1.846 (~N$36.920)** ✅
- **Tasas de parque**: Fish River (2 días) + Namib-Naukluft (2 días) ≈ **N$2.480 (~€124)** ◐
- **Camping NWR verificado**: Hobas N$960 + Sesriem N$1.340×2 = **N$3.640 (~€182)** ✅
- **Kolmanskop foto**: N$960 la pareja (~€48) ✅
- **Combustible ~2.400 km**: ~280 l × ~N$26 ≈ **N$7.280 (~€364)** ○
- **Visado**: N$3.200 (~€160) ✅
- **Resto** (noches sin verificar, comida, actividades) → ver `10-presupuesto.md`

---

<div align="center">

## 🟠 VARIANTE B — Sur + Etosha · SIN Sossusvlei
### Referencia (superada: Sossusvlei va sí o sí)

</div>

**~3.000 km · dos traslados de asfalto de 550–570 km**

```mermaid
gantt
    title Variante B · la fauna por encima de las dunas
    dateFormat YYYY-MM-DD
    axisFormat %d-%m
    section Llegada
    D1 Llegada Windhoek           :b1, 2026-11-20, 1d
    section Sur
    D2 Windhoek-Keetmanshoop      :b2, after b1, 1d
    D3 Keetmanshoop-Hobas         :b3, after b2, 1d
    D4 Miradores Fish River       :b4, after b3, 1d
    D5 Hobas-Luderitz             :b5, after b4, 1d
    D6 Kolmanskop y Luderitz      :b6, after b5, 1d
    section Subida
    D7 Luderitz-Mariental 570 asf :b7, after b6, 1d
    D8 Mariental-Otjiwarongo 520  :b8, after b7, 1d
    section Etosha
    D9 Otjiwarongo-Okaukuejo      :b9, after b8, 1d
    D10 Safari Okaukuejo-Halali   :b10, after b9, 1d
    D11 Safari Halali-Namutoni    :b11, after b10, 1d
    section Vuelta
    D12 Namutoni-Okonjima         :b12, after b11, 1d
    D13 Okonjima-Windhoek         :b13, after b12, 1d
    section Salida
    D14 Vuelo                     :b14, after b13, 1d
```

**D1–D6: idénticos a la variante A.**

### D7 · jue 26 — Lüderitz → Mariental · **~570 km asfalto** ○
- B4 hasta Keetmanshoop (334 km ✅) → B1 norte hasta Mariental (~230 km ✅).
- **Todo asfalto**: largo pero **seguro**. Sal al alba.
- 🛏️ **Bagatelle Kalahari Game Ranch** — tu pin, zona de Mariental ⚠️ *precio sin verificar*.
  Dunas rojas del Kalahari: **compensa parte de lo que pierdes en Sossusvlei**.

### D8 · vie 27 — Mariental → Otjiwarongo · **~520 km asfalto** ○
- B1 por Windhoek. **Todo asfalto.**
- 🐆 **Okonjima / AfriCat** está en este eje ⚠️ *precio sin verificar* — leopardos y guepardos.
- 🛏️ **Otjiwarongo** *(o Okonjima si el precio encaja)*

### D9 · sáb 28 — Otjiwarongo → Okaukuejo · **~195 km** ✅
- Otjiwarongo → Outjo 75 km → puerta de **Andersson** 120 km → **Okaukuejo 17–18 km**.
- ⏱️ **Trámite de puerta y pago: 20–30 min.**
- 🎫 **Tasa Etosha: ~N$620 (~€31)** la pareja + coche, **por cada 24 h** — **3 días = 3 veces**.
- 🌅 Tarde: **charca iluminada de Okaukuejo** — la famosa. **Rinocerontes**.
- 🛏️ **Camping Okaukuejo — N$460/persona → N$920 (~€46)** ✅
  *(o chalet del charco N$4.760 (~€238) — el mejor sitio del parque para ver rinoceronte de noche)*

### D10 · dom 29 — Safari Okaukuejo → Halali · **70 km nominales… 🚧 ~90 km reales** ✅
- 🚧 **OBRAS 2026**: el tramo va por **pistas de desvío de ~90 km a 30–35 km/h** con maquinaria
  pesada. **Lo que serían 1h45 se convierte en ~3 h.** ⚠️ **Confírmalo con NWR al reservar.**
- Charcas del camino. **Límite 60 km/h** y vas parando.
- 🛏️ **Camping Halali — N$920 (~€46)** ✅ *(o doble N$2.800 / ~€140 — la más barata del parque)*

### D11 · lun 30 — Safari Halali → Namutoni · **70 km · 1h45+** ✅
- Charcas **Goas, Nuamses, Springbokfontein, Batia, Chudop** — *son el motivo de la etapa*.
- 🛏️ **Camping Namutoni — N$920 (~€46)** ✅ *(o doble N$3.680 / ~€184)*

### D12 · mar 1 dic — Namutoni → Okonjima/Otjiwarongo · **~350 km** ○
- Salida por **Von Lindequist** (14 km, ~30 min — la más rápida hacia el este).
- 🥩 **LÍNEA ROJA**: **no bajes carne cruda** al salir de Etosha hacia el sur. Cómela o cocínala
  antes. **Saltarse un control veterinario es delito** (`07`).
- 🛏️ **Okonjima** o **Waterberg** ⚠️ *precios sin verificar*

### D13 · mié 2 dic — → Windhoek · **~250 km asfalto**
### D14 · jue 3 dic — Vuelo

### ⚠️ Lo que pierdes con B
**Sossusvlei y Deadvlei** — para mucha gente, **el motivo entero de venir a Namibia**. También
Swakopmund, la costa y todo el Damaraland.

> 👉 **Pregúntatelo en serio antes de elegir B.** Y ojo al dato de `08`: **en Etosha, noviembre
> (37,1 °C) es algo más fresco que octubre (38,0)** — vas en buen momento para el norte.

---

<div align="center">

## 🔴 VARIANTE C — Todo comprimido
### Aquí por honestidad, no como recomendación

</div>

```mermaid
flowchart LR
    C1["~3.900-4.100 km reales"] --> C2["~11 dias solo moviendo<br/>+ 4-5 dias para ver<br/>= 16-18 dias"]
    C2 --> C3["Tienes 12-13 de coche:<br/>320-360 km TODOS los dias<br/>sin un solo descanso"]
    C3 --> C4["Etosha reducido a cruzarlo<br/>Sossusvlei a un amanecer con prisa"]
    C4 --> C5["FATIGA = el ingrediente<br/>del vuelco en grava"]
    style C5 fill:#9d0208,color:#fff
```

**No la desarrollo día a día a propósito.** La aritmética ya la mata:

- **~3.200 km de puro tránsito** + vueltas en parques = **~3.900–4.100 km reales**
- A un techo sano de **~300 km/día**: **~11 días solo moviéndose**
- Más **4–5 días quietos** para *ver* (amanecer en Deadvlei, Kolmanskop, 2 días de safari, miradores)
- **Total mínimo realista: ~16 días.** Tienes **14**, con **12–13 útiles de coche**.

La guía de operadores dice *«no further than 400 km per day»* y, mejor, *«aim to drive no more than
4 to 6 hours per day»*. **C vive pegada al techo todos los días.**

> **El coste real no es el dinero: es la fatiga.** Y en grava, la fatiga es el ingrediente del
> vuelco — que es el **37 % de los muertos de Namibia con el 4,6 % de los accidentes**, concentrado
> justo en Hardap y !Karas, que son **tus** regiones (`05`).
>
> ❌ **Si quieres las dos coronas, la respuesta honesta no es apretar C: es alargar a 17–18 días.**

---

<div align="center">

## 🧭 Cómo se eligió

</div>

Con las dos decisiones del viajero —**primera quincena de noviembre** y **Sossusvlei + Etosha
juntos**— la elección quedó hecha: **Variante D**. A y B se conservan arriba como referencia de lo
que costaría cada renuncia, y C sigue documentada como el porqué de que no quepa todo.

```mermaid
flowchart TD
    D1{"Decisiones del viajero"}
    D1 -->|"Sossusvlei + Etosha juntos"| D2["Ni A ni B valen"]
    D2 --> D3["¿Que cede? El sur se recorta:<br/>fuera Ai-Ais y Luderitz/Kolmanskop<br/>se quedan canon, D707, Garub, kokerbooms"]
    D3 --> D["⭐ VARIANTE D<br/>~3.100 km · 13 dias de coche"]
    style D fill:#2d6a4f,color:#fff
```

<div align="center">

## 🕳️ Lo que falta para cerrar cualquiera de los tres

- ❌ **Vuelos** para tus fechas — sin tarifa verificada tras varios intentos
- ❌ **Lodges privados** por noche — sin precios (Gondwana bloqueó el acceso)
- ⚠️ **Seis etapas** con km sin verificar (`04`)
- 🚧 **Las obras de Etosha** — confirmar con NWR *(solo afecta a B)*
- ⚠️ **Conflicto Keetmanshoop → Hobas**: 150–160 km vs ~275 derivados. **Sin resolver.**
