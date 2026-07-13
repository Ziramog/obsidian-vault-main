---
handoff: HO-2026-07-12-002
status: done
actor: pc-ops
coordinator: brain-local
completed-at: 2026-07-12T21:38:23-03:00
---

# Resultado — Sync V6 local

Implementación completada en la PC local usando `pc-ops` vía coordinación de `brain-local`.

## Resumen operativo

- Se sincronizó el vault una vez al abrir la sesión (`git pull --ff-only`; resultado: `Already up to date`).
- Se creó el script versionado `Hermes/Systems/local/scripts/vault-sync-local.sh`.
- Se instalaron comandos humanos en `~/.local/bin`:
  - `hermes-vault-sync --sync|--pull-only|--status|--dry-run`
  - `hermes-sync`
  - `hermes-sync-status`
  - `close-hermes`
  - `brain-local-sync`
- Se creó una tarea Windows Task Scheduler no administrativa: `HermesVaultSyncLocal`.
- Se exportó la definición real de la tarea a `Hermes/Systems/local/sync-v6/task-scheduler.xml`.
- Se conservó `close-hermes` como fallback manual, ahora llamando al script común.
- No se modificó `Hermes/Config/`.
- No se almacenaron secretos ni credenciales en scripts, XML, logs o documentación.

## Descubrimiento obligatorio

| Item | Resultado |
|---|---|
| Host Windows | `DESKTOP-3V091DM` |
| Usuario Windows | `ingju` (`DESKTOP-3V091DM\\ingju`) |
| Distribución WSL real | **No hay distro WSL configurada**. `wsl.exe` existe, pero `wsl.exe --list --verbose` devuelve la ayuda de instalación; `wsl.exe --list --online` muestra distros instalables. |
| Usuario Linux local | No aplica: no hay distro WSL inicializable. |
| Ruta real del vault local | `C:/Projects/Obsidian/obsidian-vault-main` |
| `wsl.exe` | `C:\Windows\System32\wsl.exe` |
| systemd en WSL | No aplica: sin distro WSL. |
| Cómo se inicia brain-local | Hermes Desktop/TUI con profile `brain-local`; alias oficial detectado: `brain-local.hermes-original → hermes -p brain-local` en `C:\Users\ingju\.local\bin\brain-local.hermes-original.bat`. |
| Git remote | `origin https://github.com/Ziramog/obsidian-vault-main.git` fetch/push |
| Rama | `main` |
| Autenticación GitHub | `git ls-remote --exit-code origin main` OK; no se expusieron credenciales. |

## Decisión técnica por WSL ausente

El handoff pedía Task Scheduler invocando WSL:

```text
wsl.exe -d <DISTRO_REAL> -- bash -lc '~/.local/bin/hermes-vault-sync --sync'
```

Como esta PC no tiene distro WSL configurada y el handoff no autoriza instalar software ni requerir admin, se implementó fallback operativo con Git Bash incluido por Hermes:

```text
C:\Windows\System32\wscript.exe //B //Nologo "C:\Projects\Obsidian\obsidian-vault-main\Hermes\Systems\local\scripts\run-vault-sync-hidden.vbs"
```

Ese VBS ejecuta oculto:

```text
C:\Users\ingju\AppData\Local\hermes\git\usr\bin\bash.exe -lc "~/.local/bin/hermes-vault-sync --sync"
```

## Seguridad implementada

El script incluye:

- lock: usa `flock` si existe; en este Git Bash no existe `flock`, por lo que usa fallback atómico por directorio (`~/.hermes/vault-sync-local.lock.d`);
- timeout para operaciones Git (`timeout`, 60s por defecto);
- hasta 3 intentos ante fallos transitorios;
- `git pull --rebase --autostash origin main`;
- commit condicional con mensaje `auto-sync [local]`;
- segundo pull antes de push;
- retry final de push después de rebase;
- detección de `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD` y archivos unmerged;
- ante conflicto: corta, no elige versión, devuelve código distinto de cero;
- no usa `git reset --hard`, `git clean`, borrado de stashes ni force push;
- no registra URLs con tokens ni credenciales.

## Task Scheduler

Tarea creada:

```text
HermesVaultSyncLocal
```

Evidencia `schtasks /Query /TN HermesVaultSyncLocal /V /FO LIST`:

```text
TaskName:        \HermesVaultSyncLocal
Status:          Ready
Last Run Time:   7/12/2026 9:37:01 PM
Last Result:     0
Run As User:     ingju
Task To Run:     C:\Windows\System32\wscript.exe //B //Nologo "C:\Projects\Obsidian\obsidian-vault-main\Hermes\Systems\local\scripts\run-vault-sync-hidden.vbs"
Repeat: Every:   0 Hour(s), 2 Minute(s)
```

