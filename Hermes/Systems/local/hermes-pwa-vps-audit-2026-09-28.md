---
tipo: auditoria-tecnica
proyecto: hermes-pwa (PWA mobile sobre Hermes)
repo: C:\Projects\hermes-pwa
commit-base: 46ca485 (main, working tree limpio)
fecha: 2026-09-28
autor: brain-local (orquestación) — evidencia ejecutada, no inferida
estado: pendiente-aprobación-juan
zona: Hermes/Systems/local (reporte; el fix lo ejecuta web-builder)
relacionado: Hermes/Quarantine/hermes-pwa-fix-auditoria-antigravity-prompt.md (auditoría 2026-09-27, B0-B7, sin implementar)
---

# Auditoría VPS · hermes-pwa — replicación de chats y conexión

## Pregunta de Juan

> "¿Funciona C:\Projects\hermes-pwa en el VPS? Que se repliquen las conversaciones de los
> chats, que la conexión sea correcta. Tenemos varios bugs. Espero reporte."

## Topología verificada (2026-09-28 ~21:50 UTC / 17:50 EDT)

| Nodo | Host tailscale | Servicios verificados |
|---|---|---|
| PC local | truzt 100.105.0.23 | gateway :8642 (401 sin key = vivo). PWA local :3000 **caído** |
| VPS | vmi3131751 100.124.132.48 | PWA :3000 (200), gateway :8642 (200), desktop :9119 (302) |

RTT PC→VPS 247 ms. Funnel del PC `https://truzt.taila7f43b.ts.net` → **502**.

Baseline del repo: `46ca485`, working tree limpio, `npx tsc --noEmit` = 0 errores,
`npm run build` = OK (12 rutas). El build no es el problema.

## Lo que YA funciona (verificado con requests reales)

1. Login: `POST http://100.124.132.48:3000/api/auth/validate` con la key del gateway del VPS → `{"valid":true}`.
2. `GET /api/profiles` en el VPS: 8 bots VPS (`node=local`, online) **+ 9 bots del PC resueltos cross-node**
   con `sessionCount` real (brain-local 27, web-builder 50, algolab 24, …) y labels correctos
   (☁️ VPS / 🖥️ PC Local). La conexión VPS→PC está viva.
3. `GET /api/sessions?profile=brain-local&node=vps` desde el VPS → 27 sesiones del PC.
4. `GET /api/sessions/{id}/messages?profile=brain-local&node=vps` → contenido real del PC
   (`timestamp` en epoch-segundos, el cliente multiplica x1000 → correcto).
5. **E2E de sala (el camino crítico)**: `POST /api/groups/rmugviqw9-6zez7/chat` en el VPS con
   `targetBot=web-auditor` → `bot_start` con `node:"PC Local"`, streaming SSE y respuesta real `E2E_OK`
   desde el bot del PC. El ruteo VPS→gateway del PC y el streaming funcionan.

## Bugs verificados

### B1 — Auth decorativa (CRÍTICO · seguridad, expuesto 24/7 en el VPS)
Cualquier `Authorization: Bearer <cualquier cosa>` pasa. Verificado contra el VPS:
`Bearer totally-fake-key` → **200** en `/api/profiles` (devuelve los 17 perfiles + sessionCount)
y **200** en `/api/groups/rmugviqw9-6zez7/messages` (devuelve el log).
Mismo guard en `/api/groups/*/chat`, `/api/chat`, `/api/sessions*` y en el `PATCH /api/profiles`
(traversal de escritura + inyección YAML, ver B1b del informe de 2026-09-27).
`src/lib/auth.ts` ya tiene cookie httpOnly pero **nadie la usa**; la key vive en localStorage del navegador.

### B2 — Las conversaciones de sala NO se replican (CRÍTICO · es el pedido principal)
> **Corregido el 2026-09-28 18:2x con el recon de @web-builder y los probes de @web-auditor.**
> Mi primera lectura ("la transcripción real vive en `state.db`") era imprecisa en dos puntos;
> ver `correcciones` al final de este informe. Lo que sigue es la versión corregida.

