# Biblia de continuidad · <proyecto>

> Bloques en inglés = texto que se pega literal en los prompts.

## Técnica
- Formato: 9:16 · 1080×1920 · 24 fps
- Cámara: <ARRI Alexa 35> · lente base <35mm> · excepciones: <24mm espacio / 85mm aislar>
- Grano: <fine 35mm film grain> · obturador 180°
- Zonas seguras 9:16: caras en el tercio superior; centro libre para tipografía; <x> px arriba y abajo para interfaz

## Grade y paleta
```
Color: <e.g. dense and matte, soft lifted blacks, creamy highlight roll-off, deep teal shadows, warm amber practicals>.
```

## Personajes
### <ID-PERSONA> · @<ref-nombre>
- Consentimiento: ☐ confirmado por el usuario (fecha)
- Fotos fuente: `referencias/<persona>/`
- Hoja aprobada: `referencias/<persona>_sheet_v<n>.png`
```
<PERSON>: a <number>-year-old <man/woman>, <build>, <hair>, <distinctive mark repeated in every shot>. Wears <wardrobe per scene: concrete matte materials, plain and unbranded>.
(Con fotos reales adjuntas, no describir los rasgos de la cara: los aporta la hoja.)
```
- Vestuario por escena: <escena → vestuario>
- Clave en el blockout: <cápsula de rayas rojas y negras>

## Sets
### <ID-SET> · @<ref-nombre>
- Estados: <estado-1 (ref) → estado-2 (edición de la ref)>
- Props fijos y posición: <…>
```
Lighting: <motivated source described in the world, e.g. the window behind the desk>, <hard/soft>, <K>, <haze/dust>.
Scene: <fixed description>.
```

- Frame plate (set vacío desde el primer clip rodado): `activos/<set>_plate_v<n>.png`
- Light rig (si se usa Cinema Studio 4.0): `light_custom` = <json idéntico para todos los planos del set>

## Estado por clip (stateIn → stateOut)
| Clip | Entra | Sale |
|---|---|---|
| S1 | <A de pie junto a la puerta; taza sobre la mesa> | <A sentado; taza en su mano derecha> |

## Registro de activos (ids de Higgsfield)
| id | Tipo | Archivo | job id / media id / element id | Aprobado | Vía (refs · Element · Soul) |
|---|---|---|---|---|---|

## Props
| id | Qué es | Dónde está | Clave en el blockout |
|---|---|---|---|

## Ejes y dirección en pantalla
| Escena | Lado de cámara | A mira hacia | B mira hacia |
|---|---|---|---|
