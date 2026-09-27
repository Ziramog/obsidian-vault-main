---
tipo: prompt-antigravity
proyecto: hermes-pwa
repo: C:\Projects\hermes-pwa
commit-base: 0265d11 (verde: build + tsc OK)
baseline-dirty: working tree con 13 archivos modificados (+598/-470) y 12 paths sin trackear (medido 2026-09-27) — congelar antes de ejecutar (ver B0)
origen: auditoría web-auditor 2026-09-27
estado: pendiente-aprobación-juan
zona: Hermes/Quarantine (borrador técnico, no validado)
---

# Prompt Antigravity — fix auditoría hermes-pwa (seguridad + robustez)

Verificado por web-builder contra el repo (código leído, no solo el informe) — **v3**.
Estado del baseline: `0265d11` + un working tree en vuelo (rediseño mobile, iconos PWA y un
`PATCH /api/profiles` nuevo). Los bloques **B0 + B1 + B1b + B2 se ejecutan juntos**: separados dejan
la app sin forma de autenticarse, o dejan vivos el bypass y el traversal de escritura.

---

## Objetivo

Reemplazar la auth decorativa de la capa Next por auth real basada en la cookie httpOnly
que ya existe sin usar, sacar la API key maestra del navegador, resolver bien la raíz de
datos de Hermes y dejar la escritura de `profile.yaml` a prueba de corrupción.

## Contexto del proyecto

- Next 16.3.6 (App Router) + React 19 + Zustand. Router de API propio en `src/app/api/**`
  que proxea al gateway de Hermes (`HERMES_API_URL`, default `http://127.0.0.1:8642`).
- Cliente: la API key vive en `localStorage` (`hermes-pwa-token`), se lee en
  `src/app/page.tsx:43` y `src/app/auth/login/page.tsx:15`, se guarda en
  `src/app/auth/login/page.tsx:38`, se pasa como prop por todo el árbol (page.tsx → ChatView,
  GroupChatView, SessionList, GroupList, BotSelector) y viaja como `Authorization: Bearer`
  en cada request (`src/lib/api.ts:5-10`).
- `src/lib/auth.ts` ya tiene `setAuthCookie()` / `clearAuthCookie()` / `getAuthToken()`
  (cookie `hermes-pwa-token`, httpOnly, sameSite lax) pero **nadie la usa**.
- Rutas de disco con auth falsa: `api/profiles/route.ts:73-78`, `api/groups/route.ts:54-57`,
  `api/groups/[groupId]/messages/route.ts:9-12` — solo chequean
  `authHeader?.startsWith("Bearer ")`, cualquier valor pasa.
- `api/auth/validate/route.ts:30` devuelve `{valid:true, apiKey}` (la clave viaja de vuelta en el body).
- `profile.yaml` real: `C:\Users\ingju\AppData\Local\hermes\profile.yaml` (~55 KB, config viva
  del Desktop, contiene `ui_meta.hermes-bots-groups`). **Ojo:** cuando Hermes lanza un proceso,
  `HERMES_HOME` vale `C:\Users\ingju\AppData\Local\hermes\profiles\<perfil>` (verificado en esta
  sesión: `...\profiles\web-builder`), y ahí adentro hay un `profile.yaml` **de 175 bytes que NO
  es el documento de grupos** — es un stub por perfil. Regla correcta:
  si `basename(dirname(HERMES_HOME)) === "profiles"` → la raíz es `dirname(dirname(HERMES_HOME))`.

---

## Tarea

### B0 — Congelar baseline (antes de tocar nada)

- El working tree se movió y **no todo es parte de este fix**: hay un rediseño mobile en vuelo
  (`src/components/{BottomNav,BottomSheet,NewChatSheet,BotDirectory}.tsx`, `src/lib/icon-map.tsx`,
  `public/icons/` ×5, `scripts/generate-icons.ps1`, `iniciar-pwa.bat`, `public/manifest.json`,
  `src/app/layout.tsx`, y `src/app/page.tsx` reescrito), más el `PATCH` nuevo en `api/profiles/route.ts`.
