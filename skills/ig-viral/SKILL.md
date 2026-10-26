---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahora en el nicho de la
  persona, los ordena según cuánto superaron a su propia cuenta, nombra la
  fórmula de gancho de cada uno y lo convierte en un archivo de referentes del
  que se puede grabar. Úsala cuando digan "busca videos virales", "qué está
  funcionando", "qué publica la gente de mi nicho", "analiza esta cuenta",
  "hazme un archivo de referentes", "por qué a este reel le fue tan bien", o
  cuando pregunten qué hacer después y no tengan evidencia para responder.
---

# ig-viral

La habilidad de investigación. Todo lo demás en este paquete escribe; esta va y
mira. Córrela cada mes, no cada día. Las fórmulas duran una temporada.

En esta carpeta hay un programa que funciona:

```bash
python3 referentes.py recogidos.tsv --salida referentes.md
```

El programa está en la carpeta de esta habilidad: córrelo desde ahí o con su
ruta completa. Esta carpeta trae su propia copia de `ganchos.json` y
`puntaje_gancho.py` (los mismos de `ig-reel`) para funcionar aunque se instale
sola.

## La idea que hace que valga la pena

**Las vistas solas no son evidencia.** Una cuenta de dos millones de seguidores
con 400.000 vistas tuvo un martes tranquilo. Una cuenta de cuatro mil seguidores
con 400.000 vistas encontró algo, y ese algo se puede copiar.

Por eso aquí todo se ordena por **cuántas veces superó lo normal**: las vistas
divididas entre la mediana reciente de esa misma cuenta. Más de 3 veces es una
señal. Menos de 1,5 veces es un día normal de esa cuenta y no te enseña nada,
por grande que se vea la cifra.

Recoge cuentas que estén **a unas 10 veces o menos del tamaño de la persona**.
Una fórmula que funciona con 2 millones de seguidores muchas veces funciona
porque tiene 2 millones de seguidores.

## Paso 1: escoge las cuentas

Pide de 6 a 12 cuentas, o propónlas y espera la aprobación:

- **4 directas**: mismo nicho, misma oferta, un poco más adelante.
- **4 vecinas**: otro nicho, mismo público. De aquí se toman los formatos antes
  de que alguien del nicho los tenga.
- **De 2 a 4 enormes**: cuentas mucho más grandes, solo para el formato, nunca
  para la frecuencia ni el tono.

Pide también que abra su colección de **Guardados**. Es el grupo más rápido y
relevante que existe y ya viene filtrado por su gusto.

## Paso 2: ve a mirar

Usa la herramienta de navegación que de verdad tenga esta sesión: un navegador
dentro de la app, una extensión conectada al Chrome de la persona, o una
herramienta para usar el computador. No hay una API para esto y no hace falta,
porque el volumen es tan pequeño que se puede leer.

**Reglas que no se negocian:**

- **Nunca inicies sesión en Instagram por la persona y nunca pidas una
  contraseña.** Si una página pide iniciar sesión, la que ya tiene la sesión
  abierta es la persona. Maneja su navegador con ella presente, o pídele que
  pegue los datos.
- **Esto es leer, no raspar.** Diez cuentas, una docena de reels cada una, a
  velocidad de persona. Recoger datos de forma automática y en volumen viola las
  Condiciones de uso de Instagram y hace que bloqueen las cuentas. No armes un
  programa que recorra perfiles, no uses un servicio de extracción y no lo
  repitas en segundo plano.
- **Copia la fórmula, nunca el video.** La forma del gancho, la estructura, la
  duración, el ritmo de los cortes. No su guion, no su voz, no su edición.
  Pon en cada fila del archivo de referentes la cuenta de donde salió.

**Qué anotar de cada reel**, en las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | el @usuario |
| seguidores | del perfil |
| mediana | mira los últimos 12 reels y toma la cifra de vistas del medio |
| vistas | las de este reel |
| gancho | la primera frase, dicha o en pantalla, tal cual, con errores y todo |
| pantalla | la primera tarjeta de texto, si es distinta |
| duración | en segundos |
| pedido | qué pidieron al final |

La mediana es la importante. Sin ella vuelves a ordenar por número de
seguidores, que es justo lo que esta habilidad existe para evitar.

