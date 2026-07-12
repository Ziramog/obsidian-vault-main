---
owner: brain-vps
status: active
version: 6.0
implemented-at: 2026-07-12T20:46:00-03:00
director-approval: Juan explicit 2026-07-12
local-rollout: pending HO-2026-07-12-002
---

# Sync V6 — Obsidian vault

## Objetivo

Eliminar la dependencia de `git pull` / `git push` manual para el bus de coordinación Hermes, manteniendo la regla de que los agentes solo escriben archivos y un proceso independiente controla Git.

## Estado

| Componente | Estado |
|---|---|
| VPS auto-sync | ✅ Operativo y verificado |
| Frecuencia VPS | Cada 2 minutos |
| Lock concurrente | ✅ Verificado |
| Pull + rebase/autostash | ✅ |
| Commit condicional | ✅ |
| Segundo pull antes de push | ✅ |
| Retry de red | ✅ Hasta 3 intentos |
| Verificación final | ✅ `dirty=0 ahead=0 behind=0` |
| Logs user-writable | ✅ `~/.hermes/logs/` |
| PC local auto-sync | 🟡 Pendiente `HO-2026-07-12-002` |
| Freshness gate brain-local | 🟡 Pendiente `HO-2026-07-12-002` |

## Archivos

```text
Hermes/Systems/vps/scripts/vault-sync.sh
Hermes/Systems/vps/cron/user-crontab-v6.txt
Hermes/Systems/vps/cron/backups/user-crontab-2026-07-12-pre-sync-v6.txt
Hermes/Systems/vps/cron/current-crons.md
```

Runtime:

```text
/home/hermes/.hermes/logs/vault-sync-vps.log
/home/hermes/.cache/hermes-vault-sync-vps.lock
```

## Cron activo

```cron
*/2 * * * * /home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/vault-sync.sh --sync >/dev/null 2>&1
```

## Operación

### Sincronización completa

```bash
/home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/vault-sync.sh --sync
```

### Solo traer remoto

```bash
/home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/vault-sync.sh --pull-only
```

### Estado

```bash
/home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/vault-sync.sh --status
```

Estado sano:

```text
dirty=0 ahead=0 behind=0
```

### Validación sin Git

```bash
/home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/vault-sync.sh --dry-run
```

## Secuencia de seguridad

```text
flock
→ verificar que no exista merge/rebase/cherry-pick activo
→ verificar que no haya archivos unmerged
→ pull --rebase --autostash
→ add -A
→ commit solo si staged diff retorna cambios
→ segundo pull para cerrar la ventana de carrera
→ push con retry
→ validar dirty/ahead/behind
```

El script no ejecuta:

```text
git reset --hard
git clean
git push --force
resolución automática de conflictos
```

Ante un conflicto o estado Git incompleto, sale con error y exige revisión manual.

## Evidencia de implementación

Primera ejecución automática del cron nuevo:

```text
2026-07-12T20:46:02-03:00 pull OK
2026-07-12T20:46:02-03:00 commit auto-sync [vps]
2026-07-12T20:46:03-03:00 segundo pull OK
2026-07-12T20:46:04-03:00 push OK
2026-07-12T20:46:04-03:00 dirty=0 ahead=0 behind=0
```

Publicación automática del handoff local:

```text
2026-07-12T20:48:01-03:00 commit HO-2026-07-12-002
2026-07-12T20:48:03-03:00 push OK
2026-07-12T20:48:03-03:00 dirty=0 ahead=0 behind=0
```

Prueba del lock:

```text
2026-07-12T20:48:51-03:00 level=SKIP reason=lock_busy rc=0
```

## Logs corregidos

Los procesos de usuario ya no intentan crear logs nuevos bajo `/var/log/`. Rutas activas:

```text
~/.hermes/logs/vault-sync-vps.log
~/.hermes/logs/handoff-alerts.log
~/.hermes/logs/handoff-archive.log
~/.hermes/logs/vault-ownership.log
```

Los últimos tres aparecerán después de su próxima ejecución programada.

## Rollback

Si Sync V6 falla:

1. Validar el backup:

```bash
crontab -n /home/hermes/obsidian-vault/Hermes/Systems/vps/cron/backups/user-crontab-2026-07-12-pre-sync-v6.txt
```

2. Restaurar:

```bash
crontab /home/hermes/obsidian-vault/Hermes/Systems/vps/cron/backups/user-crontab-2026-07-12-pre-sync-v6.txt
```

3. Confirmar:

```bash
crontab -l
```

## Trabajo local pendiente

`HO-2026-07-12-002` pide a `brain-local → pc-ops`:

- script equivalente local;
- Windows Task Scheduler cada 2 minutos y al iniciar sesión;
- freshness gate antes de leer handoffs;
- comandos humanos `hermes-sync` y `hermes-sync-status`;
- `close-hermes` como fallback;
- prueba real PC → GitHub → VPS sin push manual final.

Hasta que ese handoff esté completado, VPS → GitHub es automático, pero la PC todavía puede necesitar un pull inicial para recibir por primera vez el propio handoff de automatización.
