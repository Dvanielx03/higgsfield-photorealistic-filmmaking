# Seedance 2.5 (`seedance_2_5`): el caballo de batalla

> Cargar cuando el router elija Seedance 2.5, que es lo habitual para planos con personas, secciones multiplano, blockout, diálogo, re-iluminación o re-etalonaje.
> Fuentes: esquema del conector (`models_explore`), workflows oficiales `drama-ads`, `angles-hf`, `lighting-hf`, `grade-hf`, y el método de Thomas Lundström. Verificado el 24-nov-2026.

## Esquema verificado

| Parámetro | Valores |
|---|---|
| `mode` | `t2v` (sin medios), `omni_reference`, `video_edit`, `video_extension` |
| `duration` | 4–30 s, **enteros** |
| `resolution` | `480p`, `720p`, `1080p`, `4k` |
| `aspect_ratio` | `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` |
| `generate_audio` | `true` por defecto |
| `bitrate_mode` | `standard`, `high` |
| `extension_mode` | `forward`, `backward` (solo en `video_extension`) |
| `draft` | `true` → borrador 480p finalizable durante 7 días |
| `draft_job_id` | finaliza un borrador a la resolución elegida; renderiza toda su duración |
| `medias` | `start_image` y `end_image` (solo `omni_reference`), `image_references` (máx. 30 entre todas las imágenes), `video_references` (máx. 10), `audio_references` (máx. 10) |

> [!IMPORTANT]
> **Pasar siempre `aspect_ratio` y `resolution`.** Un valor omitido toma el del modelo; en el workflow oficial, doce clips de una película salieron en horizontal y siete se cobraron a 720p por eso. Orden de `medias`: imágenes → videos → audio.
> **Elements no está soportado en Seedance 2.5**: las hojas de personaje y de set van como `image_references`, no como `<<<element_id>>>`.

## Cuándo elegirlo

- Secciones multiplano guiadas por un **blockout** (`video_references`).
- Personajes con identidad estable desde hojas de personaje (`image_references`).
- **Diálogo con la voz real** de una persona (`audio_references`).
- **Corregir un video ya hecho** sin regenerar la escena: `video_edit` (luz, color, ángulos).
- **Continuar una toma** sin costura: `video_extension`.
- Por MCP o CLI **siempre gasta créditos**: lo ilimitado solo funciona en la web, y Plus no incluye video ilimitado (ver `platform/plan-and-credits.md`).

## Guía oficial de prompting de Higgsfield para Seedance 2.5

