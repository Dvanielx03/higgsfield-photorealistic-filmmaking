# Blockout en Blender

> Cargar en la etapa 3 del pipeline, cuando una sección tiene movimiento de cámara, varios planos o varios personajes. Método de Thomas Lundström (ver `platform/sources.md`), adaptado a Higgsfield.

## Por qué existe

Es el paso que más créditos ahorra. Se ve el video completo, con cámaras, lentes y timing reales, **antes** de gastar un crédito. Las notas se dan por fotograma («algo falla entre los fotogramas 685 y 697») y un detalle se puede cambiar sin tocar el resto. Después, el video gris se pasa a Seedance 2.5 o a Cinema Studio 4.0 como `video_references`, para que el modelo copie la cámara y el timing pero no la apariencia.

## Cuándo usarlo y cuándo no

| Usar blockout | Basta un fotograma clave |
|---|---|
| Sección multiplano con cortes definidos | Plano fijo y aislado |
| Movimiento de cámara complejo (grúa, seguimiento, órbita) | Ficha o retrato casi inmóvil |
| Varios personajes que se cruzan o interactúan | Inserto de un objeto |
| Timing exacto que debe casar con música o tipografía | Plano que solo necesita parallax en post |

## Procedimiento (con el MCP oficial de Blender)

1. **Comprobar la conexión** con el MCP de Blender antes de prometer nada. Si no hay conexión, ofrecer el plan B: fotogramas clave aprobados como `start_image`.
2. **Una ronda de preguntas, con valores por defecto**, antes de construir: estilo, estructura (un plano o varios cortes), duración, formato, sensación de cámara, lentes, profundidad de campo y lugar. Saltarse esta ronda fue el error número uno del autor del método.
3. **Configurar la escena:** resolución real (1080×1920 para 9:16), **24 fps**, cámara con la lente en mm del plan de planos.
4. **Representar sin detalle:**
   - **personas** = cápsulas con rayas de un color distinto por personaje;
   - **props** = cajas de colores sólidos;
   - **sets** = volúmenes grises.
   La clave de colores se anota en la biblia y se copia al bloque `Blockout key` del prompt.
5. **Revisión plano a plano** desde el principio. No renderizar hasta que el usuario apruebe; abrir la escena en Blender para reproducir con la barra espaciadora.
6. **Partir en secciones** de **segundos enteros** que coincidan con duraciones aceptadas por el modelo (Seedance 2.5 y Cinema Studio 4.0: 4–30 s). Una sección por cambio de set, de luz o de técnica.
7. **Render gris** de cada sección con la duración exacta, y **placas grises** de cada set desde la cámara de su plano (son la base de las referencias de set).

## Alternativas dentro de Higgsfield

| Vía | Qué hace | Cuándo |
|---|---|---|
| **MCP oficial de Blender** (este procedimiento) | Claude construye la escena en el Blender del usuario | Control total del plano y de los tiempos |
| **[Plugin de Higgsfield para Blender](https://higgsfield.ai/blog/higgsfield-blender-plugin)** (Blender 5.1+) | Scene Builder y pestaña Video que genera con Seedance 2.5 desde Blender | Si el usuario prefiere generar desde Blender |
| **[3D Jutsu](https://higgsfield.ai/blog/higgsfield-3d-jutsu)** (`/3d-jutsu`) | Un agente monta la previsualización en gris y la exporta en MP4 como referencia de cámara | Sin Blender instalado, o para nuevos ángulos de un set |
| **Genjutsu Motion Transfer** (`hf_mult_motion_control`) | Copia el movimiento, la cámara y el timing de un video real y reconstruye la escena con las referencias | Para movimiento humano natural, el usuario se graba con el móvil haciendo la acción. **El catálogo no lista 9:16 para este modelo**: comprobar con `models_explore` |

## Cómo se usa en Higgsfield

- El video del blockout se sube (`media_upload` → `media_confirm`) y va en `medias` con el rol `video_references`. Es `@vid1` en el prompt de la sección.
- La duración de la generación = duración del blockout.
- El prompt incluye siempre el bloque «CRITICAL: @vid1 is a coarse grey blockout…» y la clave de colores (plantilla en `prompting/templates.md`).
- Según la guía de Seedance: declarar que el blockout es **grueso** (solo movimiento y composición) y **no repetir con palabras el movimiento** que ya da el video.

## Fallos típicos y su origen

| Lo que sale mal en el borrador | Origen | Arreglo |
|---|---|---|
| El personaje se mueve rígido, como un palo | El modelo copió la cápsula | Decir que la cápsula es solo marcador de posición, tamaño, dirección y velocidad, y describir el cuerpo |
| Un objeto sale con forma rara (rombo, bloque) | La forma del blockout era ambigua | Cambiar la forma en Blender o nombrarla en la clave; no solo en el prompt |
| Aparecen rayas, cápsulas o gris en el resultado | El prompt no prohibía copiar la apariencia | Bloque «Never copy how it looks…» completo |
| La cámara no hace el movimiento | Movimiento demasiado sutil en el blockout | Exagerar un poco el movimiento en Blender |
| Los cortes caen en otro sitio | Duración distinta o planos sin número | Duración idéntica y «There are exactly N shots… each cutting where @vid1 cuts» |
