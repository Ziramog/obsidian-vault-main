---
tipo: recon-tecnica
proyecto: hermes-pwa (PWA mobile sobre Hermes)
fecha: 2026-09-28
autor: web-builder (lectura directa de las 3 tiendas en el nodo PC)
estado: insumo-para-Fase-2
relacionado: Hermes/Systems/local/hermes-pwa-vps-audit-2026-09-28.md (B2/B3 corregidos acá)
---

# Dónde vive realmente la conversación de una sala (hermes-pwa)

Objetivo: fijar la fuente de verdad antes de escribir el fix de replicación. Todo lo de abajo salió de leer
los archivos del nodo PC, no de inferencia.

## 1. Las tres tiendas, medidas

| # | Store | Contenido real | Alcanzable por la PWA |
|---|---|---|---|
| A | `<HERMES_HOME>/profile.yaml` → `ui_meta["hermes-bots-groups"].rooms` | **1 sola sala**: `id:rmuag13gp-5r3kn` ("Algolab Strategy, Algolab", 54 entradas de log). Es lo que hoy lee `src/lib/hermes-fs.ts` + `app/api/groups/route.ts` | Sí (es la que usa) |
| B | `<HERMES_HOME>/profiles/<bot>/state.db` (+ el `HERMES_HOME/state.db` del perfil `default`) | Sesiones **ocultas** `Group: <roomId> · <threadId>` por perfil. Censo acordado del nodo PC (18:15): **63 sesiones, 60 `hidden=1`, 3 visibles** — 61 en perfiles de bots (algolab 16, algolab-strategy 15, brain-local 13, web-auditor 9, web-builder 8) **+ 2 del perfil `default`** en `HERMES_HOME/state.db` (miembro `default-this-device` de `rmufxz2ti`). Por sala: `rmuag13gp` 31 · `rmugviqw9` 23 · `rmufxz2ti` 6 · `rmuli31hi` 3 → contra **3 mensajes** que muestra la PWA del VPS (1 real + 2 del `PING E2E`) | Sí (no la usa) |
| C | localStorage del Electron (`%APPDATA%\hermes\Local Storage\leveldb`, origen `file://`, key **`hermes.plugin.hermes-bots.group-chats`**) | Store canónico del Desktop: catálogo de salas + log en vivo | **No** (LevelDB comprimido, del cliente, no sincroniza) |

Evidencia de A: en `C:\Users\ingju\AppData\Local\hermes\profile.yaml` el único room con log es
`id:rmuag13gp-5r3kn`. Un barrido de todos los `profile.yaml` del nodo (`profile.yaml` raíz + los 7 de
`profiles/*/`) da **0 hits** para `rmugviqw9`, `rmufxz2ti` y `rmuli31hi`. O sea: las salas que Juan usa
**no están en ningún `profile.yaml`**; el "espejo 54/54" del informe sólo existe para la sala de algolab.
Evidencia de C: `MANIFEST-000001` del LevelDB contiene la key `hermes.plugin.hermes-bots.group-chats`
(origen `file://`) — el catálogo de salas del Desktop vive ahí, fuera del alcance de la PWA.
Evidencia de B: `grep -l rmugviqw9` sobre todo `%LOCALAPPDATA%\hermes` (sin `hermes-agent`) → sólo
`profiles/{brain-local,web-auditor}/state.db(-wal)` y `profiles/web-builder/desktop/interrupted_turns.json`.

## 2. `state.db` no es un log de sala (por eso B2 hay que reescribirlo)

Una sesión de sala es **la sesión propia del bot**, no la sala:

```
sqlite> SELECT role, COUNT(*) FROM messages WHERE session_id='20260928_174642_658136' GROUP BY role;
assistant 30 | tool 53 | user 1
```

En una sala con varias rondas (web-auditor, sesión `20260927_141639_f2fa83`): `assistant 47 / tool 72 / user 7`.
Los turnos de la sala llegan al bot **envueltos en un mensaje `user`**:

```
[Group chat: "<room name>"] You are @<bot>, one participant in a group chat with @a, @b [on <node>] and the user.

New messages in the room since your last turn (oldest first):
  You (user): <texto>
  Hermes [100.124.132.48:9119]: <texto>
<bloque de reglas de la sala>
```

y la respuesta del bot es el mensaje `assistant` con contenido no vacío (los `assistant` de la cadena de
herramientas tienen `content` = "" y `tool_calls`). Detalles que el parser debe respetar:

- separador del título: **`·` U+00B7** rodeado de espacios (`Group: rmugviqw9-6zez7 · tmuk54861-6av2d`);
- `timestamp` en **epoch con decimales (segundos)**, p.ej. `1790553076.4554322`;
- todas las sesiones de sala están `hidden=1`;
- el mismo turno se replica en la sesión de **cada** miembro → dedupe obligatorio;
- el mismo room tiene varios `threadId` (8 para `rmugviqw9`): la sala es la suma de sus threads, en orden `at`.

## 3. Corrección a B3 del informe de brain-local

