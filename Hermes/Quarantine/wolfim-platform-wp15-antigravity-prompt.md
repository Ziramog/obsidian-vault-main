---
repo: C:\Projects\wolfim-platform  (TARGET — npm workspaces + vitest)
commit-base: a550994
origen: ADDENDUM-D2 §3 fila WP15 (congelada por web-auditor 2026-10-07) + PROJECT_STATE §5 P32/P33
estado: lanzado
zona: Hermes/Quarantine — no normativo; la copia que manda es la del commit de docs (a550994)
---

# WP15 — Modules + Permissions

## Objetivo

Implementar en `packages/permissions` la capa de **módulos y permisos** del TARGET
(`ModuleRegistry`, `authorize()`, `PermissionGate`, `ModuleGate`) con **fail-closed**, y entregar la
evidencia ejecutable (`tests/wp15-permissions.test.ts` + script `npm run test:wp15`). Sin consumidores
de UI: el primer consumidor es **WP16 CRM Core** (P32) y eso se verifica, no se asume.

## Contexto del proyecto

Repo TARGET: `C:\Projects\wolfim-platform`. Base `a550994`, árbol limpio. Runner: **vitest**, dev-only
(`docs/ADDENDUM-D2-vitest.md`, aprobado por Juan). `npm run build` = `tsc -b` + `typecheck:tests` +
`typecheck:app`. No hay pnpm; no hay script `test` por workspace: todo sale del root `package.json`.

**Lectura obligatoria antes de escribir una línea** (si algo de este prompt contradice estos docs, PARÁ
y reportá la contradicción en vez de elegir por tu cuenta):

- `AGENTS.md` (raíz del TARGET)
- `docs/PROJECT_STATE.md` — §2 (estructura), §3-nonies (WP13 auth), §3-undecies (WP14, guardrail 5), §4 (política de git), §5 (decisiones P24–P32)
- `docs/roles-permissions.md` — **§15 (l.532) orden de resolución**, **§24 (l.727) firma de `authorize`**, **§25 (l.751) deny by default**, §26 (roles fijos V1), §27 (policies V1), §28 (nombres de permisos), §29 (contrato por endpoint), §30 (Definition of Done)
- `docs/multi-vertical-architecture.md` §12–§13 (la UI y las decisiones salen de **módulos**, no de `vertical`)
- `docs/data-model.md` §3.1 (el mapa de capabilities del TARGET es exactamente `Tenant.features`)
- `packages/tenant/src/modules.ts`, `packages/tenant/src/resolver.ts`, `packages/auth/src/membership.ts`, `packages/auth/src/session.ts`

**Lo que ya existe y NO se toca ni se re-declara:**

- `packages/tenant/src/modules.ts` (WP11): `MODULES_FROM_FEATURES`, `modulesFromFeatures(features)`, `hasModule(modules, module)`. El tipo `ModuleKey` **ya se exporta** desde `packages/tenant/src/index.ts` (l.9-10). El `ModuleRegistry` **importa** ese tipo; prohibido re-declararlo o mantener un mapa paralelo de módulos.
- `packages/tenant/src/resolver.ts` (WP11): `buildTenantContext()` ya computa `modules: modulesFromFeatures(tenant.features)`. El `TenantContext` tiene `tenantId`, `tenantSlug`, `mode`, `status`, `modules`, `userId`, `role` y **no** tiene `vertical` (P22).
- `packages/auth/src/membership.ts` (WP13): `SessionContext = { userId: string | null; email; tenantId; role: MembershipRole; demoBypass: boolean }`; `buildSessionContext()` / `buildDemoSession()` son los únicos constructores (H6). El bypass demo se habilita **por servidor** (`WOLFIM_ALLOW_DEMO_BYPASS=1`, P25/P30) y devuelve `userId: null` + `demoBypass: true` con rol acotado.
- `packages/permissions/src/index.ts` es el **skeleton de WP03** (2 exportaciones de placeholder). Ahí va la lógica: es el único paquete que se implementa en este WP.

## Tarea (por bloques)

### Bloque A — `ModuleRegistry` (`packages/permissions/src/module-registry.ts`)

1. Importar `MODULES_FROM_FEATURES` y `type ModuleKey` desde `@wolfim/tenant` (entrada pública del paquete). El registry **deriva**; no enumera módulos a mano y **no** crea un segundo mapa.
2. Exponer
   ```ts
   export const MODULE_REGISTRY_KEYS: readonly ModuleKey[]   // = Object.values(MODULES_FROM_FEATURES)
   export function isModuleEnabled(modules: readonly string[], module: string): boolean
   export function assertModuleKey(module: string): module is ModuleKey
   ```
   `isModuleEnabled` se computa **desde los módulos del ctx resuelto** (lo que el resolver puso en `TenantContext.modules`), nunca desde env, config global, caché de proceso ni del `mode` del tenant.
