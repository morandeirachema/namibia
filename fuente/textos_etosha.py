# Lo especifico de Etosha: donde y cuando. Investigado el 03/08/2026 con fuentes.
# REGLA: si una especie no tiene informacion decente de Etosha, NO lleva linea.

INTRO_EXTRA = """
  <p><strong>El safari, en corto:</strong> dormís <strong>dentro</strong> las cuatro noches. Las
  puertas siguen al sol y cambian cada semana: para vuestras fechas, <strong>06:13–19:06</strong> del
  3 al 9 y <strong>06:10–19:10</strong> del 10 al 16 — <em>trece horas de parque al día</em>, casi dos
  más que en invierno. Dentro, <strong>60 km/h</strong> (20 en los campamentos) y
  <strong>solo se puede bajar del coche dentro de los campamentos</strong>.</p>
  <p><strong>La táctica que funciona no es conducir: es esperar.</strong> Elegid una charca, apagad
  el motor, bajad la voz y dadle tiempo — la fauna llega por turnos. En seca, <strong>mediodía es
  bueno para elefante</strong> y primera y última hora para león. De noche no se circula: la única
  forma es el <strong>safari nocturno guiado de NWR (N$750 ≈ €38 p.p.)</strong>, pero las
  <strong>tres charcas iluminadas</strong> se ven andando desde la parcela. Y de día, en esta
  ruta <strong>la salida de mañana se hace guiada desde cada campamento (N$650 ≈ €33 p.p.,
  decidido el 08/08)</strong>: los traslados entre campamentos van con el 4x4 propio.</p>
  <p>🚧 <strong>Aviso de obras — confirmado que os afecta:</strong> están asfaltando la pista
  Okaukuejo–Halali–Namutoni y la nota oficial del MEFT de 2026 fija un <strong>desvío OBLIGATORIO
  por la pista de Gemsbokvlakte del 2 de junio de 2026 a julio de 2027</strong> — vuestra ventana
  cae de lleno. Las charcas accesibles del tramo son <strong>Gemsbokvlakte, Sueda y
  Salvadora</strong> —el mejor borde de pan para guepardo y león—; <strong>Nebrownii y Kapupuhedi
  quedan fuera</strong> por la obra. Son ~108 km en vez de ~70. <strong>Reconfirmad con NWR al
  reservar</strong> (+264 67 229 800).</p>
"""

