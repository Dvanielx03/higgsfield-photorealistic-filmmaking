# Kling · Gemini Omni Flash · Veo en Higgsfield

> Cargar cuando el router elija uno de estos modelos: un plano único desde un fotograma aprobado, un control de fotogramas clave ordenados, o escalar 1:1 con prompt.
> Fuente: esquema del conector y workflow oficial `higgsfield-enhance-video`, verificados el 24-nov-2026. Para Kling 3.0, Omni Flash y Veo **no hay reglas oficiales de prompting** en los workflows de Higgsfield; se aplican las de `prompting/principles.md` y las guías de cada fabricante citadas en `platform/sources.md`.

## Kling 4.0 (`kling4_0`)

| Parámetro | Valores |
|---|---|
| `mode` | `text-to-video`, `image-to-video`, `reference-to-video`, `video-edit` |
| `duration` | 3–30 s |
| `resolution` | `720p`, `1080p`, `4k` |
| `aspect_ratio` | `21:9`, `16:9`, `9:16`, `1:1`, `auto` |
| `dynamic_range` | `sdr`, `hdr` (HDR desde 1080p) |
| `medias` | `start_image`, `end_image`, `image_references` (máx. 10; en `image-to-video` son **fotogramas intermedios ordenados**), `video_references` (máx. 5; en `video-edit`, primero la base) |
| `kling_element_ids` | Hasta 7 elementos de Kling |
| Audio | No declara |

**Reglas de la [guía oficial de Kling 4.0](https://kling.ai/quickstart/kling-4-model-user-guide)** (04-11-2026):
- **Omni Reference y Keyframes no se combinan** en una misma generación.
- Sintaxis:
  - `Use @Image1 as the first frame`;
  - para editar: `Edit @Video1 … Keep everything else unchanged`. Escribir solo `Reference @Video1` genera desde referencia en lugar de editar;
  - keyframes con tiempos: `0–3 sec | Keyframe 1: …`.
- Estructura: papel de cada recurso → ajustes → eventos con tiempos → audio. Evitar términos abstractos («premium look»).
- Negativos mínimos: solo `no subtitles` y `no background music`.
- Hasta 7 Elements (3 de video, de 3 a 8 s) y 3 perfiles de voz.

**Conflictos:**
- **Resolución:** Higgsfield ofrece 720p y 1080p según su blog (20-10-2026), aunque el esquema del conector lista también 4K y HDR. Cotizar antes de prometer 4K.
- **Créditos:** la tabla y las preguntas frecuentes del propio blog dan cifras distintas. Cotizar siempre.

**Cuándo:**
- Plano único desde un fotograma aprobado, más barato que Seedance (720p i2v: **25 cr / 10 s**).
- Animar una secuencia de fotogramas clave ordenados (`image_references` en `image-to-video`).
- **Escalar o mejorar 1:1 con prompt** (workflow oficial `higgsfield-enhance-video`).

### Kling 4.0 como «Enhance Video» (escalado fiel)

Reglas oficiales del workflow:
- El prompt es la cabecera oficial (`Upscale this exact video 1:1 to native {RES}… not a reinterpretation and not a regrade…`) más un bloque cronometrado de unos 1.650 caracteres como máximo: `VIDEO / LOOK / SHOTS (seconds) / DIALOGUE / TEXT / SOUND`.
- **Nunca** pedir «upscale this» a secas. El diálogo va palabra por palabra en su idioma original y todo texto legible, deletreado exacto.
- Si el video no tiene subtítulos, escribir `no captions or subtitles`: Kling quema el diálogo citado como subtítulos.
- **Sin vocabulario de etalonaje** (`cinematic, vivid, rich, punchy, deep blacks, golden, moody`) ni de imagen suave (`soft, hazy, milky, dreamy, blurry`). Sin marcas de cámara o lente, títulos de películas ni personas reales.
- **Límites:**
  - la entrada debe tener al menos 720 px en el lado corto;
  - se trabaja en partes de unos 15 s;
  - la salida siempre es a 24 fps;
  - el color no se mantiene entre tomas.
- **Costo según el workflow:** 1080p ≈ 4 cr/s (60 / 15 s); 720p ≈ 41,25 / 15 s.
- **Control de calidad oficial:** SSIM (normal 0,76–0,89) y desfase de cortes. Se repite una parte si su duración se desvía más de 1 fotograma o un corte más de 2. «An SSIM under 0.75 alone is a reason to look, not to re-run.»

## Kling 3.0 (`kling3_0`)

- 3–15 s; modos `std`, `pro`, `4k`; `16:9`, `9:16`, `1:1`; `sound` on/off.
- Medios: solo `start_image` y `end_image`.
- **Acepta Elements solo si hay `start_image` explícito.**
- El conector lo propone por defecto para multiplano con audio y para transferir movimiento. Con fotorrealismo y blockout, Seedance 2.5 tiene más reglas verificadas.
- **Kling 3.0 Turbo:** 720p/1080p, solo `start_image`, sin audio. El centro de ayuda lo propone para borradores.
- El centro de ayuda de Kling recomienda **encadenar el último fotograma como inicio del plano siguiente**. Sirve para cadenas i2v de Kling; para las costuras de Seedance, ver `direction/continuity.md`.
- **Multiplano** de hasta 6 cortes en 15 s ([página de Kling 3.0](https://higgsfield.ai/kling-3.0)).

## Gemini Omni Flash 1.2 (`gemini_omni_flash_1_2`)

- `mode` obligatorio: `text-to-video`, `image-to-video`, `reference-to-video`, `edit`, `extend`.
- Duración: 3–15 s con texto o con un solo primer fotograma; 3–10 s con referencias, con inicio y fin, o en `extend`.
- Resolución `360p`, `720p`, `1080p`, `4k`; relaciones `16:9` y `9:16`.
- Medios: hasta 7 `image_references` según el conector (Google documenta 6: 3 por personaje y 2 personajes) y hasta 3 `video_references` (en `edit`, exactamente uno de 3–15 s). **Sin referencias de audio.**
- 1080p y 4K son **reescalados**, no nativos (Google). La extensión llega hasta 30 s en total, y el modelo solo usa los últimos 10 s como contexto: hay que volver a mencionar lo que apareció antes.
- Audio nativo, sin parámetro.
- **Costo:** 720p, 8 s, con referencias = **18 créditos** (≈ 2,25 cr/s). No admite ilimitado.
- **Guía del fabricante:** corta entre planos por defecto; pedir `single continuous shot` cuando se quiere un solo plano. Diálogo con la forma `<Person> says: <line>.`, sin comillas, para evitar que el texto aparezca en pantalla.
- **Cuándo:** planos sin personas reales, ambientes y pruebas baratas de movimiento.

## Veo 3.1 (`veo3_1`) y Veo 3.1 Lite

- `veo3_1`: 4, 6 u 8 s; calidad `basic`, `high` o `ultra`; `16:9` y `9:16`; solo `start_image`; variantes `preview` y `fast`.
- **Google anunció que retira Veo 3.1 Fast/Quality de Flow el 5-dic-2026.** En Higgsfield puede seguir en el catálogo: comprobar con `models_explore` antes de usarlo y no basar una producción nueva en él.
- **Cuándo:** casi nunca en este flujo. Solo si el usuario lo pide expresamente.
