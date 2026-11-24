# Reglas de continuidad

## Personajes: cara, cuerpo y vestuario
1. **Una hoja de personaje por persona**, aprobada antes de cualquier video. Es la única referencia de identidad que se etiqueta en los prompts.
2. **Descripción fija en inglés** en la biblia (edad aproximada, rasgos, pelo, complexión, marcas distintivas, vestuario). Se pega **idéntica** en cada prompt; no se parafrasea.
3. **Vestuario por escena** en la biblia; si cambia, se hace una hoja nueva («same person, new wardrobe»). Ropa lisa y sin marcas.
4. **Imperfecciones concretas** (lunares, asimetrías) ayudan a fijar la identidad y a que no parezca «cara de modelo IA».
5. **Pocos personajes por plano.** Cada persona más en el plano aumenta el riesgo de deriva. Con dos protagonistas juntos, plano más abierto o un protagonista de espaldas.
6. Revisar la identidad **en el primer borrador de cada sección**, antes de seguir con las demás.

## Sets, objetos y luz
1. **Un set = una referencia por estado.** Los estados nuevos (de noche, encendido, destrozado) se derivan editando la misma imagen, nunca generando otra desde cero.
2. **Inventario de props** por set en la biblia, con su posición. En el prompt: «exactly one <object>».
3. **Luz por set:** fuente motivada, dirección (izquierda o derecha del cuadro), dureza, temperatura en K, atmósfera (haze o polvo). Se copia literal.
4. **Grade único** por proyecto (descripción en palabras más un LUT en post). Todos los prompts llevan el mismo bloque de color.

## Cámara y lenguaje
1. **Lente base** del proyecto (por ejemplo 35 mm) y lentes de excepción justificadas (24 mm para espacio, 85 mm para aislar).
2. **Eje de 180°:** en diálogos o cruces de miradas, anotar en el plan de qué lado está la cámara. Mantener la **dirección en pantalla**: si alguien sale por la derecha, entra por la izquierda en el plano siguiente.
3. **Raccord de mirada:** anotar hacia dónde mira cada personaje al final de un plano y al inicio del siguiente.
4. **Movimientos motivados:** cada movimiento de cámara responde a una acción o a una emoción. Nada de órbitas gratuitas.
5. **9:16:** caras en el tercio superior, zona central libre para la tipografía, márgenes seguros arriba y abajo para la interfaz de la plataforma.

## Movimiento, expresión y física
- En el prompt: verbos concretos, una acción por plano, microgestos (respiración, parpadeo, pausa antes de reaccionar).
- Física: peso, inercia, sombras de contacto, tela y pelo que reaccionan.
- Velocidad: los modelos fallan más con la acción rápida y la física compleja. Preferir acciones a velocidad humana normal y usar cortes o speed-ramp en post para el «golpe».

## Relevo entre tomas (último fotograma → primero)
Cuando la acción continúa de un plano al siguiente:
1. Generar y aprobar la toma A.
2. Extraer su último fotograma real: `bash scripts/frames.sh last tomaA.mp4 tomaA_last.png`. No sirve el último fotograma de la previsualización.
3. Revisar ese fotograma: si sale borroso por motion blur, retroceder 2–5 fotogramas (`frames.sh at`).
4. Usarlo como `start_image` de la toma B. No fijar `end_image` en B salvo que haga falta llegar a algo exacto.
5. Igualar dirección y velocidad del movimiento en el prompt de B («continues the same slow push-in»).
6. **Mismo modelo en toda la cadena.** Cambiar de modelo a mitad cambia textura y color.

Cuando **no** hay continuidad de acción (corte de plano normal), no se encadena: se usan las mismas referencias y el blockout. Encadenar todo acumula degradación.

## Coherencia entre Higgsfield y Google Flow
Ver `flow-handoff.md`. Resumen:
- Mismas referencias (las mismas imágenes de partida en ambas herramientas).
- Mismo modelo cuando dos planos se cortan entre sí: Omni Flash 1.2 está en los dos.
- Todo a 24 fps y etalonaje común en post.
