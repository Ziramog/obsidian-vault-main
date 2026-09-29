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

### 0. Techo real de esta fase (esto decide el criterio de cierre)

El log canónico de una sala vive **sólo** en el store C (localStorage del Desktop) y **ningún componente
server-side lo puede leer**. Reconstruir desde `state.db` (store B) **no es equivalente**: el parser estricto de
web-auditor da `102 / 96 / 475 / 15` contra `115 / 172 / 327 / 10` del store — infla porque los mensajes se citan
entre sí (las líneas `  Nombre [nodo]: texto` reaparecen dentro de otros mensajes) y desinfla porque un bot que
entra tarde no tiene envoltorio de los mensajes viejos. Caso vivo: `rmuli31hi`, store 10 = lo que se ve en
pantalla. Además el store guarda **76 mappings de sesión contra 63 filas** en `state.db` (ids huérfanos): el peer
fetch tiene que tolerarlos y **no usarlos para contar**.

Por eso esta fase entrega **reconstrucción** y el endpoint debe declararlo rotulado:
`source:"reconstructed"`. Nunca reportar el número reconstruido como si fuera el log de la sala.

La igualdad con el store (`115/172/327/10`) es criterio de **Fase 3**, y requiere un puente server-visible del log
del Desktop. La vía natural ya existe: el plugin ya empuja el log vía `profiles.configure` → `ui_meta`, pero hoy
deja **1 sola sala con 54 entradas de 327** en el `profile.yaml` (consistente con el cap de 64 KB de `ui_meta`,
que viaja en cada `profiles.list`); la otra vía, leer el LevelDB del Electron, implica dependencia de snappy y
acoplarse a la key interna del app — no recomendada. Dejar el código preparado para que, si mañana aparece
`source:"store"`, se prefiera sin refactor.


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
  **Ops (B10):** el PWA del PC **no está caído** — corre en `:3111` (:3111 PID 28792) y `:3112` (PID 7160), y el
  que no escucha es el `:3000` documentado por el `.bat`/README/funnel, de ahí el 502. `HERMES_PEER_PWA_URL` tiene
  que apuntar al puerto real del par; con el par inalcanzable, el estado es "nodo PC offline" + último snapshot,
  nunca lista vacía.
- **Quién mide qué (topología, verificada el 2026-09-28 por el propio nodo VPS):** al celular lo sirve el
  **VPS** — `pm2 hermes-pwa`, cwd `/home/hermes/hermes-pwa`, `main` @ `46ca485`, en `:3000` detrás de
  `tailscale serve` (ahí `:3111`/`:3112` no existen y `:3000` **es** el deploy, no un puerto libre). El rollout en
  el VPS lo hace ese nodo con el SHA cerrado (fetch + checkout del SHA, build con el Node pinneado,
  `pm2 restart --update-env`); el agente **no** toca `pm2` ni el `:3000` del VPS. En la PC, las dos instancias
  viejas de `:3111` (:3111 PID 28792) y `:3112` (PID 7160) no se apagan. Los criterios se miden **en la PWA del
  VPS** (la que ve el celular), salvo el 2 y el 7, que salen del censo local del nodo dueño (PC).

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
4. `GET /api/groups/rmugviqw9-6zez7/messages` → `200` con `source:"reconstructed"`, orden correcto y las 3 ids del
   baseline del VPS (`msg-wb-1`, `usr_1790632373669_fm47n`, `bot_1790632380284_p90ph`) **fuera** del log.
   **El baseline no se hardcodea: se deriva en la misma corrida.** Antes de medir, correr el censo contra `state.db`
   del nodo dueño **en ese momento** y publicar los dos números (censos `n` de turnos únicos por sala + largo
   reconstruido). La foto de las 18:15 (23/6/3/31 sesiones) y los conteos viejos (`102 / 96 / 475 / 15`) quedan
   **sólo como referencia**: las salas activas crecen (esta sala pasó de 15 a 46 turnos en una tarde), así que
   comparar contra un número congelado da falso rojo y tienta a "pasar" el test por la vía equivocada. El rango
   ±10% se aplica **sólo** entre mediciones contemporáneas (censo y reconstrucción del mismo momento).
   El log reconstruido **no puede leer** el store del Desktop: si aparece el número del store (`115/172/327/10`),
   el agente leyó el LevelDB del Electron y hay que revisar cómo.
   **Ojo con la inflación por citas:** un mensaje citado dentro de otro (los bots se citan entre sí) es una cita,
   no un turno nuevo; el conteo tiene que excluirlas o el total queda por encima del censo.
5. Sala inexistente → `404 {code:"ROOM_NOT_FOUND"}` (nunca `200 {messages:[]}`).
6. Prueba de corte: con el gateway del PC caído, `GET /api/groups` sigue devolviendo las salas locales con
   `nodeStatus:"offline"` y `messageCount:null`, y `/api/groups/<id>/messages` de una sala del PC → `503 {code:"PEER_OFFLINE"}`;
   el cliente **conserva el snapshot** con el banner y no vacía la lista. Sin excepción no capturada ni 500.
