# Prompt para Antigravity — Completar PWA: sesiones reales, nueva conversación, historial, profiles, streaming

> Proyecto: `C:\Projects\hermes-pwa` (Next.js + Tailwind + Zustand)
> Kanban: t_5e004396 · Generado por web-builder · 2026-09-26
> API verificada contra el gateway real en `http://127.0.0.1:8642` (código fuente: `hermes-agent/gateway/platforms/api_server.py`)

---

## Objetivo

Terminar la PWA de Hermes conectándola a los endpoints REALES del gateway (`/api/sessions*`, `/api/sessions/{id}/chat/stream`, prefijo `/p/<profile>/`) para que sea un mirror funcional de Hermes desktop: lista de sesiones reales, crear conversación, historial paginado, selector de profile y streaming con reconexión.

## Contexto del proyecto

- Next.js (App Router) + Tailwind v4 + Zustand. Estado en `src/lib/store.ts`, tipos en `src/lib/types.ts`, cliente API en `src/lib/api.ts`, proxy server-side en `src/app/api/*`.
- El gateway Hermes corre en `http://127.0.0.1:8642`, auth `Authorization: Bearer <API_SERVER_KEY>` (validador actual: `/api/auth/validate` contra `/v1/models` — funciona, no tocar).
- `next.config` ya hace rewrite `/hermes-api/:path*` → `http://127.0.0.1:8642/:path*`.
- ⚠️ **El brief original del task decía `/v1/sessions` y `/v1/profiles`: NO EXISTEN.** Los endpoints reales están verificados abajo. No inventar rutas.

### API real verificada (fuente de verdad)

**Sesiones**

```
GET  /api/sessions?limit=50&offset=0
     → 200 { "object": "list", "data": [Session...], "limit", "offset", "has_more" }
     Session = { id, source, user_id, model, title, started_at, ended_at,
       message_count, tool_call_count, ..., last_active, preview, pinned,
       archived, hidden, has_system_prompt, has_model_config }
     - Ya viene ordenado por last_active DESC; incluye pinned.
     - archived/hidden quedan excluidos server-side.
     - last_active / started_at / ended_at son EPOCH SEGUNDOS (float), no ISO.
     - preview = resumen del último mensaje (usar como "último mensaje").
     - source ∈ {telegram, desktop, tui, api_server, ...} — mostrar todas.

POST /api/sessions   body: { title?: string }   (id se autogenera "api_<ts>_<hex>")
     → 201 { "object": "hermes.session", "session": Session }

GET  /api/sessions/{id}/messages?limit=500&order=latest|oldest&offset=0
     → 200 { "object": "list", "session_id", "data": [Message...],
             "pagination": { limit, offset, order, returned } }
     Message = { id, session_id, role, content, tool_call_id, tool_calls,
       tool_name, timestamp, token_count, finish_reason, reasoning,
       reasoning_content, display_kind }
     - default (sin params): última página de hasta 500, orden cronológico.
     - roles incluyen "tool" — filtrar en la UI, mostrar solo user/assistant
       (y system si aparece).
```

**Streaming nativo de sesión (usar ESTO, no `/v1/chat/completions`)**

```
POST /api/sessions/{id}/chat/stream   body: { "message": "texto del usuario" }
     headers: Authorization + Accept: text/event-stream
     → SSE con eventos NOMBREDOS (línea "event:" + "data: {json}"):
       run.started        { user_message, runtime, session_id, run_id, seq, ts }
       message.started    { message: { id, role } }
       assistant.delta    { message_id, delta }          ← texto incremental
       assistant.commentary { message_id, text }          ← comentarios mid-turn
       tool.progress | tool.started | tool.completed | tool.failed
                          { message_id, tool_name, preview, args }
       assistant.completed{ session_id, message_id, content, runtime }
       run.completed | run.failed | run.cancelled  (terminales, incluyen messages/usage)
       error              { message }
       done               {}                              ← fin del stream
     - Los frames de keepalive llegan como comentario ": keepalive\n\n" (líneas
       que empiezan con ":" → ignorar).
     - El payload de run.* puede traer session_id DIFERENTE al pedido (reset /new):
       si cambia, actualizar activeSessionId en el store.

Reconexión si el stream se cae (el run sigue vivo server-side):
GET  /v1/runs/{run_id}       → status + output de la última respuesta
GET  /v1/runs/{run_id}/events → eventos para re-play
     Guardar run_id del evento run.started; al perder conexión, reintentar
     GET /v1/runs/{run_id} cada 2s (máx ~30 intentos); cuando status es
     terminal, pintar el output y refrescar mensajes de la sesión.
```

