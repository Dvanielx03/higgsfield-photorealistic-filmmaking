# Router de modelos

> Cargar en la etapa de plan de planos para asignar técnica y modelo a cada plano. Después, cargar **solo** la ficha del modelo elegido.
> Antes de producir: `models_explore action=get` del modelo elegido (los esquemas cambian) y `estimate_*_cost`.

## Árbol de decisión (video)

```
¿El plano muestra personas reales o personajes recurrentes?
├─ No ─► ¿Es un plano casi fijo (ficha, inserto, fondo)?
│        ├─ Sí ─► IMAGEN + parallax en post                            (image-models.md)
│        └─ No ─► Omni Flash 1.2 o Seedance 2.5 Flash (prueba barata)  (kling-omni-veo.md)
└─ Sí ─► ¿Es una sección multiplano o con cámara compleja?
         ├─ Sí ─► ¿Hace falta luz idéntica fijada por parámetro?
         │        ├─ Sí ─► Cinema Studio 4.0 + light_custom             (cinema-studio.md)
         │        └─ No ─► SEEDANCE 2.5 omni_reference + blockout        (seedance-2-5.md)
         └─ No (plano único) ─► ¿Hay un fotograma clave aprobado?
                  ├─ Sí ─► ¿Diálogo con la voz real?
                  │        ├─ Sí ─► Seedance 2.5 + audio_references      (seedance-2-5.md)
                  │        └─ No ─► Kling 4.0 image-to-video (barato) o Seedance 2.5
                  └─ No ─► crear primero el fotograma clave (imagen) y volver aquí
```

¿El plano ya existe y tiene un defecto local? → `post-tools.md` antes de regenerar.

## Matriz resumida

| Técnica | Modelo | Costo cotizado (9:16)* | Fuerte en | Débil en |
|---|---|---|---|---|
| Sección multiplano + blockout | `seedance_2_5` | 3 · 7 · 16 cr/s (480p borrador · 720p · 1080p) | Identidad con referencias, video y audio de referencia, borrador finalizable, edición y extensión | Cortes no exactos (±0,3–2,8 s) |
| Luz fijada por parámetro | `cinematic_studio_video_4_0` | 7 cr/s (720p) | `light_custom`, modos iguales a Seedance | Ids creativos no descubribles; sin 4K; sin Elements |
| Multiplano con un prompt por plano | `cinematic_studio_video_3_5` | 5 cr/s (720p) | `multi_prompt` con duraciones | `prompt_language` en chino por defecto; máx. 15 medios |
| i2v desde fotograma | `kling4_0` | 2,5 cr/s (720p) | Barato; fotogramas intermedios ordenados; HDR | Audio no declarado |
| Escalado fiel con prompt | `kling4_0` `video-edit` | ≈ 4 cr/s (1080p) | Mantiene planos, diálogo y texto | Entrada ≥ 720 px; partes de ~15 s |
| Ambiente sin personas | `gemini_omni_flash_1_2` | 2,25 cr/s (720p) | Barato, audio nativo | Corta entre planos si no se pide un plano único |
| Prueba de concepto | `seedance_2_5_flash` | 2 cr/s (480p) | Muy barato | No finaliza como 2.5 |

\*Cotizaciones del 24-nov-2026 con `estimate_video_cost`. Son orientativas: re-cotizar.

## Imagen

| Pieza | Modelo |
|---|---|
| Hoja de personaje Realism (fotos reales adjuntas) | `gpt_image_2_6` 16:9 2K (método `character-sheet`) |
| Cara de casting sin foto | `soul_2` 3:4 |
| Hoja de set y ángulos de set (live action) | `seedream_5_5` 2K |
| Fotograma héroe | `cinematic_studio_2_5` o `nano_banana_pro` |
| Variantes y ediciones del mismo encuadre | `gpt_image_2_6` (edición con `@img1` como base) |

## Lo que el router nunca hace

- Elegir un modelo por novedad: siempre por la técnica que pide el plano.
- **Mezclar modelos dentro de una misma toma continua o de una extensión:** cambian la textura y el color.
- Usar Elements con Seedance 2.5 o Cinema Studio 4.0 (no están soportados; van como `image_references`).
- Inventar ids de Cinema Studio.
