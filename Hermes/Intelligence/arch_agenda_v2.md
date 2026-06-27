---
title: Agenda V2 — Arquitectura operativa
owner: brain-vps
status: proposed
version: 0.1
created-at: 2026-06-27T09:05:38-03:00
source: chat-con-juan
applies-to:
  - brain-vps
  - brain-local
  - pc-ops
  - telegram-gateway
related:
  - Hermes/Config/ARCHITECTURE.md
  - Hermes/Agenda/
  - Hermes/Sessions/
  - Hermes/Daily/
---

# Agenda V2 — Arquitectura operativa

## 0. Propósito

Convertir `Hermes/Agenda/` en un elemento de utilidad diaria para Juan: usable desde Telegram en el móvil, legible desde cualquier terminal de PC/VPS, sincronizado por Obsidian/Git, y capaz de disparar recordatorios sin depender de edición manual ni de memoria humana.

La Agenda V2 no reemplaza `MEMORY.md`, `Briefings/current.md`, handoffs ni pipeline comercial. Es el cockpit diario: qué hay que hacer, cuándo avisar, qué se cerró y qué debe arrastrarse.

## 1. Decisión base que se conserva

Se mantiene la decisión cerrada de Architecture V5:

```txt
Hermes/Agenda/YYYY-MM-DD.md
```

Un archivo por día. Sin base de datos en Fase 1. Markdown como fuente de verdad para que Obsidian, VPS, PC local y Telegram puedan operar sobre el mismo objeto.

## 2. Problema actual

La agenda actual funciona como lista, pero todavía no como sistema operativo diario.

| Área | Estado actual | Problema |
|---|---|---|
| Uso móvil | Telegram/chat manual | Falta protocolo de comandos y confirmaciones cortas |
| Recordatorios | Crons sueltos creados caso por caso | No hay sintaxis estándar parseable dentro de la agenda |
| Multi-terminal | PC/VPS pueden leer archivos | Falta índice/CLI común para consultar rápido |
| Sesiones | Separadas o narrativas | No hay vínculo limpio entre tarea, sesión y cierre |
| Audio | Hermes puede recibir mensajes de Telegram | Falta contrato para carga por audio y respuesta solo texto |

## 3. Principios de diseño

1. **Móvil primero:** Juan debe poder cargar tareas desde Telegram en texto o audio.
2. **Texto como respuesta:** aunque la entrada sea audio, la salida por Telegram debe ser texto. Evita loops de voz, permite copiar, revisar y auditar.
3. **Markdown como source of truth:** todo lo operativo queda en `Hermes/Agenda/YYYY-MM-DD.md`.
4. **Sin base de datos en Fase 1:** si hace falta estado, se expresa en YAML/Markdown parseable.
5. **Recordatorios declarativos:** una tarea declara `reminder`, `channel`, `status`; un scanner se encarga de ejecutar.
6. **Cualquier host puede leer:** PC local, VPS, scripts y agentes deben poder informar la agenda sin depender de contexto interno del LLM.
7. **Agenda ≠ MEMORY ≠ pipeline:** no contaminar estado estratégico con tareas diarias.
8. **Una acción prioritaria:** cuando haya muchas tareas, el sistema debe poder responder con un foco único.

## 4. Formato Agenda V2

### 4.1 Frontmatter obligatorio

```yaml
---
type: agenda
date: 2026-06-28
owner: brain-vps
status: active
source:
  - telegram
  - cli
  - manual
reminders: true
reviewed-at:
summary-status: pending
linked-session: Hermes/Sessions/2026-06-28.md
---
```

### 4.2 Cuerpo estándar

```md
# Agenda 2026-06-28 — Domingo

## 🎯 Foco del día
> Una frase. Ej: Cancelar ChatGPT y revisar leads Wolfim.

## 🔴 Hoy sí o sí
- [ ] **Cancelar prueba ChatGPT**
  - id: ag-20260628-001
  - reminder: 2026-06-28 09:00
  - channel: telegram
  - status: pending
  - source: telegram-text

## 🟡 Importante
- [ ] **Seguir GAMA**
  - id: ag-20260628-002
  - status: pending

## 🟢 Backlog
- [ ] **Revisar idea nueva de agenda**
  - id: ag-20260628-003
  - status: pending

## 🔔 Recordatorios
| Hora | Tarea | Canal | Estado | ID |
|---|---|---|---|---|
| 09:00 | Cancelar prueba ChatGPT | Telegram | scheduled | ag-20260628-001 |

## 🧠 Sesión del día
- [[Hermes/Sessions/2026-06-28]]

## ✅ Cerrado hoy
- [x] **Tarea hecha** — resultado concreto

## ➡️ Arrastre sugerido para mañana
- [ ] Tarea pendiente que requiere confirmación de Juan antes de arrastrar
```

