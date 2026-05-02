# MEMORY.md — Estado operativo de Hermes
# Ubicación: vault/Hermes/MEMORY.md (GitHub → VPS + PC + Android)
# Este archivo lo escribe Hermes al cerrar cada sesión.
# No es un log. Es siempre el estado ACTUAL. El historial vive en Daily/.

---
## Última actualización
Fecha: 2026-05-02
Sesión: Apertura — primera sesión post-configuración vault

---

## Semáforo actual

**Estado:** 🔴 Crítico
**Gap mensual:** $400 ingreso / $900 gasto = –$500/mes
**Última revisión financiera:** 2026-05-02
**Próxima revisión financiera:** domingo 2026-05-04

---

## Pipeline activo

| Lead | Empresa | Valor | Estado | Próxima acción | Fecha límite |
|---|---|---|---|---|---|
| Franco Roma | Roggero & Roma | $400 + $25/mes | ✅ CERRADO 28/04 | Enviar contrato | 2026-05-02 |
| Luis Farias | Farias & Asociados | $300 + $50/mes | PDF enviado | Follow-up si no responde | 2026-05-05 |
| Comforti Propiedades | — | — | Sin contactar | Integrar a secuencia outreach | pendiente |
| Rivas Inmuebles | — | — | Sin contactar | Integrar a secuencia outreach | pendiente |
| Gamma | — | — | Sin contactar | Integrar a secuencia outreach | pendiente |

**Días sin movimiento en pipeline:** 4 (desde cierre Franco Roma 28/04)
**Alerta activa:** sí — pipeline sin leads activos en follow-up

---

## Checkpoints China

| Checkpoint | Objetivo | Estado | Fecha límite |
|---|---|---|---|
| C1 | $400/mes estabilizados | 🔴 Pendiente | Julio 2026 |
| C2 | $700/mes | 🔴 Pendiente | Agosto 2026 |
| C3 | $1.000/mes con 2+ fuentes | 🔴 Pendiente | Septiembre 2026 |

---

## USD cobrados — historial mensual

| Mes | Ingreso | Gasto | Gap | Estado |
|---|---|---|---|---|
| Abril 2026 | $400 | $900 | –$500 | 🔴 |
| Mayo 2026 | $0 | en curso | — | 🟡 En curso |

---

## Última acción comprometida

**Acción:** Enviar contrato a Franco Roma (Roggero & Roma)
**Comprometida en sesión:** 2026-05-02
**Ejecutada:** pendiente
**Resultado:** —

---

## Modo activo actual

**Modo:** Ejecución
**Activado:** 2026-05-02
**Razón:** Primer cliente cerrado. Cobrar y entregar. Expandir pipeline.
**Condición para cambiar de modo:** Semáforo 🟢 (gap > $0 por 30 días consecutivos)

---

## Estado del daemon y VPS

| Servicio | Estado | Última verificación |
|---|---|---|
| wolfim-agent Docker | Running (port 4011) | 2026-05-02 |
| wolfim-client Docker | ⚠️ No en PM2 | 2026-05-02 |
| wolfim-cron-alerts Docker | ⚠️ No en PM2 | 2026-05-02 |
| outreach-api (PM2) | Running (pid 213055, uptime 46h) | 2026-05-02 |
| outreach-daemon (PM2) | Running (pid 228261, uptime 40h, restarts 2) | 2026-05-02 |

**Leads en DB:** [N — consultar Supabase]
**Outreach enviados (mes actual):** [N — consultar DB]
**Errores activos en PM2:** Restarts 2 en outreach-daemon — monitorear

---

## Correcciones aprendidas

*(Hermes registra aquí cada vez que Juan señala una decisión incorrecta)*

| Fecha | Decisión incorrecta | Razón | Regla nueva |
|---|---|---|---|
| — | — | — | — |

---

## Lecciones de proyectos anteriores

| Proyecto | Lección |
|---|---|
| Wolfim WA SaaS | Validar canal antes de construir |
| Market Intelligence | Validar fuente antes de vender inteligencia |
| Sistema Dental | Cobrar antes de construir. Precio desde día 1. |
| Landings web | El producto no vale nada si no se cobra |
| Sales Machine WA | Canal de distribución tan importante como el producto |
| Dashboard padre | El primer cliente real está más cerca de lo que parece |

---

## Notas de sesión activa

*(Hermes usa este espacio como scratchpad durante la sesión. Se limpia al cerrar.)*

- Vault configurado: /home/hermes/obsidian-vault → GitHub Ziramog/obsidian-vault-main
- SOUL.md, AGENTS.md sincronizados: ~/.hermes/ == vault/Hermes/Config/
- MEMORY.md actualizado al inicio de sesión
- Daily summaries y session snapshots se crean al cerrar sesión
- Nota: 2 restarts en outreach-daemon — ver causa
