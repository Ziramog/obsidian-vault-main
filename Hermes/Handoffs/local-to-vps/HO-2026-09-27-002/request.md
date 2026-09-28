---
id: HO-2026-09-27-002
status: ready
from: brain-local
to: brain-vps
project: hermes-pwa
priority: high
created-at: 2026-09-27T19:51:47-04:00
acknowledge-by: next-vps-session
escalate-after: 24h
briefing: Hermes/Briefings/current.md
director: Juan
depends-on: []
blocked-on: decision-de-juan (ver §2 — push autorizado del working tree)
---

## 1. Pedido

Desplegar **Hermes PWA** (cliente mobile para el gateway de Hermes) en el VPS
`vmi3131751` (`100.124.132.48`, Tailscale), persistente 24/7 con PM2, para que
los bots sean accesibles desde el celular sin depender de la PC local `truzt`
encendida.

Documento técnico completo (stack, endpoints, pasos de deploy, variables de
entorno): [`BRAIN_LOCAL_HANDOVER.md`](./BRAIN_LOCAL_HANDOVER.md) — mismo
directorio, copia verbatim del original `C:\Projects\hermes-pwa\BRAIN_LOCAL_HANDOVER.md`.

**Destino del código:** `/opt/hermes-pwa`
**Repo:** `https://github.com/Ziramog/PWA-Hermes.git` (branch `main`)
**Puerto:** `3000` detrás de `tailscale serve --bg 3000`
**Resumen del plan (detalle en el handover):**
1. Verificar Node >= v20 en el VPS.
2. Traer el código a `/opt/hermes-pwa`.
3. Crear `/opt/hermes-pwa/.env.local` con `HERMES_API_URL=http://127.0.0.1:8642`,
   `HERMES_HOME=/root/.hermes`, `HERMES_VPS_URL=http://100.105.0.23:8642`.
   **CORREGIDO 2026-09-27: la ruta real es `/home/hermes/.hermes` y el deploy va a
   `/home/hermes/hermes-pwa` (sin sudo). Ver §5.**
4. `npm install && npm run build` (debe salir con código 0).
5. `pm2 start npm --name hermes-pwa -- run start && pm2 save && pm2 startup`.
   **CORREGIDO: requiere startup propio del usuario `hermes`. Ver §5.**
6. `tailscale serve --bg 3000` y verificar `tailscale serve status`.
   **YA HECHO en el VPS: `https://vmi3131751.taila7f43b.ts.net` → `127.0.0.1:3000`.**
   **Paso saltable.**

## 2. BLOQUEANTE REAL — el repo de GitHub está DESACTUALIZADO

Verificado por mí en el working tree local (`C:\Projects\hermes-pwa`) el
2026-09-27 19:45-04:00:

- `origin/main` está en `0265d11` — **y ese commit NO contiene el trabajo
  multi-nodo** (BotDirectory, badges PC/VPS, selector de modelo, PATCH
  `/api/profiles`, responsive iOS, arreglos de streaming).
- El working tree local tiene **15 archivos modificados sin commitear (694
  inserciones / 486 borrados)** + **5 rutas sin trackear** (`BotDirectory.tsx`,
  `public/icons/`, `scripts/`, `iniciar-pwa.bat`, `BRAIN_LOCAL_HANDOVER.md`).
- O sea: **si clonás `PWA-Hermes.git` hoy, deployás la versión vieja.**

**Regla de equipo:** no commiteo ni pusheo sin autorización explícita de Juan.
Por eso este handoff queda `blocked-on: decision-de-juan`.

**Opciones para destrabar (Juan elige):**
- **A (recomendada):** Juan autoriza `git add -A && git commit && git push origin main`
  desde la PC local. Después el VPS hace `git clone` limpio y este handoff se
  desbloquea sin más intervención.
- **B:** transferencia directa PC → VPS por Tailscale:
  `rsync -avz --exclude node_modules --exclude .next /c/Projects/hermes-pwa/ root@100.124.132.48:/opt/hermes-pwa/`
  (requiere que Juan lo corra o autorice; evita el repo pero deja el VPS sin
  historial git).
- **C:** tarball del working tree publicado en el vault para que el VPS lo baje
  por Git. Más ruidoso, solo si A y B fallan.

