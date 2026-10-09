---
title: "WP15 — Modules + Permissions: veredicto del audit gate"
project: wolfim-platform
audit_gate: WP15
verdict: PASS con residuos declarados
auditor: web-auditor
date: 2026-10-08
tz: "-03:00 (AST)"
commits:
  codigo: cebe9c5
  cierre_docs: 4a77ccb
baseline_medido_desde: 681949f
target: C:/Projects/wolfim-platform
herramienta: npm workspaces + vitest
---

# WP15 — Modules + Permissions · veredicto del audit gate

**Veredicto: PASS con residuos declarados R1/R2.** La fila congelada en `ADDENDUM-D2` §3 se cumplió
entera. **Capa medida: `unit in-memory` (sin DB, sin red); capa de integración: N/A** (WP15 no tiene
superficie de runtime contra base).

Ventana de medición: **2026-10-08 22:20:20 → 22:27:32 -03:00 (AST)**. Commit verificado:
`cebe9c5` (código, 9 archivos, sin `docs/`); cierre documental `4a77ccb` (docs-only, 1 archivo).

## 1. Qué medí yo y qué tomo de otro informe

| Punto | Quién lo midió | Nota |
|---|---|---|
| build, `test:wp15`, suite completa, instrumento (i)(ii)(iv)(vi), SOURCE | **web-auditor** (esta corrida) | abajo, salida cruda |
| re-corrida de los must-break con ctx sintéticos propios | **web-auditor** (probe propio, `dist` compilado) | abajo, tabla completa |
| R1/R2 | **web-auditor** (hallazgo y reproducción); reproducidos además por brain-local con su propio probe | coincidentes |
| `18 passed` / `159 passed` en la primera corrida | web-builder y brain-local | **repetido por mí**: coincide con mi medición |

## 2. Evidencia cruda (comandos + salida)

```text
$ npm run build                      → BUILD_EXIT=0
  (tsc -b && typecheck:tests && typecheck:app)

$ npm run test:wp15                  → Test Files 1 passed (1) · Tests 18 passed (18) · 1.39s · EXIT 0

$ npx vitest run                     → Test Files 16 passed | 6 skipped (22)
                                       Tests 159 passed | 8 skipped (167) · 3.91s
  (141 + 18 = 159: la suite de WP14 más el archivo nuevo, sin regresión)

$ git status --porcelain -uall       → 1 línea: ` M package.json`
  (excepción nombrada: la línea `dev` del usuario, mtime 09:14:59 del 07/10; fuera de los 3 commits de WP15)

$ git diff 681949f..cebe9c5 --name-status     → exactamente el set esperado
  M package.json · M packages/permissions/{package.json,src/index.ts,tsconfig.json}
  A packages/permissions/src/{authorize,module-registry,permission-catalog,gates}.ts
  A tests/wp15-permissions.test.ts

$ git diff 681949f..cebe9c5 -- packages/tenant/src/modules.ts vitest.config.ts   → 0 líneas
$ git show cebe9c5:package.json | grep -c '"dev"'                               → 0
  (la edición del usuario NO entró en el commit; `test:wp15` sí)

$ git -C C:/Projects/wolfim-motors-demo rev-parse --short HEAD → e9f774c ; status → ` M AGENTS.md` (D1 intacto)
```

Corrida posterior al build: `status -uall` idéntico al previo → el commit es reproducible, sin artefactos
no ignorados.

## 3. Re-corrida independiente de los must-break (instrumento propio)

Probe `wp15-must-break-rerun.mjs` contra `packages/permissions/dist/index.js` (compilado), con contextos
sintéticos propios — no el archivo de evidencia del implementador:

