---
owner: brain-vps
type: registro-de-frentes
created-at: 2026-10-08
updated-at: 2026-10-09T07:45:00-03:00
single-writer: brain-vps
corte: 2026-10-09
conteo-corte-2026-10-09: 30 abiertos = 13 vencidos · 1 vence-hoy · 1 bloqueado · 10 sin-fecha · 5 en-fecha (+2 sin clasificar, no contados)
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

**Corte 2026-10-09: 30 abiertos = 🔴 13 · ⏰ 1 · 🔒 1 · ⏳ 10 · 🟢 5.** *(`sin fecha` no es un estado válido de largo plazo: se fecha o se da de baja.)* Los `❓ sin clasificar` de la bandeja **no se cuentan como frentes** (son ruido hasta que tengan dueño y fecha).

## 🔥 Hoy — los 3 del día (WIP 3/3)

> Vienen **sin cerrar del 08/10**: se arrastran con aviso, no en silencio. Si el WIP sigue lleno, no entra ningún frente nuevo.

| # | Frente | Acción de hoy | Dueño |
|---|---|---|---|
| D1 | `kpis.md` (15 semanas vacío) | Habilitar el archivo o llenarlo — 30 seg | Juan |
| D5 | Token Telegram `algolab` (PC) | "Dale": una línea + restart | Juan |
| P1 | Presol sem 2 — **333 USD** | Cobrar **hoy** + confirmar continuidad de octubre | Juan |

**Batch de 2 minutos:** D3 (¿los USD 100 de Víctor tocan el recibo ARS 178.860?).

> ✅ **D6 (Contabo CCP) cerrado hoy**: Juan confirmó que **ya está pago**.

---

## 🔴 Decisiones de Juan (bloquean trabajo de otros)

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| D1 | `Intelligence/kpis.md` | Habilitar para que brain-vps lo mantenga, o llenarlo él | 2026-10-08 | 🔴 vencido (desde 25/06) |
| D2 | Briefing reality-check | Confirmar prioridades y refrescar v2 | 2026-10-01 | 🔴 vencido |
| D3 | Víctor Abrile — recibo ARS 178.860 | ¿Los USD 100 del 08/10 son ítem nuevo o lo saldan? | 2026-10-08 | 🔴 vencido |
| D4 | 4 handoffs ANGO de julio | ¿Siguen vivos o se rescopean a uno solo? | 2026-07-28 | 🔴 vencido |
| D5 | Token Telegram en `profiles/algolab/.env` (PC) | "Dale" al fix de 1 línea + restart | 2026-10-04 | 🔴 vencido |
| D7 | RWS / TrainAI dubbing | Arrancar la cola (160 jobs prioridad 0) o dar de baja la vía | sin fecha | ⏳ sin fecha |
| D8 | `hermes-session-reset-policy` | OK de Juan | 2026-10-07 | 🔴 vencido |
| D9 | `Memory/pending/` (2 items: Sync V6, JobSeeker) | Consolidar o descartar | sin fecha | ⏳ sin fecha |

## 💰 Plata

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| P1 | Construvial — Presol sem 2 | Cobrar **333 USD** + confirmar continuidad octubre | 2026-10-09 | ⏰ vence hoy |
| P2 | Wolfim — Farias mantenimiento | Nada hasta abr-2027 (bonificado oct-26 → mar-27) | 2027-04-01 | 🟢 en fecha |
| P3 | Raypac / Leonardo Gastager | Decidir seguimiento cotización kit 360° (USD 14.750) | sin fecha | ⏳ sin fecha |

