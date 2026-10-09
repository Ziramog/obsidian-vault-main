---
id: HO-2026-10-08-001
status: ready
from: brain-local
to: brain-vps
project: hermes-system
priority: normal
depends-on: []
created-at: 2026-10-08T22:02:00-03:00
acknowledge-by: next-vps-session
due-at: 2026-10-10T18:00:00-03:00
escalate-after: 48h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — registrar ingreso de Víctor (Abrile) por publicidad

## Motivo

Juan reportó en el group chat "Brain Local" (2026-10-08):

> "ingresaron 100 USD de victor por publicidad"

`kpis.md` y `Briefings/` están fuera de mi zona de escritura (owner: Juan).
Yo no mantengo números. Este handoff transfiere el dato para registro.

## Dato a registrar

| Concepto | Monto USD | Fecha | Fuente |
|---|---|---|---|
| Víctor Abrile — publicidad | 100 | 2026-10-08 (reportado) | Juan, group chat "Brain Local" |

Contexto previo (briefing v2, sep-2026): el mismo cliente aparece como
"Víctor Abrile | 266 | ✅ Cobrado (verificar si salda recibo ARS 178.860)".
Los 100 USD de hoy son un ítem **nuevo de octubre**, no parte de los 266 de septiembre.

## Ambigüedad NO resuelta (requiere decisión de Juan)

"por publicidad" admite dos lecturas que cambian el asiento:

1. **Ingreso cobrado** — Víctor pagó 100 USD por un servicio de publicidad
   (ej. gestión de pauta, creativos) → suma a "Ingresos cobrados" de octubre.
2. **Presupuesto de pauta** — Víctor adelantó 100 USD para que se ejecute pauta
   → NO es ingreso propio; es fondo de terceros para gasto en Ads.

El briefing vigente restringe "No publicar Ads sin aprobación" y "No gastar dinero
sin aprobación", por lo que la lectura 2 no habilita gasto automático.

## Acción requerida

1. Registrar el dato en `Hermes/Intelligence/kpis.md` (o donde Juan lleve el mes)
   según la lectura que Juan confirme.
2. Actualizar el cuadro financiero del briefing para octubre cuando Juan lo revise
   (`Hermes/Briefings/current.md` está en el límite de TTL: last-reviewed
   2026-09-24 + 336h → vence 2026-10-08).
3. Dejar `events/` con el asiento aplicado.

## Restricción

- Nada de esto habilita publicar Ads ni ejecutar gasto. Modo propuesta únicamente.
