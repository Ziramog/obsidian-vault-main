---
type: implementation-update
author: brain-vps
timestamp: 2026-06-27T18:28:00-03:00
---

# Agenda bot implementado en VPS

Implementación creada:
- `Hermes/Systems/vps/scripts/agenda-telegram-bot.py`
- `Hermes/Systems/vps/scripts/agenda-telegram-bot.sh`
- `~/.hermes/scripts/agenda-telegram-bot.sh`

Cron creado:
- job_id: `3d8783e0f40f`
- name: `Agenda Telegram bot poller`
- schedule: `every 1m`
- no_agent: `true`

Notas:
- El wrapper queda silencioso si no existe `TELEGRAM_AGENDA_BOT_TOKEN`.
- Así el cron puede quedar activo sin romper el gateway actual.
- El código reutiliza `agenda.py` y usa markdown de `Hermes/Agenda/YYYY-MM-DD.md` como única fuente de verdad.
- Audio previsto vía STT Hermes → respuesta texto.

Pendiente para habilitación real:
- crear bot `Agenda` en BotFather;
- guardar token en `.env` como `[credencial: TELEGRAM_AGENDA_BOT_TOKEN]`;
- hacer prueba real desde Telegram.
