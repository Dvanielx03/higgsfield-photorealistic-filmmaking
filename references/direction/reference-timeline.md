# Mapa temporal de referencias y audio por tramo

> **Fundamental.** Cargar al recibir referencias de inspiración, al escribir el plan de planos y antes de cada ficha de generación. Cada referencia se ata a **los segundos en que actúa**, y cada tramo dice **qué audio quiere**: música, efectos, ambiente, diálogo o silencio.

Hay dos clases de referencia y las dos llevan marcas de tiempo:

| Clase | Qué es | Dónde se registra |
|---|---|---|
| **Referencias de inspiración** | Videos o imágenes que el usuario trae como ejemplo (un anuncio, un reel) | `templates/referencias.md` → desglose con timecode |
| **Referencias de producción** | Lo que se envía al modelo: `@Image…` (hojas, sets, plates), `@Video…` (blockout, movimiento), `@Audio…` (voz) | Mapa temporal de cada clip, en la `prompt-card` |

---

## 1. Desglose de una referencia de inspiración

```bash
python -I scripts/timeline.py breakdown referencia.mp4 referencias/<nombre>/
```

Detecta los cortes, guarda un fotograma por plano y crea `desglose.md` con la tabla de timecodes. Después se completa a ojo, plano por plano:

| Plano | Entra | Sale | Dur. | Tamaño / ángulo | Movimiento | Qué pasa | Texto / gráfico | **Audio** | Técnica en Higgsfield | ¿Lo tomamos? |
|---|---|---|---|---|---|---|---|---|---|---|
| P03 | 00:04.75 | 00:07.51 | 2.76 s | PP, normal | push-in lento | mira a cámara y sonríe | palabra 3D detrás de la cabeza | **música** (beat entra) + **efecto** (whoosh) | Seedance 2.5 + texto en post | sí: el golpe de música en el corte |

Reglas:
- La detección automática falla con fundidos y movimientos rápidos: **revisar siempre a ojo**. Para afinar, usar `frames.sh sheet` a 4 fps o `frames.sh at <segundo>`.
- **Cada recurso que se quiere copiar se anota con su segundo exacto** («00:02.5–00:04.5: la mano tapa el lente como transición»). Una referencia sin marcas de tiempo no se puede reproducir ni revisar.
- La columna **Audio** dice qué suena en ese tramo y de dónde viene: música, efecto, ambiente, voz o silencio.

## 2. Mapa temporal de un clip (referencias de producción)

Por cada clip, antes de cotizar, una tabla en la `prompt-card`:

| Tramo del clip | Plano | Referencias activas | Qué define cada una aquí | Fuente y tramo de origen | **Audio del tramo** | Origen del audio |
|---|---|---|---|---|---|---|
| 0–3 s | P1 | `@Image1` plate · `@Image3` Andrés · `@vid1` | set y altura de cámara · identidad · cámara y timing | `blockout/S2.mp4` 0–3 s | **ambiente** (zumbido de fluorescente) | modelo |
| 3–6 s | P2 | `@Image3` · `@vid1` | identidad · cámara | `blockout/S2.mp4` 3–6 s | **efecto** (golpe de puerta a 3,2 s) | modelo |
| 6–10 s | P3 | `@Image3` · `@Audio1` | identidad · voz | `voz/andres.wav` 0–4,1 s | **diálogo** «¿Y cómo funciona?» a 6,5 s | referencia de voz |
| 10–14 s | P4 | `@Image3` · `@vid1` | identidad · cámara | `blockout/S2.mp4` 10–14 s | **silencio** | — |
| toda la pieza | — | — | — | — | **música** | post |

### Reglas del mapa

1. **Recortar cada video y audio de referencia al tramo exacto antes de subirlo**:
   ```bash
   python -I scripts/timeline.py trim fuente.mp4 12.0 16.0 ref_movimiento.mp4
   ```
   **No está documentado** que el modelo use solo un tramo de un video de referencia si se le pide con palabras. Lo verificable es recortar.
2. **Blockout = duración exacta de la sección.** Sus segundos son los segundos del clip.
3. **Voz (`@Audio`)**: una muestra original de 3–10 s de la persona (regla de `drama-ads`). Su tramo de origen se anota.
4. **En el prompt, cada beat empieza con sus segundos y nombra las etiquetas que actúan en él:** `3-6 s: @Image3 pushes the door open…`. Las referencias que valen para todo el clip (set, identidad) se declaran una vez arriba y se repiten en los beats donde importan.
5. **Momentos puntuales** con `At <n> seconds,` (guía oficial de Seedance): un golpe, la entrada de una línea, un corte.
6. **Acotar qué aporta cada referencia y en qué tramo**, a la manera de los prompts publicados por Thomas Lundström:
   - `@Kitchen — the kitchen for 0:25.67–0:30.00 only.`
   - `@tstr — appearance of the car ONLY. … Do NOT reproduce its grey background.`
   - `@Video 1 · 30s — camera movement, cuts, speed ramps and timing ONLY, 1:1 frame-aligned.`
   El esqueleto lo genera `scripts/prompt_skeleton.py`.
