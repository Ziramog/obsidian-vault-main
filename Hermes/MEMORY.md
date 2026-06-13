# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

**Última actualización:** 2026-06-13 | **🟠 TRANSICIÓN** · Gap junio parcial **+$550** (Franco $300 06/06 + $250 08/06) · Meta $600 faltan $50 · **Víctor catálogo $300 + mensual $150** acuerdos verbales (sin fecha, sin upfront, pago contra entrega) · **Agenda persistente** activa 2026-06-10 con 6 tareas · **ROGGERO BACKP SUSPENDIDO** (10/06) — todo armado en /home/hermes/roggero_backup/ pero SIN cron, retomar a fin de mes · ⚠️ **13/06 11:00 UTC: morning-report.py falló al enviar Telegram — HTTP 401. Token en `~/.hermes/config.yaml` está truncado (`8644817415:AAFHwgOg` — solo 9 chars post-colon, debería ser ~46).** | Model: MiniMax-M3

---

## Sesión 07/06 — Investigación Ango v2 (patentes rotativas)

**Trigger:** Juan pidió ampliar el informe de patentes de sistemas de corte para cosechadoras soja/trigo del 02/06 — específicamente enfocado en **disco rotativo / cuchilla rotativa** (no sickle bar). Objetivo: "tener información detallada para saber si existen antecedentes".

**Acción ejecutada:**
- Búsqueda en 5 bases (USPTO, CIPO, EPO, CNIPA, INPI AR).
- Identificadas 20+ patentes nuevas NO cubiertas en v1.
- **Hallazgo crítico:** familia MacDon US 7,340,876 → US 11,160,206 (13+ patentes vigentes, 2007-2021). Cubre disco + impeller/auger/rock-guard/drive. Barrera dominante en EE.UU./Canadá.
- INPI Argentina: **no hay patentes locales** en este dominio. Ventana abierta para Ango.
- Descarga PDFs USPTO: **bloqueada** desde VPS (403 Forbidden). Documentadas URLs para descarga local.

**Informe entregado:** `companies/ango/research/patentes-rotativas-global-2026-06-07.md` (29.8 KB, 10 secciones, links a 20+ patentes nuevas).

**Veredicto FTO incluido en §5 del informe:**
- Argentina: ✅ libertad razonable si Ango evita impellers + auger integrado.
- EE.UU./Canadá: ❌ barrera alta — 3-4 patentes MacDon activas simultáneas en cualquier diseño con disco+impeller.

**Pendiente próximo (si Juan confirma):**
- FTO análisis con agente INPI registrado (no se puede hacer con búsquedas web).
- Investigación del "diseño argentino" del Instagram 2019 ("Reducir pérdidas en soja es posible").

---

## Semáforo
🟠 **TRANSICIÓN** — Gap mayo: –$333 (cerrado). **Cobro $300 USD Franco Roma CONFIRMADO 06/06** ✅. Gap junio parcial: +$300. **Meta junio: $600 USD → faltan $300.** Empresa prioritaria: Wolfim. **Secundarias desbloqueadas** (Ango/Construvial) con asignación de tiempo explícita. Korantis: evidence-gathering sigue permitido.

---

