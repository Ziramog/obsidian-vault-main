---
owner: brain-vps
last-reviewed: 2026-07-21
confidence: medium
status: active
source: mixed
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-07-21 10:01 ART | **Semáforo no confirmable: KPIs formales incompletos** · `cron_campaign.py` volvió a correr con cola agotada (`✅ Todos los leads han sido enviados. No hay más pendientes.`) · Luis Farias sigue como propuesta premium lista para revisión/envío · Prioridad comercial: enviar propuesta Farias + decidir si Web Viejas se reabastece o se pausa.

---

## Semáforo financiero

- **Estado operativo previo registrado:** 🟢 ESCALA — junio cerró con Wolfim $1.000 USD + Ango $333 USD = $1.333 USD.
- **Advertencia activa:** `Hermes/Intelligence/kpis.md` sigue vencido desde 2026-06-25 y sin números formales de Juan. No se puede confirmar el semáforo real.
- **Regla activa mientras no haya update formal:** Wolfim prioritaria. Ango secundaria habilitada solo por el estado previo. Construvial sigue en standby.

---

## Wolfim — Web Viejas / Email Outreach

**Estado:** ✅ El cron funciona, pero **la cola sigue agotada**.

### Pipeline
```text
dork_scout → wa_checker → enrich_leads → campaign.py / cron_campaign.py → cron diario
```

### Resultado latest — 2026-07-21
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Salida real: `✅ Todos los leads han sido enviados. No hay más pendientes.`
- No apareció ningún error nuevo en stdout durante esta corrida.
- Riesgo inmediato: seguir corriendo sin inventario no genera oportunidad comercial nueva.

### Corrida histórica breve
- 07/21: cola agotada; sin error nuevo visible en stdout.
- 07/19: 0 enviados, 0 fallos; cola agotada.
- 07/16: 0 enviados, 0 fallos; cola agotada.
- 07/15: 0 enviados, 0 fallos; cola agotada.
- 07/14: 0 enviados, 0 fallos; cola agotada.
- 07/12: 2 enviados, 0 fallos; cola quedó en ~0; Drive `invalid_grant`.
- 07/11 a 07/07: tandas consecutivas de 5/día, 0 fallos; la limitación pasó a ser inventario + follow-up humano.

### Configuración conocida
- Remitente: `Juan Gomariz <juan@wolfim.com>`; reply-to `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com`.
- API: Resend (`[credencial: wolfim-outreach]`); logo `assets.wolfim.com/v2.svg`.
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18.
- Documentación: `Hermes/Projects/web-viejas-pipeline.md`.

---

## Pipeline comercial activo

- **Franco Roma — Roggero & Roma** ✅ Cerrado/cobrado. Backup VPS operativo. Publicación/DNS siguen dependiendo de Juan/NIC.
- **Víctor Abrile** ✅ Cobrado: $450 USD total.
- **Luis Farias — Farias & Asociados** 🔴 Reactivado: propuesta portal inmobiliario premium USD 450 + USD 25/mes lista para revisión/envío. Si avanza, 50% inicial = USD 225.
- **GAMA Inmobiliaria** ❌ Caído: sin respuesta.
- **Conforti Propiedades** 🆕 Seguimiento pendiente.
- **RIVAS Inmuebles** 🆕 Seguimiento pendiente.
- **Ann** Seguimiento pendiente.

**Patrón vigente:** Juan construye bien; el cuello de botella sigue siendo cerrar ventas. Si pasan 3+ días sin follow-up a leads, activar anti-parálisis comercial.

---

## Empresas

- **Ango:** junio $333 cobrados. Sigue pendiente de fondo: MONTECOR pagar importación. Handoff local `HO-2026-07-16-001` sigue sin ack visible y ya está vencido.
- **Korantis:** sin revenue; modo evidencia + scout. No desplazar a Wolfim.
- **Construvial:** standby. No activar sin aprobación explícita de Juan.

---

## Handoffs / coordinación

- `local-to-vps`: `HO-2026-06-26-001` acknowledged; administrativamente archivable.
- `vps-to-local` activos/vencidos:
  - `HO-2026-06-27-001` — ready, normal, sin cierre visible.
  - `HO-2026-07-13-001` — high, vencido, sin ack visible.
  - `HO-2026-07-16-001` — high, vencido, sin ack visible.
- `HO-2026-06-30-001` y `HO-2026-07-06-001` siguen cancelados por Juan.
- `HO-2026-07-12-001` y `HO-2026-07-12-002` done.
- `Memory/pending`: `2026-07-12-sync-v6-architecture-update.md` espera consolidación de Juan porque `ARCHITECTURE.md` es zona Config.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar inventario real al inicio; el vault puede quedar más optimista que la cola real.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- No escribir secrets, tokens ni API keys en el vault.
