# Prompt para Antigravity — hermes-pwa · Fase 2 (replicación real de las conversaciones de sala)

**Repo:** `C:\Projects\hermes-pwa` · **Baseline:** commit de Fase 1 (o `46ca485` si se autoriza arrancar por acá)
**Commit esperado:** `feat(groups): rebuild room transcripts from state.db (drop hardcoded seeds)`
**Pedido de Juan:** "que se repliquen las conversaciones de los chats, que la conexión sea correcta".
**Recon previo (leer antes de tocar):** `Hermes/Quarantine/hermes-pwa-fase2-recon-fuente-de-verdad-2026-09-28.md`

---

## Objetivo

Que el celular muestre la conversación real de cada sala, traída de la fuente que sí la tiene, en los dos
nodos, sin seeds hardcodeados y sin borrarle la pantalla al usuario cuando una lectura falla.

## Contexto del proyecto (verificado con lecturas reales, no inferido)

Hoy la PWA arma las salas **sólo** desde
`profile.yaml → ui_meta["hermes-bots-groups"].rooms` del nodo que atiende el request
(`src/lib/hermes-fs.ts:12-14`, `src/app/api/groups/route.ts:75-117`), y ese store **no tiene las salas de Juan**:

| Store | Qué es | Estado real medido |
|---|---|---|
| `%LOCALAPPDATA%\hermes\profile.yaml` → `ui_meta["hermes-bots-groups"]` | push parcial del Desktop vía `profiles.configure` | **1 sola sala**: `id:rmuag13gp-5r3kn` (algolab, 54 entradas). Ni `rmugviqw9` ni `rmufxz2ti` ni `rmuli31hi` existen en ningún `profile.yaml` del nodo |
| `<HERMES_HOME>/profiles/<bot>/state.db` (+ `-wal`) | sesiones **de cada bot**, ocultas, tituladas `Group: <roomId> · <threadId>` | Es la única transcripción disponible en disco, pero **no es un log de sala**: en una sesión real hay `assistant 30 / tool 53 / user 1` |
| localStorage del app Electron (`file://` → key `hermes.plugin.hermes-bots.group-chats`) | store canónico del Desktop (catálogo + log en vivo) | Inalcanzable desde la PWA y no sincroniza entre nodos |

Consecuencia: la fuente de verdad alcanzable es `state.db` **del nodo que corre esos bots**, pero hay que
**reconstruir** la sala. Hechos medidos por los tres (censo acordado, `title LIKE 'Group: %'` sobre los 9
`state.db` del nodo PC): **63 sesiones de sala, 60 con `hidden=1`, sólo 3 visibles** — 61 en los perfiles de
bots (algolab 16 + algolab-strategy 15 + brain-local 13 + web-auditor 9 + web-builder 8) **+ 2 en
`HERMES_HOME/state.db` del perfil `default`**, que también es miembro de sala (`default-this-device` en
`rmufxz2ti`) y que un censo limitado a `profiles/*/state.db` se come. Por sala:
`rmuag13gp` 31 · `rmugviqw9` 23 · `rmufxz2ti` 6 · `rmuli31hi` 3. En el nodo **VPS hay 0 sesiones de sala** (8 bots + `default`),
así que para las salas del Desktop el PWA del VPS **obligatoriamente** pide la sala al nodo par; en el nodo
dueño (PC) se reconstruye de `state.db`. Dos avisos que ahorran horas: el censo **por título tiene lag de
minutos** (`session_key`/`chat_id`/`chat_type`/`thread_id`/`origin_json` están en NULL en las 63: la sala y el
thread viven sólo en el string `title`, que se escribe después de crear la fila) → comparar contra un snapshot
congelado, no recontar en vivo; y si el camino de salas pasa por el API de sesiones **no puede llevar el filtro
`hidden`** (60 de 63 caen ahí).

1. En la sesión de cada bot, los turnos de la sala entran como mensajes `user` con este sobre (formato real,
   `profile.yaml`/`state.db` de brain-local, sesión `20260927_195115_70e472`):

   ```
   [Group chat: "<room name>"] You are @<bot>, one participant in a group chat with @a, @b [<node>] and the user.

   New messages in the room since your last turn (oldest first):
     You (user): <texto, puede venir en varias líneas>
     Hermes [100.124.132.48:9119]: <texto>
     ...
   <bloque de reglas de la sala ("what was just said, claim or hand off work…")>
   ```

