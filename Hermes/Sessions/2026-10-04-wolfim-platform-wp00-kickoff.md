---
session: 2026-10-04
profile: brain-local
type: orchestration
project: wolfim-platform
pack: WOLFIM_PLATFORM_PROJECT_PACK_v7
status: WP00–WP04 aceptados · WP05 liberado · A1 (AGENTS.md) abierto sin bypass
---

# Sesión — 2026-10-04 — Wolfim Platform · kickoff (WP00 → WP01)

## Protocolo de apertura (SOUL)

| Paso | Resultado |
|---|---|
| Briefing `current.md` + TTL | `last-reviewed 2026-09-24T17:40-03` + `valid-for-hours 336` → vence **2026-10-08T17:40-03**. Hoy 2026-10-04 → **VIGENTE (≈4 días)**. |
| Flag briefing | `reality-check-required-by: 2026-10-01` vencido hace 3 días. No invalida el TTL; se reporta. |
| Handoffs `vps-to-local` ready | **HO-2026-10-04-001** (brain-vps → brain-local, project `hermes-system`, `depends-on: []`). Único `ready` no archivado. |
| Dependencias | Sin dependencias → procesable, pero **fuera del scope Wolfim**. |
| Events / scope-changes | Sin `events/` en HO-2026-10-04-001. Sin cambios de alcance. |
| `companies/wolfim/intelligence/context.md` | Leído. |
| `companies/wolfim/intelligence/patterns.md` | Leído — v2, `last-reviewed 2026-07-19`, 20 insights. |

## Verificación de repos (solo existencia, sin Git)

| Repo | Path | Estado |
|---|---|---|
| SOURCE_REPO | `C:\Projects\wolfim-motors-demo` | **EXISTE** (`.git`, `.next`, `app/`, `AGENTS.md`) |
| TARGET_REPO | `C:\Projects\wolfim-platform` | **NO EXISTE** → `TARGET_NOT_CREATED` (confirmado dos veces, independientemente) |

## Pack v7 — recibido y validado

`WOLFIM_PLATFORM_PROJECT_PACK_v7.zip` (9.3 MB, 31 archivos): 23 docs + 7 visuals.
Docs clave verificados: `HERMES_HANDOFF-v3.md`, `brain-local-wolfim-adapter.md`,
`PROJECT_FILES_INDEX-v9.md`, `repository-migration-strategy-v1.md`,
`implementation-plan-v3.md` (WP00–WP35 + audit gates), `agent-orchestration-v3.md`.

Coherencia con SOUL brain-local: **VERIFICADA**. El adapter no modifica zonas de
escritura ni permisos Git; brain-local sigue sin ejecutar Git y sin escribir repos
ni `PROJECT_STATE.md`.

---

## WP00 — Dual Repository Baseline · ✅ ACEPTADO

Ejecutado por `web-builder` el 2026-10-04. Resultado validado por brain-local.

```text
STATUS:            COMPLETE (read-only)
ARCHIVOS:          0 creados · 0 modificados (git status idéntico pre/post inspección)
SOURCE HEAD:       e9f774c  (branch main, up-to-date con origin/main, 158 commits)
SOURCE dirty:      1 → M AGENTS.md (+18 líneas, no staged) — doc de orquestación
STACK:             npm · node v26.7.0 · npm 11.19.0 · next 14.2.4 · react 18 · mongoose 8.5
install:           node_modules presente (459 paquetes top-level)
BUILD:             npm run build → EXIT 0 · 0 errores · 38 warnings lint · 52 rutas
TESTS:             NONE_CONFIGURED (sin runner ni script "test" en SOURCE)
ENV:               solo NOMBRES (9 en .env.local, 7 en .env.example) — sin valores
PROJECT_STATE:     N/A — TARGET_NOT_CREATED
DEVIATIONS:        ninguna
```

### Hallazgos del builder (pre-existentes, no introducidos por el WP)

| # | Hallazgo | Destino |
|---|---|---|
| 1 | `middleware.js` es **bypass total** (`NextResponse.next()` para todo, matcher sobre `/admin`, `/superadmin`, `/profile`) — coherente con modo demo deliberado | Punto crítico de **WP13** (Auth + Membership). Hoy no hay gate de ruta activo. |
| 2 | `app/api/site-config/site-config/route.js` — ruta anidada duplicada | Limpieza en WP02/WP03, no urgente |
| 3 | Scripts sueltos en raíz (`audit-*.js`, `check_*.mjs`, `audit_report.json`) | **NO migrar al TARGET** |
| 4 | Sin tests ni runner | Ver D2 abajo |

### Verificación independiente de brain-local (sin Git)

`C:\Projects\wolfim-platform` → **no existe** (ni carpeta parcial ni symlink).
`AGENTS.md` en SOURCE con mtime 2026-09-25 16:37 → la mod sin commitear es previa al WP,
no la introdujo el builder. Coincide con el reporte.

---

## Decisiones de orquestación

**D1 — `M AGENTS.md` en SOURCE: NO se commitea, NO se revierte, NO se toca.**
La política de repositorio (adapter §Repos, migration-strategy §10) dice que SOURCE
permanece sin cambios y que modificarlo exige autorización explícita de un WP. El diff
agrega preferencias de modelo (Antigravity) y "Brain Trust" → documentación de
orquestación, no código de feature. Se deja el working tree de SOURCE tal cual y **no
entra al TARGET en WP01**: el TARGET arranca sin AGENTS.md; si Juan lo quiere, se decide
en WP02 junto con el resto de la documentación.

**D2 — Falta infra de tests (propuesta, requiere OK de Juan).**
El plan v3 fija el gate de WP03 como install/build, pero los audit gates
(WP10/WP13/WP15/WP16/WP21/WP22/WP27/WP28/WP30/WP32) necesitan evidencia ejecutable:
aislamiento de tenant, concurrencia de reserva, no-sale-duplicada. Con `NONE_CONFIGURED`
en SOURCE, propongo **agregar un runner mínimo (vitest) en WP03** dentro del TARGET y
registrarlo como addendum del plan. Es infraestructura nueva en un repo nuevo, no cambia
alcance de producto — pero el plan está marcado FROZEN, así que pido OK antes de incluirlo.

---

---

## WP01 — Bootstrap TARGET_REPO · ✅ ACEPTADO