- Primer paso: commitear (o `git stash`) ese estado como baseline propio y **anotar el hash**. Todos los
  criterios de aceptación se verifican contra ese hash: sin hash no son reproducibles, y los servidores
  vivos (3111→PID 28792, 3112→PID 7160) corren el build **anterior** a estos cambios.
- Los números de línea de este prompt son del árbol medido el 2026-09-27. En `page.tsx` (reescrito)
  quedaron viejos: buscá por `apiKey` / `localStorage` en vez de confiar en la línea.

### B1 — Auth real por cookie (crítico)

1. `src/lib/auth.ts`:
   - `getAuthedApiKey(): Promise<string|null>` → lee la cookie con `getAuthToken()`; `null` si vacía.
   - `requireApiKey()` → devuelve la key o lanza/retorna el 401 ya armado, para reusar en handlers.
   - Cambiar la política de `secure`: hoy es `process.env.NODE_ENV === "production"` (línea 15).
     Con `next start` en HTTP sobre LAN, el navegador descarta la cookie `Secure` y el login
     entra en loop silencioso. Calcularla desde la request:
     `secure = new URL(request.url).protocol === "https:" || request.headers.get("x-forwarded-proto") === "https"`,
     con override `HERMES_PWA_COOKIE_SECURE` que acepte **tanto `true` como `false` explícito**
     (`undefined` → derivar del protocolo; `"true"`/`"false"` → forzar). No tocar
     `sameSite: "lax"` ni `maxAge` (30 d): están bien para LAN HTTP.
     Prefijo `__Host-` **solo** cuando `secure === true` — en HTTP plano el navegador rechaza el nombre.
     Mantener el nombre `hermes-pwa-token` cuando no haya TLS.
2. `POST /api/auth/validate`: validar contra `${HERMES_GATEWAY_URL}/v1/models`; si ok →
   `cookies().set(setAuthCookie(apiKey))` y responder **`{valid:true}` sin la clave**.
   Rate limit en memoria (Map IP→timestamps, 5 intentos/min, 429 con `Retry-After`).
   Estado actual a corregir: `validate/route.ts:46` **sigue devolviendo `{valid:true, apiKey}`** (C2 abierto).
   El guard de JSON inválido (línea 11) y el timeout de 5 s con `AbortController` (líneas 27-37) que ya están
   en el working tree están bien: se conservan tal cual.
3. `GET /api/auth/validate` → `{valid: boolean}` según cookie presente (verificando contra el
   gateway con caché de 60 s, para detectar clave revocada). `POST /api/auth/logout` → limpia cookie, 204.
4. Todas las rutas: reemplazar el chequeo de header por `requireApiKey()`:
   `api/profiles` (**GET y el `PATCH` nuevo, línea 184**), `api/groups`,
   `api/groups/[groupId]/messages`, `api/groups/[groupId]/chat`, `api/chat`, `api/sessions`,
   `api/sessions/[sessionId]`, `api/sessions/[sessionId]/messages`.
   **Eliminar, no degradar:** borrar por completo la rama que lee `Authorization: Bearer`
   (no dejarla como fallback ni como "compatibilidad") — si queda, el bypass sigue vivo con el
   mismo `curl`. Único método de auth: cookie. 401 JSON cuando falta o no valida.

### B1b — `PATCH /api/profiles` (traversal de escritura + inyección en el YAML)