7. Un `profile.yaml` de prueba con 0 salas en `ui_meta` sigue mostrando las salas reales (prueba de que la
   fuente dejó de ser `ui_meta`), y el censo incluye `HERMES_HOME/state.db` (sin eso, `rmufxz2ti` pierde las 2
   sesiones del miembro `default`).
8. `git diff` no toca `src/app/api/chat/route.ts` ni el flujo 1-a-1 de bots.
9. **El GET no escribe (incluido el home sin migrar).** `GET /api/groups` y los GET de sala deben dejar
   `profile.yaml` **idéntico al byte** (hash antes/después) en **dos** homes: el real y uno que **todavía tenga los
   ids semilla** (`msg-wb-1` / `msg-algo-1`) en `ui_meta`. Motivo medido: en `ba48686` quedó
   `if (doc && migrateSeedRooms(doc)) saveProfileDoc(doc);` en el camino de lectura
   (`app/api/groups/route.ts:70-73`, `app/api/groups/[groupId]/messages/route.ts:15-18`) — mismo defecto de clase
   que B3 (un GET que persiste), y la verificación que dio "hash igual" lo hizo sobre un home **ya migrado**. La
   limpieza de los ids semilla va en un **script de migración / arranque**, nunca en un GET; y el escritor sigue
   siendo el serializador del PWA sobre un archivo que también escriben Desktop y gateway (además de clobbear el
   espejo, roza el lost-update de B5).
10. **Escribir en una sala que sólo existe en `state.db`.** `POST /api/groups/<sala>/chat` tiene que resolver la
    sala por la **misma** fuente que `/messages`; hoy `/chat` la busca en `ui_meta["hermes-bots-groups"]`
    (`chat/route.ts:40-44`), así que para `rmugviqw9`/`rmufxz2ti`/`rmuli31hi` (fuera del espejo) contesta
    `404 {"error":"Group room not found"}`: **la historia se lee pero no se puede contestar**, que es justo el caso
    de uso del celular. Y el 404 de `/chat` (y el `error` del SSE de `chat/route.ts:150`) tiene que llevar
    `code:"ROOM_NOT_FOUND"` igual que `/messages`: el contrato se aplica a las dos rutas, no a una.
11. **Sin artefactos de compactación como mensajes.** *(Corregido con la medición de @web-auditor sobre `ba48686`:
no son citas internas, son **mensajes propios cuyo texto es el blob de compactación** — 6 en esta sala, 2 en
`rmugviqw9`, 2 en `rmuag13gp`, 0 en `rmufxz2ti`.)* El transcript no puede exponerlos. Filtro en **dos** niveles:
   - **Estructural** (dentro del sobre): sólo producen mensaje las líneas que matchean `^  <nombre> [<nodo>]: <texto>`
     o `^  You (user): <texto>`; todo bloque entre corchetes en línea propia se descarta.
   - **Por contenido (el que faltaba y es el que atrapa lo que hoy se ve):** un mensaje cuyo texto **empiece con**
     `[member-quoted PRIOR CONTEXT` o **contenga** `[END OF PRIOR CONTEXT` es artefacto → fuera del payload **y** del
     `messageCount`. También `[CONTEXT COMPACTION — …]` y `[OUT-OF-BAND USER MESSAGE — …]`.
   Criterio para @web-auditor: 0 apariciones de `PRIOR CONTEXT` / `COMPACTION` / `member-quoted` en el transcript de
   las 4 salas. **Nota de alcance:** el origen está en `state.db` (el registro de la propia sesión del bot), no en el
   parser, así que esto es un parche aguas abajo: la corrección de raíz (no registrar/publicar los scaffolds de
   compactación como contenido de mensaje) queda anotada para Fase 3 como decisión de arquitectura, no se arregla acá.
12. **El escritor del PWA no puede perder claves del doc.** Para **cada** camino de escritura del PWA, diff del
    **conjunto de claves** de `profile.yaml` (no sólo del hash) antes/después: ninguna clave existente puede
    desaparecer. Motivo medido: el archivo que escribió el PWA a las 20:52 son **53.122 b con 3 salas** (2 vacías)
    contra los **55.551 b con 1 sala** de las 19:00 **con el mismo log de 54 entradas** — menos contenido real y 2,4 KB
    menos de archivo. Hasta medirlo, el PWA no debe ser escritor de un archivo compartido con el Desktop y el gateway:
    si no se puede garantizar el round-trip completo, la escritura se elimina (el GET deja de escribir, criterio 9).
13. **Servicio del par: `HERMES_HOME` fijado por unidad + health honesto.** El listener del par (PC) tiene que
    **fijar `HERMES_HOME` en su unidad/servicio**, nunca heredarlo de la shell. Medido: lanzado sin él (heredando
    `…\profiles\brain-local`) **no falla y miente**: sirve **3 salas en vez de 4** (sin `rmuag13gp`), `rmugviqw9` con
    **110 mensajes en vez de 207** y `/api/health` con **`profileCount:0` y `ok:true`**. Y el health no puede quedar
    verde sin datos: si `PROFILES_DIR` no existe o `profileCount` es 0 con `profileYaml` ausente, la respuesta es
    **`ok:false`** con el motivo y el path resuelto (misma clase que el health que probaba `/v1/models`).
