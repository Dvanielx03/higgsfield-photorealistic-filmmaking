# Flujo de producción, etapa por etapa

Principio rector (Thomas Lundström, ver `sources.md`): **toma las decisiones creativas antes de generar el video.** Cada etapa existe porque reduce regeneraciones. Si una etapa no reduce riesgo ni gasto en un proyecto concreto, se salta y se dice por qué.

---

## 1. Guion → plan de planos

**Entrada:** guion aprobado.
**Salida:** `plan-de-planos.md` (plantilla en `templates/`).

Por cada plano:
- id (`S1-P3`), sección de generación a la que pertenece, duración en **segundos enteros**;
- tamaño (PG, PM, PP, PD, cenital, POV), ángulo, **lente en mm**, apertura, movimiento de cámara;
- quién y qué aparece (ids de la biblia), acción en una frase, mirada y dirección en pantalla;
- sonido del plano; texto o gráficos que se añaden en post (nunca se piden al modelo);
- herramienta (Higgsfield / Flow / post) y técnica (sección multiplano, i2v desde fotograma, imagen + parallax, efecto de post).

**Regla de agrupación en secciones:** una sección es un trozo continuo del montaje que se genera de una vez (multiplano), con un mismo set y luz. Duración de sección = duración que el modelo acepta (Seedance 2.5: 4–30 s) y en segundos enteros. Cortar secciones donde cambia el set, la luz o la herramienta.

**Clasificar cada efecto antes de pedirlo a la IA:**
| Tipo | Ejemplos | Dónde se hace |
|---|---|---|
| Físico y fotografiable | puerta que se abre, contraluz, mano que tapa el lente | generación |
| Gráfico o tipográfico | textos, pensamientos, contadores, nombres | post (motion-studio) |
| Tratamiento de imagen | contorno brillante, B/N, glitch, grano | post (filtro) |
| Composición de varias tomas | clones, muro de fotogramas | imágenes + post, o una sola generación desde un fotograma compuesto |

Los modelos de video deforman el texto: **ningún texto legible se pide en un prompt de video.**

**Criterio de salida:** la suma de duraciones cuadra con el guion y cada plano tiene herramienta asignada.

## 2. Biblia de continuidad

**Salida:** `biblia.md` (plantilla en `templates/`). Contiene la descripción fija de cada personaje (texto en inglés, listo para pegar), vestuario por escena, sets con su estado, props, luz por set (dirección, calidad, temperatura), paleta y grade, lente base, fps (24), formato (9:16) y zonas seguras.

**Criterio de salida:** cualquier prompt del proyecto se puede escribir copiando bloques de la biblia sin inventar nada.

## 3. Blockout en Blender

**Por qué:** es el paso que más créditos ahorra. Se ve el video completo con cámaras, lentes y timing antes de gastar, y las notas se dan por fotograma (Thomas: «algo falla entre los fotogramas 685 y 697»).

**Cómo:** con las herramientas MCP de Blender (verificar conexión primero).
- Personas = cápsulas con rayas de color distinto por personaje; props = cajas de color. Anotar la clave de colores en la biblia; luego va en el prompt.
- Cámara con la lente real en mm y el formato real (1080×1920 para 9:16) a 24 fps.
- Hacer preguntas de estilo, cámara, lentes, profundidad de campo y lugar **antes** de construir (el error número uno del autor fue saltárselo).
- Revisión plano a plano. No renderizar hasta que el usuario apruebe; luego render gris por sección con la duración exacta en segundos enteros.
- Exportar también **placas grises** de cada set desde la cámara del plano: son la base de las referencias de set.

**Cuándo saltarlo:** un plano fijo y aislado (una ficha, un inserto) → basta con un fotograma clave aprobado.

## 4. Referencias

Todas con nombre estable, guardadas en una carpeta del proyecto y subidas a Higgsfield (`media_upload`). El nombre es la etiqueta en el prompt.

- **Personajes:** hoja de personaje fotorrealista (frente, perfil, espalda, retrato cerrado, detalles de vestuario) a partir de 3–5 fotos reales del usuario y con consentimiento. Fondo gris neutro y luz pareja. Modelos sugeridos: `seedream_v5_pro` (caras, hojas, hasta 10 refs) o `gpt_image_2_6` (hasta 16 refs, el más barato cotizado). Opcional: Soul ID para fotogramas fijos muy fieles.
- **Sets:** placa gris del blockout → imagen fotorrealista con «keep the layout exactly…» y **pedir que se sienta habitado** (si no, sale vacío y estéril). Un estado por imagen; los estados siguientes se derivan editando esa imagen.
- **Props** que importan en la historia: hoja de producto.
- **Calidad mínima:** sin texto legible, sin logos, sin geometría del blockout, misma dirección de luz que la biblia.

## 5. Revisión

Mostrar blockout + referencias al equipo (o al cliente) **antes** de gastar en video. Cambios aquí cuestan cero.

## 6–8. Borrador → corrección → final

- Un prompt por sección con la plantilla de `prompt-templates.md`. Duración = duración exacta del blockout de esa sección.
- **Borrador** en 480p (Seedance 2.5 `draft: true`), con el mismo prompt y las mismas referencias que irán al final.
- Revisar con `scripts/frames.sh sheet` y la rúbrica de `qc-cost-protocol.md`. Localizar el error: ¿en el prompt, en una referencia o en el blockout? Se corrige en su origen.
- **Final:** finalizar el borrador aprobado (`draft_job_id`) o regenerar en la resolución final. Resolución final según presupuesto: 720p + escalado si hace falta, 1080p para los planos héroe.

## 9. Post

- **Audio:** silenciar el audio generado o separar sus pistas y quedarse con lo útil (Ultimate Vocal Remover). Música y efectos propios. La voz de los protagonistas, grabada por ellos.
- **Imagen:** conformar todo a 24 fps; etalonaje común (igualar al plano general de cada set; DaVinci Resolve Shot Match); grano fino para unir fuentes.
- **Gráficos:** skill de motion graphics con las marcas de tiempo del montaje final.
- **Máscaras** (texto detrás del sujeto): recorte local si está disponible; si no, `sam_3_video` cotizado.
