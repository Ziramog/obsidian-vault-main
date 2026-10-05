# Incidente — Telegram polling caído (gateway VPS)

- Fecha: 2026-09-28 04:00 ART
- Detectado por: `scripts/hermes-health-check.py` (cron 04:00)
- Estado: mitigado con restart programado del gateway (04:08 ART)

## Qué pasó

El adaptador de Telegram del gateway quedó en estado `fatal`
(`telegram_polling_conflict`) el **27/09 a las 19:57 ART** y volvió a fallar a las
**23:56 ART**. Desde entonces no hubo `getUpdates`: Telegram de entrada quedó
caído ~4 h (el envío de alertas por API sí funcionó, por eso los avisos salieron).

Gateway service: `hermes-gateway.service` (systemd --user), PID 2508481,
arrancado el 27/09 22:29 ART.

## Diagnóstico

- `gateway_state.json` → `platforms.telegram.state = fatal`,
  `error_code = telegram_polling_conflict`.
- Sonda directa `getUpdates` con el token del bot (04:05 ART): `ok: true`,
  0 updates → **ningún otro proceso retiene el polling**; el gateway
  simplemente no volvió a intentar tras agotar los 5 reintentos.
- No existe una segunda instancia Hermes/OpenClaw en el VPS usando el token.
- Conclusión: el conflicto original ya expiró; hace falta un restart limpio del
  gateway para recuperar el polling.

## Acción tomada

Restart programado fuera del cgroup del gateway para no cortar la sesión de cron
que reportaba:

```
systemd-run --user --on-active=150s --unit=hermes-gw-recovery --collect \
  /home/hermes/.local/bin/hermes gateway restart
```

Ejecutado: 2026-09-28 04:08:41 ART.

Verificación pendiente: `hermes gateway status` debe mostrar telegram ✓ y el
health check de las 07:00 debe dar Telegram ✅.

## Arreglo adicional al health check

`get_recent_errors()` contaba **todas** las líneas del log (WARNING incluidas) como
"errores", inflando el aviso a "139 unfixable errors" cuando en 24 h había
**7 líneas ERROR/CRITICAL** reales. Se agregó el parámetro `errors_only=True`
(usado por `check_errors_log()`), sin tocar el detector de loops de reconexión.

## Recurrencia 2026-10-05 04:03 ART (misma causa raíz, no resuelta)

Diagnóstico nuevo (ver `Handoffs/vps-to-local/HO-2026-10-04-001/`): el conflicto
**no** es una sesión stale del propio gateway, sino un **segundo poller externo**:
el perfil `algolab` de la PC de Juan (`truzt`, Tailscale `100.105.0.23`) usa el
mismo `[credencial: TELEGRAM_BOT_TOKEN]` (bot `8644817415`). Es una carrera: gana
el gateway que arranca primero.

Secuencia de hoy: health check 04:01 detectó telegram `fatal`, reinició (04:02);
el VPS perdió la carrera → 5 reintentos agotados → `fatal` a las 04:07:40. Un
restart limpio a las 04:10 reconectó (`telegram connected`, PID 3144077) y quedó
estable a las 04:11.

**Fix pendiente de Juan** (fuera de zona de brain-vps/brain-local): comentar
`TELEGRAM_BOT_TOKEN` en `AppData\Local\hermes\profiles\algolab\.env` de la PC, o
darle un bot propio. Mientras siga ahí, el cron de las 04:00 va a revertir a
`fatal` cada vez que los dos gateways arranquen y el VPS pierda la carrera.

## Pendiente (no resuelto por este cron)

`hermes-dashboard` (PM2 id 3) está en crash loop: **90.692 restarts** desde el
05/08, con `node-deps.mjs … died with SIGABRT` al construir la web UI. El
dashboard igual está servido por el proceso standalone PID 1467264
(`hermes dashboard --host 100.124.132.48 --port 9119`, escuchando OK).
Decisión sugerida: `pm2 delete hermes-dashboard` (redundante) o reconstruir
node_modules. Requiere OK de Juan.