14. **La etiqueta `node` del peer se deriva de la config y se prueba en los dos sentidos.** Hoy está hardcodeada
    (`messages/route.ts:29` `node:"pc"`, `:52` `node:"vps"`, `:64` `node:"pc"`) y como el cliente **rutea por ese
    campo** (`fetchSessions`/`createSession`/`sendMessage`), **en el VPS queda invertida**: el celular etiquetaría
    como `vps` una sala y una sesión que viven en la PC. `node` = identidad del **nodo dueño real** derivada de la
    config (`HERMES_NODE_IDENTITY`/`HERMES_NODE_NAME`), y el cliente resuelve `node → URL` con un mapa de config, no
    con literales. El test corre **en los dos nodos**, no sólo en la PC.
15. **El presupuesto del peer se deriva del p95 medido, no del arranque en frío.** Medido en el hop que usa el
    celular (VPS → PC `:3300`): `9,71 s / 9,60 s / 0,83 s / 0,83 s` en `/api/groups` y `10,51 s / 1,65 s / 10,61 s` en
    mensajes — o sea **el ~10 s reaparece intercalado después de llamadas de 0,8-1,9 s** (en la muestra acumulada,
    **6 de 10 llamadas por encima del presupuesto**, con un pico de 11,16 s), no sólo en el primer hit. Con los topes hardcodeados de `groups/route.ts:91` (**4.000 ms**) y
    `messages/route.ts:40` (**5.000 ms**) el celular va a mostrar `PEER_OFFLINE`/`PEER_TIMEOUT` **intermitente**.
    Se pide: presupuesto derivado del **p95 medido** (~10,6 s) o **caché con TTL** en el par, y test de aceptación
    con **N llamadas consecutivas sin fallos** (≥9, la muestra medida) — "una llamada pasa" no firma nada.
16. **El par escucha en la interfaz del tailnet, no en loopback.** Con bind a `127.0.0.1`/`localhost` el fetch del
    otro nodo da `ECONNREFUSED` y el celular ve `PEER_OFFLINE` con el listener "andando". El bind es la IP del tailnet
    (verificado: `100.105.0.23:3300` en `netstat`, PID 63060) y `HERMES_PEER_PWA_URL` se escribe con **IP**, no con
    nombre de host. Prohibido tocar `:3000`, `:3111`, `:3112` ni `:8642`.
17. **Configuración del par: una variable, cero secretos nuevos.** `HERMES_PEER_PWA_TOKEN` cae a
    `HERMES_VPS_API_KEY`, y con la inversión de nombres cada nodo ya guarda la key del otro (PC 21/43, VPS 43/21);
    `HERMES_GATEWAY_URL` y `HERMES_NODE_IDENTITY` tienen fallback a `HERMES_API_URL`/`HERMES_NODE_NAME`. La única sin
    default es **`HERMES_PEER_PWA_URL`**: una línea por nodo (PC → VPS `:3000`, VPS → PC `<ip-tailnet>:3300`).
    **Prohibido** agregar secretos nuevos o copiar valores entre nodos. Y el camino ya está medido de punta a punta:
    un peer fetch real PC → VPS autenticó correctamente con esos fallbacks (el VPS devolvió su 404 sin `code` y el par
    lo normalizó a `404 {code:"ROOM_NOT_FOUND"}`).
18. **Los errores del upstream se normalizan a `code`.** El gateway de un nodo responde
    `{"error":"Upstream error"}` **sin `code`** cuando se pide un perfil que no vive en ese nodo (medido en el VPS con
    `profile=algolab`). El PWA no puede propagar un error sin `code`: lo mapea a un `code` propio (perfil/nodo mal
    emparejado ≠ nodo caído ≠ sala inexistente), porque el cliente ramifica por `code` y con el texto crudo la UI
    vuelve a "lista vacía".
