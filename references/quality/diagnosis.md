# Diagnóstico: de un fallo a la corrección más barata

> Cargar cuando una generación no pasa la rúbrica (`qc-rubric.md`). Principio: **corregir el error donde nace** (blockout, referencia, prompt o parámetro) y elegir siempre el **escalón más barato** que lo arregla.

## Escalera de estrategias (de barato a caro)

1. **Arreglo en post sin regenerar:** recorte, reencuadre, corte antes del defecto, máscara, etalonaje local.
2. **Corrección dentro de Higgsfield sin rehacer la escena:** `lighting-hf`, `grade-hf`, `reframe`, `sync_so`, `video_extension` (ver `models/post-tools.md`).
3. **Corregir una referencia** (edición de imagen, ~1–3,5 cr) y hacer otro borrador.
4. **Corregir el prompt** (una frase concreta) y hacer otro borrador.
5. **Corregir el blockout** (0 cr) y hacer otro borrador.
6. **Cambiar de técnica:** dividir la sección, simplificar la acción, pasar de multiplano a planos únicos desde fotograma, o cambiar de modelo.

**Reglas:**
- Un solo cambio por intento, para saber qué lo arregló.
- Tras **2 intentos con el mismo fallo**, subir de escalón (en general, al 6). No volver a tirar los dados con el mismo prompt.
- `ip_detected`: reenviar una vez sin cambios (no se cobra).
- `nsfw`: replantear la escena sin lo que se rechazó. **Nunca** reformular para colarlo.
- Unos 6 intentos por pieza como máximo (`drama-ads`).
- **Nunca reenviar un trabajo pendiente** ni reintentar tras un timeout sin conocer el resultado del primero: puede cobrarse dos veces.

## Tabla de síntomas

| Síntoma (criterio) | Causa probable | Corrección | Escalón |
|---|---|---|---|
| Cara distinta entre planos (3) | Hoja de personaje ausente o débil; demasiadas referencias; plano muy largo | Enviar la hoja en cada clip; bloque `IDENTITY, CRITICAL`; ≤ 9 imágenes; clips de 10–15 s | 3–4 |
| Envejece o rejuvenece al personaje (3) | Palabras como `adult`, `mature`, `young man` | Edad en número (`a 27-year-old man`) | 4 |
| Cambia la ropa (3) | Vestuario descrito distinto en cada prompt | Vestuario fijo de la biblia, literal; flat-lay en la hoja | 3–4 |
| Piel de plástico, aspecto render (1) | Prompt sin vocabulario fotográfico; set de referencia «limpio» | Cámara real, piel con poros y sin retoque, grano fino; set «lived in» | 3–4 |
| Aparece la cápsula, rayas o gris del blockout (7) | Faltaba prohibir copiar la apariencia | Bloque «Never copy how it looks…» completo | 4 |
| El personaje toma el fondo gris de la hoja (7) | El set no estaba definido o faltaba su referencia | Añadir la referencia del set (primero en el orden) | 3 |
| Movimiento rígido, como un palo (5) | Copió la cápsula del blockout | «The capsules carry no body motion…» y describir el cuerpo | 4 |
| Manos deformes o dedos de más (5) | Trabajo fino de manos o contacto en un plano largo | Simplificar la acción; plano más abierto; cortar antes; insert aparte | 1 o 6 |
| Objetos que atraviesan o se funden (2) | Demasiados contactos o un cambio de estado en un plano | Máximo 2 contactos y 1 cambio de estado cada 30 s; dividir el plano | 6 |
| Gravedad o inercia rara (2) | Acción rápida o física compleja | Acción a velocidad humana; ritmo con cortes y speed-ramp en post | 4–6 |
| Corte en el sitio equivocado (6) | Los cortes de Seedance se desvían | Márgenes de 0,8 s; planos ≥ 1,5 s; duración igual al blockout | 1 (recortar) o 5 |
| Cámara que no hace el movimiento (6) | Movimiento sutil en el blockout o varios movimientos pedidos | Exagerar en el blockout; un movimiento por plano | 5 |
| Corta a otros ángulos sin pedirlo (6) | Plurales («shots», «cameras») en un plano único | Redactar en singular; con Omni, `single continuous shot` | 4 |
| La costura titila (4) | Fotograma fijado como `start_image` en una costura | Frame plate como referencia; extensión si es la misma toma | 6 |
| La luz cambia de lado entre planos (4) | Luz descrita por el lado del cuadro | Describir la fuente en el mundo; `light_custom` idéntico en Cinema Studio 4.0 | 4 o 2 (`lighting-hf`) |
| Color distinto entre clips (4) | Clips de modelos o semillas distintos | `grade-hf` o `/color-grade`; etalonaje común en post | 2 |
| Texto o logotipos inventados (descalificante) | Superficies con «letreros» o marcas en el prompt | `plain unbranded`; texto en post | 4 |
| Música no pedida (descalificante) | Faltaba la frase | `No music and no score.`; silenciar en post | 1 |
| Diálogo en otro idioma | Faltaba la frase de idioma | `Every spoken line is in <language>, exactly the words in quotes…` | 4 |
| Voz que cambia entre clips | Muestra de voz recortada de un clip generado | Muestra original de 3–10 s de la persona real, siempre la misma | 3 |
| Labios desincronizados | Diálogo demasiado cerca del final o línea larga | La última línea termina ≥ 4 s antes del final; `sync_so` como arreglo | 2–4 |
| Salió en horizontal o a otra resolución | Parámetro omitido | `aspect_ratio` y `resolution` siempre explícitos | 4 |
| No transmite lo que debía (8) | Plano sin intención clara o encuadre equivocado | Volver al plan: qué cuenta, qué hace sentir, desde dónde se mira | 5–6 |

## Cómo escribir la corrección

Anotar en `qc-report.md`:

```
Plano: S2-P3 · Fallo: criterio 5 (dedos de más al agarrar la taza) · Causa: trabajo fino de manos en un plano de 4 s
Corrección: dividir en PM sin taza (3 s) + insert de la taza de 2,8 s (Kling 4.0 i2v desde fotograma)
Escalón: 6 · Costo estimado: 7 cr · Aprobado por el usuario: ☐
```
