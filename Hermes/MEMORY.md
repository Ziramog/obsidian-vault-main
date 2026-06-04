# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

**Última actualización:** 2026-06-04 11:00 | Farias llamado (CRM GVamax, software viejo alquileres = grieta) · Franco: entrega + cobro 05/06 · Semáforo 🟡 (mañana → 🟠) | Model: MiniMax-M3

---

## Semáforo
🟡 Supervivencia — Gap mayo: –$333. **Mañana 05/06: $300 USD a cobrar de Franco Roma** (entrega producto + cobro). Si entra → gap –$33, semáforo a 🟠. Meta junio: **$600 USD**. Faltan $300 después de Franco.

---

## Pipeline activo
- **Franco Roma — Roggero & Roma** 🟢 04/06 → 05/06: credenciales admin en armado. **Entrega + cobro $300 USD mañana 05/06**. Total $500.
- **Luis Farias — Farias & Asociados** 🆕 04/06: llamada WA desde personal. CRM = **GVamax** (https://landing.gvamax.com.ar). Web actual "tipo clásica". **Grieta detectada: alquileres con software viejo fuera del CRM.** Link roggeroyroma.com enviado, esperando reacción. NO perseguir.
- **GAMA Inmobiliaria** (Mar del Plata) 🆕 04/06 — 4.5⭐ (108 reseñas) · tel 0223 633-7766 · Lead prioritario post-Franco
- **Conforti Propiedades** (Villa Carlos Paz) 🆕 04/06 — 4.5⭐ (53 reseñas) · tel 03541 67-5105
- **RIVAS Inmuebles** (CABA) 🆕 04/06 — 4.9⭐ (1 reseña) · tel 011 6827-4827
- Ann: Pitch enviado — seguimiento pendiente
- ~~Comforti/Rivas/Gamma: bloqueados por falta de datos~~ ✅ RESUELTO 04/06 vía Serper

## Korantis — STANDBY
Regla activa: no se toca con semáforo 🔴/🟡. Hoy (🟡) Juan intentó reactivar trabajo en Korantis dos veces. Frenado. Solo se reactiva cuando Wolfim llegue a 🟠 o superior **Y Juan confirma explícitamente "OK, arranco Korantis"**. No se activa por inferencia ni por impulso.

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
1. **Franco: ¿cobró los $300 el 05/06?** Si sí → semáforo a 🟠 → activar lead #1 (GAMA/Conforti/RIVAS).
2. **Farias: ¿respondió al link de Roggero y Roma?** Si en 48h sin respuesta → soltar.
3. ¿Ataco Ango o Construvial cuando llegue a 🟠? (regla SOUL: secundaria solo desde 🟠, ya permitido si se llega)

---

## Model
- **Activo:** MiniMax-M3
- **Provider:** minimax
- **Anterior:** minimax-2.7 (cambiado 02/06/2026 a pedido Juan)
- **⚠️ Cambio aplica al próximo /reset** (no mid-session para preservar prompt cache)

---

## Construvial — Plan 3 fases activo (STANDBY por semáforo 🟡)
- 21 empresas en DB: leads_oil_gas_mining.csv
- Top contactos: CISA (Neuquén), Sigma SA (SJ), Dumandzic (SJ/CAT), CASEMICA (CAT)
- Solo investigación — sin outreach hasta activación explícita de Juan
- PROPUESTA ENVIADA 19/05: Propuesta_Construvial_Wolfim_2026.pdf
- 🆕 **05/06: Viaje a AgroActiva con Construvial (viernes 06/06)** — oportunidad de networking oil&gas/mining en persona

---

## Historial financiero mayo 2026

| Fecha | Ingreso | Detalle |
|-------|---------|---------|
| 02/05 | $200 | Franco Roma — adelantados |
| 10/05 | $225 USD | Construvial — cobrado |
| 14/05 | $142 USD | Construvial — viáticos Catamarca |
| 27/05 (esperado, NO cerrado) | $0 | Cristina Welldone SRL — FALLÓ |

**Total mayo real:** $567 ingresados / $900 gastos = Gap **–$333**

## Historial financiero junio 2026

| Fecha | Ingreso | Detalle |
|-------|---------|---------|
| 05/06 (esperado) | $300 USD | Franco Roma — Roggero & Roma (entrega + cobro) |

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

## Correcciones aprendidas (2026-06-04, vigentes)
- **Leads en pausa deben verificarse al inicio de sesión** — el vault puede tener datos desactualizados. Farias "volvía en julio" según 5 sesiones, en realidad volvió 30/05. Confiar pero verificar.
- **Mockups AI no reemplazan una venta concreta.** El link de un producto terminado (roggeroyroma.com) pesa más que cualquier mockup FLOW. Mostrar producto > mostrar idea.
- **Link WhatsApp con preview automático** — pegar URL directo, no compartir desde navegador. Menos ruido, menos riesgo de enviar otra cosa.
- **Farias oportunidad real: software viejo de alquileres fuera del CRM.** Web no es lead. Alquileres sí.

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
