# -*- coding: utf-8 -*-
"""Quita del HTML los precios y las reservas, frase a frase: lo usa la guía de viaje.

La guía de viaje (`guia_viaje.py`) es el dossier que se lleva en la mano en Namibia, y en
la mano no pinta lo que cuesta cada cosa ni el estado de cada reserva. Esos datos viven
cosidos a la prosa del `01`, del `21`, del `07`… —«Camping Halali — N$920 (~€46) los dos ✅
— RESERVADO el 21/08»—, así que no basta con quitar secciones: hay que cortar dentro de la
frase. Nada de esto se escribe a mano: es el mismo markdown, recortado.

Cómo corta, de lo fino a lo grueso:

  1 · los PARÉNTESIS y los INCISOS entre rayas («—…—») que lleven un precio, una reserva,
      una remisión a un documento que la guía no lleva o una fecha de trabajo del dossier
      («(decidido 08/08)», «(OSRM 128,8)»): fuera enteros, de dentro afuera;
  2 · lo que aún lleve precio o reserva se parte por niveles —frase, «;», raya, «:», «·»,
      coma— y se quita SOLO el trozo que lo lleva. «Spreetshoogte Campsite — RESERVADO ✅,
      UNA noche — lo opera Barkhan: N$580 los dos, parcela «stand only», wifi gratis» sale
      «Spreetshoogte Campsite — UNA noche — lo opera Barkhan: parcela «stand only», wifi
      gratis».

Solo se borra TEXTO: las etiquetas se quedan donde estaban, así que el HTML no puede
quedar desparejado —una negrita que empezaba en el trozo borrado sigue cerrándose—; al
final se barren las etiquetas que se han quedado vacías y los bloques sin nada dentro.
Los diagramas de Mermaid van aparte (`limpia_mermaid`): ahí se quita la línea de la
etiqueta —lo que va entre `<br/>`— que lleve el precio.
"""
import html as _html
import re

# Lo que cuenta como precio. «cuesta» no entra a propósito: «ir y volver cuesta dos horas».
PRECIO = re.compile(
    r"N\$|€|\bEUR\b|\beuros?\b|US\$|\bUSD\b|\bZAR\b|«desde R\d|\bR\d{3,}\b"
    r"|\btarifas?\b|\btarifario\b|\b(?:sobre)?precios?\b|\bcostes?\b|\bimportes?\b|\bpresupuest\w*"
    r"|\bpag(?:o|os|ar|ado|ada|ados|adas|ando|arla|arlo|ará|an)\b|\bcobr(?:a|an|ar|ará|o)\b"
    r"|\bIVA\b|\bLevy\b|\brack\b|\bdepósito del \d|\bm[áa]s car[oa]s?\b|\bbarat[oa]s?\b"
    r"|\bcuestan? (?:más|menos|casi|el doble|el triple|lo mismo)\b|\blo que cuestan?\b",
    re.I)

# Lo que cuenta como reserva —la de alojamiento o actividad, no la natural—. Quedan fuera
# la «reserva privada» de Onguma, la «Nature Reserve», el agua y el efectivo «de reserva»,
# el gasoil «en reserva» y la «reserva con fauna libre».
RESERVA = re.compile(
    r"(?<!\ben )\b[Rr]eserv(?!e\b)"
    r"(?!as?\s+(?:privad|natural|de avería|de efectivo|de agua|limitada|con fauna|valladas))"
    r"(?!a\s+baje)\w*"
    r"|\bRESERV\w*|\bbookings?\b|\bse cancela\b|\bcancel(?:ar\w*|aci[óo]n\w*|ad[oa]s?)\b"
    r"|\bvenc(?:e|ía|ió|en)\b|\bsin cerrar\b|\bconfirm(?:ad[oa]s?|ar|arlo|arla)? por escrito\b"
    r"|\banular\b|\bpospon\w*|\bPOSPON\w*")