DONDE = {
  # --- MAMIFEROS ---
  "elefante": "**Olifantsbad, Kalkheuwel, Tsumcor y Homob** *(Nebrownii, su clásica, queda cerrada por las obras en vuestras fechas)*, y a **mediodía**, que es cuando llegan a bañarse. Los de aquí tienen los colmillos gastados de cavar buscando agua.",
  "rino-negro": "**Charca iluminada de Okaukuejo, de noche**: seguramente el mejor sitio de África para verlo. También en Halali. Etosha tiene la mayor población del mundo de la subespecie suroccidental.",
  "rino-blanco": "Se extinguió aquí y lo reintrodujeron en 1995: hoy es **apenas una docena**. Se cita de vez en cuando en Springbokfontein. ⚠️ **El 39 % de los partes que dice haberlo visto no cuadra** con una docena de animales en 22.000 km²: la mayor parte tiene que ser rinoceronte **negro** mal identificado. Mira el labio, no el color. No cuentes con verlo.",
  "leon": "**Okondeka** es la mejor (manada residente), y luego Chudop, Rietfontein y Ombika *(Nebrownii, cerrada por las obras en vuestras fechas)*. Primera y última hora. Ojo: **usan las pistas como caminos**.",
  "leopardo": "**Halali/Moringa y Goas son las dos mejores apuestas** del parque; también Ngobib, Kalkheuwel y Klein Namutoni. La charca iluminada de Halali es famosa por él.",
  "guepardo": "Llanura abierta del borde de la pan: **Salvadora, Sueda, Charitsaub, Batia y Okerfontein**. De día, que es cuando caza — su presa aquí es el springbok.",
  "jirafa": "En cualquier charca abierta y, de noche, en la iluminada de Okaukuejo. Batia y Kalkheuwel la tienen habitual.",
  "cebra-burchell": "Por todo el parque, en las llanuras del borde de la pan. **En noviembre siguen concentradas**: no vuelven al oeste hasta finales de diciembre.",
  "cebra-hartmann": "⚠️ **En esta ruta NO la veréis.** En Etosha vive solo en las lomas de dolomita del **extremo oeste** (Dolomite, Galton Gate), no en el eje Okaukuejo–Namutoni.",
  "orix": "Charcas abiertas: Olifantsbad, Kalkheuwel, King Nehale. Aguanta el calor mejor que nadie, así que se ve a horas en que el resto se esconde.",
  "springbok": "Por todas partes en llanura abierta, y en Okaukuejo llegan **en manada por la tarde**. Es la presa principal del guepardo.",
  "kudu": "Zonas arboladas y charcas con monte alrededor: Chudop, Rietfontein, Groot Okevi. Al anochecer, ojo en la carretera.",
  "eland": "Chudop es la charca donde se cita. Escaso y arisco: no es un avistamiento fácil.",
  "nu": "Grandes manadas mixtas con cebra en **Goas y Batia**.",
  "impala-cara-negra": "**Lo primero que se ve entrando por Von Lindequist.** Klein Namutoni, Chudop, Kalkheuwel, Goas y Olifantsbad — están donde las soltaron en los 70 y en 30 años se han movido 31 km.",
  "dikdik": "**El sitio fiable es el Dik-dik Drive**, el bucle nada más entrar por Von Lindequist *(~206 registros frente a 4 en Okaukuejo)*, y Klein Namutoni. Primera hora de la mañana y última de la tarde.",
  "hiena-manchada": "Charcas iluminadas, y al amanecer en King Nehale y Chudop *(Nebrownii, cerrada por obras)*. Es la hiena por defecto: ~340 en el sistema Etosha–Kunene.",
  "hiena-parda": "Está en el parque, pero **dala por improbable**: nocturna, solitaria y sin densidad publicada. Cruza desde Ongava a buscar comida. Que un 18 % de los partes diga haberla visto choca con eso: **orejas puntiagudas y melena** o es la manchada.",
  "chacal": "En todas las charcas, y merodeando los campamentos al anochecer a por las sobras.",
  "puercoespin": "**De noche, en la charca iluminada de Halali**: las guías del parque lo citan entre los visitantes habituales junto con el leopardo — GBIF, en cambio, apenas lo registra: es nocturno, como la liebre saltadora.",
  "hartebeest": "Llanuras abiertas del este; se cita en la charca de King Nehale, en Namutoni.",
  # --- AVES ---
  "tejedor-republicano": "**En Okaukuejo, a diez metros de la charca**: hay un nido enorme junto al agua y dos más en el camping. Dentro viven halcones pigmeos y agapornis de cara rosa.",
  "flamenco-enano": "⚠️ **En noviembre no están aquí:** la pan está seca. Solo crían cuando llueve por encima de 400 mm — pasó **tres veces en cuarenta años**. Los tuyos están en **Walvis Bay**.",
  "flamenco-comun": "⚠️ Lo mismo: **la pan está seca en noviembre**. En cambio en **Walvis Bay el máximo va de junio a noviembre** — allí sí, y en cantidad.",
  "grulla-azul": "**Andoni**, al norte de Namutoni, es el sitio. Pero quedaban **19 aves en 2021** —eran 138 en los 70—: es la población más aislada del mundo, a 1.200 km de la siguiente.",
  "abejaruco-europeo": "**Sí está en vuestras fechas**: llega en octubre y en noviembre se registra en el parque. Caza al vuelo desde ramas secas y postes.",
  "ciguena-abdim": "⚠️ **En noviembre, no.** En Etosha es ave de **febrero y marzo**: en noviembre su tasa de registro es cero. Va aquí para que no la busquéis en balde.",
  "bateleur": "Se cita sobre **Kalkheuwel**, junto con el milano. Etosha reúne unas 40 rapaces, casi el 70 % de las de Namibia.",
  "buho-lacteo": "En los árboles grandes **dentro de los campamentos** — mira arriba al volver de cenar.",
  "calao-amarillo": "En los tres campamentos, vigilando las mesas del desayuno.",
  "calao-rojo": "Igual que el amarillo: campamentos y bordes de pista.",
  "estornino-cabo": "En los campamentos, a por las migas.",
  "francolin-picorrojo": "En los campamentos. **Os despertará al amanecer**, sin falta.",
  "pigargo-vocinglero": "Depende de que haya agua abierta: la zona de **Fischer's Pan**, en el este, es donde tiene sentido buscarlo.",
  "pelicano": "No en Etosha: en la **laguna de Walvis Bay** (D5–D6), donde pesca en grupo.",
  # --- COSTA ---
  "lobo-marino": "**Cape Cross, D7.** Una de las mayores colonias del mundo.",
  "delfin-heaviside": "Frente a **Walvis Bay**, en las salidas en barco (D5–D6).",
}

