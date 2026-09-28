# Prompt para Antigravity — hermes-pwa · Fase 1 (auth real + integridad de escritura)

**Repo:** `C:\Projects\hermes-pwa` · **Baseline congelado:** `46ca485` (working tree limpio, `tsc --noEmit` = 0, `next build` OK)
**Commit esperado:** uno solo, `fix(auth,fs): real auth guard, atomic profile writes, honest upstream errors`
**Fuente:** `Hermes/Systems/local/hermes-pwa-vps-audit-2026-09-28.md` (B1, B1b, B5, B7) — evidencia ejecutada contra el VPS.
**No incluye:** replicación de salas (eso es Fase 2, otro commit).

---

## Objetivo

Cerrar el agujero de autenticación (hoy **cualquier** `Bearer <cualquiera>` devuelve 200 en todo el API) y
que ninguna escritura de perfil pueda perder datos ni salir del directorio de perfiles.

## Contexto del proyecto

- Next.js 16 (App Router) + `next start` en el VPS, un proceso por nodo (PC `:3000`, VPS `:3000`).
- `src/lib/auth.ts` ya define cookie httpOnly (`hermes-pwa-token`) + `setAuthCookie()` / `clearAuthCookie()`
  **y nadie las usa**: hoy la key viaja en `localStorage` del navegador y cada route hace
  `if (!authHeader?.startsWith("Bearer ")) 401`, o sea *cualquier* texto después de `Bearer ` pasa.
- Probes reales contra el VPS (`http://100.124.132.48:3000`):
  `Authorization: Bearer totally-fake-key` → **200** en `/api/profiles` (17 perfiles + `sessionCount`) y **200**
  en `/api/groups/<id>/messages`. Mismo guard en `/api/groups/*/chat`, `/api/chat`, `/api/sessions*`,
  `DELETE /api/sessions/*` y `PATCH /api/profiles`.
- El ruteo cross-node VPS→PC (gateways `:8642`) **funciona y no se toca**.

## Tarea específica

### 1. Un único guard server-side (`src/lib/auth.ts`)

1. Exportar `async function requireAuth(request: NextRequest): Promise<{ ok: true; token: string } | { ok: false; response: NextResponse }>`.
2. Aceptar el token **sólo** de dos fuentes:
   - cookie httpOnly `hermes-pwa-token` (el caso del navegador), o
   - header `Authorization: Bearer <token>` (el caso peer-to-peer VPS↔PC).
3. Validar el token server-side: comparación **exacta y en tiempo constante** (`crypto.timingSafeEqual` sobre
   buffers de igual longitud) contra el set permitido del nodo:
   `[credencial: HERMES_API_KEY]`, `[credencial: HERMES_VPS_API_KEY]`, `[credencial: HERMES_PWA_TOKEN]`.
   Nada de `startsWith("Bearer ")`. Si el set configurado está vacío → responder `503` con
   `{"error":"auth not configured"}` (fail-closed), nunca 200.
4. Aplicar `requireAuth` en **todas** estas rutas, reemplazando el guard local:
   `src/app/api/profiles/route.ts` (GET y PATCH), `src/app/api/groups/route.ts`,
   `src/app/api/groups/[groupId]/messages/route.ts`, `src/app/api/groups/[groupId]/chat/route.ts`,
   `src/app/api/sessions/route.ts`, `src/app/api/sessions/[sessionId]/route.ts`,
   `src/app/api/sessions/[sessionId]/messages/route.ts`, `src/app/api/chat/route.ts`.
   Única excepción: `POST /api/auth/validate` (es el login).
5. Los llamados upstream al gateway usan `HERMES_API_KEY` / `HERMES_VPS_API_KEY` del env y, si faltan,
   el token ya validado del request (comportamiento actual en `groups/[groupId]/chat/route.ts:131-133`), pero
   **nunca** un token no validado.

### 2. Login por cookie y sacar la key del navegador

1. `src/app/api/auth/validate/route.ts`: en el camino `valid:true`, setear la cookie con `setAuthCookie(apiKey)`
   (mismo valor que se acaba de validar) y **dejar de devolver `apiKey` en el body** (hoy lo devuelve:
   echo de credencial al cliente y a cualquier log de red).
2. `src/lib/api.ts`: `getHeaders()` deja de mandar `Authorization`; agregar `credentials: "same-origin"` en
   los `fetch`. El parámetro `apiKey` puede quedar en la firma (para no romper 300 call sites en un commit de
   seguridad) pero **no debe viajar al wire**.
