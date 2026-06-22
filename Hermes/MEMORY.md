# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

**Última actualización:** 2026-06-22 (lunes) | **🟢 ESCALA** · Campaña Web Viejas activa ✅ · 20 leads enviados día 1 · Pipeline automático corriendo · Reply-to juan@wolfim.com → ingjuangomariz@gmail.com

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
🟢 **ESCALA** — Mayo cerrado: –$333. **Junio cobrado: $750, proyectado $1.000** (lunes 23/06). Wolfim prioritaria. Tres empresas habilitadas en paralelo.

---

## Pipeline activo
- **Franco Roma — Roggero & Roma** ✅ CERRADO — Total $750 USD cobrados. Operación completa. Backup VPS operativo (cron semanal sábados 10 AM).
- **Víctor Abrile** ⏳ PENDIENTE — $250 USD cobra lunes (23/06). Adelanto $200 cobrado (10/06).
- **Luis Farias — Farias & Asociados** ⏸️ Grieta: alquileres con software viejo fuera del CRM. Link roggeroyroma.com enviado. NO perseguir.
- **GAMA Inmobiliaria** (MdP) 🆕 — 4.5⭐ 108 reseñas · tel 0223 633-7766
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
| 23/06 ⏳ | $250 | Víctor Abrile — Saldo catálogo (pendiente) |

**Cobrado a hoy (19/06):** **$750 Wolfim + $333 Ango = $1.083**
**Proyectado lunes 23/06 (Wolfim):** **$1.000**

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
- **Estado:** 🟢 En curso. Wolfim $1.000 proyectado jun. Ango primera entrada $333. Tendencia confirmada.

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
- [[companies/wolfim/clients/franco-roma|Franco Roma]]
- [[companies/wolfim/clients/luis-farias|Luis Farias]]
- [[companies/korantis|Korantis]]
- [[companies/construvial|Construvial]]
- [[companies/ango|Ango]]
