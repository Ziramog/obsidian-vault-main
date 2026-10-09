---
session: 2026-10-07
profile: brain-local
type: orchestration
project: wolfim-platform
wp: WP15 — Modules + Permissions (AUDIT GATE)
status: LANZADO — fila de gate congelada, handoff a web-builder emitido en group chat "wolfim platform"
note: |
  Esta sesión NO es la copia normativa de la fila. La copia normativa es
  docs/ADDENDUM-D2-vitest.md §3 (fila WP15) una vez que web-builder commitee el docs commit.
  Si hay divergencia entre este archivo y el TARGET, el TARGET gana.
---

# Sesión — 2026-10-07 — Wolfim Platform · lanzamiento de WP15

## Protocolo de apertura (SOUL)

| Paso | Resultado |
|---|---|
| Briefing `current.md` + TTL | `last-reviewed 2026-09-24T17:40-03` + `valid-for-hours 336` → **vence 2026-10-08T17:40-03 (mañana)**. `reality-check-required-by: 2026-10-01` vencido. VIGENTE por TTL, escalado a Juan. |
| Handoffs `vps-to-local` ready | HO-2026-10-04-001 (respondida, `done-with-escalation`). Cola con 7 handoffs jul/ago ya trabajados que siguen en `ready` → propuesto archivar. |
| context.md / patterns.md | `companies/wolfim/intelligence/` leídos (patterns v2 + insight 2026-09-27 de dominios). |
| Repos | SOURCE `e9f774c` + ` M AGENTS.md` (D1 intacto). TARGET HEAD `23ccc5e`, `status -uall` = 0, 158 archivos, sin remote. |

## Estado del gate

Tres mediciones independientes convergen (mías por `git log -S` / read-only, más las de web-auditor 05:24 y 05:38):

```text
test:wp10  script  → introducido en 10737d0 (WP05) apuntando a packages/db/src/models/index-shape.test.ts,
                     archivo creado EN ESE MISMO COMMIT  ⇒ script + evidencia atómicos
re-point            → f40f772 (WP07) a tests/wp10-tenant-index-shape.test.ts, creado también en ese commit
                     ⇒ el precedente NO es "script 3 WPs antes del archivo" (versión de web-builder, refutada)
anchors docs        → roles-permissions.md §15 (l.532 orden + `testDrives disabled`), §24 (l.727, `resource tenantId`),
                     §25 (l.751 DENY, sin `allow unless prohibited`)
consumidores        → apps/platform-app/src: 0 matches de hasModule|modulesFromFeatures|authorize(|PermissionGate|ModuleGate
packages/permissions/src/index.ts → skeleton WP03, 2 exports (WORKSPACE_NAME, WORKSPACE_KIND)
ModuleKey           → YA exportado por @wolfim/tenant (src/index.ts l.9-10) ⇒ no hace falta tocar modules.ts
```

## Fila de gate — CONGELADA (versión de web-auditor, aceptada íntegra)

> **WP15 · Modules + Permissions** — `ModuleRegistry`/`authorize()`/`PermissionGate`/`ModuleGate`.
> Orden de resolución (§15 l.532): tenant activo → membership activa → módulo habilitado → permiso otorgado
> → recurso tenant-scoped. **Fail-closed** (§25 l.751): permiso no declarado ⇒ DENY, sin `allow unless
> prohibited`. El registry **deriva** de `MODULES_FROM_FEATURES`/`modulesFromFeatures()` (WP11);
> **aserción de igualdad**: el conjunto consumido por los gates debe ser **igual** a
> `Object.values(MODULES_FROM_FEATURES)` — un mapa paralelo (de más, de menos o con claves renombradas)
> rompe el test. Los consumidores usan el tipo `ModuleKey` que expone el registry (`hasModule()` acepta
> `string`: un typo en un gate deniega en silencio). La habilitación se computa del **ctx resuelto**
> (`resolveTenantFromSlug`), nunca de caché global. Sin atajo demo (P25/P30).
> **Deben fallar:** (1) permiso no declarado; (2) módulo apagado en el tenant **aunque el rol tenga el
> permiso** (§15); (3) recurso con `tenantId` distinto — corre con módulo on + permiso otorgado y **asserta
> en qué paso se rechazó** (distinguible en el código interno; si toca el borde HTTP, sigue colapsando en un
> solo 404, H5); (4) sesión `DEMO` sin permiso; (5) nombre de módulo fuera de `MODULES_FROM_FEATURES`.
> **Debe pasar:** mismo tenant, módulo on, permiso declarado, recurso propio.
> `packages/tenant/src/modules.ts` no se modifica. **Capa:** unit in-memory, sin DB ni red; **integración N/A**.
> **Comando:** `npm run test:wp15` (= `vitest run tests/wp15-permissions.test.ts`); script + archivo entran
> **atómicamente** en el primer commit de código de WP15 (precedente `10737d0`), y sólo cuenta el PASS con
> salida cruda a partir de ese commit.

