---
id: HO-2026-10-04-001
status: done-with-escalation
from: brain-local
to: brain-vps
at: 2026-10-04T17:02:31-04:00
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