```text
(1) permiso no declarado                          → PERMISSION / PERMISSION_UNKNOWN
(2) módulo apagado + permiso otorgado             → MODULE / MODULE_DISABLED
(3) recurso cross-tenant (módulo on + permiso OK) → RESOURCE / RESOURCE_CROSS_TENANT
(4) sesión DEMO sin permiso                       → PERMISSION / PERMISSION_DENIED
(4b) DEMO con permiso (gemelo)                    → OK
(5) módulo fuera del mapa                         → MODULE / MODULE_UNKNOWN
(6) must-pass                                     → OK
adv-c: módulo off + permiso inexistente           → MODULE / MODULE_DISABLED   (orden §15: módulo antes que permiso)
adv-d: modules vacío + módulo declarado           → MODULE / MODULE_DISABLED
adv-e: rol desconocido + permiso conocido         → PERMISSION / PERMISSION_DENIED
adv-f: sesión de A sobre ctx de B                 → MEMBERSHIP / MEMBERSHIP_CROSS_TENANT
adv-j: tenant SUSPENDED                           → TENANT / TENANT_NOT_ACTIVE
registry: MODULE_REGISTRY_KEYS == Object.values(MODULES_FROM_FEATURES) → true (deriva, no enumera)
assertModuleKey('invented_key') → false · roles con comodín → ninguno
```

## 4. Residuos declarados

**R1 — allow por omisión del permiso (causa: tipos).**
`authorize(ctx, { module: 'crm' })`, sin declarar `permission`, devuelve `{"allowed":true,"step":"OK"}`
para **cualquier rol**, incluido `VIEWER`. Causa medida: `AuthorizeRequest.permission?: string`
(`authorize.ts` l.38-42) + el `else if (request.module === undefined)` (l.91-94): la rama sólo-módulo
cae al `return` final. Es la forma "allow unless prohibited" de §25 por omisión de argumento, y **no está
cubierta por ninguno de los 5 must-break** — por eso sobrevivió. No explotable hoy (0 consumidores).
**Cierre: en el tipo, no en runtime** (un parche en runtime no rompe el compile y la omisión vuelve).

**R2 — ausencia de `tenantId` en el recurso se trata como propio (causa: runtime).**
`authorize(ctx, { module: 'crm', permission: 'lead.read', resource: {} })` → `{"allowed":true,"step":"OK"}`.
Causa medida: `request.resource?.tenantId !== undefined && …` (`authorize.ts` l.97). Misma familia que la
lección de H1/WP13: **ausencia ⇒ deny**, no ⇒ allow. No enumerado en la fila.

Ninguno de los dos es FAIL: la fila congelada enumeraba 5 must-break + must-pass, y los seis se cumplen.
Ambos quedan pegados a `P32` para que **WP16** los cierre en su primer commit.

## 5. Huecos de registro (no de código)

1. **La fila WP15 de `ADDENDUM-D2` §3 no lleva anotación de veredicto.** El precedente de WP13 sí
   (esa celda lista H1–H6). Hoy quien lee la tabla ve criterio + comando, pero no que WP15 pasó: el
   veredicto vive sólo en `PROJECT_STATE` §3-duodecies. Se cierra con una línea en la celda.
2. **Corrección de atribución:** las dos secciones duplicadas `## 3-sexies` (índices de WP10 y evidencia
   de WP09) están en **`docs/PROJECT_STATE.md` l.201 y l.217**, no en `ADDENDUM-D2` (ahí no existe ningún
   heading `## 3-*`). La ambigüedad es real; la ubicación reportada no.
3. `companies/wolfim/audit/` **no existe** en el vault (los directorios de wolfim son brand, Clientes,
   finances, google-ads, intelligence, Leads, pipeline, projects, research, services, tareas; sólo
   `companies/korantis/audit/` existe). Este veredicto va a `Hermes/Systems/local/`, donde viven los
   informes de auditoría previos de Hermes.

## 6. Lección

Un gate puede quedar verde y dejar abierta **la familia de lo no enumerado**: "prohibido X" no es
falsable; exigir el tipo (que la omisión no compile) y tratar la ausencia de campo como deny sí lo son.
Corolario de método: la re-corrida de los must-break con contextos propios del auditor es lo que
convierte el PASS en medición, y es también lo que encontró R1/R2.