## 3. Notas de seguridad

- `.env.local` **no va al vault ni a un commit** con secretos. En la PC hoy solo
  tiene las dos URLs de gateway (sin API key); igual queda fuera por convención.
- La API key del gateway del VPS se la pasa Juan al brain-vps por el canal que
  él prefiera — **no escribirla acá**.
- En el VPS, cuando la PWA corra allá, `HERMES_VPS_URL` apunta *de vuelta* a la PC
  local (`100.105.0.23:8642`) para descubrir los bots de Windows cuando esté
  prendida. Los bots de Windows aparecerán ⚪ Offline con la PC apagada — es el
  comportamiento esperado, no un bug.

## 4. Definición de terminado

- `curl -I http://127.0.0.1:3000` → `200 OK` en el VPS.
- `pm2 status` muestra `hermes-pwa` como `online` sobreviviendo un reinicio.
- `tailscale serve status` muestra el proxy HTTPS al puerto 3000.
- Desde el celular (4G/5G): el Directorio de Bots carga, los bots del VPS dan 🟢
  Online, se puede abrir un chat y cambiar el modelo desde la píldora del header.
- `response.md` en este mismo directorio con URLs, paths y evidencia de los checks.

---

## 5. Preflight del VPS — correcciones al plan (2026-09-27, brain-vps)

Auditoría real del servidor `vmi3131751` contra este documento. **Estas
correcciones pisan lo que dice `BRAIN_LOCAL_HANDOVER.md`:**

1. **`HERMES_HOME` está MAL en el handover.** La instalación vive en
   `/home/hermes/.hermes` y todo corre como usuario `hermes`, no root (`/root` no
   es listable). Con `/root/.hermes` el `GET/PATCH /api/profiles` no encuentra
   ningún perfil.
2. **Node: no hay nvm ni volta.** El `node -v` (26.7.0) sale del toolchain de
   Hermes (`/home/hermes/.hermes/tools/node-26.7.0-linux-x64/bin/node`). Fijar
   Node 20 = instalar por NodeSource (sudo passwordless, OK) **y** garantizar que
   el PATH del PM2 de `hermes` apunte a ese node, no al de Hermes.
3. **El criterio "sobrevive un reinicio" hoy no se cumple solo.** Los procesos
   viven en el PM2 del usuario `hermes` (`agenda-telegram-bot`,
   `hermes-dashboard`), pero la única unit de arranque es `pm2-root.service`
   (root, `enabled`) y el `dump.pm2` de root está **vacío**. Un `pm2 save` desde
   `hermes` no resucita nada post-reboot: hace falta startup propio de `hermes`
   (systemd user + linger, o unit system corriendo como `hermes`).
4. **Falta el único secreto.** El gateway `127.0.0.1:8642` responde
   `401 Invalid gateway API key (API_SERVER_KEY)`. `HERMES_API_URL` es correcta;
   lo que falta es la key que carga la PWA en el login. **La pasa el director por
   fuera del vault — no se escribe acá.** (En la PC local el nombre de la variable
   es `API_SERVER_KEY`; en el VPS vive en `/home/hermes/.hermes/.env`.)
   @director: leerla ahí y pasarla a brain-vps por canal privado.

**Atajo:** `tailscale serve` ya apunta `https://vmi3131751.taila7f43b.ts.net` →
`http://127.0.0.1:3000`. El Paso 6 queda saltable.

**Path de deploy — decisión: `/home/hermes/hermes-pwa`** (no `/opt`): corre como el
mismo usuario dueño de PM2 y del `HERMES_HOME`, sin sudo y sin archivos
root-owned. `/opt` está limpio pero no aporta nada acá.

**Estado de red verificado por el VPS:** `TRUzT` (`100.105.0.23`) figura online, así
que `HERMES_VPS_URL` es válido. Puerto 3000 libre; ocupados 22, 53, 443, 631, 4002,
4011, 5003, 8642, 9119. Disco 73G libres / RAM 5.2Gi disponibles. PM2 6.0.14.
Tailscale 1.102.2.

**Sigue bloqueado en la decisión A/B/C del director** (ver §2). El handoff pasa a
`in-progress` cuando esté el sha del push (A) o la transferencia rsync (B).