La PWA lee las salas **sólo** de `profile.yaml → ui_meta["hermes-bots-groups"].rooms` del nodo que
sirve el request (`src/lib/hermes-fs.ts`, `src/app/api/groups/route.ts`). Ese store tiene **una sola
sala** (`id:rmuag13gp-5r3kn`, 54 entradas): el barrido de los 8 `profile.yaml` del nodo PC da
**0 hits** para `rmugviqw9`, `rmufxz2ti` y `rmuli31hi`.

El store canónico del Desktop **no es un archivo**: es localStorage del Electron (LevelDB, 61 bytes de
user key), key `hermes.plugin.hermes-bots.group-chats` con origen `file://` — inalcanzable desde la PWA
en `:3000` y sin sincronizar entre nodos. `state.db` **no es un log de sala**: sus sesiones
`Group: <roomId> · <thread>` son la sesión propia de cada bot (`assistant 30 / tool 53 / user 1` en la
de brain-local), y la sala hay que **reconstruirla** parseando el envoltorio
`[Group chat: "…"] … New messages in the room since your last turn:` + líneas `  Nombre [nodo]: texto`.
Es viable pero **no equivalente al log real**: @web-auditor reconstruyó `rmugviqw9` (204 turnos con parser
estricto) y el cruce contra el value del LevelDB dio **115** mensajes en el log del store (infla por
citas cruzadas entre bots, desinfla por bots que entran tarde). El log del store es la verdad; la
reconstrucción desde `state.db` es sólo el fallback cuando no hay acceso al store.

Censo de sesiones de sala (medido 2026-09-28 18:2x UTC, `title LIKE 'Group: %'`):

| Sala | Sesiones en el nodo PC | PWA en el VPS |
|---|---|---|
| rmuag13gp-5r3kn · Algolab Strategy, Algolab | 31 (algolab 16 + algolab-strategy 15) | 54 entradas |
| rmugviqw9-6zez7 · Brain Local, Web Builder, Web Auditor | 23 (brain-local 8 + web-builder 7 + web-auditor 8) | **3** (1 seed + los 2 de mi probe E2E) |
| rmufxz2ti-w6sk5 · Brain Local, 100.124.132.48:9119 | 4 (brain-local) + 2 (perfil `default` en `HERMES_HOME/state.db`) | **0** |
| rmuli31hi-inptr · (esta sala) | 3 (brain-local 1 + web-builder 1 + web-auditor 1) | **0** + `warning:"Group room not found"` |
| **TOTAL nodo PC** | **63** (60 `hidden=1`, 3 visibles) | — |
| **TOTAL nodo VPS** (8 perfiles + default, vía :8642) | **0** | — |

