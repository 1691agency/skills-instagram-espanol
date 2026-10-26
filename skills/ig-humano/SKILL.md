---
name: ig-humano
description: >-
  Quita de cualquier borrador las huellas de texto hecho por máquina (rayas,
  palabras de relleno típicas de la IA, caracteres invisibles) y lo califica
  con cinco revisiones antes de publicarlo. Úsala siempre que un texto tenga
  que sonar humano, cuando digan "humaniza esto", "¿esto suena a IA?", "quita
  las rayas", "suena a ChatGPT", "quítale lo robótico", o antes de mostrarle a
  la persona cualquier texto, guion, comentario, respuesta o mensaje.
---

# ig-humano

En esta carpeta hay dos programas y los dos funcionan de verdad. Úsalos. No lo
hagas a ojo.

```bash
python3 humanizar.py borrador.txt -o limpio.txt --reporte   # limpia y muestra qué cambió
python3 detectar.py borrador.txt                            # califica, cinco revisiones
python3 detectar.py borrador.txt limpio.txt                 # muestra el antes y el después
```

Los programas están en la carpeta de esta habilidad: córrelos desde ahí o con
su ruta completa.

Los dos leen `relleno.json`: unas 240 palabras y frases de relleno con su
reemplazo en palabras simples, 18 tipos de caracteres invisibles, 11 cambios
tipográficos y 16 estructuras que delatan. El último bloque de cada lista es
propio de Instagram: el vocabulario que solo aparece en textos de publicaciones
y voces en off. La lista se armó para el español (no es una traducción palabra
por palabra del original en inglés) y está hecha para editarse. Si la persona
usa a propósito una palabra que la lista quita, sácala del archivo.

## Por qué esto importa más en Instagram de lo que parece

Los textos son cortos y los guiones se dicen en voz alta. Una línea que suena
escrita en un texto de 600 caracteres pesa más que la misma línea en un ensayo,
y una voz en off que nadie diría de forma natural se nota en la primera toma. La
señal aquí no es que un detector marque la publicación. La señal es una persona
que pasa de largo porque algo suena a marca, o un creador que se traba con su
propio guion.

## Lo que se arregla solo

**1. Caracteres invisibles.** Espacios de ancho cero, uniones de palabras,
guiones suaves, marcas BOM, caracteres de etiqueta, separadores invisibles,
espacios de no separación y espacios finos. Un teclado no los produce.
Sobreviven al copiar y pegar, no se ven en ningún editor y son lo más mecánico
de un texto generado. `humanizar.py` borra todos, incluido cualquier otro
carácter de formato que no tenga en la lista.

**2. Tipografía.** Raya a coma, semirraya a guion, comillas curvas a rectas,
el carácter de puntos suspensivos a tres puntos, viñeta a guion. La pasada de la
raya es la que importa: la convierte en coma y luego limpia la puntuación doble
que queda. **Dos excepciones del español:** la raya de diálogo al empezar una
línea se respeta, y las comillas angulares « » no se tocan, porque las dos son
correctas.

**3. Las palabras de relleno.** "crucial", "fundamental", "potenciar",
"sumérgete en", "cabe destacar que", "en el vertiginoso mundo de", "hoy en día",
"déjame saber" (calco del inglés), más el bloque de Instagram: "deja de hacer
scroll", "en el video de hoy", "síguenos para más", "etiqueta a alguien que
necesite esto", "el algoritmo ama", "corre, no camines". Cada una se cambia por
una palabra simple o se borra, sin importar las tildes, conservando la
mayúscula inicial y sin tocar los enlaces. Los reemplazos cuidan el género ("el
panorama" pasa a "la situación", no a "el situación").

## Lo que NO se arregla solo

Las estructuras que delatan se **marcan, no se reescriben**, porque cambiar la
forma de una frase necesita criterio:

- "No es solo X, es Y" y "no solo X, sino también Y"
- "No se trata de X. Se trata de Y."
- Tríos de tres ("rápido, fácil y barato.")
- Líneas de pregunta retórica: "¿El resultado?"
- La introducción de video: "en este video te voy a mostrar"
- Listas con emojis como viñetas
- Tres o más palabras seguidas en MAYÚSCULAS
- Muros de más de cinco hashtags
- Carnada por reflejo: "síguenos para más", "etiqueta a alguien que", "dale like si"

Esa lista es tu trabajo. Reescribe a mano cada línea marcada, conservando el
sentido, y vuelve a correr `detectar.py`. Eso es lo que sube el puntaje de
REVISAR a PASA, y es lo que un programa no puede hacer.

## Las cinco revisiones

`detectar.py` califica cinco señales de 0 a 100; más alto es más humano:

| revisión | qué mide | cómo se ve la máquina |
| --- | --- | --- |
| VARIACIÓN | cuánto cambia el largo de las frases | todas las frases del mismo largo |
| CONCRECIÓN | cifras, nombres y datos por cada 100 palabras | sustantivos abstractos, sin cifras |
| RELLENO | palabras de la lista por cada 100 palabras | vocabulario de catálogo |
| HUELLAS | invisibles, rayas y comillas curvas por cada 1.000 caracteres | tipografía perfecta |
| VOZ | habla cotidiana, persona gramatical, estructuras que delatan | sin "yo" ni "tú", revelaciones montadas |

El resultado pesa el promedio en un 60% y la **revisión más débil** en un 40%,
porque basta una señal. PASA necesita 70 o más en total y ninguna revisión por
debajo de 55.

La revisión de VOZ cambia respecto al original en inglés: allá cuenta
contracciones ("don't", "it's"), que no existen en español, y aquí cuenta marcas
de habla cotidiana ("o sea", "la verdad", "pues", "ojo", "en serio"). Y como en
español casi nunca se dice el pronombre, la persona gramatical cuenta también
los verbos en "nosotros" ("tostamos", "pensábamos"). Son reglas nuevas y no se
han medido contra textos reales en español.

## Dilo con honestidad

Son cinco reglas simples basadas en las señales que miran los detectores
públicos. Corren solo en el equipo y no se sube nada. **No** son GPTZero,
Originality, Copyleaks, Winston ni Turnitin, no llaman a esos servicios y no
pueden prometer lo que ellos digan. Arreglar lo que miden suele mover esos
números, porque miden las mismas cosas de fondo. Eso es todo lo que se afirma.
No afirmes algo más grande en nombre de la persona, y nunca le digas que su
texto es indetectable.

## Orden de trabajo

1. `humanizar.py borrador.txt -o limpio.txt --reporte`
2. Lee las estructuras marcadas. Reescribe tú esas líneas.
3. `detectar.py borrador.txt limpio.txt` para mostrar el antes y el después.
4. Si el resultado no es PASA, arregla la revisión más débil que indica el
   programa y vuelve a correrlo. Dos rondas es normal. Cinco quiere decir que el
   borrador se escribió con fórmula, y el arreglo es otro borrador, no más
   rondas.
5. Muéstrale a la persona el texto limpio y el puntaje. Nunca el puntaje solo.

En textos muy cortos (un comentario, una respuesta), varias revisiones dicen
"muy corto para juzgar". Ahí lo útil es la limpieza de `humanizar.py`; el
puntaje no dice mucho.
