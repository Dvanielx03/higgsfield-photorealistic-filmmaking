# Principios de prompting para Higgsfield

> Cargar antes de escribir cualquier prompt. Las plantillas concretas están en `templates.md`; las reglas propias de cada modelo, en su ficha de `models/`.

## Reglas universales (verificadas en fuentes oficiales)

1. **Prompts en inglés.** La conversación con el usuario, en su idioma. El diálogo hablado, en el idioma de la pieza, con la frase que lo fija.
2. **Escribir el estado, no el fallo que se teme.** «The image model draws every noun it reads and ignores "no", "not" and "without"» (`character-sheet`). En lugar de `no blur`, escribir `tack sharp`; en lugar de `no people`, describir el lugar vacío.
   - **Excepciones**, en bloque y al final: `No music and no score.`, el bloque de blockout `Never copy how it looks…` y las frases de cierre oficiales de las hojas de set. Son textos probados en producción.
3. **Sustantivos concretos y números.** Edad en número, lente en mm, segundos en los beats, cuántas personas hay en plano.
4. **Una acción física por plano** y un movimiento de cámara por plano.
5. **Una mirada se escribe como la cara que mira** (cejas, ojos, boca), no como su objetivo.
6. **Imagen a video: describir el movimiento,** no la imagen (guía oficial de `higgsfield-generate`).
7. **Edición de imagen: describir solo el cambio** + `Keep everything else exactly as it is`.
8. **Sin marcas, sin famosos, sin texto legible:** `a plain unbranded <thing>`. El texto y los títulos van en post.
9. **Longitud:**
   - Prompts simples: unos 200 tokens (guía de `higgsfield-generate`).
   - Secciones multiplano: largas y estructuradas, por bloques. Así se producen los clips oficiales de `drama-ads` y los del método Thomas.
   - Hojas de set oficiales: entre 4.800 y 5.500 caracteres.
10. **Copiar, no parafrasear:** los bloques de la biblia (personaje, set, luz, color) se pegan literales en cada prompt.

## Vocabulario de fotorrealismo

| Capa | Frases que funcionan |
|---|---|
| Medio | `photorealistic live action`, `shot like a feature film`, `high-end television commercial` |
| Óptica | `<mm> lens`, `shot wide open at f/1.4, shallow depth of field, eyes pin sharp`, `natural optical softness at the edges` |
| Obturador y movimiento | `180° shutter motion blur`, `24fps` |
| Textura | `fine film grain`, `pore-level skin realism, natural texture, completely unretouched` |
| Luz | Fuente motivada + dirección + calidad + temperatura: `soft window light from behind her, 5600K, gentle falloff, light haze` |
| Actuación | `understated and real, micro-pauses before reactions, precise eye-line, living eyes, visible breathing` |
| Física | `real weight and inertia, correct contact shadows, cloth and hair react to movement` |
| Atmósfera | `light haze`, `dust motes in the light shafts`, `soft halation on highlights` |
| Imperfección | `lived-in`, `real-world wear and irregularity`, `slightly asymmetrical face` |

Consejos de Higgsfield contra el «aspecto IA» ([blog, 17-08-2026](https://higgsfield.ai/blog/ai-video-look-real-2026); son consejos del fabricante, no pruebas medidas):
- una fuente de luz real y con dirección;
- cámara que se mueve con alguna imperfección;
- profundidad de campo reducida;
- **instrucciones físicas en lugar de la palabra «cinematic»**;
- que se note el peso y el apoyo de los pies.

Evitar lo que delata la IA: `ultra detailed, 8k, masterpiece, hyperrealistic, trending`. No describen nada físico.

Excepción del workflow de escalado: en `video-edit` de Kling no se usan palabras de etalonaje ni de imagen suave (ver `models/kling-omni-veo.md`).

## Etiquetas de referencias

- Seedance 2.5 y Cinema Studio 4.0: `@Image1`, `@Image2`… en el **orden de envío**; `@vid1` para el blockout; `@Audio1` para la voz.
- Cada etiqueta se declara en el prompt con su identidad: `@Image2 is Andrés, one man, shown from several angles`.
- Elements (solo en los modelos que los admiten): `<<<element_id>>>` dentro del prompt.

## Bloques obligatorios según el caso

| Caso | Bloque |
|---|---|
| Hay blockout | `CRITICAL: @vid1 is a coarse grey blockout…` + `Blockout key` |
| Hay personas recurrentes | `IDENTITY, CRITICAL: …` |
| Clip con audio generado | `No music and no score.` |
| Diálogo | Frase de idioma + quién habla, las palabras entre comillas y cómo lo dice |
| Varios personajes | Cuántos hay en cada beat |
| Plano único sin cortes | Singular en todo el prompt; con Omni, `single continuous shot` |
| Cierre | Frase de mantenimiento: personajes, props, cielo y luz que no cambian |
