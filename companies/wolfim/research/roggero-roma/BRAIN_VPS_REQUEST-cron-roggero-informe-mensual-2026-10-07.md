---
type: BRAIN_VPS_REQUEST
company: wolfim
client: roggero-roma
target: brain-vps
owner: wolfim-growth
created: 2026-10-07
priority: high
status: pending
---

# Cron `roggero-roma-informe-mensual` — arreglar y limpiar formato

## Contexto

El job de cron **`roggero-roma-informe-mensual`** (`bd57ddb53d14`, schedule `0 10 7 * *`) vive en el
store de cron del **perfil por defecto** (brain-vps), no en el de `wolfim-growth`. Por eso no puedo
modificarlo directamente: escalo para que brain-vps aplique el cambio.

## Qué pasó (verificado)

El job venía fallando y, cuando por fin corrió, generó el **formato viejo**:

| Corrida | Resultado |
|---|---|
| 2026-07-08 | FAILED — `HTTP 429: usage limit` |
| 2026-08-07 | FAILED — `Skipped to prevent unintended spend` (drift de modelo, job sin pin) |
| 2026-09-07 | FAILED — `HTTP 429: usage limit` |
| 2026-10-07 10:02 | **OK** — generó y envió a Telegram (msg 8288) el informe **viejo** `2026-09-01 → 2026-09-30` |

Problemas del job actual:

1. Es un job **con agente** (`no_agent: false`): consume inferencia → queda expuesto a `HTTP 429`
   y al guard de spend por drift de modelo.
2. No está **pineado**: el 2026-08-07 se saltó por drift de config (`gpt-5.5` → `gpt-5.4`).
3. Ejecuta el script **viejo** `/home/hermes/scripts/generate_roggero_analytics_auto.py`, que usa
   totales crudos, `BUENOS AIRES` y no aplica el filtro limpio auditado.
4. El 2026-10-07 produjo un informe de **mes calendario** (Sep 1–30), que no coincide con el
   criterio del último informe entregado (ciclo **7 → 6**).

## Fix propuesto (listo para aplicar)

Convertir el job a **`no_agent`** con un wrapper de shell (sin inferencia → sin 429 ni drift) que
genera el informe **limpio ya auditado** y lo envía a Telegram.

Wrapper ya creado y probado (modo `ROGGERO_NO_SEND=1`):

- `/home/hermes/.hermes/scripts/roggero-informe-mensual-wrapper.sh`

Generador limpio que usa:

- `/home/hermes/obsidian-vault/companies/wolfim/research/roggero-roma/generate_roggero_analytics_auditado_periodo.py`
- Intérprete: `/home/hermes/.hermes/hermes-agent/venv/bin/python` (tiene `google-auth`, `fpdf2`, `requests`)
- Período por defecto: ciclo **7 → 6** (p. ej. corriendo el 7/10: `2026-09-07 → 2026-10-06`)

### Cambio exacto requerido en el job `bd57ddb53d14`

```
no_agent = true
script   = /home/hermes/.hermes/scripts/roggero-informe-mensual-wrapper.sh
deliver  = local           (el wrapper envía el PDF a Telegram por sí mismo)
schedule = 0 10 7 * *      (sin cambios)
```

Equivalente:

```
cronjob action=update job_id=bd57ddb53d14 \
  no_agent=true \
  script=/home/hermes/.hermes/scripts/roggero-informe-mensual-wrapper.sh \
  deliver=local
```

## Convención de período — CONFIRMADA por Juan

Juan confirmó **ciclo 7 → 6** (2026-10-07). Es el criterio del wrapper y del último informe
entregado (`2026-07-07 → 2026-08-06`). No usar mes calendario. Aplicar sin cambios.

## Evidencia de la migración de formato

Informes limpios ya generados y enviados a Telegram (2026-10-07):

| Período | Total depurado | message_id |
|---|---|---|
| 2026-08-07 → 2026-09-06 | 62 usuarios · 94 sesiones · 248 vistas · 57,4% engagement | 8291 |
| 2026-09-07 → 2026-10-06 | 152 usuarios · 203 sesiones · 650 vistas · 60,6% engagement | 8292 |

El informe viejo del cron (msg 8288, período 2026-09-01 → 2026-09-30) queda **obsoleto**.

## Pendiente relacionado (el job de backup)

El job `roggero-roma-backup` (`80ad16afa9df`) figura `last_status: error` por
`ModuleNotFoundError: No module named 'ruamel'` en el worker de cron externo. Es infra de brain-vps;
queda fuera de esta tarea pero conviene revisarlo.

## Seguridad

- No registrar tokens, claves ni secretos. Referenciar credenciales como `[credencial: NOMBRE]`.
