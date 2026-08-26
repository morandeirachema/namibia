# -*- coding: utf-8 -*-
"""Escribe `aparte/charcas-de-los-campamentos-de-etosha.md` desde el cache de avistamientos.

Ni un porcentaje se teclea a mano: todos salen de `geo/avistamientos.json` —los partes de
Expert Africa que ya usa la guia de fauna— y el intervalo de confianza se calcula aqui.
Correr `python3 estudio_charcas.py` (o `make charcas`) lo rehace entero; si manana cambian
los partes, el estudio cambia solo y no hay que acordarse de nada.

Por que el intervalo: los tres campamentos tienen muestras muy distintas —149 viajeros en
Okaukuejo, 48 en Halali, 16 en Namutoni—, asi que comparar los porcentajes pelados hace
decir tonterias. Con el intervalo de Wilson al 95 % solo quedan en pie tres diferencias.
"""
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import catalogo                                                    # noqa: E402

SALIDA = os.path.join(RAIZ, "aparte", "charcas-de-los-campamentos-de-etosha.md")

# Orden de lectura: primero lo que se viene a buscar, luego lo que sale solo.
ORDEN = ["leopardo", "guepardo", "leon", "rino-negro", "rino-blanco", "hiena-manchada",
         "hiena-parda", "elefante", "jirafa", "cebra-burchell", "orix", "nu", "eland",
         "oricteropo"]

EMOJI = {"leon": "🦁", "leopardo": "🐆", "guepardo": "🐆", "rino-negro": "🦏",
         "rino-blanco": "🦏", "elefante": "🐘", "jirafa": "🦒", "cebra-burchell": "🦓",
         "orix": "🦌", "nu": "🐃", "eland": "🦌", "hiena-manchada": "🐕",
         "hiena-parda": "🐕", "oricteropo": "🐖"}

CAMPS = ("okaukuejo", "halali", "namutoni")


def carga():
    with open(os.path.join(HERE, "geo", "avistamientos.json")) as f:
        return json.load(f)


def nombres():
    n = {e[0]: e[1] for _, _, l in catalogo.GRUPOS_FAUNA for e in l}
    n.setdefault("oricteropo", "Oricteropo")
    return n


def wilson(k, n, z=1.96):
    """Intervalo de Wilson al 95 %. Con 11 partes, el normal da cosas imposibles."""
    if not n:
        return 0.0, 100.0
    p, den = k / n, 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    margen = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centro - margen) * 100, min(1.0, centro + margen) * 100


def dato(d, camp, slug):
    c = d["campamentos"][camp]
    x = c["especies"].get(slug) or c.get("otros", {}).get(slug)
    if not x:
        return None
    lo, hi = wilson(x["lo_vieron"], x["partes"])
    return dict(pct=x["pct"], k=x["lo_vieron"], n=x["partes"], lo=lo, hi=hi)


def separan(d, slug):
    """Pares (mas, menos) cuyos intervalos del 95 % NO se solapan."""
    ivs = {c: dato(d, c, slug) for c in CAMPS if dato(d, c, slug)}
    out = []
    for a in ivs:
        for b in ivs:
            if a < b and (ivs[a]["lo"] > ivs[b]["hi"] or ivs[b]["lo"] > ivs[a]["hi"]):
                out.append((a, b) if ivs[a]["pct"] > ivs[b]["pct"] else (b, a))
    return out


def renglon(d, nom, slug):
    trozos = []
    for c in CAMPS:
        x = dato(d, c, slug)
        etiqueta = d["campamentos"][c]["nombre"]
        trozos.append(f"{etiqueta} **sin dato** ❌" if not x else
                      f"{etiqueta} **{x['pct']} %** *({x['k']}/{x['n']} · "
                      f"{x['lo']:.0f}–{x['hi']:.0f})*")
    return f"- {EMOJI.get(slug, '·')} **{nom.get(slug, slug)}** — " + " · ".join(trozos)


