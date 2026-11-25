# Etapa 4 · Animatic y previsualización en Blender

**Objetivo:** un animatic que muestre **cómo será el video final**, segundo a segundo: cámara, acciones, entorno, luz, gráficos y ritmo. No basta con colocar personajes en un decorado. Módulos: `direction/blockout.md`, `production/blender-kling-seedance.md`.

## Requisitos
- **Plan JSON por escena** con todo lo que el constructor (`scripts/blockout/build_blockout.py`) admite:
  - set por capas;
  - luces con `engine: "EEVEE"` cuando la luz cuenta la historia (contraluz, lámpara, cambio de luz);
  - personas con `yaw`, `head_yaw` (miradas), `height` (sentarse o levantarse) y `hand_keys` (gestos);
  - objetos animados con `pivot` (puertas), `parent` (algo en la mano o sobre una cabeza), cambios de color y `visible`;
  - **textos 3D** para los gráficos del guion (pensamientos, palabras, nombres), para que el ritmo se vea aunque el diseño final vaya en post;
  - cámaras con movimiento, `lens` animado si hay zoom y `handheld` si aplica;
  - `auto_keyframes: true` si la escena irá por la ruta K.
- **Resolución del formato final** (p. ej. 1920×1080 para 16:9) y revisión con las guías de la banda de destino.
- **Animatic completo** en el orden del montaje, sin cartelas: los momentos de imagen o post también se previsualizan (fotos fijas con movimiento, fichas con texto 3D).
- Reproducir y revisar cada escena entera, no solo los keyframes.

## Revisión obligatoria (hoja de contacto a 2–4 fps, `scripts/frames.sh sheet`)
| Comprobación | Falla si… |
|---|---|
| Oclusión | Un objeto o figurante tapa la cara del protagonista sin intención |
| Encuadre | Un personaje que debe verse sale del cuadro o queda cortado por el borde de la banda |
| Mirada | Una persona mira hacia el lado equivocado (revisar el cono de la cara) |
| Acción | Hay segundos sin acción visible donde el guion pide algo |
| Entorno | Un plano muestra solo pared o suelo vacíos |
| Cámara | Un movimiento atraviesa paredes u objetos, o no termina donde debe |
| Tiempo | Los cortes no caen donde dice el plan (`scripts/timeline.py drift`) |
| Continuidad | Personas, objetos o luz cambian de sitio entre planos sin motivo |
| Luz | Una cara importante queda a contraluz o un cambio de luz salta donde no toca |
| Gráficos | Un texto se sale de la banda, queda detrás de una cabeza o se lee al revés |

## Errores que se deben evitar
- Cartelas en lugar de planos, figurantes inmóviles como estatuas, todas las cámaras a la misma altura.
- Juzgar la luz con el motor plano (Workbench): si la luz importa, EEVEE.
- Dar el animatic por bueno sin verlo completo de principio a fin.
- **Claves de luz en el mismo fotograma.** A 24 fps, dos claves a menos de 0,042 s caen en el mismo fotograma y la segunda pisa a la primera: un parpadeo se convierte en una rampa. El constructor avisa (`AVISO luz`) y deja las luces en interpolación lineal.
- **Textos que se leen al revés.** Un texto 3D se lee desde un solo lado. Si un plano lo mira desde el lado contrario (contraplano, órbita de más de 90°), se duplica girado 180° y cada copia se muestra solo en su plano (`visible`).
- **Gráficos fuera de la banda.** En una toma cercana, la banda 2.39:1 deja muy poco alto útil a la distancia del texto. Se coloca cada texto en el aire de mirada de quien habla, a la profundidad elegida, y mirando a la cámara (`rotation` en Z).
- **Cuarto blanco que sale gris.** Un ciclorama solo se ve blanco si suelo, curva y pared tienen la misma luminancia; con superficies desiguales aparece una línea de horizonte. Se igualan con `emission`.
- **Caras a contraluz en los primeros planos.** Con la luz de la sala detrás, la cara queda negra. Se añade una llave suave motivada por una fuente del set (ventana, pantalla, el propio objeto que brilla).
- **Gráficos que el guion no pide.** Antes de cerrar, cotejar cada texto 3D con la columna de fabricación del guion aprobado. Lo que el guion deja solo en la voz en off no se escribe en pantalla, aunque un análisis de referencias lo sugiera.
- **Plano «sucio» que en realidad es un plano de dos.** Para que el compañero quede en primer término, desenfocado y cortado por el borde, la cámara entra por su lado y más cerca de él que del protagonista; si están a la misma distancia, solo es un plano de dos.

## Criterios de aprobación (puerta)
- [ ] Todas las comprobaciones de la tabla pasan en todas las escenas.
- [ ] El animatic completo dura lo que el montaje y se ve sin cartelas.
- [ ] **El usuario aprobó el animatic.** Sin esa aprobación no se genera video.