**Consecuencia de diseño para la Fase 2 (evidencia decisiva):** el nodo VPS tiene **0** sesiones de
sala, así que para las salas cuyos bots viven en el PC **no hay nada que re-derivar localmente**: la
PWA del VPS tiene que **pedir la sala al nodo par** (o el Desktop tiene que exponer su store).
Re-derivar de `state.db` sólo sirve en el nodo que corre esos bots. Si el PC está apagado, la sala no
se puede reconstruir en el VPS: hay que decidir explícitamente qué se muestra (estado "nodo PC
offline" en vez de lista vacía).

La sala `rmuag13gp` es la única con log completo en `profile.yaml`, y **sí** está espejada en el VPS
(54/54 entradas con el mismo id y timestamp) — o sea el espejo del registro de salas existe, pero no
cubre las salas activas y la PWA no tiene vía para traerlas.

### B3 — Seeds hardcodeados: pasado congelado, salas nuevas invisibles (ALTO)
> Corrección: **el mensaje del seed sí existió.** `msg-wb-1` es el último `assistant` de web-auditor en
> la sesión `20260927_141639_f2fa83`, thread `tmuk54861-6av2d`, `at=1790550198785` — idéntico al seed.

`src/lib/group-registry.ts` → `CANONICAL_ROOMS` fija 3 salas con `id`, `members` y `initialLog`, y
`ensureCanonicalRoomsInDoc()` **las reinyecta y persiste cuando el log está vacío**. El bug real es
peor que un mensaje inventado: muestra el pasado congelado de esa sala (una respuesta de ayer al
principio de una conversación de hoy) y, como la lista de salas también es fija, **toda sala nueva del
Desktop es invisible en el celular** (caso medido: `rmuli31hi-inptr`, 174 turnos, 0 en la PWA).

### B4 — Borrado silencioso de la conversación en el cliente (ALTO)
`src/lib/api.ts` `fetchGroupMessages`: `catch → return []`, y también devuelve `[]` con HTTP 404.
`GroupChatView.loadGroupMessages` reemplaza la lista cuando cambia la longitud → cualquier fallo
transitorio (o una sala no encontrada, que el server responde **200 con `messages:[]`**) **limpia la
pantalla**. El polling corre cada 3.2 s, así que la ventana de fallo se repite.

### B5 — Escrituras sin lock ni verificación (ALTO)
`src/app/api/groups/[groupId]/chat/route.ts`: escribe el mensaje del usuario, y al terminar el stream
re-lee el doc y hace push de la respuesta (read-modify-write sin mutex). `saveProfileDoc()` devuelve
`boolean` y **nadie lo mira** → si la escritura falla, el mensaje se pierde mientras la UI lo muestra.
Sin escritura atómica (tmp + fsync + rename) ni backup.

### B6 — Truncado asimétrico del mismo mensaje (MEDIO)
En el log de algolab: 12 entradas truncadas en el `profile.yaml` del PC (1200 chars, terminan en
"… [truncated]", flag `truncated:true`) vs **completas** (1187 chars, sin flag) en el del VPS.
El "message-recovery" por `node:sqlite` sólo funciona en el nodo que tiene esa `state.db`.

### B7 — El proxy traga errores del gateway (MEDIO)
`GET /api/sessions/no-such-session/messages` → **200** (debería 404/502).
`GET /api/sessions` con clave inválida → 200 con "0 conversaciones" en vez de 401.
`/api/health` (pedido en B4 del informe previo) → **404**, no existe.

### B8 — Dependencia no declarada (MEDIO)
`import yaml from "js-yaml"` en `src/lib/hermes-fs.ts` pero `js-yaml` **no está en `package.json`**
(resuelve por dependencia transitiva; `npm ls js-yaml` en el árbol hermano da `(empty)`).
Un `npm ci` limpio en el VPS puede romper `/api/groups` y `/api/groups/*/chat`.

### B9 — Modelo de los bots remotos siempre "deepseek-v4.1-flash" (BAJO)
Fallback hardcodeado: el `config.yaml` del PC no es legible desde el VPS, así que el selector de
modelo muestra un valor falso para los 9 bots del PC.

### B10 — Ops (BAJO · **corregido 18:5x**: no está caído, es un puerto mal documentado)
La PWA local del PC **sí está corriendo**: :3111 y :3112 responden 200 (dos `next start`, PIDs 28792 y
7160) sirviendo el build previo — `Bearer totally-fake-key` → **200** y `/api/health` → **404**, o sea
B1 y B7 también en el nodo PC. El problema real es de **puerto**: `iniciar-pwa.bat` y el README apuntan a
:3000 y el funnel `truzt.taila7f43b.ts.net` apunta a :3000 → de ahí el 502 (nadie escucha en :3000).
Fix: alinear el funnel con 3111/3112 o correr el PWA local en 3000; y corregir el .bat/README.

## Orquestación propuesta

**Fase 1 — bloqueante (seguridad + integridad de datos)**
B1 + B1b + B2 (cookie httpOnly, sacar la key del navegador, traversal del PATCH) → ya especificado
bloque por bloque en `Hermes/Quarantine/hermes-pwa-fix-auditoria-antigravity-prompt.md`.
Sumar B5 (escritura atómica + lock + chequear el retorno) y B7 (propagar status upstream).

**Fase 2 — el pedido de Juan: replicación real de conversaciones**
Fuente de verdad de salas = `state.db` del nodo (sesiones `Group: <roomId> · <threadId>`) + endpoint
de salas que consulte también al nodo par; eliminar los seeds hardcodeados (B3); arreglar el wipe
del cliente (B4) devolviendo error explícito en vez de `[]`.

**Fase 3 — deuda**
B6 (truncado), B8 (declarar js-yaml, sacar next-pwa duplicado), B9 (modelo remoto real),
B10 (levantar el PWA del PC + revisar el funnel), `/api/health` y raíz de datos robusta (B4 del informe previo).

**Verificación independiente:** web-auditor re-ejecuta los probes (401 sin cookie / con bearer falso,
conteo de mensajes por sala contra `state.db`, E2E de sala, `tsc` + `build`) sobre el commit congelado.
Sin esa re-ejecución el fix no se cierra.

## Comandos de reproducción

```bash
cd /c/Projects/hermes-pwa && set -a && . ./.env.local && set +a
B=http://100.124.132.48:3000; K="Authorization: Bearer $HERMES_VPS_API_KEY"
curl -s -o /dev/null -w "%{http_code}\n" $B/api/profiles -H "Authorization: Bearer totally-fake-key"   # 200 (BUG)
curl -s $B/api/groups -H "$K"                                                                          # salas y messageCount
curl -s $B/api/groups/rmugviqw9-6zez7/messages -H "$K"                                                 # 1 msg (seed) vs 838 en state.db
curl -s -N -X POST $B/api/groups/rmugviqw9-6zez7/chat -H "$K" -H 'Content-Type: application/json' \
  -d '{"text":"@web-auditor PING","targetBot":"web-auditor"}'                                          # E2E: bot_start node=PC Local + stream
```

## Nota de estado

No se tocó `profile.yaml` a mano. El único efecto colateral de la verificación fue un mensaje de prueba
E2E en el log de la sala `rmugviqw9` **del profile.yaml del VPS** (`@web-auditor PING E2E…` + `E2E_OK`);
no afecta a la conversación del Desktop, que vive en `state.db`.

## Correcciones y estado del arte (2026-09-28 18:30 UTC)

Aportes de @web-builder (recon) y @web-auditor (probes independientes) sobre este informe:

1. **B2 mal apuntado en la primera versión.** El store canónico de las salas no es un archivo ni
   `state.db`: es localStorage del Electron (LevelDB, key `hermes.plugin.hermes-bots.group-chats`,
   origen `file://`). `profile.yaml` sólo tiene la sala de algolab. `state.db` guarda la sesión propia
   de cada bot por sala y hay que reconstruir la sala desde el envoltorio del turno. Ambas cosas ya
   están incorporadas arriba.
2. **B3 mal diagnosticado en la primera versión.** El mensaje del seed **sí existió** (es el último
   `assistant` de web-auditor en `20260927_141639_f2fa83`). El bug es el log hardcodeado + la lista de
   salas fija.
3. **Censo de sesiones de sala: 63 en el nodo PC** (rmuag13gp 31 / rmugviqw9 23 / rmufxz2ti 6 /
   rmuli31hi 3), de las cuales **60 `hidden=1`** y sólo **3 visibles**. Dos correcciones sucesivas:
   el 60 de @web-auditor omitía `rmuli31hi` de web-builder (3, no 2); mi 61 omitía
   **`HERMES_HOME/state.db`** (= perfil `default`, 2 sesiones de `rmufxz2ti`, 28 y 83 msgs, ambos
   `hidden=1`), fuente legítima porque `default-this-device` es miembro real de esa sala
   (`connectionKind:"remote"`). Verificado con el censo completo (todas las fuentes) = 63/60/3.
   **El nodo VPS tiene 0** (gateway :8642, 8 perfiles + `default`): nada del VPS entra en la cuenta.
4. **Baseline mutado por mi propio probe E2E** (para cualquier comparación antes/después del
   `profile.yaml` del VPS). Log de `rmugviqw9` en el VPS, congelado con ids exactos:
   `msg-wb-1` (seed, at 1790550198785) · `usr_1790632373669_fm47n` (at 1790632373669, mi probe) ·
   `bot_1790632380284_p90ph` (at 1790632380284, respuesta `E2E_OK`). Las dos últimas desaparecen solas
   cuando aterrice la Fase 2 (el log deja de venir del seed/`profile.yaml`).
5. **Decisión de diseño de Fase 2 que queda fijada:** reconstrucción local de `state.db` **sólo** en el
   nodo que corre esos bots; para el resto, fetch al nodo par, con estado explícito de "nodo offline"
   en vez de lista vacía.

### Dato estructural confirmado (independiente, 18:4x UTC)

De las **63** sesiones de sala, **60 tienen `hidden=1`** y sólo **3** son visibles para `/api/sessions`
(brain-local `rmufxz2ti · tmufybayi-ujnk5` 162 msgs, brain-local `rmugviqw9 · tmuirrz6z-25oxp` 76 msgs,
web-builder `rmugviqw9 · tmuirrz6z-25oxp` 87 msgs). Consecuencia: quién intente derivar las salas del
**API de sesiones** ve 3 de 63 — Fase 2 lee `state.db`/gateway **sin** el filtro `hidden` o usa peer fetch.
Además ninguna de las 63 filas tiene `session_key`, `chat_id`, `chat_type`, `thread_id` ni `origin_json`
(todos NULL): la sala y el thread viven **sólo en el `title`**, escrito después de crear la fila → un censo
por título tiene lag de minutos; el antes/después se hace contra snapshot congelado.

### Contrato HTTP de Fase 2 (fijado por brain-local, para implementar tal cual)

El pedido de @web-auditor es correcto: hoy "sala vacía", "nodo caído" y "sala inexistente" colapsan en
`200 {"messages":[]}` y el cliente lo usa para borrar la pantalla. Contrato obligatorio:

| Caso | Status | Body |
|---|---|---|
| Sala inexistente en cualquier nodo | **404** | `{error:"room_not_found", code:"ROOM_NOT_FOUND"}` |
| Sala resuelta | **200** | `{messages:[…], source:"local"\|"peer", node:"pc"\|"vps", peerReachable:true}` |
| Sala vacía pero nodo alcanzable | **200** | idem con `messages:[]` y `peerReachable:true` |
| Nodo par inalcanzable | **503** | `{error:"peer_offline", code:"PEER_OFFLINE", node:"pc", lastSeenAt:<epoch>}` |
| Nodo par alcanzable pero la reconstrucción excede el budget | **504** | `{error:"peer_timeout", code:"PEER_TIMEOUT"}` |

`GET /api/groups`: cada sala lleva `source`, `nodeStatus` y `messageCount: number|null` (`null` = nodo
offline, para que la UI no lea 0 como "sala vacía"). El cliente ramifica por `code`, nunca por texto:
404 → "sala no encontrada en este nodo"; 503/504 → banner "nodo PC offline — último snapshot" y **nunca**
limpia la lista; sólo un 200 reemplaza la lista local. Se elimina el `warning:"Group room not found"`
con HTTP 200.

**Criterios de cierre de Fase 2:** (1) `rmugviqw9` en la PWA del VPS sirve el **log real de la sala**
(115 mensajes del store — `rmufxz2ti` 172, `rmuag13gp` 327, `rmuli31hi` 10), **no** los 204 de la
reconstrucción desde `state.db`, que es un artefacto del parser, y las 3 ids del baseline (`msg-wb-1`,
`usr_1790632373669_fm47n`, `bot_1790632380284_p90ph`) desaparecen del log; el store referencia **76
mappings de sesión contra 63 filas** en `state.db` (ids huérfanos: p. ej. `rmugviqw9` 30 vs 23), así que
el peer fetch debe tolerarlos y **no** usarlos para contar; (2) sala desconocida → 404 con `code`, nunca
200 `[]`; (3) prueba de corte: con el gateway del PC caído, la PWA del VPS responde 503 y el cliente
conserva el último snapshot.

### Fase 3 — dónde vive de verdad el espejo de salas (verificado en el código de hermes-agent, 19:05 UTC)

El checkout de hermes-agent está en `C:\Users\ingju\AppData\Local\hermes\hermes-agent` y el chat de
grupos es un plugin in-tree: `apps/desktop/src/plugins/hermes-bots/` (`group-chat.ts`, `group-pin.ts`,
`plugin.tsx`, + tests). Hallazgos que ajustan el alcance de Fase 3:

- `group-chat.ts:50-52` — **`GROUP_CHAT_SYNC_MAX_BYTES = 900_000`** con el comentario *"Gateway ui_meta is
  capped after Python JSON serialization. Keep a healthy [margin]"*. O sea: **no hay un cap de 64 KB**;
  hay **dos** topes — el del gateway (Python, a localizar) y este presupuesto de proyección de 900 KB.
- La proyección es **lossy por diseño**: `group-chat.ts:59` la describe como *"bounded ui_meta projection:
  a compacted log plus …"*, con un loop que **descarta entradas del log** hasta entrar en el presupuesto
  (`:398`), **descarta imágenes** (`:403`) y **capea miembros** (`:359`). Eso explica 54 entradas en
  `profile.yaml` contra 327 en el store para la sala de algolab: no es corrupción, es el espejo recortado.
- **El consumidor declarado del espejo es el celular**: `group-chat.test.ts:11` — *"profile ui_meta so
  mobile sees the same rooms"*; `group-chat.ts:277` — *"rides the default profile's ui_meta so mobile can
  show the same messages"*; y `:180` (#114341) anota que el espejo de `ui_meta` **es la única copia en
  disco de una sala**.
- Consecuencia: **Fase 3 vive en `hermes-agent` (plugin desktop + cap del gateway), no en `hermes-pwa`**,
  y su prompt debe nombrar los dos topes. Cuando el espejo sea completo, el endpoint responde
  `source:"store"` y el cliente lo prefiere; peer fetch y reconstrucción quedan como fallback.
- Pregunta abierta para Fase 3: el espejo en el nodo PC sólo tiene **1 sala (algolab)** mientras el store
  del Desktop tiene **4** → falta ver por qué el push no cubre `rmugviqw9`, `rmufxz2ti` ni `rmuli31hi`.

#### Cap del gateway y congelamiento actual (triple verificado, 19:0x–19:1x UTC)

- **El cap es una decisión documentada, no un accidente.** `tui_gateway/methods_profiles.py:487`
  `_configure_ui_meta`, docstring `:488-489`: *"Merge `params["ui_meta"]` key-wise into profile.yaml (None
  deletes). 64KB cap (rides every roster paint)"*. `:491` `applied["ui_meta"] = False`; `:494`
  `if len(json.dumps(incoming)) > 65536: return` → **rechazo mudo**: sin excepción, sin campo de error, y
  se pierde **toda** la escritura de `ui_meta` (no es por clave).
