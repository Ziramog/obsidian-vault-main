# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

**Última actualización:** 2026-06-04 09:00 | Scavenging 3 leads completado · meta junio $600 · Franco cobra hoy a la tarde | Model: MiniMax-M3

---

## Semáforo
🟡 Supervivencia — Gap mayo: –$333. **HOY 04/06 tarde: $300 USD a cobrar de Franco Roma.** Si entra → gap –$33, semáforo a 🟠. Meta junio: **$600 USD**. Faltan $300 después de Franco.

---

## Pipeline activo
- **Franco Roma — Roggero & Roma** ✅ VALIDADO 03/06 · 💰 cobrar HOY $300 USD · Total $500
- **GAMA Inmobiliaria** (Mar del Plata) 🆕 04/06 — 4.5⭐ (108 reseñas) · tel 0223 633-7766 · Lead prioritario
- **Conforti Propiedades** (Villa Carlos Paz) 🆕 04/06 — 4.5⭐ (53 reseñas) · tel 03541 67-5105
- **RIVAS Inmuebles** (CABA) 🆕 04/06 — 4.9⭐ (1 reseña) · tel 011 6827-4827
- Luis Farias: PDF enviado — en viaje, vuelve julio
- Ann: Pitch enviado — seguimiento pendiente
- ~~Comforti/Rivas/Gamma: bloqueados por falta de datos~~ ✅ RESUELTO 04/06 vía Serper

## Korantis — STANDBY
Regla activa: no se toca con semáforo 🔴/🟡. Hoy (🟡) Juan intentó reactivar trabajo en Korantis dos veces. Frenado. Solo se reactiva cuando Wolfim llegue a 🟠 o superior.

## wolfim.com — 8.5/10
Auditado 03/06. No se re-audita. Top 3 fixes anotados. NO es el cuello de botella del negocio.

---

## Diagnóstico infraestructura (02/06/2026)
- **PM2 vacío** — procesos zombie corren fuera de PM2 (PID 2281900 outreach-daemon, 2350582 wolfim-api)
- **Sesión WhatsApp muerta** — `baileys-connect/` sin `creds.json`, solo `qr.txt` raw PNG
- **Teléfonos SUPABASE MÁSCARADOS** — RLS devuelve `+549****8601`. Outreach manda a números que no existen. **0% delivery histórica.**
- **Decisión Juan:** Saltar outreach automático, ir manual.

---

## Leads calientes vs. atacables
| Lead | Estado | Atacable HOY? | Bloqueo |
|------|--------|---------------|---------|
| Franco Roma | HOY producción | ✅ SÍ | Confirmar link |
| Comforti | Vacío | ❌ NO | Falta teléfono + ciudad + nombre contacto |
| Rivas | Vacío (PDF existe) | ❌ NO | Falta teléfono + ciudad |
| Gamma | Vacío | ❌ NO | Falta teléfono + ciudad |
| Luis Farias | Julio | ❌ NO | Espera |
| Ann | Pendiente | ⚠️ Revisar | Sin datos de contacto |

---

## Preguntas pendientes para próxima sesión
1. Franco: ¿pasó a producción? ¿Tenés el link para validar?
2. Comforti/Rivas/Gamma: ¿ciudad + nombre completo? ¿O los busco yo en Google Maps?
3. ¿Ataco Ango o Construvial mientras no hay cierre? (regla SOUL: empresa secundaria solo con semáforo 🟠+, ahora 🔴)

---

## Model
- **Activo:** MiniMax-M3
- **Provider:** minimax
- **Anterior:** minimax-2.7 (cambiado 02/06/2026 a pedido Juan)
- **⚠️ Cambio aplica al próximo /reset** (no mid-session para preservar prompt cache)

---

## Construvial — Plan 3 fases activo (STANDBY por semáforo 🔴)
- 21 empresas en DB: leads_oil_gas_mining.csv
- Top contactos: CISA (Neuquén), Sigma SA (SJ), Dumandzic (SJ/CAT), CASEMICA (CAT)
- Solo investigación — sin outreach hasta activación explícita de Juan
- PROPUESTA ENVIADA 19/05: Propuesta_Construvial_Wolfim_2026.pdf

---

## Historial financiero mayo 2026

| Fecha | Ingreso | Detalle |
|-------|---------|---------|
| 02/05 | $200 | Franco Roma — adelantados |
| 10/05 | $225 USD | Construvial — cobrado |
| 14/05 | $142 USD | Construvial — viáticos Catamarca |
| 27/05 (esperado, NO cerrado) | $0 | Cristina Welldone SRL — FALLÓ |

**Total mayo real:** $567 ingresados / $900 gastos = Gap **–$333**

---

## Hito China — octubre 2026
- Meta: > $1.000 USD/mes con operación autónoma
- **Días restantes:** ~121
- **Estado:** 🔴 Crítico. Sin junio positivo, la probabilidad baja sensiblemente.

---

## Modo
Ejecución

---

## Racha cron-only finalizada
22 días (11/05 – 02/06). Sesión humana reactivada. Sin alertas pendientes.

---

## Correcciones aprendidas (2026-05-10, vigentes)
- Solo Google Reviews lo pidió Franco directamente — los otros 3 add-ons son IDEAS DE JUAN
- Productos Wolfim = solo los explícitamente en "Productos hoy" en webagency.md
- Neuquén = Oil & Gas / San Juan + Catamarca = Mining
- Los 49 leads de Posadas/San Vicente son de Wolfim (outreach manual del amigo de Juan)

## Correcciones aprendidas (2026-06-03, vigentes)
- Korantis es producto PROPIO de Juan, no un cliente ni un lead. Construido en hueco, no en evasión
- Korantis NO se toca con semáforo 🔴 o 🟡. Standby. Juan debe confirmar OK antes de cualquier trabajo en Korantis
- wolfim.com está 8.5/10 — el gap comercial NO es el sitio, es outreach/seguimiento/datos de contacto

---

## API Keys confirmadas
- Serper: `7f4c661b596a1110ec64d8ea4f137588c2176a5c`
- Firecrawl: `fc-43a...1eef`
- DataImpulse: SIN CRÉDITO (port 823 bloqueado desde VPS)
- MiniMax API: configurada en `~/.hermes/.env`

---

## Referencias
- [[Wolfim/WebAgency]]
- [[Construvial]]
- [[Franco Roma]]
- [[companies/wolfim/projects/korantis/index|Korantis proyecto]]
- [[companies/wolfim/research/korantis-audit-2026-06-03|Korantis auditoría]]
- [[companies/wolfim/research/korantis-benchmark|Korantis benchmark]]
- [[companies/wolfim/research/wolfim-com-audit-2026-06-03|wolfim.com auditoría]]
- [[SOUL]]
- [[2026-06-03-summary|Daily/2026-06-03]]
- [[2026-06-02-summary|Daily/2026-06-02]]
- [[2026-06-02|hq/sessions/2026-06-02]]