**Profiles**

```
- NO existe GET /v1/profiles ni ningún endpoint HTTP de listados de profiles.
- Multiplexación por PREFIJO DE RUTA en el mismo listener:
    /p/<profile>/api/sessions, /p/<profile>/api/sessions/{id}/chat/stream, etc.
  (verificado: /p/web-builder/api/sessions responde 401 sin key, 404 si el
   profile no existe). Sin prefijo = profile default del gateway.
- Profiles existentes en esta máquina (para la lista inicial, verificar con
  `ls C:\Users\ingju\AppData\Local\hermes\profiles\`):
  algolab, brain-local, omh-test, pcbrain, trading-performance, web-auditor,
  web-builder (+ default "Hermes").
```

## Tarea específica

1. **Adaptar tipos y parsing (`src/lib/types.ts`)**
   - Reemplazar `Session` por la forma real: `id, title, source, model, preview, message_count, last_active, started_at, ended_at, pinned, archived, hidden` (epoch seconds). Agregar adaptador `toUiSession(raw)` que derive `title` (fallback: `preview` cortada o id), `lastMessage = preview`, `updatedAt = new Date(last_active*1000).toISOString()`.
   - `Message.timestamp` puede venir epoch o ISO — normalizar en el adaptador.

2. **Cliente API (`src/lib/api.ts`) + proxy routes**
   - Corregir `fetchSessions`/`fetchMessages`/`createSession` para leer la forma `{object:"list", data:[...]}` (hoy el código asume `data.sessions ?? data` — no coincide).
   - Reescribir `sendMessage` para consumir `POST /api/sessions/{id}/chat/stream` con parser SSE que maneje `event:` + `data:` y keepalive (`:`). Callbacks: `onDelta(text)`, `onRunStarted({run_id, session_id})`, `onToolEvent`, `onCompleted(finalContent, effectiveSessionId)`, `onError`.
   - Añadir `fetchRunStatus(apiKey, runId, profile)` → `GET /v1/runs/{run_id}` y helper `recoverRun` para reconexión con backoff simple (2s, máx 30).
   - Todas las llamadas al gateway pasan por `gatewayPath(profile, path)`: si `profile` es `"default"` → `/...`; si no → `/p/<profile>/...`. Propagar por el rewrite `/hermes-api` existente o por las route handlers (`src/app/api/*`) añadiendo el prefijo antes de re-encaminar.

3. **Sesiones reales + auto-refresh (`src/app/page.tsx`)**
   - Cargar con `GET /api/sessions?limit=50` para el profile activo.
   - Polling liviano: refrescar cada 15s con `visibilitychange` como trigger extra (no refrescar con pestaña oculta). Fusionar preservando `activeSessionId`.
   - Sort client-side: `pinned` primero, luego `last_active` DESC.

4. **Botón + (nueva conversación)**
   - `POST /api/sessions {title}` con title opcional (prompt simple o `"Nueva conversación"`), en el profile activo; insertar al inicio y seleccionar.
   - Si el title da conflicto (400 `invalid_title`), reintentar sin title.

5. **Historial (`src/components/ChatView.tsx`)**
   - Al abrir sesión: `GET .../messages?limit=200` (página latest, cronológica). Filtrar `role==="tool"`.
   - Si `pagination.returned === limit` puede haber más: botón "Cargar mensajes anteriores" que pida `order=oldest` páginas iniciales hasta alcanzar el primer id conocido — implementación simple aceptable: `?limit=500&order=latest` y omitir el botón si <500 (caso común).
   - Scroll automático al final al cargar y al hacer streaming; no forzar si el usuario scrolleó arriba (detectar `scrollTop` cerca del bottom antes de auto-scroll).
   - El fix del loader actual: hoy `sessionMessages.length > 0` evita recargar pero nunca cachea "cargado" → usar `Set<string> loadedSessions` en el store.