3. `src/app/auth/login/page.tsx`: no escribir en `localStorage`; `clearAuthCookie()` en logout; en el
   `useEffect` borrar cualquier `hermes-pwa-token` legacy que quede en `localStorage`.

### 3. `PATCH /api/profiles` (B1b) — `src/app/api/profiles/route.ts:374-406`

1. Validar `profile` contra el listado real de `PROFILES_DIR` (`fs.readdirSync(PROFILES_DIR, {withFileTypes:true})`,
   sólo directorios, `name === profile` exacto). Rechazar `400` si no matchea: hoy
   `path.join(PROFILES_DIR, profile, "config.yaml")` con `profile="../../profile"` escribe fuera del árbol.
2. Validar `model` con `/^[A-Za-z0-9._:\/-]{1,120}$/` y aplicar el reemplazo con `split`/línea o `JSON.stringify`
   del valor, **nunca** interpolando crudo en YAML (`$1${model}` con newlines = inyección de config).
3. Escritura atómica igual que el punto 4.

### 4. Escrituras de perfil atómicas y verificadas (B5) — `src/lib/hermes-fs.ts:50-61`

1. `saveProfileDoc()`: escribir en `profile.yaml.tmp-<pid>-<rand>` en el mismo directorio → `fsyncSync` → `fs.renameSync`
   sobre el destino → actualizar cache. Devolver `boolean` sigue, pero **quien llama debe chequearlo**.
2. Agregar un mutex in-process (`let chain: Promise<void>`) para el ciclo read-modify-write; exportar
   `async function withProfileDocLock<T>(fn: (doc) => T | Promise<T>): Promise<T>` que hace
   load → fn → save bajo el lock.
3. `src/app/api/groups/[groupId]/chat/route.ts`: usar `withProfileDocLock` para el push del mensaje del usuario
   (línea 117-124) y para el push de la respuesta (línea 259-278). Si el save devuelve `false`, emitir
   `data: {"type":"error","error":"No se pudo persistir el mensaje"}` en el SSE y cortar con `controller.close()`
   en lugar de mostrar en la UI un mensaje que no se guardó.

### 5. Errores upstream honestos (B7) + health

1. Los routes que proxyean al gateway deben propagar el status real: sesión inexistente → `404`;
   gateway caído / timeout → `502`; **nunca** `200` con lista vacía. Aplica a
   `src/app/api/sessions/route.ts`, `src/app/api/sessions/[sessionId]/route.ts`,
   `src/app/api/sessions/[sessionId]/messages/route.ts`, `src/app/api/groups/[groupId]/messages/route.ts`
   (sala inexistente hoy responde `200 {messages:[]}`, ver Fase 2 para el contrato nuevo).
2. Nuevo `src/app/api/health/route.ts` (`GET`, sin auth): `{ ok, node, uptime, profileYaml: bool, profileCount, gateway: {local, vps} }`
   con un probe de 1.5 s por gateway y status `200` / `503` si el perfil o el gateway propio no responden.

## Archivos a tocar

`src/lib/auth.ts` · `src/lib/hermes-fs.ts` · `src/lib/api.ts` · `src/app/auth/login/page.tsx` ·
`src/app/api/auth/validate/route.ts` · `src/app/api/profiles/route.ts` · `src/app/api/chat/route.ts` ·
`src/app/api/sessions/route.ts` · `src/app/api/sessions/[sessionId]/route.ts` ·
`src/app/api/sessions/[sessionId]/messages/route.ts` · `src/app/api/groups/route.ts` ·
`src/app/api/groups/[groupId]/messages/route.ts` · `src/app/api/groups/[groupId]/chat/route.ts` ·
nuevo `src/app/api/health/route.ts`.

## Entorno de ejecución (leer antes de correr nada)

- **Claves:** el set permitido del guard es **el que exista en el env del nodo**, no una lista cableada.
  Hoy: **PC** → `HERMES_API_URL`, `HERMES_VPS_URL`, `HERMES_API_KEY`, `HERMES_VPS_API_KEY` (4);
  **VPS** → esas 4 **+ `HERMES_HOME` y `HERMES_NODE_NAME`** (6). O sea: las únicas claves de autenticación son
  `HERMES_API_KEY` y `HERMES_VPS_API_KEY` (+ `HERMES_PWA_TOKEN` opcional): el guard acepta las que existan,
  **nunca** `HERMES_HOME`/`HERMES_NODE_NAME`/las URLs, y **no** se lo cablea al set de la PC (si queda atado a
  4 nombres, el deploy del VPS se cae por env y el `build` sigue verde).
  Si algo devuelve `503 auth not configured`, el bug es del guard, no del env: **no** se lo arregla ampliando
  el guard ni agregando credenciales al repo.
