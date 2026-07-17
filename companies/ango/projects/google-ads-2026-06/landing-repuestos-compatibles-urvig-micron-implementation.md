---
company: ANGO
project: Google Ads 2026
handoff: HO-2026-07-16-001
status: published
published_at: 2026-07-16
commit: d049d432c725f2d7d702926f23baebae446be46d
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

## Nota operativa

No se configuraron campañas de Google Ads ni eventos en GA4/GTM. Los hooks de tracking quedaron preparados para implementación posterior.
