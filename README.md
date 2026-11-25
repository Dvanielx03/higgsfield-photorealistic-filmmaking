<div align="center">

<img src="assets/banner.svg" alt="Higgsfield Photorealistic Filmmaking" width="100%">

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-D97757?style=flat-square&labelColor=0F1113)](https://docs.claude.com/en/docs/claude-code/skills)
[![Higgsfield](https://img.shields.io/badge/Higgsfield-exclusivo-D1FE17?style=flat-square&labelColor=0F1113)](https://higgsfield.ai)
[![Seedance 2.5](https://img.shields.io/badge/Seedance-2.5-F7F7F8?style=flat-square&labelColor=0F1113)](references/models/seedance-2-5.md)
[![QC](https://img.shields.io/badge/QC-8_criterios-383E46?style=flat-square&labelColor=0F1113)](references/quality/qc-rubric.md)
[![Verificado](https://img.shields.io/badge/verificado-24--nov--2026-1C1E21?style=flat-square&labelColor=0F1113)](references/platform/sources.md)

**Un director audiovisual especializado en Higgsfield para video fotorrealista con continuidad de cine.**<br>
Decide modelo y técnica plano a plano, cotiza antes de gastar, evalúa cada toma y corrige por el camino más barato.

[Qué hace](#qué-hace) · [Cómo dirige](#cómo-dirige) · [Instalación](#instalación) · [Uso](#uso) · [Arquitectura](#arquitectura) · [Modelos](#modelos) · [Calidad](#control-de-calidad) · [Fuentes](#fuentes)

</div>

---

## Qué hace

Generar video con IA suele parecer una tragamonedas: se regenera hasta que algo sale, la cara cambia entre planos y los créditos se van en pruebas. Esta skill convierte a Claude Code en el **director, director de fotografía y supervisor de continuidad** de una producción hecha **exclusivamente con Higgsfield**. Toma las decisiones creativas y técnicas con base verificable y deja la ejecución en el conector de Higgsfield y en sus [skills](https://github.com/higgsfield-ai/skills) y workflows oficiales.

| Problema | Cómo lo resuelve |
|---|---|
| La cara, la ropa o el set cambian entre tomas | Hojas de personaje como referencias, frame plates por set, descripciones fijas, máximo ~9 referencias por clip, empalmes con extensión o con plates (nunca con `start_image` en la costura) |
| Encuadre y timing al azar | Plan de planos con lente, movimiento e intención, y un blockout (Blender, 3D Jutsu o Genjutsu) como `video_references` |
| Referencias que el modelo usa cuando quiere | **Mapa temporal**: cada referencia atada a sus segundos, videos y audios recortados a su tramo, desglose con timecode de los videos de inspiración |
| Música donde no tocaba, o silencio donde había que oír algo | **Audio por tramo**: cada tramo declara música, efectos, ambiente, diálogo o silencio, y se verifica en el control de calidad |
| Prompts genéricos que «parecen IA» | Estructura oficial por modelo, vocabulario físico de cámara y luz, actuación con microgestos y redacción positiva |
| Elegir modelo por moda | Un router por tipo de plano: Seedance 2.5, Cinema Studio 4.0/3.5, Kling 4.0, Omni Flash e imagen |
| Créditos gastados en pruebas | Cotización obligatoria, borrador 480p finalizable, escalera de costos, presupuesto con reserva y libro de gasto |
| No saber si una toma sirve | Rúbrica de 8 criterios con umbrales por tipo de plano y un diagnóstico de síntoma → causa → corrección más barata |
| Arreglar obliga a regenerar | Correcciones dentro de Higgsfield: re-iluminar, re-etalonar, extender, escalar 1:1, lip-sync, reencuadrar |

> [!IMPORTANT]
> **Nunca genera sin un sí explícito** en el chat. Cotizar es gratis y siempre va primero. Solo usa la imagen de personas reales con su consentimiento. Por MCP o CLI, **todo gasta créditos**: lo «ilimitado» de los planes solo funciona en la web de Higgsfield.

## Cómo dirige

```mermaid
flowchart LR
    A[1 · Guion<br/>y formato] --> B[2 · Storyboard<br/>y dirección]
    B --> C[3 · Sets y<br/>referencias]
    C --> D[4 · Animatic<br/>en Blender]
    D --> G{Animatic<br/>aprobado}
    G --> F[Ficha + cotización]
    F --> Y{Sí del usuario}
    Y --> H[5 · Generación]
    H --> I{Rúbrica 8 criterios}
    I -->|falla| J[Diagnóstico:<br/>corrección más barata]
    J --> H
    I -->|pasa| L[6 · Post y control<br/>de calidad]

    classDef free fill:#1C1E21,stroke:#383E46,color:#F7F7F8
    classDef paid fill:#0F1113,stroke:#D1FE17,color:#D1FE17
    class A,B,C,D,G,F,Y,I,J free
    class H,L paid
```

<sub>Gris: 0 créditos · lima: consume créditos</sub>

### Dos rutas para sacar más videos de 1.000 créditos

```mermaid
flowchart LR
    M[Música] --> B[beats.py<br/>cortes a ritmo]
    B --> P[plan.json]
    P --> R[run_blockout.py<br/>Blender sin interfaz]
    R --> V[blockout.mp4]
    R --> K[keyframes]
    V --> S[Ruta S · Seedance 2.5<br/>planos héroe, caras, diálogo]
    K --> F[Keyframes fotorrealistas<br/>Cinema Studio Image]
    F --> KL[Ruta K · Kling 4.0<br/>planos sencillos, producto, B-roll]
    KL -->|falla la rúbrica| S

    classDef free fill:#1C1E21,stroke:#383E46,color:#F7F7F8
    classDef paid fill:#0F1113,stroke:#D1FE17,color:#D1FE17
    class M,B,P,R,V,K free
    class S,F,KL paid
```

| Pieza de 30 s (finales a 720p) | ≈ Créditos | Piezas por mes con 1.000 |
|---|---|---|
| Seedance 2.5 en todos los planos | 450 | 2 |
| **Híbrido 70 % Kling / 30 % Seedance** | **280** | **3** |
| Kling 4.0 en todos los planos | 200 | 5 |

Kling 4.0 **no** se usa con el blockout como video de referencia, porque no lo lee; se usa con keyframes. Así lo mostró la [prueba pública de Thomas Lundström](https://www.youtube.com/watch?v=ECxZEbUdSlE). Detalle en [`references/production/blender-kling-seedance.md`](references/production/blender-kling-seedance.md).

Cada una de las seis etapas tiene objetivos, requisitos, errores aprendidos en producción y una puerta de aprobación (`references/stages/`). El usuario aprueba en cuatro puntos: guion y formato, animatic, cada gasto de video y la pieza final. **Sin animatic aprobado no se genera video.**

## Instalación

| Requisito | Para qué |
|---|---|
| [Claude Code](https://docs.claude.com/en/docs/claude-code) | Ejecutar la skill |
| Conector MCP o CLI de [Higgsfield](https://higgsfield.ai) con un plan de pago | Cotizar, subir y generar |
| [Blender](https://www.blender.org/download/) 4.2+ (probado en 5.2) | Blockout automático sin interfaz (`run_blockout.py`); el [MCP oficial](https://www.blender.org/lab/mcp-server/) es opcional para retocar la escena |
| `ffmpeg`, `ffprobe`, Python 3 y numpy | Scripts de `scripts/` |

```bash
git clone https://github.com/Dvanielx03/higgsfield-photorealistic-filmmaking.git \
  ~/.claude/skills/higgsfield-photorealistic-filmmaking
```

Para desarrollarla en Windows sin duplicar archivos, clona donde quieras y enlaza:

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\higgsfield-photorealistic-filmmaking" -Target "<ruta-del-clon>"
```

## Uso

La skill se activa sola al pedir producir o mejorar un video con Higgsfield. Ejemplos:

```text
Tengo este guion de 40 s para Reels. Arma el plan de planos y dime qué modelo usarías en cada plano y cuánto costaría.
```
```text
Haz las hojas de personaje de los dos protagonistas con estas fotos (tienen su consentimiento) y la biblia de continuidad.
```
```text
Escribe la ficha de la sección S2 para Seedance 2.5 con el blockout y las hojas, y cotiza el borrador.
```
```text
Arma el blockout de este guion con la música que te paso, decide qué planos van por Kling y cuáles por Seedance, y dime cuántos créditos cuesta.
```
```text
Desglosa este reel de referencia con marcas de tiempo y dime qué tomamos de cada plano y qué audio lleva cada tramo.
```
```text
Evalúa este borrador con la rúbrica y dime la corrección más barata.
```
```text
Este plano está bien, pero la luz cambia respecto al anterior. ¿Cómo lo arreglo sin regenerar?
```

## Arquitectura

**Carga progresiva:** `SKILL.md` es un router corto con las reglas innegociables, el ciclo de dirección y un mapa de qué módulo cargar en cada momento. Claude solo lee el módulo de la etapa en curso y la ficha del modelo elegido.

```text
higgsfield-photorealistic-filmmaking/
├── SKILL.md                         Rol, innegociables, ciclo, mapa de módulos, valores por defecto
├── references/
│   ├── stages/                      Las 6 etapas: objetivo, requisitos, errores y puerta de cada una
│   │   ├── 01-creative-script.md    Guion, formato y destino
│   │   ├── 02-storyboard-direction.md  Planos, variedad, movimiento motivado, acciones secundarias
│   │   ├── 03-sets-references.md    Sets en capas, luz con fuente, activos
│   │   ├── 04-animatic-blender.md   Animatic completo y revisión obligatoria
│   │   ├── 05-ai-generation.md      Kling por plano, Seedance por sección, cotizar y pedir el sí
│   │   └── 06-post-qc.md            Montaje, color entre modelos, sonido, entrega
│   ├── platform/
│   │   ├── capabilities.md          Qué existe y qué no; herramientas del conector; workflows oficiales
│   │   ├── plan-and-credits.md      Plan Plus, créditos, ilimitados (solo web), cuánto video da
│   │   └── sources.md               De dónde sale cada regla y qué falta verificar
│   ├── direction/
│   │   ├── pipeline.md              Etapas, puertas de salida, atajos, carpetas del proyecto
│   │   ├── shot-design.md           Tamaños, lentes, movimiento motivado, luz, 9:16, ritmo
│   │   ├── identity-and-assets.md   Hojas, Elements, Soul ID, consentimiento, sets, props
│   │   ├── continuity.md            Empalmes, raccords, luz y color entre clips
│   │   ├── reference-timeline.md    Referencias atadas a sus segundos y audio por tramo
│   │   └── blockout.md              Blender, 3D Jutsu, Genjutsu, plugin de Blender
│   ├── models/
│   │   ├── router.md                Árbol de decisión y matriz de costos
│   │   ├── seedance-2-5.md          Esquema, guía oficial, reglas de clip, voz, edición
│   │   ├── cinema-studio.md         4.0 (light_custom), 3.5 (multi_prompt), 3.0, Image 2.5
│   │   ├── kling-omni-veo.md        Kling 4.0/3.0, Gemini Omni Flash 1.2, Veo 3.1
│   │   ├── image-models.md          GPT Image 2.6, Seedream, Nano Banana, Soul, Cinema Image
│   │   └── post-tools.md            Re-iluminar, re-etalonar, escalar, lip-sync, sonido
│   ├── prompting/
│   │   ├── principles.md            Reglas universales y vocabulario de fotorrealismo
│   │   └── templates.md             Plantillas A–I por caso y modelo
│   ├── quality/
│   │   ├── qc-rubric.md             8 criterios, umbrales y decisión
│   │   └── diagnosis.md             Síntoma → causa → corrección, escalera de estrategias
│   └── production/
│       ├── cost-protocol.md         Checklist previo, reglas de gasto, presupuesto
│       └── blender-kling-seedance.md  Flujo automatizado Blender → ruta K (Kling) / ruta S (Seedance)
├── templates/                       biblia · plan-de-planos · prompt-card · referencias · qc-report · presupuesto
├── scripts/
│   ├── frames.sh                    first · last · at · sheet · compare · info
│   ├── timeline.py                  cuts · breakdown · trim · drift
│   ├── beats.py                     música → tempo y cortes a ritmo
│   ├── run_blockout.py              plan.json → blockout de Blender → fichas K y S (un comando)
│   ├── prompt_skeleton.py           timeline.json → prompt de Kling o de Seedance con tiempos
│   └── blockout/
│       ├── build_blockout.py        constructor de Blender sin interfaz
│       └── plan.example.json        formato del plan
└── assets/banner.svg
```

## Modelos

| Plano | Modelo | Por qué |
|---|---|---|
| Sección multiplano con personas y blockout | **Seedance 2.5** `omni_reference` | Video, imagen y audio de referencia; borrador finalizable; edición y extensión |
| Luz idéntica fijada por parámetro | **Cinema Studio 4.0** + `light_custom` | Único control de luz verificado por parámetro |
| Un prompt por plano con duraciones | **Cinema Studio 3.5** `multi_prompt` | Multiplano explícito (con `prompt_language: "en"`) |
| Plano único desde un fotograma aprobado | **Kling 4.0** i2v | Unas 3 veces más barato a 720p |
| Ambiente sin personas | **Gemini Omni Flash 1.2** | Barato, audio nativo |
| Hojas y fotogramas | **GPT Image 2.6** · Seedream 5.5 · Nano Banana Pro · Soul 2.0 | Según el método oficial `character-sheet` |

> [!WARNING]
> Catálogo, parámetros y precios cambian cada semana. La skill obliga a re-consultar el esquema (`models_explore`) y a re-cotizar antes de cada producción; las cifras del repositorio son una foto con fecha. Los **conflictos entre fuentes** (por ejemplo, la sintaxis `@Image1` frente a `@Image 1`, o las fotos que pide Soul ID) están marcados en cada módulo con la opción que se toma.

## Control de calidad

| # | Criterio | # | Criterio |
|---|---|---|---|
| 1 | Fotorrealismo | 5 | Naturalidad de movimientos |
| 2 | Coherencia física | 6 | Calidad cinematográfica |
| 3 | Consistencia de personajes | 7 | Fidelidad a las referencias |
| 4 | Continuidad narrativa y visual | 8 | Intención creativa |

Cada criterio vale de 0 a 2. Se aprueba con 14/16 o más y ningún 0. Un 0 en identidad, física o fidelidad descarta la toma y obliga a diagnosticar. Si el mismo fallo aparece dos veces, se cambia de estrategia en vez de volver a tirar los dados.

<details>
<summary><strong>Escalera de correcciones (de barata a cara)</strong></summary>

<br>

1. Arreglo en post sin regenerar.
2. Corrección dentro de Higgsfield (`lighting-hf`, `grade-hf`, `reframe`, `sync_so`, `video_extension`).
3. Corregir una referencia y repetir el borrador.
4. Corregir una frase del prompt y repetir el borrador.
5. Corregir el blockout y repetir el borrador.
6. Cambiar de técnica: dividir, simplificar o cambiar de modelo.

</details>

## Fuentes

- **Conector de Higgsfield:** esquemas, cotizaciones y workflows oficiales (`drama-ads`, `character-sheet`, `angles-hf`, `lighting-hf`, `grade-hf`, `higgsfield-enhance-video`, `video-sound-design`, `video-montage`).
- **Documentación de Higgsfield:** centro de ayuda, [guía de prompting de Seedance 2.5](https://higgsfield.ai/blog/seedance-2-5-prompting-guide), [guía de Cinema Studio 4.0](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide), [planes](https://higgsfield.ai/pricing.md) y [skills oficiales](https://github.com/higgsfield-ai/skills).
- **Guías de los fabricantes:** Kling, Gemini Omni, Veo, Nano Banana y GPT Image.
- **Práctica:** Thomas Lundström, [*Claude + Blender Is The Best Way To Make AI Commercials*](https://www.youtube.com/watch?v=jc0Qh09Qrlo).

Lista completa, con lo que aporta cada fuente y lo pendiente de verificar, en [`references/platform/sources.md`](references/platform/sources.md).

---

<sub>Proyecto independiente, sin afiliación con Higgsfield AI. Higgsfield y su logotipo son marcas de sus respectivos titulares y se usan solo para indicar compatibilidad.</sub>
