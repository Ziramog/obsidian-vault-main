---
event: done
handoff: HO-2026-10-09-003
at: 2026-10-09T09:10:00-03:00
by: brain-vps
status: executed-in-vps-zone
---

# Ejecución — los scripts son zona VPS; brain-vps los arregló y verificó

brain-local confirmó que `Hermes/Systems/vps/**` es zona de escritura de brain-vps
y no la toca. La ejecución se hizo desde el VPS.

## 1. Blocker del CLI — RESUELTO

`agenda.py:1065/1067`: `"detail"` registrado en la lista de subparsers con
`--date` **y** otra vez en `:1104` con `task_ref` → `ValueError: conflicting subparser: detail`.

Fix: se sacó `"detail"` de la lista de `:1065` y del set de `:1067`; queda el
parser bueno de `:1104` (que es el que consume `main()` en `:1140`, con `task_ref`).

Verificación:
- `python3 agenda.py --help` → **exit 0**; subcomandos listados:
  `today,tomorrow,list,ensure,focus,reminders,review,week,pending,cleanup,add,done,snooze,cancel,move,priority,detail,edit`.
- Vault temporal: `add` → `OK add: ag-...`, `list` muestra la tarea, `detail <ref>` devuelve el detalle.

## 2. Frente S4 — gate de consultas/vagos en el catch-all — RESUELTO

`agenda-telegram-bot.py`: se agregaron `_is_help_query()` y `_is_vague_fragment()`
y se insertaron **antes** del catch-all (`return cmd_add(vault, raw, ...)`).

- Consultas/ayuda (`agenda`, `listar comandos`, `listar comanndos`, `semana que viene`,
  y variantes con typo) → responden ayuda/panorama, **0 altas**.
- Fragmentos vagos (≤4 palabras, sin fecha y sin verbo de acción) → piden aclaración,
  **0 altas**.
- Altas claras siguen funcionando.

## 3. Ítem 5 — timeouts normales del long-poll — RESUELTO

`get_updates()` ahora usa `socket timeout = poll_timeout + 15` y **atrapa
`TimeoutError`/`URLError(timeout)` devolviendo `[]`** (sin novedades), en vez de
burbujear al `poll_loop` y ensuciar el log con falsos `LOOP ERROR TimeoutError`.

## 4. Tabla de aceptación del request — probada contra `handle_text()` (vault temporal)

| Entrada | altas | resultado |
|---|---|---|
| `agenda` | 0 | ayuda |
| `listar comandos` | 0 | ayuda |
| `listar comanndos` | 0 | ayuda (typo tolerado) |
| `semana que viene` | 0 | ayuda/panorama |
| `qué tengo hoy` | 0 | consulta |
| `/model` | 0 | comando inválido |
| `el tema ese` | 0 | pide aclaración |
| `mañana 9 llamar a GAMA` | 1 | alta |
| `urgente para mañana: llamar a Palmero` | 1 | alta |

Vault real **no** fue tocado por las pruebas (vaults temporales + checksum); mtime de
`Agenda/2026-10-09.md` y `bandeja.md` sin cambios.

## 5. Incidente lateral durante el restart (resuelto)

Al reiniciar PM2 el proceso quedó `errored`: el intérprete de PM2 no tenía
`ruamel.yaml` y `tools.transcription_tools` (import a nivel módulo) moría en
`hermes_yaml`. Se instaló `ruamel.yaml==0.18.16` en el python del runtime y se
re-verificó la cadena de import. Bot **online** desde `2026-10-09T09:08:25`, log
`Agenda bot loop started poll_timeout=25s`, sin `LOOP ERROR` nuevos.

## Pendiente (no es de este handoff)

El conflicto de `getUpdates` de `@Freedoom777bot` sigue activo (ver HO-2026-10-04-001):
con el lado PC supuestamente limpio a las 08:42, los `polling conflict` continuaron
hasta las 09:08 → la baja del token en `algolab` **no bajó el segundo poller**.
