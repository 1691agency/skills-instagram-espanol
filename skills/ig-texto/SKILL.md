---
name: ig-texto
description: >-
  Escribe el texto (caption o copy) de una publicación de Instagram: la línea
  que sobrevive al corte del "... más", el cuerpo, el único pedido, las
  palabras de búsqueda y los hashtags, y lo revisa antes de publicar. Úsala
  cuando digan "escribe el texto", "hazme el copy", "el caption", "qué pongo en
  la descripción", cuando tengan un reel o un carrusel listo y les falte el
  texto, o cuando pregunten por hashtags.
---

# ig-texto

En esta carpeta hay un programa que funciona:

```bash
python3 revisar_texto.py texto.txt
python3 revisar_texto.py texto.txt --palabras-clave "café de especialidad,barista en Ibagué"
```

Imprime el texto como lo muestra el feed: los primeros 125 caracteres en un
recuadro y todo lo demás detrás del toque. Lee ese recuadro antes de leer
cualquier otra cosa que hayas escrito. El programa está en la carpeta de esta
habilidad: córrelo desde ahí o con su ruta completa.

Si existe la voz de la marca (`voz.md` en los archivos del proyecto, o en
`~/.claude/instagram/voz.md` en Claude Code), léela antes de escribir.

## Primero, decide qué trabajo tiene este texto

Esta es la decisión que arruina los textos cuando se salta.

**Trabajo A: el video ya enganchó.** Un Reel trae su propio gancho en los dos
primeros segundos, dicho y en pantalla. El texto no es un segundo gancho, y
competir con el video es la forma de perder los dos. Su trabajo es el pedido,
el contexto que hace que el pedido tenga sentido, y las palabras que la gente
busca.

**Trabajo B: el texto es el contenido.** Una foto, una imagen sola, una portada
de carrusel que deja algo abierto. Aquí la primera línea es el gancho y funciona
igual que el de un Reel: concreto, corto, y cortado en un momento de suspenso,
no a mitad de una frase.

Pregunta cuál estás escribiendo. Si la persona tiene un Reel con un gancho
fuerte, escribe A y di por qué.

## La forma

```
Línea 1     125 caracteres visibles. Trabajo A: el pedido, sin rodeos.
            Trabajo B: el gancho.
            Nunca un saludo, nunca un hashtag, nunca un emoji como primer
            carácter.
Cuerpo      párrafos cortos, una línea en blanco entre cada uno. De dos a
            seis. Aquí van las palabras de búsqueda.
El pedido   uno solo. Comentar una palabra, guardar, o escribir por mensaje. Uno.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es de 2.200 caracteres y casi nada necesita 2.200. Un texto que se
gana el toque y luego entrega 600 caracteres le gana a uno que entrega 1.800.

## Hashtags, con honestidad

Los hashtags ya no son una palanca de alcance, y la plataforma lo dijo con un
cambio en el producto. **Instagram limitó los hashtags a cinco por publicación
en diciembre de 2025**, antes eran treinta, y le dijo a los creadores que usar
menos hashtags (hasta 5) y más específicos funciona mejor que muchos genéricos.
A comienzos de 2025, Adam Mosseri, el jefe de Instagram, ya había dicho que los
hashtags no aumentan el alcance: son una etiqueta, no una palanca de
distribución.

Entonces: hasta cinco, específicos, como etiquetas del tema. Si la persona
tiene un bloque de veinte guardado en las notas del celular, ese bloque ya es
peso muerto y el programa lo va a marcar.

`#viral`, `#fyp`, `#parati`, `#explore` no describen nada. Quítalos.

## Las palabras de búsqueda ya importan más que los hashtags

El buscador de Instagram lee el texto. Así que la frase con la que la persona
quiere que la encuentren va en el texto como la escribiría alguien que busca, en
una frase que se lea normal. "Café de especialidad" como palabras en la línea
tres, no "#cafedeespecialidad" en un bloque al final.

Pide dos o tres de esos términos y pásaselos al programa:

```bash
python3 revisar_texto.py borrador.txt --palabras-clave "café de especialidad,catación"
```

## Reglas

- **Nada de enlaces en el texto.** En el texto no se puede hacer clic. Una URL
  en el cuerpo es texto muerto que dice "no uso esta red". Va en la bio o por
  mensaje.
- **Un solo pedido.** Dos pedidos valen lo mismo que ninguno. `revisar_texto.py`
  los cuenta.
- **El pedido de comentar necesita una palabra que se pueda escribir.** Una
  palabra, sin espacios, sin emoji, y dila también en voz alta en el video.
  `Comenta CONTRATO` funciona. `Comenta "la guía del contrato"` no.
- **Si hay un enlace, escribe aparte el primer comentario.** Dilo en el resumen.
- **Emojis como puntuación, no como decoración.** El programa marca más de 4 por
  cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo.
  Lo leen los lectores de pantalla y lo lee Instagram.

## El ciclo

1. Decide Trabajo A o Trabajo B y di cuál.
2. Escribe el borrador.
3. Pásalo por `ig-humano`. Los textos son cortos, así que el relleno se nota más
   aquí que en cualquier otra parte.
4. Corre `revisar_texto.py` con las palabras de búsqueda de la persona. Arregla
   cada FALLA. Decide en voz alta sobre cada OJO, no en silencio.
5. Entrega el bloque listo para copiar y luego el resumen:

```
TEXTO LISTO
trabajo:     A - el reel lleva el gancho
visible:     118 de 125 caracteres usados antes del corte
pedido:      uno, comentar CONTRATO
hashtags:    3
búsqueda:    "café de especialidad" en la línea 3, "catación" en la línea 5
revisión:    LISTO
```

No se publica nada. La persona lo pega.
