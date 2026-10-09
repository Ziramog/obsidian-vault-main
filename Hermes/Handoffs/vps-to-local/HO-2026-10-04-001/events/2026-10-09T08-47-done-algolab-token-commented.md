---
event: done
handoff: HO-2026-10-04-001
at: 2026-10-09T08:47:00-03:00
by: brain-local
result: criterio 2 aplicado en la PC — el token del VPS ya no se pollea desde acá
request_status_owed: request.md sigue en `status: ready` (es del autor, brain-vps)
---

# Done — HO-2026-10-04-001 (token duplicado del perfil `algolab`)

Juan aprobó el 2026-10-09 08:12-03 (`events/2026-10-09T08-12-director-approval.md`).
Acción autorizada: quitar/comentar en el perfil `algolab` la credencial
`[credencial: TELEGRAM_BOT_TOKEN]` de `@Freedoom777bot` (bot id `8644817415`), sin tocar
otros bots.

## Estado verificado en la PC (2026-10-09 ~08:45 -03)

```text
# AppData/Local/hermes/profiles/algolab/.env   (mtime 2026-10-09 08:42:13 -03)
línea 339  ->  # TELEGRAM_BOT_TOKEN=8644817415:[REDACTADO]      (comentada)
activas   ^TELEGRAM_BOT_TOKEN= : 0
comentadas                    : 1
bot id de la línea            : 8644817415  == @Freedoom777bot (el del gateway VPS)
```

La baja **ya está aplicada** (08:42:13 -03). Ningún `config.yaml` lleva el token:
`grep -rn bot_token profiles/*/config.yaml config.yaml` → 0 hits.

## El gateway local ya soltó el adapter (no hizo falta `restart`)

```text
# logs/gateway.log  (timestamps en -04 → 1h por delante del ls en -03)
2026-10-09 07:42:26 INFO gateway.run_profile_reconcile: [MULTIPLEX] Re-scanned profile
'algolab' after config/.env change (0 adapter(s) connected)
```

El multiplexer del perfil `default` (PID **107572**, escucha `0.0.0.0:8642`) detectó el cambio
de `.env` y re-escaneó `algolab` → **0 adapters conectados**: ya no monta Telegram. `hermes
gateway list` confirma `algolab — served by the default multiplexer` sin adapter. Es el
"recargar" que pide la aprobación; por eso no se forzó un `hermes gateway restart`
(la recarga ya ocurrió; un restart sólo agrega downtime).

## Otros tokens de la PC — intactos, sin conflicto

```text
.env (default)                     -> 8821822061
profiles/trading-performance/.env  -> 8792684627
profiles/algolab/.env              -> comentado (era 8644817415)   <- único con el bot del VPS
brain-local / web-auditor / web-builder -> línea comentada
```

Ninguna ruta activa de la PC pollea `8644817415`. No se tocó ningún otro bot.

## Criterios de aceptación

1. SÍ/NO otro poller → resuelto el 2026-10-04 (perfil `algolab`, esta PC).
2. Desactivarlo → **HECHO** (línea comentada; adapter desmontado por el multiplexer).
3. Verificación ≥90 s sin conflictos en el gateway VPS → **lado VPS**, no accesible desde la
   PC. Pendiente de confirmar por brain-vps.
4. Mensaje real a `@Freedoom777bot` con respuesta de brain-vps → **paso humano/VPS**: enviar
   desde Telegram y ver la respuesta.
5. Cierre sin tokens → este evento; el token nunca se imprimió.

## Flip pendiente

`request.md` sigue `status: ready` — es del autor (brain-vps). Este `events/` + el `§6` de
`response.md` son el cierre del lado local.

## Nota de seguridad (residual, para Juan)

El gateway local escucha en `0.0.0.0:8642` (no sólo loopback) → alcanzable desde LAN/tailnet.
Vale revisarlo aparte; no es parte de este handoff.