# Lo que SÍ se queda aunque nombre una reserva, porque es una regla del terreno y no el
# estado de un trámite: en Ugabmund no se entra a dormir sin la de Terrace Bay en la mano.
CONSERVA = re.compile(r"reserva\s+confirmada\s+de\s+Terrace\s+Bay|confirmación\s+impresa")

# La historia de las reservas contada en el día: «las fechas bajan un día respecto al plan de
# agosto», «el reloj ya corrió». En la guantera confunde: la fecha buena es la del encabezado.
HISTORIA = re.compile(r"\bplan de agosto\b|\bfechas? bajan? un día\b|\breloj ya corrió\b")

# Lo que remite a un sitio que la guía no lleva: un documento que se queda fuera (se marca
# con este testigo antes de filtrar) o el material de trabajo de `aparte/`.
TESTIGO = "⟦ref⟧"
FUERA_DEL_LIBRO = re.compile(re.escape(TESTIGO) + r"|aparte/|\bREADME\b")

# PRECIO no distingue mayusculas («Tarifa», «PRECIO»); RESERVA si, para no tocar «Reserve».
DURO = re.compile(f"(?i:{PRECIO.pattern})|{RESERVA.pattern}|{FUERA_DEL_LIBRO.pattern}"
                  f"|{HISTORIA.pattern}")

# El sello de estado que acompaña al nombre del sitio —«Urban Camp — RESERVADO ✅»— se va
# solo, sin llevarse la frase: lo que cuelga detras («(Schanzen Road; piscina, bar…)») es
# del sitio, no de la reserva.
ESTADOS = [
    re.compile(r"\s*[—–]\s*RESERVAD[OA]S?\b(?:\s+(?:una|dos)\s+noches?)?"
               r"(?:\s+el\s+\d{1,2}/\d{1,2})?(?:\s*[✅❌◐○])?"),
    re.compile(r"\bRESERVAD[OA]S?\b(?:\s+(?:una|dos)\s+noches?)?"
               r"(?:\s+el\s+\d{1,2}/\d{1,2})?(?:\s*[✅❌◐○])?\s*(?:[—–]\s*)?"),
]

# Solo en paréntesis e incisos: la historia del dossier («(decidido 08/08)», «(OSRM 128,8)»,
# «(corregido el 28/08 — …)»). Fuera de un paréntesis estas palabras pueden ser el dato.
BLANDO = re.compile(
    r"\b\d{1,2}/\d{1,2}\b|^\W*(?:OSRM|decidido|act\.|el análisis|detalle en|cálculo|adelantado|"
    r"rehecho|verificado|confirmado|añadido|[Cc]orregido|matizado|destapado|avance del|"
    r"investigado|ampliado|cerrado el|precisado)\b|\bplan (?:de agosto|anterior)\b")

# Los niveles de corte, de lo grueso a lo fino. La frase acaba en punto seguido de algo
# que no empieza en minúscula; «p. ej.» o «8. Grúa» no son finales de frase.
NIVELES = [
    re.compile(r"(?<=[.!?…])\s+(?=[^\sa-záéíóúñ])"),
    re.compile(r";\s+"),
    re.compile(r"\s+[—–]\s+"),
    re.compile(r":\s+"),
    re.compile(r"\s+·\s+"),
    re.compile(r",\s+"),
]
ABREVIATURAS = {"p", "ej", "aprox", "pp", "p.p", "sr", "dr", "st", "núm", "n", "vs", "mt", "c",
                "s", "km", "min", "h", "art", "reg", "pág", "ca"}

# Lo que se borra del borde de un bloque cuando lo de al lado se ha ido.
SEPARADORES = set(" \t\n,;:·—–")


def _tiene_letra(t):
    return re.search(r"[0-9A-Za-zÁÉÍÓÚÑáéíóúñüÜ]", t) is not None