7. **Tolerancia:** los cortes de Seedance se desvían (la mitad ±0,33 s y uno de cada tres 0,5–2,8 s). Planificar con **margen de 0,8 s**, planos de al menos 1,5 s, y la última línea de diálogo terminada **4 s antes del final** del clip.
8. **Renumeración:** si se añade o quita una imagen, cambian `@Image2…N`. Actualizar el mapa y el prompt a la vez.

## 3. Especificación de audio por tramo

Cada tramo del plan y del mapa declara **uno o varios** de estos tipos. Si el usuario no lo dijo, **preguntar**. Si no hay respuesta, aplicar el valor por defecto: efectos y ambiente del modelo, y música en post.

| El tramo quiere | Parámetros | Cómo se escribe en el prompt | Dónde se hace y por qué |
|---|---|---|---|
| **Silencio** | Si todo el clip es silencio: `generate_audio: false` | Beat con `in silence, <action>` | Modelo. Útil para planos que llevarán música o voz en off |
| **Efectos** (sonidos con dueño: golpe, paso, puerta) | `generate_audio: true` | `Sound: <the sound>, <material and size>, <distance>` en el beat, nombrado sobre quien lo produce; `At <n> seconds,` si es puntual | Modelo o post (`video-sound-design`, con biblioteca Epidemic Sound y niveles definidos) |
| **Ambiente** (fondo continuo) | `generate_audio: true` | `Ambience: <room tone, traffic, wind>` en la línea de audio | Modelo; en post se rellena por debajo de los cortes |
| **Diálogo** | `generate_audio: true` + `audio_references` con la voz | Línea entre comillas, con su segundo, quién habla y cómo; frase de idioma; `Exactly <n> spoken lines` | Modelo, con la voz real como referencia |
| **Música** (recomendado) | En el clip, `No music and no score.` | — | **Post:** `elevenlabs_music_v2` con `force_instrumental`, duración = pieza + 5 s, unos 10 LU por debajo del diálogo y sin nombres de artistas (según `drama-ads`). Así controlas tempo, cortes y mezcla |
| **Música generada por el modelo** (solo si el usuario la pide expresamente) | `generate_audio: true` | Una frase propia con su tramo: `From 0 to 8 seconds, (music: slow warm piano, sparse)`. La notación `(…)` viene de la guía de ByteDance publicada por Higgsfield | Modelo. **Riesgo documentado:** Seedance tiende a meter piano genérico. Probar siempre en borrador; la música no se puede separar después sin herramientas externas |
| **Música de referencia** (ritmo, tono) | `audio_references` | `@Audio2 defines <the rhythm and mood of the music>` | **No documentado** para música en concreto (la guía solo muestra `@Audio 1 defines…` en general). Tratarlo como experimento en borrador |

Reglas:
- **Por defecto, todo clip lleva `No music and no score.`** La música solo entra en la generación si un tramo la pide explícitamente.
- **Música y diálogo en el mismo tramo del modelo:** evitarlo. La música tapa la voz y no se puede remezclar. Mejor diálogo en el modelo y música en post.
- **El tipo de audio de cada tramo se revisa en el control de calidad:** música no pedida, silencio que suena o diálogo fuera de su segundo cuentan como fallo (`quality/qc-rubric.md`).

## 4. Verificación temporal (control de calidad)

1. **Cortes:**
   ```bash
   python -I scripts/timeline.py drift clip.mp4 3,6,10
   ```
   Marca FUERA lo que se desvía más de 0,8 s y avisa si sobran o faltan cortes.
2. **Eventos puntuales:** `bash scripts/frames.sh at clip.mp4 <segundo> evento.png` para cada momento del mapa (el golpe, la entrada de la línea).
3. **Audio por tramo:** escuchar cada tramo contra la columna **Audio del tramo**. Si el desvío de los cortes es aceptable pero el audio no cumple, se corrige en post (silenciar, sustituir efectos o meter la música); no hace falta regenerar.
4. Anotar el peor desvío en `qc-report.md`.
