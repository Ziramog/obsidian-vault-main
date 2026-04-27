# Loop Sistema Adquisición de Clientes

## Loop Principal

```
SCRAPE → LEADS → OUTREACH → RESULT → ANALYSIS → OPTIMIZE → SCRAPE
```

> Esto corre solo si definís bien cada capa.

---

## Arquitectura Completa

```
[1] SCRAPER (Hermes + proxy)
    ↓
[2] DB (leads)
    ↓
[3] ENRICH (email / web / canal)
    ↓
[4] OUTREACH ENGINE
    ↓
[5] TRACKING (DB)
    ↓
[6] HERMES ANALYSIS
    ↓
[7] OBSIDIAN (insight)
    ↓
[8] AJUSTE AUTOMÁTICO
```

---

## 1. SCRAPING — Entrada del sistema

**Objetivo:** leads de alta probabilidad

Ejemplos de filtro:
- Negocios sin web
- Con web vieja
- Sin botón WhatsApp

> Menos volumen, más calidad.

---

## 2. ENRICHMENT — Clave

Antes de contactar, decidir canal óptimo:

| Si tiene → | Usar |
|---|---|
| WhatsApp | WhatsApp |
| Web | Form |
| Email | Email |

> Esto multiplica conversiones.

---

## 3. OUTREACH ENGINE

### Cola de estado
```
lead → pending → contacted → followup → closed
```

### Secuencia automática
- Día 1 → mensaje 1
- Día 3 → followup
- Día 7 → cierre

### Mensaje (simple y directo)
```
Vi tu negocio {{nombre}}, te puedo traer más clientes sin pagar ads
```

> No vendas web, vendé resultado.

---

## 4. TRACKING — DB

Guardar:
- `sent` — enviado
- `opened` — abierto (si email)
- `replied` — respondido
- `converted` — convertido

---

## 5. HERMES — Cerebro real

Cada X horas:
- Analiza respuestas
- Detecta patrones
- Decide cambios

---

## 6. OBSIDIAN — Solo lo importante

NO logs crudos. Solo:

```markdown
# Campaña X

- leads: 120
- respuestas: 9
- conversion: 3

## Insight
Mejor funciona mencionar "clientes por WhatsApp"

## Acción
Cambiar copy inicial
```

---

## 7. OPTIMIZACIÓN AUTOMÁTICA

Hermes puede cambiar:
- Mensajes
- Nicho
- Fuente de leads

---

## Loop Real Ejecutándose

```
cron scraping
    ↓
cron outreach
    ↓
cron analysis
    ↓
update strategy
    ↓
repeat
```

---

## Dónde Falla la Mayoría

❌ **Sin feedback loop** — hacen scraping + outreach, nunca optimizan

❌ **Sin canal dinámico** — usan solo email, pierden conversiones

❌ **Sin tracking** — no saben qué funciona

---

## Tu Ventaja

Ya tenés:
- ✅ VPS
- ✅ Hermes
- ✅ Scraper
- ✅ Visión de sistema

> Estás 80% adelante.

---

## Próximo Paso

### MVP completo funcional en VPS

Incluye:
- Scraper listo
- DB + esquema
- Outreach básico (email + form)
- Cron jobs
- Generación automática en Obsidian

> Versión simple pero operativa. Modo generar clientes reales, no solo setup.

---

## Campañas

| Campaña | Leads | Enviados | Respuestas | Conversión | Insight |
|---|---|---|---|---|---|
| TBD | — | — | — | — | — |

## Insights

## Acciones
