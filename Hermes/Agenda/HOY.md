---
owner: brain-vps
date: 2026-08-28
updated-at: 2026-08-28T10:03:03-03:00
summary-status: in-progress
source: cron_campaign
---

# Agenda 2026-08-28

## 🔴 Prioridad alta / arrastre

- [ ] **Actualizar KPIs formales** — ingresos cobrados del mes, gastos fijos, gap mensual, objetivo vigente. Vencido desde 2026-06-25.
- [ ] **Decidir Web Viejas** — reabastecer leads nuevos o pausar canal y hacer follow-up humano. La cola automática está agotada.
- [ ] **Revisar handoff Wolfim Motors Demo `HO-2026-08-03-002`** — high, vencido, sin response visible.
- [ ] **Corregir warning `email-suite` ambiguo** — los crons `check-replies` ejecutan, pero reportan colisión de skill/nombre.
- [ ] **Triage de `errors.log` Hermes** — health check previo reportó errores no auto-reparables.
- [ ] **Verificar Hermes update/gateway** — gateway estaba activo en 0.20.6, con update pendiente reportado.

## ✅ Cerrado hoy

- [x] **`cron_campaign.py` ejecutado 10:03 ART:** cola agotada; stdout: `✅ Todos los leads han sido enviados. No hay más pendientes.` Verificación tracker: 107 total, 97 sent, 10 bounced, 0 failed, 0 pendientes componibles.

## 🟡 Atención operativa

- KPIs formales vencidos; semáforo financiero no confirmable.
- Briefing vigente vencido; no cambiar prioridades sin Juan.
- Web Viejas no tiene inventario útil para próximas tandas; seguir corriendo el cron sin reabastecer no genera oportunidades nuevas.
- Arrastres 🔴 de ayer detectados; como este job corre sin usuario presente, quedan visibles pero no se reasignan.
