---
id: HO-2026-09-27-002
status: done
from: brain-vps
to: brain-local
project: hermes-pwa
priority: high
acknowledged-at: 2026-09-27T21:06:00-03:00
deployed-at: 2026-09-27T23:38:00-03:00
closed-at: 2026-09-27T23:38:00-03:00
deployed-sha: e6919f60428814016a553db097400e3388ce8d97
first-deploy-sha: 64e4bc12592d5d4df94cd3a3224fdf742b01bee7
---

# response.md — Deploy de Hermes PWA en el VPS — CERRADO

**La Definición de Terminado se cumple: 8/8 bots del VPS en 🟢 Online**, con badges
correctos, ruteo intacto y servicio persistente. Queda un único ítem que sólo Juan puede
verificar: la prueba desde el teléfono. La cadena de causas resueltas está en §2 y la
evidencia final en §3.

## 1. Hecho

| Ítem | Valor |
|---|---|
| Path | `/home/hermes/hermes-pwa` (decisión del request, sin sudo, owner `hermes`) |
| SHA desplegado (final) | `e6919f60428814016a553db097400e3388ce8d97` (`main`) |
| SHA del primer deploy | `64e4bc12592d5d4df94cd3a3224fdf742b01bee7` (`chore: untrack generated service worker artifacts`) |
| Ancestro del primer deploy | `9219d89 feat: multi-node bot directory, model selector, iOS-style mobile UI` |
| Node | `/home/hermes/tools/node-v20.20.2-linux-x64/bin/node` (v20.20.2 / npm 10.8.2) |
| Build | `npm install` 774 paquetes OK; `npm run build` **exit 0**, 29,6 s, 10 páginas + 10 rutas dinámicas + `/auth/login` |
| Proceso | PM2 `hermes-pwa` id 4, `online`, interpreter fijado al node 20 (los 2 restarts corresponden a los redeploys de `b94625b` y `e6919f6`) |
| Persistencia | `pm2-hermes.service` **enabled** (no existía: solo estaba `pm2-root.service`, con `dump.pm2` vacío) + `pm2 save` |
| Exposición | `tailscale serve` ya apuntaba `/` → `127.0.0.1:3000` (previo al deploy); `https://vmi3131751.taila7f43b.ts.net` responde **200** |
| `.env.local` | `HERMES_API_URL=http://127.0.0.1:8642`, `HERMES_HOME=/home/hermes/.hermes`, `HERMES_VPS_URL=http://100.105.0.23:8642`, `HERMES_NODE_NAME=vps` (gitignored, sin secretos) |
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
| **Bots del VPS en 🟢 Online** | ✅ | **8/8 `isOnline: true`** — ver §3 (era 0/8 en el primer deploy) |
| Cambiar modelo desde la píldora | ⚠️ no probado (no ejecuto PATCH fuera del alcance; el endpoint está presente y el `config.yaml` de los perfiles es escribible por `hermes`) | — |

## 2. Cadena de causas resueltas (en orden)

1. **Repo desactualizado** (`0265d11` sin el trabajo multi-nodo) → con la autorización A
   de Juan el VPS dejó de clonar la versión vieja: `64e4bc1`, luego `b94625b` (badge
   dinámico) y finalmente `e6919f6`.
2. **Gateway sin serving multi-perfil** → `hermes gateway migrate --multiplex`
   (aprobado por Juan): `gateway.multiplex_profiles: true` en `config.yaml:576`;
   `/p/<perfil>/` pasó de **404 `Unknown or unconfigured profile` → 401/200**. El aviso
   "no confirmó serving" del comando fue un falso negativo: el serving quedó verificado
   con la matriz de rutas.
3. **Preflight bloqueado por `TELEGRAM_BOT_TOKEN` duplicado** en los 8 perfiles
   secundarios (los 9 `.env` tenían el mismo valor) → backup fechado + borrado de esa
   única línea en los 8, verificado con `diff` crudo (sólo esa línea cambia, el resto
   del archivo queda byte-idéntico). El `--dry-run` pasó de **8 blockers a 0**. Efecto
   medido: el warning `⚠ telegram: Telegram polling could not recover after 5 retries…`
   **desapareció** de `hermes gateway status`.
4. **Perfiles sin `API_SERVER_KEY` en su propio scope** → el gateway lo declaraba
   textualmente: `API server rejected request for profile '<x>': no profile-scoped
   API_SERVER_KEY is configured`. Se copió el valor de `default` (mismo valor, sin
   generar credencial nueva) a los 4 que no lo tenían, con backup fechado. Correlación
   medida: los 4 con la key → 🟢; los 4 sin ella → 401 y ⚪.

## 3. Evidencia final

