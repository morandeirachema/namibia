# -*- coding: utf-8 -*-
"""Sol y luna, calculados aqui mismo: el `01` imprime quince amaneceres, quince ocasos y
una fraccion iluminada por noche, y hasta el 28/08 nada los comprobaba.

Orto y ocaso, por el algoritmo solar de la NOAA (el mismo que usa su calculadora publica),
con zenit 90,833 grados —refraccion mas semidiametro— sobre las coordenadas de
`trazado.PUNTOS`. Namibia va en UTC+2 todo el ano: no hay horario de verano desde 2017.

Fase lunar, por las series periodicas de Meeus (Astronomical Algorithms, cap. 48) truncadas
a los terminos principales, que dan la fraccion iluminada con menos de un punto de error.
El `01` la calculaba antes con «conjuncion de referencia mas mes sinodico» y se quedaba
entre 3 y 7 puntos alto en toda la fase menguante.

No pide red ni dependencias: es aritmetica.
"""
import datetime
import math

ZONA = 2.0                       # UTC+2, sin horario de verano
ZENIT = 90.833                   # refraccion atmosferica + semidiametro solar


def dia_juliano(y, m, d):
    if m <= 2:
        y, m = y - 1, m + 12
    a = y // 100
    b = 2 - a + a // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5


def _solar(jc):
    """Declinacion y ecuacion del tiempo para un siglo juliano dado."""
    gml = (280.46646 + jc * (36000.76983 + jc * 0.0003032)) % 360
    gma = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    ecc = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
    r = math.radians(gma)
    c = (math.sin(r) * (1.914602 - jc * (0.004817 + 0.000014 * jc))
         + math.sin(2 * r) * (0.019993 - 0.000101 * jc)
         + math.sin(3 * r) * 0.000289)
    sal = gml + c - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * jc))
    seo = 23 + (26 + (21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813))) / 60) / 60
    oc = seo + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * jc))
    decl = math.degrees(math.asin(math.sin(math.radians(oc)) * math.sin(math.radians(sal))))
    vy = math.tan(math.radians(oc / 2)) ** 2
    eq = 4 * math.degrees(
        vy * math.sin(2 * math.radians(gml)) - 2 * ecc * math.sin(r)
        + 4 * ecc * vy * math.sin(r) * math.cos(2 * math.radians(gml))
        - 0.5 * vy * vy * math.sin(4 * math.radians(gml))
        - 1.25 * ecc * ecc * math.sin(2 * r))
    return decl, eq


def minutos_de_sol(lat, lon, fecha, cual, zona=ZONA):
    """Minutos locales del orto (`cual='sale'`) o del ocaso (`cual='pone'`), o None si no
    hay ninguno ese dia a esa latitud."""
    jd = dia_juliano(fecha.year, fecha.month, fecha.day)
    t = 6 * 60 if cual == "sale" else 18 * 60
    for _ in range(4):                                   # converge en dos o tres vueltas
        jc = (jd + t / 1440.0 - zona / 24.0 - 2451545.0) / 36525.0
        decl, eq = _solar(jc)
        cos_h = ((math.cos(math.radians(ZENIT))
                  / (math.cos(math.radians(lat)) * math.cos(math.radians(decl))))
                 - math.tan(math.radians(lat)) * math.tan(math.radians(decl)))
        if abs(cos_h) > 1:
            return None
        ha = math.degrees(math.acos(cos_h))
        if cual == "pone":
            ha = -ha
        t = 720 - 4 * (lon + ha) - eq + zona * 60
    return t


def hhmm(minutos):
    m = int(round(minutos))
    return f"{m // 60:02d}:{m % 60:02d}"


def iluminada(fecha, hora_local=21, zona=ZONA):
    """Porcentaje del disco lunar iluminado, a una hora local dada."""
    jd = dia_juliano(fecha.year, fecha.month, fecha.day) + (hora_local - zona) / 24.0
    T = (jd - 2451545.0) / 36525.0
    D = math.radians((297.8501921 + 445267.1114034 * T - 0.0018819 * T * T) % 360)
    M = math.radians((357.5291092 + 35999.0502909 * T) % 360)
    Mp = math.radians((134.9633964 + 477198.8675055 * T + 0.0087414 * T * T) % 360)
    i = (180 - math.degrees(D)
         - 6.289 * math.sin(Mp) + 2.100 * math.sin(M)
         - 1.274 * math.sin(2 * D - Mp) - 0.658 * math.sin(2 * D)
         - 0.214 * math.sin(2 * Mp) - 0.110 * math.sin(D))
    return (1 + math.cos(math.radians(i))) / 2 * 100


if __name__ == "__main__":
    import trazado
    for e in trazado.ETAPAS:
        d, m = {"31 oct": (31, 10)}.get(e["fecha"], (int(e["fecha"].split()[0]), 11))
        fecha = datetime.date(2026, m, d)
        clave = e["duerme"] or "windhoek"
        lat, lon = trazado.PUNTOS[clave][:2]
        print(f"{e['id']:4} {fecha}  {trazado.PUNTOS[clave][2][:22]:22}  "
              f"sale {hhmm(minutos_de_sol(lat, lon, fecha, 'sale'))}  "
              f"pone {hhmm(minutos_de_sol(lat, lon, fecha, 'pone'))}  "
              f"luna {iluminada(fecha):5.1f} %")
