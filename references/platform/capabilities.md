# Capacidades de la plataforma: lo verificado y lo que no existe

> Cargar al empezar un proyecto, o cuando haya dudas sobre si algo se puede hacer en Higgsfield. **Regla: si no está en esta tabla ni en el esquema del modelo (`models_explore action=get`), no se promete.**
> Verificado contra el conector de Higgsfield el 24-nov-2026.

## Herramientas del conector que usa esta skill

| Para | Herramienta | ¿Gasta o escribe? |
|---|---|---|
| Saldo y plan | `balance` | No |
| Catálogo y esquema de modelos | `models_explore` (`list`, `get`, `search`, `recommend`) | No |
| Cotizar | `estimate_video_cost`, `estimate_image_cost` (devuelven un `quote_ref`) | No |
| Subir medios | `media_upload` → PUT → `media_confirm` (o `media_import_url`) | Escribe (sube archivos) |
| Generar | `generate_video`, `generate_image`, `generate_*_batch` | **Gasta** |
| Escalar | `upscale_video` (`topaz` o `bytedance`), sin cotización previa | **Gasta** |
| Elements | `elements_search`, `elements_get` (leer) · `elements_create`, `elements_assign`, `elements_update` (escribir) | Escribir requiere el sí |
| Workflows oficiales | `get_workflow_instructions`, `get_workflow_bundle_file` | No |
| Presets y recetas | `get_presets`, `get_preset_instructions` (leer); `execute_preset` (**gasta**) | — |
| Estado de trabajos | `show_generations`, `jobs_wait` | No |

**Con el CLI** (skill oficial `higgsfield-generate`), los equivalentes son `higgsfield generate cost …`, `higgsfield model get <id> --json`, `higgsfield upload create` y `higgsfield account status`.

## Workflows oficiales a los que delegar

No se reimplementan: se cargan con `get_workflow_instructions` y se siguen. Esta skill aporta la dirección, la continuidad y el control de calidad alrededor.

| Workflow | Cuándo |
|---|---|
| `character-sheet` | Hojas de personaje, caras de casting, vestuario y looks |
| `drama-ads` | Micro dramas con personajes que actúan y hablan (solo si el usuario lo elige con `/drama-ads`); sus reglas de clip están resumidas en `models/seedance-2-5.md` |
| `angles-hf` | Convertir una toma de una cámara en multicámara (`/angles`) |
| `lighting-hf` · `grade-hf` | Re-iluminar o re-etalonar un clip (comandos `/<look>-hf`) |
| `higgsfield-enhance-video` | Escalado fiel 1:1 con Kling 4.0 |
| `video-sound-design` · `video-montage` | Efectos de sonido, montaje y subtítulos |
| `/3d-jutsu` | Nuevos ángulos de un mismo set |
| `/use-blender` | Instrucciones de Higgsfield para trabajar con Blender |

## Verificado como disponible

- **Seedance 2.5:**
  - borrador 480p finalizable durante 7 días;
  - `video_references` (blockout) y `audio_references` (voz real);
  - `video_edit` y `video_extension`;
  - 4–30 s, hasta 4K y 9:16.
- **Cinema Studio 4.0:** iluminación personalizada por parámetro (`light_custom`).
- **Cinema Studio 3.5:** multiplano con un prompt por plano (`multi_prompt`).
- **Kling 4.0:** fotogramas clave ordenados, edición de video, HDR y 4K.
- **Elements:** en los modelos de imagen y video listados en `direction/identity-and-assets.md`.
- **Soul ID:** para modelos de imagen Soul.
- **Correcciones y acabado:** lip-sync (`sync_so`), recorte de sujeto (`sam_3_video`), reencuadre (`reframe`) y escalado (Topaz, ByteDance o Kling 4.0 con prompt).
- **Workflows de corrección:** re-iluminación (62 looks) y re-etalonaje (34 looks).
- **Sonido:** efectos de una biblioteca con licencia (Epidemic Sound) y música (`elevenlabs_music_v2`).

## No disponible o no documentado (no prometer)

| Supuesto | Realidad verificada |
|---|---|
| «Elements sirve para Seedance 2.5 y Cinema Studio 4.0» | **No están en la lista de modelos con Elements.** Usar hojas como `image_references` |
| «Puedo elegir cámara y lente de Cinema Studio 4.0 por id» | Los ids existen en el esquema, pero **no hay forma de descubrir sus valores** desde el conector |
| «Soul ID funciona en video» | Solo documentado para modelos de imagen Soul |
| «Seedance corta exactamente en el segundo que escribo» | La mitad de los cortes cae a ±0,33 s y uno de cada tres se desvía 0,5–2,8 s |
| «Encadenar el último fotograma como `start_image` da una costura limpia» | El workflow oficial dice que hace titilar la costura. Usar extensión o frame plates |
| «Puedo cotizar un escalado» | `upscale_video` no admite cotización previa |
| «Los modelos escriben bien el texto en pantalla» | Evitar: el texto va en post |
| «Puedo usar caras de famosos o marcas» | `ip_detected`; prohibido |
| «Kling 3.0 usa Elements sin más» | Solo con `start_image` explícito |
| «Cinema Studio 3.5 entiende el prompt en inglés por defecto» | `prompt_language` es `zh` por defecto: pasar `en` |

## Plataforma, regiones y canales

- **Lo ilimitado del plan no funciona desde Claude Code.** El conector rechaza `use_unlim: true` (sin cobrar) y dice que está disponible en Claude chat, Claude Cowork y ChatGPT; el centro de ayuda añade la web. Si el usuario solo autoriza ilimitados, la skill prepara los prompts y él genera allí (ver `plan-and-credits.md`).
- **Seedance 2.5 Flash y el 4K de Seedance 2.5:** «no disponibles en EE. UU.» según el changelog. Si el conector los ofrece, cotizar y comprobar.
- **Draft Mode** de Seedance: el detalle fino no está documentado en el centro de ayuda; el esquema del conector sí lo declara (`draft`, `draft_job_id`).
- **Cinema Studio 3.5** tiene un Director IA con Claude dentro de la web. Esta skill no lo usa: trabaja con el conector.
- **No existen o no están documentados:** «Soul Location», «Higgsfield Assist» y la extensión de Kling hasta 2 minutos («coming soon»).

## Antes de cada producción

1. `balance`: comprobar plan y saldo. **Si la cuenta conectada no es la del plan contratado, avisar antes de nada.**
2. `models_explore action=get` de cada modelo que vaya a usarse.
3. Si un workflow oficial cubre la tarea, cargarlo.
