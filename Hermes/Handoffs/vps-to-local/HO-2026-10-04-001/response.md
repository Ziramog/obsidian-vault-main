---
id: HO-2026-10-04-001
status: done
from: brain-local
to: brain-vps
at: 2026-10-04T17:02:31-04:00
closed-at: 2026-10-09T08:47:00-03:00
verdict-objetivo-1: SÍ — segundo poller = perfil `algolab` de la PC (truzt / 100.105.0.23)
verdict-objetivo-2: acción correctiva ESCALADA a Juan (fuera de zona de escritura de brain-local)
---

# Response — HO-2026-10-04-001

## 1. Respuesta explícita (criterio de aceptación 1)

**SÍ.** Existe un segundo poller del token del gateway VPS
(`[credencial: TELEGRAM_BOT_TOKEN]`, bot id `8644817415`, Freedoom777bot) fuera del VPS:
la **PC local de Juan** (`truzt`, nodo Tailscale `100.105.0.23`), perfil **`algolab`**,
servido por el gateway local **PID 13808** (`hermes_gateway run`, multiplexer del perfil
`default`; `hermes gateway list` → `algolab — served by the default multiplexer`).

Herramienta del incidente: el update del Hermes desktop en la PC reinició el gateway local
a las **2026-10-03 23:44:04 EDT**; al levantar, el multiplexer montó el adapter Telegram del
perfil `algolab` con el mismo token del gateway VPS y le robó el long-poll — mismo minuto
que el onset del VPS (00:44:25 ART).

Evidencia cruda completa: `events/2026-10-04T17-02-finding-segundo-poller-algolab-pc.md`.

## 2. Host/proceso identificado

```text
host        truzt (esta PC, Windows) — Tailscale 100.105.0.23
proceso     PID 13808 · python -m hermes_cli.main gateway run   (Hermes gateway 0.21.5)
perfil      algolab  (adapter "platforms__telegram__home_2dbab1960315")
fuente      AppData\Local\hermes\profiles\algolab\.env → TELEGRAM_BOT_TOKEN=8644817415:[REDACTADO]
            (mtime 2026-09-27 13:04 -04 · único .env de la PC con ese bot id)
estado hoy  algolab:telegram = connected (updated_at 2026-10-04T13:56:52Z) pero con
            "Updater made no getUpdates progress and is not running" → carrera de token:
            gana el gateway que arranca primero, el otro acumula conflictos (1/5 … 5/5).
```

También con adapter Telegram en la PC pero **con otro bot** (no generan conflicto):
`default` → `8821822061`, `trading-performance` → `8792684627`.

## 3. Desactivación — NO ejecutada, requiere a Juan

El fix es una línea en `AppData\Local\hermes\profiles\algolab\.env` (comentar/eliminar
`TELEGRAM_BOT_TOKEN`) o darle a `algolab` un bot propio por BotFather. Ambas cosas están
**fuera de la zona de escritura de brain-local** (perfil ajeno) → escalado, no ejecutado.

**Recomendación:** comentar la línea. El adapter `algolab` no tiene uso útil hoy: su home
channel `1479438002` responde `Chat not found` en cada arranque (config cruzada con el bot
del VPS). Reversible en <1 min: comentar la línea y `hermes gateway restart` (o esperar el
re-scan de perfil del multiplexer).

## 4. Criterio 3 — no aplica

No es falso positivo ni sesión stale. No se cierra como `falso positivo / sesión stale`.

## 5. Notas para brain-vps

- El riesgo de la §Nota de arquitectura quedó **confirmado**: el mismo `TELEGRAM_BOT_TOKEN`
  hardcodeado en los `config.yaml`/`.env` del VPS reapareció en `profiles/algolab/.env` de
  la PC. Unificar en variable de entorno única, y en la PC ningún perfil debería reutilizar
  un bot del VPS.
- Hay un segundo frente de ruido en la misma PC, **no relacionado**: su `.env` raíz sigue
  con `HASS_URL=http://homeassistant.local:8123` desde el 2026-10-03 23:47.
- Ninguna acción ejecutada fuera del vault. Sin Git.

## Referencias

- `events/2026-10-04T17-02-ack-brain-local.md`
- `events/2026-10-04T17-02-finding-segundo-poller-algolab-pc.md`
- `Hermes/Briefings/current.md` (vigente, vence 2026-10-08T17:40-03)

## 6. Cierre — 2026-10-09 (post-aprobación de Juan)

El blocker de §3 quedó resuelto: Juan aprobó el 2026-10-09 08:12-03
(`events/2026-10-09T08-12-director-approval.md`) y la acción ya está aplicada en la PC.

```text
# AppData/Local/hermes/profiles/algolab/.env  (mtime 2026-10-09 08:42:13 -03)
línea 339 -> # TELEGRAM_BOT_TOKEN=8644817415:[REDACTADO]   (comentada; activas = 0)
```

- El multiplexer `default` (PID 107572) detectó el cambio de `.env` y re-escaneó `algolab`
  → **0 adapters conectados** (`gateway.log` 2026-10-09 07:42:26 -04). Recarga hecha; no se
  forzó restart.
- Ningún `config.yaml` de perfil lleva `telegram.bot_token` (0 hits). Otros bots de la PC
  (`default` 8821822061, `trading-performance` 8792684627) intactos.
- **Pendiente del lado VPS (brain-vps):** confirmar ≥90 s sin `polling conflict` tras las
  08:42-03, y prueba real de mensaje a `@Freedoom777bot`. No accesible desde la PC.

Detalle y evidencia cruda: `events/2026-10-09T08-47-done-algolab-token-commented.md`.

## 7. CORRECCIÓN — 2026-10-09 09:18-03 (el §6 estaba mal)

El §6 afirmaba que el re-scan del `.env` había desmontado el adapter y que no hacía falta
restart. **Incorrecto.** `gateway_state.json` mostró `algolab:telegram` con
`state: connected` y `updated_at` fresco (12:15:16Z) → el poller seguía vivo con el token
`8644817415`; los conflictos en el VPS continuaron tras las 08:42.

**Fix real:** `hermes -p default gateway --accept-hooks restart` a las **09:16:41-03**
(PID 107572 → 117716). Tras el arranque, `gateway.log`:
`Profile 'algolab': skipping telegram - no bot credential in this profile's secrets`, y
`gateway_state.json` ya no tiene `algolab:telegram`. La PC ya no pollea el bot del VPS.

Lección y procedimiento: `Hermes/Systems/local/telegram-multiplexer-token-reload.md`.
Evidencia: `events/2026-10-09T09-18-correction-hard-restart-needed.md`.
Verificación ≥90 s en el VPS: pendiente de brain-vps.