## 5. Recordatorios: scanner declarativo

### 5.1 Script propuesto

```txt
Hermes/Systems/vps/scripts/agenda-reminder-scan.py
```

Corre cada 5 minutos por cron del sistema o Hermes cron no-agent.

### 5.2 Responsabilidades

1. Leer `Hermes/Agenda/YYYY-MM-DD.md` según fecha ART.
2. Detectar tareas con bloque parseable:
   - `reminder: YYYY-MM-DD HH:MM`
   - `channel: telegram`
   - `status: pending`
3. Si `now >= reminder`:
   - enviar Telegram a Juan
   - cambiar `status: pending` → `status: sent`
   - actualizar tabla `🔔 Recordatorios`
   - agregar evento breve en `🧠 Sesión del día` o `✅ Cerrado hoy` si aplica
4. No inventar tareas. Si el formato está roto, reportar error técnico y no modificar destructivamente.

### 5.3 Por qué scanner y no un cron por tarea

| Opción | Ventaja | Problema |
|---|---|---|
| Cron por tarea | Simple para casos aislados | Se fragmenta, difícil auditar, no vive en Obsidian |
| Scanner agenda | Unifica lógica, auditable, agenda declara intención | Requiere script robusto |

Decisión recomendada: scanner.

## 6. Telegram como interfaz principal

### 6.1 Entrada por texto

Ejemplos esperados:

```txt
agendame mañana 9 cancelar chatgpt
agenda hoy
agenda mañana
marcá hecho cancelar chatgpt
posponé cancelar chatgpt 2h
qué tengo hoy
cuál es el foco
```

### 6.2 Entrada por audio

Objetivo: Juan puede mandar audio a Telegram con tareas naturales.

Flujo deseado:

1. Telegram recibe audio.
2. Hermes/Gateway transcribe usando STT configurado.
3. brain-vps interpreta fechas/prioridades con `agenda-workflow`.
4. Escribe/actualiza `Hermes/Agenda/YYYY-MM-DD.md`.
5. Responde **solo texto**, aunque la entrada haya sido audio.

Respuesta ejemplo:

```txt
Listo. Agregué para mañana:
🔴 09:00 Cancelar ChatGPT — con recordatorio
🟡 Seguir GAMA
🟢 Revisar idea de agenda
Archivo: Hermes/Agenda/2026-06-28.md
```

### 6.3 Regla de salida

**Telegram puede recibir audio, pero devuelve texto por defecto.**

Motivo:
- Texto es auditable.
- Evita ruido en móvil.
- Permite abrir Obsidian y comparar.
- Reduce costo y fallos de TTS.

TTS solo se habilita si Juan lo pide explícitamente.

### 6.4 Bot dedicado `Agenda`

Decisión agregada por Juan el 2026-06-27:

> Crear un bot especial de Telegram llamado **Agenda** para separar la carga/consulta diaria de tareas del canal general de Hermes.

Objetivo:
- Hacer más práctico el uso móvil.
- Evitar mezclar agenda con conversaciones largas de estrategia, ventas o implementación.
- Permitir que Juan mande texto/audio directamente al bot Agenda y reciba confirmación textual corta.
- Mantener el bot principal de Hermes para conversación general y orquestación.

Comportamiento esperado del bot Agenda:

| Entrada al bot Agenda | Acción |
|---|---|
| texto libre: `mañana 9 cancelar ChatGPT` | parsear fecha/hora/tarea, escribir en `Hermes/Agenda/YYYY-MM-DD.md` |
| audio Telegram | transcribir, interpretar tareas, escribir agenda, responder solo texto |
| `/hoy` o `hoy` | listar agenda de hoy |
| `/mañana` o `mañana` | listar agenda de mañana |
| `/foco` o `foco` | devolver una sola tarea prioritaria |
| `/hecho ag-YYYYMMDD-NNN` | marcar tarea como `done` |
| `/posponer ag-YYYYMMDD-NNN 2h` | cambiar reminder y estado `snoozed` |

