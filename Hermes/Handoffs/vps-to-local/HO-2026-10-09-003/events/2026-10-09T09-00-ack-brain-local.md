---
event: ack
handoff: HO-2026-10-09-003
at: 2026-10-09T09:00:00-03:00
by: brain-local
status: in-progress — bloqueante del parser reproducido; implementación derivada a web-builder
---

# Ack + plan — HO-2026-10-09-003 (`@Agenda_Hbot` estricto)

Recibido. `depends-on: []` → sin bloqueo de dependencias. Vence 2026-10-12 18:00 -03;
`escalate-after: 24h` → antes del 2026-10-10 09:00 si no hay avance.

`Hermes/Briefings/current.md` v2 tiene `reality-check-required-by: 2026-10-01` vencido: este
handoff es trabajo técnico sin impacto comercial directo, así que puede ejecutarse; no toca
prioridades del briefing.

## Bloqueante reproducido (event `2026-10-09T08-12-agenda-cli-parser-blocker.md`)

```text
$ python3 Hermes/Systems/vps/scripts/agenda.py --help
Traceback (most recent call last):
  File ".../scripts/agenda.py", line 1117, in main
    args = build_parser().parse_args(argv)
  File ".../scripts/agenda.py", line 1104, in build_parser
    detail = sub.add_parser("detail")
  File ".../Lib/argparse.py", line 1258, in add_parser
    raise ValueError(f'conflicting subparser: {name}')
ValueError: conflicting subparser: detail
```

Causa exacta: `detail` se registra **dos veces** —

- `agenda.py:1065` → loop sobre `["today","tomorrow","list","ensure","focus","reminders","review","week","pending","detail","cleanup"]`
  (con el filtro de `agenda.py:1067`), y
- `agenda.py:1104` → `detail = sub.add_parser("detail")` explícito.

El handler de ejecución (`args.cmd == "detail"`) está en `agenda.py:1140`. La interfaz pública
no cambia: hay que dejar **un solo** registro de `detail`.

## Alcance acordado con el request

1. `agenda.py`: eliminar el subparser duplicado sin cambiar la CLI; `--help` con exit 0.
2. `agenda-telegram-bot.py`: consultas/ayuda (`agenda`, `listar comandos`, `listar comanndos`
   con typo, `semana que viene`, `qué tengo hoy`, `/model`) → **0 altas**; fragmentos vagos →
   pedir aclaración, sin escribir archivos; altas naturales claras → exactamente 1 alta.
3. Timeouts normales del long-poll no se reportan como error operativo.
4. Captura cruda preservada según `Hermes/Agenda/bandeja.md` (sin BD paralela).
5. Verificación: vault temporal + checksum del vault real antes/después; restart controlado
   del proceso PM2 `agenda-telegram-bot`; E2E por Telegram; evidencia en `events/` sin tokens.

## Derivación

Implementación de código → **web-builder** (dueño de la edición de scripts). brain-local
coordina y consolida; la verificación independiente queda para **web-auditor** (solo lectura).
Ninguna edición del `request.md` original; cambios de alcance van acá.

## Restricciones respetadas

- No se cambia la fuente de verdad Markdown ni se crea base paralela.
- No se mezcla el token del bot Agenda con el del bot general.
- Sin tokens ni secrets en este archivo. Sin Git.
