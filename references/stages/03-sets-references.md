# Etapa 3 · Diseño de escenarios y referencias visuales

**Objetivo:** sets creíbles y habitados, personajes con identidad fija y referencias listas para generar. Módulos: `direction/identity-and-assets.md`, `models/image-models.md`, `prompting/templates.md` (E, F, G).

## Requisitos
- **Diseño de set por capas:**
  - **primer término**: objetos cerca de cámara que dan profundidad (respaldo de silla, planta, borde de mesa, cristal);
  - **plano medio**: donde ocurre la acción;
  - **fondo**: pared con información del lugar (pizarra, ventana, estantería, cuadros, puerta), nunca vacía.
- **Objetos con propósito:** cada prop dice algo de quien usa el lugar (portátiles, tazas, papeles, una chaqueta en una silla). Distribución coherente con el uso: las sillas alrededor de la mesa y la lámpara encima.
- **Luz diseñada en el set:** la fuente motivada está en el decorado (lámpara, ventana, puerta con contraluz, pantallas) y se anota su dirección en el mundo.
- Hojas de personaje aprobadas (con consentimiento) y descripción fija en la biblia.
- Un set por estado (oscuro, encendido…), derivado por edición del maestro.
- **Canal de generación de imágenes confirmado:**
  - antes de planear imágenes «gratis», comprobar desde dónde funcionan los ilimitados;
  - desde Claude Code no funcionan (`platform/plan-and-credits.md`): ahí la skill prepara los prompts y el usuario genera en la web, en Claude chat o en Cowork.

## Errores que se deben evitar
| Error | Regla |
|---|---|
| Salas vacías o «de render» | Mínimo 3 capas y al menos 5 objetos de uso en un interior; pedir que el lugar «se sienta habitado» |
| Elementos incoherentes con la escena (objetos sin función, escalas raras) | Cada objeto se justifica por quién usa el lugar; escalas reales en metros |
| Paredes lisas detrás de las caras | El fondo detrás de un primer plano tiene un elemento de lectura (ventana, pizarra, cuadro, profundidad) |
| Luz que cambia de lado entre planos | La luz se describe por su fuente en el mundo y se mantiene en todo el set |
| Planear imágenes ilimitadas desde un canal que no las permite | Verificar el canal antes del presupuesto |

## Criterios de aprobación (puerta)
- [ ] Cada set tiene las tres capas y su fuente de luz definidas en el blockout y en la biblia.
- [ ] Hojas de personaje y sets maestros pasan la rúbrica (criterios 1, 3 y 7) y los aprueba el usuario.
- [ ] Está claro qué activos genera el usuario (y dónde) y cuáles la skill con créditos aprobados.
