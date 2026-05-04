---
title: "Hermes Kanban v0.12.0 — Multi-Agent Coordination"
type: research
created: 2026-05-04
updated: 2026-05-04
tags: [hermes, multi-agent, kanban, ops-research]
confidence: high
sources: [hermes-agent.nousresearch.com, x.com/Teknium, github.com/nousresearch/hermes-agent]
status: filed
---

# Hermes Kanban v0.12.0 — Multi-Agent Coordination

## De qué se trata

Kanban Board para coordinar múltiples agentes Hermes. Cada tarea es un row en `~/.hermes/kanban.db` (SQLite). Cada agente es un **full OS process** con identidad propia, no un thread dentro del proceso padre.

## Kanban vs delegate_task

| Aspecto | `delegate_task` | Kanban |
|---|---|---|
| Forma | RPC call (fork → join) | Durable message queue + state machine |
| Padre | Bloquea hasta que termina | Fire-and-forget tras `create` |
| Identidad del agente | Subagente anónimo | Named profile con memoria persistente |
| Recuperación | Ninguna — fail = fail | Block → unblock → re-run; crash → reclaim |
| Humano en el loop | No soportado | Comment / unblock en cualquier momento |
| Audit trail | Se pierde con context compression | Rows en SQLite para siempre |
| Coordinación | Jerárquica (padre → hijo) | Peer — cualquier profile lee/escribe cualquier task |

## Estados de tarea

```
triage → todo → ready → running → blocked → done → archived
```

## Herramientas del worker (7)

Disponibles SOLO cuando el agente corre dentro de una tarea Kanban (`HERMES_KANBAN_TASK` set in env):

- `kanban_show` — leer tarea actual (title, body, prior attempts, parent handoffs, comments)
- `kanban_complete` — terminar con `summary` + `metadata` (handoff estructurado)
- `kanban_block` — escalar para input humano
- `kanban_heartbeat` — señal de vida durante operaciones largas
- `kanban_comment` — append al thread de la tarea
- `kanban_create` — (orchestrators) crear tareas hijas
- `kanban_link` — (orchestrators) agregar dependencias post-hoc

## Workspace options

| Tipo | Ubicación |
|---|---|
| `scratch` | `~/.hermes/kanban/workspaces/<id>/` |
| `worktree` | `.worktrees/<id>/` (via `git worktree add`) |
| `dir:<path>` | Path custom (e.g. `dir:../tenants/foo/`) |

## Configuración

```yaml
kanban:
  dispatch_in_gateway: true  # default — usa el gateway como dispatcher
  dispatch_interval_seconds: 60  # default
```

**Deprecated:** `hermes kanban daemon` como proceso separado. Si se corre junto con el gateway causa claim races.

## Casos de uso complementarios

- `inbox-triage` — clasificar inbox automáticamente
- `ops-review` — revisión operativa periódica

## Features interesantes para el stack actual de Juan

### 1. Circuit breaker
Mantiene jobs largos vivos, mata runaway agents. **Relevante para:** daemon de WhatsApp que se cuelga sin motivo. El watchdog actual es manual (PM2 restart).

### 2. Dependencias entre tareas
`todo → ready` (promueve cuando todos los padres llegan a `done`). **Relevante para:**
```
scrape_leads → enrich → qualify → outreach
```
Encadenado automático: cuando scrape termina, enrich arranca solo.

### 3. Agente especializado por vertical
Un agente para `inmobiliarias`, otro para `concesionarias_autos`, cada uno con:
- Su propio workspace
- Su propia cola de leads
- Su propio skill set
- Coordinación centralizada desde dashboard

### 4. Shared workspaces para file handoffs
Un agente deja archivos, el siguiente los pickea. Relevante para el pipeline actual: scraper deja `leads.json`, enricher lo toma, calificador lo procesa.

### 5. SQLite-backed — sobrevive a crashes
El `kanban.db` persiste. Si el VPS se reinicia, las tareas retoman donde quedaron. Reemplaza los scripts Python sueltos + cron que actualmente no tienen estado durable.

### 6. Comments per task
Agentes dejan notas entre sí. Relevante para debugging comercial: "¿Lead cualificado — necesita follow-up manual?"

## Qué NO es

- No es un reemplazo del gateway de mensajería
- No corre dentro de una sesión de chat normal — necesita `hermes gateway start` + workers dedicados
- No es plug-and-play para el setup actual — requiere migrar los scripts Python a workers Kanban

## Relevancia para el Hito China (oct 2026)

| Criterio | Evaluación |
|---|---|
| ¿Acelera primer USD? | ❌ No直接的 — mejora operación, no genera ventas |
| ¿Merece tiempo de implementación? | ⚠️ Requiere evaluar costo de migración vs mejora real |
| ¿Encaja con gap actual? | ⚠️ Supone que el pipeline ya funciona — actualmente no está corriendo |

**Veredicto:** Interesante para fase de escala (>$1.000/mes). Para supervivencia actual, el foco debe ser cerrar ventas, no mejorar infrastructure.

## Cómo probarlo (cuando tenga sentido)

```bash
# 1. Inicializar board
hermes kanban init

# 2. Arrancar gateway (host del dispatcher)
hermes gateway start

# 3. Crear tarea de prueba
hermes kanban create "research AI trends for Q2" --assignee researcher

# 4. Ver actividad live
hermes kanban watch

# 5. Ver board
hermes kanban list
hermes kanban stats

# Dashboard web
hermes web
```

## Worker skill

```bash
hermes skills install devops/kanban-worker
```

## Notas

- Install skill: `hermes skills install devops/kanban-worker` (NO via skills.sh registry — es un skill oficial)
- Dashboard web: `hermes web` (nuevo en v0.12.0, separado del kanban)
- Multi-tenant: `--tenant business-a` para aislar boards

## Link

https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
