---
title: Startup Incubator
type: project
created: 2026-05-02
updated: 2026-05-02
tags: [project, research, startups, latam, idea-validation]
status: active
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

## Estado actual
- ✅ YC LatAm scrapeado: 216 companies, 8 industrias
- ✅ Guardado en `data/yc_latam_raw.json`
- ✅ Análisis en `01-yc-latam-analysis.md`
- ⏳ Enrich con descripciones individuales (opcional, para profundizar)
- ⏳ Match con mercado argentino

## Fuentes de datos
- ✅ YC Startup Directory (LatAm filter): 216 companies
- ✅ Guardado en `projects/startup-incubator/data/yc_latam_raw.json`
- [ ] Serper/Browser para enriquecimiento individual (futuro)

## Análisis rápido (216 companies)

Top industrias en LatAm:
- B2B: 76 ✅
- Fintech: 68 ⚠️ (saturado en payments, ativo en credit)
- Consumer: 27 ✅
- Real Estate: 16 ✅
- Healthcare: 14 ✅
- Education: 9 ✅
- Industrials: 4 🔴
- Government: 2 🔴

Empresas argentinas: 16 (Wallbit, Ping, Sytex, Wibond, Rebill, Coderhouse, etc.)

## Ideas promisorias para investigar

### 1. B2B Operations / Productivity
- Ya existe: Sytex (CBA), Encuadrado (Chile), Treinta (Colombia)
- Concepto: gestión de operaciones para PYMES
- Match técnico: alto (Next.js + Supabase + automation)

### 2. B2B Finance & Accounting
- Ya existe: Chipax, Contalink, Simetrik
- Concepto: automatizar contabilidad o fiscalidad para independientes
- Match técnico: medio-alto

### 3. B2B HR / Recruiting
- Ya existe: HENRY, Talentropy, lapzo
- Concepto: ATS simplificado con WhatsApp como canal
- Match técnico: alto (WhatsApp integration es diferenciador)

### 4. B2B Supply Chain / Logistics
- Ya existe: clicOH, Nuvocargo, SkydropX
- Concepto: tracking last-mile o gestión de inventario
- Match técnico: medio

### 5. Healthcare — Consumer Health
- Ya existe: Terapify, Examedi
- Concepto: booking de turnos vía WhatsApp para consultorios
- Match técnico: alto

### 6. Real Estate CRM
- Ya existe: Mudafy, Houm
- Concepto: CRM inmobiliario (ya estamos validando con Outreach)
- Match técnico: 100% — es lo que hacemos

## Nota sobre saturación
Muchas sub-industrias ya tienen players en LatAm.
No significa que no hay espacio — significa que la idea está validada.
Lo que importa es: ¿podemos差异化 (differentiate) con execution más rápida o mejor enfoque?

## Recursos
- [YC LatAm raw data](data/yc_latam_raw.json)
- [YC LatAm analysis](01-yc-latam-analysis.md)
- [YC Companies Directory reference](../../references/yc-companies-directory.md)
