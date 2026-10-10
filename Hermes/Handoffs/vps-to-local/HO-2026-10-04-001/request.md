---
id: HO-2026-10-04-001
status: done
from: brain-vps
to: brain-local
project: hermes-system
priority: normal
depends-on: []
created-at: 2026-10-04T04:20:00-03:00
acknowledge-by: next-local-session
due-at: 2026-10-06T18:00:00-03:00
escalate-after: 48h
closed-at: 2026-10-09T23:58:00-03:00
closed-by: brain-vps
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — verificar segundo poller de Telegram con el token del gateway VPS

## Motivo

El 2026-10-04 el adaptador Telegram del gateway VPS (bot **Freedoom777bot**, id `8644817415`)
quedó en estado `fatal` con `telegram_polling_conflict`:

- 00:29:43 — conectó OK tras un update de Hermes.
- 00:44:25 — empezó a recibir `Conflict: terminated by other getUpdates request`
  y a las 00:48:21 quedó `fatal` (5 reintentos agotados): ~3h20m sin Telegram entrante.
- 04:16 — un `hermes gateway restart` limpio lo reconectó; estable desde entonces.

Durante el diagnóstico desde el VPS:

- Ningún otro proceso del VPS usa ese token (`hermes gateway list` = 1 gateway; el
  `agenda-telegram-bot.py` usa otro bot: `TELEGRAM_AGENDA_BOT_TOKEN` = 8821936359).
- Long-polls de prueba desde el VPS (8s y 30s, varias rondas entre 04:14 y 04:15)
  respondieron `ok` sin conflicto → no había un segundo poller activo en ese momento.
- El onset a las 00:44 (15 min después de un connect sano) sugiere un cliente externo
  o intermitente con el mismo token, no un error del gateway VPS.

## Objetivo verificable

Determinar si algún host/proceso de la PC (o el nodo peer `100.105.0.23`, Hermes
Desktop, OpenClaw, script propio) hace `getUpdates` con el token del gateway VPS.

Criterios de aceptación:

1. Respuesta explícita: SÍ / NO existe otro poller de `8644817415` fuera del VPS.
2. Si SÍ: identificar el proceso/host y desactivarlo o darle un token propio.
3. Si NO: dejar registrado en este handoff (`events/`) el resultado y cerrar como
   `falso positivo / sesión stale`.

## Cómo verificar

En la PC, buscar cualquier proceso que use ese token o el método `getUpdates`:

```text
# Windows / WSL: buscar el bot id en configs y .env del perfil brain-local
grep -R "8644817415" %USERPROFILE%\.hermes 2>$null
# procesos Hermes/OpenClaw activos
Get-Process | Where-Object {$_.ProcessName -match 'hermes|openclaw|node|python'}
# prueba de conflicto: mientras el gateway VPS NO esté reconectando,
# un long-poll desde la PC debe dar "Conflict" sólo si algo más está polling
curl "https://api.telegram.org/bot<TOKEN>/getUpdates?timeout=30&offset=-1"
```

## Restricción

- NO pegar el token completo en el vault ni en el handoff. Referenciarlo como
  [credencial: TELEGRAM_BOT_TOKEN].

## Nota de arquitectura (residual, para Juan)

Los 9 `config.yaml` del VPS (launch + 8 profiles) tienen el mismo `telegram.bot_token`
hardcodeado. Hoy el multiplexer los sirve con un solo adaptador, pero cualquier arranque
standalone de un perfil (o de un perfil en la PC con la misma config copiada) genera el
conflicto. Conviene que todos referencien la misma variable de entorno en vez de repetir
el token.
