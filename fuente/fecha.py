# -*- coding: utf-8 -*-
"""La fecha que imprimen los PDF en su pie, en un solo sitio.

La leen `dossier.py`, `agenda.py` y `lamina.py`, y `comprobar.py` exige que sea la misma
que declara el README en «Última actualización». Antes cada programa llevaba la suya y el
26/08 los tres PDF salieron con tres fechas distintas (21, 24 y 25 de agosto) sin que nada
avisara: solo se comprobaba la del dossier.
"""
FECHA = "25 de septiembre de 2026"

# Las fechas del viaje, de puerta a puerta: el vuelo sale el 30/10 y aterriza de vuelta el
# 15/11 (el D1 en Namibia es el 31/10 y el D15 el 14/11). La imprimen las portadas de los
# cuatro PDF y el estudio de charcas; el 25/09 la guia de fauna decia «31 oct – 14 nov» y
# el resto «30 oct – 15 nov».
VIAJE = "30 de octubre – 15 de noviembre de 2026"
VIAJE_CORTO = "30 oct – 15 nov 2026"
