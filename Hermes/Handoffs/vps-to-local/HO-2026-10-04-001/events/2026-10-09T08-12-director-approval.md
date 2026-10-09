---
event: director-approval
handoff: HO-2026-10-04-001
at: 2026-10-09T08:12:59-03:00
by: brain-vps
approved-by: Juan
status: ready-to-execute
---

# Aprobación — separar el bot general del perfil algolab

Juan eligió explícitamente la arquitectura de **dos bots separados**:

- `@Freedoom777bot` → conversación general con brain-vps.
- `@Agenda_Hbot` → agenda estricta.

## Acción autorizada en la PC

Quitar/comentar del perfil `algolab` la credencial duplicada `[credencial: TELEGRAM_BOT_TOKEN]` que corresponde a `@Freedoom777bot`, sin tocar el token propio del perfil default ni otros bots.

Después:

1. Reiniciar o recargar el gateway local.
2. Confirmar que `algolab` ya no monta ese adapter de Telegram.
3. Verificar durante al menos 90 segundos que el gateway VPS deja de registrar conflictos repetidos de `getUpdates`.
4. Enviar un mensaje real a `@Freedoom777bot` y comprobar que brain-vps responde.
5. Cerrar el handoff con evidencia sin escribir tokens.
