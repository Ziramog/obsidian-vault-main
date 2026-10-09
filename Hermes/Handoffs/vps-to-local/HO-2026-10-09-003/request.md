---
id: HO-2026-10-09-003
status: ready
from: brain-vps
to: brain-local
project: hermes-system
priority: high
depends-on: []
created-at: 2026-10-09T08:12:59-03:00
acknowledge-by: next-local-session
due-at: 2026-10-12T18:00:00-03:00
escalate-after: 24h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — convertir `@Agenda_Hbot` en una agenda estricta

## Decisión de Juan

Mantener dos bots separados:

- `@Freedoom777bot` = conversación general con brain-vps.
- `@Agenda_Hbot` = captura, consulta y cierre de agenda; no conversación general.

Este handoff implementa el frente existente **S4** de `Hermes/Agenda/Frentes.md`; no crea un frente nuevo.

## Problema verificado

El bot de agenda cayó al fallback de alta y creó tareas basura con textos que eran consultas o fragmentos vagos:

- `agenda` → creó `ag-20261009-003`.
- `listar comanndos` → creó `ag-20261009-004`.
- `semana que viene` → creó `ag-20261009-005`.

Además, el loop registra `TimeoutError` repetidos porque el timeout HTTP es apenas mayor que el long-poll; distinguir timeout normal de una falla real para no ensuciar el log ni introducir pausas innecesarias.

## Objetivo verificable

Hacer que `@Agenda_Hbot` sea estricto y predecible:

1. Consultas y ayuda nunca crean tareas.
2. Fragmentos vagos nunca crean tareas: el bot pide una aclaración corta y no escribe archivos.
3. Altas naturales claras siguen funcionando.
4. El texto/audio recibido no se pierde: si no puede clasificarse, debe quedar en la bandeja cruda o pedir confirmación sin convertirlo en tarea activa, según el diseño vigente de `Agenda/bandeja.md`.
5. Timeouts normales del long-poll no se reportan como errores operativos.

## Rutas

- `Hermes/Systems/vps/scripts/agenda-telegram-bot.py`
- `Hermes/Systems/vps/scripts/agenda.py`
- `Hermes/Systems/vps/agenda-bot-manual.md`
- `Hermes/Agenda/bandeja.md`

## Casos de aceptación mínimos

En un vault temporal:

| Entrada | Resultado esperado |
|---|---|
| `agenda` | mostrar ayuda/panorama o pedir precisión; **0 altas** |
| `listar comandos` | ayuda; **0 altas** |
| `listar comanndos` | ayuda tolerando typo; **0 altas** |
| `semana que viene` | pedir qué tarea; **0 altas** |
| `qué tengo hoy` | consulta; **0 altas** |
| `/model` | comando inválido; **0 altas** |
| `mañana 9 llamar a GAMA` | exactamente 1 alta |
| `urgente para mañana: llamar a Palmero` | exactamente 1 alta roja para mañana |
| audio claro con fecha + acción | exactamente 1 alta + confirmación textual |
| audio incompleto | no alta activa; conservar captura o pedir aclaración |

## Verificación obligatoria

1. Ejecutar los casos query-only en un vault temporal.
2. Ejecutarlos contra el vault real con checksum antes/después: ninguna consulta puede modificar Agenda.
3. Reiniciar el proceso PM2 `agenda-telegram-bot` de forma controlada.
4. Probar end-to-end desde Telegram con `/todo`, `listar comandos`, `semana que viene` y una alta clara.
5. Leer el archivo exacto de agenda para verificar la alta y confirmar que no aparecieron tareas basura.
6. Adjuntar evidencia en `events/` o `response.md` sin tokens ni secrets.

## Restricciones

- No cambiar la fuente de verdad Markdown.
- No crear una base de datos paralela.
- No mezclar el token del bot Agenda con el del bot general.
- No editar este `request.md`; cambios de alcance van en `events/`.
