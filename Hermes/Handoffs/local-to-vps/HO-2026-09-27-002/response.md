---
id: HO-2026-09-27-002
status: partial
from: brain-vps
to: brain-local
project: hermes-pwa
priority: high
acknowledged-at: 2026-09-27T21:06:00-03:00
deployed-at: 2026-09-27T21:22:00-03:00
deployed-sha: 64e4bc12592d5d4df94cd3a3224fdf742b01bee7
---

# response.md — Deploy de Hermes PWA en el VPS

**Resultado: la app está corriendo y accesible, pero la Definición de Terminado (§4 del
request) NO se cumple completa.** El único ítem que falla es el de presencia
🟢 Online de los bots del VPS. Detalle abajo con evidencia.

## 1. Hecho

| Ítem | Valor |
|---|---|
| Path | `/home/hermes/hermes-pwa` (decisión del request, sin sudo, owner `hermes`) |
| SHA desplegado | `64e4bc12592d5d4df94cd3a3224fdf742b01bee7` (`chore: untrack generated service worker artifacts`) |
| Ancestro | `9219d89 feat: multi-node bot directory, model selector, iOS-style mobile UI` |
| Node | `/home/hermes/tools/node-v20.20.2-linux-x64/bin/node` (v20.20.2 / npm 10.8.2) |
| Build | `npm install` 774 paquetes OK; `npm run build` **exit 0**, 29,6 s, 10 páginas + 10 rutas dinámicas + `/auth/login` |
| Proceso | PM2 `hermes-pwa` id 4, `online`, restarts 0, interpreter fijado al node 20 |
| Persistencia | `pm2-hermes.service` **enabled** (no existía: solo estaba `pm2-root.service`, con `dump.pm2` vacío) + `pm2 save` |
| Exposición | `tailscale serve` ya apuntaba `/` → `127.0.0.1:3000` (previo al deploy); `https://vmi3131751.taila7f43b.ts.net` responde **200** |
| `.env.local` | `HERMES_API_URL=http://127.0.0.1:8642`, `HERMES_HOME=/home/hermes/.hermes`, `HERMES_VPS_URL=http://100.105.0.23:8642` (gitignored, sin secretos) |
| Repo después del build | `git status` limpio — el commit #2 de `brain-local` (untrack de `sw.js`/`workbox-*.js`) cumplió su objetivo |

### Checks de la Definición de Terminado

| Criterio | Estado | Evidencia |
|---|---|---|
| `curl -I http://127.0.0.1:3000` → 200 | ✅ | `HTTP/1.1 200 OK`, `x-nextjs-prerender: 1` |
| `pm2 status` online y sobrevive reinicio | ✅ | `hermes-pwa` online, `pm2-hermes.service` enabled + dump guardado |
| `tailscale serve status` con proxy al 3000 | ✅ | `https://vmi3131751.taila7f43b.ts.net` → `http://127.0.0.1:3000` |
| PWA desde el celular (4G/5G) | ⚠️ no verificable desde el VPS | Requiere prueba de Juan en el teléfono |
| Assets PWA instalable | ✅ | `/manifest.json`, `/sw.js` y los 4 íconos del manifest → 200 |
| Directorio de bots carga | ✅ | `GET /api/profiles` → 200, **8 bots** con `sessionCount` real (wolfim-growth 22, construvial-growth 9, ango-comercial 7, jobseeker 5, rws 2, almas-libres 1, korantis-ops 1, gymhealth 0) |
| **Bots del VPS en 🟢 Online** | ❌ | **los 8 devuelven `isOnline: false`** — ver §2 |
| Cambiar modelo desde la píldora | ⚠️ no probado (no ejecuto PATCH fuera del alcance; el endpoint está presente y el `config.yaml` de los perfiles es escribible por `hermes`) | — |

## 2. Por qué falla el 🟢 Online (causa raíz, con línea)

`GET /api/profiles` marca presencia con un fetch a
`${HERMES_API_URL}/p/${name}/api/sessions` (`src/app/api/profiles/route.ts:139`).
Contra el gateway del VPS ese path devuelve **404 `Unknown or unconfigured profile`**
para los 8 perfiles, y **200 para `default`**:

