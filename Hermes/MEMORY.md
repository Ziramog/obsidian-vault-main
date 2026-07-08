---
owner: brain-vps
last-reviewed: 2026-07-08
confidence: medium
status: active
source: cron_campaign_run
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-07-08 | **🟢 ESCALA según memoria previa / KPIs formales incompletos** · Campaña Web Viejas: +5 emails enviados hoy, 0 fallos · Drive NO actualizado por `invalid_grant` (token expirado/revocado) · Prioridad comercial: vender Wolfim.

---

## Semáforo financiero

- **Estado operativo previo:** 🟢 ESCALA — junio cerró con Wolfim $1.000 USD + Ango $333 USD = $1.333 USD.
- **Advertencia:** `Hermes/Intelligence/kpis.md` sigue sin números formales de Juan (ingresos/gastos/gap) y está vencido desde 2026-06-25. Confianza media hasta actualización.
- **Regla activa:** Wolfim sigue siendo empresa prioritaria. Ango secundaria habilitada por semáforo previo; Construvial en standby salvo aprobación explícita.

---

## Wolfim — Web Viejas / Email Outreach

**Estado:** ✅ En producción con cron diario.

### Pipeline
```text
dork_scout → wa_checker → enrich_leads → campaign.py / cron_campaign.py → cron diario
```

### Resultado latest — 2026-07-08
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Emails enviados: **5**
- Fallos de envío: **0**
- Leads enviados:
  - `amenabar.com.ar` → `info@amenabar.com.ar`
  - `nlcconsultores.com.ar` → `info@nlcconsultores.com.ar`
  - `estudiodafonseca.com.ar` → `info@estudiodafonseca.com.ar`
  - `dnb.com.ar` → `2000bnc@estudiobnc.com.ar`
  - `jorgearojas.com.ar` → `estudio@jorgearojas.com.ar`
- Pendientes estimados: **~17 leads**
- Incidente persistente: Drive no actualizado por token Google expirado/revocado: `invalid_grant: Token has been expired or revoked.`

### Resultados anteriores registrados
- 07/07: 5 enviados, 0 fallaron; quedaban ~22 leads; Drive `invalid_grant`.
- 21/06: 20 enviados, 19 entregados, 1 bounce.
- 27/06: 5 enviados, 0 fallaron; quedaban ~57 leads.
- 29/06: campaña registrada en 61/122 enviados, 0 respuestas.

### Configuración conocida
- Remitente: `Juan Gomariz <juan@wolfim.com>`
- Reply-to: `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com`
- API: Resend (`[credencial: wolfim-outreach]`)
- Logo: `assets.wolfim.com/v2.svg`
- SPF/DKIM/DMARC/BIMI: ✅ configurado
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18
- Documentación: `Hermes/Projects/web-viejas-pipeline.md`

---

## Pipeline comercial activo

- **Franco Roma — Roggero & Roma** ✅ Cerrado/cobrado. Backup VPS operativo (cron semanal sábados 10 AM). Origen: outreach WhatsApp.
- **Víctor Abrile** ✅ Cobrado: $450 USD total ($200 adelanto + $250 saldo).
- **Luis Farias — Farias & Asociados** ⏸️ No perseguir: grieta por alquileres con software viejo fuera del CRM.
- **GAMA Inmobiliaria** ❌ Caído: sin respuesta.
- **Conforti Propiedades** 🆕 Capturado, seguimiento pendiente.
- **RIVAS Inmuebles** 🆕 Capturado, seguimiento pendiente.
- **Ann** Seguimiento pendiente.

**Patrón vigente:** Juan construye bien; el cuello de botella sigue siendo cerrar ventas. Si pasan 3+ días sin follow-up a leads, activar anti-parálisis comercial.

---

## Empresas

### Ango
- Junio: $333 cobrados en operación padre.
- Agenda 2026-07-08 tiene pendiente 🔴: **ANGO, MONTECOR avisar de pagar importacion**.
- Activa como secundaria solo mientras Wolfim sostenga ingreso.

### Korantis
- Empresa propia sin revenue. Modo evidencia + scout. No desplazar a Wolfim.

### Construvial
- Standby. 21 empresas en DB. No activar sin aprobación explícita de Juan.

---

## Handoffs / coordinación

- `local-to-vps`: existe `HO-2026-06-26-001` para revisar.
- `vps-to-local` activos detectados: `HO-2026-06-25-001`, `HO-2026-06-27-001`, `HO-2026-06-30-001`, `HO-2026-07-06-001`.
- `Memory/pending`: vacío al abrir 2026-07-08.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar al inicio de sesión; vault puede estar desactualizado.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- No cuestionar decisión comercial de Juan: ayudar a redactar y cerrar.
- Datos de pago: Juan los pasa al cliente, no al revés.
- No escribir secrets, tokens ni API keys en el vault.
