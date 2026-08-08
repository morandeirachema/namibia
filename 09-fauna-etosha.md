# 09 · Fauna del viaje

> **Namibia · 30 oct – 15 nov 2026 · la clásica del norte** — [← índice del dossier](README.md)
>
> El índice de la guía de campo en PDF: 85 especies con foto, cómo reconocerlas, **qué
> posibilidades hay de verlas** y dónde y cuándo.
>
> **~N$20 = €1** *(rango 19,5–20,5)* · **✅** fuente primaria · **◐** secundaria concordante ·
> **○** práctica común, sin fuente · **❌** sin verificar, dicho en blanco
>
> *Investigación cerrada el 03/08/2026 · posibilidades de avistamiento y consejos de safari
> añadidos el 07/08/2026*

📕 **[Descargar la guía: `guia-fauna-etosha.pdf`](guia-fauna-etosha.pdf)** — 19 páginas A4,
**85 especies de toda la ruta**, con foto **completa** de cada una — sin recortes: cuernos,
cuellos y colas se ven enteros, que es justo lo que sirve para identificar.
Pensada para **imprimirla y llevarla en la guantera**: en Etosha no hay cobertura.

*(GitHub no previsualiza PDF: pulsa el enlace y se descarga. Este documento es el índice, para poder
buscar una especie desde el repo.)*

---

## Qué trae cada ficha

- **Nombre en castellano, científico e inglés** — el inglés importa: es el que veréis en los
  carteles del parque y el que usa todo el mundo allí
- **Qué posibilidades hay de verla**, medida y con su muestra detrás *(abajo, de dónde sale)*
- **Cómo reconocerla en el campo**: los rasgos que de verdad distinguen, no una descripción de
  enciclopedia *(labio del rinoceronte, rosetas frente a manchas, orejas de la hiena, pico del cálao…)*
- **Cuántas quedan**, en las ocho especies con una cifra publicada que se pueda citar
- **Foto** de Wikimedia Commons, todas con **licencia libre** (CC BY, CC BY-SA, CC0 o dominio
  público), con autoría y licencia bajo la imagen y en los créditos finales

## Las posibilidades de ver cada bicho, medidas

Nadie publica «qué probabilidad hay de ver un leopardo». Lo que sí es público son dos cosas, y
la guía usa las dos —cada una con su etiqueta, porque **no miden lo mismo**—:

```mermaid
flowchart LR
    A["14 especies grandes<br/>PARTES DE VIAJEROS"] --> A1["% que lo vio<br/>durante su estancia<br/>en el campamento"]
    B["las otras 71<br/>REGISTROS DE GBIF"] --> B1["peso de la especie<br/>en su grupo, en la zona,<br/>en oct-nov"]
    A1 --> C["frecuente / escasa<br/>siempre con la muestra"]
    B1 --> C
    style A fill:#EDF1E4,stroke:#5F7043
    style B fill:#EAF1F5,stroke:#2F6E8E
    style C fill:#F7F4ED,stroke:#C2542F
```

1. **Los partes de avistamiento que publica Expert Africa** para los tres campamentos donde se
   duerme: **Okaukuejo** *(149 viajeros)*, **Halali** *(48)* y **Namutoni** *(16)*. Ahí está la
   respuesta directa — **elefante 96 %, rinoceronte negro 82 %, león 70 %, guepardo 19 %,
   leopardo 12 %, oricteropo 0 %** ◐. Ojo con la unidad: es **por estancia en un campamento**,
   ni por día ni por viaje. Y como se duerme en los tres, son tres tiradas y no una.
2. **Los registros de GBIF** dentro del polígono real del parque *(y de otras tres zonas de la
   ruta)*, **filtrados a octubre y noviembre**: 4.529 registros de mamífero y 69.600 de ave solo
   en Etosha ◐. Eso mide **lo que se registra**, que no es lo que se ve, así que la guía dice
   «frecuente» o «escasa» y **nunca** «lo vas a ver».

**Los dos sesgos van escritos en el propio PDF**, no en letra pequeña: los partes los rellenan
viajeros y traen confusiones —un **14 % declara antílope sable en Okaukuejo, y en Etosha no hay
sable**—, y a GBIF nadie sube el chacal número doscientos ni casi nada nocturno, por lo que la
liebre saltadora sale con **cero registros** y se ve todas las noches.

Eso destapó **un conflicto que estaba escondido**: el **39 % de los partes dice haber visto
rinoceronte blanco**, y en el parque hay **apenas una docena** en 22.000 km². Casi todo eso tiene
que ser rinoceronte **negro** mal identificado — y la ficha ahora lo avisa.

