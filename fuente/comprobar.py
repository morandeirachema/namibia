#!/usr/bin/env python3
"""Comprobaciones baratas antes de dar un PDF por bueno.

No valida el contenido del viaje —eso lo hace la verificacion a tres votos del propio
dossier—, sino que el build no se ha roto por debajo: que estan todas las imagenes, que
ninguna se ha colado con licencia no libre, que el catalogo y los creditos cuadran y que
los PDF existen y tienen paginas.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import catalogo                                                    # noqa: E402
import trazado                                                     # noqa: E402

LICENCIAS_OK = ("CC BY", "CC0", "Public domain", "FAL")
FALLOS = []


def mal(msg):
    FALLOS.append(msg)
    print("  FALLO  " + msg)


def bien(msg):
    print("  ok     " + msg)


def revisa_imagenes():
    ruta = os.path.join(RAIZ, "img", "creditos.json")
    if not os.path.exists(ruta):
        return mal("no existe img/creditos.json — ejecuta `python3 fuente/descargar.py`")
    cr = json.load(open(ruta))

    esperadas = {f"lugares/{s}" for s, _, _ in catalogo.LUGARES}
    esperadas |= {f"fauna/{e[0]}" for _, _, l in catalogo.GRUPOS_FAUNA for e in l}
    faltan = esperadas - set(cr)
    if faltan:
        mal(f"{len(faltan)} imagenes del catalogo sin descargar: {sorted(faltan)[:4]}…")
    sobran = set(cr) - esperadas
    if sobran:
        mal(f"{len(sobran)} imagenes descargadas que ya no estan en el catalogo: {sorted(sobran)[:4]}…")

    sin_fichero = [k for k, v in cr.items()
                   if not os.path.exists(os.path.join(RAIZ, "img", v["carpeta"], v["local"]))]
    if sin_fichero:
        mal(f"{len(sin_fichero)} entradas de creditos sin fichero en disco")

    no_libres = [f'{k} ({v["licencia"]})' for k, v in cr.items()
                 if not v["licencia"].startswith(LICENCIAS_OK)]
    if no_libres:
        mal(f"licencia no libre en: {no_libres}")

    sin_autor = [k for k, v in cr.items() if not v.get("autor")]
    if sin_autor:
        mal(f"{len(sin_autor)} imagenes sin autor — la licencia obliga a citarlo")

    if not (faltan or sobran or sin_fichero or no_libres or sin_autor):
        bien(f"{len(cr)} imagenes, todas con fichero, licencia libre y autor")


def revisa_geo():
    faltan = [n for n in ("paises.json", "parques.json", "etosha_pan.json",
                          "etosha_pistas.json", "etosha_puntos.json", "ruta.json")
              if not os.path.exists(os.path.join(HERE, "geo", n))]
    if faltan:
        return mal(f"faltan geodatos: {faltan} — ejecuta `python3 fuente/geodatos.py`")
    ruta = json.load(open(os.path.join(HERE, "geo", "ruta.json")))
    sin_traza = [e["id"] for e in ruta if e["km"] is None]
    if sin_traza:
        mal(f"etapas sin trazado: {sin_traza}")
    total = sum(e["km"] or 0 for e in ruta)
    if not 2200 < total < 3200:
        mal(f"la ruta suma {total:.0f} km, fuera de lo razonable para este viaje")
    else:
        bien(f"ruta completa: {len(ruta)} etapas, {total:.0f} km")

    # Los tramos con firme (geo/tramos.json) son otra descarga de OSRM sobre las MISMAS
    # etapas: si se mueve una noche y se regenera ruta.json sin regenerarlos, el mapa
    # del dia de la agenda pinta el recorrido de antes. Se comprueba que cubren los
    # mismos dias y casi los mismos kilometros —a OSRM los `steps` le suman un poco por
    # el redondeo de cada paso—, y que no queda ningun tramo largo sin firme conocido.
    fich = os.path.join(HERE, "geo", "tramos.json")
    if not os.path.exists(fich):
        return mal("falta geo/tramos.json — ejecuta `python3 fuente/geodatos.py tramos`")
    tramos = {e["id"]: e["tramos"] for e in json.load(open(fich))}
    km_ruta = {e["id"]: e["km"] or 0 for e in ruta}
    if set(tramos) != set(km_ruta):
        return mal("geo/tramos.json no cubre los mismos dias que geo/ruta.json: regenera "
                   "con `python3 fuente/geodatos.py tramos --forzar`")
    desfase = [d for d in km_ruta if abs(sum(t["km"] for t in tramos[d]) - km_ruta[d]) > 3]
    if desfase:
        return mal(f"los tramos con firme no cuadran con la ruta en {desfase}: regenera "
                   "geo/tramos.json")
    sin = {t["ref"] or t["nombre"] or "?" for ts in tramos.values() for t in ts
           if t["firme"] is None and t["km"] >= 8}
    if sin:
        mal(f"carreteras de mas de 8 km sin firme en trazado.FIRME: {sorted(sin)}")
    else:
        bien(f"firme: {sum(len(t) for t in tramos.values())} tramos con carretera conocida, "
             f"ninguno largo sin clasificar")


def revisa_dia_a_dia():
    """Que los kilometros del `01` sean los que mide la geometria de la ruta.

    El `aparte/decision-del-ccf` tenia esta comprobacion desde que se despego una vez; el `01` —que es LA
    ruta— no la tuvo nunca, y es el documento que mas se toca. El 24/08, al renumerar
    los dias, dos titulares se quedaron en la cifra redondeada de una discusion vieja
    (`~340` con OSRM en 342,6) sin que nada avisara. Se comprueban solo los dias que
    declaran kilometros: la llegada, el dia de descanso y el de vuelo no lo hacen a
    proposito.
    """
    fich = os.path.join(HERE, "geo", "ruta.json")
    if not os.path.exists(fich):
        return mal("falta geo/ruta.json — ejecuta `python3 fuente/geodatos.py`")
    medido = {e["id"]: e["km"] for e in json.load(open(fich)) if e["km"] is not None}
    doc = open(os.path.join(RAIZ, "01-itinerarios-dia-a-dia.md")).read()

    dias_doc = re.findall(r"^### (D\d+) ·", doc, re.M)
    fallos = []
    if set(dias_doc) != set(medido):
        fallos.append(f"el `01` describe {sorted(set(dias_doc) - set(medido))} de mas y "
                      f"{sorted(set(medido) - set(dias_doc))} de menos que la geometria")
    con_km = 0
    for m in re.finditer(r"^### (D\d+) ·[^\n]*?(\d[\d.]*) km", doc, re.M):
        dia, km = m.group(1), float(m.group(2).replace(".", ""))
        if dia not in medido:
            continue
        con_km += 1
        if abs(km - medido[dia]) > 2:
            fallos.append(f"{dia}: el `01` titula {km:.0f} km y OSRM mide {medido[dia]:.1f}")

    if fallos:
        for f in fallos:
            mal(f)
    else:
        bien(f"el dia a dia del `01`: {len(dias_doc)} dias, {con_km} con kilometros, "
             f"todos los que mide la geometria")


def revisa_anclas_de_la_agenda():
    """Que el `01` siga teniendo los dos literales entre los que `agenda.py` recorta el dia a dia.

    La agenda corta el `01` entre `### D1 ·` y `### 💰 Coste real`. Si alguien reescribe ese
    encabezado, `make agenda` muere — y como el CI no regenera los PDF, nadie lo ve hasta el
    siguiente `make`. Mejor que lo diga esto.
    """
    texto = open(os.path.join(RAIZ, "01-itinerarios-dia-a-dia.md")).read()
    faltan = [a for a in ("\n### D1 ·", "\n### 💰 Coste real") if a not in texto]
    if faltan:
        mal(f"el `01` ya no tiene {[a.strip() for a in faltan]}, y `agenda.py` recorta el dia a "
            f"dia entre esos dos encabezados")
    else:
        bien("agenda: el `01` conserva los dos encabezados entre los que se recorta")


def revisa_ruta_alt():
    """Que el dia a dia del `aparte/decision-del-ccf` no se haya despegado de la geometria de su variante.

    El `aparte/decision-del-ccf` lleva quince etapas escritas a mano y un mapa que sale de `geo/ruta-alt.json`.
    Son la misma ruta contada dos veces, y hasta ahora nada obligaba a que dijeran lo
    mismo: cambiar una etapa en `trazado.ETAPAS_ALT` movia el mapa y dejaba la prosa
    contando los kilometros de antes. Se comprueba cada dia con 1 km de tolerancia
    —cada etapa se redondea por su cuenta— y el titular contra la suma de verdad.
    """
    fich = os.path.join(HERE, "geo", "ruta-alt.json")
    if not os.path.exists(fich):
        return mal("falta geo/ruta-alt.json — ejecuta `python3 fuente/geodatos.py ruta-alt`")
    alt = json.load(open(fich))
    if len(alt) != len(trazado.ETAPAS_ALT):
        mal(f"geo/ruta-alt.json tiene {len(alt)} etapas y trazado.ETAPAS_ALT, "
            f"{len(trazado.ETAPAS_ALT)}: regenera la geometria")
    sin_traza = [e["id"] for e in alt if e["km"] is None]
    if sin_traza:
        mal(f"etapas de la variante sin trazado: {sin_traza}")

    md = os.path.join(RAIZ, "aparte", "decision-del-ccf.md")
    if not os.path.exists(md):
        return mal("falta aparte/decision-del-ccf.md — si se ha borrado a proposito, quita con el "
                   "revisa_ruta_alt, trazado.ETAPAS_ALT y geo/ruta-alt.json")
    doc = open(md).read()
    medido = {e["id"]: e["km"] for e in alt if e["km"] is not None}
    dichos, fallos = {}, []
    for m in re.finditer(r"^- \*\*(D\d+) ·[^\n]*?(\d[\d.]*) km", doc, re.M):
        dichos[m.group(1)] = float(m.group(2).replace(".", ""))
    faltan = sorted(set(medido) - set(dichos))
    if faltan:
        fallos.append(f"el `aparte/decision-del-ccf` no lista {faltan}")
    for d, km in sorted(dichos.items()):
        if d in medido and abs(km - medido[d]) > 1:
            fallos.append(f"{d}: el `aparte/decision-del-ccf` dice {km:.0f} km y OSRM mide {medido[d]:.1f}")

    fallos += _horas_de_la_variante(doc, medido)

    total = sum(medido.values())
    m = re.search(r"\*\*~([\d.]+) km\*\* \*\(\*\*(\d+) (menos|más)\*\*", doc)
    if not m:
        fallos.append("el `aparte/decision-del-ccf` ya no lleva su titular de kilometros")
    else:
        dicho = float(m.group(1).replace(".", ""))
        if abs(dicho - total) > 1:
            fallos.append(f"el titular del `aparte/decision-del-ccf` dice {dicho:.0f} km y la geometria suma "
                          f"{total:.0f}")
        oficial = sum(e["km"] or 0 for e in
                      json.load(open(os.path.join(HERE, "geo", "ruta.json"))))
        resta = (oficial - total) if m.group(3) == "menos" else (total - oficial)
        if abs(float(m.group(2)) - resta) > 1.5:
            fallos.append(f"el `aparte/decision-del-ccf` dice {m.group(2)} km {m.group(3)} que la oficial y la resta "
                          f"da {resta:.0f}")

    # el mapa que el documento promete tiene que existir de verdad
    for ext in ("svg", "png"):
        rel = f"img/mapas/ruta-alternativa.{ext}"   # el doc lo enlaza como ../img/…
        if rel not in doc:
            fallos.append(f"el `aparte/decision-del-ccf` ya no enlaza {rel}")
        elif not os.path.exists(os.path.join(RAIZ, rel)):
            fallos.append(f"falta {rel} — ejecuta `python3 fuente/mapa.py`")

    if fallos:
        for f in fallos:
            mal(f)
    else:
        bien(f"la variante del `aparte/decision-del-ccf`: {len(medido)} etapas medidas, {total:.0f} km, "
             f"y el dia a dia cuadra con el mapa")


# Velocidades de planificacion del `13`: asfalto 100, grava 80, dentro de parque 60.
V = {"asfalto": 100.0, "grava": 80.0, "parque": 60.0}


def _horas_de_la_variante(doc, medido):
    """Que los tiempos del `aparte/decision-del-ccf` se deriven de su propio desglose de firme, y no de la nada.

    Lo que paso: el `aparte/decision-del-ccf` daba «289 km · ~3 h 35» y «294 km · ~3 h 40», la MISMA velocidad
    para una etapa que arranca dentro del parque y otra que es B1 entera. Ni salia de OSRM
    ni del convenio del `13`, y una comprobacion de banda —entre km/100 y km/60— no lo
    habria cazado: 80 km/h cae comodamente dentro. Lo unico que lo caza es exigir que el
    tiempo CUADRE con el reparto de firme, asi que la regla es esa: toda etapa que declare
    un tiempo tiene que declarar tambien sus kilometros de asfalto, grava y parque; el
    reparto tiene que sumar los kilometros de la etapa; y el minimo tiene que ser
    exactamente el que sale de las tres velocidades. El realista, nunca menor que el minimo.
    """
    fallos = []
    for trozo in re.split(r"\n(?=- \*\*D\d+ ·)", doc):
        m = re.match(r"- \*\*(D\d+) ·", trozo)
        if not m:
            continue
        dia, km = m.group(1), medido.get(m.group(1))
        renglon = trozo.split("\n- ")[0]
        tiempos = [int(a) + int(b) / 60 for a, b in re.findall(r"~(\d+) h (\d+)", renglon)]
        if not km or not tiempos:
            continue
        firme = {c: 0.0 for c in V}
        for n, clase in re.findall(r"(\d+)\s+(?:km\s+)?de\s+(asfalto|grava)", renglon):
            firme[clase] += float(n)
        p = re.search(r"(\d+)\s+dentro del parque", renglon)
        if p:
            firme["parque"] += float(p.group(1))
        if not sum(firme.values()):
            fallos.append(f"{dia}: el `aparte/decision-del-ccf` da un tiempo sin decir de que firme sale "
                          f"— pon los km de asfalto, grava y parque")
            continue
        if abs(sum(firme.values()) - km) > 2:
            fallos.append(f"{dia}: el desglose de firme del `aparte/decision-del-ccf` suma "
                          f"{sum(firme.values()):.0f} km y la etapa mide {km:.0f}")
        esperado = sum(firme[c] / V[c] for c in V)
        if abs(tiempos[0] - esperado) > 0.03:
            fallos.append(f"{dia}: el `aparte/decision-del-ccf` dice ~{int(tiempos[0])}h{round(tiempos[0] % 1 * 60):02d} "
                          f"y su propio desglose a las velocidades del `13` da "
                          f"{int(esperado)}h{round(esperado % 1 * 60):02d}")
        if len(tiempos) > 1 and min(tiempos[1:]) < tiempos[0]:
            fallos.append(f"{dia}: el `aparte/decision-del-ccf` da un tiempo realista menor que su minimo")
    return fallos


# Los documentos que se leen SOBRE EL TERRENO, donde cada N$ es dinero que se paga y
# tiene que llevar su equivalente al lado. Se comprueban solo estos a proposito: en
# los de investigacion (02, 07, 11, 12, 15) hay cifras que se citan para desmentirlas
# —«N$150 es lo que repiten los blogs», «N$445 fue un error de extraccion»— y tarifas que
# no nos aplican, como la de residente namibio. Exigirles el euro llenaria esto de avisos
# falsos, y una comprobacion que grita sin motivo se acaba ignorando. El `20` entra por la
# misma logica desde el otro lado: es el cuaderno con el que se reserva, con la tarjeta en
# la mano — cada N$ suyo es dinero que se va a pagar.
SOBRE_EL_TERRENO = ("01-itinerarios-dia-a-dia.md", "03-alojamiento-y-tasas.md",
                    "13-itinerario.md", "18-manual-de-campamento.md", "20-reservas.md",
                    "21-campamentos-de-etosha.md", "22-picadura-de-escorpion.md")

RE_NAD = re.compile(r"(?<![+\-±])N\$\s?([\d][\d.,]*)")


def revisa_precios():
    """La regla de la casa: todo precio, en N$ y en € a la vez.

    Se mira una ventana a los dos lados porque el euro tanto puede ir pegado
    —«N$920 ≈ €46»— como al final de la frase.
    """
    huerfanos = []
    for nombre in SOBRE_EL_TERRENO:
        ruta = os.path.join(RAIZ, nombre)
        if not os.path.exists(ruta):
            continue
        texto = open(ruta).read()
        for m in RE_NAD.finditer(texto):
            if m.group(1).rstrip(".,") == "0":          # franquicia N$0: no es un precio
                continue
            if texto[m.end():m.end() + 2] == "/l":      # el precio del diesel, en su serie
                continue
            cerca = texto[max(0, m.start() - 80):m.end() + 80]
            if "€" in cerca or "EUR" in cerca:          # EUR: dentro de un Mermaid, que no admite €
                continue
            huerfanos.append(f"{nombre}:{texto[:m.start()].count(chr(10)) + 1} {m.group(0)}")
    if huerfanos:
        mal(f"{len(huerfanos)} precios en N$ sin su equivalente en € al lado: "
            f"{huerfanos[:5]}…")
    else:
        bien(f"precios: los {len(SOBRE_EL_TERRENO)} documentos de campo, todos en N$ y € a la vez")


def revisa_convenciones():
    """Dos reglas de maquetacion que el markdown no delata y el PDF sufre.

    Las tablas se maquetan a mano en rejilla, asi que una tabla de markdown sale sin
    estilo; y el `%% ancho` que hace que un diagrama cruce las dos columnas tiene que ir
    en la SEGUNDA linea del bloque, porque de la primera se saca el tipo de diagrama.
    """
    fallos = []
    for f in sorted(os.listdir(RAIZ)):
        if not re.match(r"\d\d-.*\.md$", f) and f != "README.md":
            continue
        texto = open(os.path.join(RAIZ, f)).read()
        if re.search(r"^\|", texto, re.M):
            fallos.append(f"{f}: tabla de markdown — lo tabular va en rejilla o en Mermaid")
        for m in re.finditer(r"```mermaid\n(.*?)```", texto, re.S):
            for i, linea in enumerate(m.group(1).split("\n")):
                if "%% ancho" in linea and i != 1:
                    fallos.append(f"{f}: '%% ancho' en la linea {i + 1} del bloque y va en la 2")
    if fallos:
        for f in fallos:
            mal(f)
    else:
        bien("convenciones: ni una tabla de markdown y los '%% ancho' en su linea")


SALIDA_VIAJE = (2026, 10, 30)                       # el vuelo de ida, del README y del 13

MESES_ES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def revisa_fechas():
    """Que la cuenta atras del README cuadre con la fecha que el propio README declara.

    No se compara contra HOY a proposito: si no, esto fallaria todos los dias sin que
    nadie haya roto nada, y una comprobacion que falla siempre deja de leerse. Lo que
    se vigila es la incoherencia de verdad —tocar la fecha y olvidar el numero, o al
    reves— y que el dossier lleve la misma fecha que el README, porque la imprime en
    todas sus paginas.
    """
    import datetime
    texto = open(os.path.join(RAIZ, "README.md")).read()
    m = re.search(r"\*\*Última actualización: (\d{1,2}) de (\w+) de (\d{4})\*\*", texto)
    if not m:
        return mal("el README ya no dice cuando se actualizo por ultima vez")
    dia, mes, ano = int(m.group(1)), m.group(2), int(m.group(3))
    if mes not in MESES_ES:
        return mal(f"la fecha del README dice el mes «{mes}», que no existe")
    fecha = datetime.date(ano, MESES_ES.index(mes) + 1, dia)

    faltan = (datetime.date(*SALIDA_VIAJE) - fecha).days
    dichos = re.search(r"faltan-(\d+)_d%C3%ADas", texto)
    if not dichos:
        mal("el README ya no lleva la chapa de la cuenta atras")
    elif int(dichos.group(1)) != faltan:
        mal(f"la cuenta atras del README dice {dichos.group(1)} dias y desde su propia "
            f"fecha ({fecha:%d/%m/%Y}) faltan {faltan} para salir")
    else:
        bien(f"fechas: el README dice {fecha:%d/%m/%Y} y sus {faltan} dias cuadran")

    # La fecha del pie de los TRES PDF vive en fecha.py: el 26/08 cada programa llevaba la
    # suya y salieron con tres fechas distintas sin que esto —que solo miraba dossier.py— avisara.
    fecha_py = open(os.path.join(HERE, "fecha.py")).read()
    m2 = re.search(r'^FECHA = "([^"]+)"', fecha_py, re.M)
    esperada = f"{dia} de {mes} de {ano}"
    if not m2:
        mal("fuente/fecha.py ya no define FECHA, y los tres PDF la imprimen de ahi")
    elif m2.group(1) != esperada:
        mal(f"los PDF se imprimen con fecha «{m2.group(1)}» (fuente/fecha.py) y el README dice "
            f"«{esperada}»")


# Las reservas de alojamiento que hacen el viaje, con lo que pesa cada casilla del `20`
# §9: la de Etosha tacha cuatro noches de una vez (Okaukuejo, Halali y Onguma x2 — desde
# el 24/08 Namutoni ya no esta). Spreetshoogte bajo a una sola noche y el Urban Camp de
# Windhoek entro en la cuenta al reservarse, asi que el total pasa de 7 a 8.
RESERVAS_CONTADAS = (("Sesriem ×2", 1), ("Terrace Bay", 1),
                     ("noches de Etosha", 4), ("Spreetshoogte", 1),
                     ("Windhoek D1", 1))


def revisa_contador_reservas():
    """Que la chapa de reservas del README cuadre con las casillas tachadas del `20` §9.

    El 21/08 la chapa decia «4 de 6» mientras el propio README contaba tres pendientes de
    seis, y la casilla de Spreetshoogte estaba marcada con la reserva sin hacer — que en el
    PDF se imprime como casilla de verdad, para marcar a boli sobre el terreno. Nada lo
    vigilaba: la cuenta atras si tenia comprobacion y este contador no.
    """
    reservas = open(os.path.join(RAIZ, "20-reservas.md")).read()
    hechas = total = 0
    for nombre, peso in RESERVAS_CONTADAS:
        # el \b del final importa: sin el, «Windhoek D1» tambien casaba con
        # «Windhoek D14» y el contador veia dos casillas donde hay una.
        casillas = re.findall(r"^- \[([ x])\] .*" + re.escape(nombre) + r"\b",
                              reservas, re.M)
        if len(casillas) != 1:
            return mal(f"en el `20` §9 hay {len(casillas)} casillas para «{nombre}», "
                       f"y el contador de reservas del README se cuenta desde ahi")
        total += peso
        hechas += peso if casillas[0] == "x" else 0

    texto = open(os.path.join(RAIZ, "README.md")).read()
    chapa = re.search(r"reservas-(\d+)_de_(\d+)-", texto)
    if not chapa:
        return mal("el README ya no lleva la chapa de reservas")
    if (int(chapa.group(1)), int(chapa.group(2))) != (hechas, total):
        return mal(f"la chapa del README dice «{chapa.group(1)} de {chapa.group(2)}» "
                   f"reservas y las casillas del `20` §9 dan {hechas} de {total}")
    bien(f"reservas: la chapa del README y las casillas del `20` dicen las mismas "
         f"({hechas} de {total})")


# Las dos tartas del presupuesto cuentan lo mismo en unidades distintas: la del README va
# POR PERSONA y la del `02` §1, POR PAREJA. Aqui se dice cual es cual — a la derecha, las
# etiquetas del `02` que suman la partida del README (los misceláneos y las actividades van
# juntos alli y separados aqui).
TARTAS = {
    "Vuelo":              ("Vuelo ida y vuelta x2",),
    "Coche 15 dias":      ("Coche Savanna 15d",),
    "Alojamiento":        ("Alojamiento 14 noches",),
    "Combustible":        ("Combustible",),
    "Comida":             ("Comida",),
    "Seguro":             ("Seguro IATI Estrella x2",),
    "Tasas de parque":    ("Tasas de parque",),
    "Visado":             ("Visado x2",),
    "Misc + actividades": ("Miscelaneos", "Actividades"),
}


def _eur(n):
    """€1.234, con el punto de millar de la casa (formatear el mensaje entero se comia
    las comas de la propia frase)."""
    return f"€{n:,.0f}".replace(",", ".")


def _lee_tarta(texto):
    """Los pares «etiqueta : importe» de un bloque ```mermaid pie```."""
    bloque = re.search(r"```mermaid\s*\npie[^`]*?```", texto, re.S)
    if not bloque:
        return {}
    return {m.group(1): float(m.group(2))
            for m in re.finditer(r'"([^"]+)"\s*:\s*([\d.]+)', bloque.group(0))
            if m.group(1) != "title"}


def revisa_cuadre_presupuesto():
    """Que el desglose del presupuesto sume su propio total, y que las dos tartas concuerden.

    Nada vigilaba esto y costo un desfase silencioso: al cambiar la segunda noche de
    Namutoni por Onguma (+€16 la pareja) se actualizo la prosa del `02` §3 pero NO las dos
    tartas, asi que durante tres dias el README repartia €3.982 mientras su propio titular
    anunciaba €3.990, y el `02` repartia €7.963 bajo un «TOTAL LA PAREJA: ~€7.980». Los dos
    desgloses mentian por separado y los dos parecian correctos de un vistazo.

    Se comprueban dos cosas independientes, porque fallan de formas distintas: que cada
    tarta sume su total impreso —lo que caza la deriva de una partida— y que la del `02`
    sea el doble de la del README —lo que caza que se toque una y no la otra—.
    """
    antes = len(FALLOS)
    readme = open(os.path.join(RAIZ, "README.md")).read()
    presu = open(os.path.join(RAIZ, "02-presupuesto.md")).read()
    pp, par = _lee_tarta(readme), _lee_tarta(presu)
    if not pp or not par:
        return mal("no se encuentran las tartas del presupuesto (README y/o `02` §1)")

    faltan = [e for e in TARTAS if e not in pp]
    faltan += [e for grupo in TARTAS.values() for e in grupo if e not in par]
    if faltan:
        return mal(f"partidas del presupuesto que ya no estan en su tarta: {faltan}")

    # 1 · cada tarta suma el total que su propio documento anuncia
    # el titular va anclado a su encabezado: suelto, «~€17 por persona» del bus de Oporto
    # tambien encaja, y el aviso saldria contra la cifra equivocada
    for etiqueta, suma, rx, texto, tol in (
            ("por persona", sum(pp.values()), r"^### ~€([\d.]+) por persona", readme, 3),
            ("la pareja", sum(par.values()), r"TOTAL LA PAREJA: ~€([\d.]+)", presu, 6)):
        m = re.search(rx, texto, re.M)
        if not m:
            mal(f"no se encuentra el total anunciado «{etiqueta}» del presupuesto")
            continue
        dicho = float(m.group(1).replace(".", ""))
        if abs(suma - dicho) > tol:
            mal(f"el desglose {etiqueta} suma {_eur(suma)} y el total anunciado dice "
                f"{_eur(dicho)} (diferencia {_eur(abs(suma - dicho))})")

    # 2 · la tarta de la pareja es la del README multiplicada por dos
    for eti_pp, etis_par in TARTAS.items():
        doble, real = pp[eti_pp] * 2, sum(par[e] for e in etis_par)
        if abs(doble - real) > 2:                      # 2 € de margen: hay redondeos
            mal(f"«{eti_pp}»: el README dice {_eur(pp[eti_pp])} por persona "
                f"({_eur(doble)} la pareja) y el `02` dice {_eur(real)}")

    # 3 · y la linea de texto del README no puede contradecir a su propia tarta
    m = re.search(r"Alojamiento \*\*~?€([\d.]+)\*\*", readme)
    if not m:
        mal("el README ya no escribe «Alojamiento **€…**» en su desglose, y esta comprobacion "
            "lo necesita para cotejarlo con la tarta")
    elif abs(float(m.group(1).replace(".", "")) - pp["Alojamiento"]) > 1:
        mal(f"el README escribe «Alojamiento €{m.group(1)}» en el desglose y "
            f"{_eur(pp['Alojamiento'])} en su tarta")

    # 4 · el §11 reparte el mismo total en cuatro cubos por solidez (duro / tarifa
    # verificada / corroborado / estimado). Al cerrar algo hay que subirlo de cubo Y
    # bajarlo del suyo: si solo se hace lo primero, los cubos suman de mas y el reparto
    # deja de describir el total que dice describir.
    cubos = [float(x.replace(".", "")) for x in
             re.findall(r"^- \*\*[✅◐○][^—]*—\s*~?€([\d.]+)", presu, re.M)]
    if len(cubos) != 4:
        mal(f"el `02` §11 ya no reparte el total en 4 cubos de solidez (encontrados {len(cubos)})")
    elif abs(sum(cubos) - sum(pp.values())) > 3:
        mal(f"el `02` §11 reparte {_eur(sum(cubos))} entre sus cubos de solidez y el "
            f"presupuesto por persona suma {_eur(sum(pp.values()))}")

    # 5 · «todo lo demas junto son ~€X» es una RESTA del total menos vuelo y coche, y las
    # restas escritas a mano se quedan viejas calladas: las dos se quedaron en la cifra de
    # antes de Onguma mientras sus dos sumandos ya eran otros.
    for doc, texto, tarta, rx in (
            ("README", readme, pp, r"Todo lo demás junto son ~€([\d.]+)"),
            ("`02` §1", presu, par, r"Todo lo demás junto \(~€([\d.]+)")):
        m = re.search(rx, texto)
        if not m:
            mal(f"{doc} ya no dice «todo lo demás junto son ~€…», y esa resta se queda sin vigilar")
            continue
        vuelo = next(v for k, v in tarta.items() if k.startswith("Vuelo"))
        coche = next(v for k, v in tarta.items() if k.startswith("Coche"))
        resto = sum(tarta.values()) - vuelo - coche
        if abs(float(m.group(1).replace(".", "")) - resto) > 3:
            mal(f"{doc} dice que «todo lo demás junto» son €{m.group(1)} y su tarta, "
                f"quitando vuelo y coche, deja {_eur(resto)}")

    if len(FALLOS) == antes:
        bien(f"presupuesto: las dos tartas cuadran entre si y con sus totales "
             f"({_eur(sum(pp.values()))} pp / {_eur(sum(par.values()))} pareja)")


def revisa_gps():
    """Que el GPX y el KML sigan describiendo la MISMA ruta que el dossier.

    Se generan de `geo/ruta.json`, igual que el mapa y la lamina, asi que lo unico que
    puede pasar es que se queden sin regenerar tras mover una noche: entonces el GPS
    llevaria una ruta y el PDF otra, que es la peor forma de descubrirlo —en Namibia—.
    """
    import xml.etree.ElementTree as ET
    ruta = json.load(open(os.path.join(HERE, "geo", "ruta.json")))
    con_traza = [e for e in ruta if e.get("geometria")]
    km = sum(e["km"] or 0 for e in ruta)

    gpx = os.path.join(RAIZ, "ruta-namibia-2026.gpx")
    if not os.path.exists(gpx):
        return mal("falta ruta-namibia-2026.gpx — ejecuta `make gps`")
    try:
        raiz = ET.parse(gpx).getroot()
    except ET.ParseError as e:
        return mal(f"ruta-namibia-2026.gpx no es XML valido: {e}")
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    pistas = raiz.findall("g:trk", ns)
    puntos = raiz.findall("g:wpt", ns)
    if len(pistas) != len(con_traza):
        return mal(f"el GPX lleva {len(pistas)} etapas y la ruta tiene {len(con_traza)} "
                   f"con trazado — regenera con `make gps`")
    if len(puntos) != len(trazado.puntos_oficiales()):
        return mal(f"el GPX lleva {len(puntos)} puntos y la ruta oficial tiene "
                   f"{len(trazado.puntos_oficiales())} — regenera con `make gps`")
    if not os.path.exists(os.path.join(RAIZ, "ruta-namibia-2026.kml")):
        return mal("falta ruta-namibia-2026.kml — ejecuta `make gps`")
    bien(f"gps: el GPX y el KML llevan las {len(pistas)} etapas con trazado, "
         f"{len(puntos)} puntos y los {km:.0f} km de la ruta")


def revisa_avistamientos():
    """Los datos que sostienen la linea de «qué posibilidades hay» de la guia de fauna.

    Lo que se vigila no es que las cifras sean altas, sino que ninguna afirmacion se
    quede sin su denominador: una probabilidad sin muestra detras es una opinion.
    """
    ruta = os.path.join(HERE, "geo", "avistamientos.json")
    if not os.path.exists(ruta):
        return mal("no existe geo/avistamientos.json — ejecuta `python3 fuente/avistamientos.py`")
    d = json.load(open(ruta))
    esperadas = {e[0] for _, _, l in catalogo.GRUPOS_FAUNA for e in l}
    faltan = esperadas - set(d.get("especies", {}))
    if faltan:
        mal(f"{len(faltan)} especies sin recuento de GBIF: {sorted(faltan)[:4]}…")
    sobran = set(d.get("especies", {})) - esperadas
    if sobran:
        mal(f"{len(sobran)} recuentos de especies que ya no estan en el catalogo: {sorted(sobran)}")

    camps = d.get("campamentos") or {}
    if not camps:
        mal("no hay porcentajes por campamento: la guia se queda sin la cifra directa")
    sin_muestra = [f"{c['nombre']}/{s}" for c in camps.values()
                   for s, f in c.get("especies", {}).items() if not f.get("partes")]
    if sin_muestra:
        mal(f"porcentajes sin muestra detras: {sin_muestra[:4]}…")
    flojos = [c["nombre"] for c in camps.values() if (c.get("viajeros") or 0) < 10]
    if flojos:
        mal(f"campamentos con menos de 10 partes, no dan para publicar un porcentaje: {flojos}")

    if not (faltan or sobran or sin_sesgo(d) or sin_muestra or flojos):
        n = sum(len(c.get("especies", {})) for c in camps.values())
        bien(f"avistamientos: {len(d['especies'])} especies en GBIF y {n} porcentajes "
             f"de {len(camps)} campamentos, todos con su muestra")


def sin_sesgo(d):
    """El sable de Okaukuejo es la prueba de que estos partes traen ruido.

    Va en el PDF como aviso, asi que tiene que seguir estando en los datos: si Expert
    Africa lo quita algun dia, el aviso se queda hablando de algo que ya no se puede
    comprobar y hay que reescribirlo.
    """
    oka = (d.get("campamentos") or {}).get("okaukuejo", {}).get("otros", {})
    if "Sable antelope" not in oka:
        mal("ya no esta el 'Sable antelope' de Okaukuejo: el aviso de la guia de fauna "
            "sobre las identificaciones malas se queda sin su ejemplo — revisalo")
        return True
    return False


def revisa_pdf(nombre, minimo):
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return mal(f"no existe {nombre}")
    salida = subprocess.run(["pdfinfo", ruta], capture_output=True, text=True).stdout
    paginas = next((int(l.split()[1]) for l in salida.splitlines()
                    if l.startswith("Pages:")), 0)
    mb = os.path.getsize(ruta) / 1024 / 1024
    if paginas < minimo:
        mal(f"{nombre} tiene {paginas} paginas, esperaba al menos {minimo}")
    else:
        bien(f"{nombre}: {paginas} paginas, {mb:.1f} MB")


def revisa_agenda(nombre="agenda-namibia-2026.pdf"):
    """La agenda: portada y DOS paginas por dia — el mapa y la explicacion —, exactamente.

    Cada dia abre en pagina impar con su mapa a pagina entera y sigue con el texto. Si
    la explicacion de un dia se desborda a una tercera, en la guantera se lee a medias:
    se localiza cual, para no tener que abrir el PDF a mirarlo. Se lee el «Dn» de la
    cabecera: la pagina del mapa y la del texto lo llevan; una tercera sin el no."""
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return mal(f"no existe {nombre}")
    salida = subprocess.run(["pdfinfo", ruta], capture_output=True, text=True).stdout
    paginas = next((int(l.split()[1]) for l in salida.splitlines()
                    if l.startswith("Pages:")), 0)
    esperadas = 1 + 2 * len(trazado.ETAPAS)
    cuenta, ultimo = {}, None
    for i in range(2, paginas + 1):
        txt = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), ruta, "-"],
                             capture_output=True, text=True).stdout
        m = re.search(r"\b(D\d+)\b", "\n".join(txt.splitlines()[:6]))
        if m:
            ultimo = m.group(1)
        if ultimo:
            cuenta[ultimo] = cuenta.get(ultimo, 0) + 1
    # El total de paginas manda: si la explicacion de un dia empieza ya en la tercera pagina,
    # las tres llevan su «Dn» en cabecera y la cuenta por dia no lo ve — paso el 25/08 con el
    # D7, que salio a 32 paginas sin que esto avisara.
    if paginas == esperadas and all(n == 2 for n in cuenta.values()):
        return bien(f"{nombre}: portada + {len(trazado.ETAPAS)} dias, mapa y explicacion")
    if paginas != esperadas:
        sospechosos = sorted((d for d, n in cuenta.items() if n != 2),
                             key=lambda d: int(d[1:])) or ["(no se localiza: mira el PDF)"]
        return mal(f"{nombre} tiene {paginas} paginas y deberia tener {esperadas}: "
                   f"se desborda {', '.join(sospechosos)}")
    # aqui el total ya cuadra: lo que falla es el reparto (un dia a tres paginas y otro a una)
    largos = sorted((d for d, n in cuenta.items() if n > 2), key=lambda d: int(d[1:]))
    cortos = sorted((d for d, n in cuenta.items() if n < 2), key=lambda d: int(d[1:]))
    mal(f"{nombre} tiene sus {paginas} paginas pero mal repartidas"
        + (f": se desborda la explicacion de {', '.join(largos)}" if largos else "")
        + (f"; sin sus dos paginas: {', '.join(cortos)}" if cortos else ""))


def revisa_lamina(nombre="mapa-ruta-namibia-2026.pdf"):
    """La lamina de ruta es UNA hoja A2: si se desborda, salen dos y la mitad va en blanco."""
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return mal(f"no existe {nombre}")
    salida = subprocess.run(["pdfinfo", ruta], capture_output=True, text=True).stdout
    paginas = next((int(l.split()[1]) for l in salida.splitlines()
                    if l.startswith("Pages:")), 0)
    medida = next((l.split(":", 1)[1].strip() for l in salida.splitlines()
                   if l.startswith("Page size:")), "")
    # pdfinfo rotula el formato el solo; Chrome deja el tamano en 1191,12 x 1685,04 pt
    # (redondeo de pulgadas), asi que se comprueba la etiqueta y no los decimales.
    if paginas != 1:
        mal(f"{nombre} tiene {paginas} paginas y la lamina es UNA: algo se desborda")
    elif "(A2)" not in medida:
        mal(f"{nombre} no mide A2, mide «{medida}»")
    else:
        bien(f"{nombre}: una hoja A2, {os.path.getsize(ruta) / 1024:.0f} KB")


def revisa_escala(nombre, alto=267, tolerancia=3):
    """Vigila que Chrome no haya encogido el PDF entero.

    Si algo no cabe a lo ancho —una URL larga en una columna de 89 mm, sin ir mas
    lejos— el navegador ensancha la caja, abre una tercera columna y reduce TODAS
    las paginas para que quepan: el documento sale a dos tercios sin avisar. El
    ancho no lo delata (la portada es `width:100%` y se encoge con el resto, asi
    que sigue llenando la caja); el alto si, porque esta en milimetros: la
    portada pide 267 mm y en un PDF sano mide eso.

    Se mide la PRIMERA mancha continua de la pagina 1 —la foto de portada—, no de
    la primera a la ultima fila con tinta: si no, el filete del pie de pagina
    entra en la cuenta y disimula un encogido suave.
    """
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "p")
        r = subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "72", "-png", ruta, base],
                           capture_output=True)
        png = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
        if r.returncode or not png:
            return mal(f"{nombre}: sin pdftoppm no se mide la escala — instala poppler-utils; "
                       f"esta es la comprobacion de la tarde perdida y no pasa en verde sin correr")
        try:
            from PIL import Image
        except ImportError:
            return mal(f"{nombre}: sin Pillow no se mide la escala — pip install -r requirements.txt; "
                       f"esta es la comprobacion de la tarde perdida y no pasa en verde sin correr")
        im = Image.open(os.path.join(tmp, png[0])).convert("L")
        w, h = im.size
        px = im.load()
        tinta = [sum(1 for x in range(w) if px[x, y] < 200) > w * .5 for y in range(h)]
        try:
            a = tinta.index(True)
            b = tinta.index(False, a) - 1
        except ValueError:
            a, b = 0, -1
        mm = (b - a + 1) / 72 * 25.4 if b >= a else 0
    if abs(mm - alto) > tolerancia:
        mal(f"{nombre}: la portada mide {mm:.0f} mm de alto y deberia medir {alto}. "
            f"Si es menos, Chrome ha encogido el PDF entero porque algo no cabe a lo ancho: "
            f"busca una URL sin partir o un diagrama que se salga de la columna")
    else:
        bien(f"{nombre}: escala correcta, la portada mide sus {mm:.0f} mm")


def revisa_paginas_readme():
    """El README anuncia cuantas paginas tiene cada PDF: que no se quede desfasado."""
    import re
    texto = open(os.path.join(RAIZ, "README.md")).read()
    for nombre in ("dossier-namibia-2026.pdf", "guia-fauna-etosha.pdf",
                   "mapa-ruta-namibia-2026.pdf", "agenda-namibia-2026.pdf"):
        ruta = os.path.join(RAIZ, nombre)
        if not os.path.exists(ruta):
            continue
        salida = subprocess.run(["pdfinfo", ruta], capture_output=True, text=True).stdout
        real = next((int(l.split()[1]) for l in salida.splitlines()
                     if l.startswith("Pages:")), 0)
        dichas = {int(n) for n in re.findall(
            re.escape(nombre) + r"[^\n]*?(\d+)\s+páginas", texto)}
        dichas |= {int(n) for n in re.findall(
            r"\((\d+)\s+páginas[^\n]*?\)", texto)} if "guia-fauna" in nombre else set()
        # la lamina no dice «1 páginas»: dice «una sola hoja A2», y eso cuenta como 1
        if re.search(re.escape(nombre) + r"[^\n]*?una sola hoja", texto):
            dichas.add(1)
        if not dichas:
            # antes esto seguia y daba `ok` con el conjunto vacio: la lamina paso asi semanas
            mal(f"el README ya no dice cuantas paginas tiene {nombre} — o lo dice con otras "
                f"palabras y esta comprobacion no las ve")
            continue
        malas = {n for n in dichas if n != real}
        if malas:
            mal(f"el README dice {sorted(malas)} paginas de {nombre}, y tiene {real}")
        else:
            bien(f"{nombre}: el README dice las paginas que son ({real})")


def revisa_indice_readme():
    """El indice del README se numera a mano: que no se descuadre ni pierda un documento."""
    import re
    texto = open(os.path.join(RAIZ, "README.md")).read()
    listados = re.findall(r"^(\d+)\. .*?\[\*\*`(\d\d)-[a-z-]+`\*\*\]", texto, re.M)
    numeros = [int(n) for n, _ in listados]
    docs = {d for _, d in listados}
    if numeros != list(range(1, len(numeros) + 1)):
        return mal(f"el indice del README va numerado {numeros}, y deberia ir 1..{len(numeros)}")
    en_disco = {f[:2] for f in os.listdir(RAIZ) if re.match(r"\d\d-.*\.md$", f)}
    if en_disco - docs:
        return mal(f"el indice del README no lista {sorted(en_disco - docs)}")
    bien(f"el indice del README: {len(numeros)} documentos, numerados y completos")


def revisa_documentos():
    import re
    docs = sorted(f for f in os.listdir(RAIZ) if re.match(r"\d\d-.*\.md$", f))
    huecos = [f for f in docs if not open(os.path.join(RAIZ, f)).read().startswith("# ")]
    if huecos:
        mal(f"documentos sin titulo de primer nivel: {huecos}")
    else:
        bien(f"{len(docs)} documentos, todos con su titulo")


def revisa_indice_dossier():
    """Cada documento que entra en el PDF tiene su resumen en el indice (dossier.py).

    RESUMEN es un diccionario escrito a mano: al estrenar un documento es facil olvidarlo
    y el indice sale con la linea del titulo desnuda, sin que nada avise. Se leen los
    literales con una expresion regular en vez de importar dossier: importar arrastra
    markdown-it y el resto del build, y esta comprobacion tiene que poder gritar
    precisamente cuando ese fichero esta a medio tocar.
    """
    fuente = open(os.path.join(HERE, "dossier.py")).read()
    m_res = re.search(r"^RESUMEN = \{(.*?)^\}", fuente, re.S | re.M)
    m_fuera = re.search(r"^FUERA_DEL_PDF = \{([^}]*)\}", fuente, re.M)
    if not (m_res and m_fuera):
        return mal("no encuentro los literales RESUMEN o FUERA_DEL_PDF en dossier.py — "
                   "si han cambiado de forma, ajusta esta comprobacion")
    con_resumen = set(re.findall(r'"(\d\d)":', m_res.group(1)))
    fuera = set(re.findall(r'"(\d\d)"', m_fuera.group(1)))
    en_pdf = {f[:2] for f in os.listdir(RAIZ) if re.match(r"\d\d-.*\.md$", f)} - fuera
    sin = en_pdf - con_resumen
    if sin:
        mal(f"documentos del PDF sin resumen en el indice (RESUMEN de dossier.py): {sorted(sin)}")
    else:
        bien(f"indice del dossier: los {len(en_pdf)} documentos del PDF, todos con su resumen")


def main():
    print("Comprobando el build…")
    revisa_documentos()
    revisa_indice_dossier()
    revisa_convenciones()
    revisa_fechas()
    revisa_contador_reservas()
    revisa_cuadre_presupuesto()
    revisa_precios()
    revisa_imagenes()
    revisa_geo()
    revisa_dia_a_dia()
    revisa_anclas_de_la_agenda()
    revisa_ruta_alt()
    revisa_gps()
    revisa_avistamientos()
    revisa_pdf("dossier-namibia-2026.pdf", 40)
    revisa_pdf("guia-fauna-etosha.pdf", 8)
    revisa_lamina()
    revisa_agenda()
    revisa_escala("dossier-namibia-2026.pdf")
    revisa_paginas_readme()
    revisa_indice_readme()
    print(f"\n{'TODO EN ORDEN' if not FALLOS else str(len(FALLOS)) + ' FALLOS'}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    raise SystemExit(main())
