---
name: ig-reel
description: >-
  Escribe un Reel de Instagram a partir de una idea suelta: opciones de gancho
  con 26 fórmulas, el guion hablado, el texto en pantalla y una hoja de tiempos,
  en la voz de la persona y calificado antes de grabar. Úsala cuando pidan un
  reel, un guion de video corto, un gancho, una voz en off, "hazme un reel
  sobre X", "qué digo en este video", o cuando van a grabar y no tienen la
  primera frase.
---

# ig-reel

Convierte una idea suelta en un Reel que la gente termina de ver.

En esta carpeta hay dos programas que de verdad funcionan. Úsalos. No califiques
el gancho a ojo y no adivines la duración.

```bash
python3 puntaje_gancho.py opciones.txt          # ordena tus opciones de gancho
python3 puntaje_gancho.py --gancho "una frase"  # califica uno solo
python3 tiempos.py guion.txt --objetivo 30      # hoja de tiempos antes de grabar
```

Los programas están en la carpeta de esta habilidad: córrelos desde ahí o con
su ruta completa.

## Antes de escribir

1. **Lee la voz de la marca** si existe. En Claude (web o app), busca `voz.md`
   (o un documento de voz de marca) entre los archivos del proyecto o los
   adjuntos de la conversación. En Claude Code, en `~/.claude/instagram/voz.md`.
   Ahí está cómo habla la persona en cámara, lo que nunca dice y a quién le
   habla. Si no existe, pide **tres de sus propios reels**, transcríbelos o
   léelos, deduce la voz y escribe el archivo. Un guion en la voz equivocada no
   sirve, porque lo tienen que decir en voz alta.
2. **Lee `ganchos.json`** en esta carpeta. 26 fórmulas, cada una con plantilla,
   un ejemplo lleno, la versión para pantalla, para qué sirve y cómo se arruina.
3. **Si la idea es flaca, no la rellenes.** Haz una sola pregunta agrupada: qué
   pasó, a quién y cuánto costó o dejó. Un Reel necesita una cosa concreta y
   verdadera. Consíguela antes de escribir.
4. **Si existe `referentes.md`**, léelo (en los archivos del proyecto o en
   `~/.claude/instagram/referentes.md`). Lo escribe `ig-viral` y es la evidencia
   de la propia persona sobre qué fórmulas están funcionando ahora en su nicho.
   Vale más que lo que dice este archivo.

## La forma

Un Reel se decide en los primeros dos segundos y se sostiene con los cinco
siguientes.

```
0:00 - 0:02   GANCHO        la afirmación. Frase hablada y frase en pantalla,
                            escritas por separado. Movimiento en el primer
                            cuadro, no una cara quieta.
0:02 - 0:07   LO EN JUEGO   por qué le importa a quien mira. Una línea.
0:07 - ...    EL CUERPO     una idea por parte, y el cuadro cambia en cada parte.
ÚLTIMOS 3 s   LA RECOMPENSA cumple lo que prometió el gancho, y luego el único pedido.
ÚLTIMA LÍNEA  EL BUCLE      repite una palabra del gancho para que la segunda
                            vista empalme limpio.
```

Duración: de 15 a 45 segundos es el rango que funciona. Los Reels pueden durar
hasta 3 minutos y casi nadie debería usarlos. Por debajo de 7 segundos se
inflan las repeticiones y nada más.

## El ciclo

**1. Elige tres ganchos, no uno.** Pasa la idea por `ganchos.json`, escoge tres
fórmulas que de verdad le queden y escribe la frase hablada y la de pantalla de
cada una. Fórmulas distintas, no tres versiones de la misma.

**2. Califícalos.** Pon las tres frases habladas en un archivo, una por línea, y
corre `puntaje_gancho.py`. Muéstrale el ranking a la persona. Si el primero
tiene menos de 50, todavía no tienes el gancho y ninguna edición lo arregla.

**3. Escribe el guion** sobre el gancho ganador. Lenguaje hablado y sencillo,
como habla de verdad la persona. Frases cortas. Ninguna frase que tenga que
ensayar.