- **El espejo SÍ pasa por el gateway** (no es escritura directa del plugin): en `profile.yaml:1-2` está
  `_ui_meta_revisions: {hermes-bots-groups: 1668}`, el contador CAS que `_configure_ui_meta` incrementa en
  cada apply exitoso (`:519`, `:524`, y *"revisions survive deletion"* `:489-490`). Es el **instrumento
  exacto**: si avanza, el espejo está sano; si queda clavado, hay rechazo.
- **Estado hoy: congelado.** `profile.yaml` mtime **19:41:26.204Z**, `ui_meta["hermes-bots-groups"].updatedAt`
  **1790624485107 = 19:41:25.107Z**, contador CAS clavado en **1668**, sala `revision: 1936`,
  `omitted: 359`, 54 entradas, 12 con `truncated: true` → **3 h 30 min sin una sola escritura** con el
  Desktop vivo (medido 23:11 UTC / 19:11 local). El espejo no es "recortado": está **muerto**.
- **Causa raíz del "1 de 4"** (código del plugin): proyección newest-first (`group-chat.ts:283-289`) +
  trim que sólo ajusta la sala que se está agregando (`:398-401`) → la sala más nueva se come el
  presupuesto entero y las otras tres caen por `delete rooms[key]` (`:405-407`). Sin rebalanceo entre salas
  el reparto es todo o nada.
