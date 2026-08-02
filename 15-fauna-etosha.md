# Fauna de Etosha — la guía de campo en PDF

📕 **[Descargar la guía: `guia-fauna-etosha.pdf`](guia-fauna-etosha.pdf)** — 9 páginas A4,
**24 mamíferos y 20 aves**, con foto **completa** de cada especie — sin recortes: cuernos, cuellos y colas se ven enteros, que es justo lo que sirve para identificar.
Pensada para **imprimirla y llevarla en la guantera**: en Etosha no hay cobertura.

*(GitHub no previsualiza PDF: pulsa el enlace y se descarga. Este documento es el índice, para poder
buscar una especie desde el repo.)*

---

## Qué trae cada ficha

- **Nombre en castellano, científico e inglés** — el inglés importa: es el que veréis en los
  carteles del parque y el que usa todo el mundo allí
- **Cómo reconocerla en el campo**: los rasgos que de verdad distinguen, no una descripción de
  enciclopedia *(labio del rinoceronte, rosetas frente a manchas, rayas de la cebra, pico del cálao…)*
- **Foto** de Wikimedia Commons, todas con **licencia libre CC BY o CC BY-SA**, con su autoría y
  licencia bajo la imagen y en los créditos finales

## Y lo que NO trae, dicho claro

**No lleva un «dónde ver» de cada especie.** Solo tienen esa línea las **tres** que el dossier tiene
verificadas *(rinoceronte negro, elefante y jirafa en la charca iluminada de Okaukuejo de noche)*.
Para el resto habría que inventárselo, y aquí no se hace — la [regla de siempre](README.md).

Lo que sí lleva, porque está verificado: **cómo funciona el safari** —horarios de puerta calculados
para vuestros días, el límite de 60 km/h, la prohibición de bajar del coche, las tres charcas
iluminadas, el safari nocturno guiado de NWR (**N$750 ≈ €38** por persona) y las charcas que caen en
la ruta de esos cuatro días—.

---

## Las 44 especies

### 🦁 Mamíferos

- **Elefante africano de sabana** — *Loxodonta africana* · African bush elephant
- **Rinoceronte negro** — *Diceros bicornis* · Black rhinoceros
- **Rinoceronte blanco** — *Ceratotherium simum* · White rhinoceros
- **León** — *Panthera leo* · Lion
- **Leopardo** — *Panthera pardus* · Leopard
- **Guepardo** — *Acinonyx jubatus* · Cheetah
- **Jirafa angoleña** — *Giraffa giraffa angolensis* · Angolan giraffe
- **Cebra de Burchell** — *Equus quagga burchellii* · Burchell's zebra
- **Cebra de montaña de Hartmann** — *Equus zebra hartmannae* · Hartmann's mountain zebra
- **Órix o gemsbok** — *Oryx gazella* · Gemsbok
- **Springbok** — *Antidorcas marsupialis* · Springbok
- **Gran kudú** — *Tragelaphus strepsiceros* · Greater kudu
- **Eland común** — *Taurotragus oryx* · Common eland
- **Ñu azul** — *Connochaetes taurinus* · Blue wildebeest
- **Impala de cara negra** — *Aepyceros melampus petersi* · Black-faced impala
- **Dik-dik de Damara** — *Madoqua damarensis* · Damara dik-dik
- **Hiena manchada** — *Crocuta crocuta* · Spotted hyena
- **Hiena parda** — *Parahyaena brunnea* · Brown hyena
- **Chacal de lomo negro** — *Lupulella mesomelas* · Black-backed jackal
- **Ratel o tejón de la miel** — *Mellivora capensis* · Honey badger
- **Facóquero** — *Phacochoerus africanus* · Common warthog
- **Suricata** — *Suricata suricatta* · Meerkat
- **Alcélafo rojo** — *Alcelaphus buselaphus caama* · Red hartebeest
- **Steenbok** — *Raphicerus campestris* · Steenbok

### 🦅 Aves

- **Avestruz común** — *Struthio camelus* · Common ostrich
- **Avutarda kori** — *Ardeotis kori* · Kori bustard
- **Secretario** — *Sagittarius serpentarius* · Secretarybird
- **Carraca lila** — *Coracias caudatus* · Lilac-breasted roller
- **Cálao de pico amarillo sureño** — *Tockus leucomelas* · Southern yellow-billed hornbill
- **Cálao de pico rojo sureño** — *Tockus rufirostris* · Southern red-billed hornbill
- **Tejedor republicano** — *Philetairus socius* · Sociable weaver
- **Águila marcial** — *Polemaetus bellicosus* · Martial eagle
- **Buitre dorsiblanco africano** — *Gyps africanus* · White-backed vulture
- **Flamenco enano** — *Phoeniconaias minor* · Lesser flamingo
- **Grulla azul** — *Grus paradisea* · Blue crane
- **Ganga namaqua** — *Pterocles namaqua* · Namaqua sandgrouse
- **Sisón negro norteño** — *Afrotis afraoides* · Northern black korhaan
- **Azor lagartijero claro** — *Melierax canorus* · Pale chanting goshawk
- **Alcaudón de pecho carmesí** — *Laniarius atrococcineus* · Crimson-breasted shrike
- **Búho lácteo de Verreaux** — *Bubo lacteus* · Verreaux's eagle-owl
- **Abejaruco carmesí sureño** — *Merops nubicoides* · Southern carmine bee-eater
- **Cigüeña de Abdim** — *Ciconia abdimii* · Abdim's stork
- **Estornino brillante del Cabo** — *Lamprotornis nitens* · Cape starling
- **Pigargo vocinglero** — *Icthyophaga vocifer* · African fish eagle

---

## Cómo se regenera

En [`fauna-fuente/`](fauna-fuente/) está lo necesario: `fetch.py` descarga las fotos de Wikimedia
Commons con su licencia y autoría vía API, `especies.py` tiene los textos, `etosha.py` lo específico
del parque, y `build.py` arma el HTML. El PDF sale con Chrome:

```
python3 fetch.py && python3 build.py
google-chrome --headless --no-pdf-header-footer --print-to-pdf=guia-fauna-etosha.pdf guia.html
```

*Las fotos no se guardan en el repo (pesan): `fetch.py` las vuelve a bajar. · 03/08/2026*