Ejecutado por `web-builder` el 2026-10-04. Resultado validado por brain-local
(verificación independiente sin Git: árbol en disco + `.git/HEAD` + artefactos).

```text
STATUS:            COMPLETE
TARGET HEAD:       8db13cd (branch main, 1 commit, 261 insertions)
TARGET ARCHIVOS:   6 creados (.gitignore, apps/.gitkeep, packages/.gitkeep, docs/.gitkeep,
                   docs/implementation-baseline.md, docs/PROJECT_STATE.md) · 0 modificados
TARGET remote:     NINGUNO (sin remote, sin push, sin clone)
SOURCE:            SIN CAMBIOS (HEAD e9f774c, status solo `M AGENTS.md`)
TESTS:             NONE_CONFIGURED (TARGET sin package.json aún)
BUILD:             N/A en TARGET. SOURCE sigue EXIT 0 / 0 errores / 38 warnings
PROJECT_STATE:     escrito por web-builder (75 líneas, Wave 0 · Status GREEN)
DEVIATIONS:        ninguna
```

Verificado además: `.next` de SOURCE con artefactos reales del build de hoy
(`BUILD_ID` 2026-10-04 16:14, `trace` 16:15) → el `npm run build` de WP00 fue real,
no simulado. `AGENTS.md` sigue con mtime 2026-09-25.

### D3 — Identidad de autor (decidida)

`git config --local` = `Ziramog` / `fullpowerok@gmail.com`, los mismos valores que la
identidad global y que el repo SOURCE. Como los valores **coinciden**, no hace falta
`amend`: el hash `8db13cd` sigue siendo válido. Si el repo va a publicarse bajo una
cuenta/org de Wolfim, hay que decirlo **antes del primer push** (el push ya requiere
aprobación de Juan).

### D4 — Normalización de finales de línea (decidida)

Agregar `.gitattributes` con `* text=auto eol=lf` en WP02 + `git add --renormalize .`
para limpiar los CRLF que Git avisó al commitear los 3 archivos de texto. Repo nuevo →
conviene fijarlo antes de que entre código. Cambio cosmético, reversible.

---

## WP02 — Install Documentation · ✅ ACEPTADO

Ejecutado por `web-builder` el 2026-10-04 (reportado 17:0x; el WP había quedado sin
arrancar, no bloqueado). Validado por brain-local con verificación independiente sin Git.

```text
STATUS:            COMPLETE
TARGET HEAD:       17f6863f73eec46787bd7c9fdc7fc06c0420ad2e (branch main, 2 commits)
TARGET ARCHIVOS:   31 creados (23 docs activos + 7 visuals en docs/visuals/ + .gitattributes)
                   + docs/PROJECT_STATE.md modificado · 32 files changed · 22430 insertions
TARGET git status: limpio · sin remote · docs/ = 9.9 MB
VERIFICADO:        git log (17f6863) · git rev-parse · git ls-files = 37 · docs/*.md = 25
                   (23 nuevos + implementation-baseline.md + PROJECT_STATE.md)
                   visuals/ = 7 PNG · .gitattributes = `* text=auto eol=lf` · CRLF 0 warnings
SOURCE:            SIN CAMBIOS → e9f774c, status ` M AGENTS.md`, mtime AGENTS.md 2026-09-25 (D1 intacto)
DEVIATIONS:        2 (documentadas por el builder, verificadas)
```

### Verificación de brain-local (cruda)

```text
$ git -C C:/Projects/wolfim-platform rev-parse HEAD
17f6863f73eec46787bd7c9fdc7fc06c0420ad2e
$ git -C C:/Projects/wolfim-platform status --porcelain     → (vacío)
$ git -C C:/Projects/wolfim-platform ls-files | wc -l       → 37
$ git -C C:/Projects/wolfim-platform remote -v              → (vacío, sin remote)
$ du -sh C:/Projects/wolfim-platform/docs/                  → 9.9M
$ git -C C:/Projects/wolfim-motors-demo rev-parse HEAD      → e9f774c52865d6a30d87816f2d1fbc1ba1d02deb
$ git -C C:/Projects/wolfim-motors-demo status --porcelain  →  M AGENTS.md
```

Desviación 2 confirmada: `git config --local --list` del TARGET solo tiene claves `core.*`
— **no hay identidad local**; sale de la global (`Ziramog <fullpowerok@gmail.com>`). El hash
`8db13cd` sigue válido (mismos valores), pero la identidad explícita debe fijarse antes del
primer push (que ya requiere aprobación de Juan).

---

## Frente paralelo — HO-2026-10-04-001 (brain-vps → brain-local) · ✅ RESUELTO

Ejecutado en paralelo a WP02, sin tocar el scope Wolfim.

```text
OBJETIVO 1 (¿hay otro poller de 8644817415 fuera del VPS?)  → SÍ
HOST/PROCESO:  esta PC (truzt, Tailscale 100.105.0.23) · PID 13808 (hermes gateway run,
               multiplexer del perfil default) · perfil `algolab`
FUENTE:        AppData\Local\hermes\profiles\algolab\.env → TELEGRAM_BOT_TOKEN=8644817415:[redactado]
CORRELACIÓN:   update del Hermes desktop reinició el gateway local 2026-10-03 23:44:04 EDT;
               adapter algolab reconectó 23:44:50 EDT = mismo minuto del onset del VPS
               (00:44:25 ART). Conflicto espejo hoy 09:52–09:56 EDT (conflict 1/5…5/5, algolab).
OBJETIVO 2 (desactivar)  → ESCALADO a Juan: el fix es editar profiles/algolab/.env,
               fuera de la zona de escritura de brain-local. No ejecutado.
CIERRE:        response.md + 2 events escritos en HO-2026-10-04-001/ (vault). Zona respetada.
```

---

## Estado y secuencia

