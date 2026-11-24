# Modelos de imagen: referencias y fotogramas clave

> Cargar al crear hojas de personaje, sets, props, fotogramas clave o variantes. En este flujo la imagen es barata y el video caro: **todo lo que se pueda decidir en imagen se decide en imagen.**
> Fuentes: esquema del conector, workflows oficiales `character-sheet` y `drama-ads`, cotizaciones del 24-nov-2026.

## Catálogo útil (verificado)

| Modelo (id) | Referencias máx. | Resolución · formato | Elements | Ilimitado* | Costo cotizado (9:16) | Uso en este flujo |
|---|---|---|---|---|---|---|
| GPT Image 2.6 `gpt_image_2_6` | 16 | 1k/2k/4k · 15 relaciones · png/jpeg/webp/gif/svg | sí (no en SVG) | sí | **0,75 cr** (1k) · 1,25 cr (2k 16:9) | **Hojas de personaje Realism** (según `character-sheet`), ediciones y variantes |
| Seedream 5.5 `seedream_5_5` | 10 | 1k/1.5k/2k · fondo transparente | no listado | no | **3,5 cr** (2k) | Hojas y sets de live action (`drama-ads`), ángulos de un set (`/3d-jutsu`) |
| Seedream 5.0 Pro `seedream_v5_pro` | 10 | 1k/1.5k/2k · `is_inpaint`, `remove_bg` | no listado | sí | **2,5 cr** | Caras y ediciones de escenas con caras; alternativa cuando lo indica la cotización |
| Nano Banana Pro `nano_banana_pro` | 14 | 1k/2k/4k · 10 relaciones | sí | sí | 1,5 cr (alias `nano_banana_2`) | Fotorrealismo general, render 4K |
| Soul 2.0 `soul_2` | — | 3:4 para caras | — | sí | **≈ 1 cr** (2k) | **Caras de casting** de estilo Realism sin adjunto (`character-sheet`) |
| Soul Cinema `soul_cinematic` | 1 `image` | 1.5k/2k · 8 relaciones · `soul_id` | — | no | ≈ 1 cr | Fotogramas con Soul ID entrenado |
| Cinema Studio Image 2.5 `cinematic_studio_2_5` | `image` | 1k/2k/4k · 10 relaciones | sí | no | 2 cr (1k) | Fotogramas héroe de cine |

\*«Ilimitado» = `supports_unlim` en el catálogo. Solo aplica si la cuenta tiene asignación de generaciones ilimitadas (ver `platform/plan-and-credits.md`).

## Reglas oficiales de prompting de imagen (`character-sheet` y `drama-ads`)

- **Redacción positiva:** «The image model draws every noun it reads and ignores "no", "not" and "without"». Para quitar algo, describir lo que hay en su lugar.
- **Edad en número:** `a 27-year-old man`. Evitar `adult, young adult, mature, middle-aged, young woman, young man` (envejecen a la persona).
- **Con una foto o cara adjunta, no describir los rasgos faciales con palabras.** Lo hace la imagen.
- **Una sola luz en las hojas:** `soft, even, diffused studio light from the front`.
- **Colores apagados y materiales concretos:** `matte silk crepe`, no `silk`.
- **Objetos sin marca:** `a plain unbranded <thing>`.
- **Sets:**
  - terminar con `No people, figures, silhouettes or animals anywhere…`;
  - una lámpara es un objeto (nunca «glowing»);
  - no escribir el sol o la luna como cosa;
  - no usar verde u oxblood por defecto.

## Hoja de personaje: método oficial (workflow `character-sheet`)

1. **Estilo:** Realism si no se dice otro.
2. **Lectura de casting** en líneas `Key: value`: edad, origen, piel, ojos, pelo, complexión.
3. **Cara** → **parada para aprobación del usuario**.
4. **Flat-lay del vestuario.**
5. **Hoja de 3 paneles:** frente y espalda del cuello hacia abajo, y retrato a la derecha, con cara y vestuario adjuntos → **parada para aprobación**.
6. **Looks:** ropa nueva = flat-lay nuevo; cara cambiada = primero una edición de cara.
7. **Control de calidad de la hoja:** «exactly one face, in the right panel». Si falla, un único reintento; si vuelve a fallar, se muestra y se dice.
8. La hoja aprobada **se reutiliza** hasta que cambien la identidad o el vestuario.

**Con fotos reales** (los protagonistas): la cara sale de las fotos (con consentimiento) y no de `soul_2`. Las fotos van adjuntas y la cara no se describe con palabras.

Para cargar el método completo con sus textos oficiales: `get_workflow_instructions` con `{ workflow: "character-sheet" }`.

## Hoja de set y de prop

- **Set** (`drama-ads` → `location.md`): «A two-panel location reference sheet of one and the same…», con el bloque maestro de estilo palabra por palabra, entre 4.800 y 5.500 caracteres, y al final «No people…».
- **Desde una placa gris de blockout:** plantilla D de `prompting/templates.md` (método de Thomas Lundström), pidiendo que el lugar **se sienta habitado**.
- **Nuevos ángulos de un mismo set:** `/3d-jutsu`. El master aporta identidad, materiales y luz; el render del ángulo aporta cámara y layout. Evitar encadenar masters generados.
- **Prop:** «A prop reference sheet of <the prop>, as a prop of a photographed live-action film… Two views side by side on a plain light-grey background…».

## Fotograma clave (keyframe)

- Antes de un i2v o como referencia de composición.
- Modelos: `cinematic_studio_2_5` o `nano_banana_pro` para el héroe, `gpt_image_2_6` para variantes y ediciones.
- **Variantes del mismo encuadre** (otro día, otra luz, otro estado): editar la misma imagen con «Use @img1 as the exact base and recreate the same photograph… Change only this: …». Nunca generar una imagen nueva desde cero.