def hay_precio(texto):
    """¿Queda en este texto algo de lo que la guía no lleva? Lo que casa con CONSERVA no cuenta."""
    return DURO.search(CONSERVA.sub(lambda m: "·" * len(m.group(0)), texto)) is not None


def _palabras(t):
    return len(re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñü]{2,}", t))


# ---------------------------------------------------------------------------
# Un tramo de texto en línea: caracteres vivos o muertos, y las etiquetas aparte
# ---------------------------------------------------------------------------

class _Tramo:
    """Los caracteres de un bloque (un <p>, un <li>, un <h3>…) con sus etiquetas.

    `F` es el texto plano, sin etiquetas y con las entidades ya resueltas; `vivo[i]` dice
    si el caracter i sigue. Las etiquetas no se borran nunca: se guardan con el indice del
    caracter delante del que iban.
    """

    def __init__(self, trozos):
        self.F, self.etiquetas = [], []
        for es_etiqueta, s in trozos:
            if es_etiqueta:
                self.etiquetas.append((len(self.F), s))
            else:
                self.F.extend(_html.unescape(s))
        self.F = "".join(self.F)
        self.vivo = [True] * len(self.F)

    def texto(self, a, b):
        return "".join(self.F[i] for i in range(a, b) if self.vivo[i])

    def vivos(self, a, b):
        return [i for i in range(a, b) if self.vivo[i]]

    def borra(self, a, b):
        for i in range(a, b):
            self.vivo[i] = False

    def html(self):
        out, j = [], 0
        etiquetas = self.etiquetas
        for i, c in enumerate(self.F):
            while j < len(etiquetas) and etiquetas[j][0] == i:
                out.append(etiquetas[j][1])
                j += 1
            if self.vivo[i]:
                out.append(_html.escape(c, quote=False))
        out.extend(s for _, s in etiquetas[j:])
        return "".join(out)


def _parejas(F):
    """Los paréntesis y los incisos entre rayas, como (abre, cierra), de dentro afuera."""
    pares, pila = [], []
    for i, c in enumerate(F):
        if c == "(":
            pila.append(i)
        elif c == ")" and pila:
            pares.append((pila.pop(), i))
    # un inciso abre con raya tras espacio y pegada a lo que sigue, y cierra pegada a lo de
    # antes y seguida de espacio o puntuacion: «el campamento —el D10 en Okaukuejo— y…»
    abierta = None
    for i, c in enumerate(F):
        if c != "—":
            continue
        antes = F[i - 1] if i else " "
        despues = F[i + 1] if i + 1 < len(F) else " "
        if antes.isspace() and not despues.isspace():
            abierta = i
        elif abierta is not None and not antes.isspace() and (despues.isspace()
                                                             or despues in ".,;:)»"):
            pares.append((abierta, i))
            abierta = None
    return sorted(pares, key=lambda p: p[1] - p[0])


def _parte(t, a, b, nivel):
    """Los trozos de [a, b) por el separador del nivel, fuera de paréntesis.

    Devuelve [(ini_separador, ini_trozo, fin_trozo)]: el separador va delante de su trozo.
    """
    idx = t.vivos(a, b)
    vivo = "".join(t.F[i] for i in idx)
    hondo, prof = [0] * len(vivo), 0
    for k, c in enumerate(vivo):
        if c == "(":
            prof += 1
        hondo[k] = prof
        if c == ")" and prof:
            prof -= 1
    cortes = []
    for m in NIVELES[nivel].finditer(vivo):
        if hondo[m.start()] or m.start() == 0 or m.end() >= len(vivo):
            continue
        if nivel == 0:
            previa = re.search(r"([\w.]+)[.!?…]$", vivo[:m.start()])
            if previa and previa.group(1).lower().rstrip(".") in ABREVIATURAS:
                continue
            palabras = vivo[:m.start()].split()
            if len(palabras) == 1 and not _tiene_letra(palabras[0]):
                continue                              # «8. Grúa y rescate»: es un numero
        cortes.append((idx[m.start()], idx[m.end() - 1] + 1))
    trozos, ini_sep, ini = [], a, a
    for s, e in cortes:
        trozos.append((ini_sep, ini, s))
        ini_sep, ini = s, e
    trozos.append((ini_sep, ini, b))
    return trozos