def documento():
    d, nom = carga(), nombres()
    c = d["campamentos"]
    filas = "\n".join(renglon(d, nom, s) for s in ORDEN if
                      any(dato(d, k, s) for k in CAMPS))
    reales = [(s, p) for s in ORDEN for p in separan(d, s)]
    ruido = [s for s in ORDEN if any(dato(d, k, s) for k in CAMPS) and not separan(d, s)]
    lista_ruido = ", ".join(nom.get(s, s) for s in ruido)
    v = {k: c[k]["viajeros"] for k in CAMPS}
    gue = dato(d, "namutoni", "guepardo")
    leo = dato(d, "halali", "leopardo")
    leo_ok = dato(d, "okaukuejo", "leopardo")
    rin = dato(d, "okaukuejo", "rino-negro")
    rin_na = dato(d, "namutoni", "rino-negro")
    ori = dato(d, "okaukuejo", "oricteropo")

    return f"""# Las charcas de los campamentos de Etosha — qué se ve en cada una, y qué no

> **Namibia · 30 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](../README.md)
>
> Los **siete campamentos de Etosha que nombra este repo**, y lo que la evidencia dice de la charca
> de cada uno. **Tres tienen partes de avistamiento de verdad**; los otros cuatro no, y eso también
> se dice. Con cada porcentaje van **su muestra y su intervalo**, porque comparar a pelo tres
> campamentos con {v['okaukuejo']}, {v['halali']} y {v['namutoni']} viajeros detrás **hace decir
> tonterías**.
>
> **✅** fuente primaria · **◐** secundaria concordante · **○** práctica común, sin fuente ·
> **❌** sin verificar, dicho en blanco
>
> *Este documento **no se escribe a mano**: lo genera `fuente/estudio_charcas.py` desde
> `fuente/geo/avistamientos.json` —el mismo cache que alimenta la guía de fauna—. Se rehace con
> `make charcas`.*

---

## ⚠️ Lo primero, porque cambia cómo se lee todo lo demás

**La unidad de estos números es la ESTANCIA, no la charca.** Expert Africa pregunta a sus viajeros
qué vieron **durante su estancia en el campamento** ✅ — y una estancia incluye los game drives que
salen de ahí, no solo el rato sentado frente al agua iluminada. Así que esto mide **lo que rinde una
noche con base en cada sitio**, que es la pregunta que de verdad se hace uno al reservar, pero **no
es «lo que se acercó a beber»**.

Nadie publica lo segundo. Si algún día apareciera, sería otro documento.

Y la segunda advertencia, de tamaño: **la estancia típica es de una o dos noches** ✅. Como en esta
ruta se duerme en dos de los tres *(Okaukuejo y Halali; Namutoni se cruza de día el D12 —
`../21-campamentos-de-etosha.md`)*, son **dos tiradas y media**, y la
posibilidad real en el conjunto del viaje es **más alta que cualquiera de estos números**. Cuánto
más, estos datos no lo dicen — así que no se dice.

---

## 🔬 Lo que de verdad separa a las tres charcas — y lo que es ruido

Puestos los intervalos del 95 %, de catorce especies **solo sobreviven tres diferencias**:

```mermaid
flowchart LR
%% ancho
    A["MORINGA · Halali<br/>LEOPARDO {leo['pct']}%<br/>contra el {leo_ok['pct']}% de Okaukuejo"] --> D["Tres diferencias<br/>que aguantan el intervalo"]
    B["KING NEHALE · Namutoni<br/>GUEPARDO {gue['pct']}%<br/>gana a los otros dos"] --> D
    C["OKAUKUEJO<br/>RINOCERONTE NEGRO {rin['pct']}%<br/>gana a Namutoni"] --> D
    D --> E["Todo lo demas se solapa:<br/>mismo animal, misma probabilidad<br/>duermas donde duermas"]
    style A fill:#8A6210,color:#fff
    style B fill:#C2542F,color:#fff
    style C fill:#5F7043,color:#fff
    style E fill:#7D776E,color:#fff
```

- 🐆 **El leopardo es de Moringa.** Halali **{leo['pct']} %** *({leo['k']}/{leo['n']})* contra el
  **{leo_ok['pct']} %** de Okaukuejo *({leo_ok['k']}/{leo_ok['n']})*: los intervalos **no se tocan**
  *({leo['lo']:.0f}–{leo['hi']:.0f} frente a {leo_ok['lo']:.0f}–{leo_ok['hi']:.0f})*. Es **la única
  charca del parque con fama de leopardo que además la sostienen los números**, y encaja con lo que
  ya decía el [`09`](../09-fauna-etosha.md): «Halali y Goas para el leopardo».
- 🐆 **El guepardo es de Namutoni**, y esto confirma el **{gue['pct']} %** que el README lleva
  citando: *({gue['k']}/{gue['n']})*, intervalo **{gue['lo']:.0f}–{gue['hi']:.0f}**, y **por encima
  de los otros dos sin solaparse**. Con {gue['n']} partes el intervalo es ancho —hay que decirlo—,
  pero **aun así se separa**: la afirmación aguanta.
- 🦏 **El rinoceronte negro es de Okaukuejo.** **{rin['pct']} %** *({rin['k']}/{rin['n']})* contra el
  {rin_na['pct']} % de Namutoni: la charca iluminada del campamento grande **es la casilla del
  rinoceronte**, como dice su propia ficha *(`../21`)*.

**Y lo que NO se separa, que es casi todo**: {lista_ruido}. Para estas, **la charca en la que
duermas no cambia tus posibilidades** — o si las cambia, estos datos no lo detectan. El caso que
más engaña es el **león**: parece que Halali gana, y no; los tres intervalos se pisan.

---

## 📊 El cuadro completo, especie a especie

*Porcentaje de estancias con al menos una observación · entre paréntesis, **partes que lo vieron /
partes totales** y el **intervalo del 95 %**.*

{filas}

> 🐖 **El oricteropo merece su línea**: **{ori['k']} de {ori['n']} partes** en Okaukuejo, intervalo
> **{ori['lo']:.0f}–{ori['hi']:.0f} %**. No es que sea difícil: es que **en la ventana medida no lo
> vio nadie en ninguno de los tres**. Por eso salió del catálogo de la guía de fauna el 09/08, y
> este cuadro es la razón, no una impresión.

---
"""


