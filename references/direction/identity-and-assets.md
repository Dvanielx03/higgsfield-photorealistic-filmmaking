# Identidad y activos: personajes, sets y props

> Cargar en la etapa de referencias y siempre que un plano tenga personas recurrentes. Lo que aquí se decide es lo que más pesa en el criterio 3 (consistencia de personajes) y en el 7 (fidelidad) de la rúbrica.

## 1. Las tres vías de identidad en Higgsfield, y cuándo usar cada una

| Vía | Qué es | Funciona con (verificado) | Úsala para |
|---|---|---|---|
| **Hoja de personaje como `image_references`** | Imagen aprobada que se envía en cada generación | Seedance 2.5, Cinema Studio 4.0, Kling 4.0 y Omni Flash 1.2 (sus roles de imagen) | **Vía por defecto para video fotorrealista**: es la que usan los workflows oficiales `drama-ads` y `angles-hf` |
| **Element** (`<<<element_id>>>` dentro del prompt) | Activo reutilizable de la biblioteca (personaje, set o prop) | **Imagen:** GPT Image 2.6, Nano Banana Pro/2, GPT Image 2, Seedream 4.5 y 5.0 lite, Cinema Studio Image 2.5. **Video:** Cinema Studio Video 2 y 3.0, Seedance 2.0, Kling 3.0 (solo con `start_image`) | Fotogramas clave y referencias en imagen; organizar el reparto del proyecto. **No sirve para Seedance 2.5 ni para Cinema Studio 4.0** |
| **Soul ID** (identidad entrenada) | Identidad entrenada de **una sola persona** | Modelos de imagen Soul (`soul_2`, `soul_cinematic`). En la **web**, también Seedance desde Elements | Muchos fotogramas fijos de la misma persona; el resultado es «clearly the same person», no idéntico píxel a píxel |

**Conflictos sobre Soul ID:**
- **Fotos:** la skill oficial `higgsfield-soul-id` dice 5–20 (ideal 8–12); el centro de ayuda (11-11-2026) dice 20–80, recientes y variadas, con al menos una de cuerpo entero y sin gafas de sol ni gorros. **Seguir la cifra del centro de ayuda**, que es más reciente.
- **Exportar:** no se puede.
- **En video por MCP:** no está documentado. Por eso, en video, la vía es la hoja como referencia.

Reglas de uso de Elements:
- El id va **dentro del prompt** (`<<<uuid>>>`). Nunca en `medias`; la forma `@nombre` no funciona en las llamadas.
- Solo se usan los elementos con `status: completed`.
- Crear un Element (`elements_create`) **escribe en la biblioteca del usuario**: requiere su sí.
- Según la [guía de Higgsfield](https://higgsfield.ai/blog/consistent-characters-locations): la descripción del Element debe listar **lo que no puede cambiar**. Las categorías son Character, Location y Prop, y el Element funciona entre proyectos.
- **Patrón de Higgsfield con dos referencias fijas:** un plano general del lugar vacío y una hoja de personaje (cuerpo entero + primer plano); prompt `@Character + action + @Location + camera angle + light`; fijos la película, la cámara, la paleta y la luz; solo cambian el ángulo y la acción.

## 2. Personas reales (los protagonistas)

1. **Consentimiento explícito de cada persona**, dicho por el usuario en el chat, antes de subir una sola foto. Sin figuras públicas: las caras de famosos provocan el error `ip_detected`.
2. **Fotos:** 3–5 por persona para las hojas (20–80 si se va a entrenar Soul ID, según el centro de ayuda). Una persona por foto, ojos visibles, luz pareja, sin gafas de sol, sin filtros fuertes, ángulos variados.
3. **Hoja de personaje** con el método oficial `character-sheet` (resumen en `models/image-models.md`): fotos adjuntas, la cara **no se describe con palabras**, edad en número, vestuario cerrado y liso, y **parada para aprobación** tras la cara y tras la hoja.
4. **Descripción fija en inglés** en la biblia (complexión, pelo, vestuario y rasgo distintivo). Se pega idéntica en todos los prompts.

## 3. Varios personajes en un mismo plano (reglas de `drama-ads`)

- Cada persona con su referencia: `@Image2 is Marco, one man, shown from several angles`.
- **Cada beat dice cuántas personas hay en plano.**
- El rasgo distintivo de cada una se repite en cada plano.
- Un doble o un gemelo usa como referencia la hoja del original.
- Una multitud se describe por cómo llena el lugar, nunca con un número.
- **Como máximo 9 imágenes por clip** en la práctica oficial, aunque el modelo admita 30. Más referencias diluyen la atención.

## 4. Orden y numeración de referencias

Orden oficial dentro de `image_references`:

1. **Frame plates:** fotogramas del set sin personajes; marcan el estado y la altura de cámara.
2. **Hoja del set.**
3. **Hojas de personajes.**
4. **Hojas de props.**

Las imágenes se numeran en ese orden: `@Image1`, `@Image2`… Añadir o quitar una **renumera todas las siguientes**: revisar las etiquetas del prompt cada vez. La hoja de estilo maestra no va nunca en un clip.

## 5. Sets

- **Una referencia por set y por estado.** Los estados siguientes (de noche, encendido, destrozado) se obtienen **editando esa misma imagen**, nunca generando otra desde cero.
- **Frame plate:** tomar un fotograma del primer clip rodado en ese set, editarlo para vaciarlo de personajes y enviarlo **el primero** en los clips siguientes: «The first frame takes its state and its camera height from the plate sent first, never from the words.»
- Dos originales del mismo set hechos en paralelo divergen: el segundo se hace **después**, a partir de un fotograma del primero.
- **Profundidad de generación:** a 1080p, como mucho 2 generaciones encadenadas (una referencia hecha de otra referencia); a 720p o 480p, como mucho 1. Cada copia de una copia pierde fidelidad.
- **Nuevos ángulos de un set:** `/3d-jutsu`, con el master como identidad y el ángulo como cámara.

## 6. Props

- Una hoja por prop importante, enviada en **cada** clip donde aparece.
- Sin marcas: `a plain unbranded <thing>`. La etiqueta de un producto real solo se lee en un inserto cerrado, con el producto llenando el plano.

## 7. Registro de activos (en la biblia)

| id | Tipo | Archivo / job id / media id | Aprobado | Vía (refs · Element · Soul) | Notas |
|---|---|---|---|---|---|

Los ids de Higgsfield (job, media y element) se guardan aquí para reutilizarlos sin volver a subir ni a generar.
