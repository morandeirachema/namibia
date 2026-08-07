# -*- coding: utf-8 -*-
"""Una sola manera de pedir por red, con reintentos y espera creciente.

Los origenes remotos del build fallan cada uno a su manera: Commons devuelve 429 con
`Retry-After`, Overpass se satura a ratos, y GBIF suelta 503 esporadicos — a veces
disfrazados de HTTP 200 con una lista JSON donde tocaba un objeto. Antes cada script
llevaba su propia copia del bucle de reintentos, y las diferencias entre copias no
eran decisiones: eran deriva. Esta es la unica implementacion, con las reglas juntas:

  · un 4xx que no sea 429 NO se reintenta — la peticion esta mal y repetirla no la
    arregla: se levanta tal cual, que el que llama vea el error de verdad;
  · un 5xx o un 429 se reintenta doblando la espera, y respetando el `Retry-After`
    si el servidor lo manda;
  · `valida`, si se pasa, examina el cuerpo: si devuelve falso o revienta, la
    respuesta cuenta como fallo y se reintenta aunque el HTTP dijera 200.

Cada script conserva un envoltorio de una linea con SU ajuste (timeout, intentos),
para que la manía de cada servidor quede escrita donde se usa.
"""
import time
import urllib.error
import urllib.request

UA = "NamibiaTripDossier/2.0 (https://github.com/chemamm/Namibia; josemorandeira@gmail.com)"


def pide(url, datos=None, timeout=120, intentos=5, cabeceras=None, valida=None):
    """GET —o POST, si hay `datos`— que devuelve el cuerpo en bytes."""
    espera = 3
    ultimo = None
    for i in range(intentos):
        try:
            req = urllib.request.Request(
                url, data=datos, headers=dict({"User-Agent": UA}, **(cabeceras or {})))
            with urllib.request.urlopen(req, timeout=timeout) as r:
                cuerpo = r.read()
            if valida is None or valida(cuerpo):
                return cuerpo
            ultimo = ValueError("la respuesta no pasa la validacion")
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 429:
                raise
            ultimo = e
            espera = int(e.headers.get("Retry-After") or espera)
        except Exception as e:                                    # noqa: BLE001
            ultimo = e
        if i < intentos - 1:
            time.sleep(espera)
            espera = max(espera * 2, 3)
    raise RuntimeError(f"sin respuesta tras {intentos} intentos: "
                       f"{url.split('?')[0]} ({ultimo})")
