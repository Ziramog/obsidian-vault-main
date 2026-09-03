---
owner: brain-vps
last-reviewed: 2026-09-01
confidence: medium
status: active
source: mixed
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-09-02 23:58 ART | **Semáforo no confirmable: KPIs formales incompletos** · Web Viejas sigue agotado (121 leads fuente; tracker 107 registros: 97 `sent`, 10 `bounced`, 0 `failed`, 0 pendientes componibles; 19 no componibles) · 113 leads inmobiliarios 31/08 listos para outreach manual · recibo Víctor Abrile ARS 178.860 pendiente de cobro · Construvial/PRESOL activó campaña de campo 2 semanas con auto + viáticos + fijo, monto/condición no registrados · briefing vigente vencido.

---

## Semáforo financiero

- Estado operativo histórico registrado: 🟢 ESCALA — junio cerró con Wolfim $1.000 USD + Ango $333 USD = $1.333 USD.
- Advertencia activa: `Hermes/Intelligence/kpis.md` sigue vencido desde 2026-06-25 y sin números formales de Juan. No se puede confirmar el semáforo real de septiembre.
- Regla prudente mientras no haya update formal: Wolfim prioritaria. Construvial/PRESOL solo como excepción por mandato documentado; no debe desplazar cierres Wolfim.
- Briefing vigente también está vencido; no hay autorización fresca para cambiar prioridades globales.

---

## Wolfim — Web Viejas / Email Outreach

**Estado:** ✅ El cron funciona, pero **la cola sigue agotada**. Última corrida verificada: 2026-09-02 10:02 ART.

### Pipeline
```text
dork_scout → wa_checker → enrich_leads → campaign.py / cron_campaign.py → cron diario
```

### Resultado latest — 2026-09-02
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Salida real: `✅ Todos los leads han sido enviados. No hay más pendientes.`
- Verificación tracker conocida: 121 leads fuente; 107 registros en tracker, 97 `sent`, 10 `bounced`, 0 `failed`.
- Verificación inventario: 107 cubiertos por `sent`/`bounced`; 19 no componibles por reglas del script; 0 candidatos para próxima tanda.
- Riesgo inmediato: seguir corriendo sin inventario no genera oportunidad comercial nueva.

### Corrida histórica breve
- 09/02: cola agotada; 0 pendientes; cron_campaign.py OK (`Todos los leads han sido enviados`).
- 09/01: cola agotada; 0 pendientes; check-replies 10/14/18: `Sin novedades`.
- 08/31: cola agotada; 107 registros totales, 0 pendientes componibles; sin error visible en stdout.
- 08/30: cola agotada; 107 registros totales, 0 pendientes componibles; sin error visible en stdout.
- 08/29 y anteriores: canal llegó gradualmente a cola agotada; última tanda útil registrada 07/12 con 2 enviados.

### Configuración conocida
- Remitente: `Juan Gomariz <juan@wolfim.com>`; reply-to `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com`.
- API: Resend (`[credencial: wolfim-outreach]`); logo `assets.wolfim.com/v2.svg`.
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18.
- Documentación: `Hermes/Projects/web-viejas-pipeline.md`.

---

## Pipeline comercial activo

- Franco Roma — Roggero & Roma ✅ cerrado/cobrado. Backup VPS operativo. Publicación/DNS dependen de Juan/NIC.
- Víctor Abrile ✅ histórico cobrado: $450 USD total. Además, 2026-08-31 quedó emitido recibo `REC-WF-2026-08-31-VICTOR-001` por ARS 178.860, pendiente de cobro.
- Luis Farias — Farias & Asociados 🔴 propuesta portal inmobiliario premium lista; requiere follow-up humano/anticipo.
- Madelen — Suelo Argentino 🔴 analizando propuesta desde 31/08; requiere follow-up si no vuelve.
- GAMA Inmobiliaria ❌ caído: sin respuesta.
- Conforti Propiedades, RIVAS Inmuebles y Ann 🆕 seguimiento pendiente.
- Inventario Wolfim 2026-08-31 para outreach manual inmobiliario: Mar del Plata 49 leads (24 WhatsApp confirmados), Pinamar 34 (18), Villa Gesell 30 (17). Total: 113 leads, 59 WA confirmados.
- Raypac / Leonardo Gastager 🟡 inbox 2026-09-01: cotización kit cámara 360° por USD 14.750 + IVA; requiere decisión de seguimiento.

**Patrón vigente:** Juan construye bien; el cuello de botella sigue siendo cerrar ventas. Si pasan 3+ días sin follow-up a leads, activar anti-parálisis comercial.

---

## Empresas

- Wolfim: foco principal mientras KPIs formales sigan vencidos. Web Viejas sin inventario; prioridad real es seguimiento/cierre.
- Ango: junio $333 cobrados. MONTECOR pagar importación sigue pendiente. Handoffs locales de landing/medición/Ads siguen sin cierre visible.
- Construvial: PRESOL pasó a **campaña activa** 2026-09-01: Juan tiene campaña de campo 2 semanas (auto + viáticos + fijo) para logística/cargas pesadas en corredores Río Tercero→Río Cuarto/Villa María/Córdoba. Paquete creado: plan, oferta, ficha, WhatsApp, planilla, paquete dirección/campo ampliado a 117 empresas (44 clase A, 73 teléfonos OK) + PDF final 35 páginas. Falta registrar monto/condición de pago y cerrar tarifa base/km, mínima, hora hidrogrúa, responsable WhatsApp y alcance áridos/volcador.
- Korantis: sin revenue; modo evidencia + scout. No desplazar a Wolfim.
- Almas Libres: profile activo; `HO-2026-08-03-001` pide MVP institucional + padrinazgo equino en preview, sin publicación hasta validar datos y activos.

---

## Handoffs / coordinación

- `local-to-vps`: `HO-2026-06-26-001` acknowledged; administrativamente archivable.
- `vps-to-local` activos/vencidos principales: `HO-2026-08-03-002` Wolfim Motors Demo (high); `HO-2026-08-03-001` Almas Libres MVP; `HO-2026-07-13-001` Sync V6 profiles locales; `HO-2026-07-16-001`, `HO-2026-07-22-001`, `HO-2026-07-24-001`, `HO-2026-07-27-001` ANGO.
- `Memory/pending`: `2026-07-12-sync-v6-architecture-update.md` y `2026-07-24-jobseeker-profile.md` esperan consolidación / decisión de Juan.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar inventario real al inicio; el vault puede quedar más optimista que la cola real.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- Recibos Wolfim: usar diseño fijo existente; no improvisar layouts nuevos ni variantes genéricas.
- No escribir secrets, tokens ni API keys en el vault.