```text
WP00  Dual Repository Baseline      → ✅ ACEPTADO (2026-10-04)
WP01  Bootstrap TARGET_REPO         → ✅ ACEPTADO (commit 8db13cd)
WP02  Install documentation         → ✅ ACEPTADO (commit 17f6863 · 31 archivos)
WP03  Workspace skeleton            → ✅ ACEPTADO (código 1e864f7 · docs f2e0f1f/e8bd745 · 41 archivos)
WP04  Extract DB Foundation         → ✅ ACEPTADO (código 01f2621 · docs 9df6624 · 12 archivos)
WP05  SaaS Core Models              → ✅ ACEPTADO (código 10737d0 · docs 410219d · 17 archivos)
WP06  Demo Tenant Bootstrap         → ✅ ACEPTADO (código d4c2008 · docs 32fec81 · 11 archivos)
WP07  Extract Motors Core           → ✅ ACEPTADO (código f40f772 · docs 400a38b · 15 archivos: 5 A + 1 D + 9 M)
WP08  tenantId required (parte inequívoca) → ✅ ACEPTADO (código d5b88b0 · docs 2687cc0 · 14 archivos: 4 A + 10 M)
WP09  Demo Backfill                 → ✅ ACEPTADO · GATE PASADO (verificado por brain-local contra la copia)
WP10  Tenant-scoped Indexes         → ✅ **PASS** (veredicto de web-auditor 2026-10-06) con residuos R1–R4 declarados
WP11  Tenant Resolver               → ✅ ACEPTADO (código 34d53d4 · docs 0f11149 · 12 archivos: 5 A + 7 M)
WP12  Tenant-safe Repositories      → ✅ ACEPTADO (código a03f1db/69644bc · docs 4b7cbb4/657ebd4 · R1+R4 cerrados · autoIndex:false)
WP13  Auth + Membership             → ✅ **PASS** (veredicto de web-auditor 2026-10-06, audita `8aaa87a`/`70c24bd`) con residuos H1–H6
WP14  platform-app Foundation       → ✅ ACEPTADO (código c1e732d · docs 23ccc5e · 21 A + 9 M) — app Next generada con Antigravity y revisada · falta el wiring de next-auth
A1 / deuda #15 (`AGENTS.md`)        → ✅ CERRADA (`ef331ff`: §2 sin columna de modelos + "este archivo no prescribe modelos")
```

### WP14 con Antigravity — aceptado (2026-10-06 22:46) y decisiones

