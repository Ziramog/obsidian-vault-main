# Wolfim — Patterns y decisiones técnicas

## Stack de reporting (2026-06-26)

**Decisión:** Usar stack 100% gratis para informes mensuales a clientes.

**Stack:**
GA4 + GTM + Search Console + Looker Studio + Google Sheets

**Costo:** $0 USD
**Costo real:** tiempo de configuración + análisis mensual

**Por qué:**
- No requiere inversión recurrente del cliente
- Se puede presentar como "medición profesional" en el plan de mantenimiento
- Looker Studio conecta directo con GA4 y Search Console sin ETL
- Sheets permite capa manual de leads reales que Analytics no captura

## Presentación comercial

Incluir así en el plan de mantenimiento:

> Incluye medición profesional con Google Analytics, Search Console y reporte mensual de performance: visitas, consultas, canales, SEO y recomendaciones comerciales.

## Estructura del informe mensual mínimo

1. Visitas totales
2. De dónde vino la gente (canales de tráfico)
3. Páginas/lotes más vistos
4. Clicks a WhatsApp
5. Formularios o contactos
6. Palabras SEO de Google (posición, CTR)
7. Recomendaciones del mes

## Capa manual (Sheets) vs automática (GA4)

- GA4 da datos cuantitativos: "42 clicks a WhatsApp"
- Sheets agrega cualidad: "12 consultas reales, 4 calificadas, 1 visita al lote"
- Combinados = informe mucho más valioso que solo datos crudos