def _poda(t, a, b, nivel):
    """Quita de [a, b) los trozos con precio o reserva, bajando de nivel solo donde hace falta."""
    if not hay_precio(t.texto(a, b)):
        return
    if nivel >= len(NIVELES):
        t.borra(a, b)
        return
    trozos = _parte(t, a, b, nivel)
    if len(trozos) == 1:
        _poda(t, a, b, nivel + 1)
        return
    final = t.vivos(a, b)
    final = final[-1] if final else None
    for _sep, ini, fin in trozos:
        _poda(t, ini, fin, nivel + 1)
    muertos = [not _tiene_letra(t.texto(ini, fin)) for _s, ini, fin in trozos]
    # lo que va detras de dos puntos o de una coma cuelga de lo de delante: sin la cabeza
    # no se entiende («Reservado, pero el pago no consta: ni el 20 % ni el integro»;
    # «Cape Cross cobra entrada, aparte del permiso de Skeleton Coast»)
    cuelga = NIVELES[nivel].pattern in (r";\s+", r"\s+[—–]\s+", r":\s+", r",\s+")
    if all(muertos) or (cuelga and muertos[0]):
        t.borra(a, b)
        return
    # y lo que se queda solo y corto al lado de lo quitado no dice nada: «para vuestras
    # fechas — 📞 …», «— súmalo». Si lleva una cifra (un telefono, una hora) se queda.
    # (el «·» no: separa atributos —«Sundowner Drive · 3 h · N$980»— y el nombre se queda)
    if nivel >= 2 and NIVELES[nivel].pattern != r"\s+·\s+" and any(muertos):
        for k, (_s, ini, fin) in enumerate(trozos):
            resto = t.texto(ini, fin)
            if not muertos[k] and _palabras(resto) < 4 and not re.search(r"\d", resto):
                muertos[k] = True
        if all(muertos) or (cuelga and muertos[0]):
            t.borra(a, b)
            return
    for k, (sep, ini, fin) in enumerate(trozos):
        if not muertos[k]:
            continue
        t.borra(ini, fin)
        if k > 0:
            t.borra(sep, ini)                         # el separador de delante
        else:
            sig = next(j for j in range(1, len(trozos)) if not muertos[j])
            t.borra(trozos[sig][0], trozos[sig][1])   # el de detrás: el siguiente abre
    # si el ultimo trozo se fue con el punto final, el punto vuelve
    if final is not None and t.F[final] in ".!?" and not t.vivo[final]:
        t.vivo[final] = True


# Las colas que deja la historia del dossier al irse su paréntesis o su remisión:
# «descansados — decidido», «— el detalle», «, con las fechas nuevas».
COLAS = [
    re.compile(r"\s*[—–]\s*decidid[oa](?:\s+el\s+\d{1,2}/\d{1,2})?(?=\s*(?:$|[.;:]))"),
    re.compile(r"\s*[—–,]\s*(?:el|con el) detalle(?=\s*(?:$|[.;:]))"),
    re.compile(r",?\s*con las fechas nuevas(?=\s*(?:$|[.;:]))"),
    # un aviso que se ha quedado sin lo que avisaba: «reanálisis ERA5 ⚠️.»
    re.compile(r"\s*(?:⚠️|⚠)(?=\s*(?:$|[.;:,)]))"),
]


def _quita_estados(t):
    for patron in ESTADOS + COLAS:
        idx = t.vivos(0, len(t.F))
        vivo = "".join(t.F[i] for i in idx)
        for m in reversed(list(patron.finditer(vivo))):
            for k in range(m.start(), m.end()):
                t.vivo[idx[k]] = False


