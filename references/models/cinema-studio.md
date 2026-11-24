# Cinema Studio (video 4.0 · 3.5 · 3.0 · imagen 2.5)

> Cargar cuando el plano necesite un **control óptico o de iluminación explícito** que Seedance no da por parámetro, o un fotograma de cine de alta resolución.
> Fuente: esquema del conector (`models_explore`), verificado el 24-nov-2026. **No hay workflow oficial con reglas de prompting para Cinema Studio**: aplicar las reglas generales de `prompting/principles.md` y las de Seedance 2.5 para la estructura multiplano.

## Cinema Studio Video 4.0 (`cinematic_studio_video_4_0`)

| Parámetro | Valores verificados |
|---|---|
| `mode` | `t2v`, `omni_reference`, `video_edit`, `video_extension` |
| `duration` | 4–30 s enteros |
| `resolution` | `480p`, `720p`, `1080p` (sin 4K) |
| `aspect_ratio` | `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` |
| `generate_audio` | `true` por defecto |
| `medias` | Igual que Seedance 2.5: `start_image` y `end_image` (solo omni), `image_references` (30 en total), `video_references` (10), `audio_references` (10) |
| Controles creativos | `era_id`, `camera_model_id`, `camera_lens_id`, `camera_aperture_id`, `pacing_id`, `genre_id`, `light` (`preset` · `custom` · `user`) + `light_id`, `color_palette` (`preset` o `user` + id) |
| `light_custom` | Rig de luces ordenado; **la primera es la key**. Cada luz: `{direction, color, brightness, diffuse}`, con `direction` en `top`, `bottom`, `left`, `right`, `front`, `back` y sus combinaciones. Requiere `light: "custom"` |

**Opciones de cada control según la [guía oficial de 4.0](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide)** (27-10-2026). Son los nombres en la interfaz, no los ids:

| Control | Opciones |
|---|---|
| Género | General, Action, Epic, Drama, Comedy, Horror, Noir |
| Época | 1960s, 1980s, 1990s, 2000s, 2020s |
| Tempo | Auto, Chaotic, Dynamic, Calm, Single shot |
| Cámara | Modern, 35mm Film, 8mm Film, DV Camcorder |
| Lente | Clean Sharp, Anamorphic, Vintage Anamorphic, Warm Vintage, Halation Vintage |
| Apertura | f/1.4, f/4, f/11 |
| Otros | Más de 30 movimientos, emoción por personaje (`@character_name`), más de 50 paletas, 6 esquemas de luz o luz manual |

Consejos oficiales:
- Las referencias deciden la apariencia; el prompt, lo que pasa.
- No contradecir los controles con el texto (por ejemplo, pedir cortes rápidos con Tempo en *Single shot*).

Sin ids, estas opciones se pueden **pedir en el prompt** con sus nombres: `shot on 35mm film`, `anamorphic lens`, `f/1.4`, `calm pacing, single shot`.

> [!WARNING]
> **Los ids de los controles creativos no se pueden descubrir desde el conector.** `models_explore` no los lista y no hay workflow ni preset que los documente. **No inventar ids.** Si el usuario no da uno que haya visto en la interfaz web de Cinema Studio, se omite el campo y la cámara, la lente y la era se piden en el prompt.
> Lo que sí es usable y está documentado: **`light: "custom"` con `light_custom`**. Es la única forma verificada de fijar por parámetro un esquema de luz idéntico entre planos.
> **Elements no está soportado** en Cinema Studio 4.0.

**Costo cotizado:** 720p, 10 s, 9:16 = **70 créditos** (≈ 7 cr/s, igual que Seedance 2.5 a 720p). No admite generaciones ilimitadas.

**Conflicto de resolución:** la guía dice que en la API solo hay 480p y 720p (1080p en la app); el esquema del conector declara 1080p. Cotizar 1080p antes de prometerlo.

### Cuándo elegirlo frente a Seedance 2.5

| Situación | Elegir |
|---|---|
| Hace falta la **misma luz exacta** en varios planos de un set | Cinema Studio 4.0 con `light_custom` idéntico en todos |
| Plano o sección guiados por un blockout, con personajes y diálogo | Seedance 2.5 (más reglas documentadas, borrador finalizable, ilimitado en algunos planes) |
| Hace falta 4K nativo | Seedance 2.5 (Cinema Studio 4.0 llega a 1080p) |
| Borrador barato antes del final | Seedance 2.5 (`draft`); en Cinema Studio se prueba a 480p como generación normal |

Ejemplo de rig verificado por esquema (clave cálida desde la izquierda, relleno frío y suave):

```json
"light": "custom",
"light_custom": [
  {"direction": "left",  "color": "#FFB878", "brightness": 80, "diffuse": 40},
  {"direction": "right", "color": "#8FB4FF", "brightness": 25, "diffuse": 80},
  {"direction": "back",  "color": "#FFFFFF", "brightness": 45, "diffuse": 20}
]
```
Antes de usarlo, confirmar con `models_explore action=get` los rangos de `brightness` y `diffuse`.

## Cinema Studio Video 3.5 (`cinematic_studio_video_3_5`)

- Duración mínima de 4 s (15 por defecto). Resolución `480p`–`1080p`, las mismas 7 relaciones de aspecto.
- Medios: `start_image`, `end_image`, `image_references`, `video_references` y `audio_references`, con un **máximo de 15 medios** en total.
- `generate_audio` **desactivado** por defecto.
- Parámetros propios:
  - `genre`;
  - `multi_shots`, `multi_shot_mode` y `multi_prompt` (hasta 6 objetos `{prompt, duration}`): **multiplano con un prompt por plano**;
  - `camera_style` (9 opciones), `light_scheme` (6), `color_grading` (8);
  - `style_prompt` (≤ 2000) y `enhance_prompt`.
- **`prompt_language` viene en chino (`zh`) por defecto: pasar siempre `"en"`.**
- Útil cuando se quiere **un prompt por plano** dentro de una sola generación con duraciones explícitas.
- **Costo cotizado:** 720p, 10 s, 9:16 = **50 créditos** (≈ 5 cr/s), más barato que 4.0 y que Seedance 2.5 a 720p.

## Cinema Studio Video 3.0 (`cinematic_studio_3_0`)

- 4–15 s, `480p`–`4k`, `genre` (`auto`, `action`, `horror`, `comedy`, `noir`, `drama`, `epic`).
- Medios: `start_image` y `end_image`.
- **Sí acepta Elements** (`<<<element_id>>>` en el prompt).

## Cinema Studio Image 2.5 (`cinematic_studio_2_5`)

- Fotogramas de cine `1k`/`2k`/`4k`, 10 relaciones de aspecto, `image` de entrada.
- Acepta Elements.
- **Costo:** 2 créditos a 1k (9:16).
- **Uso:** fotogramas clave y planos héroe fijos en alta resolución.
