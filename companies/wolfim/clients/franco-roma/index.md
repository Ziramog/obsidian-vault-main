---
tags: [cliente-activo, cliente-cerrado, wolfim, inmobiliaria, alta-gracia]
---

# Franco Roma — Roggero & Roma
**Company:** Roggero & Roma
**Location:** Alta Gracia, Córdoba
**Vertical:** Inmobiliaria
**Owner:** [[companies/wolfim]]
**Status:** ✅ EN PRODUCCIÓN — entrega validada 03/06/2026
**Deal final:** **$500 USD** (pago único) + $25 USD/mes
- $200 USD inicial (cobrado 29/04/2026)
- **$300 USD finales por retrabajos de frontend** (cobra 04/06/2026 — Franco ya vio el sitio, paga mañana)

## Deal Terms
- Setup fee final: **$500 USD** (50% = $200 al inicio · 50% = $300 finales tras retrabajos)
- Monthly: **$25 USD/mes** (sin permanencia, sin contrato)
- Entrega: 2 semanas (incumplida — hubo retrabajo de frontend)
- Servicio: Sitio web profesional + panel de propiedades + SEO local

> **Nota 03/06/2026:** El deal original era $400. Hubo cambio radical de frontend (estilo senadaadzem.com — agencia de lujo en Miami) y se ajustó a $500 finales. Juan lo confirmó verbalmente.

## Proposal
![[roggero_roma_propuesta.pdf]]

## Pipeline
- [x] First contact
- [x] Demo/intro call (NodeMaven meeting)
- [x] Website analysis (sitio actual vs demo)
- [x] Proposal sent (PDF)
- [x] **Deal closed — aceptado 28/04/2026**
- [x] Contrato enviado / forma de pago acordada (Wise)
- [x] Recibir 50% inicial ($200 USD) → RECIBIDO 29/04/2026
- [x] Recibir credenciales dominio + propiedades
- [x] Kickoff / inicio del desarrollo
- [x] Cambio radical de frontend (estilo senadaadzem.com)
- [x] Segunda entrega / ajustes
- [x] **Lanzamiento / Go live → EN PRODUCCIÓN** 03/06/2026 (http 200, Vercel)
- [x] Validación cliente (Franco ya vio el sitio)
- [ ] **Cobrar $300 USD finales** → 04/06/2026 (mañana)

## Cambio Radical de Frontend (29/04/2026)
- Franco quiere un sitio REPLICA de uno que le gusta
- Juan lo está haciendo en PC local con Claude Code
- Frontend completamente nuevo — trabajo extra
- Scope: solo frontend (estructura + diseño), misma lógica/backend
- **Precio inicial acordado: $400 USD** (antes del retrabajo)
- **Precio final tras retrabajo: $500 USD** (ver Deal Terms arriba)

## Sitio Actual — Diagnóstico
- **URL:** roggeroyroma.com.ar
- Sin búsqueda ni filtros de propiedades
- Sin captura de leads (formularios)
- Sin WhatsApp visible en portada
- No adaptado a mobile
- Sin mapa interactivo

## Sitio Demo (referencia)
- **URL:** properties-srs5.vercel.app
- Filtros por tipo, ubicación, m²
- Mapa interactivo
- Botón WhatsApp flotante
- Formulario de contacto
- Panel de propiedades

## Sitio Referencia (29/04/2026)
- **URL:** https://www.senadaadzem.com/
- **Qué es:** Agente de lujo en Douglas Elliman, South Florida ($55M listings)
- **Estilo a replicar:**
  - Hero cinematográfico + tagline premium
  - Grid de propiedades con fotos HD y precios USD
  - Testimonios de clientes
  - Mapa de zonas de cobertura
  - News/press coverage
  - Diseño ultra-premium minimalista
- **Nota:** Escala muy diferente a Córdoba pero el estilo es replicable

## Add-ons para pronta implementación
Los 3 primeros son idea de Juan para justificar/el valor del mantenimiento. Google Reviews es lo único que Franco pidió directamente.

**Orden de implementación:**
1. Google Reviews — Franco lo pidió (pendiente API key)
2-4. Los otros tres son idea de Juan para justificar/el valor del mantenimiento

### Google Reviews en vivo (lo único que Franco pidió)
- **Qué hace:** Trae reviews reales de Google Maps automáticamente
- **Output:** Slider con nombre, rating, foto, comentario, fecha
- **Valor:** confianza inmediata para nuevos leads
- **Implementación:**
  1. Crear API Key en Google Cloud Console con "Places API" habilitada
  2. Agregar a `.env.local` como `NEXT_PUBLIC_GOOGLE_PLACES_API_KEY`
  3. Modificar Testimonials.jsx — quitar hardcode, agregar fetch a `/api/google-reviews`
  4. Estados: loading → error → data (fallback a hardcode si falla)
- **Costo:** ~$17 USD por 1,000 requests (mínimo para inmobiliaria con 20-50 reviews)

### Idea 1: Análisis de competencia
- **Qué hace:** Scraping mensual de inmobiliarias en Alta Gracia/zona
- **Output:** Informe con posicionamiento relativo de Roggero & Roma
- **Valor:** demuestra que el mantenimiento tiene inteligencia, no solo hosting

### Idea 2: Preparación de presupuestos
- **Qué hace:** Generador de presupuestos comparativos para inversores
- **Output:** PDF con comparativa de propiedades, rendimiento, escenarios
- **Valor:** herramienta comercial para cerrar operaciones

### Idea 3: Generador de descripciones de propiedades
- **Qué hace:** Copywriting AI que genera descripciones optimizadas para portales
- **Output:** Texto listo para Zonaprop, Argenprop y web propia
- **Valor:** problema real que el cliente siente — escribir descripciones a mano toma tiempo

### Precio sugerido
- Individual: $15-20 USD/mes por add-on
- Bundle 3 ideas: $35 USD/mes
- Complemento al mantenimiento: no reemplaza, suma

## Next Steps
1. [ ] Enviar contrato — acordar forma de pago Wise
2. [ ] Recibir 50% inicial ($200 USD)
3. [ ] Recibir credenciales dominio (roggeroyroma.com.ar)
4. [ ] Recibir propiedades — fotos, descripciones, datos
5. [ ] Kickoff del desarrollo
6. [ ] Entrega en 2 semanas

## Notes
- Franco es decision maker directo
- **Precio final acordado: $500 + $25/mes** (ajustado 03/06 por retrabajos)
- Dominio ya existe — no se cobra dominio adicional
- Plazo acordado: 2 semanas (incumplido)
- Competencia: Argenprop ($200-400/mes atado), Zonaprop (ads pagos)
- Primer cliente real de Wolfim — entregado
- **PAGO 50% RECIBIDO** (29/04/2026 — $200 USD)
- **PAGO RESTANTE A COBRAR** (04/06/2026 — $300 USD)
- **Nuevo scope (29/04/2026):** cambio radical de frontend — replica de sitio que Franco likes. Juan trabaja en PC local con Claude Code. Scope extra cubierto con ajuste a $500.
- **URL sitio referencia (29/04/2026):** https://www.senadaadzem.com/ — agente de lujo Douglas Elliman Miami
- **Sitio en producción 03/06/2026:** https://www.roggeroyroma.com — HTTP 200, Vercel/Next.js, cert Let's Encrypt válido, 6 reseñas Google en vivo (4.8★, 31 totales)
- **Validado por Franco 03/06/2026** — paga mañana 04/06 $300 USD
- **Lección (registrada):** venta con precio cerrado ANTES del retrabajo evita renegociación. La próxima, si hay cambio de scope, se cobra extra o se documenta ajuste de precio por escrito.