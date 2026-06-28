# Roggero & Roma — Patterns y decisiones técnicas

## Stack de reporting
GA4 + GTM + Search Console + Looker Studio + Google Sheets

## Estado actual (post-implementación 26/06/2026)

- ✅ GA4 con gtag.js activo
- ✅ 13 eventos de conversión implementados: `click_whatsapp`, `click_phone`, `click_maps`, `form_submit`, `click_facebook`
- ❌ Sin GTM (usando gtag.js directo)
- ❌ Search Console no conectado
- ❌ Sin dashboard Looker Studio

### Próximos pasos
1. Conectar Search Console a GA4
2. Armar dashboard en Looker Studio
3. Evaluar migración a GTM

## Insights del primer período (may-jun 2026)

### Tráfico
- 57% del tráfico es directo — clientes que ya conocen la marca o escriben la URL
- 26% es Google orgánico — saludable para un sitio sin SEO activo agresivo
- accounts.google.com / referral (23%) — probablemente gente que ve emails de Google Workspace y clickea links

### Propiedades más vistas
- La página de listado general (Propiedades) domina con 650 views — el resto de propiedades individuales tiene muy pocas vistas (promedio 5-10). Señal de que **las propiedades individuales no están recibiendo tráfico directo desde Google**. Hay que trabajar SEO por propiedad.

### Geografía
- Council Bluffs (51 users) y otras ciudades de data centers inflan las métricas. Usuarios reales ≈ 280.
- Buenos Aires (25), Río Tercero (21), Córdoba (16) son los mercados reales principales.

### Pendiente para próximos períodos
- [ ] Instalar GTM para trackear eventos (WhatsApp, formulario, PDF, mapas)
- [ ] Conectar Search Console para ver palabras clave
- [ ] Revisar qué propiedades tienen más potencial SEO
- [ ] Reducir ruido de bots/data centers con filtro interno
