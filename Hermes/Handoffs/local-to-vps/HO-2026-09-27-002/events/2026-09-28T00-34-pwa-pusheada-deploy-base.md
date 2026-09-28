# Evento: PWA pusheada — base de deploy fijada

- **Timestamp:** 2026-09-28T00:34Z (2026-09-27 20:34 EDT, PC local)
- **Autor:** brain-local
- **Origen:** instrucción explícita de Juan en la sala ("Proceder")
- **Repo:** `https://github.com/Ziramog/PWA-Hermes` (privado)
- **Rama:** `main`

## SHA de base del deploy (usar ESTE)

```
64e4bc12592d5d4df94cd3a3224fdf742b01bee7
```

Verificado contra el remoto, no contra el log local:

| Comprobación | Comando | Resultado |
|---|---|---|
| HEAD local | `git rev-parse HEAD` | `64e4bc12592d5d4df94cd3a3224fdf742b01bee7` |
| origin/main | `git rev-parse origin/main` (post-fetch) | `64e4bc12592d5d4df94cd3a3224fdf742b01bee7` |
| ref del remoto | `git ls-remote origin refs/heads/main` | `64e4bc12592d5d4df94cd3a3224fdf742b01bee7` |
| divergencia | `git rev-list --left-right --count origin/main...HEAD` | `0 0` |
| árbol de trabajo | `git status --porcelain` | vacío |

## Los dos commits

1. `9219d893a1435ff217a3ae505bcbcb72c4b6425f` — `feat: multi-node bot directory, model selector, iOS-style mobile UI`
   16 archivos modificados + 10 nuevos (`BotDirectory.tsx`, `BottomNav.tsx`, `BottomSheet.tsx`, `NewChatSheet.tsx`, `src/lib/icon-map.tsx`, `public/icons/` ×5, `scripts/generate-icons.ps1`, `iniciar-pwa.bat`, `BRAIN_LOCAL_HANDOVER.md`). Diff: 729 inserciones / 495 borrados sobre 17 archivos en el working tree (los mismos números que midió el VPS).
2. `64e4bc12592d5d4df94cd3a3224fdf742b01bee7` — `chore: untrack generated service worker artifacts`
   `.gitignore` += `/public/sw.js` y `/public/workbox-*.js` (glob, no nombre exacto: el próximo bump de workbox emite otro hash), más `git rm --cached` de los dos. Los archivos **siguen en disco** (9411 B y 23578 B) y siguen siendo regenerados por `next build`.

## Implicancia para el preflight del VPS

- El build del VPS (`npm ci && npm run build`) **regenera** `public/sw.js` y `public/workbox-*.js`; ya no aparecen en `git status` porque quedaron ignorados. El árbol queda limpio después del build — eso elimina el riesgo que detectamos de commitear salida generada.
- Clonar en `64e4bc1` y buildear produce, para el mismo toolchain, los mismos artefactos que corrían en la PC (mtimes 19:59 EDT).
- La base auditada es `64e4bc1`. Si alguien vuelve a escribir en el working tree antes de clonar/desplegar, el sha a desplegar **sigue siendo `64e4bc1`**, no `HEAD`.

## Hallazgo abierto (no bloqueante) — para decisión de Juan

`README.md:31` (ya versionado desde `0265d11`, sin cambios en este push) documenta:

```
API_SERVER_KEY=[credencial: API_SERVER_KEY]
```

Es el key del gateway local de Hermes. Está en el historial — y la premisa de que era un repo privado era FALSA: `obsidian-vault-main` es PUBLICO (el privado es `PWA-Hermes`). Redactado el 2026-09-28; ver el evento de incidente en la misma carpeta (commits `0265d11` y `7553e20`), así que un `git rm` normal **no lo borra**: sacarlo del historial requiere reescribir `main` (force-push) o rotar el key. No se tocó nada por decisión propia. Recomendación: rotar el key en `~/.hermes/.env` y dejar el README con un placeholder `[credencial: API_SERVER_KEY]`. Queda a criterio de Juan.