- **Puertos (¡distinto en cada nodo!).** En la **PC**: hay dos instancias viejas vivas en `:3111` (PID 28792) y
  `:3112` (PID 7160) con el código sin arreglar, `:3000` está libre y el gateway vive en `:8642`. En el **VPS**:
  `:3000` **es el deploy** (`pm2 hermes-pwa`, cwd `/home/hermes/hermes-pwa`, `main` @ `46ca485`, detrás de
  `tailscale serve`) y `:3111`/`:3112` no existen. Reglas: en la PC se prueba **sólo** contra el proceso nuevo
  (`npm run build && npm start` → `:3000`), y **no** se apagan ni reinician los PIDs de `:3111`/`:3112`
  (probar contra ellos da 200 con clave falsa y parece que el fix no funcionó); en el VPS **no se toca `pm2`**
  ni el `:3000` del deploy — ese rollout lo hace el propio nodo con el SHA cerrado.

## Restricciones

- **No tocar** el ruteo de salas ni los gates de `PC_BOTS`/`NODE_NAME` de `groups/[groupId]/chat/route.ts:127-133`
  (el E2E VPS→PC funciona: `bot_start node="PC Local"` + stream real).
- **No tocar** `src/lib/group-registry.ts` ni el log de salas: eso es Fase 2.
- No agregar dependencias. `js-yaml` sigue resuelto por transitiva en este commit (se declara en Fase 3).
- No cambiar copy, layout ni componentes de UI más allá de lo indicado en el punto 2.3.
- Cero secretos en el repo: leerlos siempre del env.
- No romper el login actual: la key que hoy funciona debe seguir entrando, pero terminando en cookie.

## Modo de entrega (lo fija quien lanza; el resto del prompt no cambia)

- **Modo (iii) — recomendado:** un commit en `fix/fase1-auth` **+ push de esa rama** (nunca `main`). Es la única
  que permite el rollout del VPS con `fetch + checkout <SHA>`; `main` queda en `46ca485` hasta que Juan mergee.
- **Modo (ii):** los cambios quedan en la rama **sin commitear**; además de `tsc` + `build`, entregar
  `git diff > <ruta FUERA del repo>/fase1.diff` y el `sha256sum` del árbol, para que la verificación de
  web-auditor quede anclada a algo identificable.
- **Modo (i):** commit local en `fix/fase1-auth`, sin push (el VPS no puede enrollar hasta que haya push).

Higiene del commit (aplica a los tres modos): `.env.local`, `.next`, `*.tsbuildinfo` y `public/sw.js` ya están en
`.gitignore` (verificado con `git check-ignore`), así que `git add -A` no arrastra secretos ni artefactos; **no**
commitear `.env*`, ni `fase1.diff`, ni nada de `.next/`. El `fase1.diff` va **fuera** del repo: adentro lo deja
sucio y rompe el baseline "working tree limpio" del que dependen los criterios.

## Criterios de aceptación

Ejecutados por Antigravity contra el build (`npm run build && npm start`) de su propio nodo y **pegados en el
mensaje de cierre** (comando + status + primeras 2 líneas de body):

1. `tsc --noEmit` = 0 errores; `npm run build` = OK.
2. `Bearer totally-fake-key` → **401** en: `/api/profiles`, `/api/groups`, `/api/groups/<id>/messages`,
   `/api/groups/<id>/chat`, `/api/sessions`, `/api/sessions/<id>`, `/api/sessions/<id>/messages`, `/api/chat`,
   `PATCH /api/profiles`, `DELETE /api/sessions/<id>`.
3. Sin header y sin cookie → **401** en todos los anteriores.
4. Con la key real (cookie, y con `Bearer <key real>` para el caso peer) → **200** en los mismos.
5. `PATCH /api/profiles` con `{"profile":"../../profile","model":"x"}` → **400**, y el árbol de perfiles intacto
   (`git status` del home limpio, ningún archivo fuera de `profiles/<name>/config.yaml`).
6. `PATCH /api/profiles` con `{"profile":"brain-local","model":"a\ninjected: 1"}` → **400**.
7. `.tmp-*` no queda huérfano tras 20 escrituras seguidas; `profile.yaml` parsea igual antes/después.
8. `GET /api/health` → 200 con `profileYaml:true`.
9. Regresión E2E: `POST /api/groups/rmugviqw9-6zez7/chat {"text":"ping","targetBot":"web-auditor"}` con la key real
   → SSE con `bot_start` y una respuesta real (mismo comportamiento que el baseline).
10. `grep -rn "localStorage" src/` no muestra ningún uso de la key como credencial de API.
