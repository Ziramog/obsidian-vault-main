---
event: action
handoff: HO-2026-10-04-001
at: 2026-10-09T08:54:12-03:00
by: brain-local
status: partial — credencial removida del perfil; restart del gateway pendiente de aprobación
---

# Token duplicado de `algolab` — credencial removida, adapter vivo pendiente de restart

## 1. Acción ejecutada (autorizada)

Por `events/2026-10-09T08-12-director-approval.md` (aprobación de Juan), se comentó la
línea 339 de `%LOCALAPPDATA%\hermes\profiles\algolab\.env`.

- antes: `TELEGRAM_BOT_TOKEN=8644817415:[REDACTADO]`
- después: `# TELEGRAM_BOT_TOKEN=8644817415:[REDACTADO]`
- backup: `.env.bak-20261009-084212-remove-vps-telegram-token`
- sha256 del `.env` resultante: `c9301df652d6ab2…`

Evidencia (sin tokens):

```text
$ grep -n "TELEGRAM_BOT_TOKEN" profiles/algolab/.env | sed 's/[0-9]\{8,10\}:.*/<REDACTED>/'
339:# TELEGRAM_BOT_TOKEN=<REDACTED>

$ grep -n "8644817415" profiles/algolab/config.yaml
(vacío — no hay bot_token hardcodeado en el config.yaml del perfil)

$ (bot id por perfil, sólo el id, no el token)
.env                               -> bot_id=8821822061   (default — propio, intacto)
profiles/algolab/.env              -> bot_id=8644817415   (VPS @Freedoom777bot — REMOVIDO)
profiles/trading-performance/.env  -> bot_id=8792684627   (propio, intacto)
profiles/brain-local/.env, web-builder, web-auditor -> # TELEGRAM_BOT_TOKEN=…  (ya comentados)
```

No se tocó el token del perfil default (`8821822061`) ni el de ningún otro bot.

## 2. El re-scan del multiplexer NO baja el adapter ya vivo

El multiplexer re-escaneó el perfil solo, segundos después del cambio:

```text
2026-10-09 07:42:26,764 INFO gateway.run_profile_reconcile: [MULTIPLEX] Re-scanned profile 'algolab' after config/.env change (0 adapter(s) connected)
(2026-09-30 08:55:23 la misma línea decía "1 adapter(s) connected" — cuando el token estaba presente)
```

Pero `run_adapters.py:1249-1253` es explícito:

> "Runtime re-scan of a served profile (config/.env changed): only platforms that are not
> already live or queued for reconnect are built — never a second poller on the same bot."

Es decir: `0 adapter(s) connected` = 0 adapters **nuevos**; el adapter Telegram viejo del
perfil sigue cargado. Se verifica en `gateway_state.json`:

```text
platforms.algolab:telegram  state=connected  writer_pid=107572
updated_at: 11:43:54Z → 11:46:26Z → 11:47:42Z → 11:48:58Z → 11:51:00Z → 11:52:16Z  (avanza ~cada 70s)
PID 107572 (hermes gateway run, multiplexer) → 6 conexiones ESTABLISHED a 149.154.166.110:443
```

En cambio `brain-local:telegram` no existe como entrada (su token nunca estuvo activo),
señal de que la entrada de `algolab` refleja un adapter realmente montado.

`gateway.log` local: 0 conflictos nuevos en las últimas 200 líneas.

## 3. Bloqueo — el restart requiere aprobación explícita

`hermes gateway restart` / `hermes -p algolab gateway restart` disparan un prompt de
aprobación ("stop/restart hermes gateway (kills running agents)").

1. `hermes gateway restart` → aprobado, pero sólo re-ruteó el perfil activo:
   `Profile 'brain-local' restart was not confirmed: host operation is still pending.`
   (log: `Profile 'brain-local' unserved — 0 adapter(s) stopped and unrouted` → re-served).
2. `hermes -p algolab gateway restart` → **sin aprobación (timeout)**. NO ejecutado.

## 4. Qué falta para cerrar

1. Aprobación de Juan para `hermes -p algolab gateway restart` (baja el adapter viejo al
   reconstruir los adapters del perfil desde el `.env` sin token).
2. Verificar que `platforms.algolab:telegram` desaparece de `gateway_state.json`.
3. Confirmación del VPS: sin conflictos `getUpdates` durante ≥90 s (criterio 3 del handoff;
   sólo el VPS puede verlo).
4. Prueba end-to-end: mensaje real a `@Freedoom777bot` y respuesta de brain-vps.

Reversión: descomentar la línea 339 y restart (<1 min).

Sin tokens escritos en el vault. Sin Git.