**Cuando Instagram no deja ver lo suficiente:** la misma gramática de ganchos
funciona en YouTube Shorts, donde las vistas y los subtítulos son públicos y no
hace falta iniciar sesión. Es un segundo grupo legítimo, y ahí el gancho hablado
es más fácil de sacar:

```bash
# vistas de los Shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera frase dicha de un Short, desde los subtítulos automáticos
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DEL_VIDEO"
```

Toma cada palabra de los subtítulos que tenga una marca de tiempo antes de los
3,0 segundos. Ese es el gancho, como se dijo, no como se escribió.

## Paso 3: ordénalo

Llena un archivo separado por tabulaciones con una primera fila de encabezados
(en español o en inglés) y corre el programa. Las cifras pueden ir como 412000,
412.000, 412k, 412 mil o 1,2M:

```
cuenta	seguidores	mediana	vistas	gancho
@alguien	48000	11000	412000	nadie te dice que tus primeros 30 reels están hechos para fracasar
```

```bash
python3 referentes.py recogidos.tsv --salida referentes.md
```

Calcula cuántas veces superó cada reel a su cuenta, nombra la fórmula de gancho
con las mismas 26 fórmulas con las que escribe `ig-reel`, califica cada gancho
con `puntaje_gancho.py` e imprime qué separa al tercio de arriba del de abajo.

## Paso 4: di qué significa, con cuidado

Reporta tres cosas y nada más:

1. **Qué fórmulas aparecen de más** en el tercio de arriba, con conteos. Dos
   fórmulas que aparecen cuatro veces cada una en seis cuentas es un hallazgo.
   Una que aparece dos veces no lo es.
2. **Qué tienen en común en estructura** los de arriba que no tengan los de
   abajo: largo del gancho, si la recompensa es visual, si el primer cuadro se
   mueve, dónde está el pedido.
3. **Las filas sin clasificar.** Cada gancho que el programa no pudo nombrar es
   ruido o una fórmula que todavía no está en `ganchos.json`. Léelos a mano. Es
   la columna más valiosa del resultado y por eso el programa imprime el conteo.
   Las fórmulas en español se escribieron para esta versión y no se han medido
   contra muchos ganchos reales: si una se equivoca seguido, corrige su
   expresión en `ganchos.json`.

Luego di el tamaño de la muestra y la confianza en palabras simples. Cuarenta
reels en seis cuentas sostienen una afirmación. Doce no, y decirlo es la
diferencia entre investigar y leer el horóscopo.

## Paso 5: conviértelo en algo para grabar

Para las tres fórmulas de arriba, escribe **la versión de la persona**: su
propia historia, su propia cifra, con la forma que está funcionando. Pásale cada
una a `ig-reel` con la fórmula ya escogida.

Nunca entregues "haz un reel como este". Entrega una frase de gancho que pueda
decir mañana.

## Resultado

```
REFERENTES  ·  38 reels  ·  7 cuentas  ·  base: mediana de la cuenta

POR ENCIMA DE 3 VECES
  38,4x  gancho 87  #3  Nadie te dice     @cuenta_a    412.000  (mediana 10.700)
  11,2x  gancho 79  #9  Róbate esto       @cuenta_c    180.000  (mediana 16.100)
  ...

LO QUE APARECE DE MÁS
  #3 Nadie te dice      x5 en el tercio de arriba, 0 abajo
  #2 Orden negativa     x4
  largo medio del gancho   8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en ganchos.json: un gancho que empieza
  leyendo en voz alta el comentario de otra persona. Vale la pena agregarla.

TU VERSIÓN
  #3  "Nadie te dice que las primeras 20 propuestas están hechas para perderse."
  ...
```

(Esto es un ejemplo de formato; los números reales salen del programa.)

Guarda el archivo de referentes. En Claude Code, en
`~/.claude/instagram/referentes.md`. En Claude (web o app), entrégale
`referentes.md` a la persona para que lo suba a los archivos del proyecto.
`ig-reel` e `ig-plan` lo leen, y esa es la idea: después de correr esto una vez,
el resto del paquete trabaja con la evidencia de la propia persona y no con
valores por defecto.

Esta habilidad no publica, no sigue, no da me gusta ni envía mensajes. Lee.
