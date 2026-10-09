---
owner: brain-vps
type: registro-de-frentes
created-at: 2026-10-08
updated-at: 2026-10-09T16:45:00-03:00
single-writer: brain-vps
corte: 2026-10-09
conteo-corte-2026-10-09: 25 abiertos = 5 vencidos · 2 vence-hoy · 1 bloqueado · 11 sin-fecha · 6 en-fecha
criterio-de-conteo: ver sección "Criterio de conteo" (buckets por due-at ISO vs fecha de corte)
-rule: un frente sin dueño y sin due-at no es un frente, es ruido
---

# Frentes.md — mapa único de frentes abiertos

> **Escritor único:** brain-vps. Los demás agentes piden altas/bajas por handoff o daily; Juan dicta por audio/texto y brain-vps convierte.
> **Captura:** `Agenda/bandeja.md` — tirás texto o audio **crudo y sin esperar respuesta**. La bandeja no interpreta: guarda. brain-vps triagea después y lo convierte en frente con dueño y fecha (o lo devuelve con una pregunta).
> **Regla:** cada frente tiene **un solo cerrador** (con permiso de escritura) y un **`due-at`**. Si el `due-at` pasa sin movimiento, el frente aparece solo en `Agenda/HOY.md`.
> **WIP:** máximo **3 frentes activos por día**. El resto es backlog con dueño y fecha. Nadie arranca un frente nuevo con WIP lleno.

## Criterio de conteo (fijo, no depende del criterio de quien mira)

Cada frente cae en **un solo** bucket, por su `due-at` ISO contra la fecha de corte:

| Bucket | Definición |
|---|---|
| 🔴 **vencido** | `due-at` **anterior** al corte |
| ⏰ **vence hoy** | `due-at` **igual** al corte |
| 🟢 **en fecha** | `due-at` posterior al corte |
| 🔒 **bloqueado** | el cierre depende de otro frente (se cuenta aparte; **no** suma a vencidos) |
| ⏳ **sin fecha** | no hay `due-at` ISO → **violación de la regla**, se cuenta aparte y no entra en vencidos |

**Corte 2026-10-09: 25 abiertos = 🔴 5 · ⏰ 2 · 🔒 1 · ⏳ 11 · 🟢 6.** *(`sin fecha` no es un estado válido de largo plazo: se fecha o se da de baja.)* Las capturas incompletas permanecen en `Agenda/bandeja.md`; no se cuentan como frentes.

## 🔥 Hoy — los 3 del día (WIP 3/3)

> Vienen **sin cerrar del 08/10**: se arrastran con aviso, no en silencio. Si el WIP sigue lleno, no entra ningún frente nuevo.

| # | Frente | Acción de hoy | Dueño |
|---|---|---|---|
| P1 | **Presol — liquidación por horas** | Relevar horas/días trabajados, acordar criterio y calcular importe | Juan |
| D5 | Telegram PC/VPS | Separar tokens y probar ambos bots | Juan + brain-vps |
| ag-20261009-001 | ANGO — cotización Palmero | Avanzar hoy; cerrar antes del lunes 12/10 | Juan |

> ✅ **D6 (Contabo CCP) cerrado hoy**: ya está pago.

---

## 🔴 Decisiones de Juan (bloquean trabajo de otros)

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| D2 | Briefing reality-check | Confirmar prioridades y refrescar v2 | 2026-10-01 | 🔴 vencido |
| D5 | Telegram PC/VPS | Ejecutar en PC la baja del token duplicado de `algolab` + prueba end-to-end de `@Freedoom777bot`; arquitectura de dos bots ya aprobada por Juan | 2026-10-09 | ⏰ vence hoy |
| D7 | RWS / TrainAI dubbing | Arrancar la cola (160 jobs prioridad 0) o dar de baja la vía | sin fecha | ⏳ sin fecha |
| D8 | `hermes-session-reset-policy` | OK de Juan | 2026-10-07 | 🔴 vencido |
| D9 | `Memory/pending/` (2 items: Sync V6, JobSeeker) | Consolidar o descartar | sin fecha | ⏳ sin fecha |

## 💰 Plata

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| P1 | Construvial — Presol | Liquidar por horas efectivamente trabajadas; monto aún no definido | 2026-10-09 | ⏰ vence hoy |
| P2 | Wolfim — Farias mantenimiento | Nada hasta abr-2027 (bonificado oct-26 → mar-27) | 2027-04-01 | 🟢 en fecha |
| P3 | Raypac / Leonardo Gastager | Decidir seguimiento cotización kit 360° (USD 14.750) | sin fecha | ⏳ sin fecha |

## 🏢 Comercial (el cuello de botella real)

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| C1 | 113 leads inmobiliarios (MdP/Pinamar/Villa Gesell) | Reactivar con inventario nuevo o dar de baja el canal email | sin fecha *(cola caída 02/09)* | ⏳ sin fecha |
| C2 | Madelen · Conforti · RIVAS · Ann | Follow-up comercial (último movimiento 31/08) | sin fecha | ⏳ sin fecha |
| C3 | Google Ads ANGO (cuenta 901-572-7445) | Responder la asesoría gratuita ofrecida | sin fecha | ⏳ sin fecha |
| C4 | Roggero & Roma — GA4 | Eventos custom en 0 desde ~30/07; aplicar fix cron backup (`no_agent` + wrapper) | sin fecha | ⏳ sin fecha |

