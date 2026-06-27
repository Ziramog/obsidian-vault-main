---
type: cron-activated
author: brain-vps
timestamp: 2026-06-27T09:27:00-03:00
---

# Agenda V2 scanner activado

Juan ordenó explícitamente: "activa".

Se creó Hermes cron:
- job_id: `acafddde60b4`
- name: `Agenda V2 reminder scanner`
- schedule: `every 5m`
- no_agent: `true`
- deliver: `origin`
- script: `/home/hermes/.hermes/scripts/agenda-reminder-scan.sh`
- next_run_at informado por Hermes: `2026-06-27T09:34:06.688852-03:00`

Wrapper creado para evitar spam: si no hay recordatorios vencidos, stdout queda vacío y no se entrega nada a Juan. Si hay recordatorio enviado o error, stdout no vacío/error se entrega.
