---
name: ig-auditoria
description: >-
  Revisa lo que la persona ya publicó: qué reels funcionaron de verdad, por qué,
  y qué dejar de hacer. Úsala cuando peguen sus estadísticas de Instagram o sus
  publicaciones pasadas y pregunten "qué está funcionando", "por qué le fue mal
  a este", "lee mis estadísticas", "audita mi contenido", o quieran saber de qué
  hacer más.
---

# ig-auditoria

La única fuente honesta de lo que funciona para una cuenta es esa cuenta. Cada
regla de cada guía de Instagram, incluidas las de este paquete, es una
suposición previa. Las últimas 30 publicaciones de la persona son la evidencia.

## Lo que necesitas

Pide lo que la persona tenga:

- Estadísticas por publicación: vistas, alcance, interacciones, tiempo de
  reproducción, guardados, veces compartido, seguidores ganados y qué parte del
  alcance vino de gente que no sigue la cuenta. Los pantallazos sirven.
- O la gráfica de retención de sus mejores y peores reels recientes. Ese
  pantallazo vale más que todo lo demás junto.
- O solo las publicaciones y sus vistas, que alcanza para una primera pasada.

Si esta sesión tiene conectada una herramienta que lee las estadísticas de la
cuenta, úsala en vez de pedir pantallazos, y di de dónde salieron los números.

Lee también el historial si existe (`historial.md` en los archivos del proyecto,
o `~/.claude/instagram/historial.md` en Claude Code), porque ahí está qué
fórmula de gancho usó cada publicación.

## Qué medir de verdad

Las vistas solas son el número menos útil de la página, porque dependen sobre
todo de cuánta gente ya sigue la cuenta. Calcula esto en su lugar y muestra las
cuentas:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Veces sobre lo normal** | vistas / mediana de vistas de la propia cuenta | si fue un éxito real o un día normal |
| **Alcance de no seguidores** | % del alcance que vino de gente que no sigue | si viajó o no |
| **Retención a los 3 s** | quienes siguen a los 3 s / quienes empezaron | si funcionó el gancho. Esta es la nota del gancho. |
| **Tiempo medio de reproducción** | directo de las estadísticas | si funcionó la mitad |
| **Envíos por alcance** | veces compartido / alcance | la señal más fuerte que te puedes ganar. Enviar es poner tu nombre detrás. |
| **Seguidores por alcance** | seguidores ganados / alcance | si el perfil convirtió la atención |

Ordena por veces sobre lo normal y por envíos por alcance, no por vistas. Un reel
con 4.000 vistas y 90 envíos le ganó al de 60.000 vistas y 11.

## Luego busca el patrón

Con los cinco de arriba y los cinco de abajo lado a lado, busca qué los separa,
y prepárate para concluir algo que a la persona no le va a gustar:

- **Retención a los 3 segundos.** Si los de arriba y los de abajo se diferencian
  aquí, es el gancho y nada más, y todo lo que viene después es distracción.
- **Fórmula de gancho.** ¿Qué números de `ganchos.json` (de `ig-reel`) están
  entre los cinco de arriba?
- **Formato.** Reel, carrusel, imagen sola.
- **Duración.** Agrupa en menos de 15 s, de 15 a 30 s, de 30 a 60 s, más de 60 s.
- **Tema.**
- **Si la persona respondió comentarios en la primera hora.**
- **Día y hora.** Revísalo **de último** y solo si lo demás no muestra nada.
  Casi nunca es la causa y es donde la gente quiere que esté.

Di el hallazgo como una afirmación con la evidencia al lado, y di qué tan seguro
es. Con 30 publicaciones se puede ver un patrón. Con 6 no, y decirlo es mejor
que inventar uno.

## La distinción que ahorra meses

**Un reel con vistas y sin seguidores nuevos no es un reel fallido, es un
problema del perfil.** Un reel sin vistas es un problema del gancho. Separa las
dos cosas antes de recomendar nada. Si el alcance de no seguidores es alto y los
seguidores por alcance son bajos, deja de reescribir ganchos y pasa a
`ig-perfil`.

## Resultado

```
AUDITORÍA  ·  31 publicaciones  ·  12 jun - 5 sep  ·  mediana de vistas 4.100

LOS 5 DE ARRIBA POR VECES SOBRE LO NORMAL
  18,2x  #3  Nadie te dice        74.600 vistas  62% no seguidores  retención@3s 71%  128 envíos
   6,4x  #1  Confesión de costo   26.300 vistas  48% no seguidores  retención@3s 64%   71 envíos
  ...

LOS 5 DE ABAJO
   0,3x  #11 Lista con favorito    1.200 vistas   9% no seguidores  retención@3s 31%    2 envíos
  ...

LO QUE DICEN LOS DATOS
1. La retención a los 3 segundos lo explica todo. Los de arriba promedian 66%,
   los de abajo 33%. Todo lo demás que te preocupa viene después de los dos
   primeros segundos.
2. Las publicaciones donde tú quedabas mal: promedio 8,1x contra 0,9x de todo lo
   demás. n=5. La señal más fuerte de aquí, y no hay comparación.
3. Las listas de herramientas tienen vistas y nada más. Mucho alcance, ningún
   envío, ningún seguidor. Tres de tus cinco de abajo.
4. El día de la semana no muestra nada. Tus promedios de martes y viernes están
   dentro del ruido. Deja de optimizarlo.

DEJA DE HACER: listas.
HAZ MÁS: las que tienen un costo que pagaste y una cifra.
```

(Esto es un ejemplo de formato; los números salen de los datos de la persona.)

Luego pásale las conclusiones a `ig-plan` para que la próxima semana se arme con
la evidencia propia y no con valores por defecto, y a `ig-viral` para que el
archivo de referentes se filtre por las fórmulas que funcionan para esta cuenta
en particular.