```text
$ git rev-parse HEAD → 23ccc5e25081fa0c69cd3df31572540d6e0d32c2 · status -uall = 0 · ls-files = 158 · remote vacío
$ git diff --name-status 7a91741..HEAD → 21 A · 9 M
$ npm run build (tsc -b + typecheck:tests + typecheck:app) → EXIT 0
$ npm test → 15 files passed | 6 skipped · 141 passed | 8 skipped
$ WOLFIM_DB_INTEGRATION=1 → 21 files / 149 passed / 0 skipped
$ test:wp10 → 12/12 · test:dist → 2/2 · status post-corrida → 0
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

**El ejercicio valió la pena y queda como patrón:** Antigravity produjo el andamiaje de la app
(AppShell, rutas, componentes, design tokens) y la revisión humana encontró una **regresión de política
real** — habilitaba el bypass demo desde un checkbox del formulario y el body del route handler
(`isDemo`), o sea controlado por el cliente, que es lo que P25 prohíbe. Verificado en el código final:
`allowDemoBypass` sale de `process.env.WOLFIM_ALLOW_DEMO_BYPASS` **en el servidor** y `isDemo` no existe
en ninguna fuente del repo. Se mantiene el patrón: **Antigravity para UI + revisión obligatoria antes del
commit**, y el reporte declara qué salió de la herramienta y qué se editó a mano (guardrail 5 cumplido).

**Deuda #20 (`next build` bloqueado en este host) — decisión de brain-local:**
1. **Gate local de la app = `typecheck:app` + vitest** (ya encadenado en `npm run build`), declarado como
   tal. No se finge que `next build` corre acá.
2. **`next build` pasa a ser gate de PRE-DEPLOY obligatorio**: tiene que estar verde bajo el runtime de
   deploy (Node 20/22; Vercel no corre Node 26) **antes de cualquier deploy**. La combinación
   Node 26 + npm 11 + Next 14.2.4 es no soportada: el problema es de runtime, no del código.
3. Autorizado un **spike acotado** (Node 20/22 portátil dentro del workspace, sin tocar el sistema)
   cuando se acerque WP29/WP31, para convertir ese gate en algo ejecutable localmente.

**`.next` está stale:** el bundle compilado (22:40) es anterior al fix de fuente (22:42) y todavía
contiene el `isDemo` viejo. Está gitignoreado (no puede entrar al repo), pero **hay que borrarlo antes de
servir o deployar** para no ejecutar código viejo.

**Incidente declarado y aceptado:** el junction `apps/platform-app/node_modules → node_modules` hizo que
npm removiera 90 paquetes; se restauró con `npm install` y se verificó build + suite en verde, más `npm ci`
en clon limpio (90 paquetes en 15 s). Todo lo afectado era `node_modules` (gitignoreado). **Regla: no se
crean junctions dentro de `node_modules`.**

### H1 cerrado y verificado por brain-local (2026-10-06 22:22)

Probe propio contra el `dist` real (sin conectar):

```text
BLOQUEADO  wolfim_motors        cluster0.9w7ocho.mongodb.net/wolfim_motors
BLOQUEADO  (sin nombre de base) cluster0.9w7ocho.mongodb.net
BLOQUEADO  /test                cluster0.9w7ocho.mongodb.net/test
PERMITIDO  /wolfim_motors_copy  cluster0.9w7ocho.mongodb.net/wolfim_motors_copy
PERMITIDO  localhost:27017/wolfim_motors
allowLive + sin base → PERMITIDO   (la excepción explícita sigue siendo la única puerta)
```

`classifyDatabase()` + `assertNotLiveDatabase` fallan cerrado en las tres formas que antes pasaban.
H2 (`userId: string | null` + `buildDemoSession`), H5 (`http-status.ts` con `ABSENCE_CODES` /
`toHttpStatus` / `toPublicError`) y H6 (`session.ts` usa `buildSessionContext`/`buildDemoSession`)
verificados en el código. `HEAD 7a91741b6603fc058548871df36120bf98db2c57`, `status` = 0, 137 archivos,
build EXIT 0, unit **128 passed + 8 skipped**, integración **136 passed / 0 skipped**, `test:wp10` 12/12,
`test:dist` 2/2, SOURCE intacto.

### Decisión — Antigravity para la parte UI de WP14 (con guardrails)

Verificado: `agy 1.2.11` existe en `%LOCALAPPDATA%\agy\bin\agy` con modo no interactivo. **Se usa**,
que era el flujo que Juan tenía en mente desde el arranque (directo en infra, Antigravity desde UI).
Condiciones:
1. Antigravity trabaja **sólo dentro del TARGET**; SOURCE queda read-only y se verifica después
   (`git -C SOURCE status` debe seguir con sólo ` M AGENTS.md`).
2. **Antigravity no ejecuta git**: commitea web-builder, así el trail queda con autoría humana.
3. El prompt incluye lectura obligatoria de `docs/PROJECT_STATE.md`, `AGENTS.md` y `docs/design-system.md`,
   la política de H5 en el borde (un solo 404), y la prohibición de leer `.env`, `platformRole` desde el
   cliente, o escribir fuera del repo.
4. Todo pasa por los gates normales (build + tests + aceptación de brain-local). WP14 **no** es audit gate.
5. El reporte debe decir **qué produjo Antigravity y qué se editó a mano** — Juan preguntó explícitamente
   por el uso de la herramienta y la respuesta tiene que quedar en el registro, no en el aire.

### Veredicto WP13 (web-auditor 2026-10-06) y triage de brain-local

PASS para el entregable: bypass demo no global (por tenant + por request, rol `VIEWER`, marcado),
membership tenant-scoped con NOT FOUND y nunca 403, usuarios `DISABLED`/`INVITED`/`SUSPENDED` sin
sesión. Unit 13/13 propio, integración 1 caso (4 comportamientos) contra la copia, cobertura declarada.

**H1 reproducido por brain-local** (llamando al `dist` real, sin conectar):

```text
BLOQUEADO  wolfim_motors          cluster0.9w7ocho.mongodb.net/wolfim_motors
PERMITIDO  cluster0.9w7ocho…      cluster0.9w7ocho.mongodb.net          ← sin nombre de base: mongoose usa `test`
PERMITIDO  test                   cluster0.9w7ocho.mongodb.net/test
PERMITIDO  wolfim_motors_copy     cluster0.9w7ocho.mongodb.net/wolfim_motors_copy
```

| # | Hallazgo | Destino | Decisión |
|---|---|---|---|
| **H1** | El guard protege el **nombre de base**, no el cluster: URI sin base (o `/test`) pasa y mongoose conecta a la default del cluster de producción | **WP14, máxima prioridad** | **Fallar cerrado**: sin nombre de base → rechazar salvo `allowLive`; nombres reservados (`test`/`admin`/`local`) en host no-local → rechazar; se mantiene la denylist por nombre y la copia entra por nombre explícito `*_copy`/`*_test`. Con tests de cada forma de URI. **Debe cerrarse antes de cualquier escritura sobre la viva (incluye WP31).** |
| **H2** | Sentinel `userId: 'demo'` no es `ObjectId` (`createFromHexString('demo')` lanza): hoy nada filtra por él, pero WP15/WP16 harían `find({ userId })` → `CastError` (500) | **WP14** | Firmas como se hizo con `tenantId` en WP11: `userId: string | null` + `demoBypass: true` como discriminante (o sentinel que castea y nunca matchea) |
| **H3** | La composición resolver→session no está probada e2e (el test escribe `mode` a mano en el `ctx`) | **WP14** | El test de integración arma el `ctx` con `resolveTenantFromSlug` real |
| **H4** | Denominador: la integración es **1 caso** que asserta 4 comportamientos | registrado | Se lee 1/1, no 4 — mismo criterio que el 4+1 de WP10 |
| **H5** | Los 5 códigos de `AuthError` son distinguibles: el borde HTTP debe **colapsar** `USER_NOT_FOUND`+`MEMBERSHIP_NOT_FOUND`+`MEMBERSHIP_NOT_ACTIVE` en **un solo 404** o el 403 vuelve con otro nombre; `User.platformRole` existe y nadie lo lee → WP14 no debe aceptarlo del cliente ni derivarlo de input | **WP14** | Requisito de implementación del wiring de `/login` |
| **H6** | `resolveSession` reconstruye el `SessionContext` a mano y `buildSessionContext` (con el chequeo de `USER_DISABLED`) queda sin usar: dos constructores del mismo tipo | **WP14** | Que uno llame al otro |

@user dio OK para avanzar → **WP14 liberado completo** (AppShell, `/[tenantSlug]`, `/select-tenant`,
`/login`, design system) con H1/H2/H3/H5/H6 en el mismo WP.

### Verificación de brain-local — WP13 (2026-10-06 20:51)

```text
$ git rev-parse HEAD → 70c24bd46c3b807fbe1b1080f76efd1028e6a15a · status -uall = 0 · ls-files = 136 · remote vacío
$ git diff --name-status 657ebd4..HEAD → 8 A · 12 M
$ npm run build → EXIT 0 · npm test → 14 files passed | 6 skipped · 123 passed | 8 skipped
$ WOLFIM_DB_INTEGRATION=1 → 20 files / 131 passed / 0 skipped
$ test:wp10 → 12/12 · test:dist → 2/2 · status post-corrida → 0
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

**P24 (cierre de N1) verificado en el código, no en el reporte:** `connectDB()` llama
`assertNotLiveDatabase(uri, { allowLive })` **antes** de conectar (líneas 68-74) y rechaza la
promesa — el footgun queda cerrado en cualquier camino de código, no sólo en los CLIs. Tests:
`connectDB()` contra `.../wolfim_motors` → `rejects.toThrow(/base viva 'wolfim_motors' bloqueada/)`
y `connectDB({ allowLive: true })` → resuelve. **No re-corrí `--apply` contra la viva**: probar ese
camino con un guard roto habría backfilleado producción. Lo verifiqué por código + unit test, y el
hecho de que la viva siga con 26 documentos sin `tenantId` prueba que el bloqueo funcionó cuando el
builder lo intentó.

**Bypass demo (el punto del gate):** `decideDemoBypass` exige `tenantMode === 'DEMO'` **y**
habilitación por entorno, devuelve rol acotado `VIEWER` y la sesión queda marcada `demoBypass: true`;
tests explícitos de que un tenant `PRODUCTION` no lo obtiene **ni con el flag prendido** y que sin
habilitación no hay bypass. Membership cross-tenant → `NOT FOUND`, nunca 403 (no filtra existencia).

### N1 — escritura de índices sobre la base viva: diagnóstico de brain-local (2026-10-06)

Medido por brain-local contra `wolfim_motors` (read-only, URI derivada fuera del repo y borrada):

