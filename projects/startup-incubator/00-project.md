---
title: Startup Incubator
type: project
created: 2026-05-02
updated: 2026-05-02
tags: [project, research, startups, latam, idea-validation]
status: germination
confidence: low
---

# Startup Incubator — Germinando

> Investigar startups de YC que puedan replicarse o adaptarse a LatAm.
> Sin presión. Ir cosechando ideas until one clicks.

## Meta
Encontrar UNA idea que:
1. Exista y funcione en otro mercado (validado por YC)
2. Sea replicable o adaptable a LatAm
3. Matchée con nuestras capacidades (Next.js, Supabase, WhatsApp, scrapers, automation)
4. Tenga mercado local real

## Fuentes de datos
- [YC Startup Directory](https://www.ycombinator.com/companies) — 5,860 companies
- [YC Companies filter: Latin America](https://www.ycombinator.com/companies?regions=Latin+America) — 217 companies
- [ ] Scraper de YC companies (API o scraping)

## Playbook lento

### Fase 1 — Germinar (sin fecha límite)
- [ ] Scrapear YC companies → JSON con nombre, industria, descripción, batch,HQ, URL
- [ ] Normalizar por industria/categoría
- [ ] Guardar en CSV/Supabase
- [ ] Investigar: ¿cuáles de esas ideas tienen mercado en LatAm?
- [ ] Scoring: Replicabilidad × Mercado LatAm × Nuestros skills

### Fase 2 — Nutrir (post-germinación)
- [ ] Profundizar en las 5-10 ideas más promising
- [ ] Investigar competencia local (Argentina, LatAm)
- [ ] Validar con datos: ¿hay demanda real o solo curiosidad?

### Fase 3 — Elegir (post-nutrición)
- [ ] Una sola idea
- [ ] Validación de pago (primer cliente antes de construir)
- [ ] MVP mínimo

## Capacidades disponibles para matchear
- Next.js / React
- Supabase (DB + auth + functions)
- WhatsApp automation (YCloud API)
- Scrapers (Google Maps, Serper)
- Make.com automations
- Ventas B2B (concesionarias, inmobiliarias)

## Categorías YC para investigar primero en LatAm
- [ ] Fintech (622 companies) — pagos, lending, banking
- [ ] B2B SaaS (2,994 companies) — herramientas para empresas
- [ ] Healthcare (668) — healthtech
- [ ] Real Estate (153) — proptech
- [ ] Education (124) — edtech

## Próximo paso
Scrapear YC directory completo con categorización por industria.
Guardar en CSV → Obsidian → Supabase para consultas.

## Nota
Este proyecto es LONG-TERM. No compete con el pipeline de concessionarias.
Se trabaja cuando hay espacio mental, no cuando hay presión financiera.