Reglas técnicas:
- El bot Agenda debe usar el mismo source of truth: `Hermes/Agenda/YYYY-MM-DD.md`.
- No crear una base de datos separada para el bot.
- No duplicar lógica: reutilizar `Hermes/Systems/vps/scripts/agenda.py` y `agenda-reminder-scan.py`.
- Respuesta por defecto: texto corto, no audio.
- Credenciales del bot Agenda deben vivir fuera del vault, en `.env` o secret store, referenciadas como `[credencial: TELEGRAM_AGENDA_BOT_TOKEN]` si hay que documentarlas.
- Si conviven varios bots, cada bot debe tener token/chat routing separado y explícito para no romper el gateway principal.
- Parser de fechas preferido: gramática propia simple en español antes que sumar librerías externas. Más mantenible y suficiente para los casos operativos de Juan.

Gramática de fechas soportada (2026-06-27 ajuste fino):
- `hoy`
- `mañana`
- `pasado mañana`
- `en 3 días`
- `viernes`, `lun`, `mie`, `jue`, etc. → próximo día futuro
- `martes o miércoles` → toma el primer día futuro posible
- prioridad explícita al inicio: `rojo mañana 9 llamar a GAMA`, `verde cuando pueda probar idea`
- `miércoles que viene`, `viernes que viene`, `prox lunes`, `el otro miércoles` → siguiente semana
- `la semana que viene` → próximo lunes de la semana siguiente
- `fin de mes`
- `primer lunes de julio`
- `mie 26`, `mierc 26`, `viernes 8` → día de mes próximo futuro
- `26/7`, `26-7`, `2026-07-26`
- `vie 4 de julio`

Heurística importante:
- En frases como `miércoles que viene 14 pasar a ver ANGO`, el `14` se interpreta como **hora**, no como día del mes.
- En frases como `mie 26 reunión`, el `26` se interpreta como **día del mes**.
- Prioridad implícita: `urgente`, `ya`, `sin falta` → 🔴 ; `cuando pueda`, `probamos`, `sondear` → 🟢 ; fechas futuras no urgentes → 🟡.
- Carga múltiple soportada: `mañana: llamar a GAMA, ver ANGO, pasar presupuesto`.
- Carga multilinea soportada: 
  ```txt
  mañana
  - llamar a GAMA
  - ver ANGO
  - pasar presupuesto
  ```
- Frases de reminder soportadas: `recordámelo a las 10 pagar monotributo`, `pagar seguro después de las 15`, `pagar seguro a la tarde`, `mandar presupuesto antes de las 12`.
- Reprogramación natural simple soportada: `mandar mail si no responde recordámelo mañana` y `seguir propuesta si no llego el viernes pasalo al lunes`.
- Transcripción corrida soportada cuando mantiene conectores simples: `mañana llamar a GAMA y después ver ANGO y también pasar presupuesto`.
- Comandos de producto nuevos: `/pendientes`, `/editar ag-... nuevo texto`, `/cancelar`, `/mover`, `/revisar`, `/esta-semana`, `/detalle`, `/prioridad`, `/limpiar`.
- Deduplicación simple: si una tarea abierta igual entra dos veces, la segunda se salta con `SKIP duplicate`.

Fase de implementación nueva:
1. Crear bot en BotFather con nombre operativo `Agenda`.
2. Guardar token como variable de entorno fuera del vault.
3. Crear handler dedicado o routing en gateway para mensajes recibidos por ese bot.
4. Conectar handler a `agenda.py`.
5. Probar texto primero.
6. Probar audio → transcripción → respuesta texto.
7. Documentar cómo pausar/desactivar el bot sin tocar agenda ni cron.

### Implementación inicial del bot Agenda — 2026-06-27

Archivos creados:

```txt
Hermes/Systems/vps/scripts/agenda-telegram-bot.py
Hermes/Systems/vps/scripts/agenda-telegram-bot.sh
~/.hermes/scripts/agenda-telegram-bot.sh
Hermes/Systems/vps/state/agenda-bot-state.json   (se crea al primer poll real)
Hermes/Systems/vps/cache/agenda-bot-audio/       (se crea al primer audio)
```

