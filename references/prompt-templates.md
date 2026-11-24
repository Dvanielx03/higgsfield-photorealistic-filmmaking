# Plantillas de prompt

Prompts en **inglés**. Lo que va entre `<…>` sale de la biblia, siempre literal. Límite práctico: la guía oficial de Higgsfield recomienda unos 200 tokens para prompts simples. Los prompts de **sección multiplano con blockout** son la excepción probada en producción: largos y estructurados, con un bloque por plano.

Reglas de redacción:
- **Positivo antes que negativo** («tack sharp» mejor que «no blur»). Las exclusiones críticas sí van explícitas y en bloque (`NO MUSIC, CRITICAL`, «No legible text»), porque Seedance y Omni no tienen campo de negativo.
- **Imagen a video:** describir **movimiento**, no la imagen. Lo estático ya lo fija el fotograma.
- **Edición de imagen:** describir **solo el cambio** + «Keep everything else exactly as it is».
- **Cámara siempre física:** tamaño de plano, ángulo, mm, movimiento, f-stop.
- **Luz motivada:** de dónde viene, qué calidad tiene y de qué color, copiado de la biblia.
- **Un momento por plano**, con verbos de acción concretos y microgestos («micro-pause before reacting, visible breathing»).

---

## A. Sección multiplano con blockout (Seedance 2.5 · Cinema Studio 4.0)

`mode: omni_reference` · `video_references: [blockout]` · `image_references: [hojas, sets, props]` · `duration` = duración del blockout · `aspect_ratio: 9:16` · `draft: true` en la primera pasada.

```
Style: High-end <commercial|film> shot on <ARRI Alexa 35>, photorealistic live action. No 3D render, no game engine, no animation look.
CRITICAL: @vid1 is a coarse grey blockout. Follow it exactly for camera position, camera movement, lens perspective and the timing of every cut, and for where each subject is, how large it is in frame, which way it faces and when it moves. There are exactly <N> shots, in the order written below, each cutting where @vid1 cuts. Never add or drop a shot. Never copy how it looks: no capsules, stripes, coloured blocks or grey geometry may appear in the result.
Blockout key: <red-black striped capsule> = <PERSON A>. <blue-black striped capsule> = <PERSON B>. <yellow box> = <prop>. The capsules carry no body motion: give every character natural human movement that keeps the capsule's position, path, speed and facing.
IDENTITY, CRITICAL: <PERSON A> is @<ref-a> in every shot: the same face, hair and clothes. Whenever the face is visible it is unmistakably that face. No identity drift.
NO MUSIC, CRITICAL: no music, score, melody, humming, pad, drone or rising tone anywhere. Sound design only as written in each shot. No dialogue unless written. No subtitles, titles, logos or legible text anywhere.
Lighting: <from bible: motivated source, direction, quality, colour temperature, haze>. Motivated light only.
Color: <from bible: grade, palette, black level, highlight roll-off>.
Camera: Physical cine lenses, composed and smooth, <no handheld | subtle handheld>. Close-ups wide open at f/<1.4> with shallow depth of field, eyes pin sharp. Wide shots hold more depth. 180° shutter motion blur. Fine film grain. 24fps.
Skin: Pore-level realism, natural texture, no smoothing.
Acting: Understated and real. Micro-pauses before reactions, precise eye-line, living eyes, visible breathing.
Physics: Gravity and inertia respected, real weight, correct contact shadows, cloth and hair react to movement.
Continuity: Characters, wardrobe, props and locations identical to their references in every cut. Every object stays where it was in the shot before.
Characters: <PERSON A>: @<ref-a>. <fixed description from bible>. <PERSON B>: ...
Scene: <location>: @<ref-set>. <fixed description from bible>.
SHOT 1 (<size>, <angle>, <mm>, <movement>, f/<x>): <one moment, concrete action>. Sound: <...>.
SHOT 2 (...): ...
```

## B. Plano único desde un fotograma aprobado (i2v)

`start_image` = fotograma clave aprobado (y `end_image` si debe aterrizar en un fotograma exacto).

```
<Camera movement> on a <mm> lens. <Subject> <single concrete action with timing: "over two seconds…">. <Secondary motion: hair, cloth, dust in light>. Natural human movement, real weight, no morphing. The face, clothes and lighting stay exactly as in the first frame. No legible text. 24fps, 180° shutter motion blur.
```

## C. Hoja de personaje desde fotos reales (imagen)

Referencias: 3–5 fotos de la persona (con consentimiento). Modelo: `seedream_v5_pro` o `gpt_image_2_6`.

```
Photorealistic character reference sheet of the person in the attached photos, identical face, proportions and skin tone, on a seamless neutral mid-grey studio background. Panels: full-body front view, full-body left profile, full-body back view, a tight face portrait looking into the lens, and a three-quarter head-and-shoulders view. Wardrobe: <fixed wardrobe from bible, plain and unbranded>. Real skin texture with visible pores and natural imperfections, completely unretouched. Soft, even light from a large overhead softbox with gentle fill, neutral true-to-life colour, deep focus. Same person in every panel. No text, labels or logos.
```

## D. Set fotorrealista desde una placa gris del blockout (imagen)

```
Turn this grey blockout into a photorealistic frame from a high-end <commercial|film>. Keep the layout exactly: the same camera position and <mm> lens, every wall, opening and piece of furniture where the blockout has it and at the same size. <What each grey shape is>. Dress the space so it feels truly lived in by <who uses it>: <3–6 specific details>. Lighting: <from bible>. Color grade: <from bible>. No people, no legible text or logos, no capsules or grey geometry. <mm> lens feel, fine film grain.
```

## E. Variante de un set o de un fotograma (edición de imagen)

```
Use @img1 as the exact base and recreate the same photograph <a few minutes later | at night | in the morning>. Keep everything identical: camera position and lens, walls, furniture, props and their positions, wardrobe, colour grade, grain. Change only this: <the change, concrete>. No new objects, no text.
```

## F. Google Flow / Gemini Omni Flash 1.2

Estructura recomendada por Google: **cinematografía + sujeto + acción + contexto + estilo y ambiente**, con el audio en frases aparte.

```
<Shot size, angle, lens, camera movement>. <Subject with the fixed bible description>. <Action, one moment>. <Location and time of day>. <Lighting and colour from bible>. Single continuous shot, no scene cuts. Photorealistic, shot on <camera>, fine film grain.
Audio: <ambience>. SFX: <...>. No music.
```
- Omni corta entre planos por defecto: pedir «single continuous shot» cuando se quiere un plano único.
- Diálogo según la guía actual de Google: `<Person> says: <line>.` con dos puntos y **sin comillas**; las comillas pueden escribir el texto en pantalla.
- Con referencias (`@`), sujeto sobre fondo liso y sin personas extra en las referencias de lugar.

## G. Diálogo a cámara con la voz real (Seedance 2.5)

`audio_references: [voz grabada]` · `start_image` = fotograma aprobado del personaje.

```
<Medium close-up>, eye level, <50mm>, static. <PERSON> looks straight into the lens and speaks the line in the reference audio with natural lip sync, subtle head movement, a blink, a breath before speaking. The face, clothes and lighting stay exactly as in the first frame. No music, no subtitles.
```
Probar siempre en borrador. Si el lip-sync falla, generar sin voz y aplicar `sync_so` con el audio real (cotizar).