19. **Los remitentes: tres formas legítimas y ninguna inventada (la aserción va sobre el payload).**
    Medido: hasta el **40 %** de los turnos servidos en `rmugviqw9` tienen autor fuera del roster (`"model"`,
    `headers`, `body`, `apikey`, `"state_sha256"`, fragmentos de código y listas) — en el celular eso son autores que
    no existen, y **también inflan el `messageCount`**. Las tres formas que **sí** son remitente:
    1. `^  <Nombre> \[<nodo>\]: ` — `<nodo>` con forma válida (`This device` | `PC Local` | `IPv4:port`). Es la que
       deja pasar al nodo remoto (`Hermes [100.124.132.48:9119]`, 30 turnos reales en `rmufxz2ti`).
    2. `^  <Nombre> (you) \[<nodo>\]: ` — **turno propio de ese bot**, nunca filtrado: sin esta forma se descarta la
       mayoría del contenido de la sala (247 líneas en `rmuag13gp`, 27 en `rmuli31hi` = un tercio de la sala).
    3. `^  <Nombre>: ` **sin** etiqueta de nodo — legítima **sólo** si ese nombre ya apareció **etiquetado en esa
       misma sala** (compuerta de roster derivado del propio corpus). Sin la compuerta entra basura de depuración
       (`todos: isOnline=True, nodeLabel='☁️ VPS'…`); con ella entran `Algolab: …` ×24 y sale el volcado.
    El nombre no puede contener `"`, backtick, `(`, `)`, `=`, `,`, `?` ni arrancar con `-`: eso mata las líneas de
    lista (`--long`, `--máximo`, `--**total`) y de código, que son cuerpo citado. **Ni el espejo ni el store son
    fuente del roster** (medido: el espejo tiene 1 sala, con `members` sólo locales; el store es localStorage del
    Electron, inalcanzable): el roster se deriva del **corpus de esa sala** ∪ censo ∪ `You`.
    **La aserción va sobre el payload, nunca sobre la regex:** el **100 %** de los turnos servidos tiene
    `from.name ∈ roster ∪ {You}`, contando **turnos atribuidos**. Un criterio escrito como "0 líneas que no matchean
    la regex" pasa dejando fantasmas adentro (medido: `53 vs 83` y `6 vs 15` según cómo se cuente) y, al revés,
    empuja a recortar contenido legítimo. Esperados post-fix, medidos: **808 / 124 / 118 / 53** para
    `rmuag13gp / rmugviqw9 / rmufxz2ti / rmuli31hi` — declarados explícitos para que el fix no se autosabotee
    conservando fantasmas con tal de no bajar el número.
20. **Sala presente en los dos nodos: unión con dedup, no precedencia.** Ningún nodo es superconjunto del otro: el
    corpus del PC en esta sala arranca **17:57:35** (2 h 52 min antes de la única sesión del VPS, 20:49:15) y el del
    VPS en `rmufxz2ti` llega hasta **09-28 00:11:57** (55 min después del PC, que corta en 09-27 23:16). Cualquier
    regla de precedencia ("gana el local" o "gana el dueño de los bots") **pierde contenido medible**, así que donde
    los dos nodos tienen corpus el resultado es **`source:"merged"`**; `source:"local"` sólo cuando el otro nodo no
    tiene esa sala.
    **La clave de dedup NO puede incluir `at` — medido, y era mi error.** El mismo texto llega con timestamp distinto
    según quién lo reconstruya: `2,377 s`, `2,217 s` y **`2.201 s` (36 min 41 s)** de delta entre el `state.db` de un
    nodo y el payload del par, porque el par observa los envoltorios **cuando corre su propia sesión**, así que su
    `at` es una hora de *entrega*, no de emisión (2 s con su bot activo, 36 min sin actividad). Y los `id` no salvan
    la identidad: el par emite ids de 22 hex que **no existen** en el store del otro nodo. Con `(nombre, at, texto)`
    exacto el merge **duplica en vez de fusionar**.
    **Clave correcta: multiset por `(nombre, texto normalizado)`** (con ordinal de ocurrencia, para no colapsar dos
    envíos legítimamente idénticos). Hoy la clave es **inyectiva** en las cuatro salas (998/207/133/60 turnos, **0
    colisiones**, repetición máxima 1), así que el ordinal sólo se ejercita con un test **sintético**; lo que sí es
    aserción estructural es que **tras la fusión no haya ningún par `(nombre, texto)` repetido** (distintos del merge
    == distintos de la unión).
    **`at` no sirve para identidad, ni para orden, ni como timestamp — y no sale del store.** Los valores que el
    payload repite 3 / 52 / 70 veces (`1790639791.454`, `1790481940.471`, `1790480669.478`) dan **0 filas** con ese
    timestamp en las 63 sesiones de sala de un nodo y en las ~98k filas del otro: la reconstrucción lo **deriva**. Es
    la hora de **entrega del sobre** (2,2 s con el bot activo, 37 min sin actividad) y dentro de un mismo payload llega
    a estar compartido por **70 turnos** (998 turnos / 649 timestamps en `rmuag13gp`), así que ordenar por él desordena
    70 turnos de golpe.
    **Orden = `rowid` del sobre + índice de la línea dentro del sobre**, y la unión ordena por
    (`started_at` de la sesión, `rowid` del sobre, índice de línea) con **el nodo como clave externa**. **Timestamp
    canónico = el de la fila del sobre** (el único honesto y disponible): 70 turnos con el mismo timestamp dejan de
    ser un defecto y pasan a ser el resultado esperado de 70 líneas leídas del mismo sobre — medido en el otro nodo,
    una sesión con **10 sobres y 57 líneas de remitente** (13/10/12/2/4/2/2/8/2/2), cada sobre con un solo timestamp.
    **Aserciones estructurales, sólo dos:** (a) ningún par `(nombre, texto)` repetido tras la fusión; (b) **0
    inversiones entre filas de sobre** (alcanzable y estricto: da 0 por construcción). La monotonía del timestamp
    sobre la mitad completa **no es aserción, es métrica que se reporta** — hoy **13 de 63** mitades tienen
    inversiones y **9 de 63** timestamps repetidos antes de tocar nada, así que exigir 0 ahí obligaría al agente a
    violar el criterio o a recortar datos.
    **Unidad fijada antes de comparar:** se cuentan **eventos de envoltorio** (líneas de remitente en rol `user`),
    nunca filas de `state.db` — en la sesión del VPS de esta sala, 86 filas = 7 `user` + 37 `assistant` + 42 `tool`,
    o sea contar filas infla entre **5× y 12×**.
    **Test que discrimina (más barato que un conteo):** el transcript que ve el celular tiene que contener **un evento
    en el tramo que sólo un nodo tiene** — en esta sala alguno entre **17:57:35 y 20:49:15** (sólo PC); en
    `rmufxz2ti` alguno entre **09-27 23:16 y 09-28 00:11:57** (sólo VPS). Un `merged` que no traiga esos dos tramos
    no fusionó nada, aunque el total dé verde.
    **Test de no-duplicación, con el caso real:** el par **ya emite 7 eventos `hermes`** en esta sala, así que el
    `merged` no puede mostrarlos dos veces — se contrasta el **conteo por `(nombre, texto)`** contra el de cada nodo
    por separado (ningún texto puede aparecer más veces que el máximo de las dos mitades).