Qué hace `agenda-telegram-bot.py`:
- Usa un bot dedicado con token `TELEGRAM_AGENDA_BOT_TOKEN`.
- Si no encuentra la variable en entorno, la busca en `~/.hermes/.env`.
- Hace polling one-shot de Telegram (`getUpdates`) para poder correr por cron cada 1 minuto.
- Guarda `offset` en `Hermes/Systems/vps/state/agenda-bot-state.json`.
- Reutiliza `agenda.py` para `/hoy`, `/mañana`, `/foco`, `/hecho`, `/posponer` y alta por texto libre.
- Descarga audio/voice, transcribe con el stack STT de Hermes y responde en texto.
- No usa DB separada.

Comandos soportados en el bot:

```txt
/start
/help
/hoy
/mañana
/foco
/hecho ag-YYYYMMDD-NNN
/posponer ag-YYYYMMDD-NNN 11:00
mañana 9 llamar a GAMA
hoy 14 enviar presupuesto
```

Cron creado:

```txt
job_id: 3d8783e0f40f
name: Agenda Telegram bot poller
schedule: every 1m
script: agenda-telegram-bot.sh
mode: no_agent
```

Diseño del cron:
- Si todavía no existe `TELEGRAM_AGENDA_BOT_TOKEN`, el wrapper sale silencioso.
- Eso permite dejar el poller activo sin romper nada mientras Juan crea el bot en BotFather.
- Apenas el token exista en `~/.hermes/.env`, el bot queda operativo sin reescribir código.

Estado real al 2026-06-27:
- Código implementado y probado en modo local/simulado.
- Cron creado y verificado (`last_status: ok`).
- Token del bot Agenda ya fue cargado fuera del vault en `~/.hermes/.env` como `[credencial: TELEGRAM_AGENDA_BOT_TOKEN]`.
- Username validado por `getMe`: `@Agenda_Hbot`.
- **Bloqueante pendiente:** el bot todavía no recibió ningún mensaje (`getUpdates` = 0), por lo que no se pudo hacer prueba end-to-end real contra Telegram. Hasta que Juan no abra el chat e inicie `/start`, Telegram no deja enviarle mensajes desde ese bot.
- Próximo paso operativo: Juan debe abrir `@Agenda_Hbot`, tocar `Start` y mandar `/hoy` o `mañana 9 llamar a GAMA`.

## 7. CLI común para PC/VPS

Comando futuro sugerido:

```bash
agenda hoy
agenda mañana
agenda add "mañana 9 cancelar ChatGPT"
agenda done "cancelar ChatGPT"
agenda snooze "cancelar ChatGPT" 2h
agenda focus
agenda reminders
```

Implementación inicial: script Python sin dependencias externas.

Ruta sugerida:

```txt
Hermes/Systems/vps/scripts/agenda.py
```

Luego brain-local/pc-ops puede replicar alias equivalente en local apuntando al vault sincronizado.

## 8. Capas: Agenda, Sessions, Daily

La agenda no debe convertirse en diario narrativo. Se propone separación por capas:

| Capa | Archivo | Rol |
|---|---|---|
| Operación | `Hermes/Agenda/YYYY-MM-DD.md` | tareas, prioridad, reminders, estado |
| Bitácora | `Hermes/Sessions/YYYY-MM-DD.md` | qué pasó durante el día, eventos por hora |
| Síntesis | `Hermes/Daily/YYYY-MM-DD-summary.md` | cierre del día, acciones comprometidas, aprendizajes |

Agenda linkea a Sessions. Daily resume solo si hubo trabajo real o acciones pendientes.

## 9. Estados de tarea

Estados permitidos:

| Estado | Significado |
|---|---|
| `pending` | abierta |
| `scheduled` | recordatorio programado o detectado |
| `sent` | recordatorio enviado |
| `done` | completada |
| `cancelled` | cancelada por Juan |
| `snoozed` | postergada con nuevo reminder |

Checkbox y estado deben mantenerse coherentes:

| Checkbox | status esperado |
|---|---|
| `[ ]` | pending/scheduled/sent/snoozed |
| `[x]` | done |

## 10. IDs de tarea

Formato propuesto:

```txt
ag-YYYYMMDD-NNN
```

Ejemplo:

```txt
ag-20260628-001
```

Sirve para editar tareas sin depender del texto exacto.

## 11. Fases de implementación

### Fase 1 — Documento + formato

- Crear este documento.
- Definir template Agenda V2.
- Avisar a brain-local mediante handoff.

### Fase 2 — Parser/escritor de agenda

- Crear script Python para:
  - crear agenda diaria
  - agregar tarea
  - listar hoy/mañana
  - marcar done
  - snooze
  - focus