Triggers configurados:

- al iniciar sesión del usuario;
- al desbloquear sesión;
- repetición cada 2 minutos.

## Freshness gate

Se creó wrapper reversible, sin sobrescribir el alias oficial:

```text
brain-local-sync
```

Workflow:

```bash
hermes-vault-sync --pull-only
hermes --profile brain-local
```

Si `--pull-only` falla, el wrapper corta con:

```text
⚠️ Vault no sincronizado. No ejecuto handoffs porque puedo estar leyendo información vieja.
```

Limitación: Hermes Desktop/TUI puede abrir `brain-local` sin pasar por wrappers externos. La tarea cada 2 minutos reduce la ventana de stale reads; para gate estricto en CLI, Juan debe abrir con `brain-local-sync`.

## Verificación ejecutada

### Sintaxis

```text
bash -n Hermes/Systems/local/scripts/vault-sync-local.sh
=> OK
```

### Dry run

```text
DRY RUN OK
Host: local
Vault: C:/Projects/Obsidian/obsidian-vault-main
Branch: origin/main
Git: /mingw64/bin/git
Timeout command: /usr/bin/timeout
Lock command: missing; using mkdir fallback
GitHub: accesible
```

### Lock

Prueba con dos ejecuciones simultáneas:

```text
first_rc=0
second_rc=75
second_output=ERROR: vault sync already running (mkdir lock fallback).
```

### Pull-only / freshness gate

Después de corregir el código de retorno, `hermes-vault-sync --pull-only` devuelve `0` cuando el pull fue exitoso aunque existan cambios locales pendientes por publicar.

### Task Scheduler real

Se ejecutó `schtasks /Run /TN HermesVaultSyncLocal` y luego `schtasks /Query` mostró:

```text
Status:      Ready
Last Result: 0
```

### Status humano

Cuando no había cambios pendientes, el comando devolvió:

```text
✅ Vault sincronizado
Host: local
GitHub: accesible
Cambios pendientes: 0
Handoffs nuevos: 6
Conflictos: 0
Ahead: 0
Behind: 0
```

Logs reales en `~/.hermes/logs/vault-sync-local.log`:

```text
2026-07-12T21:37:11-0300 host=local level=OK mode=--sync committed=1 pushed=1 dirty=0 ahead=0 behind=0
2026-07-12T21:37:13-0300 host=local level=OK mode=--sync committed=1 pushed=1 dirty=0 ahead=0 behind=0
```

## Archivos tocados

Dentro del vault:

- `Hermes/Systems/local/scripts/vault-sync-local.sh`
- `Hermes/Systems/local/scripts/run-vault-sync-hidden.vbs`
- `Hermes/Systems/local/sync-v6/task-scheduler.xml`
- `Hermes/Systems/local/sync-v6/README.md`
- `Hermes/Handoffs/vps-to-local/HO-2026-07-12-002/response.md`
- `Hermes/Handoffs/vps-to-local/HO-2026-07-12-002/events/2026-07-12T21-38-done.md`

Fuera del vault:

- `~/.local/bin/hermes-vault-sync`
- `~/.local/bin/hermes-sync`
- `~/.local/bin/hermes-sync-status`
- `~/.local/bin/close-hermes`
- `~/.local/bin/brain-local-sync`
- Windows Task Scheduler: `HermesVaultSyncLocal`
- Logs: `~/.hermes/logs/vault-sync-local.log`

## Limitaciones / desviaciones aceptadas

1. **WSL**: no se pudo usar WSL porque no hay distro instalada/configurada. No instalé Ubuntu/Debian porque implicaría software nuevo y posible privilegio/admin. Implementé Git Bash fallback funcional.
2. **flock**: Git Bash de Hermes no trae `flock`; el script intenta usarlo si aparece en PATH y usa lock por directorio mientras tanto.
3. **Desktop freshness gate**: no modifiqué destructivamente el alias oficial ni el launcher de Hermes Desktop. El wrapper CLI recomendado es `brain-local-sync`.
4. **Verificación VPS**: local quedó publicando a GitHub; la verificación de aparición en VPS corresponde a `brain-vps` después de un ciclo remoto.

## Estado final esperado

Tras el próximo ciclo de `HermesVaultSyncLocal`, este `response.md` y el evento `done` deben quedar publicados sin `git push` manual final, con:

```text
dirty=0 ahead=0 behind=0
```