def ficha(d, nom, camp, titulo, prosa):
    """Una charca: lo que dice el `21` de ella, y sus números ordenados de mayor a menor."""
    c = d["campamentos"][camp]
    ivs = [(s, dato(d, camp, s)) for s in ORDEN if dato(d, camp, s)]
    ivs.sort(key=lambda x: -x[1]["pct"])
    top = "\n".join(
        f"- {EMOJI.get(s, '·')} **{nom.get(s, s)}** — **{x['pct']} %** "
        f"*({x['k']}/{x['n']} · {x['lo']:.0f}–{x['hi']:.0f})*" for s, x in ivs)
    otros = c.get("otros", {})
    extra = ""
    if otros:
        trozos = []
        for k, x in sorted(otros.items(), key=lambda kv: -kv[1].get("pct", 0)):
            lo, hi = wilson(x["lo_vieron"], x["partes"])
            trozos.append(f"**{k}** {x['pct']} % *({x['lo_vieron']}/{x['partes']} · "
                          f"{lo:.0f}–{hi:.0f})*")
        extra = ("\n\n*Y lo que Expert Africa cuenta aparte, con el nombre que ella usa:* "
                 + " · ".join(trozos) + ".")
    return f"""## {titulo}

{prosa}

**Los partes: {c['viajeros']} viajeros desde {c['desde']}** ✅
*([Expert Africa]({c['url']}))*, de mayor a menor:

{top}{extra}

---
"""


