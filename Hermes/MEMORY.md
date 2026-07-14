---
owner: brain-vps
last-reviewed: 2026-07-12
confidence: medium
status: active
source: mixed
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-07-14 10:02 ART | **Semáforo no confirmable: KPIs formales incompletos** · Web Viejas ejecutado sin envíos: cola agotada (0 leads pendientes) · Luis Farias sigue como propuesta premium USD 450 lista para revisión/envío · Prioridad comercial: enviar propuesta Farias + reabastecer Wolfim si la campaña continúa.

---

## Semáforo financiero

- **Estado operativo previo:** 🟢 ESCALA — junio cerró con Wolfim $1.000 USD + Ango $333 USD = $1.333 USD.
- **Advertencia:** `Hermes/Intelligence/kpis.md` sigue sin números formales de Juan y está vencido desde 2026-06-25. Confianza media hasta actualización.
- **Regla activa:** Wolfim prioritaria. Ango secundaria habilitada por semáforo previo; Construvial en standby salvo aprobación explícita.

---

## Wolfim — Web Viejas / Email Outreach

**Estado:** ✅ En producción con cron diario.

### Pipeline
```text
dork_scout → wa_checker → enrich_leads → campaign.py / cron_campaign.py → cron diario
```

### Resultado latest — 2026-07-14
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Resultado: **Todos los leads han sido enviados. No hay más pendientes.**
- Emails enviados: **0**
- Fallos de envío: **0**
- Pendientes estimados: **0 leads**
- Incidente persistente conocido: Drive no actualizado por token Google inválido/revocado: `invalid_grant: Bad Request`.
- Riesgo inmediato: la cola está agotada; el cron no sostendrá nuevas tandas sin reabastecimiento y sanitización.

### Resultados anteriores registrados
- 07/12: 2 enviados, 0 fallaron; cola quedó ~0 leads; Drive `invalid_grant`.
- 07/11: 5 enviados, 0 fallaron; quedaban ~2 leads; Drive `invalid_grant`.
- 07/10: 5 enviados, 0 fallaron; quedaban ~7 leads; Drive `invalid_grant`.
- 07/09: 5 enviados, 0 fallaron; quedaban ~12 leads; Drive `invalid_grant`.
- 07/08: 5 enviados, 0 fallaron; quedaban ~17 leads; Drive `invalid_grant`.
- 07/07: 5 enviados, 0 fallaron; quedaban ~22 leads; Drive `invalid_grant`.
- 29/06: campaña registrada en 61/122 enviados, 0 respuestas.
- 21/06: 20 enviados, 19 entregados, 1 bounce.

### Configuración conocida
- Remitente: `Juan Gomariz <juan@wolfim.com>`; reply-to `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com`.
- API: Resend (`[credencial: wolfim-outreach]`); logo `assets.wolfim.com/v2.svg`.
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18.
- Documentación: `Hermes/Projects/web-viejas-pipeline.md`.

---

## Pipeline comercial activo

- **Franco Roma — Roggero & Roma** ✅ Cerrado/cobrado. Backup VPS operativo.
- **Víctor Abrile** ✅ Cobrado: $450 USD total.
- **Luis Farias — Farias & Asociados** 🔴 Reactivado: propuesta portal inmobiliario premium USD 450 + USD 25/mes posterior lista para revisión/envío; si avanza, 50% inicial = USD 225.
- **GAMA Inmobiliaria** ❌ Caído: sin respuesta.
- **Conforti Propiedades** 🆕 Seguimiento pendiente.
- **RIVAS Inmuebles** 🆕 Seguimiento pendiente.
- **Ann** Seguimiento pendiente.

**Patrón vigente:** Juan construye bien; el cuello de botella sigue siendo cerrar ventas. Si pasan 3+ días sin follow-up a leads, activar anti-parálisis comercial.

---

## Empresas

- **Ango:** junio $333 cobrados. Pendiente vencido 2026-07-08: MONTECOR pagar importación.
- **Korantis:** sin revenue; modo evidencia + scout. No desplazar a Wolfim.
- **Construvial:** standby. No activar sin aprobación explícita de Juan.

---

## Handoffs / coordinación

- `local-to-vps`: `HO-2026-06-26-001` ya tiene `response.md` acknowledged; revisar si debe archivarse.
- `vps-to-local`: `HO-2026-06-30-001` y `HO-2026-07-06-001` cancelados por Juan el 2026-07-13 para frenar alertas repetidas de handoffs high vencidos; revisar `HO-2026-06-25-001` y `HO-2026-06-27-001` si corresponde archivar.
- `HO-2026-07-12-001` done: profile local `trading-performance` creado y probado; trading manual, sin gateway/cron ni ejecución automática.
- `HO-2026-07-12-002` done: Sync V6 local implementado con Git Bash + Windows Task Scheduler + `brain-local-sync`.
- Sync V6 VPS y local operativos: procesos independientes cada 2 minutos; estado VPS final `dirty=0 ahead=0 behind=0`; ver `Hermes/Systems/vps/sync-v6.md` y `Hermes/Systems/local/sync-v6/README.md`.
- `Memory/pending`: `2026-07-12-sync-v6-architecture-update.md` espera consolidación de Juan porque `ARCHITECTURE.md` es zona exclusiva de Config.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar al inicio de sesión; vault puede estar desactualizado.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- No escribir secrets, tokens ni API keys en el vault.
