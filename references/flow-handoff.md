# Trabajar con Google Flow en paralelo

> Datos de Flow revisados el 24-nov-2026 (fuentes en `sources.md`). Flow cambia rápido: comprobar en flow.google.com antes de producir.

## Lo que hay que saber de Flow hoy
- **Modelo recomendado:** Gemini Omni Flash 1.2. **Veo 3.1 Fast/Quality y Omni Flash 1.1 se retiran el 5-dic-2026**; no empezar un proyecto con ellos. Veo 3.1 Lite sigue disponible.
- **Omni Flash 1.2:**
  - 3–15 s con suscripción. Genera a 360p o 720p y escala a 1080p (4K solo con Ultra).
  - 16:9 y 9:16, audio nativo.
  - Corta entre planos por defecto: pedir «single continuous shot» cuando se quiere un plano único.
- **Funciones útiles:**
  - Frames to Video (inicio, fin o ambos).
  - Ingredients (referencias con @; en la API: hasta 6 imágenes, 3 por personaje y 2 personajes).
  - Extend (solo Omni 1.2 con suscripción).
  - Save frame (guardar un fotograma para usarlo como ingrediente o como inicio).
  - Scenebuilder (ordenar y recortar).
- **Imágenes en Flow** (Nano Banana Pro, Nano Banana 2.1): **no consumen créditos**, con límite diario según el plan.
- **Créditos de video** (ver la página oficial, pueden cambiar):
  - Omni 1.2 a 720p: 3 cr/s hasta 10 s.
  - Omni 1.2 a 360p: 1 cr/s.
  - Escalado a 1080p: gratis hasta 10 s.
  - Planes: AI Plus 200 cr/mes · AI Pro 1.000 · Ultra 10.000 o 25.000.
- **Personas reales:**
  - El avatar `@me` solo puede ser de uno mismo.
  - La API de Omni no acepta material con personas reconocibles.
  - Generar la imagen de alguien sin su consentimiento puede violar la política de Google.
  - La ayuda de Flow no detalla qué pasa al subir fotos de terceros.

## Reparto de trabajo por defecto

| Va en **Flow** | Va en **Higgsfield** |
|---|---|
| Fotogramas clave y referencias de sets (imágenes gratis) | Todo plano donde se ve la cara de los protagonistas |
| Sets vacíos, ambientes, insertos sin caras | Secciones multiplano con blockout (Seedance 2.5 acepta video de referencia) |
| Planos que el usuario de Flow pueda resolver con Omni 1.2 sin caras reales | Diálogo a cámara y lip-sync |

**Por qué:**
- Las caras reales en Higgsfield evitan el riesgo de política de Google y concentran la identidad en una sola herramienta.
- Flow aporta imágenes gratis y video barato sin caras.

## Cómo mantener el mismo look
1. **Las mismas referencias en las dos herramientas.** Se generan una vez (en Flow, gratis) y se suben a Higgsfield con el mismo nombre.
2. **El mismo bloque de luz, color y cámara** de la biblia en los dos prompts, traducido a la estructura de cada herramienta (ver `prompt-templates.md` A y F).
3. **El mismo modelo cuando dos planos se cortan entre sí:** `gemini_omni_flash_1_2` existe en Higgsfield, así que un plano de Flow y uno de Higgsfield pueden salir del mismo motor.
4. **Relevo de fotograma:** en Flow, «Save frame» del último fotograma (o `frames.sh last` sobre el archivo descargado) → `start_image` en Higgsfield, y viceversa.
5. **Entrega técnica de Flow:** descargar a la máxima resolución disponible, sin recomprimir, y nombrar `S<sección>-P<plano>_flow_v<n>.mp4`.
6. **Post común:** conformar todo a 24 fps; igualar color a un plano maestro por set (DaVinci Resolve Shot Match o a mano) con un LUT común; el mismo grano por encima de todo.

## Protocolo entre las dos personas
- La biblia y el plan de planos son **un solo archivo compartido**; nadie cambia un bloque de la biblia sin avisar.
- Cada uno lleva su libro de gasto (créditos de Flow y créditos de Higgsfield por separado).
- Cada plano entregado pasa la misma rúbrica de control de calidad (`qc-cost-protocol.md`).
