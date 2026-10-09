---
event: evidencia-aceptacion
handoff: HO-2026-10-09-003
at: 2026-10-09T09:06:49-03:00
by: web-builder
status: implementación presente en HEAD; matriz literal 10/10; generalización con huecos; falta restart PM2 + E2E Telegram (VPS)
---

# Evidencia — verificación de `@Agenda_Hbot` estricto (matriz del request)

Sin tokens ni secrets. Vault temporal; el vault real sólo se usó en lectura.
Estado verificado en `16164b3d` (auto-sync [vps]) — **no** toqué el código: los
cambios S4 (guards de consulta/vago + timeout del long-poll) ya estaban en HEAD,
aplicados desde el VPS a las 09:00–09:02, y el fix del parser en `4ee470bc`.

## Montaje

- Cargué `agenda-telegram-bot.py` en Windows con stubs POSIX (`fcntl`) y
  `tools.transcription_tools`, rebasando `BASE_DIR`/`AGENDA_PY` a un vault temporal.
- Ninguna escritura en el vault real durante las pruebas.

## Matriz de aceptación (10 casos) — 10/10

| Entrada | Altas | Resultado |
|---|---|---|
| `agenda` | 0 | ayuda / "No guardé nada por esta consulta" |
| `listar comandos` | 0 | idem |
| `listar comanndos` | 0 | idem (typo tolerado) |
| `semana que viene` | 0 | idem |
| `qué tengo hoy` | 0 | lista de hoy (`Agenda 2026-10-09: sin tareas abiertas`) |
| `/model` | 0 | "Comando no reconocido. No guardé nada." |
| `mañana 9 llamar a GAMA` | 1 | `ag-20261010-001 — llamar a GAMA` |
| `urgente para mañana: llamar a Palmero` | 1 | `ag-20261010-002` en `## 🔴 Hoy sí o sí` de 2026-10-10 |
| transcript claro (proxy `mañana 11 pasar a ver ANGO`) | 1 | `ag-20261010-003` |
| transcript incompleto (proxy `ehh esto no sé`) | 0 | "No me quedó claro qué tarea agendar… No guardé nada." |

Nota: al repetir exactamente el mismo texto, `agenda.py` responde
`SKIP duplicate` (dedupe correcto, no es fallo).

## Criterio 2 — vault real intacto

6 casos query-only contra el vault real, checksum del árbol `Hermes/Agenda` antes/después:

- before `aa788ecabb60eb1a2d329455d6c03330179c9db264c698a0433166bd13ecc997`
- after  `aa788ecabb60eb1a2d329455d6c03330179c9db264c698a0433166bd13ecc997`
- idénticos, 0 altas nuevas.

## Criterio 5 — timeout del long-poll

`get_updates` con `telegram_api` forzado a fallar: `TimeoutError → []`,
`URLError(TimeoutError) → []`, `URLError(connection refused) → raise`.
No hay `LOOP ERROR` por corte normal. ✔

## CLI (`4ee470bc`)

`agenda.py --help` → exit 0; `agenda.py detail --help` → exit 0 con `task_ref`.
Observación menor: `add --priority rojo` responde `Prioridad inválida: rojo. Usá
red/yellow/green` pero igual deja creado el `.md` del día (exit 1) — no bloquea 003.

## Hallazgo abierto — la matriz literal pasa, la generalización no

Batería de 16 entradas fuera de la lista: **10 crean tarea**. Causas:

1. `_is_vague_fragment` corta por `len(low.split()) > 4`: cualquier fragmento de
   5+ palabras sin fecha ni verbo se guarda como tarea —
   `ehhh bueno no me acuerdo` → `ag-20261009-001`.
2. Cualquier verbo de `_ACTION_VERB_RE` desactiva el guard:
   `ver` → 1 alta; `revisar eso` → 1 alta.
3. Las consultas se resuelven por sets de coincidencia exacta, así que una
   variante no listada cae al alta: `qué tenés mañana`, `mostrame la agenda de
   mañana`, `tengo algo el viernes?`, `qué hay para el lunes` → 1 alta cada una.

Contra el objetivo 1–2 del request ("consultas **nunca** crean tareas",
"fragmentos vagos **nunca** crean tareas") los guards están ajustados a los
strings del ejemplo, no a la clase. Invertir el default (alta sólo con token de
fecha o comando explícito `/agendar`) cierra los dos últimos grupos; el guard de
vagos debe dejar de tratar "tiene verbo" como suficiente.

## Pendiente (no ejecutable desde este host)

- Criterio 3: restart controlado del proceso PM2 `agenda-telegram-bot` en el VPS
  (los guards S4 están en el repo pero el proceso vivo puede no haberlos cargado).
- Criterio 4: E2E desde Telegram (`/todo`, `listar comandos`, `semana que viene`,
  una alta clara) y lectura del `.md` resultante.
- Decisión de diseño abierta: hoy el fragmento vago se responde sin persistir; el
  request acepta "conservar captura **o** pedir aclaración", pero `bandeja.md`
  dice "nunca se descarta en silencio". Si se quiere persistencia real, el alta
  cruda debería appendear a `Agenda/bandeja.md`.

## Riesgo de concurrencia

El mismo archivo fue editado por el lado VPS a las 09:00/09:02 sobre `16164b3d`.
Un patch desde local puede chocar con el próximo `auto-sync [vps]`; conviene un
solo editor a la vez.