2. La respuesta del bot es el mensaje `assistant` con `content` no vacío de esa misma sesión
   (verificado: el seed `msg-wb-1` de `src/lib/group-registry.ts:54-62` — "eslint . = 118 problems" — es
   literalmente el último `assistant` de web-auditor en `state.db`, `at 1790550198785`; **sí existió en la sala**).
3. El mismo turno se replica en la sesión de cada miembro → hay que deduplicar.

## Tarea específica

### 1. Nuevo módulo `src/lib/room-store.ts` (server-only)

- `listNodeStores()` → `HERMES_HOME/state.db` + cada `HERMES_HOME/profiles/<dir>/state.db` que exista
  (`HERMES_HOME` ya está exportado en `hermes-fs.ts:5-13`). Excluir `-wal`/`-shm` del listado.
- `readRooms(): RoomRecord[]`:
  - `SELECT id, title, message_count, last_activity_at, profile_name FROM sessions WHERE title LIKE 'Group:%'`
    (incluir `hidden=1`: **todas** las sesiones de sala son ocultas; hay 13 en brain-local, 7 en web-builder,
    8 en web-auditor para `rmugviqw9`, repartidas en 8 threads).
  - Parsear el título con `/^Group:\s*([^\s·]+)\s*·\s*(\S+)$/` — **el separador es `·` (U+00B7) con espacios**.
  - `roomId` → sala; **miembros** = perfiles con ≥1 sesión de ese `roomId` (mapear `profile_name`/dueño del
    archivo a label con el `BOT_METADATA` que ya vive en `app/api/groups/route.ts:9-27`), ordenados por label;
    `name` = labels unidos por `", "` (esto reproduce "Brain Local, Web Builder, Web Auditor").
  - `messageCount` real de la sala = largo del log reconstruido (no `log.length` de `profile.yaml`).
- `readRoomTranscript(roomId): GroupMessageItem[]`:
  - Para cada store, para cada sesión del `roomId`: `SELECT role, content, timestamp FROM messages WHERE session_id=? ORDER BY timestamp`.
  - De los `user`: cortar desde el header `New messages in the room since your last turn (oldest first):` hasta el
    inicio del bloque de reglas (primera línea que empiece con `- Reply with ONE conversational message` /
    `what was just said, claim or hand off work` / `Rules for this room`), y parsear las líneas
    `^\s{2}(.+?)(?:\s\[(.+?)\])?(?:\s\((user)\))?:\s?(.*)$` con continuación por indentación.
    `You (user):` → `from:{kind:"user",name:"You"}`; `Nombre [nodo]:` → `from:{kind:"member",name:nodo,source:nodo}`.
  - De los `assistant` con `content` no vacío → `from:{kind:"member",name:<perfil dueño>,source:"This device"}`.
  - `at` = `Math.round(timestamp * 1000)` (los `timestamp` de `state.db` son epoch **en segundos con decimales**).
  - **Merge** de todas las filas por `at`; **dedupe** por `(from.name, texto normalizado)` dentro de una ventana
    de ±5 s (el mismo turno aparece en N sesiones; el mismo reply puede aparecer 1 sola vez).
  - Ordenar por `at`; `id` estable `sha1(roomId|thread|at|from.name|texto)` para que el cliente no re-renderice.
- **Abrir los SQLite read-only con red**: usar `node:sqlite` (`DatabaseSync`, igual que `src/lib/message-recovery.ts:35`).
  Los datos vivos están en `-wal`: si `open` falla, copiar `state.db` + `-wal` + `-shm` a un tmp del proceso y abrir
  la copia. Cachear el resultado 2 s (`last_activity_at` como clave) para no leer 10 DB por poll de 3.2 s.

### 2. API de salas — **contrato congelado por brain-local, implementar tal cual**

`GET /api/groups` — por sala: `source: "local"|"peer"`, `nodeStatus: "online"|"offline"|"timeout"`,
`messageCount: number|null` (**`null`, nunca `0`, cuando el nodo está offline**: la UI no puede poder leer
"nodo caído" como "sala vacía").