- **Build viva vs fuente:** HEAD de `hermes-agent` = `5a3e03ef37` (23-sep) con
  `GROUP_CHAT_SYNC_MAX_BYTES = 48000` / `SYNC_TEXT_CHARS = 1200`; el **working tree** (3 archivos
  modificados **sin commitear**, 30 inserciones, editados hoy 11:27 y 15:43) trae `900_000` / `60_000`.
  `apps/desktop/dist/` reconstruido **15:47** contiene `9e5` y `6e4` → la app que corre usa el working
  tree, cuyo payload de 4 salas **excede los 65.536** del gateway → rechazo mudo → espejo congelado desde
  las 15:41 (escrito por la build anterior de `dist/`, ~48 KB de presupuesto). Ojo: `24e3` en el bundle es
  `GROUP_CHAT_SYNC_IMAGE_CHARS`, **idéntico en HEAD y en el worktree**, así que no discrimina build; los
  que sí discriminan son `9e5` y `6e4`.
- **Criterios de aceptación de Fase 3 (punto 1, sin cambio de comportamiento):** (i) `ui_meta` > 65.536 →
  respuesta con error explícito (`ui_meta_error:"too_large"`) en vez del mudo `applied.ui_meta=false`;
  (ii) tras reconstruir `dist`, `_ui_meta_revisions["hermes-bots-groups"]` **avanza** desde 1668 y
  `updatedAt` lo sigue, dentro del minuto siguiente a un mensaje de sala; (iii) el espejo lleva las **4
  salas** con `omitted` por sala (no 1 con `delete rooms[key]`).

