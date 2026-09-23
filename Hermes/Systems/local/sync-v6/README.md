# Sync V6 local — estado de instalación

Fecha: 2026-07-12
Host: DESKTOP-3V091DM
Usuario Windows: DESKTOP-3V091DM\\ingju

## Decisión operativa

El handoff pidió Windows Task Scheduler invocando WSL. En esta PC `wsl.exe` existe, pero no hay una distribución Linux configurada; `wsl.exe --list --verbose` devuelve la ayuda de instalación y `wsl.exe --list --online` muestra distros instalables. Para no instalar software ni requerir privilegios, la implementación local usa Git Bash incluido por Hermes.

## Archivos

- Script versionado: `Hermes/Systems/local/scripts/vault-sync-local.sh`
- Runner oculto Windows: `Hermes/Systems/local/scripts/run-vault-sync-hidden.vbs`
- Export Task Scheduler: `Hermes/Systems/local/sync-v6/task-scheduler.xml`
- Log fuera del vault: `~/.hermes/logs/vault-sync-local.log`
- Lock fuera del vault: `~/.hermes/vault-sync-local.lock` o fallback `~/.hermes/vault-sync-local.lock.d`

## Comandos instalados en `~/.local/bin`

- `hermes-vault-sync --sync|--pull-only|--status|--dry-run`
- `hermes-sync`
- `hermes-sync-status`
- `close-hermes`
- `brain-local-sync`

`close-hermes` queda como fallback manual y llama al script común. `brain-local-sync` ejecuta `hermes-vault-sync --pull-only` antes de lanzar `hermes --profile brain-local`.

## Task Scheduler

Tarea: `HermesVaultSyncLocal`

Triggers:

- Logon del usuario `DESKTOP-3V091DM\\ingju`
- Unlock de sesión
- Repetición cada 2 minutos

Acción:

```text
C:\Windows\System32\wscript.exe //B //Nologo "C:\Projects\Obsidian\obsidian-vault-main\Hermes\Systems\local\scripts\run-vault-sync-hidden.vbs"
```

El VBS ejecuta Git Bash oculto:

```text
C:\Users\ingju\AppData\Local\hermes\git\usr\bin\bash.exe -lc "~/.local/bin/hermes-vault-sync --sync"
```

## Limitaciones documentadas

- `flock` no existe en el Git Bash de Hermes; el script lo usa si aparece en PATH y, mientras no exista, usa lock por directorio atómico como fallback reversible.
- No se modificó el alias oficial de Hermes; el wrapper reversible recomendado para sesiones CLI es `brain-local-sync`.
- Hermes Desktop/TUI puede abrir el profile sin pasar por wrappers externos. La tarea cada 2 minutos reduce esa ventana; si Juan abre por CLI y quiere freshness gate estricto, usar `brain-local-sync`.

## Hardening 2026-09-22 (post-incidente)

Detalle completo en `incident-2026-09-22-lock-huerfano.md`. Resumen:

- El lock por directorio quedó **consciente del dueño**: escribe `lock.d/pid` y rompe el
  lock solo si el dueño está muerto, o si no hay PID y la antigüedad supera
  `HERMES_VAULT_SYNC_LOCK_STALE_SECONDS` (default 600 s). Romper = renombrar a
  `lock.d.stale.<pid>`, nunca borrar. Antes un proceso muerto dejaba el lock para
  siempre y el sync salía 75 en silencio (44 días, 36.309 corridas).
- El detector de conflictos **ahora sí dispara**: `rev-parse --git-path` responde
  relativo al vault y hay que resolverlo contra `$VAULT` antes de testearlo.
- `resolve_vault` normaliza con `cygpath -m` cuando existe: git nativo de Windows no
  traduce paths MSYS, y con `HERMES_VAULT_PATH=/c/...` todas las llamadas a git fallaban
  en silencio.
- Rotación automática del log por encima de `HERMES_VAULT_SYNC_LOG_MAX_BYTES` (5 MiB).
- La segunda tarea duplicada `Hermes Vault Sync Local V6` quedó **deshabilitada**
  (corría el mismo script cada 2 min, duplicando corridas). Reactivar con
  `schtasks /change /tn "Hermes Vault Sync Local V6" /enable` solo si se quiere volver
  al esquema duplicado.
- Verificación: 9/9 casos en repo descartable + probe sobre el vault real
  (`rebase-merge` recreado a propósito → exit 2 con mensaje explícito).

