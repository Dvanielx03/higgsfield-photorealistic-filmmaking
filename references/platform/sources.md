# Fuentes y de dónde sale cada regla

> Investigación del 24-nov-2026. Cada regla de la skill sale de una de estas fuentes. Si dos fuentes chocan, el módulo lo marca como **conflicto** y explica qué opción se toma.

## 1. Conector de Higgsfield (fuente técnica principal)

- **Esquemas de modelo** (`models_explore action=get`): parámetros, duraciones, roles de medios, relaciones de aspecto y si admiten ilimitado.
- **Cotizaciones** (`estimate_video_cost`, `estimate_image_cost`) en 9:16 → tarifas de `models/*.md`.
- **Workflows oficiales** (`get_workflow_instructions`, `get_workflow_bundle_file`). De cada uno sale:
  - **`drama-ads`:** el orden del prompt de clip, las etiquetas @, el máximo de 9 imágenes, la voz con `audio_references`, la desviación medida de los cortes, el largo de clip, los frame plates, la profundidad de generación, la regla de no fijar `start_image` en las costuras, los reintentos y la regla de no reutilizar precios.
  - **`character-sheet`:** el método de hojas de personaje, la edad en número, la redacción positiva, «exactly one face».
  - **`angles-hf`:** lentes, número de planos por energía, variedad de ángulos, 2–14 planos por clip y la regla de no usar plurales.
  - **`lighting-hf` · `grade-hf`:** re-iluminar y re-etalonar con `video_edit`.
  - **`higgsfield-enhance-video`:** escalado fiel con Kling 4.0 y control de calidad por SSIM.
  - **`video-sound-design` · `video-montage`:** niveles y loudness, montaje y subtítulos.
  - **`/3d-jutsu`:** ángulos de un set.
- **Descripción de `elements_search`:** qué modelos admiten Elements.

## 2. Documentación oficial de Higgsfield (web)

- Centro de ayuda:
  - [Seedance](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-seedance) (17-11-2026)
  - [Cinema Studio](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio) (19-11-2026)
  - [Kling](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-kling) (17-11-2026)
  - [Soul ID](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character) (11-11-2026)
  - [Soul Cinema](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-soul-cinema)
  - [Nano Banana](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-nano-banana)
  - [Popcorn](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-popcorn)
  - [Lipsync Studio](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-lipsync-voiceover-and-aspect-ratios)
  - [Qué modelo usar](https://higgsfield.ai/creator-hub/help-center/ai-models/which-ai-model-should-i-use)
  - [Uso comercial](https://higgsfield.ai/creator-hub/help-center/account/who-owns-my-generations-and-can-i-use-them-commercially)
- Guías y blog:
  - [Guía de prompting de Seedance 2.5](https://higgsfield.ai/blog/seedance-2-5-prompting-guide) (13-08-2026)
  - [Seedance 2.5 en Higgsfield](https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026) (10-11-2026)
  - [Guía completa de Cinema Studio 4.0](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide) (27-10-2026)
  - [Kling 4.0 en Higgsfield](https://higgsfield.ai/blog/kling-4-0-on-higgsfield) (20-10-2026)
  - [Personajes y localizaciones consistentes](https://higgsfield.ai/blog/consistent-characters-locations) (04-11-2026)
  - [Que el video de IA parezca real](https://higgsfield.ai/blog/ai-video-look-real-2026) (17-08-2026)
  - [3D Jutsu](https://higgsfield.ai/blog/higgsfield-3d-jutsu) (05-09-2026)
  - [Plugin de Blender](https://higgsfield.ai/blog/higgsfield-blender-plugin) (28-10-2026)
- Guía de ByteDance para Seedance publicada por Higgsfield: [enterprise help center](https://higgsfield.ai/enterprise-help-center/platform/seedance-prompt-guides).
- Planes: [pricing.md](https://higgsfield.ai/pricing.md) (24-11-2026). Novedades: [changelog](https://higgsfield.ai/changelog).
- Skills oficiales: [`higgsfield-ai/skills`](https://github.com/higgsfield-ai/skills) v0.14.0 (commit 27000402, 05-11-2026). De aquí salen:
  - el límite de unos 200 tokens en prompts simples;
  - que en imagen a video se describe el movimiento;
  - que conviene formular en positivo;
  - Soul ID para imagen;
  - los comandos del CLI.

## 3. Guías de los fabricantes de modelos

- Kling 4.0: [guía de usuario](https://kling.ai/quickstart/kling-4-model-user-guide) (04-11-2026).
- Gemini Omni: [documentación de la API](https://aistudio.google.com/docs/omni) y [guía de prompts de DeepMind](https://deepmind.google/models/gemini-omni/prompt-guide/).
- Veo 3.1: [guía de prompting de Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1) (15-10-2025).
- Nano Banana: [guía de prompting de Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana) (05-03-2026).
- GPT Image: [guía de prompting de OpenAI](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.6).
- Seedream: no se pudo acceder a la guía oficial (no documentado).

## 4. Práctica de producción

- **Thomas Lundström:**
  - video [*Claude + Blender Is The Best Way To Make AI Commercials*](https://www.youtube.com/watch?v=jc0Qh09Qrlo) (20-11-2026);
  - su guía de instalación y su PDF de prompts (comunidad de Skool; no se redistribuyen aquí).
  - De aquí salen el blockout como paso central, las secciones de segundos enteros, el borrador antes del final, los sets «lived in» y la corrección del error en su origen.
- **Pruebas de terceros con Seedance 2.5:**
  - [MindStudio](https://www.mindstudio.ai/blog/seedance-2-5-review-guide): proporción de 3,2 s generados por segundo útil; morphing en la acción rápida.
  - [Kittl](https://www.kittl.com/blogs/kittl-review-seedance-2-5/): el fotograma inicial mejora la estabilidad; los briefs con muchos planos se fusionan.
  - Se usan solo como indicio, no como regla.

## 5. Pendiente de verificar con trabajos reales

- Costo de finalizar un borrador de Seedance 2.5 con `draft_job_id`.
- Calidad del lip-sync de Seedance 2.5 con `audio_references`, frente a `intone` y `sync_so`.
- Si `hf_mult_motion_control` (Genjutsu) admite 9:16.
- Los ids de los controles creativos de Cinema Studio 4.0.
