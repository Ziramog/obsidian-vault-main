---
type: operational-change
system: agenda-telegram-bot
owner: brain-vps
status: active
created-at: 2026-06-28T19:50:00-03:00
---

# Agenda Telegram Bot — resident service mode

## Cambio

Juan reportó que el problema principal de la agenda en Telegram era la demora. Se reemplazó el polling por cron como camino principal por un proceso residente PM2 con long-polling.

## Estado actual

- Bot dedicado: `@Agenda_Hbot`
- Servicio PM2: `agenda-telegram-bot`
- Script residente: `Hermes/Systems/vps/scripts/agenda-telegram-bot-service.sh`
- Loop: `Hermes/Systems/vps/scripts/agenda-telegram-bot.py --loop --poll-timeout 25`
- Logs:
  - `/home/hermes/.hermes/logs/agenda-telegram-bot.out.log`
  - `/home/hermes/.hermes/logs/agenda-telegram-bot.err.log`
- Lock: `Hermes/Systems/vps/state/agenda-bot-loop.lock`

## Crons pausados

Se pausaron los 4 crons anteriores de polling para evitar doble `getUpdates`:

- `3d8783e0f40f` — Agenda Telegram bot poller
- `faaa769592e9` — Agenda bot poller +15s
- `b967560c84c5` — Agenda bot poller +30s
- `0e66a98691dc` — Agenda bot poller +45s

El scanner de recordatorios `acafddde60b4` sigue activo cada 5 minutos; no es el bot interactivo.

## Verificación ejecutada

- `python3 -m py_compile agenda-telegram-bot.py` OK
- `--simulate-text /foco` OK
- `--simulate-text /mañana` OK en 0.232s
- `pm2 describe agenda-telegram-bot` → online, 0 restarts
- Logs sin errores tras >60s

## Comandos operativos

```bash
pm2 list
pm2 describe agenda-telegram-bot
pm2 logs agenda-telegram-bot --lines 80
pm2 restart agenda-telegram-bot
pm2 save
```

## Expectativa UX

- Texto simple en `@Agenda_Hbot`: ~1–3 segundos.
- Audio: mayor demora por descarga + transcripción local.
- El bot general `@Freedoom777bot` no debe usarse para comandos `/hoy`, `/mañana`, `/foco`; esos comandos pertenecen al bot Agenda.
