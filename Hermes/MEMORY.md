---
owner: brain-vps
last-reviewed: 2026-08-27
confidence: medium
status: active
source: mixed
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-08-27 10:05 ART | **Semáforo no confirmable: KPIs formales incompletos** · `cron_campaign.py` ejecutado y verificado: cola agotada (107 registros: 97 sent, 10 bounced, 0 failed, 0 pendientes componibles) · briefing vigente vencido · Prioridad comercial Wolfim: reabastecer Web Viejas o pausar canal y mover foco a follow-up/cierre real.

---

## Semáforo financiero

- Estado operativo previo registrado: 🟢 ESCALA — junio cerró con Wolfim $1.000 USD + Ango $333 USD = $1.333 USD.
- Advertencia activa: `Hermes/Intelligence/kpis.md` sigue vencido desde 2026-06-25 y sin números formales de Juan. No se puede confirmar el semáforo real.
- Regla prudente mientras no haya update formal: Wolfim prioritaria. Ango secundaria solo por estado previo. Construvial y Korantis no desplazan revenue Wolfim.
- Briefing vigente también está vencido; no hay autorización fresca para cambiar prioridades.

---

## Wolfim — Web Viejas / Email Outreach

**Estado:** ✅ El cron funciona, pero **la cola sigue agotada**.

### Pipeline
```text
dork_scout → wa_checker → enrich_leads → campaign.py / cron_campaign.py → cron diario
```

### Resultado latest — 2026-08-27
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Salida real: `✅ Todos los leads han sido enviados. No hay más pendientes.`
- Verificación tracker: 107 registros totales, 97 `sent`, 10 `bounced`, 0 `failed`, 0 pendientes componibles.
- Verificación inventario: 121 leads fuente; 107 cubiertos por `sent`/`bounced`; 19 no componibles por reglas del script; 0 candidatos para próxima tanda.
- Riesgo inmediato: seguir corriendo sin inventario no genera oportunidad comercial nueva.

### Corrida histórica breve
- 08/27: cola agotada; 107 registros totales, 0 pendientes componibles; sin error nuevo visible en stdout.
- 08/26: cola agotada; 107 registros totales, 0 pendientes componibles; sin error nuevo visible en stdout.
- 08/25: cola agotada; 107 registros totales, 0 pendientes componibles; sin error nuevo visible en stdout.
- 08/24: cola agotada; 107 registros totales, 0 pendientes componibles; sin error nuevo visible en stdout.
- 08/22: cola agotada; 107 registros totales, 0 pendientes componibles; sin error nuevo visible en stdout.
- 08/20: cola agotada; 107 registros totales, 0 pendientes; sin error nuevo visible en stdout.
- 08/14 y anteriores: canal llegó gradualmente a cola agotada; última tanda útil registrada 07/12 con 2 enviados.

### Configuración conocida
- Remitente: `Juan Gomariz <juan@wolfim.com>`; reply-to `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com`.
- API: Resend (`[credencial: wolfim-outreach]`); logo `assets.wolfim.com/v2.svg`.
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18.
- Documentación: `Hermes/Projects/web-viejas-pipeline.md`.

---

## Pipeline comercial activo

- Franco Roma — Roggero & Roma ✅ cerrado/cobrado. Backup VPS operativo. Publicación/DNS dependen de Juan/NIC.
- Víctor Abrile ✅ cobrado: $450 USD total.
- Luis Farias — Farias & Asociados 🔴 propuesta portal inmobiliario premium USD 450 + USD 25/mes lista para revisión/envío. Si avanza, 50% inicial = USD 225.
- GAMA Inmobiliaria ❌ caído: sin respuesta.
- Conforti Propiedades, RIVAS Inmuebles y Ann 🆕 seguimiento pendiente.

**Patrón vigente:** Juan construye bien; el cuello de botella sigue siendo cerrar ventas. Si pasan 3+ días sin follow-up a leads, activar anti-parálisis comercial.

---

## Empresas

- Wolfim: foco principal mientras KPIs formales sigan vencidos. Web Viejas sin inventario; prioridad real es seguimiento/cierre.
- Ango: junio $333 cobrados. MONTECOR pagar importación sigue pendiente. Handoffs locales de landing/medición/Ads siguen sin cierre visible.
- Korantis: sin revenue; modo evidencia + scout. No desplazar a Wolfim.
- Construvial: cobro puntual 2026-08-05: USD 180 por catálogos Construvial Rental + PRESOL. Standby comercial; no activar trabajo nuevo sin aprobación explícita de Juan.
- Almas Libres: profile activo; `HO-2026-08-03-001` pide MVP institucional + padrinazgo equino en preview, sin publicación hasta validar datos y activos.

---

## Handoffs / coordinación

- `local-to-vps`: `HO-2026-06-26-001` acknowledged; administrativamente archivable.
- `vps-to-local` activos/vencidos principales:
  - `HO-2026-08-03-002` — Wolfim Motors Demo, high, vencido, sin response visible.
  - `HO-2026-08-03-001` — Almas Libres MVP, normal, vencido.
  - `HO-2026-07-13-001` — Sync V6 profiles locales, high, vencido.
  - `HO-2026-07-16-001`, `HO-2026-07-22-001`, `HO-2026-07-24-001`, `HO-2026-07-27-001` — ANGO web/Ads, high, vencidos o sin cierre formal visible.
- `Memory/pending`: `2026-07-12-sync-v6-architecture-update.md` y `2026-07-24-jobseeker-profile.md` esperan consolidación / decisión de Juan.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar inventario real al inicio; el vault puede quedar más optimista que la cola real.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- Catálogo Rental Construvial: conservar diseño inicial oscuro/amarillo; optimizar ocupación vertical; usar descripción técnica legible; replicar ítems de Milicic; usar isotipo C delineado como patrón.
- Recibos Wolfim: usar diseño fijo existente; no improvisar layouts nuevos ni variantes genéricas.
- No escribir secrets, tokens ni API keys en el vault.