### CLI Antigravity headless — receta verificada (2026-09-28, 4 corridas reales)

`language_server.exe agentapi` funciona de verdad, pero necesita **tres** variables de entorno y la
app corriendo (el LS vive dentro de la IDE):

| var | de dónde sale | falla con |
|---|---|---|
| `ANTIGRAVITY_LS_ADDRESS` | `http://127.0.0.1:<puerto gRPC>` del `language_server.exe --standalone` (hoy **59804**; el otro puerto del mismo PID, 59803, es HTTP/1.1 y contesta `error reading server preface: EOF`) | `ANTIGRAVITY_LS_ADDRESS is not set` |
| `ANTIGRAVITY_CSRF_TOKEN` | el `--csrf_token <uuid>` de la propia línea de comandos del LS | `Unauthenticated ... missing CSRF token` |
| `ANTIGRAVITY_PROJECT_ID` | `~/.gemini/config/projects/<uuid>.json` (`hermes-pwa` = `ee38b6c1-8799-4305-af6c-1533a4c86471`) | `project_id is required when providing project_env_config` |

Comandos: `new-conversation [--model=flash_lite|flash|pro] [--title=] [--profile=] "<prompt>"` →
`{conversationId}`; `get-conversation-metadata <id>` → workspace/rama/settings; `send-message
<recipient_id> "<content>"`. **El project id NO se deduce del cwd** (probado: dentro del repo sin la
variable falla; desde `/tmp` con ella el workspace es el del proyecto). La respuesta se lee sin GUI en
`~/.gemini/antigravity/conversations/<id>.db` (SQLite, tabla `steps`). Script operativo:
`Hermes/Systems/local/antigravity-cli.sh` (`discover` / `new` / `read`), probado end-to-end: pidió
`git branch --show-current` en el repo y devolvió `SCRIPT_OK main`.