`GET /api/groups/[groupId]/messages` — sólo estos tres casos, y el cliente ramifica **por `code`, nunca por texto**:

| Caso | Respuesta |
|---|---|
| resuelta (aunque esté vacía) | `200 {messages:[…], source:"local"|"peer", node:"pc"|"vps", peerReachable:true}` |
| la sala no existe en ningún nodo | `404 {code:"ROOM_NOT_FOUND"}` |
| el nodo par no responde | `503 {code:"PEER_OFFLINE", node:"pc", lastSeenAt:<epoch>}` |
| responde pero la reconstrucción excede el budget | `504 {code:"PEER_TIMEOUT"}` |

Implementación:

- `src/app/api/groups/route.ts`: reemplazar la lectura de `ui_meta` por el censo de `state.db` local
  (`readRooms()`) **sin filtro `hidden`**, más el censo del par cuando esté configurado y alcanzable.
  Cada sala del nodo OWNER se reconstruye localmente; las salas del Desktop vistas desde el VPS vienen del peer.
- `src/app/api/groups/[groupId]/messages/route.ts`: si la sala existe localmente → reconstruir y `200` con
  `source:"local"`; si no, pedirla al par (`GET <peer>/api/groups/<id>/messages`, timeout 4 s, budget de
  reconstrucción 5 s) y devolver `200` con `source:"peer"`; `404` sólo si ninguno de los dos la tiene.
  **Eliminar** el `200 {messages:[], warning:"Group room not found in local profile"}` actual.
- `src/app/api/groups/[groupId]/chat/route.ts`: al persistir el mensaje del usuario y la respuesta, seguir
  escribiendo en `profile.yaml` bajo `withProfileDocLock` (Fase 1) **pero** sólo como caché local; la lectura
  ya no depende de ese log.
- **Cross-node:** `HERMES_PEER_PWA_URL` + `HERMES_PEER_PWA_TOKEN` (o reusar `[credencial: HERMES_VPS_API_KEY]`)
  en el `.env` de cada nodo. Sin la variable → local-only y `peerReachable:false`, sin excepción no capturada.
  **Ops (B10):** el PWA del PC está caído hoy, así que el celular no ve las salas del Desktop hasta que el par
  esté arriba; con el par caído la PWA del VPS debe mostrar el estado "nodo PC offline" + último snapshot, nunca
  una lista vacía.

### 3. Eliminar los seeds hardcodeados (B3)

- Borrar `CANONICAL_ROOMS` y `ensureCanonicalRoomsInDoc()` de `src/lib/group-registry.ts` (dejar sólo `findRoom`).
- En `readRooms()` ignorar salas cuyo log provenga del seed: la sala real de `rmugviqw9` debe salir de `state.db`.
- **Migración única:** al arrancar, borrar de `ui_meta["hermes-bots-groups"].rooms` las entradas cuyo `log`
  matchee exactamente los `initialLog` removidos, para que el VPS no siga mostrando el mensaje fantasma.

### 4. Cliente: no borrar la pantalla (B4)

- `src/lib/api.ts:213-228` (`fetchGroupMessages`): quitar `catch → return []` y el `if (res.status === 404) return []`.
  Devolver un resultado tipado `{ok:true, messages, source, peerReachable} | {ok:false, code:"ROOM_NOT_FOUND"|"PEER_OFFLINE"|"PEER_TIMEOUT"|"NETWORK", node?, lastSeenAt?}`.
- `src/components/GroupChatView.tsx:68-96`: eliminar el criterio `list.length !== currentList.length`
  (línea 79) y reemplazarlo por merge por `id`. Reglas de render, ramificando por `code`:
  `200` → reemplaza/mergea la lista; `404 ROOM_NOT_FOUND` → estado vacío explícito ("sala inexistente"), sin
  inventar contenido; `503 PEER_OFFLINE` / `504 PEER_TIMEOUT` / error de red → **no tocar la lista**, mostrar
  banner "nodo PC offline — último snapshot (hh:mm)" con `lastSeenAt`. El polling de 3.2 s debe seguir corriendo.