### Fase 3 — Reminder scanner

- Crear `agenda-reminder-scan.py`.
- Probar contra archivo de agenda controlado.
- Configurar cron cada 5 min.
- Verificar envío Telegram.

### Fase 4 — Telegram UX

- Estandarizar prompts de entrada por texto.
- Verificar pipeline de audio Telegram → STT → texto.
- Forzar salida textual por defecto.

### Fase 5 — Integración con apertura/cierre

- Apertura brain-vps muestra:
  - 🔴 pendientes
  - próximo reminder
  - foco sugerido
- Cierre marca completadas y propone arrastre, sin autoarrastrar.

## 12. Riesgos y controles

| Riesgo | Control |
|---|---|
| Duplicar tareas por texto parecido | usar IDs y búsqueda fuzzy conservadora |
| Recordatorio enviado dos veces | status `sent` + lock file temporal |
| Audio mal transcripto | responder resumen texto y pedir confirmación si hay ambigüedad crítica |
| Agenda se vuelve MEMORY paralelo | regla: solo tareas y eventos accionables |
| PC local no se entera | handoff vps-to-local informativo |
| Conflictos Git | mantener un archivo por día y edits pequeños |

## 13. Criterios de éxito

- Juan carga tareas desde Telegram en menos de 20 segundos.
- Juan puede mandar audio y recibir confirmación textual.
- Cualquier terminal puede ejecutar `agenda hoy` y ver lo mismo que Obsidian.
- Recordatorios salen sin crear crons manuales por tarea.
- La apertura de sesión muestra foco y próximo recordatorio.
- No se mezcla agenda con MEMORY ni pipeline comercial.

## 14. Implementación inicial — 2026-06-27

### Archivos implementados

```txt
Hermes/Systems/vps/scripts/agenda.py
Hermes/Systems/vps/scripts/agenda-reminder-scan.py
Hermes/Systems/vps/scripts/agenda
```

### Comandos disponibles

```bash
# Ver agenda de hoy / mañana
Hermes/Systems/vps/scripts/agenda hoy
Hermes/Systems/vps/scripts/agenda mañana

# Equivalente Python explícito
python3 Hermes/Systems/vps/scripts/agenda.py today
python3 Hermes/Systems/vps/scripts/agenda.py tomorrow

# Crear archivo Agenda V2 si no existe
python3 Hermes/Systems/vps/scripts/agenda.py ensure --date 2026-06-28

# Listar día específico
python3 Hermes/Systems/vps/scripts/agenda.py list --date 2026-06-28

# Agregar tarea
python3 Hermes/Systems/vps/scripts/agenda.py add --date 2026-06-28 --priority red --title "Cancelar prueba ChatGPT" --reminder "09:00"

# Marcar tarea como hecha
python3 Hermes/Systems/vps/scripts/agenda.py done ag-20260628-001 --date 2026-06-28

# Posponer recordatorio
python3 Hermes/Systems/vps/scripts/agenda.py snooze ag-20260628-001 11:00 --date 2026-06-28

# Ver foco único
python3 Hermes/Systems/vps/scripts/agenda.py focus --date 2026-06-28

# Ver recordatorios
python3 Hermes/Systems/vps/scripts/agenda.py reminders --date 2026-06-28

# Scanner de recordatorios en modo prueba
python3 Hermes/Systems/vps/scripts/agenda-reminder-scan.py --date hoy --dry-run
```

### Estado de activación

- Parser/CLI: implementado y probado en vault temporal.
- Scanner de recordatorios: implementado y probado en `--dry-run`.
- Cron recurrente cada 5 minutos: **activado por orden explícita de Juan el 2026-06-27 09:26 ART**. Job Hermes `acafddde60b4` — `Agenda V2 reminder scanner` — schedule `every 5m` — `no_agent: true` — script `agenda-reminder-scan.sh`.
- Agenda real `2026-06-28.md`: migrada a formato V2 para la tarea de cancelar ChatGPT. Tiene `status: scheduled` porque ya existe cron Hermes externo `9f6b80cff249` para el aviso del 28/06 09:00 ART.

### Próxima acción propuesta

Validar con Juan si activamos el scanner automático cada 5 minutos mediante Hermes cron `no_agent` o crontab del sistema. Recomendación: Hermes cron `no_agent` al inicio para poder pausarlo/listarlo desde Hermes.