3. No inventar módulos finos (`vehicles`, `reservations`, `sales`): llegan con WP22/WP27/WP28 (así lo dice `modules.ts`).
4. Si importar `@wolfim/tenant` arrastra `@wolfim/db`/mongoose y algo se rompe al correr los tests, **reportalo**; la salida jamás es re-declarar el mapa a mano.

### Bloque B — `authorize()` (`packages/permissions/src/authorize.ts`)

Firma según §24 (`authorize(ctx, { permission, resource })`), con el módulo del endpoint según §29
(cada endpoint declara required module + required permission). Tipado **estructural**: `authorize` no
importa `@wolfim/auth` en runtime (así el test arma ctx planos, sin DB).

```ts
export type AuthorizeContext = {
  tenant: { tenantId: string; status: string; mode: string }
  /** módulos del ctx resuelto (TenantContext.modules) — no un parámetro libre del caller */
  modules: readonly string[]
  /** sesión (real o bypass demo); `null` = sin sesión */
  session: { userId: string | null; tenantId: string; role: string; demoBypass: boolean } | null
}

export type AuthorizeStep = 'TENANT' | 'MEMBERSHIP' | 'MODULE' | 'PERMISSION' | 'RESOURCE'

export type AuthorizeDecision =
  | { allowed: true; step: 'OK' }
  | { allowed: false; step: AuthorizeStep; code: AuthorizeDenyCode }

export function authorize(
  ctx: AuthorizeContext,
  request: { module?: ModuleKey; permission: string; resource?: { tenantId?: string } },
): AuthorizeDecision
```

**Orden de resolución obligatorio (§15, l.532)** — se evalúa en este orden y el rechazo declara el paso:

1. `TENANT`: tenant servible (`USABLE_TENANT_STATUSES` de `@wolfim/tenant`, reusar; no copiar la lista).
2. `MEMBERSHIP`: hay sesión y `session.tenantId === ctx.tenant.tenantId`. Sin sesión ⇒ deny.
3. `MODULE`: si el endpoint declaró `module` y no está habilitado ⇒ deny (`MODULE_DISABLED`). Si el nombre **no pertenece** a `MODULE_REGISTRY_KEYS` ⇒ deny (`MODULE_UNKNOWN`) — sin depender de `hasModule()` (acepta cualquier `string`).
4. `PERMISSION`: permiso **declarado** en el catálogo y otorgado al rol ⇒ allow; declarado y no otorgado ⇒ `PERMISSION_DENIED`; **no declarado ⇒ `PERMISSION_UNKNOWN` + deny** (fail-closed, §25 l.751: no existe el camino "allow unless prohibited").
5. `RESOURCE`: si viene `resource.tenantId` y **no** coincide con `ctx.tenant.tenantId` ⇒ `RESOURCE_CROSS_TENANT` (§24 lista `resource tenantId` en la resolución). Este paso se evalúa **después** de módulo y permiso: el caso de prueba corre con módulo on + permiso otorgado para que falle acá y no antes.

**Sin atajo demo:** `demoBypass: true` no cambia ninguna decisión; el rol acotado de la sesión demo
(`VIEWER`) se evalúa contra el mismo catálogo. Prohibido cualquier `if (demoBypass) allow`.

**Catálogo de permisos (V1)** — `packages/permissions/src/permission-catalog.ts`, derivado de docs, sin
inventar nombres:

