# Etapa 5 · Generación audiovisual con IA

**Objetivo:** convertir el animatic aprobado en clips que pasen la rúbrica, con el mínimo de créditos. Módulos: `models/router.md` + la ficha del modelo, `production/blender-kling-seedance.md`, `production/cost-protocol.md`, `direction/reference-timeline.md`.

## Requisitos
- Animatic aprobado (etapa 4) y activos aprobados (etapa 3).
- Una ficha (`templates/prompt-card.md`) por generación, con:
  - el mapa temporal de referencias y audio;
  - el prompt (esqueleto de `scripts/prompt_skeleton.py`, rellenado con la biblia);
  - parámetros explícitos (`aspect_ratio`, `resolution`, duración entera);
  - la cotización.
- **Sí del usuario** por generación o por lote cotizado. Primer clip de cada modelo y modo, solo.
- **Ruta K (Kling 4.0):**
  - **una generación por plano** (`--model kling-shots`), con los keyframes fotorrealistas de ese plano;
  - nunca el blockout como video de referencia;
  - duración ≥ 3 s, que se recorta en montaje;
  - un plano pensado para Seedance (con la cola de diálogo de ≥ 4 s) se acorta a lo que se usa más un margen: Kling no tiene esa regla y cada segundo cuesta.
- **Producción solo con Kling:** cada proyecto escribe su `adaptacion-kling.md` con la tabla plano a plano (lo que se usa, lo que se genera, los keyframes que se suben, las acciones del tramo y el riesgo) y el presupuesto con techo, siguiendo `production/blender-kling-seedance.md` §6b.
- **Ruta S (Seedance 2.5):** blockout como `video_references`, hojas como `image_references`, borrador a 480p primero.

## Errores que se deben evitar
| Error | Regla |
|---|---|
| Generar antes de aprobar el animatic | Bloqueado: la puerta de la etapa 4 manda |
| Usar precios de memoria o de terceros | Cotizar siempre: los precios cambian (Kling 4.0 pasó de 30 a 112,5 créditos por 30 s a 1080p en un mes) |
| Cuenta conectada distinta del plan | `balance` antes de presupuestar |
| Mandar a Kling una sección con cortes como un solo clip | Kling hace tomas continuas: una generación por plano |
| Fijar el último fotograma como `start_image` en una costura de Seedance | Extensión de video o frame plate (`direction/continuity.md`) |

## Criterios de aprobación (puerta)
- [ ] Cada clip pasa la rúbrica (`quality/qc-rubric.md`) con ≥ 14/16 y ningún 0.
- [ ] El libro de gasto cuadra con lo aprobado.
- [ ] Los clips cubren todos los tramos del montaje con colas para cortar en movimiento.