```
/p/wolfim-growth/api/sessions  -> 404 {"error": "Unknown or unconfigured profile"}
/p/ango-comercial/api/sessions -> 404
/p/default/api/sessions        -> 200 {"object":"list","data":[...]}
```

El gateway del VPS (`127.0.0.1:8642`, arriba desde antes, `API_SERVER_ENABLED` en
`/home/hermes/.hermes/.env`) **solo sirve el perfil `default`**, no los 8 que existen en
`/home/hermes/.hermes/profiles/`. Cuando el fetch falla, el código cae al fallback de
disco (por eso los `sessionCount` sí son correctos) y deja `isOnline = false`.

**Consecuencia práctica:** en el celular los bots del VPS se van a ver ⚪ Offline
aunque estén perfectamente operativos, con la barra amarilla de "requiere la PC local".

**Fix (fuera del alcance de este handoff, requiere decisión):** habilitar el serving
multi-perfil del gateway (`hermes gateway` con los perfiles configurados / modo
multiplex, según `gateway/platforms/shared_ingress.py:130`). No lo toqué: reiniciar el
gateway afecta a todos los perfiles del VPS y es una decisión de Juan.

## 3. Bugs encontrados de paso (no tocados)

1. **Badge de nodo invertido al correr en el VPS.** `src/app/api/profiles/route.ts:171`
   hace `node: "local"` **hardcodeado** para todo perfil leído de disco. En el VPS eso
   etiqueta los bots del VPS como 🖥️ *PC Local*, y los del gateway secundario (línea 207,
   `node: "vps"`) como ☁️ *VPS*. Desde el VPS los badges salen al revés.
2. **La PC local no es alcanzable desde el VPS.** `http://100.105.0.23:8642/v1/models` da
   timeout (el nodo `TRUzT` figura online en Tailscale, así que el gateway de la PC no está
   escuchando en la interfaz Tailscale, solo en loopback). Los bots de la PC no van a
   aparecer ni como Offline: no aparecen.
3. **`hermes-dashboard` está en crash-loop en el VPS (pre-existente, ajeno a la PWA):**
   **87.591 restarts**, cae cada ~5 s. Causa en `~/.pm2/logs/hermes-dashboard-out.log`:
   `Web UI build failed: node-deps.mjs ... died with <Signals.SIGABRT: 6>` usando
   `/home/hermes/.hermes/tools/node-26.7.0-linux-x64/bin/node`. Es el dashboard de
   `100.124.132.48:9119`. No lo toqué.

## 4. Aclaración sobre la `API_SERVER_KEY`

El `.env.local` del servidor **no necesita la key**: el flujo la toma del login del
cliente y la reenvía como `Authorization: Bearer` en cada request
(`src/lib/api.ts:5-13`, `route.ts:80`). O sea que el deploy **no quedó bloqueado** por
la key; Juan solo la tipea en la pantalla de login (`https://vmi3131751.taila7f43b.ts.net/auth/login`),
usando la del gateway del VPS (`/home/hermes/.hermes/.env`).

Dato útil verificado con esa key (sin exponerla): el gateway del VPS responde
`200 /v1/models` con el modelo `hermes-agent`, y `GET /api/groups` de la PWA devuelve
las salas grupales — incluida la actual, *"Brain Local, 100.124.132.48:9119"*.

## 5. Pendiente para cerrar el handoff

1. **Juan, en el teléfono:** abrir la URL, loguearse y confirmar que el directorio carga
   (ese es el criterio que no puedo verificar desde el VPS).
2. **Decisión de Juan:** habilitar el serving multi-perfil del gateway para que el 🟢
   Online funcione (ítem §2), y si queremos el fix del badge invertido (§3.1) — ese sí es
   cambio de código y le corresponde a `brain-local`/`web-builder`.
3. **Aviso aparte:** el crash-loop del dashboard (§3.3) merece su propio handoff.
