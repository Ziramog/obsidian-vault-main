---
event: finding
handoff: HO-2026-10-04-001
at: 2026-10-04T17:02:31-04:00
by: brain-local
verdict: SÍ existe segundo poller — perfil algolab de esta PC
---

# Finding — segundo poller de `8644817415` (Freedoom777bot)

## Respuesta a criterio 1

**SÍ.** El segundo poller del token del gateway VPS (`[credencial: TELEGRAM_BOT_TOKEN]`,
bot id `8644817415`) es **esta misma PC**: perfil **`algolab`**, servido por el gateway
local (PID 13808, multiplexer del perfil `default`).

## Evidencia (cruda)

```text
# 1. profiles/algolab/.env  (mtime 2026-09-27 13:04 -04) — único .env de la PC con ese bot id
TELEGRAM_BOT_TOKEN=8644817415:[REDACTADO]

# 2. gateway_state.json (PID 13808, kind hermes-gateway, gateway_state running)
telegram                    → connected   (profile default)
algolab:telegram            → connected   (updated_at 2026-10-04T13:56:52Z)
trading-performance:telegram→ connected

# 3. hermes gateway list
✓ default                  — PID 13808
✓ algolab                  — served by the default multiplexer
✓ brain-local (current)    — served by the default multiplexer   (…10 profiles)

# 4. netstat — polling vivo desde la PC
TCP 192.168.0.48:60xxx  149.154.166.110:443  ESTABLISHED  13808

# 5. Otros bot ids de la PC (todos distintos del VPS)
.env (default)                  TELEGRAM_BOT_TOKEN=8821822061:[REDACTADO]
profiles/trading-performance/.env TELEGRAM_BOT_TOKEN=8792684627:[REDACTADO]
```

### Correlación temporal (EDT -04 == ART -03 + 1h)

```text
VPS  incidente: connect OK 00:29:43 ART · onset conflicto 00:44:25 ART · fatal 00:48:21 ART
                 → = 23:29:43 / 23:44:25 / 23:48:21 EDT del 2026-10-03

PC   gateway.log / gateway-stdio.log (hora local -04):
  2026-10-03 23:44:04  restart del gateway local (update del Hermes desktop)
  2026-10-03 23:44:18  ✓ telegram connected (default) — "getUpdates progressing (generation 1)"
  2026-10-03 23:44:26  ✗ telegram failed to connect (profile: algolab)
  2026-10-03 23:44:50  ✓ telegram reconnected (profile: algolab)   ← arranca a pollear el token del VPS
  2026-10-04 09:52:12–09:56:26  adapter telegram__home_2dbab1960315 (algolab):
                                 "Telegram polling conflict (1/5 … 5/5)"
                                 "Updater made no getUpdates progress and is not running"
  2026-10-04 09:51:57 / 23:44:52  "Home-channel startup notification failed for
                                 telegram:1479438002: Chat not found"
```

El adapter `algolab` reconecta en el **mismo minuto** en que el VPS empieza a registrar
`Conflict: terminated by other getUpdates request`. Y el conflicto es **espejo**: hoy a
las 09:52–09:56 EDT el que se cae es el adapter local cuando el VPS tiene el token tomado
→ es una carrera: gana el gateway que arranca primero.

## Lectura

Herramienta del incidente = update del Hermes desktop en la PC (23:44:04 EDT), que reinició
el gateway local; al levantarse, el multiplexer montó el adapter del perfil `algolab` con el
mismo `TELEGRAM_BOT_TOKEN` del gateway VPS y le robó el long-poll.

## Criterio 2 — acción correctiva: ESCALADO a Juan (no ejecutado)

Fix de una línea en `AppData\Local\hermes\profiles\algolab\.env` (comentar/eliminar
`TELEGRAM_BOT_TOKEN`) o bot propio para `algolab` vía BotFather. Está **fuera de mi zona
de escritura** (perfil ajeno) → requiere aprobación explícita de Juan. No se tocó nada.

Recomendación: comentar la línea. El adapter `algolab` no tiene uso útil hoy — su home
channel `1479438002` responde "Chat not found" en cada arranque (config cruzada). Reversible
en <1 min: comentar la línea y `hermes gateway restart` (o esperar el re-scan de perfil).

## Criterio 3 — no aplica

No es falso positivo ni sesión stale. Ver el `response.md` de este handoff.
