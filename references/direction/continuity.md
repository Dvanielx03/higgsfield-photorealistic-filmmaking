# Continuidad entre planos y entre clips

> Cargar al planificar secciones y antes de generar cualquier clip que se corte con otro. La identidad de personajes y sets está en `identity-and-assets.md`; aquí está el **empalme**.

## 1. Tres tipos de empalme, tres técnicas

| Situación | Técnica correcta en Higgsfield | Por qué |
|---|---|---|
| **La misma toma continúa** sin corte (la cámara sigue) | `video_extension` (`forward`) del mismo modelo | Continúa el movimiento real. La salida repite el último fotograma del origen: recortarlo |
| **Corte de plano** dentro del mismo set (otro ángulo o tamaño) | Nuevo clip con las **mismas referencias** + **frame plate** del set como primera `image_references` | Fijar el fotograma como `start_image` en una costura la hace titilar («a pinned first frame makes the seam shimmer», `drama-ads`) |
| **Plano único que debe arrancar en una composición exacta** (no empalma en continuidad) | Fotograma clave aprobado como `start_image` | El fotograma fija cara, luz y encuadre; el prompt describe solo el movimiento |

> [!IMPORTANT]
> **No** usar el último fotograma de un clip como `start_image` del siguiente para empalmar en continuidad: es la técnica que más falla en las costuras. Para continuar una toma, extensión. Para cortar a otro plano, referencias y corte en movimiento.

## 2. Diseñar las costuras (reglas de `drama-ads`)

- **En cada costura cambia algo visible:** tamaño, sujeto o ángulo. Dos beats seguidos del mismo sujeto y la misma vista se funden en uno.
- **El clip siguiente abre en la consecuencia del anterior**, nunca con «continuing from the previous shot».
- **Cambio de lugar o de tiempo:** abrir en plano general.
- **Cortar en movimiento** (`cut on the move`) esconde el empalme.
- Las posiciones se describen **relativas a un ancla del set** (la mesa, la puerta), no como «frame left/right». Llevar en la biblia un `stateIn` / `stateOut` por clip: dónde está cada cosa al entrar y al salir.
- **Planos mínimos:** 1,5 s (2 s con acción física); en una costura, nunca un plano de menos de 1 s (un «stub»).

## 3. Raccords que revisar en cada empalme

| Raccord | Qué comprobar |
|---|---|
| Posición | Personas y objetos donde el `stateOut` anterior los dejó |
| Mirada | Hacia dónde mira cada personaje al salir y al entrar |
| Dirección en pantalla | Sale por la derecha → entra por la izquierda |
| Eje de 180° | La cámara no cruza el eje en un diálogo |
| Luz | La fuente sigue en el mismo lugar del mundo (no del cuadro) y con la misma temperatura |
| Vestuario y props | Mismo estado (manchado, abierto, en la mano izquierda…) |
| Sonido | Ambiente continuo por debajo del corte |

## 4. Luz y color entre clips

- **Luz descrita por su fuente en el mundo** («the window behind her»), no por su lado del cuadro: en un contraplano el lado cambia, la fuente no.
- **Mismo bloque de luz y de color, literal**, en todos los prompts de un set.
- **Si se usa Cinema Studio 4.0,** `light_custom` idéntico en todos los planos del set (ver `models/cinema-studio.md`).
- **Diferencias residuales:** se corrigen con `grade-hf` o `/color-grade` dentro de Higgsfield, o con etalonaje en post. No se corrigen regenerando.

## 5. Ritmo de la pieza

- Primeros planos y planos medios dominan en vertical; un inserto cada 3–4 planos refresca.
- **Gancho:** la acción entre los segundos 1 y 3, con las caras principales visibles antes del segundo 3 (`drama-ads`).
- Fundidos, cámara lenta, títulos y texto: **siempre en montaje**, nunca en el prompt.

## 6. Comprobación de costuras (control de calidad)

- Localizar los cortes con detección de escena y mirar los fotogramas a ambos lados de cada uno.
- Revisar cada costura a 4 fps: `bash scripts/frames.sh sheet clip.mp4 seam.png 4`.
- Contar personas en el fotograma central de cada plano.
- Para continuidad estricta: `frames.sh last` del clip A y `frames.sh first` del clip B, comparados con `frames.sh compare`.
