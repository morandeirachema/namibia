#!/usr/bin/env python3
"""Imprime un HTML a PDF con Chrome, hablando su protocolo de depuracion (CDP).

Por que no `chrome --print-to-pdf`: esa opcion no deja poner encabezado ni pie, asi
que el PDF sale SIN NUMEROS DE PAGINA — inaceptable en un documento de cien paginas
pensado para imprimir y llevar encima. `Page.printToPDF` por CDP si los admite.

Por que no WeasyPrint, que si sabe numerar: no ejecuta JavaScript, y los diagramas del
dossier los pinta Mermaid en el navegador.

El cliente WebSocket va aqui a mano, con la biblioteca estandar: son cuarenta lineas y
evita meter una dependencia en un repo que por lo demas solo necesita Python.

Uso:  python3 fuente/imprimir.py entrada.html salida.pdf [--titulo "..."] [--espera 6]
"""
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser", "chrome")
               if shutil.which(c)), None)


# ---------------------------------------------------------------------------
# WebSocket minimo (solo cliente, solo texto, sin extensiones)
# ---------------------------------------------------------------------------

class WS:
    def __init__(self, url):
        m = re.match(r"ws://([^:/]+):(\d+)(/.*)", url)
        host, puerto, ruta = m.group(1), int(m.group(2)), m.group(3)
        self.s = socket.create_connection((host, puerto), timeout=180)
        clave = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(
            f"GET {ruta} HTTP/1.1\r\nHost: {host}:{puerto}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {clave}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n".encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.s.recv(4096)
        if b" 101 " not in resp.split(b"\r\n")[0]:
            raise RuntimeError(f"el navegador no acepto el WebSocket: {resp[:120]!r}")
        self.resto = resp.split(b"\r\n\r\n", 1)[1]

    def _lee(self, n):
        while len(self.resto) < n:
            trozo = self.s.recv(max(65536, n - len(self.resto)))
            if not trozo:
                raise ConnectionError("el navegador cerro la conexion")
            self.resto += trozo
        salida, self.resto = self.resto[:n], self.resto[n:]
        return salida

    def envia(self, obj):
        carga = json.dumps(obj).encode()
        cab = bytearray([0x81])                      # FIN + opcode texto
        n = len(carga)
        if n < 126:
            cab.append(0x80 | n)
        elif n < 65536:
            cab.append(0x80 | 126)
            cab += struct.pack(">H", n)
        else:
            cab.append(0x80 | 127)
            cab += struct.pack(">Q", n)
        mascara = os.urandom(4)
        cab += mascara
        self.s.sendall(bytes(cab) + bytes(b ^ mascara[i % 4] for i, b in enumerate(carga)))

    def recibe(self):
        """Devuelve el siguiente mensaje completo, reensamblando fragmentos."""
        partes = []
        while True:
            b1, b2 = self._lee(2)
            fin, opcode = b1 & 0x80, b1 & 0x0F
            n = b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._lee(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._lee(8))[0]
            carga = self._lee(n)
            if opcode == 0x9:                        # ping -> pong
                self.s.sendall(b"\x8a\x80" + os.urandom(4))
                continue
            if opcode == 0x8:
                raise ConnectionError("el navegador cerro la sesion")
            partes.append(carga)
            if fin:
                return json.loads(b"".join(partes))

    def cierra(self):
        try:
            self.s.close()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Sesion de Chrome
# ---------------------------------------------------------------------------

class Navegador:
    def __init__(self, puerto=None):
        if not CHROME:
            raise RuntimeError("no encuentro Chrome ni Chromium en el PATH")
        self.puerto = puerto or _puerto_libre()
        self.perfil = tempfile.mkdtemp(prefix="namibia-chrome-")
        self.proc = subprocess.Popen(
            [CHROME, "--headless=new", f"--remote-debugging-port={self.puerto}",
             f"--user-data-dir={self.perfil}", "--disable-gpu", "--no-sandbox",
             "--no-first-run", "--disable-extensions", "--hide-scrollbars",
             "--allow-file-access-from-files", "--font-render-hinting=none",
             "--disable-lcd-text", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.base = f"http://127.0.0.1:{self.puerto}"
        self._espera_arranque()

    def _espera_arranque(self, limite=40):
        for _ in range(limite * 5):
            try:
                urllib.request.urlopen(self.base + "/json/version", timeout=2).read()
                return
            except Exception:                                     # noqa: BLE001
                if self.proc.poll() is not None:
                    raise RuntimeError("Chrome se cerro nada mas arrancar")
                time.sleep(0.2)
        raise TimeoutError("Chrome no abrio el puerto de depuracion")

    def pestana(self):
        """Se reutiliza la pestana con la que arranca Chrome: /json/new exige PUT en
        las versiones nuevas y no merece la pena depender de eso."""
        for _ in range(50):
            d = json.load(urllib.request.urlopen(self.base + "/json/list", timeout=20))
            for t in d:
                if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                    return t["webSocketDebuggerUrl"]
            time.sleep(0.2)
        raise RuntimeError("Chrome no expone ninguna pestana")

    def cierra(self):
        try:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        except Exception:                                         # noqa: BLE001
            self.proc.kill()
        shutil.rmtree(self.perfil, ignore_errors=True)


def _puerto_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# El pie de pagina
# ---------------------------------------------------------------------------

PIE = """
<style>
  #pie {{ font-family: Georgia, 'Times New Roman', serif; width: 100%;
      font-size: 8px; color: #7D776E; padding: 0 12mm; -webkit-print-color-adjust: exact; }}
  #pie .fila {{ display: flex; align-items: baseline; justify-content: space-between;
           border-top: .5px solid #C6C4BB; padding-top: 3px; width: 100%; }}
  #pie .obra {{ letter-spacing: .06em; text-transform: uppercase; font-size: 7px; }}
  #pie .num {{ font-weight: 700; color: #16130F; font-size: 9px; }}
</style>
<div id="pie"><div class="fila">
  <span class="obra">{izquierda}</span>
  <span class="num"><span class="pageNumber"></span></span>
  <span class="obra">{derecha}</span>
</div></div>
"""

VACIO = '<div style="height:0"></div>'


def _pie(izquierda, derecha):
    return PIE.format(izquierda=izquierda, derecha=derecha)


# Tamanos de papel en pulgadas, que es lo que pide printToPDF.
PAPEL = {"A4": (8.27, 11.69), "A3": (11.69, 16.54), "A2": (16.54, 23.39)}


def a_pdf(html, salida, izquierda="Namibia 2026", derecha="", espera=8.0,
          margenes=(14, 12, 16, 12), escala=1.0, papel="A4"):
    """Renderiza `html` (ruta local) a `salida` (PDF). Margenes en mm: arriba, der, abajo, izq.

    `papel` es una clave de PAPEL o una tupla (ancho, alto) en pulgadas. El dossier y la
    guia van en A4; la lamina de ruta, en A2.

    El pie va en TODAS las paginas, tambien en la portada y en los separadores. No es
    pereza: cualquier intento de imprimirlas sin pie —plantilla vacia, `visibility:
    hidden` o tinta transparente— hace que Chrome recalcule la caja de pagina y esas
    secciones salen a dos tercios de su alto. Como las paginas de imagen van
    enmarcadas dentro del margen, el pie cae en el blanco de abajo y no pisa la foto.
    """
    nav = Navegador()
    ws = None
    try:
        url = "file://" + urllib.parse.quote(os.path.abspath(html))
        ws = WS(nav.pestana())
        ident = [0]

        def manda(metodo, **params):
            ident[0] += 1
            ws.envia({"id": ident[0], "method": metodo, "params": params})
            while True:
                m = ws.recibe()
                if m.get("id") == ident[0]:
                    if "error" in m:
                        raise RuntimeError(f"{metodo}: {m['error']}")
                    return m.get("result", {})

        manda("Page.enable")
        manda("Page.navigate", url=url)
        # Mermaid pinta despues de load: se espera a que no queden bloques sin dibujar.
        limite = time.time() + espera + 40
        listo = False
        while time.time() < limite:
            time.sleep(0.6)
            r = manda("Runtime.evaluate", returnByValue=True, expression="""
                (function () {
                  if (document.readyState !== 'complete') return null;
                  var t = document.querySelectorAll('pre.mermaid, .mermaid').length;
                  var h = document.querySelectorAll('.mermaid svg, pre.mermaid svg').length;
                  var estado = document.documentElement.dataset.diagramas || '';
                  if (t && estado !== 'listos' && estado !== 'error') return '1:0';
                  return t + ':' + h;
                })()""")
            v = r.get("result", {}).get("value")
            if v:
                total, hechos = (int(x) for x in v.split(":"))
                if hechos >= total:
                    listo = True
                    break
        if not listo:
            print("   aviso: algun diagrama pudo no terminar de dibujarse", file=sys.stderr)
        time.sleep(espera)

        arriba, der, abajo, izq = margenes
        hoja = PAPEL[papel] if isinstance(papel, str) else papel
        r = manda("Page.printToPDF",
                  printBackground=True, preferCSSPageSize=False,
                  paperWidth=hoja[0], paperHeight=hoja[1], scale=escala,
                  marginTop=arriba / 25.4, marginRight=der / 25.4,
                  marginBottom=abajo / 25.4, marginLeft=izq / 25.4,
                  displayHeaderFooter=True, headerTemplate=VACIO,
                  footerTemplate=_pie(izquierda, derecha),
                  transferMode="ReturnAsBase64")
        with open(salida, "wb") as f:
            f.write(base64.b64decode(r["data"]))
        return salida
    finally:
        if ws:
            ws.cierra()
        nav.cierra()


def paginas(pdf):
    """Numero de paginas, con pdfinfo (poppler)."""
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


def indice_de_paginas(pdf, marcas):
    """En que pagina cae cada marca. `marcas` es {clave: texto que aparece en el titulo}.

    Se lee el texto del PDF ya maquetado — que es la unica forma honesta de saberlo,
    porque los saltos de pagina los decide el maquetador, no nosotros.
    """
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                         capture_output=True, text=True).stdout
    hojas = txt.split("\f")
    encontrado = {}
    for clave, aguja in marcas.items():
        objetivo = _normaliza(aguja)
        for i, hoja in enumerate(hojas, start=1):
            if objetivo and objetivo in _normaliza(hoja):
                encontrado[clave] = i
                break
    return encontrado


def _normaliza(t):
    t = re.sub(r"[^\w\s]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        raise SystemExit(2)
    kw = {}
    if "--titulo" in args:
        kw["izquierda"] = args[args.index("--titulo") + 1]
    if "--espera" in args:
        kw["espera"] = float(args[args.index("--espera") + 1])
    a_pdf(args[0], args[1], **kw)
    print(f"{args[1]} · {paginas(args[1])} paginas")
