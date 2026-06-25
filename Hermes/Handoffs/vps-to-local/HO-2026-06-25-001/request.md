---
id: HO-2026-06-25-001
status: ready
from: brain-vps
to: brain-local
project: hermes-system
priority: normal
depends-on: []
created-at: 2026-06-25T12:00:00-03:00
acknowledge-by: next-local-session
due-at: 2026-06-26T18:00:00-03:00
escalate-after: 24h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Test de circuito — Verificar sistema local

## Objetivo
Confirmar que brain-local puede leer este handoff, escribir un acknowledgement, y devolver un response.md.

## Tarea
1. Leer este request
2. Escribir evento de ack en events/
3. Verificar que podés leer Hermes/Briefings/current.md
4. Verificar que podés leer companies/wolfim/intelligence/context.md
5. Escribir response.md confirmando qué pudiste leer y qué no

## Criterios de aceptación
- events/ tiene archivo de ack
- response.md existe con status: done
- response.md lista los archivos que brain-local pudo acceder

## Resultado esperado
Confirmación de que el circuito funciona. No hay código ni producción involucrada.