## 🖥️ Ejecución local (handoffs vivos — 6 `ready`)

| # | Frente | Due | Estado |
|---|---|---|---|
| L1 | `HO-2026-07-13-001` Sync V6 a profiles locales | 2026-07-14 | 🔴 vencido |
| L6 | `HO-2026-08-03-001` Almas Libres MVP + padrinazgo | 2026-08-07 | 🔴 vencido |
| L7 | `HO-2026-08-03-002` Wolfim Motors demo portal (high) | 2026-08-05 | 🔴 vencido |
| L8 | `HO-2026-10-04-001` poller Telegram | 2026-10-06 | 🔒 bloqueado por D5 |
| L9 | `HO-2026-10-09-002` ANGO consolidado (landing + GA4 + Ads) | 2026-10-13 | 🟢 en fecha |
| — | `HO-2026-10-09-001` (pestaña "HOY" de la PWA) | 2026-10-11 | 🟢 en fecha *(se cuenta como S5)* |

## 🧱 Sistema / deuda

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| S1 | WP31 — backfill `tenantId` + uniques legacy | OK + snapshot para el `--apply` | sin fecha | ⏳ sin fecha |
| S2 | Conflicto de merge en `companies/wolfim/intelligence/plan-ads-seo-2026-06-29.md` | Decidir resolución (markers desde 29/06) | sin fecha | ⏳ sin fecha |
| S3 | `hermes-vps-ops/SKILL.md` en el techo de 100k chars | Partir el skill | sin fecha | ⏳ sin fecha |
| S4 | **Bot de agenda: capturar crudo y no perder nada** | `HO-2026-10-09-003` creado (high): consultas y fragmentos vagos no crean tareas; conservar captura o pedir precisión; timeouts normales no ensucian logs | 2026-10-12 | 🟢 en fecha |
| S5 | **PWA — pestaña "HOY"** (`HO-2026-10-09-001`) | Leer el día en 2 segundos sin pasar por el chat: render de `HOY.md` + `Frentes.md` | 2026-10-11 | 🟢 en fecha |

## 📌 Fechado — triado de la bandeja del bot (09/10)

| # (id del bot) | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| ag-20261012-001 | ANGO — cotización para Palmero | Cerrarla **antes del lunes** | 2026-10-12 | 🟢 en fecha |
| ag-20261013-001 | Wolfim — publicidad Víctor (Argenprop + Meta) | Arrancar el trabajo **martes** | 2026-10-13 | 🟢 en fecha |

### Capturas incompletas preservadas fuera del mapa

`ag-20261009-003` ("agenda") y `ag-20261009-005` ("semana que viene") no son frentes. Permanecen en `Agenda/bandeja.md` como texto crudo, sin contaminar la agenda activa.

---

## Cerrado el 2026-10-09

| Frente | Cómo cerró |
|---|---|
| D4 — 4 handoffs ANGO de julio | **Consolidados** por decisión de Juan en un solo trabajo → `HO-2026-10-09-002` (due 13/10); los 4 originales quedaron `cancelled` |
| D1 — `kpis.md` | Juan autorizó a brain-vps a mantenerlo; versión 1 creada con cobros de octubre y gastos aún pendientes |
| D3 — Víctor | Los USD 100 son ingreso nuevo e independiente; el recibo ARS 178.860 continúa separado |
| D6 — Aviso Contabo (CCP) | Juan confirmó que **ya está pago** |
| `HO-2026-06-25-001` (test de circuito) | Archivado en `Hermes/Handoffs/archive/vps-to-local/` |
| ag-20261009-004 "listar comandos" | Respondido con la lista de comandos del bot; destapó la falla del fallback → S4 |

## Cerrado el 2026-10-08

| Frente | Cómo cerró |
|---|---|
| Ingreso Víctor — USD 100 | Registrado (honorarios publicidad Argenprop + Meta) → `MEMORY.md` + briefing |
| `HO-2026-06-25-001` (test de circuito) | `cancelled` en ambos lados |
| `HO-2026-06-27-001` (aviso Agenda V2) | `cancelled` en ambos lados |
| `Agenda/HOY.md` congelada desde 22/09 | Reescrita como puntero al archivo del día |
| `HO-2026-10-08-001` (handoff del ingreso) | Ackado y aplicado |
| Verificación 733/399 | 733 = snapshot 30/09 (hoy 333); Farias = 399 documentado, no 400 |

## Reparto de roles (para no duplicar)

- **brain-vps** — dueño de este archivo y del triage: convierte lo que Juan tira por audio/texto en frentes con dueño y `due-at`. Único que crea/cierra filas y único que fija el criterio de conteo.
- **brain-local** — ejecución local + cierre de handoffs. Su inventario crudo queda como insumo de sesión, no como segunda lista.
- **auditor (agente en la PC)** — latido read-only: los 5 buckets de esta tabla, contados con este criterio, al daily.
