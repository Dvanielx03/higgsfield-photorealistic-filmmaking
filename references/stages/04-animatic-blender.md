# Etapa 4 · Animatic y previsualización en Blender

**Objetivo:** un animatic **simple** que muestre el **flujo del video** segundo a segundo con objetos: cámara, posiciones, acciones, entorno y ritmo. Es una herramienta para decidir el encuadre y el tiempo, no un avance del look final. No basta con colocar personajes en un decorado, pero tampoco se pinta luz ni texto. Módulos: `direction/blockout.md`, `production/blender-kling-seedance.md`.

## Requisitos
- **Look simple por defecto:**
  - motor plano (`engine: "WORKBENCH"`) con colores de objeto y fondo neutro;
  - **sin luces, textos 3D, brillos (`emission`) ni fondos de color**.
  - La luz, los gráficos y el color se escriben en el plan de planos y se resuelven en generación y post. Solo se añaden al animatic si el usuario lo pide (ver el último apartado).
- **Plan JSON por escena** con lo que el constructor (`scripts/blockout/build_blockout.py`) admite para el flujo:
  - set por capas;
  - personas con `yaw`, `head_yaw` y `head_pitch` (miradas), `height` (sentarse o levantarse) y `hand_keys` (gestos);
  - objetos animados con `pivot` (puertas), `parent` (algo en la mano o sobre una cabeza) y `visible`. Lo que en el final será un gráfico o un efecto se marca con un objeto simple: una esfera para «la idea», una franja para la luz bajo una puerta;
  - cámaras con movimiento, `lens` animado si hay zoom y `handheld` si aplica;
  - `auto_keyframes: true` si la escena irá por la ruta K.
- **Resolución del formato final** (p. ej. 1920×1080 para 16:9) y revisión con la banda de destino.
- **Animatic completo** en el orden del montaje, sin cartelas: los momentos de imagen o post también se previsualizan (por ejemplo, la ficha como plano del personaje).
- **Sobre el video, nada que distraiga:** sin título ni timecode; como mucho, el nombre de la escena en la barra inferior.
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
| Tiempo | Los cortes y las entradas caen donde dice el plan y el usuario no siente que algo tarde de más (`scripts/timeline.py drift`) |
| Continuidad | Personas u objetos cambian de sitio entre planos sin motivo |

## Errores que se deben evitar
- Cartelas en lugar de planos, figurantes inmóviles como estatuas, todas las cámaras a la misma altura.
- **Convertir el animatic en un look final.** Luz, textos y fondos de color alargan cada ronda y distraen del flujo, que es lo que se aprueba aquí.
- **Una entrada que tarda.** Si el protagonista aparece después de unos 3 s, el gancho se pierde; se acorta la escena previa antes de alargar las demás.
- Dar el animatic por bueno sin verlo completo de principio a fin.
- **Plano «sucio» que en realidad es un plano de dos.** Para que el compañero quede en primer término, desenfocado y cortado por el borde, la cámara entra por su lado y más cerca de él que del protagonista; si están a la misma distancia, solo es un plano de dos.
- **Acciones o elementos que el guion no pide.** Cotejar cada acción y cada marcador con la columna de fabricación del guion aprobado. Lo que el guion deja solo en la voz en off no se pone en pantalla, aunque un análisis de referencias lo sugiera.

## Solo si el usuario pide luz o gráficos en el animatic
- **Motor:** `engine: "EEVEE"` con `lights[]`. Workbench no sirve para juzgar la luz.
- **Claves de luz en el mismo fotograma:**
  - a 24 fps, dos claves a menos de 0,042 s caen en el mismo fotograma y la segunda pisa a la primera, así que un parpadeo se convierte en una rampa;
  - el constructor avisa (`AVISO luz`) y deja las luces en interpolación lineal.
- **Caras a contraluz:** se añade una llave suave motivada por una fuente del set.
- **Textos que se leen al revés:**
  - un texto 3D se lee desde un solo lado;
  - si otro plano lo mira desde el lado contrario, se duplica girado 180° y cada copia se muestra solo en su plano.
- **Gráficos fuera de la banda:** cada texto va en el aire de mirada de quien habla y mirando a la cámara (`rotation` en Z).
- **Cuarto blanco que sale gris:** suelo, curva y pared con la misma luminancia (`emission`); si no, aparece un horizonte.

## Criterios de aprobación (puerta)
- [ ] Todas las comprobaciones de la tabla pasan en todas las escenas.
- [ ] El animatic completo dura lo que el montaje, se ve sin cartelas y con el look simple.
- [ ] **El usuario aprobó el animatic.** Sin esa aprobación no se genera video.