## 🏢 Comercial (el cuello de botella real)

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| C1 | 113 leads inmobiliarios (MdP/Pinamar/Villa Gesell) | Reactivar con inventario nuevo o dar de baja el canal email | sin fecha *(cola caída 02/09)* | ⏳ sin fecha |
| C2 | Madelen · Conforti · RIVAS · Ann | Follow-up comercial (último movimiento 31/08) | sin fecha | ⏳ sin fecha |
| C3 | Google Ads ANGO (cuenta 901-572-7445) | Responder la asesoría gratuita ofrecida | sin fecha | ⏳ sin fecha |
| C4 | Roggero & Roma — GA4 | Eventos custom en 0 desde ~30/07; aplicar fix cron backup (`no_agent` + wrapper) | sin fecha | ⏳ sin fecha |

## 🖥️ Ejecución local (handoffs vivos — 8 `ready`)

| # | Frente | Due | Estado |
|---|---|---|---|
| L1 | `HO-2026-07-13-001` Sync V6 a profiles locales | 2026-07-14 | 🔴 vencido |
| L2 | `HO-2026-07-16-001` ANGO landing Urvig/Micron | 2026-07-17 | 🔴 vencido |
| L3 | `HO-2026-07-22-001` ANGO GA4 + Ads | 2026-07-23 | 🔴 vencido |
| L4 | `HO-2026-07-24-001` ANGO tag AW | 2026-07-25 | 🔴 vencido |
| L5 | `HO-2026-07-27-001` ANGO cuenta de Ads nueva | 2026-07-28 | 🔴 vencido |
| L6 | `HO-2026-08-03-001` Almas Libres MVP + padrinazgo | 2026-08-07 | 🔴 vencido |
| L7 | `HO-2026-08-03-002` Wolfim Motors demo portal (high) | 2026-08-05 | 🔴 vencido |
| L8 | `HO-2026-10-04-001` poller Telegram | 2026-10-06 | 🔒 bloqueado por D5 |

## 🧱 Sistema / deuda

| # | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| S1 | WP31 — backfill `tenantId` + uniques legacy | OK + snapshot para el `--apply` | sin fecha | ⏳ sin fecha |
| S2 | Conflicto de merge en `companies/wolfim/intelligence/plan-ads-seo-2026-06-29.md` | Decidir resolución (markers desde 29/06) | sin fecha | ⏳ sin fecha |
| S3 | `hermes-vps-ops/SKILL.md` en el techo de 100k chars | Partir el skill | sin fecha | ⏳ sin fecha |
| S4 | **Bot de agenda: capturar crudo y no perder nada** | Que nunca pierda tu texto (guarda crudo + marca para triage) y responda en ≤2 s; si no da, se retira el canal y queda solo la bandeja | 2026-10-12 | 🟢 en fecha |
| S5 | **PWA — pestaña "HOY"** (`HO-2026-10-09-001`) | Leer el día en 2 segundos sin pasar por el chat: render de `HOY.md` + `Frentes.md` | 2026-10-11 | 🟢 en fecha |

## 📌 Fechado — triado de la bandeja del bot (09/10)

| # (id del bot) | Frente | Próxima acción | Due | Estado |
|---|---|---|---|---|
| ag-20261009-001 | ANGO — cotización para Palmero | Cerrarla **antes del lunes** | 2026-10-12 | 🟢 en fecha |
| ag-20261009-002 | Wolfim — publicidad Víctor (Argenprop + Meta) | Arrancar el trabajo **martes** | 2026-10-13 | 🟢 en fecha |

### ❓ Sin clasificar (no son frentes todavía — falta contexto de Juan)

| id | Lo que entró | Qué falta |
|---|---|---|
| ag-20261009-003 | "agenda" | No dice qué de la agenda: ¿revisarla, arreglarla, mostrarla? |
| ag-20261009-005 | "semana que viene" | Audio cortado: ¿qué cosa es para la semana que viene? |

---

## Cerrado el 2026-10-09

| Frente | Cómo cerró |
|---|---|
| D6 — Aviso Contabo (CCP) | Juan confirmó que **ya está pago** (09/10) |
| ag-20261009-004 "listar comandos" | Respondido en el chat con la lista de comandos del bot; destapó la falla del fallback → S4 |

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