- Roles fijos §26: `OWNER`, `MANAGER`, `SELLER`, `VIEWER`.
- Nombres §28: `lead.read|create|update|assign` · `opportunity.read|create|update|assign|close` · `vehicle.read|create|update|publish|financial.read|document.*` · `quotation.read|create|update|send` · `tenant.settings.*` · `membership.*` · `audit.read` (§23) · `platform.audit.read` (§23, rol de plataforma) · `reservation.create` (§29).
- `§30` DoD: permisos **financieros** y de **documentos** aislados (no en `SELLER`), roles de plataforma separados de los roles de tenant, OWNER protegido.
- Los comodines (`vehicle.document.*`, `tenant.settings.*`, `membership.*`) se **expanden a nombres concretos al construir el catálogo**; ninguna entrada del catálogo resuelto puede quedar con `*`.
- **Fuera de alcance, con destino registrado (P33, §27):** las 5 policies configurables por tenant **no** se implementan en WP15 — el campo `policies` no existe en `TenantConfig` y **no hay valor legacy que migrar** (medido: 0 matches de los 5 nombres en todo SOURCE). Destinos ya fijados: `sellerCanPickUnassignedLeads` y `sellerVisibility` → **WP17 Leads Slice** (extiende a WP18/WP19); `sellerCanCreateReservation` → **WP27**; `sellerCanCreateSale` → **WP28**; `managerCanViewFinancials` → **sin WP asignado** (gap del plan; lo toma el primer WP que enforce `vehicle.financial.read`/`sale.financial.read` — candidatos WP22/WP25/WP28). WP15 **no** las implementa, pero tampoco deja un camino que las insinúe: el catálogo de roles fijos no introduce ninguna ruta "clave ausente ⇒ allow". La regla de ausencia ya está decidida para cuando lleguen: `sellerVisibility` ausente ⇒ `OPEN_TEAM` (§10, default recomendado para Motors); los cuatro booleanos ausentes ⇒ **false** (§9: habilitación explícita; §11: nunca inferir acceso). Ausente nunca significa allow.

### Bloque C — `PermissionGate` / `ModuleGate` (`packages/permissions/src/gates.ts`)

Envoltorios **puros**, sin framework (nada de React/JSX, ninguna dependencia nueva):

```ts
export function moduleGate(ctx: AuthorizeContext, module: ModuleKey): GateResult   // { allowed, decision }
export function permissionGate(ctx: AuthorizeContext, permission: string, resource?: { tenantId?: string }): GateResult
```

Ambos son atajos a `authorize()` con el mismo orden y el mismo fail-closed: un permiso o módulo
desconocido **deniega**. No crean estado, no cachean, no leen env. `apps/platform-app` no los consume
todavía (P32): no agregues el consumidor.

### Bloque D — Evidencia (`tests/wp15-permissions.test.ts` + script)

- Archivo en `tests/wp15-permissions.test.ts` (el `include` de `vitest.config.ts` ya levanta `tests/**/*.test.ts`; **no** tocar la config).
- Script nuevo en el root `package.json`: `"test:wp15": "vitest run tests/wp15-permissions.test.ts"` (precedente `test:wp10`).
- **Dos tenants con `features` distintas** (fixtures planos vía `buildTenantContext` de `@wolfim/tenant`, que es pura, o directamente ctx planos): **A** con `crm: true` / `testDrives: false`; **B** con `crm: false` / `testDrives: true`. Sin Mongo, sin red, sin `MONGODB_URI`.
- **Casos que DEBEN ROMPER** (cada uno asserta `allowed === false` **y el `step`**):
  1. permiso no declarado ⇒ `step: 'PERMISSION'`, `PERMISSION_UNKNOWN`.
  2. módulo apagado en el tenant **aunque el rol tenga el permiso** ⇒ `step: 'MODULE'`, `MODULE_DISABLED`.
  3. recurso con `tenantId` distinto, corriendo con **módulo on + permiso otorgado** ⇒ `step: 'RESOURCE'`, `RESOURCE_CROSS_TENANT`.
  4. sesión `DEMO` sin permiso ⇒ deny (y su gemelo: la misma sesión demo **con** permiso otorgado ⇒ allow, para probar que no hay ni atajo ni bloqueo por ser demo).
  5. nombre de módulo fuera de `MODULES_FROM_FEATURES` ⇒ deny.
- **Caso que DEBE PASAR**: mismo tenant, módulo on, permiso declarado y otorgado, recurso propio ⇒ `allowed: true`.
- **Aislamiento entre tenants**: el permiso otorgado en A **no** habilita nada en B con la misma sesión/rol (módulo apagado en B).
- **Igualdad del registry**: aserción de que `MODULE_REGISTRY_KEYS` es **igual** a `Object.values(MODULES_FROM_FEATURES)` (multiset, misma longitud): un mapa paralelo con una clave de más, de menos o renombrada rompe el test.
- **Wildcards**: aserción de que ninguna entrada del catálogo resuelto contiene `*`.

## Archivos a tocar

```text
packages/permissions/src/index.ts               (barrel: exportar la API nueva)
packages/permissions/src/module-registry.ts     (nuevo)
packages/permissions/src/authorize.ts           (nuevo)
packages/permissions/src/permission-catalog.ts  (nuevo)
packages/permissions/src/gates.ts               (nuevo)
packages/permissions/package.json               (+ dependency "@wolfim/tenant": "*" si el import lo exige)
packages/permissions/tsconfig.json              (+ references: [{ "path": "../tenant" }] si el import lo exige, igual que packages/auth)
tests/wp15-permissions.test.ts                  (nuevo)
package.json                                    (root: script "test:wp15")
```

