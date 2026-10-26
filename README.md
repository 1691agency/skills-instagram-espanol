# Skills de Instagram en español

Trece habilidades de Claude para manejar una cuenta de Instagram, en español.
Gratis, licencia MIT, sin registros, sin claves de API, sin nada que conectar.

Es la versión en español de
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
de Jake Schincariol. No es solo una traducción: los programas se adaptaron para
que entiendan tildes, ñ, signos de apertura (¿¡) y cifras escritas a la manera
latina (18.000.000, 48k, 1,2M), y las listas de palabras se armaron de nuevo
para el español.

Una de las habilidades escribe tus Reels con 26 fórmulas de gancho y califica el
gancho antes de que pierdas una toma. Otra busca los reels que de verdad están
funcionando en tu nicho y los ordena según cuánto superaron a su propia cuenta.
Otra escribe el texto de la publicación y te muestra exactamente lo que se ve
antes del "... más". Otra califica tu perfil sobre 100 y reescribe lo que pierde
puntos. Otra planea la semana.

Y una es el humanizador, que es lo que hace usable todo lo demás. Quita las
rayas, las palabras de relleno típicas de la IA y los caracteres invisibles de un
borrador, y califica lo que queda con cinco revisiones antes de que lo veas.

**Nada se publica hasta que tú digas que sí.** Estas habilidades escriben. Tú
publicas.

## Instalación

### En Claude (web, escritorio o celular)

Necesitas un plan de pago (Pro, Max, Team o Enterprise) y tener activada la
ejecución de código.

1. Entra a la carpeta [`descargas/`](descargas) de este repositorio y descarga
   los 13 archivos `.zip` (abre cada uno y usa el botón de descargar).
2. En Claude, ve a **Configuración → Capacidades** y revisa que esté activada la
   ejecución de código y creación de archivos.
3. En la sección **Habilidades**, toca **Subir habilidad** y sube los `.zip`, uno
   por uno.