## Archivos a tocar

nuevo `src/lib/room-store.ts` · `src/lib/group-registry.ts` · `src/lib/api.ts` ·
`src/lib/types.ts` (si hace falta `RoomRecord`) · `src/app/api/groups/route.ts` ·
`src/app/api/groups/[groupId]/messages/route.ts` · `src/app/api/groups/[groupId]/chat/route.ts` ·
`src/components/GroupChatView.tsx` · `src/components/GroupList.tsx` (contador de mensajes real) ·
`.env.local` de cada nodo (`HERMES_PEER_PWA_URL` / `HERMES_PEER_PWA_TOKEN`).

## Restricciones

- **No escribir** en `ui_meta` de los perfiles de bots para logs de sala: el path de escritura del room log
  hacia `profile.yaml` no escala (cap de 64 KB en `ui_meta`) y es lo que hoy produce logs fantasma.
- **No tocar** el ruteo de respuesta de bots (`PC_BOTS` / `NODE_NAME` / gateways `:8642`): funciona.
- No leer el localStorage del Electron (opaco, comprimido) ni pedirle nada al Desktop.
- No agregar `better-sqlite3` ni dependencias nativas: usar `node:sqlite`.
- No mostrar tool calls ni mensajes `system`/`tool` en la sala: el usuario ve turnos y respuestas.
- Sin secretos en el repo; el peer token va por env.

## Criterios de aceptación

Antigravity debe **pegar en el mensaje de cierre** la salida real de:

1. `tsc --noEmit` = 0 y `npm run build` = OK.
2. Tabla por sala (script temporal, no commiteado) con columnas
   `roomId | threads | miembros | log reconstruido (n) | primeros/últimos 2 timestamps ISO` para las 4 salas
   conocidas, contra el censo congelado del nodo dueño (snapshot a las 18:15, no recontado en vivo):
   `rmugviqw9-6zez7` 23 sesiones (brain-local 8 + web-builder 7 + web-auditor 8) · `rmufxz2ti-w6sk5` 6
   (brain-local 4 + `default` 2) · `rmuli31hi-inptr` 3 · `rmuag13gp-5r3kn` 31 (algolab 16 + algolab-strategy 15).
   El número reconstruido **no puede ser menor** que la cantidad de turnos únicos (`user` parseados + `assistant`
   con contenido, deduplicados) de esas sesiones; si es menor, el parseo del sobre está mal.
3. `GET /api/groups` → cada sala con `messageCount` = largo real del log, `source` y `nodeStatus`, y **ninguna**
   sala con el log del seed.
4. `GET /api/groups/rmugviqw9-6zez7/messages` → `200` con **204 turnos** (número de la auditoría) y las 3 ids del
   baseline del VPS (`msg-wb-1`, `usr_1790632373669_fm47n`, `bot_1790632380284_p90ph`) **fuera** del log.
5. Sala inexistente → `404 {code:"ROOM_NOT_FOUND"}` (nunca `200 {messages:[]}`).
6. Prueba de corte: con el gateway del PC caído, `GET /api/groups` sigue devolviendo las salas locales con
   `nodeStatus:"offline"` y `messageCount:null`, y `/api/groups/<id>/messages` de una sala del PC → `503 {code:"PEER_OFFLINE"}`;
   el cliente **conserva el snapshot** con el banner y no vacía la lista. Sin excepción no capturada ni 500.
7. Un `profile.yaml` de prueba con 0 salas en `ui_meta` sigue mostrando las salas reales (prueba de que la
   fuente dejó de ser `ui_meta`), y el censo incluye `HERMES_HOME/state.db` (sin eso, `rmufxz2ti` pierde las 2
   sesiones del miembro `default`).
8. `git diff` no toca `src/app/api/chat/route.ts` ni el flujo 1-a-1 de bots.

Estos tres son los **criterios de cierre de Fase 2** fijados con @web-auditor; sin los tres no se cierra:
`rmugviqw9` reconstruida con sus 204 turnos y las 3 ids del baseline fuera · sala desconocida → `404` con `code`
y nunca `200 []` · corte con el par caído → `503` y el cliente conservando el snapshot.