21. **"Veo los bots pero no puedo hablarles" — el chat rutea por `body.node`, no por el perfil (medido en el código
    que hoy corre en el celular).** `src/app/api/chat/route.ts:19-20` (`3186a37`): `isVps = body.node === "vps" ||
    x-hermes-node === "vps"` y `targetBaseUrl = isVps ? HERMES_VPS_URL : HERMES_API_URL` — o sea **sin `node` en el
    body la petición va al gateway local**, y ahí un perfil que vive en el otro nodo (`brain-local`, `web-builder`,
    `web-auditor`, `algolab`, `algolab-strategy`, `trading-performance`, `pcbrain`, `algolab-darwin`, `omh-test`)
    devuelve **`404 "Unknown or unconfigured profile"`**. No existe ningún mapa perfil→nodo: la lista de bots se
    construye con los dos nodos, pero el envío no sabe a cuál ir. Pedido: **(a)** resolver el nodo **desde el perfil**
    (mapa perfil→nodo derivado de la config/censo, no de un campo del cliente), con el `node` del body sólo como
    desempate explícito; **(b)** el mismo criterio aplica a `/api/chat`, no sólo a salas y sesiones; **(c)** error con
    `code` propio cuando el perfil no vive en ningún nodo alcanzable (≠ "no autorizado" ≠ "nodo caído"). Sin esto, el
    rollout puede dejar las salas andando y **el envío a 9 de los 17 bots igual roto**.
    **Spec final acordada (A.1–A.4) — el ruteo sale de una medición, no de una etiqueta ni de un campo del cliente:**
    - **A.1** agregar **`?scope=local`** a `/api/profiles`: devuelve **sólo lo que este nodo puede atender**. Hoy no
      existe: las cinco variantes probadas en la PC y las tres en el VPS (`""`, `?scope=local`, `?node=local`,
      `?local=1`, `?peer=0`, `?node=pc`) devuelven **siempre los 17 nombres agregados**.
    - **A.2** la tabla perfil→nodo se arma con **dos llamadas** (local + par) y se cachea con **TTL ≥ 60 s**. Si el par
      falla, sus perfiles quedan **desconocidos, nunca ausentes** (hoy `sessionCount: 0` con `catch` silencioso dice
      "existe pero sin datos" y se lee igual que "no existe").
    - **A.3** el sondeo por perfil queda como **respaldo**, preguntando a **los dos nodos**: uno solo **no discrimina** —
      medido: desde la PC `brain-local` → 200 y `rws` → 404; desde el VPS exactamente al revés. El mismo 404 sirve
      para "vive en el otro nodo" y para "no existe", y encima responde en ~0,6 s, así que el error no se nota.
    - **A.4** los **hosts se resuelven desde el env del nodo que ejecuta** (`HERMES_VPS_URL` está invertido según quién
      pregunta, igual que `HERMES_VPS_URL` vs `HERMES_API_URL`), **jamás** desde el `node=` del cliente: si no, el fix
      arregla un sentido y rompe el otro.
    La resolución de nodo por dato del cliente **no son tres rutas: son 6 sitios en 4 archivos** (medido con grep
    sobre la rama) + 1 del cliente — el fix es **una sola función de ruteo** usada por todos, no seis parches:
    `app/api/chat/route.ts:19` (`body.node`), `app/api/sessions/route.ts:15` (POST) y `:56` (GET, `?node=`),
    `app/api/sessions/[sessionId]/route.ts:18` y `:56`, `app/api/sessions/[sessionId]/messages/route.ts:18`; del lado
    cliente, `lib/api.ts:153` (`if (node) body.node = node`). **Criterio de aceptación por grep:** no debe quedar
    ninguna coincidencia de `node === "vps"`, `body.node`, `searchParams.get("node")` ni `x-hermes-node` decidiendo el
    gateway en `src/app/api/**`; el test de los dos sentidos corre en **las cuatro rutas**, no sólo en el chat.
    **Por qué no sirve la etiqueta que la app ya pinta:** `profiles/route.ts:43-44`
    define `PC_BOTS` y `VPS_BOTS` **hardcodeados** y `:146` elige la lista del par con
    `NODE_NAME === "vps" ? PC_BOTS : VPS_BOTS`; lo que sí se mide después es `sessionCount` (`:108`/`:165`, con
    `catch → 0`). Rutear por esa etiqueta sería mudar el mismo defecto de clase que ya matamos con `CANONICAL_ROOMS`
    (B3): una lista que se desincroniza de la realidad y no avisa. El ruteo sale de la **medición** — el mismo probe
    por perfil que ya existe — con las dos listas a lo sumo como pista inicial, y el mapa **cacheado con TTL** (las
    llamadas al par medidas llegan a 11 s, criterio 15).
    **Dos fallos que hoy se ven iguales y no lo son:** *el perfil no vive en ese nodo* (el nodo contesta) ≠ *el nodo es
    inalcanzable* (el probe falla y queda `sessionCount: 0`, la misma mentira de B7). Van con **`code` distintos**,
    porque el cliente decide cosas distintas con cada uno.