`src/app/api/profiles/route.ts:184-210` (introducido por los cambios en vuelo; **no existe en `0265d11`**):
- **Traversal de escritura:** valida con el mismo `startsWith("Bearer ")` decorativo y arma
  `path.join(PROFILES_DIR, profile, "config.yaml")` con `profile` crudo del body. Un `profile` tipo
  `"../../../../Users/x"` resuelve fuera de `PROFILES_DIR` y el `fs.writeFileSync` de la línea 210 pisa
  cualquier `config.yaml` alcanzable del disco C: (el `existsSync` previo limita el blanco a archivos ya
  existentes con ese nombre, no lo hace seguro). Fix: whitelist por `readdirSync(PROFILES_DIR)` + el
  resultado de `path.resolve` debe cumplir `resolved.startsWith(path.resolve(PROFILES_DIR) + path.sep)`;
  rechazar `..`, `/`, `\`, `%2e`.
- **Inyección en el reemplazo:** `content.replace(/(model:...)([^\n\r]+)/, `$1${model}$3`)` mete `model`
  dentro de la *replacement string*, donde `$&`, `$'`, `$1` tienen significado propio, y un `model` con
  saltos de línea inyecta claves YAML arbitrarias en `config.yaml`. Fix: validar con
  `^[A-Za-z0-9._:\/-]{1,64}$` **y** usar replacer función (`(m, p1, p2, p3) => p1 + model + p3`).
- Orden obligatorio: esto entra en el **mismo commit** que B1. Si el auth nuevo se implementa encima sin
  arreglar esto, el endpoint se queda con el bypass heredado más el traversal.

### B2 — Sacar la clave del navegador (crítico, junto con B1)

5. `src/app/auth/login/page.tsx`: borrar `localStorage.getItem/setItem("hermes-pwa-token")`;
   on-mount `GET /api/auth/validate` → si `valid` redirigir a `/`; mostrar 429 como
   "demasiados intentos, esperá un minuto".
6. `src/app/page.tsx`: borrar `useState apiKey` y las lecturas de localStorage (líneas de `0265d11`;
   **`page.tsx` fue reescrito en el working tree**, así que confirmá cada referencia con
   `grep -n 'apiKey\|localStorage' src/app/page.tsx` antes de editar); el gate de boot pasa a ser `GET /api/auth/validate` → si `valid:false`
   `router.replace("/auth/login")`. `handleLogout` (línea 183) → `POST /api/auth/logout` + redirect.
7. `src/lib/api.ts`: `getHeaders()` sin parámetro y **sin** `Authorization` (la cookie viaja sola
   same-origin); quitar el parámetro `apiKey` de `fetchProfiles`, `fetchSessions`, `fetchMessages`,
   `createSession`, `deleteSession`, `sendMessage`, `fetchGroups`, `fetchGroupMessages`,
   `sendGroupMessage`; `validateApiKey` → `checkSession()`. Envolver los 401 del proxy en un error
   tipado (`AuthError`) y propagar `res.status` en vez de genérico.
8. Actualizar el árbol de componentes que recibe `apiKey`:
   `ChatView.tsx` (líneas 14,22,69,74,95,106,126,162), `GroupChatView.tsx`
   (14,20,63,68,88,99,119,171), `SessionList.tsx`, `GroupList.tsx`, `BotSelector.tsx`,
   y los call sites en `page.tsx:463,482`. `npx tsc --noEmit` debe quedar limpio (ese es el
   detector de que no quedó ningún call site viejo).

### B3 — Status upstream propagado

9. `api/sessions/route.ts` (POST `:28-29`, GET `:56-57`), `api/sessions/[sessionId]/route.ts`
   (`:26`, `:55`), `api/sessions/[sessionId]/messages/route.ts` (`:29`):
   mirar `res.ok`; upstream 401 → 401 `{error:"session_expired"}`; 404 → 404; 5xx → 502
   `{error:"upstream_error", upstreamStatus}`; nunca devolver cuerpo de error con HTTP 200.
   En el cliente, `AuthError` dispara redirect a `/auth/login`.

### B4 — Raíz de datos robusta

