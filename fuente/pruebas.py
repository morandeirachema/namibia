#!/usr/bin/env python3
"""Pruebas de las funciones puras del build: lo que `make comprueba` solo ejercita de refilon.

El sol y la luna, el intervalo de Wilson, el firme por carretera, los rangos de dias, las letras
de los numeros, el titulo de cada casilla de la lista… Cada una tiene un valor que se sabe de
antemano, y si cambia, aqui se ve en segundos y con nombre; en `make comprueba` se veria como un
fallo del `01` o de un derivado, dos capas mas arriba.

    python3 fuente/pruebas.py        (o `make pruebas`; el CI lo pasa antes que `comprueba`)
"""
import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import astro                                                       # noqa: E402
import comun                                                       # noqa: E402
import estudio_charcas                                             # noqa: E402
import fecha                                                       # noqa: E402
import mapa                                                        # noqa: E402
import sin_precios                                                 # noqa: E402
import trazado                                                     # noqa: E402


class Letras(unittest.TestCase):
    def test_en_letras(self):
        self.assertEqual(comun.en_letras(0), "cero")
        self.assertEqual(comun.en_letras(21), "veintiuna")
        self.assertEqual(comun.en_letras(32), "treinta y dos")
        self.assertEqual(comun.en_letras(100), "cien")
        self.assertEqual(comun.en_letras(135), "ciento treinta y cinco")
        self.assertEqual(comun.en_letras(200), "200")       # fuera de rango: la cifra

    def test_mil(self):
        self.assertEqual(comun.mil(2728), "2.728")
        self.assertEqual(comun.mil(999), "999")

    def test_marca_texto(self):
        self.assertIn('class="marca m-si"', comun.marca_texto("✅ hola"))
        self.assertIn('class="rot">sol</span>', comun.marca_texto("☀️ amanecer"))
        self.assertNotIn("🦁", comun.marca_texto("🦁 leon"))     # decorativo: fuera
        self.assertIn("→", comun.marca_texto("A → B"))          # flecha: texto, se queda


class Calendario(unittest.TestCase):
    def test_de_etapa(self):
        self.assertEqual(fecha.de_etapa({"id": "D1", "fecha": "31 oct"}), datetime.date(2026, 10, 31))
        self.assertEqual(fecha.de_etapa({"id": "D9", "fecha": "8 nov"}), datetime.date(2026, 11, 8))
        with self.assertRaises(ValueError):
            fecha.de_etapa({"id": "Dx", "fecha": "8 xyz"})

    def test_etapas_seguidas(self):
        dias = [fecha.de_etapa(e) for e in trazado.ETAPAS]
        self.assertEqual(dias[0], fecha.SALIDA + datetime.timedelta(days=1))
        self.assertEqual(dias[-1], fecha.VUELTA - datetime.timedelta(days=1))
        self.assertEqual([(b - a).days for a, b in zip(dias, dias[1:])], [1] * (len(dias) - 1))


class SolYLuna(unittest.TestCase):
    def test_amanecer_windhoek(self):
        lat, lon = trazado.PUNTOS["windhoek"][:2]
        m = astro.minutos_de_sol(lat, lon, datetime.date(2026, 10, 31), "sale")
        self.assertEqual(astro.hhmm(m), "06:08")                 # el que imprime el `01` en el D1
        p = astro.minutos_de_sol(lat, lon, datetime.date(2026, 10, 31), "pone")
        self.assertEqual(astro.hhmm(p), "19:03")

    def test_sin_orto_en_el_polo(self):
        self.assertIsNone(astro.minutos_de_sol(89.0, 0.0, datetime.date(2026, 12, 21), "sale"))

    def test_luna(self):
        self.assertAlmostEqual(astro.iluminada(datetime.date(2026, 10, 31)), 62.3, delta=0.5)
        self.assertLess(astro.iluminada(datetime.date(2026, 11, 9)), 3)      # luna nueva del `01`
        self.assertEqual(astro.hhmm(4.6), "00:05")


class Ruta(unittest.TestCase):
    def test_firme(self):
        self.assertEqual(trazado.firme_de("B1"), "asfalto")
        self.assertEqual(trazado.firme_de("C34", lat=-22.5, lon=14.4), "asfalto")   # al sur de Henties
        self.assertEqual(trazado.firme_de("C34", lat=-21.5, lon=14.0), "sal")
        self.assertEqual(trazado.firme_de("C40", lat=-19.6, lon=14.5), "grava")     # al oeste de Kamanjab
        self.assertEqual(trazado.firme_de("C40", lat=-19.9, lon=15.5), "asfalto")
        self.assertEqual(trazado.firme_de("", lat=-19.2, lon=16.0), "parque")       # Etosha, sin ref
        self.assertEqual(trazado.firme_de("", nombre="Sossusvlei Road"), "asfalto")
        self.assertIsNone(trazado.firme_de("Z99"))                                  # nunca se inventa

    def test_dias_del_punto(self):
        self.assertEqual(trazado.dias_del_punto("sesriem"), ["D3", "D4", "D5"])
        self.assertEqual(trazado.dias_del_punto("deadvlei"), ["D4"])               # solo por A_MANO
        self.assertEqual(trazado.dias_del_punto("ccf"), [])                        # de la variante
        self.assertEqual(trazado.dias_del_punto("ccf", trazado.ETAPAS_ALT), ["D13", "D14"])

    def test_dias_derivados(self):
        self.assertEqual(trazado.dia_de_arena(), "D4")
        self.assertEqual(trazado.dias_de_safari(), ["D11", "D12", "D13"])
        self.assertEqual(trazado.dias_texto(), "15 días")
        self.assertEqual(len(trazado.noches()), 14)

    def test_gasolineras_y_clases(self):
        self.assertEqual(trazado.PUNTOS["solitaire"][3], "combu")
        self.assertEqual(trazado.CLASE_BASE["solitaire"], "ciudad")
        self.assertNotIn("ccf", trazado.puntos_oficiales())

    def test_color_kml(self):
        self.assertEqual(trazado.color_kml("#C2542F"), "ff2f54c2")

    def test_dias_seguidos(self):
        self.assertEqual(mapa._dias_seguidos(["D2", "D3", "D4", "D7"]), "D2–D4 · D7")
        self.assertEqual(mapa._dias_seguidos(["D5"]), "D5")


