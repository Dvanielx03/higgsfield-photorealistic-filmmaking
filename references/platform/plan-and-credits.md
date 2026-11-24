# Plan contratado y créditos

> Cargar al empezar un proyecto y al hacer el presupuesto. Fuente: [higgsfield.ai/pricing.md](https://higgsfield.ai/pricing.md), actualizada el 24-11-2026, y el centro de ayuda de Higgsfield. Los planes cambian: comprobar la página antes de un proyecto grande.

## Plan del usuario: Plus

| Recurso | Plus (mensual) |
|---|---|
| Créditos | **1.200 al mes, que no pasan al mes siguiente** |
| Generaciones en paralelo | **6 videos y 8 imágenes** |
| Generaciones ilimitadas (solo en la web) | Nano Banana, Kling O1 Image, Seedream 4.5, Seedream 5.0 Lite, Flux.2 Pro (2K). Seedream 5.0 Pro y GPT Image 2.6 a 2K, solo durante 7 días. Nano Banana Pro, solo en el plan anual |
| Gratis | 3.000 generaciones de Soul V2 y Cinema, y 2 de Genjutsu |
| Video ilimitado | **Ninguno** (Seedance 2.5 ilimitado solo existe en el plan Scale) |
| Seedance 2.5 | Hasta 1080p (no está en Starter). El 4K de 2.5 «no está disponible en EE. UU.» según el changelog |
| Uso comercial | No depende del plan, según el centro de ayuda |
| Soul ID | Requiere plan de pago (Plus lo es) |

> [!IMPORTANT]
> **Lo «ilimitado» funciona solo en la interfaz web.** Lo que se genera por **MCP, CLI, Canvas o Supercomputer siempre gasta créditos**, aunque el plan lo tenga como ilimitado. Esta skill trabaja por MCP o CLI, así que **todo lo que genera cuesta créditos**.
> Consecuencia práctica: si el usuario quiere aprovechar las imágenes ilimitadas de Plus, puede generar las imágenes de referencia **él mismo en la web** con los prompts que prepara la skill y pasarle el archivo o el job id. Ofrecerlo cuando el presupuesto aprieta.

## Comprobar la cuenta

- `balance` devuelve los créditos y el `subscription_plan_type`. **Si no dice `plus` (o el plan esperado), la cuenta conectada no es la del plan contratado:** avisar antes de presupuestar o generar.
- `models_explore` trae un bloque `unlim`. Si `available: false`, no hay asignación ilimitada utilizable desde el conector.

## Cuánto video da Plus

Con las tarifas cotizadas el 24-11-2026 (Seedance 2.5 y Cinema Studio 4.0, 9:16):

| Uso de los 1.200 créditos | Segundos |
|---|---|
| Solo finales a 1080p (16 cr/s) | ≈ 75 s |
| Solo finales a 720p (7 cr/s) | ≈ 171 s |
| Solo borradores a 480p (3 cr/s) | ≈ 400 s |

**Proporción realista de producción:** en el caso documentado de Thomas Lundström salieron 47 s finales con 4 borradores y 3 finales. En las pruebas de MindStudio, la proporción fue de 3,2 s generados por cada segundo útil. **Presupuestar como mínimo 2–3 s generados por cada segundo final.**

Ejemplo para una pieza de 40 s con Seedance 2.5, con un borrador más una corrección por sección y el final a 720p:

```
40 × (3 × 2 + 7) × 1,15 ≈ 600 créditos  → cabe en un mes de Plus con margen para referencias
```

Con finales a 1080p (40 × (3 × 2 + 16) × 1,15 ≈ 1.010) se consume casi todo el mes: **finales a 720p y escalado selectivo** de los planos héroe (ver `models/post-tools.md`).

## Paralelismo

Con 6 videos en paralelo, las secciones que **comparten técnica ya validada** pueden lanzarse juntas con `generate_video_batch`, cada una cotizada. **El primer clip de cada modelo y modo siempre va solo.**
