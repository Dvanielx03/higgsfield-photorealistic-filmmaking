# Fuentes

## Fuentes principales
1. **Thomas Lundström, «Claude + Blender Is The Best Way To Make AI Commercials»**, YouTube, 20-nov-2026. https://www.youtube.com/watch?v=jc0Qh09Qrlo
   - Anuncio de 47 s hecho con solo 3 generaciones de Seedance 2.5 (más 4 borradores). Costo reportado: unos 32 USD.
   - De aquí salen:
     - el blockout como paso central;
     - las secciones de segundos enteros;
     - el borrador antes del final;
     - las referencias con nombre como etiqueta;
     - la petición de que los sets se sientan habitados;
     - la idea de corregir el error donde nace (prompt, referencia o blockout);
     - el silenciar la música de Seedance y separar las pistas;
     - el grano en post.
2. **Thomas Lundström, «Claude and Blender setup guide»** y **«Headphone commercial: every prompt and asset»** (PDF de su comunidad de Skool; no se redistribuyen en este repositorio).
   - De aquí salen:
     - la estructura del prompt de sección (Style → CRITICAL blockout → Blockout key → IDENTITY → NO MUSIC → …);
     - las plantillas de hoja de personaje;
     - el paso de placa gris a set;
     - el «same photograph a few minutes later».
3. **Repositorio oficial `higgsfield-ai/skills`**, versión 0.14.0, commit 27000402 del 5-nov-2026, idéntico a las skills instaladas en local.
   - De aquí salen:
     - que el modelo de video por defecto es `seedance_2_5`;
     - el límite de unos 200 tokens en prompts simples;
     - que en imagen a video se describe el movimiento;
     - que conviene formular en positivo;
     - que Soul ID solo funciona con modelos de imagen;
     - el relevo de último fotograma («Never mix models mid-chain»), que solo aparece en la skill de websites.
4. **Catálogo y cotizaciones del conector de Higgsfield** (`models_explore`, `estimate_video_cost`, `estimate_image_cost`), consultados el 24-nov-2026.

## Google Flow / Gemini Omni / Veo
- Créditos y planes: https://support.google.com/flow/answer/16526234
- Modelos y retiros: https://support.google.com/flow/answer/16352836
- Funciones (Ingredients, Frames, Extend, edición): https://support.google.com/flow/answer/16353334 · https://support.google.com/flow/answer/16935718 · https://support.google.com/flow/answer/16935308
- Imágenes en Flow: https://support.google.com/flow/answer/16729550
- Personas reales y política: https://support.google.com/flow/answer/17102997 · https://support.google.com/flow/answer/16719589
- Omni (API): https://aistudio.google.com/docs/omni
- Anuncio de Omni Flash 1.2 (5-nov-2026): https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/
- Guía de prompts de Omni: https://deepmind.google/models/gemini-omni/prompt-guide/
- Guía de prompts de Veo (Vertex AI): https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide · buenas prácticas: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice

## Pendientes de verificar
- Costo de finalizar un borrador de Seedance 2.5 (`draft_job_id`).
- Créditos mensuales del plan Higgsfield Plus. Hay fuentes que dicen 1.000 y otras 1.200; ver higgsfield.ai/pricing.
- Calidad real del lip-sync de Seedance 2.5 con `audio_references`.