"El VPS muestra en `rmugviqw9` un mensaje de web-auditor ('eslint . = 118 problems') que en esa sala **nunca
existió**" — **existe**: es el último `assistant` de web-auditor en la sesión `20260927_141639_f2fa83`
(thread `tmuk54861-6av2d`), con `at = 1790550198785`, exactamente el `at` del seed
(`src/lib/group-registry.ts:54-62`). El bug real de B3 es otro y peor: el **log completo está hardcodeado** y
`ensureCanonicalRoomsInDoc()` lo reinyecta cuando el log está vacío, así que (a) las conversaciones nuevas no
llegan nunca por esa vía, (b) las salas nuevas son invisibles y (c) lo que se ve en el VPS es el pasado
congelado, no un fantasma inventado.

## 4. Pitfalls de implementación (para Fase 2)

- Los datos vivos de `state.db` están en el **`-wal`** (`grep` no encuentra el roomId en el `.db`, sí en el `-wal`).
  Una apertura read-only puede fallar con el WAL activo → copiar `state.db` + `-wal` + `-shm` a tmp y abrir la copia.
- `node:sqlite` (`DatabaseSync`) ya se usa en `src/lib/message-recovery.ts:35`; no hace falta dependencia nativa.
- `ui_meta` tiene cap de 64 KB y se manda en cada `profiles.list` (comentario en
  `apps/desktop/src/plugins/hermes-bots/data.ts` del repo del agente): escribir logs de sala ahí no escala y es
  el origen de la deriva entre nodos.
- El PWA del PC está caído (`:3000`) y el funnel da 502 → cualquier agregación cross-node necesita
  `HERMES_PEER_PWA_URL` y el par arriba, si no el celular ve sólo el VPS.

## 5. Cierres del equipo (2026-09-28, sobre este recon)

- **web-auditor** encontró el value completo en el `.log` del LevelDB: origen `file://`, key real de 55 bytes
  `_file://\x00\x01hermes.plugin.hermes-bots.group-chats`, con `roomId:"rmuli31hi-inptr"`, `members` (incluye
  `default` con `connectionKind:"remote"`) y un mapa `sessions:{"thread:tmuls27a9-gy4qv::local::web-auditor":"20260928_180756_e235d7"}`
  → el store del Desktop mapea thread → id de sesión de `state.db`, así que reconstruir no exige adivinar salas.
  Igual vive en localStorage del cliente: la PWA en `:3000` no lo puede leer.
- **web-auditor** reconstruyó `rmugviqw9` entera sólo con `state.db`: **204 turnos** ordenados (primero
  `1790357897`, último `1790550139`) parseando el envoltorio — o sea la reconstrucción es viable sin el store.
- **brain-local**: el nodo **VPS tiene 0 sesiones de sala** (8 bots + `default`, 52 sesiones), por lo que las
  salas del Desktop vistas desde el celular **tienen** que venir por peer fetch; con el PC apagado el estado es
  "nodo offline", no lista vacía. Contrato HTTP congelado en el prompt de Fase 2.
- **58→60 `hidden=1` / 3 visibles** (ids: brain-local `rmufxz2ti` 162 msgs, brain-local `rmugviqw9` 76,
  web-builder `rmugviqw9` 87): quien derive salas del API de sesiones ve 3 de 63 → el camino de salas no puede
  llevar el filtro `hidden`.
- **El censo por título tiene lag de minutos**: `session_key`/`chat_id`/`chat_type`/`thread_id`/`origin_json`
  están en NULL en las 63 filas; la sala y el thread viven sólo en el string `title`, que se escribe después de
  crear la fila. Comparar antes/después contra un snapshot congelado, nunca recontando en vivo.
- **Gap detectado acá (2026-09-28, posterior al censo de 61):** el censo limitado a `profiles/*/state.db` se
  come las **2 sesiones del perfil `default`** en `HERMES_HOME/state.db` (`rmufxz2ti` → 6, no 4; total 63, no 61).
  El `default` es miembro real de esa sala (`default-this-device`), así que si el PWA censa sólo directorios de
  perfiles pierde sus respuestas.

## 6. Reproducción

```bash
# A: qué salas ve hoy la PWA desde profile.yaml
python - <<'PY'
import os,yaml
p=os.path.join(os.environ["LOCALAPPDATA"],"hermes","profile.yaml")
d=yaml.safe_load(open(p,encoding="utf8"))
print(list(d["ui_meta"]["hermes-bots-groups"]["rooms"].keys()))
PY

# B: cuántas sesiones de sala hay por perfil
python - <<'PY'
import sqlite3,os
base=os.path.join(os.environ["LOCALAPPDATA"],"hermes","profiles")
for prof in ("brain-local","web-builder","web-auditor"):
    c=sqlite3.connect(f"file:{base}/{prof}/state.db?mode=ro",uri=True)
    print(prof, c.execute("SELECT COUNT(*) FROM sessions WHERE title LIKE 'Group:%'").fetchone()[0])
PY

# C: dónde vive el store del Desktop
grep -o -a "hermes[.]plugin[.]hermes-bots[a-zA-Z0-9_.:-]*" \
  "$APPDATA/hermes/Local Storage/leveldb/MANIFEST-000001" | sort -u
```
