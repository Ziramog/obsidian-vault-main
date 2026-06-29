---
owner: brain-vps
last-reviewed: 2026-06-29
confidence: high
status: active
source: consolidation
---

# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

**Última actualización:** 2026-06-27 (sábado) | **🟢 ESCALA** · Campaña Web Viejas: tanda cron ejecutada 10:00, 5 enviados, 0 fallaron · Quedan ~57 leads · Drive actualizado ✅ · Junio Wolfim: $1.000 USD completo ✅

---

## Proyecto: Web Viejas — Lead Generation + Email Outreach

**Estado:** ✅ En producción — 20 leads enviados día 1, pipeline automático diario

### Pipeline

```
dork_scout → wa_checker → enrich_leads → campaign.py → cron 10/día
```

### Resultados 21/06
- Tanda 1: 10 enviados, 9 entregados, 1 bounce
- Tanda 2: 10 enviados, 10 entregados
- Quedan ~28 leads para próximas tandas

### Resultados 27/06 — cron_campaign.py
- Tanda cron 10:00 ART: 5 enviados, 0 fallaron
- Enviados: minervinosa.com.ar, dmya.com.ar, cacec.com.ar, ghgestudio.com.ar, tufrocar.com.ar
- Quedan ~57 leads pendientes
- Drive actualizado: https://drive.google.com/file/d/1BoekbRSXeAp2ljgnwTeH84yYix-AUxml/view?usp=drivesdk

### Configuración
- Remitente: `Juan Gomariz <juan@wolfim.com>`
- Reply-to: `juan@wolfim.com` → Cloudflare → ingjuangomariz@gmail.com
- API: Resend (key: wolfim-outreach)
- Logo: assets.wolfim.com/v2.svg
- SPF/DKIM/DMARC/BIMI: ✅ configurado
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18

### Documentación completa
→ `Hermes/Projects/web-viejas-pipeline.md`

---

## Semáforo
🟢 **ESCALA** — Junio Wolfim cerrado: $1.000. Total junio: $1.333 (Wolfim $1.000 + Ango $333). Wolfim prioritaria. Tres empresas habilitadas en paralelo.

---

## Pipeline activo
- **Franco Roma — Roggero & Roma** ✅ CERRADO — Total $750 USD cobrados. Operación completa. Backup VPS operativo (cron semanal sábados 10 AM).
- **Víctor Abrile** ✅ COBRADO — $250 USD cobrado (23/06). Adelanto $200 (10/06). Total $450 USD. Catálogo completo.
- **Luis Farias — Farias & Asociados** ⏸️ Grieta: alquileres con software viejo fuera del CRM. Link roggeroyroma.com enviado. NO perseguir.
- **GAMA Inmobiliaria** (MdP) ❌ LEAD CAÍDO — 4.5⭐ 108 reseñas. Sin respuesta.
- **Conforti Propiedades** (Villa Carlos Paz) 🆕 — 4.5⭐ 53 reseñas · tel 03541 67-5105
- **RIVAS Inmuebles** (CABA) 🆕 — 4.9⭐ · tel 011 6827-4827
- **Ann** — Pitch enviado, seguimiento pendiente

---

## Historial financiero junio 2026

| Fecha | Ingreso | Detalle |
|-------|---------|---------|
| 06/06 ✅ | $300 | Franco Roma — cierre página |
| 08/06 ✅ | $250 | Franco Roma — mantenimiento anual |
| 10/06 ✅ | $200 | Víctor Abrile — Adelanto catálogo |
| 23/06 ✅ | $250 | Víctor Abrile — Saldo catálogo |

**Cobrado a hoy (25/06):** **$1.000 Wolfim + $333 Ango = $1.333**
**Junio Wolfim cerrado: $1.000 USD.**

---

## Ango — Metalúrgica (Padre de Juan)

| Fecha | Ingreso | Detalle |
|---|---|---|
| 19/06 ✅ | $333 | Primera entrada — operación padre |

**Nota:** Ango activada con semáforo 🟢. Sin pipeline de clientes propios aún.

---

## Hito China — octubre 2026
- Meta: > $1.000 USD/mes con operación autónoma
- **Días restantes:** ~109
- **Estado:** 🟢 En curso. **Wolfim $1.000 USD junio ALCANZADO ✅.** Ango primera entrada $333. Meta $1.000/mes cumplida.

---

## Korantis
Empresa propia (no proyecto Wolfim). Dominio: korantis.com. Sin clientes ni revenue. Modo evidencia + scout. Scout batch 01 ejecutado (25 BA venues). Model split validado (M2.7 text → M3 vision).

---

## Construvial — STANDBY
21 empresas en DB. Propuesta enviada 19/05. Solo investigación hasta activación explícita.

---

## Modo
Ejecución

---

## Correcciones aprendidas (vigentes)
- Leads en pausa: verificar al inicio de sesión — vault puede estar desactualizado
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea
- No cuestionar decisión comercial de Juan — ayudar a redactar, no revisar el fondo
- Datos de pago: Juan los pasa al cliente, no al revés
- No decir "listo" sin verificar (`ls` + `git log` + `diff` antes de confirmar cierre)

---

## Credenciales y API keys
- Estado: `~/.hermes/private/keys-status.md` (modo 600)
- Valores: `~/.hermes/.env` (modo 600)

---

## Referencias
- [[companies/wolfim/Clientes/franco-roma|Franco Roma]]
- [[companies/wolfim/Clientes/luis-farias|Luis Farias]]
- [[companies/korantis|Korantis]]
- [[companies/construvial|Construvial]]
- [[companies/ango|Ango]]
