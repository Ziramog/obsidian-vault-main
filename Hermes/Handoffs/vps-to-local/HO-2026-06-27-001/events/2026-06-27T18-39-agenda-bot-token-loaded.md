---
type: activation-update
author: brain-vps
timestamp: 2026-06-27T18:39:00-03:00
---

# Agenda bot — token cargado y bot validado

Estado actualizado:
- Token cargado fuera del vault en `~/.hermes/.env` como `[credencial: TELEGRAM_AGENDA_BOT_TOKEN]`.
- `getMe` validó el bot: `@Agenda_Hbot` / nombre `Agenda`.
- Cron del poller sigue activo: `3d8783e0f40f`.

Bloqueante real restante:
- `getUpdates` devolvió `0` mensajes.
- El intento de `sendMessage` al chat principal devolvió `400 Bad Request`, consistente con bot nuevo sin `Start` del usuario.

Siguiente paso de Juan:
- abrir `@Agenda_Hbot` en Telegram;
- tocar `Start`;
- mandar `/hoy` o `mañana 9 llamar a GAMA`.

Luego brain-vps puede verificar end-to-end real inmediatamente.
