---
name: ig-carrusel
description: >-
  Arma un carrusel de Instagram: la portada que se gana el deslizar, el texto
  de cada diapositiva y los archivos de 1080x1350 para subir. Úsala cuando
  digan "carrusel", "diapositivas", "publicación para deslizar", "convierte
  esto en un carrusel", o cuando la idea tenga forma de lista o de pasos y
  moriría como una sola imagen.
---

# ig-carrusel

Los carruseles son el formato de la cuadrícula donde la gente más se queda,
porque deslizar es una interacción y bajar no lo es. Además tienen una segunda
oportunidad: Instagram puede volver a mostrar un carrusel, empezando desde una
diapositiva posterior, a alguien que no interactuó la primera vez. Por eso la
diapositiva dos también tiene que sostenerse sola.

El formato premia una idea partida en pasos. Castiga un texto cortado en
pedazos.

Si existe la voz de la marca (`voz.md` en los archivos del proyecto, o en
`~/.claude/instagram/voz.md` en Claude Code), léela antes de escribir.

## Cuándo usarlo en vez de un Reel

Usa un carrusel cuando la idea tiene **secuencia y hay que volver a leerla**:
pasos, un método con partes, un antes y un después, una lista que vale un
pantallazo. Usa un Reel cuando la idea tiene movimiento, una cara, o una
recompensa que hay que ver pasar.

Si la idea es una sola afirmación, no es ninguno de los dos. Pásasela a
`ig-reel` y dilo.

## Estructura

De 6 a 10 diapositivas. El tope es 20, y 20 casi siempre es un libro que nadie
termina. Con menos de 5, el deslizar ni empieza.

```
1         PORTADA     el gancho. Seis palabras o menos, a un tamaño que se lea
                      en miniatura en la cuadrícula. Una línea de promesa debajo.
2         LO EN JUEGO por qué importa, en una frase. Esta diapositiva también
                      es una segunda portada, así que no puede ser introducción.
3 a N     UNA IDEA POR DIAPOSITIVA. Un título de 3 a 7 palabras y como máximo
                      25 palabras debajo. Si una diapositiva necesita un
                      párrafo, son dos diapositivas.
N+1       RESUMEN     todo como lista. Esta es la diapositiva del pantallazo.
ÚLTIMA    PEDIDO      una acción. Guardar, comentar una palabra o seguir. Una.
```

## Reglas del texto de cada diapositiva

- **La portada es el 80% del resultado.** Seis palabras. Grandes. Nada del resto
  salva una portada que nadie desliza.
- **Diseña para el recorte de la cuadrícula.** La cuadrícula del perfil recorta
  a un rectángulo vertical, y la proporción exacta ha cambiado más de una vez.
  Construye en 1080x1350 y deja el texto de la portada bien adentro, lejos de
  los 120 píxeles de cada borde, y el recorte deja de importar.
- **Numera las diapositivas** (3/8). Más gente termina cuando ve dónde acaba.
- **Ninguna diapositiva es un párrafo.** Si no cabe en 25 palabras, divídela.
- **La diapositiva de resumen es la que la gente captura y envía.** Los envíos
  son la señal más fuerte que te puedes ganar. Que se entienda sola y sin
  contexto.
- **El @usuario en cada diapositiva**, pequeño, en una esquina de abajo. Los
  pantallazos viajan sin ti.
- **Texto alternativo al menos en la portada.** Lo leen los lectores de
  pantalla y lo lee Instagram.

## Cómo hacer los archivos

Instagram pide 1080x1350 (4:5), JPG o PNG, hasta 20 elementos. Arma el carrusel
en HTML y convierte cada diapositiva en imagen:

```bash
# una <section> por diapositiva, 1080x1350, page-break-after: always
# luego Chrome sin interfaz (headless) o cualquier convertidor de HTML a imagen que tengas
```

Escribe el HTML con `width:1080px; height:1350px`, un solo color de acento, y
letra de mínimo 32px, porque se lee en un celular a un tercio de su tamaño real.
Si el proyecto tiene una guía de marca o un sistema de diseño, úsalo y no
inventes una paleta.

## Resultado

Primero el texto de cada diapositiva como una lista numerada que la persona
pueda leer en diez segundos y corregir antes de que se haga cualquier imagen.
Luego el **texto de la publicación**, que en un carrusel es el Trabajo B de
`ig-texto`: aquí el texto sí trabaja, porque la portada ya gastó sus seis
palabras.

Pasa las dos cosas por `ig-humano`. Haz los archivos solo después de que la
persona apruebe el texto.

```
CARRUSEL  ·  8 diapositivas

1  PORTADA  LA CLÁUSULA DE 18 MILLONES
            La línea que ahora pongo en todos mis contratos.
2  EN JUEGO Aprobé el trabajo. Nueve días después me pidieron la plata de vuelta.
3           QUÉ DICE
            Pago a la entrega, no a la aprobación.
...
7  RESUMEN  Las cuatro líneas, en orden.
8  PEDIDO   Comenta CONTRATO y te mando la cláusula completa.

Texto: Trabajo B, gancho en la línea 1, un pedido, 3 hashtags.
```

No se sube nada. La persona lo publica.