Más detalles en la [ayuda oficial de Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### En Claude Code

```bash
git clone https://github.com/1691agency/skills-instagram-espanol.git
cp -r skills-instagram-espanol/skills/ig-* ~/.claude/skills/
```

O como complemento (plugin):

```
/plugin marketplace add 1691agency/skills-instagram-espanol
/plugin install instagram-agente-es
```

### Sin instalar nada

Pega cualquier `SKILL.md` al principio de un chat y funciona como un modo para
esa conversación. Pierdes los cinco programas, que son casi todo el valor de
`ig-reel` e `ig-humano`, pero el resto funciona.

## Antes de empezar: tu voz

Dedícale diez minutos a [`plantillas/voz.md`](plantillas/voz.md). Llénala y
guárdala como `voz.md`:

- **En Claude:** súbela a los archivos del proyecto donde trabajas esa marca. Si
  manejas varias marcas, cada proyecto lleva su propio `voz.md`.
- **En Claude Code:** cópiala a `~/.claude/instagram/voz.md`.

También puedes mandarle a Claude tres de tus reels y decirle "escribe mi voz.md
con estos". Las habilidades la leen. Importa más aquí que en otras redes, porque
las palabras las tienes que decir en voz alta.

## Cómo se usa

Pide las cosas con palabras normales: "hazme un reel sobre por qué subimos los
precios", "revisa este texto", "califica mi perfil". Claude usa la habilidad que
corresponde. También puedes nombrarla ("usa ig-reel para..."), y en Claude Code
funciona con `/ig-reel`.

## Las trece

| habilidad | qué hace |
| --- | --- |
| `ig-reel` | De una idea a un Reel. Tres ganchos con [26 fórmulas](skills/ig-reel/ganchos.json), calificados, y luego el guion, el texto en pantalla y una hoja de tiempos. |
| `ig-viral` | Busca lo que está funcionando en tu nicho, lo ordena por cuántas veces superó lo normal de cada cuenta, nombra la fórmula y escribe el archivo de referentes. |
| `ig-texto` | El texto de la publicación, revisado. Te muestra los 125 caracteres que de verdad se ven antes del toque. |
| `ig-carrusel` | Publicaciones para deslizar. La portada que se gana el deslizar, el texto de cada diapositiva y los archivos de 1080x1350. |
| `ig-historias` | La secuencia de historias del día, qué sticker hace qué trabajo, y el embudo a los mensajes que empieza cuando ellos se mueven primero. |
| `ig-perfil` | Califica tu perfil con una [rúbrica de 12 puntos](skills/ig-perfil/rubrica.json) sobre 100 y reescribe en orden de lo que más urge. |
| `ig-plan` | La semana. Qué publicar, en qué formato, cuándo, y las 10 cuentas con las que interactuar. |
| `ig-humano` | El humanizador. Dos programas que de verdad funcionan. Ver abajo. |
| `ig-comentar` | Comentarios en publicaciones de otros. Nueve tipos, escogidos según lo que es la publicación. Nunca "🔥🔥🔥". |
| `ig-responder` | Los comentarios de tu propia publicación. Los ordena en palabra clave / cliente / aporte / pregunta / apoyo / ruido, y responde en ese orden. |
| `ig-mensajes` | La entrega por palabra clave, el primer mensaje, la propuesta de colaboración y los dos seguimientos. Dos. |
| `ig-reutilizar` | Un video, podcast o boletín convertido en una semana de reels y carruseles que se sostienen solos. |
| `ig-auditoria` | Revisión de lo que ya publicaste. Ordena por veces sobre lo normal y envíos por alcance, no por vistas. |

## Los cinco programas que de verdad funcionan

Sin dependencias, sin internet, no suben nada. Corren en tu equipo, sobre tu
texto. Todo lo que se muestra abajo es la salida real de los programas.

### Ganchos

```bash
python3 puntaje_gancho.py opciones.txt          # ordena tus opciones
python3 tiempos.py guion.txt --objetivo 30      # mídelo antes de grabar
```

```
RANKING DE GANCHOS
==============================================================================
->  87.0 FUERTE    Nadie te dice que tus primeros 30 reels están hechos para...
        lo más débil: CONCRECIÓN (75)
    84.4 FUERTE    Perdí 18 millones por una cláusula que no puse en el cont...
        lo más débil: DESTINATARIO (70)
    51.4 ACEPTABLE Deja de hacer scroll si quieres vender más en Instagram 🔥
        lo más débil: TENSIÓN (70)
        descarte: Empieza con "deja de hacer scroll". Pedir atención demuestra que no te la has ganado.
        descarte: Emoji en el gancho. En texto de pantalla a tamaño de gancho cabe una palabra o un emoji, no las dos.
     5.4 DÉBIL     Hola a todos, hoy les quiero hablar de estrategia de cont...
        lo más débil: ARRANQUE (0)
        descarte: Saludo. Nadie entró al feed a que lo saludaran.
```

`tiempos.py` calcula cuánto se demora cada línea en decirse, las suma en tiempos
y marca las cuatro cosas que matan un Reel en la edición: un gancho de más de
tres segundos, una parte tan larga que la gente se va, varias líneas seguidas
sin nada concreto, y que el final no vuelva a la primera línea.

```
HOJA DE TIEMPOS  ·  54 palabras  ·  ~19.6 s a 165 ppm  ·  objetivo 30 s
========================================================================
  0:00.0   2.2s  GANCHO        Perdí 18 millones por una cláusula.
  0:02.2   6.9s                Esta es la cláusula exacta que ahora pongo en todos mis contratos, sin falta, porque aprendí por las malas.
                               ^ 6.9 s en una sola parte
  0:09.1   3.6s  MITAD         Cláusula cuatro. Pago a la entrega, no a la aprobación.
  0:12.7   3.6s                La aprobación es un sentimiento. La entrega es una fecha.
  0:16.4   3.3s  CIERRE        Ese cambio de una palabra me vale 18 millones.
------------------------------------------------------------------------
  - La(s) parte(s) 2 pasan de 4 s. Divide la línea o cambia lo que se ve en pantalla en la mitad. Un plano quieto es donde la gente se va.
  - Hay bucle: la última parte repite "18, millones" del gancho. Las segundas vistas son alcance gratis.
  - 10.4 s por debajo del objetivo. Agrega 28 palabras o grábalo más corto. Más corto casi siempre es mejor.
```

### El texto de la publicación

```bash
python3 revisar_texto.py texto.txt --palabras-clave "cláusula,contratos"
```

Instagram muestra unos 125 caracteres del texto en el feed y esconde el resto
detrás de un toque. Casi todos los textos que fallan, fallan ahí. Por eso lo
primero que imprime es esa ventana, en un recuadro, como la lee un desconocido
que va bajando:

```
  LO QUE MUESTRA EL FEED
  +------------------------------------------------------+
  | Perdí 18 millones por una cláusula que faltaba en un |
  | contrato, y lo peor es que lo había leído dos veces  |
  | antes de firmarlo.                                   |
  +--------------------------------------------- ... más +

  BIEN  LONGITUD         340 / 2200 caracteres
  BIEN  PRIMERA LÍNEA    123 caracteres, se ve completa
  BIEN  GANCHO CONCRETO  1 cifra(s) o nombre(s) en la parte visible
  BIEN  HASHTAGS         3 hashtag(s): #freelance #contratos #agencias
  BIEN  UBICACIÓN TAGS   los hashtags quedan debajo del corte
  BIEN  ENLACES          no hay enlaces muertos en el texto
  BIEN  UNA ACCIÓN       un solo llamado a la acción: comentar una palabra
  BIEN  EMOJIS           0 emoji(s), 0.0 por cada 100 caracteres
  BIEN  BÚSQUEDA         2/2 presentes, 1 en la parte visible
```

Aplica el tope actual de hashtags, que es de **cinco por publicación**, no
treinta. Instagram lo bajó en diciembre de 2025. También reconoce los pedidos
típicos de negocios locales ("reserva", "haz tu pedido", "visítanos") además de
"comenta", "guárdalo", "sígueme" y "escríbeme al DM".

### El humanizador

```bash
python3 humanizar.py borrador.txt -o limpio.txt --reporte   # limpia y muestra cada cambio
python3 detectar.py borrador.txt                            # califica, cinco revisiones
python3 detectar.py antes.txt despues.txt                   # muestra la diferencia
```

**Lo que se quita solo:**

- **Caracteres invisibles.** Espacios de ancho cero, uniones de palabras, guiones
  suaves, marcas BOM, caracteres de etiqueta, separadores invisibles, espacios
  de no separación. Tu teclado no los produce. Sobreviven al copiar y pegar y no
  se ven en ningún editor.
- **Tipografía.** Raya a coma, semirraya a guion, comillas curvas a rectas,
  puntos suspensivos de un solo carácter a tres puntos. Respeta la raya de
  diálogo al empezar una línea y las comillas angulares « », que son correctas
  en español.
- **Las palabras de relleno.** Unas 240 palabras y frases con reemplazos en
  palabras simples, buscadas con o sin tildes: "crucial", "potenciar", "cabe
  destacar que", "en el vertiginoso mundo de", "déjame saber"... El último
  bloque es de Instagram: "deja de hacer scroll", "en el video de hoy",
  "síguenos para más", "etiqueta a alguien que necesite esto", "el algoritmo
  ama". Está en [`relleno.json`](skills/ig-humano/relleno.json) y está hecha
  para editarse.

**Lo que se marca en vez de arreglarse:** "No es solo X, es Y", "no solo X,
sino también Y", tríos de tres, la introducción de video, listas con emojis como
viñetas, tres palabras seguidas en mayúsculas, muros de hashtags, carnada por
reflejo y frases todas del mismo largo. Cambiar la forma de una frase necesita
criterio, así que eso vuelve para que lo reescribas en vez de que lo destroce
una expresión regular.

Con un texto escrito para sonar lo más a IA posible:

```
  VARIACIÓN     ####################....  82.0
                variación 0.61 en 10 frases (ideal 0,55 o más)
  CONCRECIÓN    #######.................  28.4
                2 dato(s) concreto(s), 2.1 por cada 100 palabras (ideal 4 o más)
  RELLENO       ........................   0.0
                16 términos de relleno, 16.5 por cada 100 palabras (asimismo, brindarte, cabe destacar que, crucial, ...)
  HUELLAS       #####...................  21.0
                1 invisibles, 1 rayas, 0 comillas curvas, 0 puntos suspensivos en un carácter, 0 espacios duros
  VOZ           #####...................  21.9
                0.0 marcas de habla cotidiana, 4.1 marcas de primera o segunda persona por cada 100 palabras, 6 estructura(s) que delatan [no-es-solo, triada, cohete, muro-hashtags]
--------------------------------------------------------------
  HUMANO        ####....................  18.4   MARCADO
```

Después de `humanizar.py`, sin reescribir las estructuras marcadas:

```
  HUMANO        ############............  50.6   REVISAR
```

Después de reescribir a mano lo marcado y poner datos concretos:

```
  HUMANO        #####################...  89.5   PASA
```

### Los referentes

```bash
python3 referentes.py recogidos.tsv --salida referentes.md
```

Las vistas solas no son evidencia. Una cuenta de 2.000.000 de seguidores con
400.000 vistas tuvo un martes tranquilo. Una cuenta de 4.000 seguidores con
400.000 vistas encontró algo. `referentes.py` ordena por cuántas veces superó
cada reel lo normal de su propia cuenta, nombra la fórmula del gancho e imprime
qué separa al tercio de arriba del de abajo. Entiende cifras como 412.000, 48k,
300 mil o 1,2M.

```
REFERENTES  ·  5 reels  ·  5 cuentas  ·  base: mediana de la cuenta
==============================================================================
   120.0x  gancho  47  #9  Róbate esto              @cafe_c              180.000
           "Róbate esta receta de cold brew. Me tomó dos años dejarla bien"
    37.5x  gancho  87  #3  Nadie te dice            @barista_a           412.000
           "Nadie te dice que tus primeros 30 reels están hechos para fracasar"
    30.0x  gancho  34  #16 La pregunta tal cual     @foto_e               75.000
           "¿Cuánto cobro por una sesión de fotos? Me lo preguntan cada semana."
     1.8x  gancho  78  #23 El dato                  @agencia_d             9.000
           "El 80% de mis clientes llegó por un solo reel"
     1.2x  gancho   5  -   sin clasificar           @burger_b            360.000
           "Hola a todos, hoy les traigo la hamburguesa del mes"
```

## Lo que se midió, y lo que no

**El autor original midió su versión en inglés** con 74 ganchos reales (los
primeros tres segundos de los mejores y peores Shorts de cinco canales de
YouTube). Sus resultados: el calificador detecta bien los ganchos malos
(AUC 0,83: nueve de diez ganchos escritos para ser malos quedaron por debajo de
la mediana), pero **no elige ganadores**: entre los aciertos y los fracasos de
un mismo creador acertó con AUC 0,56, donde 0,50 es lanzar una moneda. Los
detalles están en el
[repositorio original](https://github.com/Jakeschincariol/instagram-agent-skill).

**Esta versión en español no se ha medido así.** Las listas de palabras, las
reglas del calificador y las 26 expresiones que reconocen fórmulas se
escribieron de nuevo para el español. Lo que sí se comprobó: cada una de las 26
fórmulas reconoce su propio ejemplo, y en una prueba con 15 ganchos escritos a
mano en español, 14 quedaron en la fórmula esperada (el que no, no tenía
fórmula). Eso es una prueba de funcionamiento, no una medición de qué tan bien
predice.

Así que el uso honesto es el mismo del original: descartar los ganchos
claramente flojos antes de grabarlos, y después confiar en tu propia gráfica de
retención. Nada que lea texto puede decirte cuál de dos ganchos decentes va a
funcionar, porque eso lo deciden tu cara, tu edición, tu audio y a quién se lo
muestra Instagram. Si lo pruebas con muchos ganchos reales en español y te da
otro resultado, abre un *issue*: es justo lo que hace falta.

## Qué cambió respecto al original

- Todo el texto, las instrucciones y los mensajes de los programas están en
  español, con ejemplos en pesos y en contexto latinoamericano.
- Los programas entienden tildes, ñ, ¿¡ y cifras como 18.000.000, 48k, 300 mil
  o 1,2M. Las búsquedas no distinguen tildes ("café" y "cafe" cuentan igual).
- Las listas de palabras de relleno, de tensión, de arranques débiles y de
  pedidos se armaron para el español, cuidando el género de los reemplazos y
  evitando frases legítimas (por ejemplo, "a fin de mes" no se toca).
- La revisión de voz cambió: el inglés cuenta contracciones, que en español no
  existen; aquí cuenta habla cotidiana y verbos en "nosotros".
- Las habilidades funcionan también en Claude (web y app): la voz y el historial
  se buscan en los archivos del proyecto, no solo en una carpeta del computador.
- `ig-viral` trae su propia copia de `ganchos.json` y `puntaje_gancho.py`, para
  que funcione aunque se suba sola. Si editas uno, edita también la copia.
- Se corrigieron detalles pequeños del original: un arranque débil ya no se
  confunde con una palabra que empieza igual ("has" con "hasta"), un mismo
  término de relleno ya no se cuenta dos veces, y guardar el archivo de
  referentes ya no falla si se le da solo un nombre de archivo.
- La revisión del texto ahora también avisa si la primera línea empieza con un
  saludo o con un emoji, como pedían las instrucciones originales.

## La letra pequeña, que es la parte honesta

**Estas habilidades no publican en Instagram.** Existe una API real de
publicación para cuentas profesionales, pero necesita una aplicación de
desarrollador de Meta, una página vinculada, un token de larga duración y una
revisión de la aplicación, y eso no es algo que una habilidad te pueda dar. Casi
todo lo demás que la gente usa para automatizar publicaciones, comentarios,
seguidos o mensajes es automatización del navegador o herramientas de terceros,
y las dos cosas violan las
[Condiciones de uso de Instagram](https://help.instagram.com/581066165581870) y
hacen que bloqueen las acciones de la cuenta. Por eso todas las habilidades
terminan igual: un bloque listo para copiar, y tú lo publicas.

La única excepción son las respuestas automáticas por palabra clave en mensajes,
que Instagram permite con sus propias herramientas y socios aprobados, y que
solo se activan después de que alguien comenta primero. `ig-mensajes` explica
dónde está esa línea.

**`ig-viral` lee, no raspa.** Diez cuentas, una docena de reels cada una, a
velocidad de persona, contigo manejando tu propio navegador. Nunca pide tu
contraseña ni inicia sesión por ti.

**Las cinco revisiones son reglas simples locales, no detectores.** Se basan en
las señales que miran los detectores públicos y corren en tu equipo. No son
GPTZero, Originality, Copyleaks, Winston ni Turnitin, no llaman a esos servicios
y no pueden prometer lo que ellos digan. Nadie puede venderte con honestidad
algo "indetectable".

**La limpieza de caracteres invisibles es real y es limitada.** Quita los
caracteres de formato que terminan en el texto generado y sobreviven al copiar y
pegar. No dice nada sobre romper una marca de agua criptográfica.

**Nada aquí inventa.** Ninguna cifra, cliente ni resultado inventado va a tu
nombre. Si un borrador necesita un número que no diste, vuelve con
`{{tu cifra}}` y un aviso, siempre.

**Los datos de la plataforma envejecen.** El tope de hashtags pasó de 30 a 5 en
diciembre de 2025. Si algo de aquí contradice lo que Instagram está haciendo
cuando lo leas, Instagram tiene la razón.

## Archivos

```
skills/ig-reel/ganchos.json          26 fórmulas de gancho: plantilla, ejemplo, versión para
                                     pantalla, para qué sirve, cómo se arruina y su expresión
skills/ig-reel/puntaje_gancho.py     las cinco revisiones del gancho
skills/ig-reel/tiempos.py            del guion a una hoja de tiempos
skills/ig-texto/revisar_texto.py     la ventana visible y la revisión del texto
skills/ig-humano/relleno.json        la lista: ~240 términos, 18 tipos de invisibles, 16 estructuras
skills/ig-humano/humanizar.py        las tres pasadas de limpieza
skills/ig-humano/detectar.py         las cinco revisiones
skills/ig-viral/referentes.py        orden por veces sobre lo normal y clasificación de fórmulas
skills/ig-perfil/rubrica.json        el puntaje del perfil sobre 100
plantillas/voz.md                    tu perfil de voz. Llénalo primero.
descargas/                           un .zip por habilidad, listo para subir a Claude
```

## Créditos

- **Versión original:**
  [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
  de Jake Schincariol ([opusjake.ai](https://opusjake.ai)), licencia MIT.
- **Traducción y adaptación al español:** Juan Sebastian Cruz - 1691 Agency.

Esta adaptación no está afiliada ni respaldada por el autor original, ni por
Instagram o Meta.

## Licencia

MIT. Úsala, cámbiala, compártela. Conserva el archivo [`LICENSE`](LICENSE), que
incluye el aviso de derechos del autor original.
