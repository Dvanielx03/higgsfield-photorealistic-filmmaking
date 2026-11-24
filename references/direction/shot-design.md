# Diseño de planos: lenguaje cinematográfico

> Cargar al escribir el plan de planos o el bloque `SHOT N (...)` de un prompt. Es conocimiento de oficio, independiente del modelo: el modelo solo lo ejecuta si se le pide con estas palabras.

## 1. Cada plano responde tres preguntas

1. **¿Qué tiene que entender el espectador?** (información)
2. **¿Qué tiene que sentir?** (emoción)
3. **¿Desde dónde lo mira?** (punto de vista: testigo, cómplice, sujeto)

Si un plano no responde a ninguna, sobra. Si responde a las tres, el prompt casi se escribe solo.

## 2. Vocabulario que los modelos entienden (en inglés en el prompt)

| Tamaño | Prompt | Uso dramático |
|---|---|---|
| Gran plano general | `extreme wide shot` | Escala, soledad, ubicación |
| Plano general | `wide shot` / `full shot` | Acción completa, relación con el espacio |
| Plano medio | `medium shot` | Gesto y diálogo |
| Primer plano | `close-up` | Emoción |
| Primerísimo / detalle | `extreme close-up` / `insert` | Tensión, información clave |
| Plano conjunto | `two shot` | Relación entre dos personajes |
| Sobre el hombro | `over-the-shoulder` | Diálogo, punto de vista |
| Subjetivo | `POV shot` | Ponerse en la piel del personaje |

| Ángulo | Prompt | Lectura |
|---|---|---|
| Normal | `eye level` | Neutral, verdad |
| Picado | `high angle` | Vulnerabilidad |
| Contrapicado | `low angle` | Poder, amenaza |
| Cenital | `overhead` / `top-down` | Destino, patrón, distancia |
| Holandés | `Dutch angle` | Desequilibrio |

| Lente (formato completo) | Carácter | Úsala para |
|---|---|---|
| 14–18 mm | Deforma, exagera la profundidad | Espacio, caos, POV extremo. **Nunca para caras de cerca** |
| 24–28 mm | Amplio y natural | Establecer, seguir acción, POV |
| 35 mm | El ojo narrativo | **Lente base por defecto** |
| 50 mm | Neutral e íntimo | Plano medio, diálogo |
| 85 mm | Comprime y aísla | Retrato, emoción |
| 100–135 mm | Muy comprimido | Observación a distancia, tensión |

Profundidad de campo: `shot wide open at f/1.4, shallow depth of field, eyes pin sharp` para aislar; `f/5.6–f/8, deep focus` para planos generales con información.

## 3. Movimiento de cámara motivado

Un movimiento sin motivo delata la IA. Cada movimiento responde a algo:

| Movimiento | Prompt | Motivación típica |
|---|---|---|
| Fija | `static, locked-off` | Observar, dejar actuar. **La opción más segura para el fotorrealismo** |
| Acercamiento lento | `slow push-in` | Revelación interior, tensión que crece |
| Alejamiento | `slow pull-back` | Revelar contexto, soledad, final |
| Travelling lateral | `lateral tracking shot` | Acompañar un desplazamiento |
| Seguimiento | `follow shot from behind` | Inmersión, persecución |
| Paneo / tilt | `pan left`, `tilt up` | Mirar lo que el personaje mira |
| Grúa | `crane up` / `crane down` | Cambio de escala, entrada o salida de escena |
| Órbita | `slow orbit` | Momento suspendido. **Usar con moderación** |
| Cámara en mano | `subtle handheld` | Urgencia, documental. Solo si la escena lo pide |
| Dolly zoom | `dolly zoom` | Vértigo, revelación. Una vez por pieza como máximo |

Reglas:
- **Un movimiento principal por plano.** Combinar tres movimientos en un plano es la receta del «look IA».
- **Velocidad humana.** Los modelos fallan más con la acción rápida y la física compleja. El ritmo rápido se consigue con **cortes y speed-ramp en post**, no con movimientos violentos.
- Escribir la **duración** del movimiento cuando importa: `over four seconds, a slow push-in from medium to close-up`.

## 4. Continuidad de lenguaje

- **Regla de 180°:** en un diálogo, la cámara se queda a un lado del eje entre los personajes. Se anota en el plan.
- **Dirección en pantalla:** si alguien sale por la derecha del cuadro, entra por la izquierda en el plano siguiente.
- **Raccord de mirada:** la mirada al final de un plano apunta a lo que muestra el siguiente.
- **Corte en movimiento:** cortar durante una acción (`cut on the move`) esconde el empalme entre generaciones.
- **Progresión de tamaños:** general → medio → primer plano para entrar en una escena; saltar de general a primerísimo solo como golpe deliberado.

## 5. Luz con intención

Siempre **motivada**: de dónde viene (ventana, lámpara, pantalla, sol), desde qué lado del cuadro, dura o suave, y temperatura.

| Esquema | Prompt | Lectura |
|---|---|---|
| Clave baja | `low-key, single motivated source, deep shadows` | Drama, misterio |
| Clave alta | `high-key, soft even light` | Calma, comercial limpio |
| Contraluz y contorno | `backlit, warm rim light separating the subject` | Épica, revelación |
| Luz de ventana | `soft window light from frame left, gentle falloff` | Naturalismo |
| Práctica | `practical lamps in frame, warm 3200K pools` | Intimidad, realismo |
| Atmósfera | `light haze, visible light shafts, dust motes` | Volumen, cine |

Para que no se note la IA: **imperfección controlada** (haze, polvo, halación suave, grano fino) y **negros densos sin aplastar**.

## 6. Vertical 9:16

- Caras en el **tercio superior**; dejar libres la franja central (tipografía) y los márgenes superior e inferior (interfaz de la plataforma).
- La verticalidad favorece **cuerpos completos, contrapicados y movimientos verticales** (tilt, crane); los travellings laterales lucen menos.
- Para dos personajes, **escalonar en profundidad** (uno cerca y otro lejos) en lugar de ponerlos uno al lado del otro.
- Primeros planos más amplios que en 16:9: en vertical, un `close-up` cortado en la frente se siente claustrofóbico.

## 7. Ritmo y montaje

- Pensar los planos en **segundos enteros** desde el principio: los modelos generan duraciones enteras y el blockout se corta así.
- Un plano de diálogo o emoción necesita **2–4 s**; un plano de golpe, **0,5–1 s** (se recorta de uno más largo en post).
- Generar siempre **algo más largo** que el uso final (cabeza y cola) cuando el presupuesto lo permite: da margen para cortar en movimiento.
