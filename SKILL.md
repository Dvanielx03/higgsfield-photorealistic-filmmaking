---
name: higgsfield-photorealistic-filmmaking
description: Dirección y preproducción de cine fotorrealista con IA en Higgsfield (y Google Flow como segunda herramienta). Convierte una idea, guion o storyboard en plan de planos, biblia de continuidad, blockout en Blender, referencias, prompts cinematográficos por modelo y presupuesto de créditos con borrador antes del final. Úsala SIEMPRE que el usuario quiera producir un video o corto cinematográfico/fotorrealista con IA de varios planos, mantener a las mismas personas, vestuario, lugares y luz entre tomas, escribir prompts de video «de cine» para Seedance, Cinema Studio, Kling, Omni Flash o Veo, repartir trabajo entre Higgsfield y Google Flow, o controlar el gasto de créditos antes de generar, aunque no diga el nombre de la skill. Complementa a higgsfield-generate (que ejecuta las generaciones) y a higgsfield-soul-id; no las reemplaza.
---

# Higgsfield · cine fotorrealista

Esta skill es el **departamento de dirección y continuidad**. La ejecución (subir medios, generar, esperar trabajos) sigue siendo de las skills oficiales y del conector de Higgsfield:

| Necesito… | Uso |
|---|---|
| Generar, cotizar, subir medios, consultar modelos | `higgsfield-generate` o las herramientas MCP de Higgsfield (`models_explore`, `estimate_video_cost`, `estimate_image_cost`, `generate_*`, `media_upload`) |
| Entrenar una identidad facial para **imágenes** | `higgsfield-soul-id` (Soul ID solo funciona con modelos de imagen Soul; no está documentado para video) |
| Tipografía, motion graphics, montaje y render final | tu skill de montaje y motion graphics (por ejemplo `motion-studio` o HyperFrames) |
| Blockout 3D | herramientas MCP de Blender |
| Lo demás de este flujo (plan, biblia, prompts, presupuesto, control de calidad) | **esta skill** |

## Reglas que no se negocian

1. **Ningún crédito sin autorización explícita del usuario en el chat**, por generación o por lote cotizado. Cotizar (`estimate_*_cost`) es gratis y va siempre primero.
2. **No inventar** capacidades, precios ni duraciones. El catálogo cambia cada semana: antes de cada producción, re-consultar `models_explore action=get` del modelo elegido y re-cotizar. Las cifras de `references/model-matrix.md` son una foto con fecha.
3. **Personas reales solo con consentimiento** de cada una, dicho por el usuario en el chat. Nada de figuras públicas.
4. **Fotorrealismo y continuidad por encima de resolución y efectos.** Un 720p coherente gana a un 4K que cambia de cara.
5. **Decidir antes de generar.** Toda decisión creativa (encuadre, lente, timing, vestuario) se cierra en el blockout y en las referencias, no a base de regenerar.

## El flujo (solo etapas que aportan valor)

Detalle de cada etapa en `references/workflow.md`.

| # | Etapa | Entregable | Créditos |
|---|---|---|---|
| 1 | **Guion → plan de planos** | `plan-de-planos.md`: cada plano con duración en segundos enteros, tamaño, lente, movimiento, acción, sonido, quién aparece, herramienta | 0 |
| 2 | **Biblia de continuidad** | `biblia.md`: personajes, vestuario, sets, props, luz, paleta, lente base, reglas de eje (plantilla en `templates/`) | 0 |
| 3 | **Blockout** (Blender) | video gris por sección + placas grises por set, con timing exacto | 0 |
| 4 | **Referencias** | hojas de personaje, sets fotorrealistas desde las placas grises, props; nombradas igual que en la biblia | bajo (imágenes ~0.75–2.5 cr c/u) |
| 5 | **Revisión con el equipo** | blockout + referencias aprobados | 0 |
| 6 | **Borrador** por sección | 480p con el mismo prompt y referencias del final | ~3 cr/s (Seedance 2.5) |
| 7 | **Corrección** | arreglar prompt, referencia o blockout según dónde esté el error (`references/qc-cost-protocol.md`) | 0 o borrador nuevo |
| 8 | **Final** | misma petición en resolución final | ~7 cr/s 720p · ~16 cr/s 1080p |
| 9 | **Post** | etalonaje común, grano, sonido propio, tipografía, máscaras | 0 (local) |

Atajo legítimo para producciones cortas: si un plano es fijo y simple, se puede saltar el blockout y usar un **fotograma clave aprobado** (imagen) como `start_image`.

## Selección de modelo (resumen)

Tabla completa con roles de medios, límites y costos en `references/model-matrix.md`.

