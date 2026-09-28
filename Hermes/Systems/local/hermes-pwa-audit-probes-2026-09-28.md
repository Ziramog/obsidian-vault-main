# hermes-pwa — probes del auditor sobre infra viva (2026-09-28 ~18:15-18:20)

Ejecutado por `@web-auditor` desde el nodo PC. Todo medido, nada leído del informe previo.

## 0. Estado del repo (bloqueante)

- `C:\Projects\hermes-pwa` → HEAD `46ca485`, árbol limpio (`git status` vacío).
- Los prompts de Fase 1 y Fase 2 existen sólo como markdown en `Hermes/Quarantine/` (18:06 / 18:07).
- **No hay commit que reverificar**: cero diferencia entre baseline auditado y HEAD. Cuando aterricen,
  corro los probes sobre el commit y publico el delta (así el "después" es atribuible).

## 0-bis. CORRECCIÓN (18:35) — el censo y el "204" quedaron corregidos

- Censo verificado: **63** sesiones de sala (falta `HERMES_HOME/state.db`, perfil `default`, 2 en `rmufxz2ti`),
  **60 `hidden=1` / 3 visibles**, por sala: rmuag13gp 31 · rmugviqw9 23 · rmufxz2ti 6 · rmuli31hi 3.
  Excluir del censo `HERMES_HOME/state-snapshots/*/state.db` (copia vieja, esquema sin columna `hidden`).
- Cruce independiente (value real de `hermes.plugin.hermes-bots.group-chats`, leído del `.ldb` con
  footer+index+snappy): 4 salas, con su `log` / `sessions` / `watermarks` / `members`:

| sala | log (store) | sessions (store) | state.db sesiones | members |
|---|---|---|---|---|
| rmugviqw9-6zez7 | 115 | 30 | 23 | 3 |
| rmufxz2ti-w6sk5 | 172 | 10 | 6 | 3 |
| rmuag13gp-5r3kn | 327 | 33 | 31 | 2 |
| rmuli31hi-inptr | 10 | 3 | 3 | 4 |

- **El "204 turnos" era un artefacto de mi parser**: reconstruir desde los envoltorios de `state.db` no reproduce
  el log del store (parser estricto: 102 / 96 / 475 / 15 vs store 115 / 172 / 327 / 10). Infla porque los mensajes
  se citan entre sí (las líneas `  Nombre [nodo]: texto` reaparecen dentro de otros mensajes) y desinfla porque
  un bot que se suma tarde no tiene envoltorio de los mensajes viejos. El número correcto para cerrar Fase 2 es
  **115 (log del store)**, no 204.
- El store referencia **76 mappings de sesión** (30+10+33+3) contra 63 filas reales: guarda ids huérfanos
  (rmugviqw9 30 vs 23) → el peer fetch debe tolerarlos y no usarlos como fuente del conteo.

## 1. B1 — auth decorativa (reproducido por el auditor)

Contra la PWA del VPS `http://100.124.132.48:3000`:

| request | resultado |
|---|---|
| `GET /api/profiles` + `Authorization: Bearer totally-fake-key` | **200**, 3881 bytes, 17 perfiles (8 local + 9 vps) con `sessionCount` real |
| `GET /api/profiles` sin header | **401** |
| `GET /api/groups/rmugviqw9-6zez7/messages` + key falsa | **200** |
| `GET /api/health` | **404** (no existe) |
| `GET /api/sessions?...&node=pc` | **200** con `{"error":"Unknown or unconfigured profile"}` → B7 (proxy traga errores) |
| Hermes del VPS en `:9119` + misma key falsa | **401** → el agujero es del PWA, no del gateway |

sessionCount devueltos con key falsa: wolfim-growth 22, algolab 24, brain-local 27, web-builder 50, web-auditor 1.

## 2. B2 — replicación de salas: número propio

Nodos comparados: lo que sirve el PWA del VPS vs lo que hay en los `state.db` del nodo PC.

| sala | PWA VPS | state.db (nodo PC) |
|---|---|---|
| `rmugviqw9-6zez7` | **3** msgs (1 real + 2 del `PING E2E` / `E2E_OK`) | 23 sesiones de bot → **204 turnos distintos** (508 menciones con repetición) |
| `rmufxz2ti-w6sk5` | **0** (`{"messages":[]}`) | 4 sesiones / 548 msgs |
| `rmuli31hi-inptr` (sala actual) | **0** + `warning:"Group room not found in local profile"` | 2 sesiones / 174 msgs |
| `rmuag13gp-5r3kn` | **54** | 31 sesiones / 4590 msgs |

- El "1 msg" del informe previo hoy es 3: el E2E escribió 2 mensajes en el log del `profile.yaml` del VPS.
  El baseline quedó mutado por la propia verificación → comparar antes/después exige congelar ese log.
- Total de sesiones de sala en los 9 `state.db` del nodo PC: **60**, no 61.
  Desglose: `rmugviqw9` 23 (brain-local/web-auditor/web-builder), `rmuag13gp` 31 (algolab 16 + algolab-strategy 15),
  `rmufxz2ti` 4 (brain-local), `rmuli31hi` 2 (brain-local, web-builder). Falta ubicar la sesión 61.
- **Reconstrucción exitosa**: parseando el envoltorio de cada `user` de las sesiones de `rmugviqw9`
  (`New messages in the room since your last turn:` + líneas `  Nombre [nodo]: texto`) sale la conversación
  ordenada completa: 204 turnos, primero `1790357897`, último `1790550139`. Fase 2 es viable **sólo con `state.db`**.
- Las sesiones de sala se titulan `Group: <roomId> · <thread>` de forma estable, incluidas las de la sala actual
  (`Group: rmuli31hi-inptr · tmuls27a9-gy4qv`: brain-local 84 msgs, web-builder 90 msgs).

## 3. Store del Desktop: la evidencia de Fase 2, a nivel de byte

- `%APPDATA%\Hermes\Local Storage\leveldb\MANIFEST-000001` (vivo, 18:15): la clave aparece como
  **clave real de 55 bytes** `_file://\x00\x01hermes.plugin.hermes-bots.group-chats` (origen `file://`),
  releída ~1967 veces en los rangos de archivo del MANIFEST a lo largo de la churn de compactación.
  No es texto de mensaje: es la user key del LevelDB.
- A las 18:08 se capturó un **value completo** en el `.log` vivo: registro con `roomId:"rmuli31hi-inptr"`,
  `members` (incluye `default` con `connectionKind:"remote"` en `100.124.132.48:9119`), `watermarks`,
  `heldMessages`, `externalCursors` y `sessions:{"thread:tmuls27a9-gy4qv::local::web-auditor":"20260928_180756_e235d7"}`.
- Consecuencia: el store del Desktop **ya contiene el mapeo thread → id de sesión de `state.db`**, así que
  la reconstrucción no necesita adivinar salas; pero vive en localStorage del Electron (origen `file://`),
  inalcanzable para un PWA servido en `:3000` del VPS, y se reescribe de forma continua.
  → Fase 2 debe pedir la sala al nodo par / re-derivarla de `state.db`; cualquier fix que lea ese localStorage
  desde el PWA no cierra.

## 4. Pendiente para cerrar

1. Commit de Fase 1 y de Fase 2 (separados) → re-correr: 401 con bearer falso, conteo por sala vs `state.db`,
   E2E de sala, `tsc --noEmit` + `next build`.
2. Congelar el log de sala del `profile.yaml` del VPS antes de comparar (ya tiene 2 mensajes de prueba).
3. Ubicar la sesión 61 y aclarar de dónde sale ese total.
