---
type: config-update-proposal
status: pending-juan
created-at: 2026-07-12T20:50:30-03:00
created-by: brain-vps
target: Hermes/Config/ARCHITECTURE.md
section: 12 Sincronización
reason: runtime-changed-with-explicit-juan-approval
---

# Actualizar ARCHITECTURE.md — Sync V6

## Motivo

Juan autorizó explícitamente Sync V6 el 2026-07-12. El runtime VPS ya fue cambiado y verificado, pero `Hermes/Config/ARCHITECTURE.md` continúa mostrando el cron anterior cada 15 minutos con una expresión `&& ... || ...` sin agrupación robusta.

brain-vps no modifica `Hermes/Config/`; esta nota solicita que Juan consolide el cambio documental.

## Estado real a reflejar

- Los agentes no ejecutan Git; un proceso independiente mantiene el sync.
- VPS ejecuta `Hermes/Systems/vps/scripts/vault-sync.sh --sync` cada 2 minutos.
- El script usa lock, pull con rebase/autostash, commit condicional, segundo pull, retry de push y verificación final.
- Logs VPS: `~/.hermes/logs/vault-sync-vps.log`.
- Ante conflictos se detiene y exige revisión manual; no usa reset hard, clean ni force push.
- PC local queda pendiente de `HO-2026-07-12-002` para implementar Task Scheduler, freshness gate y script equivalente.
- `close-hermes` quedará como fallback y deberá reutilizar el script común local.

## Fuente operativa

```text
Hermes/Systems/vps/sync-v6.md
Hermes/Systems/vps/cron/current-crons.md
Hermes/Handoffs/vps-to-local/HO-2026-07-12-002/request.md
```

## Acción requerida

Juan debe aprobar/realizar la actualización de la sección 12 de `ARCHITECTURE.md` y luego marcar esta nota como consolidada o archivarla.