10. `src/lib/hermes-fs.ts:5-13` — reemplazar el cálculo por una resolución explícita, en este orden:
    1. `process.env.HERMES_PWA_DATA_HOME` (override explícito).
    2. Si `HERMES_HOME` está seteado y `basename(dirname(HERMES_HOME)) === "profiles"` →
       raíz = `dirname(dirname(HERMES_HOME))`.
    3. Si `HERMES_HOME` está seteado y `HERMES_HOME/profile.yaml` existe **y** `HERMES_HOME/profiles`
       es directorio con entradas → raíz = `HERMES_HOME` (caso proceso lanzado a mano sin perfil).
    4. Fallback `%LOCALAPPDATA%\hermes`.
    **Nunca** elegir un `profile.yaml` de un directorio que sea `<raíz>/profiles/<perfil>` (el stub de 175 B).
    Dos restricciones que ya causaron diagnóstico erróneo:
    - El stub **no contiene `hermes-bots-groups`**: usa `ui_meta.hermes-bots.groups`, una lista de
      strings legacy sin logs (grep verificado: stub → `hermes-bots`; real → `hermes-bots-groups`).
      Las salas, `roomId` y logs existen **solo** en `ui_meta["hermes-bots-groups"].rooms` del
      archivo raíz. **No unificar ambos keys** en el refactor: `/api/groups` empezaría a leer una
      lista de nombres sin logs.
    - Prohibido usar heurísticas tipo "el `profile.yaml` más reciente" o de mayor tamaño: los stubs
      tienen su propio mtime.
11. `api/profiles/route.ts:5-11` duplica el cálculo — borrar el duplicado e importar de `@/lib/hermes-fs`
    (en el working tree ese archivo creció a 214 líneas con el `PATCH`: unificá el cálculo ahí también).
12. Fallar fuerte en vez de devolver vacío: si `profile.yaml` no existe → 500
    `{error:"profile.yaml not found", dataRoot: <ruta resuelta>}`; log una vez al arrancar.
13. Agregar `GET /api/health` (sin auth) → `{dataRoot, hermesHome, profileYaml:{path,exists,sizeBytes}, profilesDir:{path,exists,count}}`
    para diagnosticar en un request.

### B5 — Escritura atómica de `profile.yaml`

14. `src/lib/hermes-fs.ts:50-61`: escribir a `profile.yaml.tmp-<pid>-<rand>` en el **mismo** directorio,
    `fsync`, `fs.renameSync` sobre el destino (rename es atómico en NTFS del mismo volumen), con
    reintentos (3, backoff 50/150/400 ms) en `EPERM/EBUSY/EACCES` (AV/OneDrive/Desktop con el archivo abierto).
    Antes de pisar, copiar la versión anterior a `profile.yaml.bak` (rotar 3).
15. Serializar: un mutex en proceso (cadena de promesas) que envuelva leer-modificar-escribir;
    el "reload" de `api/groups/[groupId]/chat/route.ts:193-209` debe pasar a hacer
    read-modify-write **dentro** del lock (hoy el mensaje del usuario ya pisó cambios concurrentes).
16. `saveProfileDoc` devuelve `boolean` y **nadie lo mira**: en `chat/route.ts:107` la falla se traga
    en silencio y el mensaje del usuario se pierde mientras la UI lo muestra. Chequear el retorno y,
    si falla, devolver error explícito (o rollback del push en memoria).
17. Deuda conocida a documentar en el repo (no bloquea): el Desktop también escribe este archivo, así que
    el lock solo cubre nuestra escritura. Objetivo real a futuro: dejar de escribir `profile.yaml`
    directamente (usar API/plugin de Hermes o un store propio de grupos).

### B6 — PWA instalable (A4 ya resuelto en el working tree)

18. **Hecho, sin commitear** (verificado leyendo los archivos, no el informe):
    `manifest.json` con `id`, `scope` y `purpose any|maskable`; 5 PNG en `public/icons/`
    (192/512 + maskable 192/512 + apple-touch-icon 180); `metadata.manifest` + `metadata.icons` +
    `<link rel="apple-touch-icon">` en `layout.tsx`. Ojo: al sacar el `<link rel="manifest">` manual quedó
    la clave `manifest: "/manifest.json"` en los metadatos — verificado que el `<link>` **sigue emitiéndose**.
    Queda solo: commitearlo y verificar en runtime (Chrome → "Instalar app" sin warnings en DevTools →
    Application → Manifest). Los iconos son un monograma "H" dorado sobre tile oscuro, generados por
    `scripts/generate-icons.ps1`: están bien formados (verificado visualmente; el ring del maskable queda
    ~76-79% del ancho, dentro del safe zone) pero son de estética genérica de plantilla — si @user quiere
    el logo real hay que regenerar los 5 PNG cambiando solo el script.

