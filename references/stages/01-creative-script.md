# Etapa 1 · Desarrollo creativo y guion

**Objetivo:** una historia aprobada que se pueda fabricar con IA dentro del presupuesto, en el formato y la plataforma correctos.

## Requisitos
- Brief cerrado:
  - objetivo, público, duración, **formato y plataforma de destino** (16:9 cine o feed, 9:16 reels);
  - restricciones (reglas de un concurso, consentimiento de las personas reales, créditos disponibles).
- Referencias de inspiración **desglosadas con timecode** (`direction/reference-timeline.md` §1). Lo que se toma de cada una, anotado con su segundo.
- Guion por escenas con duración aproximada, y para cada momento: qué se ve, qué se oye (música · efectos · ambiente · diálogo · silencio) y qué se siente.
- Cada efecto clasificado: **generación**, **imagen + post**, **solo post** (`direction/pipeline.md`).

## Errores que se deben evitar
| Error | Regla |
|---|---|
| Decidir el formato tarde y rehacer todos los encuadres | El formato y la plataforma se fijan en el brief, antes del primer encuadre |
| Pedir al modelo textos, gráficos, fundidos o cámara lenta | Van a post; el guion los marca como tales |
| Escenas que dependen de muchas caras en primer plano sin medir el costo | Contar los segundos de cara, diálogo o cámara compleja: son los caros (`production/blender-kling-seedance.md` §5) |
| Copiar una referencia en lugar de traducir su lenguaje | Se extraen principios con evidencia (timecode); el contenido es propio |
| Diálogo que termina al final del clip | La última línea termina ≥ 4 s antes del final del clip generado; se prevé la cola |

## Criterios de aprobación (puerta)
- [ ] El usuario aprobó el guion y el formato por escrito en el chat.
- [ ] Cada escena tiene duración, intención (qué cuenta y qué hace sentir) y audio por tramo.
- [ ] Cada referencia usada tiene su desglose con timecode.
- [ ] Hay estimación de costo de alto nivel compatible con el saldo real (`balance`).