Lo baja y lo cachea [`fuente/avistamientos.py`](fuente/avistamientos.py) en
`fuente/geo/avistamientos.json`; el PDF se monta desde ese fichero, sin tocar la red.
Fuentes: [GBIF](https://www.gbif.org) ·
[Expert Africa · Etosha](https://www.expertafrica.com/namibia/etosha-national-park)

## Cómo se hace un safari, delante de las fichas

Tres páginas antes de las especies, maquetadas como un documento del dossier: **la ropa**
*(Okaukuejo promedia 37,1 °C de máxima y 18,9 °C de mínima en noviembre ✅ — se viste por
capas)*, **lo que tiene que ir dentro del habitáculo y no en el maletero** *(prismáticos uno por
persona, 4 L de agua por persona y día ✅, frontal de luz roja, efectivo, microfibra)*, **la
táctica de la charca** *(motor apagado y tres cuartos de hora, que es lo que de verdad funciona)*,
**fotografía sin trípode** y un bloque aparte en rojo con **lo que es reglamento y no consejo**
✅: 60 km/h, no bajar del coche fuera de los campamentos, no salirse de las pistas y estar dentro
antes de que cierre la puerta.

## El «dónde y cuándo», en 37 de las 85 fichas

Charca por charca y con su fuente: **Okondeka** para el león, **Halali y Goas** para el leopardo,
**Salvadora–Sueda–Charitsaub** para el guepardo, el **Dik-dik Drive** nada más entrar por Von
Lindequist, y el nido de tejedor republicano **a diez metros de la charca de Okaukuejo**.

Las 46 fichas restantes **no llevan esa línea**: no apareció información
específica de Etosha en ninguna fuente decente, y rellenarlo a ojo sería inventar.

### Y cuatro avisos que corrigen lo que dicen las webs de safaris

- **Flamencos: en noviembre no hay.** La depresión está seca —la NASA la fotografió «bone dry» en
  diciembre— y solo crían cuando la lluvia pasa de 400 mm, algo que ocurrió **tres veces en cuarenta
  años**. Los flamencos de vuestro viaje están en **Walvis Bay**, donde el máximo va de junio a
  noviembre.
- **El abejaruco carmesí no está en Etosha**: cero registros dentro del parque. El que sí veréis es
  el **abejaruco europeo**, que llega en octubre.
- **La cigüeña de Abdim tampoco**: en Etosha es ave de febrero y marzo.
- **La cebra de montaña de Hartmann no está en vuestro eje**: vive en las lomas de dolomita del
  extremo oeste del parque.

Lo que sí lleva, porque está verificado: **cómo funciona el safari** —horarios de puerta calculados
para vuestros días, el límite de 60 km/h, la prohibición de bajar del coche, las tres charcas
iluminadas, el safari nocturno guiado de NWR (**N$750 ≈ €38** por persona) y —decidido el
08/08— **las salidas guiadas de mañana desde cada campamento (N$650 ≈ €33 por persona)**: los
traslados entre campamentos van con el 4x4 propio—, y un **bloque de
seguridad** con las serpientes y el escorpión que de verdad importan.

---

## Las 85 especies

### 🦁 Mamíferos (32)

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
- **Zorro orejudo** — *Otocyon megalotis* · Bat-eared fox
- **Jineta de manchas pequeñas** — *Genetta genetta* · Small-spotted genet
- **Puercoespín del Cabo** — *Hystrix africaeaustralis* · Cape porcupine
- **Liebre saltadora** — *Pedetes capensis* · Springhare
- **Klipspringer o saltarrocas** — *Oreotragus oreotragus* · Klipspringer
- **Mangosta amarilla** — *Cynictis penicillata* · Yellow mongoose
- **Oricteropo o cerdo hormiguero** — *Orycteropus afer* · Aardvark
- **Babuino chacma** — *Papio ursinus* · Chacma baboon *(añadido el 08/08: es el «mono» real de
  los miradores y campamentos de esta ruta — el vervet se descartó a propósito: sin un solo
  registro en la consulta GBIF del 08/08, archivada en `15`)*

### 🦅 Aves (28)

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
- **Pelícano blanco común** — *Pelecanus onocrotalus* · Great white pelican
- **Águila volatinera o bateleur** — *Terathopius ecaudatus* · Bateleur
- **Buitre orejudo** — *Torgos tracheliotos* · Lappet-faced vulture
- **Flamenco común** — *Phoenicopterus roseus* · Greater flamingo
- **Cormorán del Cabo** — *Phalacrocorax capensis* · Cape cormorant
- **Charrán damara** — *Sternula balaenarum* · Damara tern
- **Ostrero africano** — *Haematopus moquini* · African oystercatcher
- **Francolín de pico rojo** — *Pternistis adspersus* · Red-billed spurfowl

### 🦎 Reptiles (11)

*Las tres primeras van por seguridad: dormís trece noches en tienda.*

- **Víbora bufadora** — *Bitis arietans* · Puff adder
- **Cobra escupidora cebra** — *Naja nigricincta* · Zebra spitting cobra
- **Mamba negra** — *Dendroaspis polylepis* · Black mamba
- **Víbora de Péringuey** — *Bitis peringueyi* · Peringuey's adder
- **Víbora cornuda** — *Bitis caudalis* · Horned adder
- **Camaleón del Namib** — *Chamaeleo namaquensis* · Namaqua chameleon
- **Gecko palmeado del Namib** — *Pachydactylus rangei* · Web-footed gecko
- **Agama de roca de Namibia** — *Agama planiceps* · Namibian rock agama
- **Varano de roca** — *Varanus albigularis* · Rock monitor
- **Tortuga leopardo** — *Stigmochelys pardalis* · Leopard tortoise
- **Lagarto de nariz de pala** — *Meroles anchietae* · Shovel-snouted lizard

### 🌊 La costa, la roca y la arena (5)

*Lo de fuera de Etosha: Cape Cross (D7), la laguna de Walvis Bay (D5–D6) y los roquedos de Damaraland.*

- **Lobo marino del Cabo** — *Arctocephalus pusillus* · Cape fur seal
- **Delfín de Heaviside** — *Cephalorhynchus heavisidii* · Heaviside's dolphin
- **Ballena jorobada** — *Megaptera novaeangliae* · Humpback whale *(añadida el 08/08: migra
  frente a la costa jun–nov — los registros GBIF de la zona, consulta del 08/08/2026
  archivada mes a mes en `15`, dan pico jul–sep y 27 aún en noviembre: el crucero del D6 cae en
  temporada)*
- **Damán roquero** — *Procavia capensis* · Rock hyrax
- **Ardilla terrestre del Cabo** — *Xerus inauris* · Cape ground squirrel

### 🐞 Bichos (9)

*Los que se ven seguro en un viaje de camping — más que al leopardo.*

- **Escarabajo de la niebla** — *Onymacris unguicularis* · Fog-basking beetle
- **Escorpión de cola gruesa** — *Parabuthus villosus* · Black hairy thick-tailed scorpion
- **Araña blanca del Namib** — *Leucorchestris arenicola* · Dancing white lady spider
- **Termita constructora** — *Macrotermes michaelseni* · Termite
- **Escarabajo pelotero** — *Scarabaeus satyrus* · Dung beetle
- **Solífugo o araña camello** — *Solifugae* · Sun spider / camel spider
- **Gusano de mopane** — *Gonimbrasia belina* · Mopane worm
- **Milpiés gigante o shongololo** — *Archispirostreptus gigas* · Giant African millipede
- **Mosquito anofeles** — *Anopheles* · Anopheles mosquito

---

## Cómo se regenera

Todo vive en [`fuente/`](fuente/): `catalogo.py` fija qué fichero exacto de Wikimedia Commons usa
cada especie, `descargar.py` los baja con su licencia y autoría, `textos_especies.py` guarda los
rasgos de identificación, `textos_etosha.py` lo específico del parque, `textos_poblacion.py` las
cifras de cuántos quedan, `textos_safari.py` los consejos, `avistamientos.py` los recuentos de
GBIF y los porcentajes por campamento, y `guia_fauna.py` arma el HTML. El PDF lo imprime Chrome
desde `imprimir.py`, que es quien pone los números de página.

Con un solo comando, desde `fuente/`: **`make fauna`** *(o `make todo` para rehacerlo desde cero,
imágenes y recuentos incluidos; `make avistam` solo los recuentos)*. Y **`make comprueba`** valida
que están las 122 imágenes, que ninguna se ha colado con licencia no libre, que los dos PDF tienen
las páginas que deben y que los datos de avistamiento cubren las 85 especies.

*Las fotos **sí** están en el repo, en [`img/fauna/`](img/fauna/): son 5,6 MB, y a cambio el PDF
se puede regenerar idéntico dentro de un año sin depender de que Commons siga ordenando igual una
búsqueda. · 05/08/2026*
