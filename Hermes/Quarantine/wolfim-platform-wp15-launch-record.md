---
proyecto: wolfim-platform
wp: WP15 — Modules + Permissions
estado: prompt congelado, corrida NO lanzada (espera OK de @user sobre el modo de permisos de Antigravity)
escrito_por: web-builder
zona: Hermes/Quarantine (no normativo)
---

# WP15 — registro de lanzamiento (insumo congelado)

Instrumento de atribución pedido por @web-auditor: sin hash del prompt, el código que salga no queda
atribuido a la versión exacta del insumo que lo produjo (es el control que en WP14 permitió rastrear
de dónde vino la regresión del bypass demo).

## Insumo

| | |
|---|---|
| Prompt | `Hermes/Quarantine/wolfim-platform-wp15-antigravity-prompt.md` |
| **sha256** | `7d4582a04ac12218f559c10a90b942f7ab47120b559618908c21926bc1150b9e` |
| bytes | 16901 |
| vault HEAD al congelar | `5a002a54` (2026-10-07 05:53:05 -04:00) — el vault **auto-pushea** cada 4 min (`\HermesVaultSyncLocal`), así que el sha del vault avanza; lo que ata el insumo es el **sha256 del archivo** |
| TARGET base | `681949f` (docs-only: fila WP15 + P32 + P33 con relabel) · `status --porcelain -uall` = 0 |
| Redacción | P33 con **relabel aceptado** (fail-closed sólo para los booleanos; `sellerVisibility` ausente = default de negocio) aplicada en el prompt por **frase textual, no por número de línea** (el parche mueve las líneas): el párrafo de `## Objetivo` que empieza "**Alcance del rótulo `fail-closed`:**" + el bullet de P33 que empieza "**Fuera de alcance, con destino registrado (P33, §27)**" y cierra "Ausente nunca significa allow *para un permiso*…"; y en `PROJECT_STATE §5`, la fila `P33` con el mismo relabel |

## Corrida

- Comando previsto: `agy --print "$(cat <prompt>)" --mode accept-edits --project wolfim-platform`
  desde `C:\Projects\wolfim-platform`.
- **Bloqueante:** en headless, `agy --print` no puede pedir el permiso de `command` → auto-denegado y
  salida sin producir nada (medido 05:47, `AGY_EXIT=0`, log de 303 bytes, árbol intacto). El desbloqueo
  es una decisión de @user sobre su máquina: **(A)** `--dangerously-skip-permissions` (modo que ya
  funcionó en WP14) o **(B)** allow-rule en `~/.gemini/antigravity-cli/settings.json` (esquema **no**
  verificado: ese archivo hoy sólo tiene `colorScheme` y `trustedWorkspaces`).
- Verificación post-corrida (declarada por @web-auditor, pre-registrada): `git diff 681949f..HEAD
  --name-status` = sólo `package.json` (root) + `tests/wp15-permissions.test.ts` +
  `packages/permissions/**`; `git diff 681949f..HEAD -- packages/tenant/src/modules.ts vitest.config.ts`
  = vacío; commit atómico **sin** `docs/`; `status -uall` = 0 después de build + `test:wp15` + suite;
  y re-corrida propia de los must-break (1)–(5). Vault: "ningún commit entre el sha del vault al
  arrancar y el final, fuera de los archivos esperados".

## Estado

`prompt congelado` → `corrida pendiente de OK` → `corrida lanzada` → `diff revisado` → `commit atómico`
→ `gate de web-auditor`.
