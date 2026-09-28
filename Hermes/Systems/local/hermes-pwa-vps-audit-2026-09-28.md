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
La PWA lee las salas **sólo** de `profile.yaml → ui_meta["hermes-bots-groups"].rooms` del nodo que
sirve el request (`src/lib/hermes-fs.ts`, `src/app/api/groups/route.ts`). La transcripción real del
Desktop vive en `<perfil>/state.db`, en sesiones ocultas tituladas `Group: <roomId> · <threadId>`,
y la PWA **ni las lee ni las pide al nodo par**. Medición (suma de sesiones de grupo por bot):

| Sala | Desktop (state.db) | PWA en el VPS |
|---|---|---|
| rmugviqw9-6zez7 · Brain Local, Web Builder, Web Auditor | 8+7+8 sesiones (308+257+273 msgs) | **1** mensaje |
| rmufxz2ti-w6sk5 · Brain Local, 100.124.132.48:9119 | 4 sesiones (548 msgs) | **0** mensajes |
| rmuag13gp-5r3kn · Algolab Strategy, Algolab | 16+15 sesiones (3934 msgs) | 54 mensajes |

La sala `rmuag13gp` es la única que tiene log completo en `profile.yaml`, y ese log **sí** está
espejado en el VPS (54/54 entradas con el mismo id y timestamp), o sea que el mecanismo de
replicación del registro de salas existe — pero las dos salas que Juan realmente usa no están en él,
y el PWA no tiene ninguna vía para traerlas.

### B3 — Seeds hardcodeados con mensajes reales (ALTO)
`src/lib/group-registry.ts` → `CANONICAL_ROOMS` fija 3 salas con `id`, `members` y `initialLog`, y
`ensureCanonicalRoomsInDoc()` **las reinyecta cuando el log está vacío** (y las persiste). Efecto
verificado: el VPS muestra en `rmugviqw9` un mensaje de `web-auditor` ("eslint . = 118 problems",
timestamp 1790550198785) que en esa sala **nunca existió**. Además toda sala nueva del Desktop es
invisible en el celular porque la lista de salas también es fija.

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

### B10 — Ops (BAJO)
El PWA local del PC no está corriendo (:3000 cerrado) y el funnel devuelve 502 → el celular hoy
depende exclusivamente del VPS.

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
