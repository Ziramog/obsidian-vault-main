---
event: closed
handoff: HO-2026-10-04-001
at: 2026-10-09T23:58:00-03:00
by: brain-vps
status: done
---

# Cierre — `status: ready` → `done` (verificación del lado VPS completada)

La escalada del token duplicado quedó resuelta el 2026-10-09 y el criterio 3 (que sólo el VPS
puede ver) se confirmó recién ahora, al cierre del día. Con eso el handoff pasa a `done`.

## Qué se cumplió

| Criterio | Estado |
|---|---|
| 1 — ¿Existe otro poller? | ✅ SÍ: perfil `algolab` de la PC (`gateway_state.json` → `algolab:telegram connected`, `writer_pid` del gateway local) |
| 2 — Desactivarlo | ✅ token comentado en `profiles/algolab/.env` (08:42) **+ restart duro del gateway local** (09:16:41, PID 107572 → 117716) — el re-scan del `.env` no bajaba el adapter vivo |
| 3 — ≥90 s sin conflictos en el gateway VPS | ✅ **verificado desde el VPS:** último `polling conflict` en `~/.hermes/logs/gateway.log` → **09:16:11**; después, **cero** (~14 h al cierre) |
| 4 — Mensaje real a `@Freedoom777bot` con respuesta | ✅ los mensajes de Juan de 16:33–17:21 ART fueron entregados y respondidos por brain-vps por ese canal |
| 5 — Cierre sin tokens | ✅ este evento; nunca se imprimió el valor del token |

## Evidencia

- `events/2026-10-09T08-12-director-approval.md` — autorización de Juan (arquitectura de dos bots).
- `events/2026-10-09T08-47-done-algolab-token-commented.md` (cierre apresurado, corregido).
- `events/2026-10-09T08-54-token-removed-restart-pending.md` — el re-scan no baja adapters vivos.
- `events/2026-10-09T09-18-correction-hard-restart-needed.md` — fix real + verificación en la PC.
- `Hermes/Systems/local/telegram-multiplexer-token-reload.md` — regla dura del multiplexer.
- VPS: `grep -n "polling conflict" ~/.hermes/logs/gateway.log | tail -1` → `2026-10-09 09:16:11`.

## Residuos (no bloquean el cierre, quedan como frentes aparte)

- El gateway local de la PC escucha el api_server en `0.0.0.0:8642` (no loopback) con terminal
  backend `local` → firewallear a LAN/tailnet confiable o pasar a backend sandboxeado.
- Los crons agent-mode del VPS heredan el modelo default nuevo (`deepseek-v4-flash-vision-exp`).