## Pipeline activo
- **Franco Roma — Roggero & Roma** ✅✅ **OPERACIÓN COMPLETA** — Total $750 USD cobrados: $200 adelantados page + $300 cierre page (06/06) + $250 mantenimiento anual (08/06). Cerrado.
- **Víctor Abrile** 🆕 09/06 — Acuerdo verbal: catálogo de venta de terrenos $300 USD + servicio mensual publicar/publicidad $150 USD/mes. **SIN fecha de inicio ni cobro.** Requiere: definir kickoff + factura upfront antes de empezar trabajo.
- **Luis Farias — Farias & Asociados** 🆕 04/06: llamada WA desde personal. CRM = **GVamax** (https://landing.gvamax.com.ar). Web actual "tipo clásica". **Grieta detectada: alquileres con software viejo fuera del CRM.** Link roggeroyroma.com enviado, esperando reacción. NO perseguir.
- **GAMA Inmobiliaria** (Mar del Plata) 🆕 04/06 — 4.5⭐ (108 reseñas) · tel 0223 633-7766 · Lead prioritario post-Franco
- **Conforti Propiedades** (Villa Carlos Paz) 🆕 04/06 — 4.5⭐ (53 reseñas) · tel 03541 67-5105
- **RIVAS Inmuebles** (CABA) 🆕 04/06 — 4.9⭐ (1 reseña) · tel 011 6827-4827
- Ann: Pitch enviado — seguimiento pendiente
- ~~Comforti/Rivas/Gamma: bloqueados por falta de datos~~ ✅ RESUELTO 04/06 vía Serper

## Korantis — ahora empresa propia (no proyecto Wolfim)
**2026-06-05: Juan reasignó Korantis a su propia carpeta `companies/korantis/`** (antes vivía como `projects/korantis/` bajo Wolfim). Dominio real: **korantis.com** (no Corantis.com). Status: sin clientes ni revenue; modo evidencia.

**Scout batch 01 ejecutado 2026-06-05:** 25 BA venues, JSON 177.8 KB con 56 image candidates. Top HERO: Ninina, Verne Club, Milion, Oporto, Gran Bar Danzon, Don Julio, Niño Gordo, Uptown. `data/korantis_ba_hermes_soft_scout_batch_01_2026-06-05.json`

**Scraping policy registrada 2026-06-05:** curl plain como default, chrome solo si curl <500 bytes, no retries contra TA/IG, TMPDIR=/home/hermes/.chrome_tmp para chrome/playwright. Ver [[companies/korantis/scraping-policy|policy]] completa.

**Model split test ejecutado 2026-06-05 16:09:** Phase A (M2.7 text scout, 5 venues premium) → 42 prevision candidates reducidos a 9 vision queue (78% ahorro). Phase B (M3 vision) → 9/7 passed gate → 1 hero, 4 product, 2 marketing collage. **Veredicto honesto:** ahorra 83% de vision calls pero el cuello de botella real es source quality, no costo de modelo. Editorial sourcing (Michelin/50Best) es el próximo paso.

**Visual references 2026-06-05 16:11:** 9 imágenes de Ninina/Verne/Mishiguene descargadas a `companies/korantis/references/ba-venues/` (~2.7 MB, 767²–3063²). Material premium de sitios oficiales.

Regla activa: no se toca con semáforo 🔴/🟡. Hoy (🟡) Juan reactivó Korantis con un scout aislado (no es "trabajo comercial" en el sentido de la regla — es evidence-gathering sin outreach ni ventas). Si Juan pide presupuesto/marketing/outreach, frenar hasta 🟠.

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
1. ✅ Franco cobró $300 → semáforo 🟠. **Atacar lead #1 ahora: GAMA / Conforti / RIVAS — decisión de Juan.**
2. **Farias: ventana 48h vence HOY 06/06.** ¿Respondió al link? Si no → soltar, pasar a siguiente.
3. Korantis en sesión HOY: definir tarea concreta.

---

## Model
- **Activo:** minimax-2.7 (cambio 06/06 pedido Juan, efectivo próximo /reset)
- **Provider:** minimax
- **Anterior:** MiniMax-M3 (usado 02/06 → 06/06)
- **Regla:** swap automático a M3 en sesión para: redacción comercial, código, visión de imágenes, auditoría, decisiones irreversibles. M2.7 default para: scout masivo, clasificación, generación de variantes, tareas en pipeline. Veredicto split test 05/06: M2.7 hace text scout, M3 hace vision gate.
- ⚠️ Cambio aplica al próximo /reset (no mid-session para preservar prompt cache)

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
| 06/06 ✅ | $300 USD | Franco Roma — Roggero & Roma (cobro final page-job) |
| 08/06 ✅ | $250 USD | Franco Roma — mantenimiento anual (nuevo cobro, separado del page-job) |

**Total junio parcial: +$550** (meta $600 → faltan $50, casi cerrada). **Franco total acumulado operación: $750 USD** ($200 adelantados page + $300 cierre page + $250 mantenimiento anual).

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
- **Errores de pensamiento M3 (04/06, sesión Franco-mantenimiento):** NO cuestionar la decisión comercial de Juan. Cuando defina precio/estrategia, ayudar a redactar, no revisar el fondo. Costo $12/año sobre $300 de ingreso = margen enorme, $250 anual cobrados ya es buena decisión aunque represente descuento.
- **Datos de pago: YO se los paso al cliente, no al revés.** Regla simple: "te paso los datos de pago" en boca de Juan, "pasame datos para factura" en boca de Franco.
- **No mezclar conceptos en la misma frase.** $250 anual mantenimiento y $300 entrega son transacciones separadas, no se confunden.

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
