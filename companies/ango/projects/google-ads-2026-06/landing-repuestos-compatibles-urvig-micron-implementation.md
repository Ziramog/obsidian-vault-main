---
company: ANGO
project: Google Ads 2026
handoff: HO-2026-07-16-001
status: published
published_at: 2026-07-16
commit: 26b2188ef781e0a76fcf9bed4d6b6915f02b4948
---

# Landing ANGO — repuestos compatibles Urvig / Micron

## URL de producción

https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron

## Implementación

Se creó una landing específica para búsquedas de repuestos compatibles con equipos Urvig y Micron, manteniendo la home enfocada en la línea propia RG y tomas de fuerza.

La landing incluye:

- H1 único orientado a intención de compra.
- Copy legalmente seguro: “compatibles”, sin afirmar representación ni condición oficial.
- Bloques específicos para Urvig y Micron.
- Solicitud de marca, modelo, cantidad, localidad, teléfono y detalle.
- Envío del formulario a WhatsApp con mensaje precompletado.
- Preservación de `utm_source` y `utm_campaign` en el mensaje de consulta.
- IDs y atributos `data-event` para futura medición de `whatsapp_clicked`, `phone_clicked`, `email_clicked` y `lead_form_submitted`.
- CTA sticky de WhatsApp en mobile.
- Aclaración legal de compatibilidad.
- Catálogo técnico responsive con 14 referencias Urvig y sus equivalencias Micron.
- CTA individual por repuesto con WhatsApp precargado.
- Campo opcional de código Urvig/Micron en el formulario.
- Hook `part_consulted` con descripción y ambos códigos.
- Supresión del CTA sticky mobile dentro del catálogo y formulario para evitar superposiciones.
- Hero mobile-first con imagen técnica visible en el primer viewport de 390 × 844 px.
- Copy y CTAs del hero orientados a cotización de repuestos para tomas de fuerza industriales.
- Catálogo mobile compactado: descripción, códigos Urvig/Micron en paralelo y CTA full width.
- Sticky de WhatsApp visible solo después del hero y oculto dentro del catálogo/formulario.

También se corrigió la home para diferenciar claramente:

- Repuestos de línea propia RG.
- Reacondicionamiento.
- Soluciones compatibles verificadas por modelo.

## Archivos modificados

- `src/pages/repuestos-compatibles-urvig-micron.astro`
- `src/components/Hero.astro`
- `src/components/Navbar.astro`
- `src/components/Spares.astro`
- `src/components/Specs.astro`
- `src/layouts/Layout.astro`

## Publicación

- Repo: `https://github.com/Ziramog/angoweb.git`
- Rama: `main`
- Commit inicial: `901ebe76a81dd0bc9ff7ede13b55598ffbe2673f`
- Commit catálogo: `d049d432c725f2d7d702926f23baebae446be46d`
- Commit mobile-first: `26b2188ef781e0a76fcf9bed4d6b6915f02b4948`
- Deploy automático confirmado con HTTP 200.

## Verificación

- `npm run build`: aprobado; 3 rutas generadas.
- Ruta local de landing: aprobada.
- Producción desktop: aprobada.
- Producción mobile real 390 × 844 px: aprobada.
- Sin overflow horizontal: `scrollWidth = viewport = 390`.
- CSS de producción cargado: 100 reglas de la landing.
- CTA mobile visible y FAB global oculto en la landing.
- Formulario probado con datos ficticios; construye URL de WhatsApp correcta.
- `utm_source` y `utm_campaign` preservados en el mensaje.
- Un solo H1.
- Sin errores JavaScript en consola.
- Home validada con wording RG / compatibles corregido.
- 14 filas verificadas en producción, sin precios.
- Todos los códigos aparecen una vez en la fuente de datos.
- `TAE44A / 98342044506` y `TAA10A / 103934011` verificados.
- Tracking `part_consulted` probado con datos de repuesto, códigos y UTM.
- Producción 390 × 844: 174 px de imagen técnica visibles dentro del primer viewport.
- Sticky verificado oculto en hero, visible después del hero y oculto en catálogo.
- Código Micron `98342044506` visible completo en mobile.

## Nota operativa

No se configuraron campañas de Google Ads ni eventos en GA4/GTM. Los hooks de tracking quedaron preparados para implementación posterior.
