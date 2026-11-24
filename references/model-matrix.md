# Matriz de modelos

> **Foto del catálogo del 24-nov-2026.** Fuente: `models_explore` (Higgsfield MCP) y cotizaciones con `estimate_video_cost` / `estimate_image_cost` en 9:16. **Re-consultar y re-cotizar antes de cada producción.** Las cotizaciones no gastan créditos.

## Video: candidatos para cine fotorrealista

| Modelo (id) | Duración | Resolución | Medios | Audio | Para qué | Costo cotizado (9:16, 10 s) |
|---|---|---|---|---|---|---|
| **Seedance 2.5** `seedance_2_5` | 4–30 s enteros | 480p, 720p, 1080p, 4K | `start_image`, `end_image`, `image_references` (máx. 30 en total), `video_references` (máx. 10), `audio_references` (máx. 10), solo en `omni_reference` | sí | **Por defecto.** Secciones multiplano siguiendo blockout, identidad con referencias, edición y extensión. Tiene `draft` (480p finalizable en 7 días) | borrador 480p: **30 cr** · 720p: **70 cr** · 1080p: **160 cr** |
| Seedance 2.5 Flash `seedance_2_5_flash` | 4–30 s | 480p, 720p | igual; 10 imgs, 5 videos, 5 audios | sí | Pruebas de concepto muy baratas. **No** sirve de borrador finalizable del 2.5 | 480p: **20 cr** |
| Cinema Studio 4.0 `cinematic_studio_video_4_0` | 4–30 s | 480p–1080p | igual que Seedance 2.5 | sí | Control explícito de cámara, lente, apertura, luz, era, género y paleta mediante ids | 720p: **70 cr** |
| Kling 4.0 `kling4_0` | 3–30 s | 720p, 1080p, 4K (HDR desde 1080p) | `start_image`, `end_image`, `image_references` (fotogramas ordenados en i2v), `video_references` | no declarado | i2v desde un fotograma aprobado, más barato | 720p i2v: **25 cr** |
| Gemini Omni Flash 1.2 `gemini_omni_flash_1_2` | 3–15 s (3–10 con referencias o con inicio y fin) | 360p–4K | `start_image`, `end_image`, hasta 7 `image_references`, hasta 3 `video_references` | nativo según Google | **Casar con Google Flow**: es el modelo actual de Flow | 720p, 8 s, referencias: **18 cr** |
| Cinema Studio 3.0 `cinematic_studio_3_0` | 4–15 s | 480p–4K | `start_image`, `end_image` | opcional | Alternativa con `genre` | no cotizado |

Utilidades (cotizar cada vez):
- `sync_so`: lip-sync de un video a un audio.
- `topaz_video`: escalado a 1080p o 2160p e interpolación.
- `sam_3_video`: recorte de fondo en video.
- `fps_boost`.

**Tarifa por segundo derivada de las cotizaciones** (para presupuestos rápidos; confirmar siempre):

| Modelo | Créditos por segundo |
|---|---|
| Seedance 2.5, borrador 480p | ≈ 3 |
| Seedance 2.5, 720p | ≈ 7 |
| Seedance 2.5, 1080p | ≈ 16 |
| Kling 4.0, 720p | ≈ 2,5 |
| Omni Flash 1.2, 720p | ≈ 2,25 |

**Pendiente de verificar con un trabajo real:** cuánto cuesta finalizar un borrador de Seedance 2.5 (`draft_job_id`). Se cotiza con el id del borrador antes de finalizar.

## Imagen: referencias y fotogramas clave

| Modelo (id) | Uso | Costo cotizado (9:16, 1 imagen) |
|---|---|---|
| GPT Image 2.6 `gpt_image_2_6` | Por defecto de Higgsfield. Hasta 16 referencias. Ediciones | **0,75 cr** |
| Seedream 5.0 Pro `seedream_v5_pro` | Caras, hojas de personaje, ediciones de escenas con caras. Hasta 10 refs | **2,5 cr** |
| Nano Banana Pro (id `nano_banana_2`, que es un alias de Pro) | Fotorrealismo general, mismo modelo que Google Flow | **1,5 cr** |
| Cinema Studio Image 2.5 `cinematic_studio_2_5` | Fotogramas de cine hasta 4K | **2 cr** (1k) |
| Soul Cinema `soul_cinematic` | Fotogramas con Soul ID | **≈1 cr** (2k) |

En Google Flow, las imágenes con Nano Banana no consumen créditos (con límite diario según el plan). Ver `flow-handoff.md`.

## Qué modelo para qué plano

| Tipo de plano | Primera opción | Alternativa | Por qué |
|---|---|---|---|
| Sección multiplano con personajes y movimiento de cámara | Seedance 2.5 + blockout | Cinema Studio 4.0 | Sigue el video de referencia de cámara y timing, y admite muchas referencias de identidad |
| Plano único desde un fotograma aprobado | Seedance 2.5 `start_image` | Kling 4.0 i2v (más barato) | El fotograma fija composición, cara y luz; el prompt solo describe movimiento |
| Transición a un fotograma exacto | Seedance 2.5 `start_image` + `end_image` | Omni Flash 1.2 | Asegura el empalme |
| Set vacío o inserto sin caras | Flow (Omni Flash 1.2) o Seedance 2.5 Flash | Kling 4.0 | Barato; sin riesgo de identidad |
| Ficha o retrato casi fijo | Imagen + parallax en post | i2v corto con Kling 4.0 | Una imagen cuesta ~1–2,5 cr frente a 25–70 cr de video |
| Plano con diálogo a cámara | Seedance 2.5 con `audio_references` (su voz real) | Generar sin voz + `sync_so` | Probar en borrador; el lip-sync es el punto más frágil |
| Efecto gráfico (contorno, B/N, clones de texto) | Post | — | No se gasta en lo que hace un filtro |

## Límites conocidos que afectan al fotorrealismo

- **Texto en imagen:** pedir siempre «no legible text»; el texto va en post.
- **Identidad:** el riesgo crece con la duración y con el número de personajes por plano. Mitigación: hoja de personaje como referencia y bloque `IDENTITY, CRITICAL`.
- **Cuerpos rígidos del blockout:** el modelo puede copiar la cápsula como pose. Mitigación: decir que la cápsula es solo marcador de posición, tamaño, dirección y velocidad, y describir el cuerpo en el prompt.
- **Música genérica en el audio de Seedance:** pedir `NO MUSIC, CRITICAL` y hacer la música en post.
- **Seguridad:** sin figuras públicas, marcas registradas ni contenido sexual (`nsfw`, `ip_detected`).
