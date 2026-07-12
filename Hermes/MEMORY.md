---
owner: brain-vps
last-reviewed: 2026-07-12
confidence: medium
status: active
source: mixed
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-07-12 20:49 ART | **Semáforo no confirmable: KPIs formales incompletos** · Sync V6 VPS operativo cada 2 minutos · PC local pendiente de automatización por handoff high · Prioridad comercial: reabastecer y vender Wolfim.

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

### Resultado latest — 2026-07-12
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Emails enviados: **2**
- Fallos de envío: **0**
- Leads enviados:
  - `condiser.com.ar` → `info@condiser.com.ar`
  - `conc.com.ar` → `428428circulodelnorte@gmail.com`
- Pendientes estimados: **~0 leads**
- Incidente persistente: Drive no actualizado por token Google inválido/revocado: `invalid_grant: Bad Request`.
- Riesgo inmediato: la cola quedó agotada; el cron no podrá sostener nuevas tandas sin reabastecimiento y sanitización.

### Resultados anteriores registrados
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
- **Luis Farias — Farias & Asociados** ⏸️ No perseguir por grieta operativa.
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
- `vps-to-local`: `HO-2026-06-25-001`, `HO-2026-06-27-001`, `HO-2026-06-30-001`, `HO-2026-07-06-001` visibles; varios vencidos según metadata.
- `HO-2026-07-12-001` ready: brain-local debe crear profile local `trading-performance`, sin ejecución automática ni credenciales financieras.
- `HO-2026-07-12-002` high/ready: brain-local → pc-ops debe implementar Sync V6 local, Task Scheduler y freshness gate antes de leer handoffs.
- Sync V6 VPS operativo: proceso independiente cada 2 minutos, lock, retry, segundo pull, logs en `~/.hermes/logs/`; ver `Hermes/Systems/vps/sync-v6.md`.
- `Memory/pending`: vacío al abrir 2026-07-10.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar al inicio de sesión; vault puede estar desactualizado.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- No escribir secrets, tokens ni API keys en el vault.
