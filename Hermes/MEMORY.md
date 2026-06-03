# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

**Última actualización:** 2026-06-03 | Franco Roma validado · cobra $300 USD mañana 04/06 | Model: MiniMax-M3

---

## Semáforo
🟡 Supervivencia (transición a 🟠) — Gap mayo: –$333. **Hoy 03/06: $300 USD confirmados para mañana 04/06** (Franco Roma). Si entra, gap baja a –$33.
**Cristina Welldone SRL CAÍDA** — descartada por Juan (farsante, no cerró)
**Franco Roma — PRODUCCIÓN** — Sitio en producción 03/06 (roggeroyroma.com HTTP 200). $200 ya cobrados. **$300 USD finales a cobrar 04/06** por retrabajos de frontend. Total $500 (ajuste desde $400 original).

---

## Pipeline activo
- **Franco Roma — Roggero & Roma** ✅ VALIDADO 03/06: Sitio en producción. Franco ya lo vio. Cobra $300 USD mañana 04/06. Add-ons (Google Reviews + 3 ideas Juan) próximos a implementar.
- **Comforti Propiedades** — Plantilla vacía. Sin datos de contacto. Necesita scavenging.
- **RIVAS Inmuebles** — Propuesta PDF armada pero sin contexto de contacto.
- **Gamma** — Sin contactar. Datos de contacto vacíos.
- Luis Farias: PDF enviado — en viaje, vuelve julio. Follow-up retomar julio.
- Ann: Pitch enviado — seguimiento pendiente
- Comforti/Rivas/Gamma: Juan pidió atacar — bloqueados por falta de datos (teléfono/email)

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
- [[SOUL]]
- [[2026-06-02-summary|Daily/2026-06-02]]
- [[2026-06-02|hq/sessions/2026-06-02]]
