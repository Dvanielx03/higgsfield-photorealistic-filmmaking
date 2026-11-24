# Plan contratado y créditos

> Cargar al empezar un proyecto y al hacer el presupuesto. Fuentes: lo que dice el usuario sobre su contrato (manda sobre todo lo demás), [higgsfield.ai/pricing.md](https://higgsfield.ai/pricing.md) (24-11-2026) y el centro de ayuda de Higgsfield.

## Plan del usuario: Plus de 1.000 créditos al mes

| Recurso | Valor |
|---|---|
| **Créditos** | **1.000 al mes** (dato del usuario). No pasan al mes siguiente |
| Generaciones en paralelo | 6 videos y 8 imágenes según la página actual. Puede variar en contratos anteriores: confirmar si un lote falla por concurrencia |
| Generaciones ilimitadas (solo en la web) | Según la página actual: Nano Banana, Kling O1 Image, Seedream 4.5, Seedream 5.0 Lite, Flux.2 Pro (2K); Seedream 5.0 Pro y GPT Image 2.6 a 2K durante 7 días; Nano Banana Pro solo en el plan anual |
| Video ilimitado | **Ninguno** (Seedance 2.5 ilimitado solo existe en el plan Scale) |
| Seedance 2.5 | Hasta 1080p (no está en Starter). El 4K de 2.5 «no está disponible en EE. UU.» según el changelog |
| Uso comercial | No depende del plan, según el centro de ayuda |
| Soul ID | Requiere plan de pago (Plus lo es) |

> [!NOTE]
> **La página de precios actual muestra Plus con 1.200 créditos**, pero el plan del usuario es de **1.000**. Probablemente es un contrato anterior o con otra modalidad; otras fuentes de Higgsfield también citaban 1.000. **El presupuesto se hace siempre con la cifra del usuario** y el saldo real de `balance`, nunca con la de la página.

> [!IMPORTANT]
> **Lo «ilimitado» funciona solo en la interfaz web.** Lo que se genera por **MCP, CLI, Canvas o Supercomputer siempre gasta créditos**, aunque el plan lo tenga como ilimitado. Esta skill trabaja por MCP o CLI, así que **todo lo que genera cuesta créditos**.
> Consecuencia práctica: si el usuario quiere aprovechar las imágenes ilimitadas, puede generar las imágenes de referencia **él mismo en la web** con los prompts que prepara la skill y pasarle el archivo o el job id. Ofrecerlo siempre que el presupuesto apriete.

## Comprobar la cuenta

- `balance` devuelve los créditos disponibles y el `subscription_plan_type`. **Si no dice `plus`, la cuenta conectada no es la del plan contratado:** avisar antes de presupuestar o generar.
- **Presupuestar contra el saldo real**, no contra los 1.000 del mes: si ya se gastó parte, el techo es lo que queda.
- `models_explore` trae un bloque `unlim`. Si `available: false`, no hay asignación ilimitada utilizable desde el conector.

## Cuánto video dan 1.000 créditos

Tarifas cotizadas el 24-11-2026 (Seedance 2.5 y Cinema Studio 4.0, 9:16):

| Uso de los 1.000 créditos | Segundos |
|---|---|
| Solo finales a 1080p (16 cr/s) | ≈ 62 s |
| Solo finales a 720p (7 cr/s) | ≈ 142 s |
| Solo borradores a 480p (3 cr/s) | ≈ 333 s |

**Proporción realista de producción:** en el caso documentado de Thomas Lundström salieron 47 s finales con 4 borradores y 3 finales. En las pruebas de MindStudio, la proporción fue de 3,2 s generados por cada segundo útil. **Presupuestar como mínimo 2–3 s generados por cada segundo final.**

### Techo práctico por pieza

Fórmula de `production/cost-protocol.md`: `s × (3 × 2 + tarifa_final) × 1,15`, con un borrador más una corrección por sección y un 15 % de reserva. Sin contar imágenes:

| Duración de la pieza | Final a 720p | Final a 1080p |
|---|---|---|
| 20 s | ≈ 300 cr | ≈ 505 cr |
| 30 s | ≈ 450 cr | ≈ 760 cr |
| 40 s | ≈ 600 cr | ≈ 1.010 cr (**no cabe en un mes**) |
| 60 s | ≈ 895 cr (casi todo el mes) | ≈ 1.520 cr (no cabe) |

**Reglas que salen de esta tabla:**
- **Finales a 720p por defecto.** El 1080p se reserva para los planos héroe, o se llega a él con escalado selectivo (`models/post-tools.md`), que cuesta menos que generar a 1080p.
- Con 1.000 créditos, una pieza de **más de ~40 s** exige recortar: menos correcciones, más planos fijos en imagen con parallax, o repartir la producción en dos meses.
- **Las imágenes de referencia** (~0,75–3,5 cr cada una) suman unas decenas de créditos por proyecto. Si se generan en la web, donde son ilimitadas, cuestan 0.
- Si el presupuesto supera el saldo, **se dice antes de empezar**, con dos o tres opciones para que quepa.

## Paralelismo

Las secciones que **comparten técnica ya validada** pueden lanzarse juntas con `generate_video_batch`, cada una cotizada. **El primer clip de cada modelo y modo siempre va solo.**