**Para Fase 3:** no hay ningún proyecto apuntando a `AppData\Local\hermes\hermes-agent`, así que el CLI
no puede trabajar sobre ese repo hasta crear/registrar un proyecto para esa carpeta.

### Prompts de fix ya escritos (vault, pendientes de commit)

| Fase | Archivo | Contenido |
|---|---|---|
| 1 | `Hermes/Quarantine/hermes-pwa-fase1-auth-integridad-antigravity-prompt.md` | B1 + B1b + B5 + B7 (guard único fail-closed, sin echo de la key, traversal/inyección del PATCH, tmp+fsync+rename con lock, `/api/health`) |
| 2 | `Hermes/Quarantine/hermes-pwa-fase2-replicacion-salas-antigravity-prompt.md` | Fuente de verdad de salas + fetch al nodo par + quitar seeds + no vaciar la UI ante error |
| — | `Hermes/Quarantine/hermes-pwa-fase2-recon-fuente-de-verdad-2026-09-28.md` | Evidencia del recon (LevelDB, MANIFEST, mapeo thread→sesión) |
| — | `Hermes/Systems/local/hermes-pwa-audit-probes-2026-09-28.md` | Probes independientes de web-auditor |

**Recomendación consolidada (brain-local + web-builder + web-auditor, unánime): Fase 1 primero.**
El VPS está abierto a cualquiera del tailnet con cualquier string en el header, el fix es chico y no
toca datos; la Fase 2 cambia semántica de salas y necesita el baseline congelado.

