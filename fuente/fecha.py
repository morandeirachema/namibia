# -*- coding: utf-8 -*-
"""La fecha que imprimen los PDF en su pie, en un solo sitio.

La leen `dossier.py`, `agenda.py` y `lamina.py`, y `comprobar.py` exige que sea la misma
que declara el README en «Última actualización». Antes cada programa llevaba la suya y el
26/08 los tres PDF salieron con tres fechas distintas (21, 24 y 25 de agosto) sin que nada
avisara: solo se comprobaba la del dossier.
"""
FECHA = "28 de agosto de 2026"