- **Secciones multiplano con personajes, siguiendo un blockout:** `seedance_2_5`, modo `omni_reference`, `video_references` = blockout, `image_references` = hojas y sets (máx. 30 entre todas). Tiene borrador 480p que se puede finalizar (`draft` → `draft_job_id`).
- **Plano único desde un fotograma aprobado:** `seedance_2_5` con `start_image` (y `end_image` si hace falta llegar a un fotograma exacto), o `kling4_0` en `image-to-video` como alternativa más barata a 720p.
- **Control de cámara/óptica explícito:** `cinematic_studio_video_4_0` (mismos modos que Seedance 2.5 más ids de cámara, lente, apertura, luz, era y paleta).
- **Planos hechos en Google Flow o que deben casar con Flow:** `gemini_omni_flash_1_2` existe en ambas plataformas; usar el mismo modelo en los dos lados cuando un plano de Flow y uno de Higgsfield se cortan entre sí.
- **No usar** Veo 3.1 Fast/Quality ni Omni Flash 1.1 para proyectos nuevos en Flow: Google los retira el 5-dic-2026.
- **Lip-sync posterior:** `sync_so` (video + audio). **Escalado:** `topaz_video`. **Recorte de sujeto en video:** `sam_3_video`. Cotizar cada uno antes.

## Estructura de prompt

Plantillas completas por modelo en `references/prompt-templates.md`. El esqueleto del prompt de sección (probado en producción con Seedance 2.5) es:

`Style → CRITICAL: cómo usar el blockout → Blockout key (qué color/forma = qué cosa) → IDENTITY CRITICAL → Audio/NO MUSIC → Lighting → Color → Camera → Skin → Acting → Physics → Continuity → Technical → Characters (descripción fija pegada igual en cada prompt) → Scene → SHOT 1 … SHOT N (tamaño, ángulo, mm, movimiento, f-stop): acción + Sound`

Prompts de herramientas siempre en **inglés**; la conversación con el usuario, en español.

## Continuidad

Reglas completas en `references/continuity.md`. Las cinco que más fallan:

1. **Descripción fija del personaje**, copiada palabra por palabra en todos los prompts y con la misma referencia etiquetada.
2. **Un set = una imagen de referencia por estado** (sala oscura, sala encendida). Los cambios se hacen editando esa misma imagen («the same photograph a few minutes later…»), nunca generando otra desde cero.
3. **Relevo de fotograma:** extraer el último fotograma real con `scripts/frames.sh last` y usarlo como `start_image` de la toma siguiente cuando hay continuidad de acción. Mismo modelo en toda la cadena.
4. **Luz motivada y dirección fija** en la biblia («key from frame left, warm 3200K practical»). Se repite literal en todos los prompts del set.
5. **Eje de 180°, dirección en pantalla y mirada** anotados por plano en el plan.

## Costos y validación

Antes de cada generación, el checklist de `references/qc-cost-protocol.md`:
cotizar → comprobar saldo (`balance`) → presentar al usuario «modelo, duración, resolución, créditos, por qué» → esperar el sí → generar **un** borrador → revisar con hoja de contacto (`scripts/frames.sh sheet`) → decidir: final, corregir o descartar. Llevar el libro de gasto en `presupuesto.md` del proyecto.

## Higgsfield + Google Flow

Reparto y relevo en `references/flow-handoff.md`. En corto: Flow genera imágenes con Nano Banana sin gastar créditos de video (útil para referencias y sets), y sus políticas son más estrictas con fotos de personas reales. Por eso, por defecto, **los planos con caras reales van en Higgsfield** y Flow se encarga de sets sin personas, insertos y fotogramas de referencia. Todo se conforma a 24 fps y se etaloniza junto al final.

## Archivos

- `references/workflow.md`: cada etapa con entradas, salidas y criterio de salida.
- `references/model-matrix.md`: modelos por tipo de plano, capacidades, límites y costos cotizados con fecha.
- `references/prompt-templates.md`: plantillas por modelo y por tipo de referencia.
- `references/continuity.md`: reglas de identidad, vestuario, sets, luz, cámara y relevo.
- `references/qc-cost-protocol.md`: checklist previo, rúbrica de control de calidad y árbol de decisión de regeneración.
- `references/flow-handoff.md`: cómo trabajar con Google Flow en paralelo.
- `references/sources.md`: fuentes y de dónde sale cada regla.
- `templates/biblia.md`, `templates/plan-de-planos.md`, `templates/presupuesto.md`: plantillas para el proyecto.
- `scripts/frames.sh`: primer y último fotograma y hoja de contacto con ffmpeg.