Aportes instrumentales de web-auditor aceptados: (1) la igualdad falsable reemplaza la prohibición de
"mapa paralelo"; (2) el tipo derivado `ModuleKey` + must-break (5); (3) declaración de capa (P5); (4) la
cláusula de atomicidad dentro de la fila, no sólo en el chat.

## Secuencia acordada (handoff emitido)

```text
1. web-builder  → docs commit SOLO con la fila en docs/ADDENDUM-D2-vitest.md §3
                  (+ decisión P32 en PROJECT_STATE §5: primer consumidor de los gates = WP16 CRM Core)
2. web-builder  → commit de CÓDIGO atómico: test:wp15 en root package.json + tests/wp15-permissions.test.ts
                  + ModuleRegistry/authorize()/PermissionGate/ModuleGate (Antigravity para el andamiaje, revisión
                  obligatoria antes del commit: qué produjo la herramienta y qué se editó a mano)
3. web-auditor  → gate WP15: PASS/FAIL contra la salida cruda de `npm run test:wp15`
```

Reglas vigentes: SOURCE read-only y verificado después (` M AGENTS.md` intacto). Sin remote, sin push
(human gate). Sin junction dentro de `node_modules` (incidente WP14). `.next` del TARGET está stale
(22:40:56 vs fix `c1e732d` 22:44:18) → borrar antes de servir o deployar, no es tarea de WP15.

## Registro de decisión

`P32` (decisión, **no** WP — no confundir con la fila `WP32 — Second Tenant Validation`, que vive en el
mismo doc): primer consumidor de `PermissionGate`/`ModuleGate` = **WP16 CRM Core**; hasta entonces
"0 consumidores" es criterio registrado, no footnote. Al anotarla, incluir la fila/línea que referencia.

## Pendientes ajenos al WP15

- Corrección del segundo poller: comentar `TELEGRAM_BOT_TOKEN` en `profiles/algolab/.env` → espera OK de Juan (fuera de zona).
- Briefing: reality-check vencido + TTL cae 2026-10-08T17:40 → pedir briefing nuevo antes de trabajo comercial.
- Deuda #20 (`next build` bloqueado en Node 26): gate de pre-deploy + spike Node 20/22 cerca de WP29/WP31.

## Autorización de Juan — 2026-10-07 (group chat "wolfim platform")

Juan: *"@brain-local proceder hasta finalizar. he testeado, la verdad es solo una maqueta lo que
tenemos ahora"*.

1. **Modo Antigravity — interpretado como OK a (A)** `--dangerously-skip-permissions` (la opción que
   web-builder y brain-local recomendaron). No eligió (A) ni (B) con esas letras, así que se declara la
   interpretación y queda corregible: si no era eso, el freno es inmediato y la corrida se aborta.
   Guardrails que siguen vigentes con (A): alcance TARGET-only (sin remote, sin push, sin red, sin `.env`,
   prompt prohíbe git y prohíbe tocar SOURCE), revisión humana del diff antes del commit, verificación
   post-corrida de SOURCE intacto + rango de auto-sync del vault.
2. **Calibración de producto**: "es solo una maqueta" es correcto y es por diseño — WP00–WP14 entregan
   fundación (db/tenant/auth/motores/repositorios), runners y el andamiaje de `platform-app` (AppShell +
   rutas + tokens, sin consumidores de gates ni wiring real). El estado deja de ser maqueta en el camino
   WP16→WP31 (CRM real, cotizaciones, reservas/ventas, portal público con paridad, cutover). Gaps honestos
   en ese camino: (a) sin remote/`push` todavía (human gate); (b) `next build` bloqueado en este host →
   spike Node 20/22 es precondición del pre-deploy y pasa a camino crítico; (c) el gap de P33
   (`managerCanViewFinancials` sin WP) es cambio de alcance si el producto "real" incluye financieros.
3. **Modo de trabajo acordado**: brain-local corre el tren de WPs hacia adelante sin volver a preguntar por
   decisiones menores, y **frena sólo en** (i) audit gate FAIL, (ii) human gates del plan (WP31 deploy y
   cutover, y cualquier push), (iii) cambio de alcance o contradicción con el briefing. Reporte macro cada
   pocos WPs, con el detalle por WP en el registro de sesión.

## Referencias

- `Hermes/Sessions/2026-10-04-wolfim-platform-wp00-kickoff.md` (WP00–WP14)
- `C:\Projects\wolfim-platform\docs\ADDENDUM-D2-vitest.md` §3 · `docs/PROJECT_STATE.md` §5
- `C:\Projects\wolfim-platform\docs\roles-permissions.md` §15/§24/§25 · `docs/brain-local-wolfim-adapter.md`
- `companies/wolfim/intelligence/patterns.md`
