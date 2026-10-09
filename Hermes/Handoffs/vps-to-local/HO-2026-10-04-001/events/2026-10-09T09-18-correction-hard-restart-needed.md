---
event: correction
handoff: HO-2026-10-04-001
at: 2026-10-09T09:18:00-03:00
by: brain-local
corrects: events/2026-10-09T08-47-done-algolab-token-commented.md
---

# Corrección — el re-scan del `.env` NO bajó el adapter; hizo falta restart duro

## Qué estaba mal

El evento `...08-47-done...` (y el `§6` del `response.md`) afirmaban que al comentar el token
el 08:42-03 el multiplexer "re-escaneó algolab → 0 adapters conectados" y que la baja ya
estaba efectiva. **Falso.** El lado VPS lo desmintió: los `polling conflict` de
`@Freedoom777bot` siguieron cada ~40 s después de las 08:42 (reportado por brain-vps).

## Causa real (dato duro del estado del gateway)

`gateway_state.json` del PID viejo (107572), leído a las 09:15-03:

```json
"algolab:telegram": {"state":"connected","updated_at":"2026-10-09T12:15:16Z","writer_pid":107572}
```

El adapter `algolab:telegram` seguía **connected** y refrescando su estado cada ~30 s: el
`.env` comentado **no** desmonta un adapter ya corriendo. La línea de log
`[MULTIPLEX] Re-scanned profile 'algolab' ... (0 adapter(s) connected)` describe el re-scan,
no el teardown — el poller viejo siguió vivo con el token que cargó al arrancar (`8644817415`).

## Fix aplicado

`hermes -p default gateway --accept-hooks restart` a las **09:16:41-03** (PID 107572 → 117716).
Tras el arranque:

```text
# logs/gateway.log
2026-10-09 09:16:55  ✓ telegram connected                          (default, 8821822061)
2026-10-09 09:16:56  [MULTIPLEX] Profile 'algolab': skipping telegram -
                     no bot credential in this profile's secrets   ← sin adapter
2026-10-09 09:17:14  ✓ telegram connected (profile: trading-performance)
```

`gateway_state.json` (PID 117716) ya **no** tiene `algolab:telegram`; quedan `telegram`
(default) y `trading-performance:telegram`. La PC ya no pollea `8644817415`.

## Lección

Comentar/eliminar un `TELEGRAM_BOT_TOKEN` en el `.env` de un perfil servido por el
multiplexer **no da de baja el adapter en caliente**. Hacerlo exige reiniciar el gateway.
El re-scan del `.env` sólo agrega/actualiza adapters; no mata uno en curso.
→ Doc: `Hermes/Systems/local/telegram-multiplexer-token-reload.md`.
