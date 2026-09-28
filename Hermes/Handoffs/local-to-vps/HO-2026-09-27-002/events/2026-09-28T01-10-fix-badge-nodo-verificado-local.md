# Fix del badge de nodo — implementado y verificado en local

- **Fecha:** 2026-09-28 ~01:10 UTC (2026-09-27 ~21:10 -04:00)
- **Actor:** brain-local (PC local)
- **Origen:** hallazgo de brain-vps en `response.md` §3 — "badge de nodo invertido",
  asignado explícitamente a brain-local.

## Causa

`src/app/api/profiles/route.ts` hardcodeaba el origen en las dos ramas:
`node: "local"` (perfiles leídos de disco) y `node: "vps"` (los del gateway
secundario). Corriendo en el VPS, esa etiqueta era falsa para ambos lados.

Ojo con el detalle que casi rompe esto: **`node` NO es solo display, es la clave de
ruteo** (`/api/chat`, `/api/sessions` y `/api/sessions/[id]/messages` hacen
`isVps = body.node === "vps"` para elegir entre `HERMES_API_URL` y
`HERMES_VPS_URL`). Invertir los valores de `node` habría mandado los chats de los
bots del VPS al gateway de la PC. Por eso el fix **no toca `node`**: agrega un
campo de display aparte.

## Cambio

| Archivo | Cambio |
|---|---|
| `src/app/api/profiles/route.ts` | `HERMES_NODE_NAME` (alias aceptado: `HERMES_NODE_IDENTITY`) elige el label propio; `NODE_LABEL` / `OTHER_NODE_LABEL` se emiten como `nodeLabel` en cada rama. `node` queda intacto. |
| `src/lib/types.ts` | `Profile.nodeLabel?: string` |
| `src/components/BotDirectory.tsx` | `{bot.nodeLabel ?? (bot.node === "vps" ? "☁️ VPS" : "🖥️ PC Local")}` |

## Verificación

- `npx tsc --noEmit` → limpio; `npm run build` → exit 0, 10 páginas + 10 rutas
  dinámicas.
- Runtime, dos servidores `next start` sobre el mismo build y los mismos 9 perfiles
  de disco:
  - default (`HERMES_NODE_NAME` sin setear) → 9/9 con `nodeLabel: "🖥️ PC Local"`
  - `HERMES_NODE_NAME=vps` → 9/9 con `nodeLabel: "☁️ VPS"`
  - `node` = `"local"` en los 9 en ambos casos → **el ruteo no se movió**.
- `git status` tras el build: solo los 3 archivos del fix — los generados
  (`public/sw.js`, `public/workbox-*.js`) quedaron ignorados por el commit #2, o
  sea que el untrack cumplió su objetivo.

## Estado

**Sin commitear.** Requiere autorización del director para commit+push. Al
desplegar, el VPS necesita `HERMES_NODE_NAME=vps` en `.env.local` y un
`pm2 restart hermes-pwa`.