class Charcas(unittest.TestCase):
    def test_wilson(self):
        lo, hi = estudio_charcas.wilson(0, 16)
        self.assertEqual(lo, 0.0)
        self.assertTrue(19 < hi < 20)
        lo, hi = estudio_charcas.wilson(12, 39)                   # el leopardo de Moringa
        self.assertTrue(18 < lo < 19 and 46 < hi < 48)
        self.assertEqual(estudio_charcas.wilson(0, 0), (0.0, 100.0))


class Textos(unittest.TestCase):
    def test_hm(self):
        import agenda
        import comprobar
        self.assertEqual(comprobar._hm(4.995), "5h00")            # no «4h60»
        self.assertEqual(agenda.hm(4.995), "5 h 00")
        self.assertEqual(agenda.hm(2.5), "2 h 30")

    def test_titulo_de_casilla(self):
        import lista_web
        t, d = lista_web.parte_titulo("**Pasaporte** ×1 p.p. — válido hasta el 2027")
        self.assertEqual((t, d), ("**Pasaporte** ×1 p.p.", "válido hasta el 2027"))
        t, d = lista_web.parte_titulo("Billetes de avión impresos ×1 p.p.")
        self.assertEqual((t, d), ("Billetes de avión impresos ×1 p.p.", ""))
        self.assertEqual(lista_web.slug("Camisetas transpirables ×5"), "camisetas-transpirables-5")


class SinPrecios(unittest.TestCase):
    """El filtro de la guia de viaje: quita el trozo con precio o reserva y deja el resto."""

    def limpia(self, md_texto):
        return sin_precios.limpia(comun.md.render(md_texto)).strip()

    def test_corta_dentro_de_la_frase(self):
        h = self.limpia("- **Spreetshoogte Campsite — RESERVADO ✅ (24/08), UNA noche** — lo opera "
                        "**Barkhan**: **N$290 (~€14,50) por persona**, parcela «stand only», wifi "
                        "gratis. Se reservó en **bookings@barkhan.africa**")
        self.assertIn("Spreetshoogte Campsite, UNA noche", h)
        self.assertNotIn("N$", h)
        self.assertNotIn("€", h)
        self.assertNotIn("serv", h.lower().replace("servicio", ""))

    def test_la_lista_tras_el_precio_se_queda(self):
        h = self.limpia("- 💱 **~10:15 · dinero y SIM** — cajeros de FNB y Bank Windhoek ✅: "
                        "**N$500–1.000 (~€25–50) de bolsillo** — y la **SIM de MTC**")
        self.assertIn("cajeros de FNB y Bank Windhoek", h)
        self.assertIn("SIM de MTC", h)
        self.assertNotIn("bolsillo", h)

    def test_la_etiqueta_queda_cerrada(self):
        h = self.limpia("Aquí la **carga de efectivo (~N$6.000 · ~€300)**, en cajero.")
        self.assertEqual(h.count("<strong>"), h.count("</strong>"))
        self.assertIn("carga de efectivo", h)

    def test_lo_que_no_es_reserva_se_queda(self):
        for texto in ("Onguma es una reserva privada de 35.970 ha.",
                      "La garrafa es la reserva de avería.",
                      "Hace falta reserva confirmada de Terrace Bay para entrar."):
            self.assertFalse(sin_precios.hay_precio(texto), texto)
        self.assertTrue(sin_precios.hay_precio("Camping Halali — RESERVADO el 21/08"))
        self.assertTrue(sin_precios.hay_precio("la Tarifa de noviembre"))

    def test_bloque_solo_de_precio_desaparece(self):
        self.assertEqual(self.limpia("- 🎫 Namib-Naukluft ~N$620 (~€31)/24 h"), "")

    def test_lo_que_parece_dinero_y_no_lo_es_se_queda(self):
        # Lo que el 18/10 se llevó por delante: reglas del terreno y el nombre de una ficha.
        for texto in ("No pagar nunca una «multa» en mano en un control.",
                      "No perder de vista la tarjeta al pagar.",
                      "La regla barata: a nadie de uniforme, a ninguna verja con garita.",
                      "Cobra escupidora cebra · Zebra spitting cobra",
                      "Presupuesta 130–150 km de combustible para el día.",
                      "Su reserva declara 34.000 ha con fauna libre."):
            self.assertFalse(sin_precios.hay_precio(texto), texto)
        for texto in ("se pagan N$650 por persona", "lo cobra NWR", "sale más barato que el lodge",
                      "en Booking.com", "Cancelación gratuita hasta 48 h", "el pago del 20 %"):
            self.assertTrue(sin_precios.hay_precio(texto), texto)

    def test_mermaid(self):
        m = sin_precios.limpia_mermaid('    B --> C["13:00<br/>comida<br/>los ultimos N$"]')
        self.assertEqual(m, '    B --> C["13:00<br/>comida"]')


if __name__ == "__main__":
    unittest.main(verbosity=1)