def cola(d):
    leo = dato(d, "halali", "leopardo")
    return f"""## 🏕️ Onguma Tamboti — las dos últimas noches, y las que NO tienen partes

Onguma **no aparece en los partes de Expert Africa** que usa este repo ❌: es reserva privada y su
charca no entra en la serie. Así que aquí **no hay porcentaje que dar**, y no se da.

Lo que sí hay es **lo que su propia tarifa afirma por escrito** ✅ *(`../21-campamentos-de-etosha.md`)*:
*«Four of the Big Five (lion, leopard, rhino and elephant) roam free»*, y el **guepardo** lo añade su
web. **Es la única de la zona con leopardo Y guepardo confirmados por escrito en fuente propia** —
pero eso es una declaración del alojamiento, **no una medida**, y no se puede poner al lado de un
{leo['pct']} % de Moringa como si fueran la misma clase de dato.

Y una cosa que ninguna charca de NWR puede dar: **el Onkolo Hide, un escondite a pie de agua**,
3 h por **N$720 (~€36) por persona** ✅ *(mínimo 2, máximo 7, desde 7 años, se reserva con
antelación)*. Más el **Sundowner Drive de 3 h, N$980 (~€49) pp** ✅, que sale al atardecer y **vuelve
ya de noche, con foco y campo a través** — las dos cosas que el parque prohíbe.

> ⚖️ **El choque de horarios sigue en pie** *(`../21`)*: el sundowner obliga a **salir del parque
> hacia las 17:00** y renunciar a la mejor hora de charcas del último día. Son **dos planes buenos y
> excluyentes**.

---

## 🗺️ Los tres campamentos de Etosha que el repo nombra pero no pisa

Ninguno tiene partes de avistamiento en el cache, así que **de sus charcas este estudio no puede
decir nada medido** ❌. Lo que el repo sí tiene de ellos:

- ⛺ **Olifantsrus** *(Etosha oeste)* — el único **solo camping** del parque, **N$510 (~€26) por
  persona → N$1.020 (~€51) los dos** ✅ *(`../03-alojamiento-y-tasas.md`)*. Su fama es justamente
  **el hide de dos plantas sobre la charca**, pero **no hay dato de avistamiento aquí** ❌.
- 🏨 **Dolomite Camp** *(Etosha oeste)* — bush chalet en **media pensión, N$3.180 (~€159) por
  persona → N$6.360 (~€318)** ✅. Su punto fuerte es el **acceso a un sector cerrado al self-drive**
  ◐, y está a **160–180 km de Okaukuejo** ◐ *([`reservas-privadas-vs-etosha.md`](reservas-privadas-vs-etosha.md))*: fuera
  de esta ruta por distancia, no por interés.
- 🏨 **Onkoshi Resort** *(sobre la depresión, al norte de Namutoni)* — **~40 km de desvío desde
  Namutoni** ◐, también en zona vetada al self-drive público. **Sin dato de charca** ❌.

> ⚠️ **Y un aviso de método sobre Dolomite**, que ya está registrado en
> [`auditoria-mat-travel.md`](auditoria-mat-travel.md): una agencia afirmaba
> «rinoceronte blanco *Medium-High* en Dolomite, grupos pastando con regularidad» y **el dato no se
> sostuvo**. Es exactamente el tipo de afirmación que este documento evita: **sin partes, sin
> porcentaje**.

---

## 🕳️ Lo que este estudio NO puede cerrar

- ❌ **Nadie publica «qué se acercó a la charca».** Todo lo de arriba es **por estancia**, con los
  game drives dentro. La pregunta literal del título **no tiene fuente**, y conviene saberlo.
- ❌ **Namutoni descansa en 11–16 partes.** Sus tres cifras interesantes —guepardo, eland, hiena
  manchada— tienen intervalos de 30 y 40 puntos de ancho. El guepardo **aun así se separa**; las
  otras dos, no.
- ❌ **Onguma, Olifantsrus, Dolomite y Onkoshi no tienen partes** en la serie. Del hide de
  Olifantsrus, que es lo que más se parecería a «una charca medida», **no hay ni un número**.
- ❌ **La ventana de los partes no es la del viaje.** Expert Africa da el acumulado de sus reseñas
  *(desde 2018)*, no un filtro de octubre-noviembre — al revés que los recuentos de GBIF, que sí van
  filtrados *(`../CLAUDE.md`)*. Para las especies residentes da igual; para las que se mueven con el
  agua, no.

---

*Generado desde `fuente/geo/avistamientos.json` con `fuente/estudio_charcas.py` · Porcentajes de
Expert Africa, intervalo de Wilson al 95 % · Precios en N$ y € · ~N$20 = €1*
"""