22. **El ruteo del commit 4 se llama a sí mismo por HTTP a un puerto adivinado (verificado en el código de
    `97104fd`; es el #5 de la auditoría externa y es correcto).** `src/lib/routing.ts`: la mitad local de la tabla sale
    de `fetch(\`http://localhost:${process.env.PORT || 3000}/api/profiles?scope=local\`)`. **El puerto nunca está en
    `PORT`**: los dos nodos arrancan con flag (`next start -H <ip> -p 3300`), así que la autollamada va a **3000**.
    Hay **dos variantes del mismo defecto** y las dos hay que cubrir:
    - **(i) `:3000` vacío** → la llamada entra en `catch (err) {}` **silencioso**, la mitad local de la caché queda
      **vacía** y se cree verdadera **60 s** (TTL de `profileCacheTimestamp`).
    - **(ii) `:3000` ocupado por un proceso ajeno** — es el estado **medido hoy**: hay un `next start` sin `-p`
      (PID 61184, arrancado 08:11, anterior al commit 4) escuchando en `0.0.0.0:3000`; la autollamada **contesta**, y
      por eso **el defecto es latente, no activo** (una sonda de `GET :3000/api/profiles?scope=local` da **200**).
      Pero contesta **con otra verdad que la del servidor que atiende**: misma consulta al proceso ajeno →
      `source:"reconstructed"`, `peerReachable:false`, **205** turnos; a un servidor fresco con el build del commit 4 →
      `source:"merged"`, `peerReachable:true`, **208**. Y como `PROFILES_DIR` sale de `HERMES_HOME`, el proceso ajeno
      puede además estar respondiendo por **otro home** (la trampa del `HERMES_HOME` heredado, ahora del otro lado del
      hop).
    **La corrección que va al prompt es la de la variante latente**, no la de "está vacío": *la autollamada funciona
    porque un proceso ajeno y anterior ocupa `:3000`; el defecto es que la fuente de verdad del ruteo es un hop HTTP a
    un puerto adivinado, y por eso el arreglo no depende de que eso siga siendo cierto.*
    **Punto exacto de extracción (verificado):** `app/api/profiles/route.ts` **ya** arma la lista local **en proceso** —
    `:47-48` (`scope === "local"`) y `:68-126` (recorre `PROFILES_DIR` de este nodo y arma `profiles`); el `fetch` al par
    está en `:152` y es otra cosa. El fix es **exportar ese bloque como función** y que `resolveProfileNode` la use:
    **una sola fuente local, la misma que sirve la ruta**. Criterio de aceptación por grep: **0** apariciones de
    `localhost`, `process.env.PORT` y `127.0.0.1` en `src/lib/routing.ts`.
    Pedido: **(a)** la mitad local sale de esa **función en proceso**, nunca de un HTTP a sí mismo; **(b)**
    `HERMES_PEER_PWA_URL` **exigida**, sin derivación de puerto (`replace(/:\d+$/, ":3000")` prohibido en el camino de
    ruteo); **(c)** un fallo de mitad **nunca** se cachea como "ausente" — es `NODE_UNREACHABLE` (criterio 21) y la
    caché sólo guarda resultados **medidos**; **(d)** el test del ruteo corre en un **puerto ≠ 3000** (como los dos
    nodos reales) **y en los dos escenarios**: con `:3000` libre **y** con `:3000` ocupado por un listener ajeno.

23. **Gramática de autoría, versión medida (para el commit 6: los "fantasmas" no son fantasmas).** Extraje **todos**
    los candidatos a autor de las cuatro salas desde los sobres `user` de este nodo: **258 candidatos / 1878
    apariciones**. Con la forma estricta (`^[A-Za-z0-9][A-Za-z0-9_.\- ]{0,63}( \(you\))? \[[^\]]{1,40}\]$`) caen
    **244**, de los cuales **243 son basura real** (`"model"` ×12, `headers` ×12, `"agent"` ×12, `"pattern"` ×12,
    `method`/`body`/`id`, `- Resolución` ×15, líneas de espacios) y **uno es legítimo con otra gramática**:
    **`You (user):` ×433**, que necesita su **propia forma positiva** (autor `You`), no el filtro.
    Y el hallazgo que ordena el resto: **lo que hoy figura como "fuera del roster" son los mismos participantes con
    nombre de pantalla** — `Algolab [This device]` ×239, `Algolab Strategy (you) [This device]` ×210,
    `Web Builder [This device]` ×34, `Brain Local (you) [This device]` ×18, `Web Auditor [This device]` ×13,
    `Hermes [100.124.132.48:9119]` ×49, `Hermes (you) [This device]` ×6. La comparación label↔`profile_name` falla por
    **forma del nombre**, no por pertenencia: normalizando (`casefold` + quitar espacios, `-`, `_`) **coinciden 5 de 6
    pares** — `Web Builder`≡`web-builder`, `Web Auditor`≡`web-auditor`, `Brain Local`≡`brain-local`,
    `Algolab Strategy`≡`algolab-strategy`, `Algolab`≡`algolab`.
    - **El sexto no se arregla normalizando**: `Hermes` ⇄ `default` es un **alias**, y el `config.yaml` de los perfiles
      **no expone `display_name`** (`display:` sólo tiene `resume_display`), así que no hay de dónde leerlo. `Hermes` es
      el **nombre de pantalla del NODO**, no del perfil: por eso la etiqueta `Hermes [100.124.132.48:9119]` lleva la IP
      del nodo del VPS y `Hermes (you) [This device]` es ese mismo nodo en local. El roster de la compuerta tiene que
      ser **normalizado(perfiles del censo) ∪ normalizado(nombres de nodo del env/config) ∪ {`You`}**.
    - **Regla final**: forma estricta **y** nombre normalizado en ese roster (la compuerta sigue siendo obligatoria para
      la forma sin etiqueta `Nombre:`); el `nodo` de la etiqueta se sirve tal cual (`This device`, `PC Local`, IPv4:puerto).
    - **Test negativo con corpus**: las **243 formas** medidas no pueden aparecer nunca como autor en el payload (lista
      de patrones como casos de prueba), y el test positivo exige que las etiquetas legítimas de arriba **sobrevivan**
      (si no, el filtro borra contenido real: es el fallo del 19(i) otra vez).

**Los conteos que dependen del tiempo se miden, no se citan.** Los baselines de las salas activas crecen durante la
tarde (esta sala pasó de 15 a 46 a 49 a 53 turnos; los artefactos de compactación dieron 6/2/2/0, 8/2/0/2 y 2/9/0/2
en tres momentos distintos), así que todo criterio de cantidad se evalúa **contra el censo derivado en la misma
corrida**. Los números explícitos de los criterios 11 y 19 (`808/124/118/53`, artefactos `0`) son de referencia: el
esperado es **igual o mayor** que esos valores — el fix no puede bajarlos, sólo subir el conteo con el crecimiento
real de la sala — y la aserción fuerte es siempre la **estructural** (100 % de los turnos con autor del roster,
0 artefactos), no el total.

Estos tres son los **criterios de cierre de Fase 2** fijados con @web-auditor; sin los tres no se cierra:
`rmugviqw9` reconstruida y rotulada `source:"reconstructed"` dentro del baseline **derivado en la misma corrida**
(nunca el `115` del store del Desktop)
con las 3 ids del baseline fuera · sala desconocida → `404` con `code` y nunca `200 []` · corte con el par caído →
`503` y el cliente conservando el snapshot.

## Higiene de entrega (aplica al commit 3 y al 4)

- **Los scripts auxiliares del agente no van al repo.** Verificado en la rama: quedaron **12 sin trackear** en la raíz
  (`apply-fixes.js`, `fix-types.py`, `fix-types2.py`, `fix-types3.py`, `patch.py`, `patch2.py`, `patch3.py`,
  `patch_chat.py`, `patch_room_store.py`, `test.ps1`, `verify.ts` y `out.txt` — 63 KB, salida de una corrida).
  **Ninguno entró a un commit**: `46ca485..HEAD` no contiene ni un `.py`, `.js`, `.mjs`, `.sh`, `.ps1` ni `verify.ts`.
  **`verify.ts` NO se borra**: importa `readRooms`/`readRoomTranscript` de `src/lib/room-store` e imprime
  `roomId | members | messageCount | first/last timestamp` — es el instrumento para re-correr los criterios 4, 11 y 20
  después del fix; se cosecha a `scripts/` o fuera del repo **antes** del `git clean`. El riesgo es el próximo
  `git add -A`: esos patrones **no** están en `.gitignore`, así que van al `.gitignore` o —mejor— los temporales se
  escriben **fuera del repo** (`$TMPDIR`), como el `fase1.diff` de Fase 1.
- **Cero archivos ajenos al cambio en el commit**: revisar `git show --stat` antes de commitear y no incluir
  temporales, evidencias ni artefactos de build.

## Addendum commit 5 — medido sobre `ec2adac` (para la spec del 5)

Los dos rojos del commit 3 (duplicados y pérdida del autor remoto) se arreglan en el commit 5; tres mediciones propias
que la spec necesita antes de implementarlo:

1. **"La sesión del dueño" es un CONJUNTO, no una sesión.** Censo de los stores de este nodo por sala y perfil:
   `rmugviqw9` → brain-local **8**, web-auditor **8**, web-builder **7**; `rmuag13gp` → algolab **16** +
   algolab-strategy **15**; `rmufxz2ti` → brain-local 4 + `default` 2; `rmuli31hi` → 1 por perfil. Una regla que
   conserve "la sesión del autor" (singular) **pierde hasta 15 de 16 turnos** de un perfil: el dueño es el **conjunto
   de sesiones de ese `profile_name` para ese `roomId`**, y dentro de ese conjunto cada línea es un evento.
2. **No hay ninguna columna que marque "propio vs contexto" — medido, y es un resultado negativo.** En las 26
   sesiones de sala, **todas** las filas (683 sobres `user` incluidos, más `assistant`/`tool`) tienen
   `observed=0, active=1, compacted=0, display_kind=NULL`: constantes. La distinción propio/contexto sólo se puede
   deducir **estructuralmente** (la etiqueta de la propia línea + el `profile_name` de la sesión), nunca leyendo una
   columna. `display_identity` es un blob de 24 bytes **único por fila** (no agrupa nada).
3. **El "0 repetidos" no es alcanzable sin excluir los repetidos triviales.** Dentro de las sesiones **propias** de cada
   autor en `rmugviqw9`: brain-local 52 `assistant` con **1** texto repetido (hasta 8 copias), web-auditor 37 con
   **1** (17 copias), web-builder 46 con **2** (12 y 3 copias) — son avisos cortos tipo `(pass)`, envíos legítimamente
   idénticos. La aserción queda **con umbral explícito**: 0 pares repetidos para texto no trivial (p. ej. ≥ 120
   caracteres) **y** ningún autor pierde turnos (piso = máximo entre las dos mitades); los repetidos cortos se
   reportan como métrica con estos valores esperados (1 / 1 / 2 por autor en `rmugviqw9`).
4. **Consecuencia declarada del arreglo de autoría:** si las líneas del nodo remoto se sirven sólo desde las sesiones
   propias de ese autor y el par está caído, **esos turnos no aparecen** (no se inventan ni se atribuyen a otro). Es
   el comportamiento correcto bajo el principio de honestidad, y va escrito en la UI como "nodo offline" — nunca como
   "mensajes de otro autor".

## Addendum — verificado en el código de `3a7d929` (commit 2), para el commit 3

Tres criterios **no** quedaron en la forma pedida; con líneas, para que el addendum los toque sin re-hacer nada más:

1. **Criterio 20 — la clave de dedup quedó con `at` adentro.** `src/lib/room-store.ts:337-344`:
   `if (Math.abs(d.at - item.at) <= 5000)` antes de comparar `(nombre, texto normalizado)`. Con la asincronía medida
   (2,2 s con el bot activo, **36 min** sin actividad) eso **no** deduplica: duplica o no según la suerte del reloj.
   Y el `id` estable es `sha1(roomId|thread|at|nombre|texto)` (`:346-348`) → el mismo evento con distinto `at` en los
   dos nodos recibe **id distinto** y el cliente lo re-renderiza. Pedido: clave = multiset `(nombre, texto
   normalizado)` con ordinal, **sin `at`**; `at` sólo como dato informativo de la fila del sobre.
2. **Criterio 9 — la migración se movió a *module load*.** `src/lib/room-store.ts:8-14` (`// Module load migration`:
   `if (doc && migrateSeedRooms(doc)) saveProfileDoc(doc)`), o sea **cualquier import** del store escribe
   `profile.yaml`, no sólo un GET. La migración va a un **script de arranque/migración**, no a un efecto de import.
3. **Criterio 10 — el `404` con `code` quedó bien (`chat/route.ts:43`) pero el camino de envío sigue persistiendo en
   el espejo.** `chat/route.ts:124-141` entra en `withProfileDocLock`, exige `rooms[roomKey]` en
   `ui_meta["hermes-bots-groups"]` y hace `log.push(userMsg)` ahí dentro; si la sala existe sólo en `state.db`, el
   `:43` la deja pasar y el error `ROOM_NOT_FOUND` sale **dentro del stream** (`:144`), después de que el celular ya
   empezó a enviar. Además contradice la restricción de Fase 2 ("no escribir logs de sala en `ui_meta`"): el mensaje
   del usuario tiene que persistir en la fuente de `state.db`, no en el espejo.

Lo demás del commit 2 sí aterrizó: el censo por `state.db`, el gate de remitentes con `labeledNames`/`(you)`
(`room-store.ts:270-290`), la normalización de errores con `code` y el health nuevo.

**Fase 3 (no en este commit):** igualar el log real del Desktop (`115/172/327/10`) haciendo server-visible el
store del Electron — subir/eliminar el cap de 64 KB de `ui_meta` en el push de `profiles.configure` del plugin
`hermes-bots` (repo `hermes-agent`, no este repo), y recién entonces el endpoint puede responder
`source:"store"`. Mientras tanto queda la reconstrucción, que es incompleta por diseño (el bot que entra tarde no
tiene el historial previo) y hay que decirlo en la UI: mostrar el origen del log, no hacerlo pasar por completo.