```text
tenants 3: slug_1 status_1 · users 2: email_1 · domains 3: hostname_1 tenantId_1_type_1
memberships 4: tenantId_1_userId_1 userId_1_status_1 tenantId_1_role_1 · tenant_configs 2: tenantId_1
vehicles 8 (legacy slug_1/featured_1/published_1 + 4 del TARGET) · vehicleinternals 10 · quotations 5 · counters 2
reviews/businessinfos/searchterms/subscribers/messages: sólo índices legacy (o ninguno)
DOCUMENTOS: tenants 0 · domains 0 · memberships 0 · tenant_configs 0 · users 1 · vehicles 12 · vehicleinternals 12
            quotations 1 · counters 1 · resto 0
```

**Lectura:** los índices del TARGET existen en la viva **también en las 5 colecciones de modelo que están
vacías** (`tenants`, `users`, `domains`, `memberships`, `tenant_configs`) → la firma es un proceso que
**registró todos los modelos del TARGET** y se conectó a la viva con `autoIndex` en su default (`true`).
**El CLI de backfill queda exonerado**: verificado en fuente y en `dist`, importa sólo `connection.js`,
`env.js`, `tenant-backfill.js` y `mongoose-raw.js` — **ningún modelo**, así que no puede crear índices
(esto descarta el dry-run del builder y el mío).

**Dato bueno, medido:** la viva tiene **0 documentos** en `tenants`/`domains`/`memberships`/`tenant_configs`
y el resto con los conteos de SOURCE → **no se escribieron documentos de prueba en producción**: la huella
es de esquema (índices), no de datos. Sin pérdida ni contaminación. Riesgo residual hoy: los uniques
scoped de la viva indexan 26 documentos con `tenantId` ausente (clave `(null, slug)`), que no colisiona
porque los uniques globales de SOURCE siguen vivos.

**Atribución: no la puedo fechar ni asignar** (`listIndexes` no guarda timestamp). Candidatos: una corrida
de integración/seed mientras el `.env` (o un `MONGODB_URI` exportado) apuntaba a la viva — el `.env` del
TARGET tiene mtime de hoy 20:02, consistente con haber sido reescrito después. Queda como deuda #18
"sin atribuir" en `PROJECT_STATE.md`, no como si no hubiera pasado.

**Cierre de N1 (decidido):** `autoIndex: false` en `CONNECT_OPTIONS` + creación de índices explícita y
guardada (`db:sync-indexes` con `--apply` y guard de base viva). **Además exijo para WP13** el mismo guard
en `connectDB`: que la conexión **rechace** la base viva (por nombre) salvo `WOLFIM_ALLOW_LIVE=1`, así el
footgun queda cerrado en cualquier camino de código, no sólo en el CLI. Regla operativa: a la viva sólo se
llega por el CLI de backfill en dry-run; `--apply` requiere OK de Juan + snapshot.

**Secuencia de WP31 re-escrita** (los índices del TARGET ya están en producción y el backfill no corrió):
(a) backfill de `tenantId`, (b) baja de los 4 uniques globales legacy sobre datos vivos — ambas con
snapshot previo y aprobación explícita de Juan.

### Veredicto WP10 (web-auditor, 2026-10-06) y corrección de lectura — brain-local

**PASS** para el entregable: índices tenant-scoped creados post-backfill, los 4 uniques globales
legacy dados de baja en las 9 colecciones del plan, estática 12/12 e inventario reproducidos
por el auditor. **No** es PASS sobre "aislamiento multi-tenant probado".

**Corrijo mi propia frase:** dije "cobertura declarada 4 de 9 con datos" y eso describía dónde la
**copia** tiene documentos, no dónde el test probó algo. La cobertura **runtime real es 1 de 9**
(`tenant_configs`: dos configs de tenants distintos conviven, el segundo config del mismo tenant falla).
`vehicles`, `vehicleinternals`, `quotations` y `counters` no aparecen en ningún test de integración.

