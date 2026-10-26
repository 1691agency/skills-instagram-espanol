---
name: ig-comentar
description: >-
  Escribe comentarios para publicaciones y reels de otras personas en
  Instagram que suenen a alguien con una opinión, no a un bot. Úsala cuando
  peguen una publicación o un reel y quieran un comentario, cuando digan
  "comenta esto", "interactúa con esto", "qué pongo aquí", o cuando quieran un
  grupo de comentarios para su ronda diaria de interacción.
---

# ig-comentar

Comentar son los veinte minutos que más rinden en Instagram y los más fáciles
de hacer mal. Un comentario cerca de arriba en un reel de 40.000 vistas lo ve
más gente que la mayoría de publicaciones propias de una cuenta, y es el único
lugar donde un desconocido puede tocar y llegar directo a un perfil.

Un comentario genérico es peor que ninguno. Cuesta un toque que no lleva a nada
y marca la cuenta como de "grupo de interacción" ante la única persona cuya
opinión importaba: el creador.

Si existe la voz de la marca (`voz.md` en los archivos del proyecto, o en
`~/.claude/instagram/voz.md` en Claude Code), léela antes de escribir.

## Lo que necesitas

La persona pega el texto de la publicación o el reel, o un pantallazo, con el
nombre de la cuenta. Si te da un enlace que no puedes abrir, pídele que lo pegue.
No uses un navegador para recorrer el feed y no publiques nada.

## Los nueve tipos de comentario

Escoge según lo que de verdad es la publicación. Nunca uses el tipo 1 por
costumbre.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Suma un dato** | la publicación afirma algo que puedes respaldar con una cifra | "A nosotros igual: el 40% de..." |
| 2 | **Suma el caso que falta** | la publicación tiene razón pero está incompleta | "Esto funciona hasta que {condición}." |
| 3 | **Desacuerdo respetuoso** | de verdad crees que está mal | primero en qué estás de acuerdo, luego dónde te separas |
| 4 | **Extiende una línea** | una línea de la publicación es la buena | cítala y construye sobre ella |
| 5 | **Haz la pregunta de verdad** | la publicación se saltó la parte difícil | una pregunta, concreta |
| 6 | **El comprobante** | tú hiciste lo que describe | qué pasó, en dos frases |
| 7 | **La corrección** | hay un error de dato | ten razón, sé breve, sé amable, ten certeza |
| 8 | **El otro ángulo** | los datos están bien, el enfoque no | "Otra forma de verlo:" |
| 9 | **La frase corta** | la publicación no necesita nada, quieres estar presente | menos de 10 palabras, que sea graciosa o cierta |

## Reglas

- **De una a tres frases.** Los comentarios se leen en una columna angosta
  debajo de un video. Un párrafo queda escondido detrás de "más" y nadie lo
  abre.
- **Nunca empieces con** "Excelente publicación", "Me encanta", "Muy cierto",
  "Esto 👏", "Necesitaba esto hoy", ni con el nombre del creador seguido de
  signos de admiración. Todos son invisibles.
- **Nada de comentarios solo con emojis** y nada de emoji como primer carácter.
- **Nunca repitas el reel.** Todos los que están mirando acaban de verlo.
- **Una idea.** Un comentario con dos puntos se lee como un secuestro.
- **Di lo concreto.** Si el comentario podría ir debajo de cualquier publicación
  del tema, no es un comentario, es ruido.
- **Nunca vendas.** Ni la oferta, ni el enlace, ni "pasa por mi perfil". Es la
  forma más rápida de que te bloquee justo la persona a la que querías llegar.
- **Temprano importa más aquí que en cualquier otra parte.** Un comentario en la
  primera hora de un reel que luego viaja, viaja con él.

## Resultado

Da **dos opciones de tipos distintos**, con su etiqueta, más una línea sobre cuál
publicarías y por qué. Pasa las dos por `ig-humano` primero: los comentarios son
cortos, así que una raya o una frase de relleno pesa más que en un texto largo.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre precios)

[6 · Comprobante]
Nosotros subimos precios un 40% en marzo y perdimos un solo cliente, el que nos
llenaba medio buzón. Nos tomó ocho meses dejar de tenerle miedo.

[3 · Desacuerdo respetuoso]
De acuerdo con lo del anclaje. Donde no estoy de acuerdo es en hacerlo a mitad
del proyecto. Lo intentamos y nos costó una renovación que iba bien.

Publicaría el primero. Concede algo y tiene una cifra.
```

## Modo por grupos

Para una ronda de interacción, pide las 5 a 10 publicaciones como texto pegado
en un solo mensaje, devuelve un comentario para cada una en un solo bloque, y
lleva una nota en el historial de a quién se le ha comentado esta semana (en
Claude Code, `~/.claude/instagram/historial.md`; en Claude web o app, entrega el
archivo actualizado para subirlo al proyecto). Comentarle a las mismas tres
cuentas todos los días se nota, y se ve exactamente como lo que es.

## Nunca

No publiques solo, no automatices comentarios y no uses un navegador para
publicar por la persona. La interacción automatizada viola las Condiciones de
uso de Instagram y hace que bloqueen las acciones de la cuenta. Esta habilidad
escribe el comentario. La persona lo publica.
