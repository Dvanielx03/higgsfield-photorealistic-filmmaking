# Ficha de generación · <sección / plano>

> Se rellena **antes** de cotizar. Es lo que se le muestra al usuario para pedir el sí.

| Campo | Valor |
|---|---|
| Objetivo del plano (qué cuenta y qué hace sentir) | |
| Modelo y modo | p. ej. `seedance_2_5` · `omni_reference` |
| Por qué este modelo | |
| Duración (s enteros) · formato · resolución | p. ej. 8 · 9:16 · 480p borrador |
| `video_references` | blockout `S2.mp4` (8 s) |
| `image_references` / Elements | `@persona_a_sheet`, `@set_principal` |
| `start_image` / `end_image` | |
| `audio_references` / audio generado | |
| Cotización (`estimate_video_cost`) | __ créditos · `quote_ref` |
| Saldo antes → después | |
| Criterios de QC más exigentes para este plano | p. ej. 3 y 5 (primer plano) |
| Plan B si falla | |

## Mapa temporal de referencias y audio

> Obligatorio. Método en `references/direction/reference-timeline.md`.

| Tramo del clip | Plano | Referencias activas (tags) | Qué define cada una aquí | Fuente y tramo de origen | Audio del tramo (música · efectos · ambiente · diálogo · silencio) | Origen del audio (modelo · referencia · post) |
|---|---|---|---|---|---|---|
| 0–3 s | P1 | | | | | |

- Videos y audios de referencia recortados al tramo exacto (`timeline.py trim`): ☐
- `generate_audio`: <true / false> · ¿algún tramo pide música al modelo?: <no / sí, con autorización>
- Cortes planeados para verificar con `timeline.py drift`: <3, 6, 10>

## Prompt (inglés)

```
<prompt final, armado con prompting/templates.md y la biblia>
```

## Aprobación
- [ ] El usuario aprobó esta generación en el chat (fecha y hora).