def _repasa_bordes(t):
    """Lo que queda colgando al principio o al final del bloque: «, », « — », «: »."""
    idx = [i for i in range(len(t.F)) if t.vivo[i]]
    for i in idx:
        if t.F[i] in SEPARADORES:
            t.vivo[i] = False
        else:
            break
    for i in reversed(idx):
        if t.F[i] in SEPARADORES:
            t.vivo[i] = False
        else:
            break
    # dos separadores seguidos («X — , Y»): se queda el primero
    idx = [i for i in range(len(t.F)) if t.vivo[i]]
    previo = None
    for i in idx:
        c = t.F[i]
        if c in ",;:·—–":
            if previo is not None:
                t.vivo[i] = False
                continue
            previo = i
        elif not c.isspace():
            previo = None


def limpia_tramo(trozos):
    """Filtra un bloque en línea. `trozos` es [(es_etiqueta, texto)]. Devuelve HTML."""
    t = _Tramo(trozos)
    if not t.F.strip():
        return t.html()
    # las listas de fuentes («Fuentes: namibian.org — subida de tasas · …») son del dossier
    if re.match(r"\W*Fuentes?\s*:", t.F):
        return ""
    for a, b in _parejas(t.F):
        dentro = t.texto(a + 1, b)
        if not t.vivo[a] or not t.vivo[b]:
            continue
        if hay_precio(dentro) or BLANDO.search(dentro):
            t.borra(a, b + 1)
    _quita_estados(t)
    _poda(t, 0, len(t.F), 0)
    _quita_estados(t)
    if not _tiene_letra(t.texto(0, len(t.F))):
        t.borra(0, len(t.F))
        return ""
    _repasa_bordes(t)
    return t.html()


# ---------------------------------------------------------------------------
# El documento entero
# ---------------------------------------------------------------------------

BLOQUE = {"p", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "div",
          "section", "figure", "figcaption", "hr", "pre", "dl", "dt", "dd", "table", "tr",
          "td", "th", "article", "header"}
RE_ETIQUETA = re.compile(r"<(/?)([a-zA-Z0-9]+)[^>]*>")
RE_MERMAID = re.compile(r'(<pre class="mermaid[^"]*">)(.*?)(</pre>)', re.S)
# Los mapas van en SVG en linea: sus rotulos son <text> y no se tocan.
RE_SVG = re.compile(r"<svg\b.*?</svg>", re.S)
RE_INTOCABLE = re.compile(RE_MERMAID.pattern + "|" + RE_SVG.pattern, re.S)


def limpia_mermaid(codigo):
    """En un diagrama, fuera la línea de etiqueta que lleve precio o reserva.

    Las etiquetas de los nodos van partidas en líneas con `<br/>`: se quita la que lo
    lleva y, si el nodo se queda sin nada, la línea entera del diagrama.
    """
    def etiqueta(m):
        partes = [p for p in re.split(r"<br\s*/?>", m.group(2)) if not hay_precio(p)]
        return m.group(1) + "<br/>".join(partes or ["…"]) + m.group(3)

    salida = []
    for ln in codigo.split("\n"):
        if hay_precio(ln):
            # la etiqueta va entre comillas, en la definicion del nodo o en una arista
            # («B --> C["13:00-16:30<br/>comida y gastar<br/>los ultimos N$"]»)
            ln = re.sub(r'([\[\(\{]+")(.*?)("[\]\)\}]+)', etiqueta, ln)
            if hay_precio(ln):
                continue
        salida.append(ln)
    return "\n".join(salida)


