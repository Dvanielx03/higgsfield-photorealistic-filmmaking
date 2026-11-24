# Plantillas de prompt

> Cargar solo la plantilla que toca. Lo que va entre `<…>` sale de la biblia, literal. Reglas generales en `principles.md`.

---

## A. Sección multiplano con blockout · Seedance 2.5 / Cinema Studio 4.0

`mode: omni_reference` · `medias`: imágenes (frame plate, set, personajes, props) → `video_references` (blockout) → `audio_references` (voz) · `duration` = duración del blockout · `aspect_ratio` y `resolution` explícitos · `draft: true` en la primera pasada (Seedance).

```
Style: Photorealistic live action, shot like a feature film on <ARRI Alexa 35>. No 3D render, no game engine, no animation look.
CRITICAL: @vid1 is a coarse grey blockout. Follow it exactly for camera position, camera movement, lens perspective and the timing of every cut, and for where each subject is, how large it is in frame, which way it faces and when it moves. There are exactly <N> shots, in the order written below, each cutting where @vid1 cuts. Never add or drop a shot. Never copy how it looks: no capsules, stripes, coloured blocks or grey geometry may appear in the result.
Blockout key: <red-black striped capsule> = <PERSON A>. <blue-black striped capsule> = <PERSON B>. <yellow box> = <prop>. The capsules carry no body motion: give every character natural human movement that keeps the capsule's position, path, speed and facing.
@Image1 is <the place, empty plate>. @Image2 is <the place sheet>. @Image3 is <PERSON A>, one <man/woman>, shown from several angles. @Image4 is <PERSON B>, …
IDENTITY, CRITICAL: <PERSON A> is @Image3 in every shot: the same face, hair and clothes; whenever the face is visible it is unmistakably that face. <same for B>.
No music and no score.
Lighting: <bible: motivated source in the world, direction, quality, K, haze>.
Color: <bible grade>.
Camera: Physical cine lenses, composed and smooth. Close shots wide open with shallow depth of field, eyes pin sharp; wide shots hold more depth. 180° shutter motion blur. Fine film grain. 24fps.
Skin: Pore-level realism, natural texture, unretouched.
Acting: Understated and real. Micro-pauses before reactions, precise eye-line, living eyes, visible breathing.
Physics: Real weight and inertia, correct contact shadows, cloth and hair react to movement.
Characters: <PERSON A>: <fixed bible description>. <PERSON B>: …
SHOT 1 (0-3 s · <size>, <angle>, <mm>, <movement>): <how many people in frame>. <one concrete action>. <face: brows, eyes, mouth>. Sound: <owned sound>.
SHOT 2 (3-6 s · …): …
Hold: <characters, props, sky and light that stay the same throughout>.
```

## B. Sección sin blockout (beats cronometrados) · Seedance 2.5

Para escenas sencillas donde el encuadre puede describirse con palabras. Clips de 10–15 s, unos 4 beats y 6 planos.

```
Style: <style line> <video words>.
@Image1 is <place>. @Image2 is <PERSON A>, one <man/woman>, shown from several angles.
0-3 s: <framing>. <how many in frame>. <action>. <face>.
3-6 s: <framing>. …
6-10 s: <framing>. … <PERSON A> says, <how>: "<line>".
10-14 s: <framing>, in silence, <action>.
Every spoken line is in <language>, exactly the words in quotes; nobody speaks any other language.
No music and no score. <sound effects named on their owner>.
Hold: <characters, props, sky and light>.
```

## C. Plano único desde un fotograma aprobado · Kling 4.0 `image-to-video` / Seedance 2.5 `start_image`

```
<Camera movement> on a <mm> lens, over <n> seconds. <Subject> <one concrete action>. <Secondary motion: hair, cloth, dust in the light>. Natural human movement with real weight. The face, clothes and lighting stay as in the first frame. 24fps, 180° shutter motion blur.
```

## D. Diálogo a cámara con la voz real · Seedance 2.5

`audio_references`: muestra original de 3–10 s de la persona. `image_references`: su hoja. Opcional: `start_image` con el fotograma clave.

```
@Image1 is <PERSON>, one <man/woman>. @Audio1 is the voice of @Image1, <calm register>: every line <he/she> speaks is in this voice.
<Medium close-up>, eye level, <50mm>, static. <PERSON> looks straight into the lens, <face>, takes a small breath and says, <how>: "<line>". Natural lip sync, a blink, subtle head movement.
In silence, <PERSON> holds the look for <n> seconds.
Every spoken line is in <language>, exactly the words in quotes; nobody speaks any other language. No music and no score.
```

Dejar al menos 4 s de silencio después de la última línea dentro del clip.

## E. Hoja de personaje desde fotos reales · `gpt_image_2_6` 16:9 2K

Usar los textos oficiales del workflow `character-sheet` cuando sea posible (`get_workflow_instructions {workflow:"character-sheet"}`). Versión resumida coherente con sus reglas:

```
A three-panel live-action character reference sheet of the person in the attached photos, a <number>-year-old <man/woman>, on a plain light-grey background. Left: full body from the front, from the neck down. Centre: full body from the back, from the neck down. Right: a head-and-shoulders portrait looking into the lens. <Wardrobe from the bible: concrete, matte materials, plain and unbranded>. Soft, even, diffused studio light from the front. Real skin texture with visible pores, unretouched. Exactly one face, in the right panel.
```

No describir los rasgos de la cara con palabras: los aportan las fotos.

## F. Set fotorrealista desde una placa gris · `seedream_5_5` / `gpt_image_2_6`

```
Turn this grey blockout into a photorealistic frame from a live-action film. Keep the layout exactly: the same camera position and <mm> lens, every wall, opening and piece of furniture where the blockout has it and at the same size. <What each grey shape is>. Dress the place so it feels truly lived in by <who uses it>: <3–6 specific details>. Lighting: <bible>. Color: <bible>. <mm> lens feel, fine film grain. The place is empty: an unoccupied room with every surface plain and unbranded.
```

## G. Variante del mismo encuadre (edición de imagen)

```
Use @Image1 as the exact base and recreate the same photograph <a few minutes later | at night | the next morning>. Keep everything identical: camera position and lens, walls, furniture, props and their positions, wardrobe, colour grade and grain. Change only this: <the change, concrete>.
```

## H. Ambiente sin personas · Gemini Omni Flash 1.2

```
<Shot size>, <angle>, <mm>, <one camera movement>. <The place, from the bible>, empty, <time of day>. <Lighting and colour from the bible>. Single continuous shot, no scene cuts. Photorealistic, fine film grain.
Audio: <ambience>. No music.
```

## I. Multiplano con un prompt por plano · Cinema Studio Video 3.5

Parámetros, no texto libre:

```json
{
  "model": "cinematic_studio_video_3_5",
  "prompt_language": "en",
  "multi_shots": true,
  "multi_prompt": [
    {"prompt": "<shot 1 in the style of template C>", "duration": 3},
    {"prompt": "<shot 2>", "duration": 4}
  ],
  "aspect_ratio": "9:16",
  "resolution": "720p"
}
```

Antes de usarlo, comprobar con `models_explore action=get` los valores de `multi_shot_mode`, `camera_style`, `light_scheme` y `color_grading`.
