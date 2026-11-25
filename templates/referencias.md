# Referencias con marcas de tiempo · <proyecto>

> Método en `references/direction/reference-timeline.md`. Toda referencia se ata a sus segundos, y todo tramo dice qué audio quiere.

## A. Referencias de inspiración

Desglose automático: `python -I scripts/timeline.py breakdown <video> referencias/<nombre>/`

### <REF-01> · <nombre o enlace>
- Duración: <s> · formato: <9:16> · desglose: `referencias/<nombre>/desglose.md`
- Qué se toma de esta referencia, con su timecode:

| Timecode | Recurso que copiamos | Audio en ese tramo (música · efectos · ambiente · diálogo · silencio) | Plano nuestro donde se usa |
|---|---|---|---|
| 00:02.5–00:04.5 | La mano tapa el lente como transición | efecto: roce + golpe grave | S2-P4 |

## B. Referencias de producción (lo que se envía al modelo)

| Tag | Tipo | Archivo / job id / media id | Tramo de origen (in–out) | Qué define | Clips donde va |
|---|---|---|---|---|---|
| `@Image1` | plate | `activos/sala_plate_v1.png` | — | set vacío y altura de cámara | S2, S6 |
| `@vid1` | blockout | `blockout/S2.mp4` | 0–8 s (sección completa) | cámara y timing | S2 |
| `@Audio1` | voz | `voz/andres.wav` | 12,4–16,5 s de la grabación original | voz de Andrés | S4, S7c |

## C. Audio por tramo de la pieza

| Tramo de la pieza | Música | Efectos | Ambiente | Diálogo | Silencio | Dónde se hace |
|---|---|---|---|---|---|---|
| 0:00–0:05 | — | reloj | fluorescente | — | — | modelo |
| 0:05–0:13 | post (beat entra a 0:05) | golpe de puerta | — | VO en post | — | modelo + post |