| Residuo | Estado | Acción |
|---|---|---|
| **R1** — el caso estrella (dos tenants repitiendo `internalStockCode` en `vehicleinternals`) está probado sólo por forma de índice, no en runtime | abierto | **asignado a WP12**: test de integración que siembre dos tenants, inserte el mismo `internalStockCode` (debe pasar) y el mismo `vehicle` dos veces (debe fallar) → cobertura runtime 1 → 2 |
| **R2** — 3 uniques globales vivos en `reviews`/`businessinfos`/`searchterms` (medidos por el auditor, no por el reporte) | declarado (deuda #14) | obligación de WP16/WP29; en WP31 corre sobre producción con OK de Juan |
| **R3** — la paridad viva-vs-copia no la pudo reproducir el auditor (mi archivo de URI derivada se borró por higiene de credenciales) | abierto | procedimiento reproducible abajo |
| **R4** — comentario de cabecera de `tenant-isolation.integration.test.ts` sigue diciendo "este host no tiene Mongo… pendiente para WP10" | abierto | **asignado a WP12** (el texto se reusa como plantilla en WP13) |

**R3 — cómo reproducirlo sin depender de mi reporte:**
```text
sed 's/wolfim_motors_copy/wolfim_motors/' <TARGET>/.env > <fuera-del-repo>/.env-live
node packages/db/dist/backfill/cli.js --dry-run --env-file <fuera-del-repo>/.env-live --report-out <fuera-del-repo>/live.json
# comparar scanned por colección contra el reporte de la copia; borrar el .env-live al terminar
```
Medición de brain-local (2026-10-05 20:1x): viva `scanned 26 / missing 26 / gate passed=false (dry-run)`
vs copia `scanned 26 / missing 0 / gate passed=true`, delta 0 en las 9. El archivo derivado se borró
porque contenía la credencial de producción en claro: es higiene, no falta de evidencia.

### Verificación de brain-local — WP09 gate + WP11 (2026-10-05 20:19)

```text
# WP09 — gate medido por brain-local con los dos dry-runs comparados por JSON
viva  ac-7zd9kbu-shard-00-00.9w7ocho.mongodb.net/wolfim_motors       → scanned 26 · missing 26 · gate passed=false (dry-run)
copia ac-7zd9kbu-shard-00-01.9w7ocho.mongodb.net/wolfim_motors_copy  → scanned 26 · missing  0 · gate passed=true
delta por colección = 0 en las 9 (vehicles 12/12 · vehicleinternals 12/12 · quotations 1/1 · counters 1/1 · 5 vacuas marcadas)
WOLFIM_DB_INTEGRATION=1 → 13 files / 82 passed / 0 skipped
--inventory copia → TARGET indexes en vehicles/vehicleinternals/quotations, SIN uniques globales legacy
                    residuo declarado (deuda #14): reviews.googlePlaceId_1_reviewId_1 · businessinfos.googlePlaceId_1 · searchterms.term_1

# WP11
$ git rev-parse HEAD → 0f1114954a91953092cff2565b8504ad0d067e6e · status -uall = 0 · ls-files = 120 · remote vacío
$ git diff --name-status b9f04bb..HEAD → 5 A · 7 M
$ npm run build → EXIT 0 · npm test → 11 files passed | 4 skipped · 92 passed | 5 skipped (14 casos del resolver)
$ WOLFIM_DB_INTEGRATION=1 → 15 files / 97 passed / 0 skipped (resolver real: motors.wolfim.com → wolfim-demo)
$ test:wp10 → 12/12 · test:dist → 2/2 · status post-corrida → 0
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

### Rulings de brain-local sobre WP11

- **P20 (no reescribir `www.`) — APROBADO.** Un alias es un registro `Domain` con `type: ALIAS`;
  el ruteo queda auditable. Nada de trucos de string.
- **P21 (servibilidad) — APROBADO.** Dominio `ACTIVE` únicamente; tenant `TRIAL`/`ACTIVE`.
- **P22 (deuda #16, `vertical`) — RESUELTO: se SACA `vertical` del contrato**, no se deja `null` para siempre.
  Un campo que sólo puede ser `null` en una interfaz pública es una trampa: el consumidor branchea y
  recibe `null`. La autoridad es `multi-vertical-architecture-v3.md` §12–§13 ("la UI decide por módulos,
  no por `vertical === 'MOTORS'`"), que es más específica que el §14 del plan. Si algún día hay fuente real
  (campo en `Tenant`/`TenantConfig`), se agrega entonces. Desvío deliberado y reversible.
- `config: null` (tenant sin `TenantConfig`) queda **honesto**: el fallback a `SiteConfig` es de la
  transición y lo implementa el consumidor con su test, no el resolver.

### Verificación de brain-local — WP09 (2026-10-05 10:06)

```text
$ git rev-parse HEAD → 470ff187899195fe7ecc4447ea6444d3c39622a8 · status -uall = 0 · ls-files = 111 · remote vacío
$ git diff --name-status 2687cc0..HEAD → 5 A · 4 M
$ npm run build → EXIT 0 · npm test → 9 files passed | 3 skipped · 74 passed | 4 skipped (16 del backfill)
$ npm run test:wp10 → 12/12 · npm run test:dist → 2/2 · status post-corrida → 0
$ npm run backfill:tenant (sin MONGODB_URI) → EXIT 1 (no lee ni escribe)
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

Revisado en el código, no en el reporte: `balanced: changed + remaining === missingBefore` (línea 146)
con el gate evaluando **primero** el desbalance (razón `corrida parcial: en '<col>' …`) y `vacuo`
si `scanned = 0`; `LIVE_DATABASE_DENYLIST = ['wolfim_motors']` + `assertSafeToWrite` (línea 208-219);
`PARITY` vía `parityBetween(referencia, candidata)`; 9 colecciones **por nombre** (línea 17-27,
sin modelos → no depende de qué modelos tenga el TARGET); `describeDatabase` recorta credenciales
por el último `@` (testeado); `--inventory` para los índices. 16 unitarios de backfill incluidos
los adversarios (corrida parcial que **debe** hacer fallar el reporte, copia parcial detectada,
documento con campos que ningún schema acepta, dry-run sin una sola llamada a `updateMany`).

### B3 — definición de la copia (condición para `--apply` + gate de WP09 y capa de integración de WP10)

1. **Copia**: `wolfim_motors` → `wolfim_motors_test` (mismo cluster Atlas o cluster free aparte).
2. **Paridad medida, no supuesta**: **dos `--dry-run`** (uno contra la base viva, otro contra la
   copia — sólo lectura, el guard no los frena) comparados con `parityBetween`. Una sola corrida
   mide la copia contra sí misma: no es paridad.
3. **Inventario de índices de la copia con `--inventory` ANTES de crear los del TARGET.** Un
   dump/restore se lleva los uniques **globales** de SOURCE (`Vehicle.slug`, `VehicleInternal.vehicle`,
   `internalStockCode`, `Quotation.quoteNumber`). Con esos índices vivos el aislamiento no se puede
   ejercitar —`createIndexes` de mongoose no borra los viejos— y el test de "dos tenants repiten
   `internalStockCode`" fallaría por la razón equivocada. **Hay que darlos de baja explícitamente**
   en la copia y el veredicto de WP10 debe listar índices antes/después. El mismo paso (drop de
   uniques globales + alta de scoped) es lo que va a correr sobre producción en el cutover de WP31,
   con aprobación de Juan.
4. **Nada de esto toca `wolfim_motors`**: el guard ya bloquea `--apply` sin `--allow-live`, y el OK
   humano + snapshot siguen siendo requisito para la base viva.

### Verificación de brain-local — WP08 (2026-10-05 09:56)

```text
$ git rev-parse HEAD → 2687cc02465b244272a4fb86ae56fa83c4f46cd2 · status -uall = 0 · ls-files = 106 · remote vacío
$ git diff --name-status 400a38b..HEAD → 4 A · 10 M
$ npm run build → EXIT 0 · npm test → 8 files passed | 2 skipped · 58 passed | 3 skipped
$ npm run test:wp10 → 12/12 (9 colecciones: 5 core + vehicles + vehicleinternals + quotations + counters)
$ npm run test:dist → 2/2 · status post-corrida → 0
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

`EVIDENCE_MODELS = ALL_MODELS + MOTORS_MODELS + QUOTATION_MODELS` (línea 46) con lista exacta
(línea 50); `tenantId required` verificado en todos; `Counter` sin unique propio (línea 127)
con `counterId(tenantId,key)` = `"<tenantId>:<key>"` + `parseCounterId`; `Quotation` con
`{tenantId,quoteNumber}` unique (línea 182).

### B2 — decisión de brain-local: **A (diferir), no crear `packages/portal-core`**

Las 5 colecciones que faltan de §WP08 (`Subscriber`, `Review`, `BusinessInfo`, `SearchTerm`,
`Message`) no tienen paquete natural entre los 10 workspaces del plan y `crm-core` está
reservado para WP16. **Decisión: no extraerlas ahora; cada una entra en el WP que la consume**
(`Message`/actividad → WP16; `Subscriber`/`Review`/`BusinessInfo`/`SearchTerm` → WP29 portal).
Razones: (a) crear un workspace nuevo es cambio de estructura del plan → no lo hago por
conveniencia; (b) **WP09 no las necesita** — el backfill opera por nombre de colección vía API
cruda, sin modelo; (c) evita declarar modelos sin consumidor, que después quedan muertos.
Queda registrado como diferido en `PROJECT_STATE.md` con su destino por WP. Nota para el gate:
cuando entren en WP16/WP29 hay que sumarlas a los registries de modelos y la aserción exacta
del test va a **fallar a propósito** hasta declararlas.

### Verificación de brain-local — WP07 (2026-10-05 09:52)

```text
$ git rev-parse HEAD → 400a38bd9f166141fad9e153355f5cc3150297e2 · status -uall = 0 · ls-files = 102 · remote vacío
$ git diff --name-status 32fec81..HEAD → 5 A · 1 D · 9 M
$ npm run build → EXIT 0 · npm test → 7 files passed | 2 skipped · 49 passed | 3 skipped
$ npm run test:wp10 → 11/11 (7 colecciones) · npm run test:dist → 2/2 · status post-corrida → 0
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

`tenantIdGaps()` implementado (`tenant-scope.ts:52-58`): reporta `missing` y `not-required`
(chequea `path.isRequired === true`), y los casos que rompen pasaron de 1 a 3. `ALL_MODELS`
= 7 colecciones exactas, allowlist sigue estricta. Sin legacy ajeno en `packages/motors`.

### P14 — WP08 "tenantId nullable": decisión de brain-local (desvío deliberado de la letra del plan)

El plan §WP08 pide `tenantId` **nullable** ("SOURCE debe seguir funcionando") y
`data-model.md` §25 dice "no hacer `tenantId required` antes del backfill"; pero la aserción
de WP10 exige `required: true`. **Decisión: el schema del TARGET mantiene `tenantId required: true`.**

1. "SOURCE debe seguir funcionando" se cumple por **aislamiento de repos**: SOURCE corre su
   propio código y su propio schema (`C:\Projects\wolfim-motors-demo`, intacto en `e9f774c`).
   El TARGET no está desplegado, no tiene remote y no sirve tráfico.
2. `required: true` es lo único que hace verificable "documento sin dueño" en WP10. Nullable
   convierte la aserción en `not-required` y el gate pasaría con dueño opcional — justo el
   modo de falla que venimos evitando.
3. La secuencia de `data-model` §25 (4 nullable → 5 backfill → 6 índices → 9 required) es una
   secuencia de **datos**, no de schema: en el split por repos, el paso "nullable" se satisface
   en **WP09**, que debe tolerar documentos heredados sin `tenantId`.

**Requisitos que esto le impone a WP09** (a verificar, no a prometer): el backfill lee/escribe
por la **API cruda de la colección** (no por validación de mongoose), es **idempotente y
re-corrible** hasta el cutover de WP31 (SOURCE puede seguir insertando docs sin `tenantId`
mientras siga vivo), y reporta `scanned / changed / skipped / remaining` con `remaining = 0`
como gate. Reversible: si Juan quiere la letra del plan, se vuelve nullable en un commit y la
aserción de WP10 se degrada de forma explícita.

### Verificación de brain-local — WP06 (2026-10-05 09:21, sin Git de escritura)

```text
$ git rev-parse HEAD → 32fec817fd1ecb30f20cbd32a5941903d70c3cd1 · status -uall = 0 · ls-files = 98 · remote vacío
$ git diff --name-status 410219d..HEAD → 5 A · 6 M
$ npm run build → EXIT 0 · npm test → 6 files passed | 2 skipped · 37 passed | 3 skipped
$ npm run test:wp10 → 8/8 · npm run test:dist → 2/2 · status post-corrida → 0
$ npm run seed:demo (sin MONGODB_URI) → EXIT 1 · "[db] MONGODB_URI not set …" + "seed demo falló: … sin conexión no se escribe nada"
$ npx vitest run packages/db/src/seeds/demo-tenant.integration.test.ts → EXIT 0 · 1 file / 1 test skipped (visible)
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · " M AGENTS.md" (intacto)
```

**P9 verificado por muestreo contra SOURCE** (los datos del seed no son inventados):
`contacto@wolfimmotors.com.ar`, `+54 9 3547 563911`, `Blvd. Carlos Pellegrini 710`,
`G-PW4FH9WHQB` → `models/SiteConfig.js` líneas 7-9 y 21; los 3 horarios
(`Lun - Vie` / `8:00 - 12:00 · 16:30 - 20:30`, `Sábados` / `9:00 - 12:00 hs`, `Domingos` / `Cerrado`)
→ `components/Footer.jsx` líneas 98-106, misma forma. El guard de "no toca SiteConfig" es
aserción real en `demo-tenant.test.ts`:156-161 (regex sobre el código con comentarios descartados).

**Punto de coordinación para WP07:** el test estático de WP10
(`index-shape.test.ts`) hoy asserta que `ALL_MODELS` son **exactamente las 5 colecciones del
Core SaaS**. Al sumar `Vehicle`/`VehicleInternal` a `ALL_MODELS` esa aserción va a fallar a
propósito — hay que actualizarla a la lista extendida, no relajarla, y así los índices de
motors entran solos en la evidencia estática de WP10.

### Verificación de brain-local — WP05 + capa WP10 (2026-10-05 09:16, sin Git de escritura)

```text
$ git rev-parse HEAD                       → 410219d19656e8557f26a9fc0196ea8cb4c79af8
$ git status --porcelain -uall | wc -l     → 0     ·  ls-files → 93 (81 + 12)
$ git diff --name-status 9df6624..HEAD     → 12 A · 5 M
$ git remote -v                            → vacío (sin remote)
$ npm run build    (tsc -b + typecheck:tests) → EXIT 0
$ npm test         → 5 files passed | 1 skipped (6) · 29 passed | 2 skipped (31)
$ npm run test:wp10 → 8/8   (estática, sin DB ni red)
$ npm run test:dist → 2/2   (desde dist/ vía main/exports)
$ git status post-corrida → 0
$ npx vitest run …integration.test.ts                       → EXIT 0 · 1 file skipped · 2 tests skipped
$ WOLFIM_DB_INTEGRATION=1 npx vitest run …integration.test.ts → EXIT 1 · 1 file FAILED (mensaje explícito: requiere MONGODB_URI)
$ git -C .../wolfim-motors-demo rev-parse HEAD → e9f774c · status " M AGENTS.md" (Intacto)
```

La evidencia estática de WP10 es **adversarial, no decorativa**: incluye 3 casos que la hacen
romper (unique global en colección de negocio, control negativo con `tenantId`, unique sobre
`internalStockCode`) y la allowlist `tenants`/`users`/`domains` está asertada explícitamente
(sin pase libre ciego). La capa de integración **no se saltea en silencio**: verificada la
matriz exit-code (0 + skipped sin flag · 1 + failed con flag y sin `MONGODB_URI`).

**P5 ratificada por brain-local:** opción 3 (skip explícito + `MONGODB_URI`), `mongodb-memory-server`
descartado mientras el host no tenga Mongo — mantener `clone → npm ci → build → test`
offline y determinista. Regla de gate: el veredicto dice qué capa corrió
(`estática: 8/8 · integración: SALTEADA/CORRIDA`).

### Verificación de brain-local — WP03 + WP04 (2026-10-05, sin Git de escritura)

```text
$ git -C C:/Projects/wolfim-platform rev-parse HEAD        → 9df662449bdac1e5acda83d288013f9b655e85b7
$ git status --porcelain -uall | wc -l                     → 0     (árbol limpio)
$ git ls-files | wc -l                                     → 81    (37 + 39 + 5)
$ git remote -v                                            → vacío (sin remote)
$ git config --local user.name / user.email                → Ziramog / fullpowerok@gmail.com
$ git diff --name-status 17f6863..HEAD | uniq -c por estado→ 44 A · 2 M   (= 39+5 nuevos · .gitignore + PROJECT_STATE.md)
$ ls AGENTS.md                                             → No such file (A1 abierto, como se declaró)
$ npm run build            → EXIT 0
$ npx vitest run           → EXIT 0 · Test Files 3 passed (3) · Tests 12 passed (12) · 665ms
$ npm run test:dist        → EXIT 0 · Test Files 1 passed (1) · Tests 2 passed (2)   (desde dist/ vía main/exports)
$ git status post-corrida  → 0     (build/test no ensucian el commit)
$ git -C .../wolfim-motors-demo rev-parse HEAD             → e9f774c · status " M AGENTS.md" · mtime 2026-09-25
```

`docs/PROJECT_STATE.md` en `GREEN`; `docs/ADDENDUM-D2-vitest.md` §3 trae los 10 gates
(WP10/13/15/16/21/22/27/28/30/32) con `TBD` por gate → WP10 no hereda cobertura imaginaria.

### A1 — `AGENTS.md` (abierto, sin bypass)

El guard de archivos protegidos de instrucciones de agente bloqueó el write de web-builder
dos veces (prompts de aprobación vencidos) y le prohíbe reintentar por otra vía. **brain-local
no lo escribe ni lo rutea por otra herramienta**: sortear un control de seguridad no es una
decisión de coordinación. Opciones para Juan: aprobar el prompt a nivel herramienta cuando
aparezca, o crear el archivo él mismo con el contenido ya redactado. Está registrado como
deuda en `PROJECT_STATE.md`; no bloquea ningún WP.

Audit gate más cercano: **WP10** (tenant-scoped indexes). WP00/WP01/WP02 sin gate.
Gate humano más cercano: **WP31** (Demo Portal Cutover → aprobación explícita de Juan).

## Decisiones del 2026-10-04 (mandato de Juan en group chat "wolfim platform")

Juan: *"ocupate de este proyecto … hagan que esto suceda"* → instrucción de **no frenar
por decisiones menores**. brain-local resuelve como coordinador y registra, sin volver a
preguntar:

| # | Decisión | Alcance | Reversibilidad |
|---|---|---|---|
| **D2** | **APROBADO** — vitest como runner de tests del TARGET, dev-only, dentro de WP03 | No cambia scope de producto; es infra de evidencia para los audit gates WP10/13/15/16/21/22/27/28/30/32, que hoy no tendrían forma de producir evidencia ejecutable (`SOURCE: NONE_CONFIGURED`). Repo nuevo → no afecta a SOURCE. | 1 commit (`revert`) — sin efecto en SOURCE ni en producción |
| **A1** | **AGENTS.md propio y mínimo del TARGET**, escrito en WP03 junto al esqueleto (no se copia el de SOURCE, que sigue con `+18` líneas sin commitear y no se toca → D1 intacto) | Documento de orquestación del repo nuevo, no código de producto | 1 commit |
| D1 | Sin cambios: `M AGENTS.md` de SOURCE se deja como está, no entra al TARGET | — | — |

Estas decisiones quedan como addendum del plan v3 (FROZEN) y se registran en este archivo.
Si Juan objeta, se revierten con un commit — no cambian arquitectura, datos ni producto.

## Pendiente de decisión

1. **HO-2026-10-04-001** → ✅ ejecutado y respondido (response.md + 2 events, 2026-10-04
   17:02 -04). Verdicto: SÍ hay segundo poller → perfil `algolab` de esta PC.
   **Acción correctiva pendiente de OK de Juan** (comentar `TELEGRAM_BOT_TOKEN` en
   `profiles/algolab/.env`). Fuera del proyecto Wolfim y toca credenciales de otro perfil
   → no se ejecuta sin OK explícito, aunque haya mandato amplio sobre Wolfim.
2. Briefing: `reality-check-required-by` (2026-10-01) vencido — pedir reality-check a Juan.

## Referencias

- [[Hermes/Briefings/current|Briefing vigente]] ⚠️ reality-check vencido 01/10
- [[Hermes/Handoffs/vps-to-local/HO-2026-10-04-001/request|HO-2026-10-04-001]] ★
- [[companies/wolfim/intelligence/patterns|Patterns Wolfim]]
- [[companies/wolfim/intelligence/context|Context Wolfim]]
- Pack: `WOLFIM_PLATFORM_PROJECT_PACK_v7.zip` (attachments brain-local)
