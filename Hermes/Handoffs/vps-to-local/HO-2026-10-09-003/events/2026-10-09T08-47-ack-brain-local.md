---
event: ack
handoff: HO-2026-10-09-003
at: 2026-10-09T08:47:00-03:00
by: brain-local
action: tomado; reproducido el blocker; bloqueo de zona para las rutas VPS
---

# Ack — HO-2026-10-09-003 (bot `@Agenda_Hbot` estricto)

Handoff tomado en la sesión local del 2026-10-09. Vault en `HEAD 2041ccbe` == `origin/main`
(`rev-list --left-right --count origin/main...HEAD` = `0 0`), sin cambios locales → lectura fresca.

## Blocker del CLI — reproducido

```text
$ python3 Hermes/Systems/vps/scripts/agenda.py --help
Traceback (most recent call last):
  File ".../agenda.py", line 1117, in main
    args = build_parser().parse_args(argv)
  File ".../agenda.py", line 1104, in build_parser
    detail = sub.add_parser("detail")
  File ".../argparse.py", line 1258, in add_parser
    raise ValueError(f'conflicting subparser: {name}')
ValueError: conflicting subparser: detail
```

Causa exacta: `build_parser()` registra `"detail"` **dos veces**:

- `agenda.py:1065` → `for name in [... "detail" ...]: sub.add_parser(name)` (sólo `--date`).
- `agenda.py:1104` → `detail = sub.add_parser("detail")` (con `task_ref` + `--date`).

Fix: quitar `"detail"` de la lista de la línea 1065 y del set de la 1067; dejar la definición
rica de la 1104. Verificado que ningún otro subparser está duplicado
(`add_parser("...")` → 1 cada uno: add/done/snooze/cancel/move/priority/detail/edit).

## Causa de las altas basura (frente S4)

`agenda-telegram-bot.py:691` → `return cmd_add(vault, raw, source=source)` es el **catch-all**:
todo lo no reconocido se da de alta. Por eso `"agenda"`, `"listar comanndos"` y
`"semana que viene"` (sin espacio final / sin match) caen a `cmd_add` y crean tareas.
(`/model` ya está cubierto por `:684` → "Comando no reconocido. No guardé nada.")

## Bloqueo de zona

Las rutas del handoff (`Hermes/Systems/vps/scripts/{agenda.py,agenda-telegram-bot.py}`,
`agenda-bot-manual.md`) son **zona VPS**, fuera de la zona de escritura de brain-local
(SOUL + skill `hermes-local-operations`). No las edito sin OK explícito. El cambio de código
corresponde al dueño del archivo (brain-vps); brain-local aporta el diagnóstico, el patch
exacto y coordina la verificación. Escalado a Juan en el room 2026-10-09 08:47-03.