### B7 — Hardening restante (no bloquea B1-B4)

19. Validar segmentos antes de armar la URL del gateway: `profile` debe existir en
    `PROFILES_DIR` (whitelist por `readdirSync`) o matchear `^[a-z0-9][a-z0-9-]{0,63}$`;
    `sessionId` `^[A-Za-z0-9_-]{1,64}$`; `encodeURIComponent` siempre. Rechazar `..`, `/`, `\`, `%2e`
    (hoy `profile=..` alcanza rutas arbitrarias del loopback).
20. `next.config.ts`: `poweredByHeader: false` + headers (`X-Content-Type-Options: nosniff`,
    `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY`); sacar `s-maxage=31536000` del HTML.
21. Deps: agregar `js-yaml` y `@types/js-yaml` a `package.json` (hoy funciona por dependencia
    transitiva); sacar `next-pwa@5.6.0` (duplicado de `@ducanh2912/next-pwa`); `git rm --cached
    public/sw.js public/workbox-*.js` y agregarlos a `.gitignore` (son artefactos de build ya versionados).
22. Lint — medición desglosada (web-builder, working tree del 2026-09-27; los números del baseline
    `0265d11` ya no son comparables porque el árbol se movió):
    - `npx eslint` / `npx eslint .` = **13 errores / 105 warnings**.
    - `npx eslint src` = **12 errores / 19 warnings** (código real, ya incluye los 5 componentes nuevos).
    - `npx eslint public` = **0 errores / 86 warnings** (bundle generado).
    - Inestabilidad comprobada: dos corridas **idénticas** de `npx eslint .` seguidas dieron 118 y 32
      problems, según si el `sw.js` recién regenerado entraba en el linter. Es el argumento definitivo para
      `globalIgnores`: con `public/` afuera el número es estable y comparable entre commits. Corregir
      `set-state-in-effect` en `page.tsx:48,55,140` y `purity` por `Date.now()` en render en
      `ChatView.tsx:30,139,151` — mientras estén, esos componentes quedan fuera de la compilación optimizada.
    - `npx eslint public` = **0 errores / 86 warnings**: ruido puro de `public/sw.js` y
      `public/workbox-f1770938.js` (bundle regenerado en cada build; el conteo sube solo). Agregarlos a
      `globalIgnores` en `eslint.config.mjs` junto a `.next/`, `build/`, `out/`.
    - El error 13 es real y del config raíz: `next.config.ts:3:17`, `require()` en config TS/ESM
      (`@typescript-eslint/no-require-imports`). Fix: `import withPWA from "@ducanh2912/next-pwa"`
      (el `.default()` actual se va con el import).
    Resultado esperado: `npx eslint` = 13 errores / 19 warnings sin tocar código de app.

---

## Archivos a tocar

```
src/lib/auth.ts                      (B1-B2)
src/lib/api.ts                       (B2-B3)
src/lib/hermes-fs.ts                 (B4-B5)
src/app/api/auth/validate/route.ts   (B1)
src/app/api/auth/logout/route.ts     (nuevo, B1)
src/app/api/health/route.ts          (nuevo, B4)
src/app/api/profiles/route.ts        (B1, B4)
src/app/api/groups/route.ts          (B1)
src/app/api/groups/[groupId]/messages/route.ts   (B1)
src/app/api/groups/[groupId]/chat/route.ts       (B1, B5)
src/app/api/chat/route.ts            (B1)
src/app/api/sessions/route.ts        (B1, B3)
src/app/api/sessions/[sessionId]/route.ts        (B1, B3)
src/app/api/sessions/[sessionId]/messages/route.ts (B1, B3)
src/app/page.tsx                     (B2, B7)
src/app/auth/login/page.tsx          (B2)
src/app/layout.tsx                   (B6)
src/components/{ChatView,GroupChatView,SessionList,GroupList,BotSelector}.tsx (B2)
public/manifest.json, public/icons/* (B6)
next.config.ts, package.json, .gitignore (B7)
```

## Restricciones

- No tocar `C:\Users\ingju\AppData\Local\hermes\profile.yaml` a mano ni borrarlo; el Desktop lo usa en vivo.
- No bajar credenciales al cliente ni loguear la API key (`console.log` prohibido con la clave).
- No usar la clave real en pruebas escritas: referenciar `[credencial: HERMES_API_KEY]`.
- No cambiar el design system ni la UI (salvo lo indicado en B6/B7); no refactorizar componentes por gusto.
- No deployar a Vercel: con las rutas de disco publicadas sería exponer `profile.yaml` a internet.
- Un bloque = un commit. B1 y B2 en el mismo commit.

## Criterios de aceptación

```bash
npm run build && npx tsc --noEmit && npx eslint
```

PoC del auditor, todo debe cambiar de resultado. Reparto de tareas: la verificación post-fix la
re-ejecuta **web-auditor** (independiente). Los PIDs 26652/6092 ya no existen; 3111/3112 los tienen ahora
**28792** y **7160**, que sirven el build **anterior** al working tree: hay que reconstruir y relanzar
contra el commit congelado en B0 (`npm run build && npx next start -p 3112`) o los probes no prueban
el código nuevo.

```bash
# 1. Sin cookie → 401 (ya daba 401)
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3112/api/profiles
# 2. Bearer falso → 401 (hoy 200 con 9 perfiles y sessionCount)
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer totally-fake-key" http://127.0.0.1:3112/api/profiles
# 3. Log de sala con Bearer falso → 401 (hoy 200 con los 16 mensajes)
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer totally-bogus" \
  http://127.0.0.1:3112/api/groups/rmugviqw9-6zez7/messages
# 4. Flujo bueno: login → cookie → datos
curl -s -c jar.txt -X POST -H "Content-Type: application/json" \
  -d '{"apiKey":"[credencial: HERMES_API_KEY]"}' http://127.0.0.1:3112/api/auth/validate   # {"valid":true}, SIN apiKey en el body
curl -s -b jar.txt http://127.0.0.1:3112/api/profiles | head -c 200                          # 200 con perfiles
curl -s -b jar.txt -X POST http://127.0.0.1:3112/api/auth/logout -o /dev/null -w "%{http_code}\n"  # 204
curl -s -b jar.txt -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3112/api/profiles      # 401 tras logout
# 5. En navegador: localStorage NO debe contener hermes-pwa-token (DevTools → Application)
# 6. Arrancado con HERMES_HOME apuntando al perfil, /api/health debe mostrar dataRoot = ...\hermes (y no ...\hermes\profiles\x)
# 7. sessions con clave inválida: 401 session_expired, no 200 con "0 conversaciones"
```

- Probe (i) — arrancado con `HERMES_HOME=...\hermes\profiles\web-auditor`, `GET /api/profiles` debe
  devolver los **9 perfiles** (hoy `{"profiles":[]}`). Mismo apunte en `/api/health`: `dataRoot`
  = `...\hermes`, nunca `...\hermes\profiles\<perfil>`, y `profileYaml.sizeBytes` ≈ 55 KB (no 175 B).
- Probe (ii) — en `next start` sobre HTTP, la respuesta de `/api/auth/validate` debe traer
  `Set-Cookie` con `HttpOnly` y **sin** `Secure` (y con `Secure` cuando hay TLS); el navegador debe
  conservar la cookie y el login no debe quedar en loop.
- Un corte de energía durante un mensaje de grupo no debe dejar `profile.yaml` truncado ni sin backup
  (`profile.yaml.bak` presente y parseable).
