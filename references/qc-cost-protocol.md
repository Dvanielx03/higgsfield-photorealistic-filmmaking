# Validación y control de costos

## Checklist antes de cada generación (todas en sí)

1. ☐ El plano o la sección está en el plan y la biblia está cerrada para lo que aparece.
2. ☐ El blockout (o el fotograma clave) de esta sección está aprobado por el usuario.
3. ☐ Las referencias están aprobadas, subidas y etiquetadas con el nombre de la biblia.
4. ☐ La duración es un número entero igual a la del blockout.
5. ☐ Formato 9:16 (o el del proyecto) explícito en los parámetros.
6. ☐ Re-consulté el modelo (`models_explore action=get`) y los parámetros siguen existiendo.
7. ☐ Cotización hecha (`estimate_video_cost`) y saldo comprobado (`balance`).
8. ☐ Presenté al usuario: modelo · modo · duración · resolución · créditos · saldo después · por qué.
9. ☐ **El usuario dijo que sí en el chat a esta generación concreta.**
10. ☐ Es un **borrador** (salvo que el borrador ya esté aprobado).

Generar con el `quote_ref` de la cotización para que la petición sea exactamente la cotizada.

## Escalera de costos (de barato a caro)

1. Plan, biblia y blockout: 0 cr.
2. Imágenes de referencia y fotogramas clave: ~0,75–2,5 cr cada una.
3. Borrador de video 480p: ~3 cr/s (Seedance 2.5).
4. Final 720p: ~7 cr/s.
5. Final 1080p: ~16 cr/s.
6. Escalado o utilidades: cotizar.

Nunca se sube un escalón sin haber aprobado el anterior.

## Rúbrica de control de calidad del borrador

Revisar con `bash scripts/frames.sh sheet borrador.mp4` (hoja de contacto) y el video a velocidad normal.

| Criterio | Pasa si… |
|---|---|
| Identidad | La cara es reconocible en cada plano donde se ve; sin cambios entre cortes |
| Vestuario y props | Igual que la biblia; número correcto de objetos |
| Set y luz | Coincide con la referencia; la luz viene del mismo lado |
| Cámara | Sigue el blockout: encuadre, lente y timing de cortes |
| Movimiento | Peso y velocidad humanos; manos con cinco dedos y bien agarradas; sin deformaciones |
| Expresión | Coherente con la acción; mirada al punto correcto |
| Artefactos | Ni texto, ni geometría del blockout, ni parpadeo, ni objetos que aparecen o desaparecen |
| Audio (si se usa) | Sin música no pedida; efectos sincronizados |

## Árbol de decisión

- **Todo pasa** → final (finalizar el borrador o regenerar en la resolución final).
- **Falla algo que está en el blockout** (pose rara, objeto con forma rara, timing) → corregir el blockout → nuevo borrador.
- **Falla una referencia** (el set salió vacío, un personaje tomó el fondo gris de la hoja) → corregir la imagen de referencia (edición barata) → nuevo borrador.
- **Falla el prompt** (objeto duplicado, acción mal entendida) → corregir la frase concreta → nuevo borrador.
- **Falla solo un detalle menor en un plano final ya aceptable** → arreglarlo en post (recorte, reencuadre, máscara, grade) antes de pensar en regenerar.
- **Dos borradores fallan por lo mismo** → parar y replantear el plano (simplificar la acción, dividir la sección o cambiar de técnica). No insistir.

## Libro de gasto

Cada generación se anota en `presupuesto.md` del proyecto (plantilla en `templates/`): fecha, sección, modelo, parámetros, créditos cotizados, créditos reales, resultado (aprobado o descartado) y motivo. El total se compara con el presupuesto aprobado antes de cada nueva generación.

## Reservas

Presupuestar **1 borrador + 1 corrección por sección** y una reserva del 15 % del total. Si la reserva se agota, se para y se replantea con el usuario.
