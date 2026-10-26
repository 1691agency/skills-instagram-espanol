---
name: ig-perfil
description: >-
  Califica un perfil de Instagram sobre 100 con una rúbrica de 12 puntos y
  reescribe las partes que pierden puntos: campo del nombre, bio, enlace,
  destacadas, los tres fijados y la cuadrícula. Úsala cuando digan "optimiza
  mi perfil", "arregla mi bio", "califica mi Instagram", "por qué no me
  siguen", o cuando peguen su perfil y pregunten cómo se ve.
---

# ig-perfil

Casi todo el mundo optimiza lo que no es. El perfil no es una vitrina que la
gente recorre. Es una **pantalla de decisión**, a la que se llega desde un solo
reel, y tiene unos tres segundos para responder una pregunta: ¿aquí hay más de
eso, y es para mí?

Si existe la voz de la marca (`voz.md` en los archivos del proyecto, o en
`~/.claude/instagram/voz.md` en Claude Code), léela antes de reescribir.

## Lo que necesitas

Pide que pegue o mande pantallazo de: el campo del nombre, el @usuario, la bio,
a dónde lleva el enlace, los nombres de las destacadas, qué está fijado y las
primeras nueve portadas de la cuadrícula. Un pantallazo de la parte de arriba
del perfil más las dos primeras filas de la cuadrícula alcanza para una primera
pasada.

No inicies sesión en Instagram por la persona.

## Califícalo

Lee `rubrica.json` en esta carpeta. Doce puntos, 100 en total, cada uno con cómo
se ve la nota completa y cómo suele fallar. Califica cada punto, muestra la
tabla y da el total. Sé honesto. La mayoría de perfiles quedan entre 30 y 49 en
la primera pasada, y un puntaje generoso no sirve de nada.

```
PUNTAJE DEL PERFIL  38/100

  campo del nombre     2/12   solo el nombre, ninguna palabra que alguien busque
  bio, primera línea   3/12   tres sustantivos y un emoji de café
  tres fijados         0/10   no hay nada fijado
  destacadas           2/8    "Random", "Vida", "2023"
  cuadrícula legible   4/8    seis de nueve portadas son una cara a mitad de frase
  ...
```

## Luego reescribe, en este orden

Arregla de mayor a menor según los puntos perdidos. No reescribas todo de una
vez: la persona tiene que ir a cambiar cada cosa a mano.

**1. El campo del nombre (unos 30 caracteres).** La línea en negrita debajo de
la foto, no el @usuario. Es el campo que lee el buscador de Instagram, y la
mayoría de cuentas pone solo un nombre. El formato que funciona:
`{Nombre} | {qué haces, en palabras que se buscan}`. Da tres opciones.

**2. La primera línea de la bio.** Para quién es esto y qué cambia. No un cargo,
no adjetivos, no una lista de identidades separadas por rayas. El resto de los
150 caracteres lleva una prueba o una oferta simple.

**3. Los tres fijados.** Tres espacios, tres trabajos distintos: la mejor
prueba, la explicación más clara de la oferta y la mejor presentación de la
persona. Es el arreglo que más rinde de todo el perfil y toma cuatro toques. Una
cuadrícula sin fijados muestra lo último que se publicó, que es echarlo a la
suerte.

**4. Las destacadas.** De cuatro a seis, con los nombres de las preguntas que
hace un comprador: Precios, Resultados, Cómo funciona, Quiénes somos. No
"Random". Borra el resto.

**5. El enlace.** Un destino que coincida con lo que acaba de prometer la bio.
Se permiten cinco; dos ya es un menú, y un menú convierte peor que una puerta.

**6. Las portadas de la cuadrícula.** Las primeras nueve en miniatura. Las
portadas de los reels se escogen, no se dejan en el primer cuadro que salió.
Cuatro palabras de texto en una portada hacen que la cuadrícula se entienda de
un vistazo.

## Resultado

La tabla de puntajes y luego las reescrituras como bloques listos para copiar,
en orden de lo que más urge, cada uno pasado por `ig-humano`. Vuelve a calificar
al final y muestra la diferencia con honestidad. Si la reescritura llega a 84 y
no a 98, di 84, y di qué necesita el resto, que casi siempre es una cuadrícula,
la costumbre de subir historias y una publicación fijada que todavía no existe.
Nada de eso es una reescritura.

Esta habilidad no guarda nada en Instagram. La persona edita cada campo.
