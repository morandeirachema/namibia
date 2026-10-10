# -*- coding: utf-8 -*-
"""La fecha que imprimen los PDF en su pie, en un solo sitio.

La leen `dossier.py`, `agenda.py` y `lamina.py`, y `comprobar.py` exige que sea la misma
que declara el README en «Última actualización» y que de verdad salga impresa en los tres
PDF. Antes cada programa llevaba la suya y el 26/08 los tres PDF salieron con tres fechas
distintas (21, 24 y 25 de agosto) sin que nada avisara: solo se comprobaba la del dossier.
"""
import datetime

FECHA = "10 de octubre de 2026"

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")

# Las fechas del viaje, de puerta a puerta: el vuelo sale el 30/10 y aterriza de vuelta el
# 15/11 (el D1 en Namibia es el 31/10 y el D15 el 14/11). La imprimen las portadas de los
# cuatro PDF y el estudio de charcas; el 25/09 la guia de fauna decia «31 oct – 14 nov» y
# el resto «30 oct – 15 nov». Desde el 09/10 los textos salen de estas dos fechas, y de
# aqui las lee tambien `comprobar.py`, que hasta entonces llevaba su propio 2026-10-30.
SALIDA = datetime.date(2026, 10, 30)
VUELTA = datetime.date(2026, 11, 15)
VIAJE = (f"{SALIDA.day} de {MESES[SALIDA.month - 1]} – "
         f"{VUELTA.day} de {MESES[VUELTA.month - 1]} de {VUELTA.year}")
VIAJE_CORTO = (f"{SALIDA.day} {MESES[SALIDA.month - 1][:3]} – "
               f"{VUELTA.day} {MESES[VUELTA.month - 1][:3]} {VUELTA.year}")

# Cuando se midio con OSRM la geometria de `geo/ruta.json` —el dossier lo imprime bajo la
# tabla de etapas—. ruta.json no guarda la fecha dentro, asi que va aqui, y
# `comprobar.revisa_fechas` avisa si git dice que el fichero cambio despues. Decia «8 de
# agosto» desde que se escribio, y la ruta se rehizo entera el 24/08.
RUTA_MEDIDA = datetime.date(2026, 8, 24)


def larga(d):
    """date -> «24 de agosto de 2026»."""
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def de_etapa(etapa):
    """La fecha de una etapa de `trazado.ETAPAS` («31 oct», «9 nov») como `date`.

    El año sale de la salida del viaje, y si el mes es anterior al de la salida es que el
    viaje ha cruzado de año. Falla si el mes no existe, en vez de inventarse uno.
    """
    d, m = etapa["fecha"].split()
    abrev = [x[:3] for x in MESES]
    if m not in abrev:
        raise ValueError(f"{etapa['id']}: el mes «{m}» no es una abreviatura de MESES")
    mes = abrev.index(m) + 1
    ano = SALIDA.year + (1 if mes < SALIDA.month else 0)
    return datetime.date(ano, mes, int(d))
