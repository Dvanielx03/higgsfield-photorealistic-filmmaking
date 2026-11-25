# Rúbrica de control de calidad

> Cargar después de **cada** generación (imagen de referencia, borrador o final). Si algo falla, pasar a `diagnosis.md`.

## Cómo se revisa

1. **Hoja de contacto** a 4 fps para ver movimiento y deriva:
   `bash scripts/frames.sh sheet clip.mp4 clip_sheet.png 4`
2. **Comparación lado a lado** del fotograma más revelador contra su referencia:
   `bash scripts/frames.sh compare clip.mp4 2.5 ref.png clip_vs_ref.png`
3. **Primer y último fotograma** si la toma empalma con otra (`frames.sh first|last`).
4. **Marcas de tiempo:** `python -I scripts/timeline.py drift clip.mp4 <cortes planeados>` y `frames.sh at` en cada momento del mapa temporal. Comprobar que cada referencia actuó en su tramo.
5. **Audio por tramo:** escuchar cada tramo contra el mapa (música · efectos · ambiente · diálogo · silencio).
6. **Reproducción a velocidad real**, dos veces: una mirando caras y manos y otra mirando fondo y física.
7. Anotar la puntuación en `templates/qc-report.md` del proyecto.

## Los 8 criterios (0 · 1 · 2)

| # | Criterio | 2 = cumple | 1 = defecto menor | 0 = inaceptable |
|---|---|---|---|---|
| 1 | **Fotorrealismo** | Piel con poros e imperfecciones, materiales con textura real, grano y óptica creíbles | Piel algo pulida o una superficie «de render» en segundo plano | Piel de plástico, brillo de videojuego, aspecto 3D o ilustración |
| 2 | **Coherencia física** | Peso, inercia, sombras de contacto, tela y pelo que responden; objetos que no atraviesan nada | Un detalle dudoso breve (una sombra débil, un rebote raro) | Objetos que se funden, manos que atraviesan cosas, gravedad rota, deformaciones |
| 3 | **Consistencia de personajes** | Misma cara, peinado, complexión y vestuario en todos los fotogramas y cortes | Variación leve que solo se ve en pausa | Cara distinta, cambio de ropa o de edad, rasgos que derivan |
| 4 | **Continuidad narrativa y visual** | Raccord de posición, mirada, dirección en pantalla, luz y props con los planos vecinos | Un raccord menor que se esconde con el corte | Salto de eje, luz que cambia de lado, objeto que aparece o desaparece |
| 5 | **Naturalidad de movimientos** | Ritmo humano, microgestos (respiración, parpadeo), manos bien formadas y bien agarradas | Un gesto rígido o una mano poco clara en un momento breve | Movimiento robótico, deslizamiento sin pasos, dedos de más, *morphing* |
| 6 | **Calidad cinematográfica** | Encuadre, lente, movimiento y luz como se pidieron; composición con intención | Movimiento algo distinto pero válido | Cámara errática, encuadre que corta caras, luz plana sin motivo |
| 7 | **Fidelidad a las referencias** | Set, personajes y props reconocibles como sus referencias; blockout respetado | Pequeñas diferencias de atrezo | Geometría del blockout visible, fondo gris de la hoja de personaje, set distinto |
| 8 | **Cumplimiento de la intención creativa** | Comunica lo que el plano debía contar y sentir | Se entiende, pero con menos fuerza | No cuenta lo que debía o contradice la historia |

Además, **descalificantes automáticos** (equivalen a 0 en el criterio afectado):
- texto ilegible, logotipos o marcas inventadas en imagen;
- música no pedida en el audio, o un tramo cuyo audio no coincide con el mapa temporal (suena donde debía haber silencio, falta el diálogo);
- un corte o un evento desviado más de 0,8 s de su marca cuando el plano depende de ella (sincronía con música o con tipografía);
- fotograma final inutilizable para un relevo previsto.

## Decisión

| Resultado | Acción |
|---|---|
| **≥ 14/16 y ningún 0** | Aprobar. Si era borrador → finalizar. Si era final → a post |
| **11–13 y ningún 0** | Arreglar en post si el defecto es local (ver `diagnosis.md`, columna «Arreglo sin regenerar»). Si no, una corrección dirigida |
| **Cualquier 0 en 3, 2 o 7** (identidad, física, fidelidad) | Rechazar. Diagnosticar la causa antes de gastar más |
| **≤ 10** | Rechazar y replantear el plano: simplificar la acción, dividir la sección o cambiar de técnica |
| **Mismo fallo en 2 intentos** | Parar. Cambiar de estrategia, no de semilla (ver `diagnosis.md`, «Escalera de estrategias») |

## Umbrales por tipo de plano

No todos los planos pesan igual. Ajustar la exigencia:

| Tipo de plano | Criterios que deben puntuar 2 |
|---|---|
| Primer plano o diálogo | 1, 3, 5 |
| Plano general de establecimiento | 1, 6, 7 |
| Plano de acción | 2, 5 |
| Plano de empalme con otra toma | 4 y primer y último fotograma limpios |
| Plano héroe (portada, revelación) | todos |
