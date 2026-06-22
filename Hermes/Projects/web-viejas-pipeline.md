# Web Viejas — Pipeline de Lead Generation + Outreach
# Actualizado: 21 Junio 2026
# Estado: ✅ Producción

---

## Resumen

Sistema completo de generación de leads para Wolfim: busca sitios .com.ar con copyright viejo, verifica que NO tengan WhatsApp, enriquece con datos de contacto, y envía campañas de email automatizadas desde `juan@wolfim.com`.

---

## Pipeline completo

```
dork_scout.py → 223 leads .com.ar con copyright 2017-2019
       ↓
wa_checker.py → 74 leads (negocio real + sin WhatsApp)
       ↓
enrich_leads.py → 54 outreach-ready (48 email, 32 teléfono)
       ↓
email_campaign.py / campaign.py → Envío personalizado vía Resend
       ↓
cron_campaign.py → Automático 10/día a las 10am
```

---

## Componentes

### 1. dork_scout.py
**Ruta:** `workspace/scraping/dork_scout.py`
**Qué hace:** Busca en Google vía Serper API sitios .com.ar con "Copyright 2017/2018/2019" por vertical (inmobiliaria, abogado, contador, constructora, clínica, taller, hotel).
**Output:** CSV en `data/dork_scout_{fecha}.csv`

### 2. wa_checker.py
**Ruta:** `workspace/scraping/wa_checker.py`
**Qué hace:** Visita cada web y verifica:
- Presencia de WhatsApp (links wa.me, api.whatsapp.com, botones flotantes, iconos)
- Clasifica si es un negocio real vs portal/diario/blog
- Verifica SSL/HTTPS
- Extrae copyright real
**Output:** `data/wa_checked_{fecha}.csv` con columna `wa_presence = YES/NO`

### 3. enrich_leads.py
**Ruta:** `workspace/scraping/enrich_leads.py`
**Qué hace:** Visita cada web y extrae:
- Emails del body, mailto:, meta tags
- Teléfonos (con limpieza de formato)
- Nombre de contacto
- Si tiene formulario de contacto
- Si tiene página "Nosotros"
**Output:** `data/enriched_{fecha}_outreach.csv`

### 4. campaign.py / cron_campaign.py
**Ruta:** `workspace/scraping/campaign.py`
**Qué hace:** 
- Genera email personalizado con hallazgos reales por dominio
- Hallazgos priorizados: HTTPS > WhatsApp > Copyright
- Máximo 2 hallazgos por email, en formato de viñetas
- Envía vía Resend con logo Wolfim embebido (CID)
- Reply-to: `juan@wolfim.com`
**Ruta cron:** `workspace/scraping/cron_campaign.py`
**Tracker:** `data/campaign_tracker.csv`

---

## Template de email final

```
Hola,

Soy Juan, de Wolfim. Estuve revisando [dominio] y noté [1|2] detalles:

* [hallazgo 1]
* [hallazgo 2]

¿Querés que te envíe algunas ideas concretas para mejorarlo?

Saludos,

Juan Gomariz
Wolfim
wolfim.com
[logo Wolfim]

Si preferís que no vuelva a escribirte, respondeme "BAJA".
```

---

## Hallazgos disponibles (por orden de prioridad)

1. ❌ Sin HTTPS (HTTP) → "El sitio todavía utiliza HTTP en vez de HTTPS..."
2. ❌ Sin WhatsApp → "No encontré un acceso visible a WhatsApp..."
3. ❌ Copyright desactualizado → "El pie del sitio todavía muestra copyright AÑO..."
4. ⚠️ Sin copyright → "El sitio no muestra un copyright visible..."

---

## Configuración técnica

| Componente | Detalle |
|---|---|
| **Remitente** | `Juan Gomariz <juan@wolfim.com>` |
| **Reply-to** | `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com` |
| **API** | Resend (`re_7mRutuUJ_DLhKJwu1jNx5oBhJkuQnrv6o`) |
| **SMTP alternativo** | Himalaya configurado con `ingjuangomariz@gmail.com` + app password |
| **Logo** | `https://assets.wolfim.com/v2.svg` (servido desde VPS, nginx puerto 80/443) |
| **BIMI** | `default._bimi.wolfim.com` → `v=BIMI1; l=https://assets.wolfim.com/v2.svg;` |
| **DMARC** | `v=DMARC1; p=quarantine; rua=mailto:wolfimhq@gmail.com` |
| **SPF** | `include:_spf.mx.cloudflare.net include:_spf.resend.com` |
| **DNS Logo** | `assets.wolfim.com` A `194.163.161.99` (Cloudflare proxy) |

---

## Cron jobs activos

| Job | Schedule | Acción |
|---|---|---|
| `wolfim-campaign` | `0 10 * * *` (diario 10am) | Envía 10 leads |
| `check-replies` | `0 10,14,18 * * 1-5` (lun-vie) | Revisa respuestas en Gmail |

---

## Resultados (21 Junio 2026)

| Tanda | Leads | Entregados | Rebotes |
|---|---|---|---|
| Tanda 1 | 10 | 9 | 1 (email sucio) |
| Tanda 2 | 10 | 10 | 0 |
| **Total** | **20** | **19** | **1** |

---

## Archivos clave

```
workspace/scraping/
├── dork_scout.py              # Fase 1: búsqueda de leads
├── wa_checker.py              # Fase 2: filtro WhatsApp + negocio
├── enrich_leads.py            # Fase 3: extracción de contactos
├── build_outreach.py          # Armado de tracker
├── email_campaign.py          # Gestión de campaña
├── campaign.py                # Envío con template final
├── cron_campaign.py           # Envío automático por cron
├── save_drafts.py             # Borradores Gmail
├── send_v4.py                 # Tests de template
├── generate_campaign.py       # Preview con validación
└── data/
    ├── campaign_tracker.csv   # Tracking de envíos
    ├── outreach_tracker_*.csv # Leads listos para campaña
    ├── enriched_*.csv         # Leads enriquecidos
    └── wa_checked_*.csv       # Leads filtrados por WA
```

---

## Próximos pasos

- [ ] Monitorear respuestas de tanda 1 y 2
- [ ] Evaluar tasa de apertura y respuesta
- [ ] Ajustar template según resultados
- [ ] Escalar a más verticales si funciona
- [ ] Mejorar limpieza de emails sucios