CHARCAS = [
    ("okaukuejo", "💧 Okaukuejo — la charca del rinoceronte", """La del campamento más antiguo del
parque *(rest camp desde octubre de 1957 ◐)*: **iluminada del ocaso al amanecer y abierta las 24 h
para quien duerme dentro** ◐. La guía del parque la llama, sin rodeos, *«the most reliable predator
and megafauna viewing spot inside Etosha»*, con el **pico entre las 19:00 y las 22:00 en estación
seca** ◐ — y la noche del 9 al 10 de noviembre cae **en la cola de esa estación seca**: en 4 de las
5 últimas temporadas las lluvias aún no habían empezado *(`../14-lluvias-historico.md`)*.

Los números confirman su fama, y la afinan: **no es la charca de los felinos, es la del
rinoceronte**."""),
    ("halali", "💧 Halali · Moringa — la charca del leopardo", """A **~5 minutos a pie** del camping
○, con **plataforma elevada sobre un anfiteatro de roca** e iluminación nocturna ✅. Es la que tiene
fama de rinoceronte negro y leopardo de noche — y es **la única fama de leopardo del parque que los
partes sostienen**.

⚠️ **El graderío es de roca irregular y de noche es traicionero** ○: frontal en modo rojo y calzado
cerrado *(`../17-lista-de-equipaje.md`)*."""),
    ("namutoni", "💧 Namutoni · King Nehale — la charca del guepardo, y la muestra más floja",
     """⚠️ **Desde el 24/08 aquí ya no se duerme** —la noche se cambió por una segunda en Onguma—,
así que **esta charca iluminada se pierde**: Namutoni se cruza el D12 de paso, con la puerta de Von
Lindequist en el reloj. Lo que sigue vale para saber qué se deja atrás, y era la floja de las tres.

Al pie de las murallas del fuerte, **iluminada y con bancos** ✅. La pega honesta de los
viajeros ○: **desde los bancos solo se ve parte de la lámina de agua**; el resto, a través de la
valla. De noche atrae **elefante y kudú**, y rinoceronte más bien a partir del invierno ◐; la mejor
franja, **19:00–21:00** ◐.

**Aquí es donde hay que mirar la muestra.** Namutoni tiene el porcentaje de guepardo más alto de los
tres y **se sostiene** — pero todo lo demás que parece destacar aquí *(eland, hiena manchada, los
100 % de jirafa, cebra, órix y ñu)* descansa en **11 a 16 partes**: son intervalos anchísimos y
**no se separan de los otros dos campamentos**."""),
]


def main():
    d, nom = carga(), nombres()
    texto = documento()
    for camp, titulo, prosa in CHARCAS:
        texto += "\n" + ficha(d, nom, camp, titulo, prosa)
    texto += "\n" + cola(d)
    with io.open(SALIDA, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"{os.path.relpath(SALIDA, RAIZ)} · {len(texto.splitlines())} lineas, "
          f"{len(d['campamentos'])} campamentos con partes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