Fuentes: [guía de prompting de Higgsfield](https://higgsfield.ai/blog/seedance-2-5-prompting-guide) (13-08-2026), [guía de ByteDance publicada por Higgsfield](https://higgsfield.ai/enterprise-help-center/platform/seedance-prompt-guides) y [centro de ayuda](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-seedance) (17-11-2026).

- **Secciones del prompt, en este orden:** `GLOBAL STYLE` · `SCENE` · `CHARACTERS` · `LOCATION` · `FIRST FRAME AND BLOCKING` · planos · `OPTICS` · `CAMERA` · `PHYSICS` · `LIGHTING` · `AUDIO`.
- **Multiplano:**
  - `Shot 1 (0.0s to 3.0s): …` terminado en `HARD CUT`;
  - una línea `FORMAT MODE` con el número de segmentos y en qué segundo cae cada corte.
- **Papel de cada referencia:** `@Image 1 defines <the character | the location | the style>`, `@Video 1 defines camera`, `@Audio 1 defines <the voice>`. **Una referencia por elemento, sin collages**; 1–8 imágenes por sujeto. Excluir lo que no se quiere de una referencia: `Do not use the image background`.
- **Blockout:** decir si es **grueso** (solo movimiento y composición) o **fino** (modelo completo para re-renderizar). **No repetir en el texto el movimiento que ya da el video de referencia**: crea conflicto.
- **Cronología:** etapas `[Stage 1]` con *initial state / primary event / end state*; tramos `0-5 seconds:`; momentos `At 5 seconds,`.
- **Candados contra los fallos frecuentes:**
  - **número exacto de personas** en plano;
  - **dirección en pantalla** explícita, para evitar inversiones de izquierda y derecha;
  - `NOT 3D-render` contra el aspecto de plástico;
  - **cambios en un solo sentido** (lo mojado solo se moja más; nada vuelve a crecer).
- **Localización concreta:** una localización vaga es «the most common reason» de la deriva entre cortes. Sin referencias, las caras se vuelven genéricas hacia el 3.º o 4.º corte.
- **Diálogo:** entre comillas, con su marca de tiempo y una nota de entrega, y **contando las líneas**: `Exactly two scripted spoken lines`.
- **Iterar:** empezar en baja resolución, **cambiar una sola cosa por iteración** y revisar con especial atención **los segundos 5–8**.
- **50 referencias son un techo, no un objetivo.**

> [!NOTE]
> **Conflictos entre fuentes, resueltos así:**
> - **Etiqueta:** la guía y el blog escriben `@Image 1` (con espacio); el workflow `drama-ads` escribe `@Image1`. Usar la forma que muestre la interfaz o el workflow con el que se trabaja, y la misma en todo el prompt.
> - **Diálogo:** la guía de ByteDance usa llaves `{…}` (y `(…)` para música, `<…>` para efectos y `【…】` para rótulos); Higgsfield usa comillas. **Usar comillas**, que es lo que usan los workflows oficiales del conector.
> - **Elements en Seedance:** la web de Higgsfield tiene un botón «@ Elements» en Seedance, pero por MCP Seedance 2.5 **no está en la lista de modelos con Elements**. Por el conector, pasar las hojas como `image_references`.

## Estructura del prompt en `omni_reference` (combinada)

Orden validado por el workflow oficial `drama-ads`, combinado con las secciones de la guía oficial y el bloque de blockout de Thomas:

1. **Línea de estilo** y «video words» (cómo se rueda: lentes, cámara, actuación).
2. **Bloque de blockout** si hay `video_references` (ver `prompting/templates.md` A).
3. **Etiquetas de referencias**, en el orden en que se envían: `@Image1 is <the place>…; @Image2 is <name>, <look>`. Añadir o quitar una imagen **renumera todas las siguientes**.
4. **Beats**, cada uno en su párrafo y empezando por sus segundos, con las etiquetas que actúan en él: `0-3 s (@Image3 @vid1): <framing>, <action>` (mapa temporal en `direction/reference-timeline.md`).
5. **Diálogo**: quién habla, las palabras entre comillas y cómo lo dice.
6. **Efectos de sonido**, nombrados sobre quien los produce.
7. **Frase de mantenimiento** al final: los personajes, props, cielo y luz que no cambian.

Frases obligatorias:
- `No music and no score.` (la música se pone en post).
- Con diálogo, fijar el idioma: `Every spoken line is in <language>, exactly the words in quotes; nobody speaks any other language.` Sin ella, un clip oficial salió entero en mandarín.

## Reglas de dirección (medidas en el workflow oficial)

- **Los cortes no caen exactos.** La mitad de los cortes cae a menos de 0,33 s del segundo escrito y uno de cada tres se desvía 0,5–2,8 s. Por eso:
  - plano mínimo de 1,5 s (2 s si hay acción física);
  - dejar 0,8 s de margen;
  - inserts de al menos 2,8 s;
  - la última línea de diálogo termina como mínimo 4 s antes del final del clip; los planos posteriores dicen `in silence, <action>`.
- **Clips de 10–15 s con unos 4 beats y 6 planos.** Un clip de 30 s con 12–16 planos comprimió los momentos clave a menos de un segundo.
- **Admite 2–14 planos por clip**, de 0,5 s mínimo cada uno (`angles-hf`). Como mucho 2 primeros planos de cara por clip.
- **Escribir el estado, no lo que se quiere evitar:** el modelo dibuja lo que nombran las palabras.
- **Una mirada se escribe como la cara que mira**, no como su objetivo; si no, se convierte en un tilt de cámara.
- **Una sola acción física por plano.** Máximo 2 contactos entre cuerpos y 1 cambio de estado (romperse, mojarse) cada 30 s.
- **Objetos y marcas:** `a plain unbranded <thing>`.
- **No escribir** `continuing from the previous shot`, ni fundidos, cámara lenta o títulos (van en montaje).
- Para un solo ángulo, **no usar plurales** («cameras», «shots»): Seedance corta a otros ángulos si se los prometen.
- En la frase de mirada de `video_edit`, **nunca usar la palabra «camera»**: una vez metió un trípode en el plano.

## Voz y lip-sync con `audio_references`

- `@Audio1 is the voice of @Image2, <look>: every line he speaks is in this voice.`
- Muestra de **3–10 s**: una línea tranquila de la persona real. Nunca se corta de un clip que ya usó la muestra («a copy of a copy drifts»).
- Repetir el registro de la voz en la frase de enlace. Evitar `yells`, `screams`, `shrieks`, `loud`.

## Modos de corrección (sin rehacer la escena)

| Modo | Para qué | Notas oficiales |
|---|---|---|
| `video_edit` + preset de luz (`lighting-hf`) | Re-iluminar con uno de 62 looks | Clip de 4–30 s, `generate_audio: false` y después devolver el audio original. Salida a 24 fps; puede durar unas décimas menos |
| `video_edit` + preset de etalonaje (`grade-hf`) | Re-etalonar con uno de 34 looks | Solo color; igualar toda una película es el comando `/color-grade` |
| `video_edit` + lista de planos (`angles-hf`) | Re-rodar una toma de una cámara como multicámara | Detrás del sujeto hay que nombrar lo que la toma original nunca mostró, o copia el encuadre; Seedance gira el ángulo más de lo escrito |
| `video_extension` | Alargar una toma hacia delante o hacia atrás | La salida repite el último fotograma del origen: recortarlo al montar |

## Borrador → final

1. Generar con `draft: true` (480p): mismo prompt, mismas referencias y misma duración que el final.
2. Revisar con `quality/qc-rubric.md`.
3. Si se aprueba: finalizar con `draft_job_id` a 720p o 1080p (cotizar con ese id antes de finalizar). Si falla: corregir en el origen y hacer otro borrador.

## Costos cotizados (9:16, 10 s, 24-nov-2026)

| Variante | Créditos |
|---|---|
| Borrador 480p | 30 (≈ 3 cr/s) |
| 720p | 70 (≈ 7 cr/s) |
| 1080p | 160 (≈ 16 cr/s) |
| 4K (según el blog oficial; no disponible en EE. UU. según el changelog) | 280 |
| Seedance 2.5 Flash 480p (no finalizable como 2.5) | 20 |

Re-cotizar siempre: los precios cambian.

## Fallos típicos

| Fallo | Arreglo |
|---|---|
| Sale en horizontal o a otra resolución | Faltaba `aspect_ratio` o `resolution` explícito |
| Idioma equivocado en el diálogo | Frase de idioma obligatoria |
| Música de piano genérica | `No music and no score.` y silenciar el audio en post |
| Cortes desplazados | Márgenes de 0,8 s y plano mínimo de 1,5 s; blockout con la duración exacta |
| La costura entre dos clips titila | No fijar `start_image` en la costura: enviar el fotograma como `image_references` (frame plate) |
| Copia la cápsula del blockout | Bloque «The capsules carry no body motion…» completo |
