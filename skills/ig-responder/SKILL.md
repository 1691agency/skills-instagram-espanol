---
name: ig-responder
description: >-
  Maneja los comentarios debajo de los reels y publicaciones propios: redacta
  respuestas para los que vale la pena contestar, ordenados según cuáles valen
  más. Úsala cuando peguen sus comentarios, cuando digan "responde estos",
  "ayúdame con mis comentarios", "alguien dijo X en mi reel", o cuando estén
  lidiando con un crítico, alguien que odia o un posible cliente en los
  comentarios.
---

# ig-responder

La conversación debajo de tu propia publicación es donde se decide el alcance.
Cada respuesta es otra interacción en la publicación, las respuestas de la
primera hora hacen la mayor parte del trabajo, y en Instagram una respuesta
también puede ser un Reel, que es la jugada menos usada de toda la plataforma.

Pero no todos los comentarios valen lo mismo, así que esta habilidad ordena
antes de escribir.

Si existe la voz de la marca (`voz.md` en los archivos del proyecto, o en
`~/.claude/instagram/voz.md` en Claude Code), léela antes de escribir.

## Lo que necesitas

La persona pega los comentarios, idealmente con los @usuarios. Los pantallazos
sirven. No recorras la conversación con un navegador.

## Primero, ordenar

Pon cada comentario en uno de seis grupos y di los conteos:

| grupo | qué es | qué recibe |
| --- | --- | --- |
| **PALABRA CLAVE** | la palabra que pediste que comentaran | lo prometido, enviado a mano o con tu herramienta aprobada |
| **CLIENTE POTENCIAL** | alguien que describe el problema que tú resuelves | una respuesta de verdad en público, y luego una puerta |
| **APORTE** | suma datos, no está de acuerdo, amplía | la respuesta más larga de la conversación |
| **PREGUNTA** | una pregunta que tiene mucha gente | se vuelve un Reel, no solo una respuesta |
| **APOYO** | "🔥", "buenísimo", una etiqueta | un me gusta, y de 3 a 8 palabras como mucho |
| **RUIDO** | venta, spam, mala fe, provocación | nada, o una línea y ya |

Escribe en ese orden y para cuando se acabe el valor.

## La jugada que casi todos se pierden

Si una pregunta de los comentarios es una que también tienen otras treinta
personas, **respóndela con un Reel**. Instagram pega el comentario al video
nuevo como un sticker, a quien preguntó le llega una notificación, y una
pregunta con demanda real se vuelve una publicación con el gancho ya escrito.
Marca cada PREGUNTA que califique y pásasela a `ig-reel` como fórmula #16.

## Cómo responder

- **Responde la pregunta de verdad.** Si alguien pregunta cómo, dile cómo, en la
  respuesta. No lo mandes al privado a escuchar una respuesta que podía tener
  ahí mismo.
- **Usa su nombre una vez**, al principio, sin signos de admiración.
- **Iguala su largo.** Un comentario de cuatro palabras no recibe una respuesta
  de cuatro líneas.
- **A un crítico:** primero concede la parte que es cierta, en sus palabras, y
  luego sostén tu punto. Nunca borres, nunca te pongas a la defensiva, nunca
  respondas dos veces en el mismo hilo.
- **A alguien que odia:** nada. Una respuesta es alcance, y alcance es lo que
  vino a buscar. Oculta el comentario si es ofensivo. Los controles de
  comentarios de Instagram existen y usarlos no es perder.
- **A un cliente potencial:** responde completo en público. La puerta es una
  frase al final y es un ofrecimiento de ayuda, no una venta. La respuesta
  pública es lo que hace que la siguiente persona te escriba.

## Comentarios con palabra clave

Si la publicación pedía comentar una palabra, esos comentarios son todo el
punto de la publicación. Cada uno es una persona que levantó la mano. Responde a
cada uno y luego envía lo prometido. Si la persona tiene automatización
configurada con las herramientas de Instagram o un socio aprobado, dilo y deja
que funcione; si no, las respuestas son a mano, y a este volumen está bien.
Nunca mandes mensajes masivos a gente que no comentó.

## Resultado

Un solo bloque, agrupado, con cada respuesta lista para copiar y ya pasada por
`ig-humano`:

```
RESPUESTAS  ·  84 comentarios  ·  41 PALABRA CLAVE, 2 CLIENTE, 3 APORTE, 2 PREGUNTA, 34 APOYO, 2 RUIDO

PALABRA CLAVE  (41)  envía la cláusula. Una línea a cada uno, mismo cariño, sin copiar y pegar.

CLIENTE POTENCIAL
@usuario - "a nosotros nos pasó exactamente esto en junio"
> Lo que nos lo arregló fue sacar el pago de la aprobación del todo.
> Si te sirve, te mando la redacción.

PREGUNTA -> REEL
@usuario - "¿y qué haces si no lo quieren firmar?"
  34 me gusta en este comentario. Eso es un Reel, no una respuesta. Fórmula #16.

RUIDO  (2)  sin responder. Responder les da alcance.
```

Y luego el filtro: no se publica nada hasta que la persona diga que sí. Ella
pega las respuestas.