FUENTES_ETOSHA = [
  "<b>Horarios de puerta:</b> tabla oficial <i>Etosha National Park Gates Opening &amp; Closing Time</i> (3–9 nov 06:13–19:06 · 10–16 nov 06:10–19:10). Cambian cada semana y están puestas en cada puerta.",
  "<b>Reglamento del parque</b> (60 km/h, 20 en campamentos, prohibido bajar del coche fuera de los campamentos, prohibido salir de las pistas): <i>Park Regulations</i> de NWR/MEFT.",
  "<b>Rinoceronte negro:</b> MEFT (ficha de Etosha) y NWR confirman león, elefante y rinoceronte negro de noche en Okaukuejo. Lo de «mayor población mundial» es de la <i>subespecie suroccidental</i>: WWF sitúa el 72 % de la población nacional en Etosha.",
  "<b>Impala de cara negra:</b> UICN (Vulnerable, endémica de Kaokoveld y suroeste de Angola) y Matson 2006 — cinco subpoblaciones que coinciden con los cinco puntos de suelta de los años 70.",
  "<b>Grulla azul:</b> Craig 2017 (<i>Bull. B.O.C.</i>) y el Namibia Crane Working Group — 19 aves en el censo de noviembre de 2021, y 1.200 km hasta la población sudafricana.",
  "<b>Flamencos:</b> NASA Earth Observatory (la pan seca en diciembre, inundada en enero), Simmons 1996 (tres eventos de cría en 40 años) y BirdLife (umbral de 400 mm). Máximos de Walvis Bay de junio a noviembre: SABAP1.",
  "<b>Migradores:</b> tasas de registro mensuales de SABAP2 / African Bird Atlas filtradas a Etosha. Ahí se ve que el abejaruco carmesí tiene <i>cero</i> registros en el parque y que la cigüeña de Abdim es de febrero-marzo.",
  "<b>Cebra de montaña:</b> |Uiseb 2024 — en Etosha está restringida a las lomas de dolomita del oeste; la de llanura, por todo el parque.",
  "<b>Dik-dik:</b> Travel News Namibia (Dik-dik Drive) y registros de GBIF: ~206 en la cuadrícula de Namutoni frente a 4 en Okaukuejo.",
  "<b>Obras de la carretera:</b> nota oficial del MEFT de 2026 —«Traffic deviation via Gemsbokvlakte road from Okaukuejo to Halali», meft.gov.na/news/335, con aviso paralelo de NWR—: desvío obligatorio del 2 jun 2026 al jul 2027. La página devuelve 403; las fechas convergen en cinco secundarias (◐). Reconfirmar con NWR (+264 67 229 800).",
  "<b>Charcas:</b> Expert Africa, etosha.org, Roxanne Reid y etoshanationalpark.co.za — secundarias, pero coincidentes entre sí.",
  "<b>Sin dato (y no se rellena):</b> la hora punta nocturna del rinoceronte en Okaukuejo, el número absoluto de rinocerontes del parque, la orientación solar de cada charca y la frecuencia real de la hiena parda.",
]
