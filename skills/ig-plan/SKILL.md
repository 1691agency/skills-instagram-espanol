---
name: ig-plan
description: >-
  Arma la semana en Instagram: qué publicar, en qué formato, cuándo y con
  quién interactuar. Úsala cuando digan "planea mi semana", "qué publico",
  "calendario de contenido", "parrilla de contenido", "no tengo de qué
  publicar", o cuando quieran un horario de publicación y una lista de cuentas
  para interactuar.
---

# ig-plan

La sala de control. Todo lo demás en este paquete ejecuta; esto decide qué se
ejecuta. Córrela una vez por semana, siempre el mismo día.

## Lo que necesitas

Lee estos archivos si existen. En Claude (web o app), búscalos entre los
archivos del proyecto o los adjuntos de la conversación; en Claude Code, en
`~/.claude/instagram/`:

- `voz.md`: la voz de la marca.
- `referentes.md`: la evidencia de la propia persona, sacada con `ig-viral`,
  sobre qué fórmulas están funcionando ahora en su nicho. Vale más que cualquier
  cosa de este archivo.
- `historial.md`: evita que el plan repita un tema de las últimas dos semanas.

Si no existen, pide cuatro cosas y anótalas:

1. Qué vende la persona, y a quién.
2. Los tres o cuatro temas por los que quiere ser conocida.
3. Qué pasó de verdad esta semana: una llamada con un cliente, una cifra, un
   error, algo que construyó, una discusión que tuvo. De ahí salen las
   publicaciones.
4. Diez cuentas ante las que vale la pena hacerse visible.

## Qué publicar

De cuatro a cinco publicaciones por semana, y al menos tres de ellas Reels. Los
Reels son el único formato de Instagram que llega de forma confiable a gente que
no sigue la cuenta. Los carruseles profundizan con la gente que ya la sigue. Las
historias son diarias y se planean aparte.

Mezcla durante la semana, nunca dos del mismo tipo seguidas:

| tipo | cuántas | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con una cifra. Reel. |
| **Enseñar** | 1 a 2 por semana | una cosa que quien mira puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 por semana | una postura que te podría costar seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un costo. Reel. |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho sin rodeos, sin pedir perdón. Carrusel o historias. |

Para cada espacio da: el tema, el ángulo concreto sacado de lo que pasó esta
semana, el formato y el número de fórmula de gancho de `ganchos.json` (de
`ig-reel`). No un tema, un ángulo. "IA" no es un plan. "La propuesta que
perdimos porque el borrador tenía una raya de IA" es un Reel.

## Cuándo publicar

Publica cuando el público de la persona está despierto y no está trabajando.
Para la mayoría de públicos de consumo eso es al empezar la noche, hora local;
para un público de negocios, temprano en la mañana.

Pero dilo claro: **la hora importa mucho menos que los dos primeros segundos.**
Instagram sigue mostrando un Reel durante días si funciona, y entierra uno bien
programado que no funciona. Si la persona está afinando horarios antes de que
sus ganchos funcionen, está puliendo lo que no es, y se lo tienes que decir.

Usa la zona horaria del público, no la de la persona, si son distintas.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Arma una lista de 10:

- **5 de alcance**: cuentas con un público que la persona quiere, donde un buen
  comentario se ve. Comenta temprano, antes de que haya 200 comentarios.
- **3 pares**: mismo tamaño, mismo campo. Este es el grupo que devuelve el gesto.
- **2 compradores**: gente que de verdad podría comprar. Comenta durante semanas
  antes de cualquier mensaje, y nunca vendas en un comentario.

Pásale la lista a `ig-comentar`.

## Resultado

```
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interacción  (20 min, lista abajo)
MAR  7:30 pm  REEL      PRUEBA    #5  Tiempo comprimido  - de 5 horas a 20 minutos por propuesta
MIÉ  solo historias + interacción
JUE  7:00 pm  CARRUSEL  ENSEÑAR   Trabajo B en el texto  - la cláusula explicada en 4 diapositivas
VIE  7:30 pm  REEL      OPINIÓN   #2  Orden negativa     - deja de hacer llamadas de diagnóstico
SÁB  -
DOM  6:00 pm  REEL      HISTORIA  #21 Empezar a mitad de frase - el correo pidiendo la devolución

HISTORIAS  todos los días, de 3 a 5 cuadros, caja de preguntas el jueves.

INTERACCIÓN  (5 alcance / 3 pares / 2 compradores)
  ...

Dime "escribe el martes" y lo redacto.
```

Guarda el plan como `plan.md` para que las otras habilidades lo puedan leer. En
Claude Code, en `~/.claude/instagram/plan.md`. En Claude (web o app), entrégale
el archivo a la persona para que lo suba a los archivos del proyecto. No se
programa ni se publica nada en ninguna parte. Es un plan, y lo ejecuta la
persona.
