---
id: HO-2026-06-27-001
status: ready
from: brain-vps
to: brain-local
project: hermes-system
priority: normal
depends-on: []
created-at: 2026-06-27T09:05:38-03:00
acknowledge-by: next-local-session
due-at: 2026-06-30T18:00:00-03:00
escalate-after: 72h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Aviso de lanzamiento — Agenda V2

## Objetivo

Que brain-local quede al tanto de la propuesta de Agenda V2 antes de implementación y pueda coordinar pc-ops/web-builder si luego Juan pide trabajo local.

## Documento a leer

- `Hermes/Intelligence/arch_agenda_v2.md`

## Contexto

Juan pidió evolucionar la agenda para que sea una herramienta diaria usable desde móvil vía Telegram, legible por cualquier terminal PC/VPS, con recordatorios automáticos y posible carga por audio.

Decisión de diseño propuesta:
- Mantener `Hermes/Agenda/YYYY-MM-DD.md` como fuente de verdad.
- Agregar formato Agenda V2 con frontmatter, IDs de tarea, reminders declarativos y vínculo a Sessions/Daily.
- Telegram puede recibir audio, pero debe devolver texto por defecto.
- Implementar primero CLI/parser y luego scanner de recordatorios.

## Pedido para brain-local

1. Leer `Hermes/Intelligence/arch_agenda_v2.md`.
2. Confirmar en `response.md` que brain-local entiende el lanzamiento y qué parte correspondería a local/pc-ops si Juan lo pide.
3. No implementar todavía. La implementación arranca después de confirmación explícita de Juan.

## Criterios de aceptación

- `response.md` con `status: acknowledged` o `status: done`.
- Lista de consideraciones locales si las hay: alias CLI, Windows/WSL, Telegram desktop, sync local, audio/STT local.
- Sin cambios de código ni cron todavía.

## Restricciones

- No tocar `Hermes/Config/`.
- No modificar crons.
- No implementar sin nueva orden de Juan.
