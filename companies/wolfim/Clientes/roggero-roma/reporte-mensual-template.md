---
title: Informe mensual de Analytics — Roggero & Roma
type: report-template
client: Roggero & Roma
owner: wolfim-growth
created: 2026-07-08
status: active
period: mensual
---

# Informe mensual de Analytics — Roggero & Roma

## Estructura del informe (5 páginas)

1. **Portada**
   - Logo Wolfim + pill "INFORME WOLFIM"
   - Título, subtítulo, cliente, período, destinatario, fecha
   - Frase de cierre: "convertir datos en decisiones comerciales"

2. **Resumen ejecutivo**
   - Párrafo de lectura comercial principal
   - 6 metric cards: usuarios, sesiones, pageviews, Google orgánico, páginas/sesión, engagement rate
   - Callout con conclusión principal

3. **Procedencia + Fuentes**
   - Tabla de países con lectura
   - Callout aclaratorio de tráfico internacional vs Argentina
   - Tabla de fuentes/secciones con dato y lectura

4. **Qué busca la gente**
   - Callout "Lo más buscado: Casas" con hallazgo principal
   - Tabla de filtros usados
   - Párrafo de dispositivos (mobile/desktop)
   - Callout "Cuándo navegan" con picos horarios
   - Tabla de horarios con recomendación de publicación
   - Tabla de propiedades más vistas con lecturas

5. **Cierre Wolfim**
   - Panel oscuro con isologo blanco
   - Mensaje de valor y dirección

## Queries GA4 utilizados

Todos contra `properties/539918073` con la service account `wolfim-analytics-tools`.

| Dato | Dimensiones | Métricas |
|---|---|---|
| Resumen país | `country` | `totalUsers`, `sessions`, `screenPageViews` |
| Fuentes/Secciones | `pagePathPlusQueryString`, `pageTitle` | `screenPageViews`, `totalUsers`, `engagementRate` |
| Filtros usados | `pagePathPlusQueryString` (con ?type= o ?operation=) | `screenPageViews`, `totalUsers` |
| Dispositivos | `deviceCategory` | `totalUsers`, `sessions`, `screenPageViews` |
| Horarios | `hour` | `sessions`, `screenPageViews` |
| Días de semana | `dayOfWeekName` | `sessions`, `screenPageViews` |
| Propiedades individuales | `pageTitle` (filtrar /properties/ID) | `screenPageViews`, `totalUsers` |
| Eventos comerciales | `eventName` (form_start, click, click_whatsapp) | `eventCount`, `totalUsers` |

## Assets requeridos

- Logo Wolfim black PNG (portada, header, footer)
- Isologo black PNG (footer)
- Isologo white PNG (cierre oscuro)
- Fuentes: Space Grotesk, Inter, JetBrains Mono (en `brand/fonts/`)

## Scripts

- Preset reutilizable: `/home/hermes/scripts/wolfim_report_preset.py`
- Generador específico: `/home/hermes/scripts/generate_roggero_analytics_mensual_wolfim.py`
- Output: `Transfer-files/roggero_roma_informe_mensual_analytics_wolfim_webstyle_YYYY-MM-DD.pdf`
