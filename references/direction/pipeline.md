# Pipeline de producción

> Cargar al empezar un proyecto. Cada etapa dice **qué módulo cargar** y **qué tiene que salir** antes de pasar a la siguiente. Principio rector: decidir en imagen y en blockout, generar video solo cuando ya no quedan decisiones.

| # | Etapa | Cargar | Sale | Créditos | Puerta de salida |
|---|---|---|---|---|---|
| 0 | **Brief** | `direction/reference-timeline.md` | Objetivo, público, duración, formato (9:16 por defecto en redes), plataforma, tono, restricciones (concurso, consentimiento), y **cada referencia de inspiración desglosada con timecode** (`timeline.py breakdown`), con su audio | 0 | El usuario confirma el brief y qué se toma de cada referencia |
| 1 | **Plan de planos** | `direction/shot-design.md`, `models/router.md` | `plan-de-planos.md`: cada plano con su intención, tamaño, lente, movimiento, acción, técnica, modelo, **referencias activas** y **audio del tramo** (música · efectos · ambiente · diálogo · silencio); agrupado en **secciones** de segundos enteros | 0 | Las duraciones suman bien y cada plano tiene técnica |
| 2 | **Biblia** | `direction/identity-and-assets.md`, `direction/continuity.md` | `biblia.md`: descripciones fijas en inglés, vestuario, sets y estados, props, luz por set, color, lente base, ejes, `stateIn`/`stateOut` | 0 | Cualquier prompt se puede escribir copiando bloques de la biblia |
| 3 | **Blockout** (si alguna sección lo necesita) | `direction/blockout.md`, `production/blender-kling-seedance.md` | Automático con `build_blockout.py`: video gris (ruta S), keyframes (ruta K), placas y `timeline.json`; cada plano asignado a la ruta K o a la ruta S | 0 | El usuario aprueba cámara, timing y ruta de cada plano |
| 4 | **Activos** | `models/image-models.md`, `prompting/templates.md` (E, F, G) | Hojas de personaje, sets por estado, props y fotogramas clave, cada uno aprobado | bajo (imágenes) | Cada activo pasa la rúbrica y el usuario lo aprueba |
| 5 | **Fichas de generación** | `prompting/principles.md`, la ficha del modelo, `direction/reference-timeline.md` | Una `prompt-card` por sección: **mapa temporal de referencias y audio**, prompt, medios recortados a su tramo, parámetros y cotización | 0 | Cotización presentada y **sí del usuario** |
| 6 | **Borrador** | `production/cost-protocol.md` | Seedance 2.5 `draft` a 480p (u otra prueba barata) | ≈ 3 cr/s | — |
| 7 | **Control de calidad** | `quality/qc-rubric.md` → `quality/diagnosis.md` si falla | `qc-report.md` con la puntuación y la decisión | 0 | ≥ 14/16 y ningún 0 |
| 8 | **Final** | ficha del modelo | Finalizar el borrador (`draft_job_id`) o regenerar en la resolución final | ≈ 7–16 cr/s | Pasa la rúbrica al ver el final |
| 9 | **Acabado** | `models/post-tools.md` | Montaje, correcciones de luz y color, escalado, lip-sync, sonido y gráficos | según la herramienta | Rúbrica sobre la pieza completa |

## Reglas de flujo

- **El primer envío de cada modelo y modo va solo:** se espera, se revisa y después se lanza el resto (`drama-ads`).
- **Una sección cada vez** hasta validar la técnica; después, las secciones que comparten técnica pueden ir en lote (`generate_video_batch`), cada una cotizada.
- **El usuario aprueba en tres puertas:** brief, blockout más activos, y cada gasto de video.
- Si el usuario ya tiene un video y quiere mejorarlo, se salta a la etapa 9 (`post-tools.md`).

## Atajos legítimos

| Proyecto | Atajo |
|---|---|
| Un solo plano | Etapas 0, 4, 5, 6, 7 y 8 (sin blockout) |
| Pieza sin personas recurrentes | La biblia se reduce a sets, luz y color |
| Planos fijos (fichas, insertos) | Imagen + parallax en post, sin video |
| Sección sencilla de 1–2 planos | Plantilla B con beats cronometrados, sin blockout |

## Organización del proyecto en disco

```
<proyecto>/
├── brief.md · plan-de-planos.md · biblia.md · presupuesto.md · qc-report.md
├── referencias/<persona>/        fotos originales (con consentimiento)
├── activos/                      hojas, sets, props y fotogramas aprobados (con su job id)
├── blockout/                     S1.mp4, S2.mp4 … y placas grises
├── fichas/                       prompt-card por sección
├── generaciones/                 borradores y finales descargados (S2_draft_v1.mp4 …)
├── qc/                           hojas de contacto y comparaciones
└── post/                         montaje, sonido y entregables
```
