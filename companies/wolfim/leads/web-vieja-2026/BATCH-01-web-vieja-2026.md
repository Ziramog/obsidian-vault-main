---
title: Web Vieja 2026 — Batch 01
type: lead_batch
empresa: wolfim
fecha_batch: 2026-06-14
fuente: serper + scoring + phone enrichment
total_scraped: "167"
total_high_score: "44"
total_valid_phones: "8"
status: outreach_pending
---

# Web Vieja 2026 — Batch 01

> Campaña: outreach a empresas con web vieja para renovación Wolfim.
> Generado: 2026-06-14 via Hermes VPS

## Proceso

| Fase | Descripción | Resultado |
|---|---|---|
| Fase 1 | Scraping Serper (25 queries × 10 results) | 167 leads únicos |
| Fase 2 | Score automático (SSL, mobile, HTML, sitemap, WHOIS) | 44 con score ≥60 |
| Fase 3 | Phone enrichment (HTTP fetch + wa.me extraction) | 8 válidos, 7 sospechosos, 4 malos |

## Leads válidos para outreach

| # | Nombre | WA Link | Ciudad | Vertical | Score |
|---|---|---|---|---|---|
| 1 | MMLUISA Inmobiliaria | wa.me/543541528601 | Córdoba | inmobiliaria | 70 |
| 2 | AABA (Abogados BsAs) | wa.me/5491143718869 | CABA | abogado | 70 |
| 3 | Estudio Jurídico Mogliani | wa.me/543511559438 | Córdoba | abogado | 60 |
| 4 | IZA Inmobiliaria (MdP) | wa.me/542235776000 | MdP | inmobiliaria | 60 |
| 5 | FACPCE (Contadores) | wa.me/5491148131758 | CABA | contador | 60 |
| 6 | Clínica del Sol (Córdoba) | wa.me/543517555444 | Córdoba | clinica | 60 |
| 7 | RYM GROUP (Abogados MdP) | wa.me/54992236125533 | MdP | abogado | 60 |
| 8 | Sanatorio Otamendi (CABA) | wa.me/5491128382351 | CABA | clinica | 60 |

## Leads sospechosos (revisar manualmente)

| # | Nombre | WA parcial | Ciudad | Score | Nota |
|---|---|---|---|---|---|
| 1 | Sanatorio Providencia | 541152999000 | CABA | 70 | 11 dígitos — verificar |
| 2 | Estudio del AMO | +549****5387 | CABA | 70 | Número parcialmente visible |
| 3 | Constructora Kohon | +549****8507 | CABA | 70 | Parcialmente oculto |
| 4 | Grupo Legal (Abogados) | +549****9797 | CABA | 60 | Parcialmente oculto |
| 5 | CCA Estudio Contable | +549****0541 | CABA | 60 | Parcialmente oculto |
| 6 | Dr. Perez Lloveras | +543****4268 | Córdoba | 60 | Córdoba 351 parcial |
| 7 | MDO Garage | 541521760897 | CABA | 60 | Falta 54 prefix |

## Archivos del batch

- `mmluisa-inmobiliaria-cordoba.md`
- `aaba-asociacion-abogados-bsas.md`
- `estudio-mogliani-abogados-cordoba.md`
- `iza-inmobiliaria-mar-del-plata.md`
- `facpce-fed-contadores-caba.md`
- `clinica-maternidad-del-sol-cordoba.md`
- `rym-group-abogados-mar-del-plata.md`
- `sanatorio-otamendi-caba.md`
- `web-vieja-leads-20260614.csv` — todos los 167 leads (en `/workspace/scraping/data/`)
- `web_vieja_scored_20260614.csv` — los 167 con score (en `/workspace/scraping/data/`)
- `web_vieja_enriched_20260614.csv` — los 44 con enrichment (en `/workspace/scraping/data/`)

## Próxima acción

Outreach manual por WhatsApp — empezar por los 8 leads válidos.
Mensaje sugerido: mockup gratuito de renovación web.

## Notas técnicas

- Supabase no accesible desde VPS (DNS bloqueado en Contabo) — CSVs en `/workspace/scraping/data/`
- Scripts: `web_vieja_scraper.py`, `web_vieja_score_v2.py`, `web_vieja_phone_enrich.py`
