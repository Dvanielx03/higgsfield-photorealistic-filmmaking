# Flujo automatizado Blender → Kling 4.0 / Seedance 2.5 (más videos con 1.000 créditos)

> Cargar al planificar una producción con presupuesto ajustado, al decidir entre Kling y Seedance para un plano, o al construir el blockout. Base: prueba publicada de Thomas Lundström ([video](https://www.youtube.com/watch?v=ECxZEbUdSlE), [recursos](https://higgsfield.ai/@thomas_lundstrom/blogs/kling-4-0-vs-seedance-2-5-3-tests-every-prompt), 23-oct-2026) y cotizaciones del conector del 24-nov-2026.

## 1. Lo que dice la evidencia (y por eso el flujo es híbrido)

Thomas probó **los mismos recursos y el mismo prompt** en los dos modelos:

| Prueba | Resultado |
|---|---|
| Blockout de Blender como video de referencia | **Seedance 2.5 claramente mejor.** Kling 4.0 «just doesn't seem to read the Blender sequence the way Seedance 2.5 does» |
| 7 keyframes en una toma larga de 30 s | Kling 4.0 **mejora mucho**, pero Seedance sigue siendo más fotorrealista, con mejor adherencia; Kling tiene «more of that mushy AI detail» y más errores |
| Animación 2D y texto | Resultados **cercanos**; Kling «half decent» por su precio (estropeó el texto final) |
| Veredicto | «For photorealism, camera control and prompt adherence, Seedance 2.5 is still in a league of its own. Kling 4.0 costs a fraction of the credits and is worth testing for animation and simpler shots.» |

**Consecuencia de diseño:**
- **Kling 4.0 nunca se usa con un blockout como video de referencia.** Se usa con **keyframes** (fotogramas clave) que salen del mismo blockout, convertidos a fotorrealistas.
- **Seedance 2.5 se reserva para los planos donde el fotorrealismo o la cámara compleja son críticos.**

## 2. Costos verificados (9:16, 24-nov-2026)

| Modelo y modo | Cotización | cr/s |
|---|---|---|
| Kling 4.0 `image-to-video` 720p | 75 por 30 s | **2,5** |
| Kling 4.0 `image-to-video` 1080p | 112,5 por 30 s | **3,75** |
| Kling 4.0 `reference-to-video` 720p | 25 por 10 s | 2,5 |
| Kling 4.0 Flash 720p (sin keyframes) | 15 por 10 s | 1,5 |
| Seedance 2.5 borrador 480p | 30 por 10 s | 3 |
| Seedance 2.5 720p | 70 por 10 s | 7 |
| Seedance 2.5 1080p | 480 por 30 s | **16** |

Thomas pagó 30 créditos por 30 s de Kling 4.0 a 1080p en octubre; **hoy cuesta 112,5**. Aun así, Kling 4.0 a 1080p es **unas 4 veces más barato** que Seedance a 1080p, y Kling a 720p cuesta menos que un borrador de Seedance a 480p. Re-cotizar siempre.

## 3. Las dos rutas

| | **Ruta K · Kling 4.0 por keyframes** | **Ruta S · Seedance 2.5 por blockout** |
|---|---|---|
| Para | Planos sencillos, producto, insertos, ambientes, B-roll, animación y gráficos, tomas largas definidas por keyframes | Planos héroe, caras en primer plano, diálogo, cámara compleja, cortes precisos, fotorrealismo crítico |
| Entrada | **Keyframes fotorrealistas** (inicio, intermedios en orden, fin), hechos desde los keyframes del blockout | **Video del blockout** (`video_references`) + hojas de personaje y set |
| Identidad | Va dentro de los keyframes: Kling no combina Keyframes con Omni Reference | Hojas como `image_references` |
| Prueba barata | 720p directamente (2,5 cr/s, sin modo borrador) | Borrador 480p (3 cr/s) |
| Final | 720p, o 1080p (3,75 cr/s) | 720p (7 cr/s) o 1080p (16 cr/s) |
| Prompt | `X–Y sec \| Keyframe N:` (sintaxis oficial de Kling) | Video lock + `CUT n (t1–t2)` + referencias con su tramo |

### Regla de asignación por plano

1. ¿Primer plano de cara, diálogo con lip-sync o plano héroe? → **S**.
2. ¿Cámara compleja con cortes que deben caer exactos sobre la música? → **S** (Kling no lee el blockout).
3. ¿El plano se puede describir con 2 a 10 keyframes y un movimiento continuo? → **K**.
4. ¿Animación, producto o inserto? → **K**.
5. En duda → **K primero a 720p**: es más barato que un borrador de Seedance. Si no pasa la rúbrica, se escala.

### Escalado de K a S (sin perder lo hecho)

- Si un plano K saca **0 en fotorrealismo (1), identidad (3) o física (2)**, o falla dos veces en lo mismo, **pasa a la ruta S**.
- **Los mismos keyframes aprobados** entran como `image_references` en Seedance. Thomas los usó así en su prueba 2 (`@image_1` a `@image_7`).
- El blockout de ese plano ya existe: se añade como `video_references` si hay cámara que respetar.

## 4. Flujo automatizado, paso a paso

```
música ─► beats.py ─► cortes ─► plan.json ─► build_blockout.py (Blender sin interfaz)
                                                     │
              ┌──────────── blockout.mp4 ────────────┼──── keyframes/*.png ─── plates/*.png ── timeline.json
              ▼                                      ▼                                              │
     Ruta S: Seedance 2.5                Keyframes fotorrealistas (imagen)                          │
     (video lock)                        → Ruta K: Kling 4.0 image-to-video                         │
              └───────────────────────► prompt_skeleton.py ◄────────────────────────────────────────┘
                                          → ficha → cotización → SÍ → generar → rúbrica + drift
```

### Paso 0 · Música primero (opcional, recomendado si la pieza va a ritmo)

```bash
python scripts/beats.py musica.mp3 --duration 30 --cuts 12 --json cortes.json
```

Estima el tempo y propone cortes sobre los golpes fuertes, respetando el plano mínimo de 1,5 s. Los cortes se copian a `shots` del plan. Así el blockout ya nace a ritmo y no hay que forzar el montaje después (el segundo truco de Thomas). **Revisar los cortes escuchando**: el detector propone, el oído decide.

### Paso 1 · Plan del blockout (`plan.json`)

Claude lo escribe a partir del plan de planos. El formato está en `scripts/blockout/plan.example.json`:
- `set.boxes`: volúmenes del set;
- `subjects`: personas, con `keys` de posición y `yaw`, donde 0 = mirando hacia −Y, el lado de la cámara por defecto;
- `props`;
- `shots`: inicio, fin, `lens_mm` y `camera` (posición y punto al que mira, con keyframes);
- `keyframes`: segundos donde se quieren fotogramas clave para Kling;
- `audio`: tramos con tipo (`silencio`, `ambiente`, `efectos`, `dialogo`, `musica`) y descripción.

### Paso 2 · Blockout automático (un solo comando)

```bash
python scripts/run_blockout.py plan.json blockout/ [--refs refs.json]
```

Busca Blender (variable `BLENDER`, PATH o la instalación más reciente), ejecuta `build_blockout.py` sin interfaz y deja `fichas/kling.md` y `fichas/seedance.md` con los esqueletos de prompt. No toca Higgsfield ni gasta créditos. El script de Blender también se puede llamar directo: `blender -b -P scripts/blockout/build_blockout.py -- plan.json blockout/`.

Sin abrir Blender genera:
- `blockout.blend`: editable a mano o con el MCP de Blender;
- `blockout.mp4`: previz gris a 24 fps;
- `keyframes/KF##_<t>s.png` a resolución completa;
- `plates/<plano>_plate.png`: set sin personas;
- `timeline.json`: cortes, lentes, keyframes, clave de colores en inglés y audio por tramo.

Un plan de 8 s se construye y renderiza en **~50 s**. Iterar es editar `plan.json` y repetir: **espera varias versiones** (Thomas fijó la versión 8 de su blockout).

### Paso 3 · Keyframes fotorrealistas (ruta K) y referencias

**La calidad de los keyframes es la calidad del video.** Thomas: el mismo prompt con GPT Image 2.5 frente a las cámaras de Cinema Studio dio una diferencia cinematográfica «absolutely huge».

- **Modelos:**
  - `cinematic_studio_2_5` (Cinema Studio Image) para los keyframes;
  - Soul Cinema (`soul_cinematic`) para el plano de establecimiento;
  - hojas de personaje según `models/image-models.md`.
- **Cada keyframe** se genera con:
  - el keyframe gris de Blender como guía de composición;
  - la hoja de personaje;
  - **el keyframe anterior ya aprobado**, para encadenar la continuidad como hizo Thomas.
  Prompt de la plantilla F/G de `prompting/templates.md`, describiendo el estado de ese instante.
- **Producto u objeto complejo:** una imagen por ángulo, cada una partiendo de la anterior, y luego se juntan en una hoja (truco 1 de Thomas). Da más control y calidad que pedir la hoja entera de una vez.
- **Costo:** unos 2 créditos por keyframe en Cinema Studio Image 1k. Generados en la web, los modelos ilimitados del plan cuestan 0 (ver `platform/plan-and-credits.md`).
- **Rúbrica sobre cada keyframe antes de animar.** Un keyframe malo garantiza un video malo.

### Paso 4 · Esqueleto del prompt

```bash
python scripts/prompt_skeleton.py blockout/timeline.json --model kling    --out fichas/S1_kling.md
python scripts/prompt_skeleton.py blockout/timeline.json --model seedance --refs refs.json --out fichas/S1_seedance.md
```

- **Kling:**
  - medios: `start_image` = KF01, `image_references` = intermedios en orden, `end_image` = último;
  - texto: `One single continuous <n>-second take…` + una línea por tramo `a–b sec | Keyframe N → Keyframe N+1: …` con su sonido.
- **Seedance:**
  - referencias con su tramo, a la manera de Thomas: `@sala — the room, for 0:00.00–0:08.00 only`;
  - bloque **Video lock** con la clave de colores, en el que el blockout es la «SOLE authority» para cámara y timing y se «re-dresses, never re-imagines»;
  - `CUT n (t1–t2)` por plano con su audio.
- Claude rellena los `<…>` con la biblia y el mapa temporal (`direction/reference-timeline.md`).

### Paso 5 · Cotizar, aprobar, generar

Ficha (`templates/prompt-card.md`) → `estimate_video_cost` → **sí del usuario** → generar.

| Ruta | Pasada de prueba | Final |
|---|---|---|
| K | Kling 4.0 720p | Se queda en 720p si pasa la rúbrica; 1080p solo si el plano lo pide |
| S | Seedance 2.5 `draft` 480p | `draft_job_id` a 720p |

**El primer clip de cada ruta va solo.** Con la técnica validada, los demás pueden ir en lote.

### Paso 6 · Control de calidad

- Rúbrica de 8 criterios (`quality/qc-rubric.md`).
- `python -I scripts/timeline.py drift clip.mp4 <cortes de timeline.json>`.
- `frames.sh at` en cada keyframe: el video debe pasar por los keyframes en sus segundos.

### Paso 7 · Montaje sobre la música elegida en el paso 0

Los cortes ya están a ritmo. Sonido según el mapa temporal; música en post (`models/post-tools.md`).

## 5. Cuántos videos dan 1.000 créditos

Supuestos:
- un intento de corrección por plano;
- 6 keyframes a ~2 créditos con un reintento (~24 créditos por pieza en la ruta K);
- reserva del 15 %;
- finales a 720p.

Re-cotizar antes de presupuestar.

| Pieza de 30 s | Cálculo | ≈ Créditos | Piezas por mes con 1.000 |
|---|---|---|---|
| Todo Seedance 2.5 (borrador + corrección + final 720p) | 30 × (3×2 + 7) × 1,15 | ≈ 450 | **2** |
| Híbrido 70 % K / 30 % S | (21 × 2,5×2 + 9 × 13) × 1,15 + 24 | ≈ 280 | **3** |
| Todo Kling 4.0 (dos pasadas a 720p) | 30 × 2,5×2 × 1,15 + 24 | ≈ 200 | **5** |

**Calidad:** el híbrido mantiene la calidad en los planos que se notan, porque los héroe van por Seedance. El «todo Kling» rinde en animación, producto y B-roll, pero la evidencia dice que pierde fotorrealismo y adherencia en acción real con personas. Usarlo solo si la pieza lo permite, y siempre con la rúbrica.

## 6. Límites verificados de la ruta K

- **Kling 4.0 no combina Keyframes con Omni Reference** (guía oficial de Kling). En la ruta K no hay hojas de personaje ni video de referencia: la identidad va en los keyframes.
- **Audio:** el esquema del conector no declara audio para `kling4_0`, aunque el blog de Higgsfield habla de audio estéreo. Hasta verificarlo, el sonido de la ruta K se hace en post.
- **Duración** de 3–30 s; **hasta 10 imágenes** contando inicio y fin.
- **No hay modo borrador:** la prueba barata es la propia pasada a 720p.
- **Texto en pantalla:** Kling lo estropea (prueba 3 de Thomas). El texto va en post.

## 7. Alternativas oficiales para manejar Blender

- [Plugin Higgsfield for Blender](https://higgsfield.ai/plugins/blender): genera desde Blender.
- **Higgsfield Bridge** (conector MCP `https://bridge.higgsfield.ai/mcp`): según la guía de Thomas, permite que Claude trabaje dentro de la escena abierta de Blender.

No son necesarios para este flujo: `build_blockout.py` funciona sin interfaz, con el Blender instalado y sin conectores extra. Añadirlos es decisión del usuario, porque los conectores los configura él.
