# Herramientas de corrección y acabado dentro de Higgsfield

> Cargar cuando un plano casi aprobado tenga un defecto **local** (luz, color, resolución, encuadre, lip-sync, fondo, duración) o al llegar a la postproducción. Regla de oro: **arreglar es más barato que regenerar**.
> Fuente: workflows oficiales del conector (`lighting-hf`, `grade-hf`, `angles-hf`, `higgsfield-enhance-video`, `video-sound-design`, `video-montage`) y esquemas, verificados el 24-nov-2026.

| Necesito… | Herramienta | Modelo / vía | Restricciones verificadas |
|---|---|---|---|
| **Cambiar la luz** de un plano ya hecho | Workflow `lighting-hf` (62 looks) | `seedance_2_5` · `video_edit` | 4–30 s; el prompt del preset no se reescribe (solo se añade una nota de luz al final); `generate_audio: false` y después se devuelve el audio original; 720p por defecto |
| **Cambiar el etalonaje** | Workflow `grade-hf` (34 grades) | `seedance_2_5` · `video_edit` | Solo color; igualar una película completa es `/color-grade`; el workflow prohíbe LUTs y ffmpeg para esto |
| **Más ángulos** desde una toma de una cámara | Workflow `angles-hf` | `seedance_2_5` · `video_edit` | Toma continua de 4–30 s; lista de planos con lentes; 2–14 planos de 0,5 s mínimo; máximo 2 primeros planos de cara |
| **Alargar** una toma | — | `seedance_2_5` · `video_extension` (`forward`/`backward`) | La salida repite el último fotograma del origen: recortarlo |
| **Escalar fiel 1:1 con prompt** | Workflow `higgsfield-enhance-video` | `kling4_0` · `video-edit` | Entrada ≥ 720 px; partes de ~15 s; 24 fps; ≈ 4 cr/s a 1080p; control de calidad con SSIM |
| **Escalar sin prompt** | `upscale_video` | `topaz` (1080p/2160p, por relación de aspecto) o `bytedance` (1080p/2k/4k, necesita ancho y alto del origen; más de 30 fps duplica el costo) | Sin cotización previa posible: la herramienta no la admite. Avisar al usuario de que el costo se conoce al ejecutar |
| **Reencuadrar** (p. ej. 16:9 → 9:16) | `reframe` | — | 480p–1080p; hasta 2 `image_references` y un `start_image` opcional |
| **Lip-sync** a un audio real | `sync_so` | `input_video` + `input_audio` | `sync_mode` (`bounce`, `loop`, `cut_off`, `silence`, `remap`); con varios hablantes, un `segments` por turno, cada uno con su `active_speaker_detection` (fotograma y coordenadas de quien habla) |
| **Personajes que hablan** a partir de imágenes | `intone` (Higgsfield Intone, hasta 30 s) u otras opciones de Lipsync Studio (Veo 3.1, Kling Avatars 2.0, Higgsfield Speak 2.0…) | `intone`: `character_images`, `location_image`, `audio_references` | Comprobar el esquema con `models_explore`; probar contra Seedance 2.5 + `audio_references` en borrador |
| **Transferir movimiento real** grabado a los personajes | Genjutsu Motion Transfer | `hf_mult_motion_control` | Video de 4–30 s y hasta 30 imágenes; conserva el movimiento, la cámara y el timing. Comprobar si admite 9:16 |
| **Cambiar el personaje o un objeto** de un video | Recast · Genjutsu Object Swap | `hf_mult_replace_object` | Imágenes de referencia + un video de origen |
| **Recortar sujeto** (texto detrás de la persona, composición) | `sam_3_video` | — | Un solo video de entrada; `apply_mask`, `frames_count` |
| **Diseño sonoro** | Workflow `video-sound-design` | Biblioteca Epidemic Sound primero; `seed_audio` de respaldo | Prompt de efecto: `<sound>, <material and size>, <distance>, <space>, isolated, no music, no voice, about <n> seconds`. Niveles: hero entre −2 y −4 dB, detalles entre −12 y −18, ambientes entre −18 y −24, efectos 17–23 dB por debajo de la voz. Master a −14 LUFS (YouTube e Instagram) o −12 (TikTok), true peak ≤ −1 dBTP |
| **Música** | — | `elevenlabs_music_v2` con `force_instrumental` (según `drama-ads`) | Duración = película + 5 s; unos 10 LU por debajo del diálogo; sin nombres de artistas |
| **Montaje y subtítulos** | Workflow `video-montage` | — | Cortes secos por defecto, concatenación con stream copy, sin música si no se pide, subtítulos al final |

## Orden recomendado de acabado

1. Montaje con los finales aprobados (cortes en movimiento; fundidos y cámara lenta solo aquí, nunca en el prompt).
2. Correcciones locales por plano: luz y color con `lighting-hf` o `grade-hf`, o reencuadre.
3. Igualar el color de toda la pieza (`/color-grade` o etalonaje local).
4. Escalado: `higgsfield-enhance-video` si hay diálogo o texto que preservar; si no, Topaz.
5. Lip-sync si hace falta (antes del escalado si el escalado reinterpreta las bocas; comprobar).
6. Sonido: diálogo, efectos, música y master.
7. Gráficos y tipografía (skill de motion graphics del usuario), con las marcas de tiempo del montaje final.

Cargar el workflow oficial correspondiente con `get_workflow_instructions` antes de usarlo: cada uno trae sus textos de prompt exactos y sus propios controles de calidad.