**Prohibido tocar:** `packages/tenant/**` (incluido `modules.ts`), `packages/auth/**`, `apps/**`,
`docs/**`, `vitest.config.ts`, `tsconfig*.json` que no sean los dos listados arriba, `AGENTS.md`,
`C:\Projects\wolfim-motors-demo` (SOURCE — ni leerlo ni escribirlo), ningún `.env`, ningún `dist/`
commiteado, nada de git.

## Entorno de ejecución

- Nodo medido: **esta PC** (Windows, Node 26, npm 11). Comandos desde la raíz del TARGET.
- Variables de entorno que el código puede tratar como credenciales: **ninguna**. WP15 es unit in-memory: no se conecta a MongoDB, no lee `MONGODB_URI`, no hace red. Si tu implementación necesita una env para pasar, eso es un defecto de diseño: reportalo.
- Puertos: **ninguno**.
- `next build` está **bloqueado** en este host (deuda #20) y **no** se toca acá: el gate de la app es `npm run build` (`typecheck:app` incluido) + vitest.
- No hay `.next` ni deploy en este WP. No ejecutes `next dev`/`next start`.
- No corras `npm install` salvo que agregar la dependency de workspace lo requiera; si lo corrés, decilo en el reporte.

## Modo de entrega

- **No ejecutes ningún comando git.** Dejá los cambios **sin commitear** en el árbol de trabajo.
- Un solo commit atómico lo hace web-builder después de revisar: `test:wp15` + `tests/wp15-permissions.test.ts` + el código, juntos (precedente `10737d0`: script y archivo destino nacen en el mismo commit).
- **No hay push. No hay remote.** El TARGET no tiene remote a propósito.
- Al terminar, `git status --porcelain -uall` debe mostrar **sólo** los archivos de la lista "Archivos a tocar" (y sólo los que efectivamente cambiaste).

## Restricciones

- **Guardrail 5 (lección de WP14):** el reporte final declara explícitamente **qué produjo la herramienta y qué editaste a mano**. En WP14 la regresión de política (bypass demo controlable desde el cliente) salió justo de no distinguirlo.
- Prohibido `any`, `as unknown as`, `@ts-ignore`, `eslint-disable` y silenciar errores de tipo para pasar el build.
- Prohibido duplicar: el mapa de módulos (existe en `@wolfim/tenant`), el catálogo de roles (docs §26), la lista de estados servibles (`USABLE_TENANT_STATUSES`), el mapa de features.
- Nada de lógica en `index.ts`: es barrel.
- Comentarios en español, mismo tono que el resto del repo (citan el doc y la decisión: `§15`, `§24`, `§25`, `P22`, `P25`).

## Criterios de aceptación

Pegá la **salida cruda** de cada uno en el reporte. Omitir uno invalida la entrega. No compares contra
números congelados: informá lo que produce **tu** corrida, en tu corrida.

1. `npm run build` ⇒ EXIT 0 (incluye `tsc -b`, `typecheck:tests`, `typecheck:app`).
2. `npm run test:wp15` ⇒ EXIT 0, con los 6 casos (5 must-break + 1 positivo) visibles por nombre, y cada must-break mostrando el `step` esperado (`MODULE`, `PERMISSION`, `RESOURCE`, …).
3. `npm test` ⇒ suite completa, pegar el resumen (passed/skipped) y confirmar **0 fallos nuevos**; si algún test preexistente cambia de estado, decilo con su nombre.
4. `node -e "console.log(require('./package.json').scripts['test:wp15'])"` ⇒ imprime exactamente `vitest run tests/wp15-permissions.test.ts`.
5. `git diff --stat -- packages/tenant` ⇒ **vacío** (no se tocó el registry de WP11).
6. `grep -rn "hasModule\|modulesFromFeatures\|authorize(\|ModuleRegistry\|PermissionGate\|ModuleGate" apps/platform-app/src` ⇒ **0** matches (la deferral a WP16/P32 sigue en pie). Pegá la salida del grep (vacía o con el conteo).
7. Sin `MONGODB_URI` en el entorno: `env | grep -c MONGODB_URI` ⇒ `0`, y la suite de WP15 igual pasa (declaración de capa: **unit in-memory · integración N/A**).
8. `git status --porcelain -uall` ⇒ sólo los archivos de "Archivos a tocar".
9. Reporte con la sección "**qué produjo la herramienta vs qué edité a mano**" y una sección "**deuda declarada**" (§27 policies fuera de alcance; cualquier otra cosa que hayas dejado pendiente).