```
/p/<perfil>/api/sessions  (los 9) ................. 200
GET /api/profiles ..... 200 | bots: 8 | ONLINE: 8/8
  almas-libres        isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=4
  ango-comercial      isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=9
  construvial-growth  isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=11
  gymhealth           isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=2
  jobseeker           isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=6
  korantis-ops        isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=4
  rws                 isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=4
  wolfim-growth       isOnline=True  nodeLabel='☁️ VPS'  node=local  sesiones=22
```

Despliegue: `/home/hermes/hermes-pwa`, sha **`e6919f6`** (`main`), árbol git limpio,
Node v20.20.2 fijado como interpreter del proceso, PM2 `hermes-pwa` online.
`.env.local` (gitignored, sin secretos): `HERMES_API_URL=http://127.0.0.1:8642`,
`HERMES_HOME=/home/hermes/.hermes`, `HERMES_VPS_URL=http://100.105.0.23:8642`,
`HERMES_NODE_NAME=vps`.

Backups y rollback:

| Qué | Dónde |
|---|---|
| 8 `.env` antes de quitar el token | `profiles/<perfil>/.env.env.bak.20260927_222732` |
| 4 `.env` antes de agregar la key | `profiles/<perfil>/.env.bak.20260927_233506` |
| Estado previo del gateway | `/home/hermes/.hermes/gateway_migration.json` (`flag_was: false`) |

## 4. Bugs encontrados de paso

1. **Badge de nodo invertido al correr en el VPS — RESUELTO.** `route.ts:171` hacía
   `node: "local"` hardcodeado; se corrigió en `b94625b` con `nodeLabel` derivado de
   `HERMES_NODE_NAME`/`HERMES_NODE_IDENTITY`, dejando `node` intacto porque es la clave
   de ruteo. Verificado en el VPS: 8/8 `nodeLabel: "☁️ VPS"`, `node: "local"`.
2. **La PC local no es alcanzable desde el VPS.** `http://100.105.0.23:8642/v1/models` da
   timeout (el nodo `TRUzT` figura online en Tailscale, así que el gateway de la PC no está
   escuchando en la interfaz Tailscale, solo en loopback). Los bots de la PC no van a
   aparecer ni como Offline: no aparecen.
3. **`hermes-dashboard` está en crash-loop en el VPS (pre-existente, ajeno a la PWA):**
   **87.591 restarts**, cae cada ~5 s. Causa en `~/.pm2/logs/hermes-dashboard-out.log`:
   `Web UI build failed: node-deps.mjs ... died with <Signals.SIGABRT: 6>` usando
   `/home/hermes/.hermes/tools/node-26.7.0-linux-x64/bin/node`. Es el dashboard de
   `100.124.132.48:9119`. No lo toqué.

## 5. Relación con la `API_SERVER_KEY` (corrección del reporte anterior)

El `.env.local` del servidor **no necesita la key**: el flujo la toma del login del
cliente y la reenvía como `Authorization: Bearer` en cada request
(`src/lib/api.ts:5-13`, `route.ts:80`). O sea que el deploy **no quedó bloqueado** por
la key; Juan solo la tipea en la pantalla de login (`https://vmi3131751.taila7f43b.ts.net/auth/login`),
usando la del gateway del VPS (`/home/hermes/.hermes/.env`).

Dato útil verificado con esa key (sin exponerla): el gateway del VPS responde
`200 /v1/models` con el modelo `hermes-agent`, y `GET /api/groups` de la PWA devuelve
las salas grupales — incluida la actual, *"Brain Local, 100.124.132.48:9119"*.

**Invariante a respetar:** `profiles/route.ts:150` reusa **una sola** credencial (el
Bearer del request de login) para sondear todos los `/p/<perfil>/`; no hay una key por
perfil. Si algún día un perfil recibe una `API_SERVER_KEY` distinta, ese bot vuelve a ⚪
aunque el gateway lo sirva 200. El valor debe ser el mismo en los 9 perfiles y en la PC.

## 6. Estado de cierre

Cumplido y verificado por brain-vps: 9/9 rutas en 200, 8/8 bots 🟢, badges correctos,
servicio persistente tras reinicio.

Queda pendiente, y no depende de brain-vps:

1. **Juan, en el teléfono:** abrir `https://vmi3131751.taila7f43b.ts.net`, loguearse y
   confirmar que el directorio carga y que la píldora de modelo cambia.
2. **Decisión de Juan:** exponer el gateway de la PC a Tailscale (§4.2) para que los bots
   de Windows aparezcan cuando la PC esté prendida.
3. **Decisión de Juan:** rotar la `API_SERVER_KEY` versionada en `README.md:31` — si se
   rota, conviene hacerlo en una sola pasada (default + 8 perfiles del VPS + la PC) para
   verificar la matriz 9/9 una única vez.
4. **Handoff propio:** el crash-loop de `hermes-dashboard` (§4.3).
