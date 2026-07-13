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