6. **Selector de profile**
   - Lista estática en `src/lib/profiles.ts`: `const PROFILES = ["default","brain-local","web-builder","web-auditor","algolab","pcbrain","trading-performance","omh-test"]` + label legible. (Sin endpoint HTTP; documentar el porqué en comentario.)
   - Dropdown en header (mobile) y sidebar footer (desktop); cambiar profile → persistir en `localStorage`, limpiar `sessions`/`messages` cacheados y recargar sesiones del nuevo scope. El perfil activo se muestra como chip en el header.

7. **Streaming con sesiones reales + reconexión**
   - Reemplazar el uso de `/v1/chat/completions` por `chat/stream`. Pintar deltas en el mensaje assistant; mostrar indicador discreto de tool activity cuando lleguen `tool.started`/`tool.completed` (ej. "🔧 usando `terminal`…" bajo el bubble).
   - Al desconectarse el reader sin `done`: entrar en modo reconexión con `recoverRun(run_id)` y al terminar refrescar mensajes de la sesión.
   - Botón stop actual: mantener (abort del fetch) — server-side el run se interrumpe por desconexión (verificado en el código del gateway: `_drain_session_stream_task_on_disconnect`).

## Archivos a tocar

```
src/lib/types.ts          (Session/Message forma real, ChatState + loadedSessions/profile)
src/lib/api.ts            (endpoints reales, parser SSE chat/stream, run recovery, gatewayPath)
src/lib/store.ts          (loadedSessions set, activeProfile por persistencia)
src/lib/profiles.ts       (nuevo: lista de profiles + labels)
src/app/page.tsx          (sesiones reales, polling, + nueva sesión, selector profile)
src/components/ChatView.tsx (chat/stream, tool events, scroll inteligente, reconexión)
src/components/SessionList.tsx (badge pinned, format epoch, preview)
src/app/api/sessions/route.ts + .../messages/route.ts (proxy: admitir query params y prefijo /p/)
```

## Restricciones

- **NO tocar** auth/login (`/api/auth/validate`, `src/app/auth/*`): ya funciona contra `/v1/models`.
- **NO agregar** dependencias nuevas (el parser SSE se hace a mano con `ReadableStream`, como el código actual).
- **NO hardcodear** la API key en el cliente: sigue viniendo de `localStorage` → header Bearer, como hoy.
- Mantener el dark theme CSS y las variables existentes; sin rediseño visual, solo lo funcional (chip de profile + dropdown simples con los tokens actuales).
- Next.js route handlers: `params` es `Promise` (ya se hace `await params` en messages/route.ts — mantener el pattern).
- No usar `/v1/responses` ni `/v1/runs` (POST) — fuera de scope.
- Verificar build: `npm run build` debe pasar sin errores de TS.

## Criterios de aceptación

1. La sidebar muestra las sesiones reales del gateway (mismas que ve desktop: títulos, preview, tiempo relativo correcto desde epoch, orden pinned→recientes).
2. "+" crea sesión vía `POST /api/sessions` en el profile activo, aparece arriba y queda seleccionada con chat vacío.
3. Al seleccionar una sesión con historial se cargan los mensajes previos (user/assistant, sin tool rows) y se scrollea al final.
4. Enviar mensaje hace streaming visible con `assistant.delta` en vivo; los tool events muestran indicador; el markdown se renderiza; el `streaming-cursor` desaparece en `assistant.completed`.
5. Cambiar de profile (dropdown) recarga la lista de sesiones del scope `/p/<profile>/api/sessions` y el chat funciona dentro de ese profile.
6. Si el stream se corta (ej. poner el device offline a mitad), al volver la app recupera la respuesta vía `GET /v1/runs/{run_id}` o refrescando mensajes, sin dejar el bubble vacío.
7. `npm run build` sin errores; sin regresión en login.
