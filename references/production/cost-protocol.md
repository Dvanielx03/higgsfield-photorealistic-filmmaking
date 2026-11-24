# Protocolo de costos y autorización

> Cargar antes de **cualquier** llamada que genere, escale, edite o cree datos en Higgsfield. Las cotizaciones son gratis; las generaciones no.

## Checklist previo (todas en sí)

1. ☐ El plano o la sección está en el plan y la biblia cubre todo lo que aparece.
2. ☐ El blockout o el fotograma clave de esta sección está aprobado.
3. ☐ Las referencias están aprobadas y subidas (`media_upload` → PUT → `media_confirm`), con su id anotado en la biblia.
4. ☐ `models_explore action=get` del modelo: los parámetros siguen existiendo.
5. ☐ `aspect_ratio` y `resolution` explícitos; duración en segundos enteros igual a la del blockout.
6. ☐ `estimate_video_cost` / `estimate_image_cost` hecho; `quote_ref` guardado.
7. ☐ `balance` consultado.
8. ☐ Ficha (`templates/prompt-card.md`) presentada al usuario: modelo · modo · duración · resolución · créditos · saldo después · por qué.
9. ☐ **El usuario dijo que sí en el chat a esta generación o a este lote concreto.**
10. ☐ Es un borrador, salvo que el borrador ya esté aprobado.

Generar con `params: {"ref": "<quote_ref>"}` para que se ejecute **exactamente** lo cotizado.

## Reglas de gasto

- **Nunca reutilizar ni calcular de memoria un precio:** cotizar en el momento (regla de `drama-ads`). Las cifras de esta skill son orientativas y llevan fecha.
- **En cada aprobación, mostrar «gastado X de ≈ Y».**
- **Primer envío de cada modelo y modo, solo.** Se revisa antes de lanzar el resto.
- **No reenviar un trabajo pendiente.** Tras un timeout, consultar el estado del trabajo antes de reintentar.
- **Generaciones ilimitadas (`use_unlim`):** solo si la cuenta tiene asignación para ese modelo y el usuario lo pide. Si se omite el campo y hay asignación, el servidor no envía nada y devuelve la pregunta `unlim_choice` para el usuario.
- **`upscale_video` no admite cotización previa:** avisar al usuario de que el costo se verá al ejecutar.
- **Escribir en la biblioteca** (Elements, proyectos o carpetas) también requiere el sí del usuario, aunque no gaste créditos.

## Escalera de costos

| Escalón | Créditos orientativos (24-nov-2026, 9:16) |
|---|---|
| Plan, biblia, blockout, cotizaciones | 0 |
| Imagen de referencia o fotograma clave | 0,75–3,5 por imagen |
| Borrador Seedance 2.5 (480p) | ≈ 3 cr/s |
| Final Seedance 2.5 720p · Cinema Studio 4.0 720p | ≈ 7 cr/s |
| Final Seedance 2.5 1080p | ≈ 16 cr/s |
| i2v Kling 4.0 720p | ≈ 2,5 cr/s |
| Escalado fiel Kling 4.0 1080p | ≈ 4 cr/s |

Nunca se sube un escalón sin haber aprobado el anterior.

## Presupuesto de un proyecto

`templates/presupuesto.md`:
- Partidas: referencias, borradores, **una corrección por sección**, finales, acabado, y una **reserva del 15 %**.
- Si la reserva se agota, se para y se replantea con el usuario.
- Cada generación se anota en el libro de gasto (cotizado frente a real).

Fórmula rápida de video:

```
Σ secciones [ s × (tarifa_borrador × 2  +  tarifa_final) ]  × 1,15
```

(`× 2` porque se cuentan un borrador y una corrección por sección.)