def _limpia_bloques(h):
    pos, salida, linea = 0, [], []

    def vacia():
        if linea:
            salida.append(limpia_tramo(linea))
            linea.clear()

    for m in RE_ETIQUETA.finditer(h):
        if m.start() > pos:
            linea.append((False, h[pos:m.start()]))
        if m.group(2).lower() in BLOQUE:
            vacia()
            salida.append(m.group(0))
        else:
            linea.append((True, m.group(0)))
        pos = m.end()
    if pos < len(h):
        linea.append((False, h[pos:]))
    vacia()
    return "".join(salida)


VACIOS = [
    r"<(strong|em|b|i|code|a|s|del|small|mark)(?:\s[^>]*)?>\s*</\1>",
    r"<li>\s*</li>", r"<p>\s*</p>", r"<blockquote>\s*</blockquote>",
    r"<(ul|ol)(?:\s[^>]*)?>\s*</\1>", r"<h([1-6])(?:\s[^>]*)?>\s*</h\1>",
    r"<li>\s*(?:<p>\s*</p>\s*)+</li>",
    # los rotulos y avisos de `comun.marca_texto` que se han quedado sin su frase
    r'<span class="(?:rot|et [^"]*)">\s*</span>',
]


def _barre(h):
    previo = None
    while previo != h:
        previo = h
        # un <li> que se ha quedado sin texto propio y solo lleva su sublista: la sublista
        # sube un nivel en vez de colgar de una viñeta vacía
        h = re.sub(r"<li>\s*<(ul|ol)>((?:(?!<(?:ul|ol)>).)*?)</\1>\s*</li>", r"\2", h, flags=re.S)
        for p in VACIOS:
            h = re.sub(p, "", h)
        h = re.sub(r"\(\s*\)", "", h)
        h = re.sub(r"(?<!\.)\.\.(?!\.)", ".", h)
        h = re.sub(r"[ \t]{2,}", " ", h)
        h = re.sub(r" +([,.;:)»])", r"\1", h)
        h = re.sub(r"([(«]) +", r"\1", h)
    return h


def _sin_titulos_huerfanos(h):
    """Fuera los encabezados que se han quedado sin nada debajo hasta el siguiente de su nivel."""
    while True:
        heads = list(re.finditer(r"<h([1-6])(?:\s[^>]*)?>.*?</h\1>", h, re.S))
        quita = None
        for k, m in enumerate(heads):
            nivel = int(m.group(1))
            fin = len(h)
            for n in heads[k + 1:]:
                if int(n.group(1)) <= nivel:
                    fin = n.start()
                    break
            cuerpo = h[m.end():fin]
            sin_tags = re.sub(r"<[^>]+>", "", cuerpo)
            if not sin_tags.strip() and not re.search(r"<(pre|img|svg|figure)\b", cuerpo):
                quita = m
                break
        if not quita:
            return h
        h = h[:quita.start()] + h[quita.end():]


def limpia(h):
    """El HTML de un documento, sin precios ni reservas. Los Mermaid aparte, y los SVG intactos."""
    piezas, pos, salida = [], 0, []
    for m in RE_INTOCABLE.finditer(h):
        piezas.append((False, h[pos:m.start()]))
        piezas.append((True, m))
        pos = m.end()
    piezas.append((False, h[pos:]))
    for aparte, p in piezas:
        if not aparte:
            salida.append(_barre(_limpia_bloques(p)))
        elif p.group(1):
            salida.append(p.group(1) + limpia_mermaid(p.group(2)) + p.group(3))
        else:
            salida.append(p.group(0))
    return _sin_titulos_huerfanos("".join(salida))


def restos(h):
    """Lo que aún huele a precio o a reserva en un HTML ya limpio: [(contexto)]. Para avisar."""
    texto = _html.unescape(re.sub(r"<[^>]+>", " ", RE_SVG.sub(" ", h)))
    texto = CONSERVA.sub(lambda m: "·" * len(m.group(0)), texto)
    return [texto[max(0, m.start() - 50):m.end() + 50].replace("\n", " ")
            for m in DURO.finditer(texto)]
