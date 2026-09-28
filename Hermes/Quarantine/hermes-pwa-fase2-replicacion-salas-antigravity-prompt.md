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

Consecuencia: la fuente de verdad alcanzable es `state.db`, pero hay que **reconstruir** la sala:

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

### 2. API de salas

- `src/app/api/groups/route.ts`: reemplazar la lectura de `ui_meta` por `readRooms()`. Aceptar
  `?node=local|vps|all` (**default: `all`**) y, cuando el par esté configurado, pedir
  `GET <peer>/api/groups?node=<origin>` con el token de servicio y mergear por `roomId` (gana el log más largo).
- `src/app/api/groups/[groupId]/messages/route.ts`: devolver el log reconstruido con `?node=`. Sala
  desconocida → **404** `{error:"Room not found"}` (nunca `200 {messages:[]}`), ver Fase 1 punto 5.
- `src/app/api/groups/[groupId]/chat/route.ts`: al persistir el mensaje del usuario y la respuesta, seguir
  escribiendo en `profile.yaml` bajo `withProfileDocLock` (Fase 1) **pero** marcar la sala en
  `ui_meta["hermes-bots-groups"].rooms` sólo como caché local; la lectura ya no depende de ese log.
- **Cross-node:** agregar `HERMES_PEER_PWA_URL` (+ `HERMES_PEER_PWA_TOKEN`, o reusar
  `[credencial: HERMES_VPS_API_KEY]`) al `.env` de cada nodo; sin esa variable el endpoint funciona local-only
  y devuelve `peerConfigured:false` en la respuesta. **Nota de ops (B10):** el PWA del PC está caído, y hoy el
  celular depende sólo del VPS; sin el par arriba, las salas del otro nodo no aparecen → avisar por log, no fallar.

### 3. Eliminar los seeds hardcodeados (B3)

- Borrar `CANONICAL_ROOMS` y `ensureCanonicalRoomsInDoc()` de `src/lib/group-registry.ts` (dejar sólo `findRoom`).
- En `readRooms()` ignorar salas cuyo log provenga del seed: la sala real de `rmugviqw9` debe salir de `state.db`.
- **Migración única:** al arrancar, borrar de `ui_meta["hermes-bots-groups"].rooms` las entradas cuyo `log`
  matchee exactamente los `initialLog` removidos, para que el VPS no siga mostrando el mensaje fantasma.

### 4. Cliente: no borrar la pantalla (B4)

- `src/lib/api.ts:213-228` (`fetchGroupMessages`): quitar `catch → return []`. Propagar el error y
  distinguir `404` (sala inexistente → estado vacío explícito, con mensaje) de error de red/servidor
  (→ conservar la última lista buena).
- `src/components/GroupChatView.tsx:68-96`: eliminar el criterio `list.length !== currentList.length`
  (línea 79) y reemplazarlo por merge por `id`: sólo reemplazar cuando el conjunto de `id` cambia, y jamás
  escribir una lista vacía si la respuesta falló. Mostrar banner "sin conexión, mostrando último estado".

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
   `roomId | threads | miembros | log reconstruido (n) | primeros/últimos 2 timestamps ISO` para las 3 salas
   conocidas, y comparación contra el baseline medido en `state.db`:
   `rmugviqw9-6zez7` (23 sesiones: brain-local 8, web-builder 7, web-auditor 8) · `rmufxz2ti-w6sk5` (6 sesiones) ·
   `rmuag13gp-5r3kn` (31 sesiones: algolab 16, algolab-strategy 15).
   El número reconstruido **no puede ser menor** que la cantidad de turnos únicos (`user` parseados + `assistant`
   con contenido, deduplicados) de esas sesiones; si es menor, el parseo del sobre está mal.
3. `GET /api/groups` → cada sala con `messageCount` = largo real del log, y **ninguna** sala con el log del seed.
4. `GET /api/groups/rmugviqw9-6zez7/messages` incluye los mensajes de hoy (los que ya están en `state.db`), no un
   único mensaje.
5. Sala inexistente → `404` (no `200 {messages:[]}`), y el cliente muestra "no se pudo cargar" sin vaciar la lista.
6. Con el gateway del otro nodo apagado, `/api/groups` sigue devolviendo las salas locales y
   `peerConfigured:false`; no hay excepción no capturada ni 500.
7. Un `profile.yaml` de prueba con 0 salas en `ui_meta` sigue mostrando las 3 salas reales (prueba de que la
   fuente dejó de ser `ui_meta`).
8. `git diff` no toca `src/app/api/chat/route.ts` ni el flujo 1-a-1 de bots.