**4. Mídelo.** Corre `tiempos.py guion.txt --objetivo {duración}`. Arregla cada
alerta: un gancho de más de 3 segundos, cualquier parte de más de 4 segundos,
varias partes seguidas sin nada concreto, o que no haya bucle. Repite hasta que
salga limpio.

**5. Humanízalo.** Pasa el guion por `ig-humano` antes de mostrarlo. Una línea
que suena escrita se nota apenas alguien la dice en voz alta.

**6. Entrega el bloque.** El guion en un bloque de código, el texto en pantalla
como una lista aparte con tiempos, y luego:

```
REEL LISTO
gancho:     #3 Nadie te dice, 87 FUERTE
duración:   28,4 s en 9 partes a 165 ppm
pantalla:   6 tarjetas
humano:     4 huellas quitadas, puntaje humano 81 PASA
texto:      sigue con ig-texto

Responde "sí" para guardarlo en el historial, o dime qué cambio.
```

**7. Nunca publiques.** Esta habilidad produce un guion. La persona lo graba y
lo publica. Si responde "sí", agrega al historial la fecha, la fórmula de gancho
usada y la primera línea, para que `ig-auditoria` tenga historia después. En
Claude Code, el historial está en `~/.claude/instagram/historial.md`. En Claude
(web o app), entrégale el archivo `historial.md` actualizado para que lo suba a
los archivos del proyecto.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de que se escuche.

- **Seis palabras o menos por tarjeta.** Lo lee a un brazo de distancia alguien
  que todavía no está escuchando.
- **La tarjeta del gancho está desde el cuadro 1**, no después de un silencio.
- **Mantenlo dentro de la zona segura.** En un cuadro de 1080x1920, nada por
  encima de y=230 ni por debajo de y=1440, y deja libres los 230 píxeles de la
  derecha. La interfaz tapa todo lo que queda por fuera: el texto de la
  publicación, la columna de botones, la franja del audio.
- **Nunca pongas el gancho donde va el texto de la publicación.** Eso es la
  parte de abajo del cuadro y queda tapado.
- **Subtítulos quemados en el cuerpo.** Casi todo el mundo mira primero sin
  sonido.

## Reglas que hacen la diferencia

- **Una idea por Reel.** Si el guion tiene dos, son dos Reels. Dilo.
- **Cifras, no adjetivos.** "4,2 millones" le gana a "un montón". Si la persona
  no dio una cifra, pídela en vez de escribir alrededor del hueco.
- **Corta la introducción.** Nada de saludo, ni "en este video", ni nombre, ni
  logo animado. El video empieza en la frase a la que normalmente llegarías en
  el segundo seis.
- **Cambia el cuadro en cada parte.** Un plano quieto de 8 segundos es donde la
  gente se va, y `tiempos.py` lo marca.
- **Un solo pedido al final.** Comentar una palabra, guardar o seguir. Uno.
- **Nunca inventes.** Ni cifras, ni clientes, ni ventas, ni resultados a nombre
  de la persona, ni siquiera como relleno. Si hace falta una cifra y no la
  sabes, deja `{{tu cifra}}` en el guion y avísalo.
- **No escribas un guion alrededor de un audio en tendencia que la persona no
  puede usar.** Si la idea necesita la voz propia, dilo.

## Ejemplo

```
ig-reel bajamos el tiempo de las propuestas de 5 horas a 20 minutos con una plantilla
```

```
GANCHOS  (calificados con puntaje_gancho.py)
  81 FUERTE     #1  Confesión de costo "Durante dos años cobré cuatro horas semanales por darle formato."
                                       en pantalla: 2 AÑOS PERDIDOS
  51 ACEPTABLE  #5  Tiempo comprimido  "Las propuestas me tomaban cinco horas. Ahora veinte minutos."
                                       en pantalla: 5 HORAS -> 20 MIN
  37 DÉBIL      #9  Róbate esto        "Róbate la plantilla que lo logró."
                                       en pantalla: RÓBATE ESTO

Grabaría el #1: tiene dos cifras, el costo lo pagaste tú y se dice en
menos de tres segundos. El #5 se entiende mejor en pantalla, pero no tiene
nada en juego: si lo prefieres, agrégale lo que perdías ("cinco horas que
no cobraba").
```

Los puntajes salen de correr `puntaje_gancho.py`; nunca los escribas a ojo.
