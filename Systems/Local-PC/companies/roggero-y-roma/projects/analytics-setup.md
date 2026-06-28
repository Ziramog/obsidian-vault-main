# Roggero & Roma — Analytics Setup

**Estado:** GA4 activo. Falta GTM + Search Console.
**Próximo paso:** Configurar eventos de conversión vía GTM.

---

## Lo que está funcionando

- ✅ GA4 data stream web activo
- ✅ Recolectando: usuarios, sesiones, páginas vistas, tráfico por fuente
- ❌ **Sin GTM** — no hay eventos trackeados (WhatsApp, formulario, PDF, mapas)
- ❌ **Sin Search Console** — no sabemos qué palabras clave traen tráfico
- ❌ **Sin Looker Studio** — no hay dashboard armado

---

## Plan de acción

### Fase 1 — Eventos (GTM)
1. Crear contenedor GTM
2. Instalar snippet en el sitio
3. Configurar triggers:
   - `click_whatsapp` — botones de WhatsApp en el sitio
   - `click_phone` — enlaces tel:
   - `form_submit` — formulario de contacto (si existe)
   - `click_maps` — enlaces a Google Maps
   - `download_pdf` — descargas
4. Publicar contenedor

### Fase 2 — SEO (Search Console)
1. Verificar propiedad en Search Console
2. Asociar con GA4

### Fase 3 — Dashboard (Looker Studio)
1. Conectar GA4 + Search Console
2. Armar dashboard con:
   - Resumen mensual
   - Canales de tráfico
   - Eventos y conversiones
   - Páginas populares
   - SEO (cuando Search Console esté activo)

### Fase 4 — Informe mensual
1. Usar template de Google Sheets para leads reales
2. Generar informe narrativo
