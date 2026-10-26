---
name: ig-reutilizar
description: >-
  Convierte un material largo (un video de YouTube, un podcast, un en vivo, un
  boletín, una entrada de blog o una llamada con un cliente) en una semana de
  reels y carruseles. Úsala cuando digan "reutiliza esto", "conviértelo en
  reels", "tengo un video/podcast/transcripción", "córtalo en pedazos", o
  cuando peguen algo largo y lo quieran en Instagram.
---

# ig-reutilizar

Un buen material largo tiene adentro de cuatro a seis publicaciones. La mayoría
de la gente saca una y bota el resto.

Si existe la voz de la marca (`voz.md` en los archivos del proyecto, o en
`~/.claude/instagram/voz.md` en Claude Code), léela antes de escribir.

## Lo que necesitas

Una transcripción, un artículo, un boletín, un guion, el resumen de una llamada,
un en vivo. Si la persona da un enlace y esta sesión tiene una herramienta para
sacar transcripciones, úsala; si no, pide que lo pegue. Lee todo antes de sacar
cualquier cosa.

Si el material es un video de la propia persona, pide también el archivo. Un
Reel hecho con su propio video le gana a uno hecho con sus palabras leídas otra
vez.

## Saca piezas, no resumas

El resumen de un video no es un Reel. Nadie quiere el resumen. Recorre el
material y saca las cosas que se sostienen solas:

| saca | qué es |
| --- | --- |
| **Afirmaciones** | cada frase que empezaría una discusión |
| **Cifras** | cada número, costo, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada "en realidad esto funciona así..." |
| **Errores** | cada vez que admite algo que salió mal |
| **Frases** | cada frase que ya se puede citar tal cual |

Haz la lista de lo que encontraste, con conteos, antes de escribir nada. Si el
material da menos de cuatro piezas, es flaco, y cuatro publicaciones sacadas de
ahí también van a ser flacas. Dilo.

## Luego escoge el formato de cada pieza

No todo es un Reel.

- **Afirmación, error, historia** a Reel. Necesitan una voz y una cara.
- **Mecanismo, lista numerada** a carrusel. Hay que volver a leerlos.
- **Una frase citable** a un cuadro de historia, no a una publicación.

## Luego arma la semana

Cada pieza se vuelve una publicación, y cada publicación se sostiene sola por
completo. Quien mira no ha visto el material original y nunca lo verá. Nunca
escribas "como dije en mi último video". La publicación es la cosa.

Asígnale a cada una una fórmula de gancho de `ganchos.json` (de `ig-reel`) y
varíalas. Cinco publicaciones de un mismo material con la misma forma de gancho
se leen como una fábrica de contenido, porque lo son.

Si el material es un video de la propia persona, **usa las imágenes reales**. El
clip donde dijo la cosa, con la reacción real, le gana a volver a grabar, siempre.
Corta en la frase, no en la respiración.

Ordénalas en la semana para que la afirmación más fuerte vaya primero, la
historia caiga a mitad de semana y el mecanismo vaya al final, cuando la gente
a la que le gustaron las anteriores lo está esperando.

## Resultado

```
MATERIAL: "Por qué dejamos de hacer llamadas de diagnóstico" (podcast de 42 min, 8.900 palabras)

ENCONTRÉ  5 afirmaciones, 9 cifras, 3 historias, 4 mecanismos, 2 errores, 7 frases citables

SEMANA
MAR  REEL      #2  Orden negativa             Deja de hacer llamadas de diagnóstico
                                              usa el clip del 14:20, al final se ríe
MIÉ  CARRUSEL  Trabajo B en el texto          El formulario de 4 preguntas que reemplazó la llamada
VIE  REEL      #21 Empezar a mitad de frase   "...y nueve días después me pidió la devolución"
DOM  REEL      #5  Tiempo comprimido          Seis horas a la semana de vuelta, un enlace menos

Dime "escribe el martes" y lo redacto.
```

Luego redacta lo que pidan, de a uno, cada uno pasado por `ig-reel` e
`ig-humano`. No sueltes cuatro guiones terminados de una vez. Van a sonar todos
igual y la persona no va a grabar ninguno.
