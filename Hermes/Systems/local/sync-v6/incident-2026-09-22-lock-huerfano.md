---
tipo: incidente
sistema: sync-v6-local
host: DESKTOP-3V091DM (PC local)
fecha-deteccion: 2026-09-22
fecha-inicio: 2026-08-09T17:57:01-03:00
fecha-resolucion: 2026-09-22T20:50-04:00
severidad: alta (silencio de 44 días, sin pérdida de datos)
estado: resuelto
detectado-por: brain-local
---

# Incidente — el sync local del vault estuvo muerto 44 días (lock huérfano)

## Síntoma

`hermes-vault-sync` no sincronizaba nada desde el **2026-08-09 18:56** y nadie se
enteró: la tarea programada terminaba con código **75 (lock busy)** cada 2 minutos,
en silencio, 36.309 veces. El log creció a 7,38 MB de líneas idénticas
`lock=busy fallback=mkdir` hasta rotar.

## Causa raíz

Doble falla:

1. **Lock huérfano.** El fallback de lock por directorio (`~/.hermes/vault-sync-local.lock.d`)
   se limpia con `trap ... EXIT INT TERM`. Un `kill` duro del proceso (fin de sesión,
   reinicio, Task Scheduler cortando por `ExecutionTimeLimit`) no ejecuta el trap: el
   directorio queda. La versión de ese momento **no escribía el PID del dueño ni
   validaba antigüedad**, así que toda corrida posterior salió con 75 para siempre.
2. **Detector de conflictos que nunca disparaba.** `conflict_state()` evaluaba
   `[ -d "$(git rev-parse --git-path rebase-merge)" ]`. Ese comando devuelve una ruta
   **relativa al vault** (`.git/rebase-merge`), así que el test se evaluaba contra el
   cwd del proceso y daba falso siempre. Consecuencia real: cuando quedó un
   `rebase-merge` interrumpido (17/07 09:48) el script intentó el pull 3 veces en vez
   de abortar limpio, y el mensaje de error no orientaba.

## Daño real

- **Sin pérdida de datos.** El autostash del rebase interrumpido
  (`da9dbf59…`, 1 archivo: `Systems/Local-PC/Reports/setup-desktops-20260717-104728.log`)
  ya estaba en `HEAD` y en `origin/main` — recuperado por el backup diario posterior.
- Divergencia acumulada al momento de la detección: `behind=2 ahead=1 dirty=9`.
  El local leyó un vault de 6 semanas (los handoffs del VPS no cambiaron en ese lapso;
  el remoto solo archivó los ya cerrados, así que **no había trabajo perdido**).
- Efecto operativo: el freshness gate del protocolo de apertura estaba fallando, así
  que brain-local no podía ejecutar handoffs con confianza.

## Fix aplicado

| # | Acción | Evidencia |
|---|---|---|
| 1 | Verificar que no hubiera proceso vivo | sin procesos de sync |
| 2 | Remover lock huérfano (backup previo en `~/.hermes/vault-sync-stale-lock-backup-20260922`) | `rmdir` OK |
| 3 | Archivar y remover el `rebase-merge` husk (backup en `cache/scratch/rebase-husk-20260922`) | `git status` vuelve a operar |
| 4 | `hermes-vault-sync --sync` | `committed=1 pushed=1 dirty=0 ahead=0 behind=0` |
| 5 | Hardening del script (ver abajo) | 9/9 tests + probe sobre el vault real |
| 6 | Desactivar la 2ª tarea duplicada `Hermes Vault Sync Local V6` | queda solo `HermesVaultSyncLocal` (2 min) |
| 7 | Rotación automática del log | 7,38 MB → `vault-sync-local.log.1`, log nuevo en 309 B |

## Hardening del script (v2026-09-22)

Script live: `~/.local/bin/hermes-vault-sync` · copia versionada:
`Hermes/Systems/local/scripts/vault-sync-local.sh` (sha256 idéntico: `5b495ee4…`).

1. **Lock consciente del dueño.** Al crear el lock se escribe `$$` en `lock.d/pid`.
   Si el lock existe:
   - dueño vivo → `lock=busy` (75), correcto;
   - dueño muerto (PID grabado y ya no existe) → se **rompe** el lock y sigue;
   - sin PID y con antigüedad ≥ `HERMES_VAULT_SYNC_LOCK_STALE_SECONDS` (default 600 s) → se rompe y sigue;
   - sin PID y joven → busy (protege la ventana de un dueño viejo que no escribía PID).
   Romper el lock es **reversible**: se renombra el directorio a `lock.d.stale.<pid>`
   en lugar de borrarlo (no hay `rm -rf` en el camino crítico).
2. **Detector de conflictos arreglado.** `git_path()` resuelve la salida de
   `rev-parse --git-path` contra el vault, así que ahora **sí** detecta
   `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD` y `ls-files -u`
   antes de tocar nada (aborta con exit 2 y mensaje explícito).
3. **Normalización de path.** `resolve_vault` pasa el path por `cygpath -m` cuando
   existe (Git Bash). **git nativo de Windows NO traduce paths MSYS**: con
   `HERMES_VAULT_PATH=/c/...` todas las llamadas a git fallaban en silencio y el script
   no hacía nada sin reportar error.
4. **Rotación de log** al superar `HERMES_VAULT_SYNC_LOG_MAX_BYTES` (default 5 MiB).

## Verificación

Suite de 9 casos (`cache/scratch/test-vault-sync.sh`, repo descartable): lock fresco sin
PID → 75 · lock viejo sin PID → rompe y sigue · PID muerto → rompe y sigue · PID vivo →
75 · sin residuo de lock · conflicto por `rebase-merge` (path nativo y MSYS) → exit 2 ·
`MERGE_HEAD` → exit 2 · sin conflicto → dry-run corre.

**9 PASS / 0 FAIL.** Probe adicional sobre el vault real: con `rebase-merge` recreado a
propósito, `--dry-run` devuelve `ERROR: Git conflict/rebase/merge state detected` y exit
2 (antes intentaba el pull 3 veces y fallaba con el mensaje de rebase de git).

Post-fix, el log de producción muestra corridas cada 2 minutos con
`level=OK ... dirty=0 ahead=0 behind=0`.

## Pendientes / limitaciones declaradas

- **Heurística de PID**: con PID presente y vivo el script nunca rompe el lock, para no
  corromper una corrida concurrente. Si ese PID hubiera sido reciclado por un proceso
  ajeno al sync, la corrida quedaría en `busy`. El riesgo real es bajo: la tarea tiene
  `ExecutionTimeLimit` PT5M, así que un dueño colgado muere y la corrida siguiente lo
  detecta como PID muerto y rompe el lock. Mitigación manual si hiciera falta:
  `rmdir ~/.hermes/vault-sync-local.lock.d`.
- La ficha del perfil no cambia: sigue `pc-ops` documentado sin profile real
  (ver la conversación del 22/09) — fuera del alcance de este incidente.
