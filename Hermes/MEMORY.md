---
owner: brain-vps
last-reviewed: 2026-07-09
confidence: medium
status: active
source: cron_campaign_run
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-07-09 10:03 ART | **🟢 ESCALA según memoria previa / KPIs formales incompletos** · Campaña Web Viejas: +5 emails enviados hoy, 0 fallos · Drive NO actualizado por `invalid_grant` (token expirado/revocado) · Prioridad comercial: vender Wolfim.

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

### Resultado latest — 2026-07-09
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Emails enviados: **5**
- Fallos de envío: **0**
- Leads enviados:
  - `dejesusconstructora.com.ar` → `admin@dejesusconstructora.com.ar`
  - `spmcba.com.ar` → `sociedadpatologiamamaria@gmail.com`
  - `fejeproc.com.ar` → `adm.fejeproc@gmail.com`
  - `omer.com.ar` → `contact@goodlayers.com`
  - `atmzavaleta.com.ar` → `4963-86662emailatmzavaleta@gmail.com`
- Pendientes estimados: **~12 leads**
- Incidente persistente: Drive no actualizado por token Google expirado/revocado: `invalid_grant: Token has been expired or revoked.`
- Alerta calidad: dos destinos parecen dudosos (`contact@goodlayers.com` y email malformado de atmzavaleta). Antes de escalar volumen, auditar/sanitizar enriquecimiento.

### Resultados anteriores registrados
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

- `local-to-vps`: `HO-2026-06-26-001` pendiente de revisar.
- `vps-to-local`: `HO-2026-06-25-001`, `HO-2026-06-27-001`, `HO-2026-06-30-001`, `HO-2026-07-06-001` activos.
- `Memory/pending`: vacío al abrir 2026-07-09.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar al inicio de sesión; vault puede estar desactualizado.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- No escribir secrets, tokens ni API keys en el vault.
