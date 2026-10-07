---
type: LOCAL_REQUEST
company: wolfim
client: roggero-roma
target: web-builder
owner: wolfim-growth
created: 2026-10-07
priority: high
status: pending
---

# Roggero & Roma — restaurar eventos GA4 `property_viewed` y `click_whatsapp`

## Problema (verificado en GA4)

Los eventos custom de GA4 **dejaron de dispararse alrededor del 2026-07-30** y no volvieron:

| Evento | Última fecha con datos | Período ago | Período sep |
|---|---|---|---|
| `property_viewed` (ficha de propiedad vista) | **2026-07-29** | 0 | 0 |
| `click_whatsapp` (clic en WhatsApp) | **2026-07-28** | 0 | 0 |

Verificado con la GA4 Data API sobre la propiedad `Roggero & Roma`:

- Entre 2026-07-08 y 2026-07-29, `property_viewed` acumuló 92 eventos (users 26).
- Entre 2026-07-03 y 2026-07-28, `click_whatsapp` acumuló 4 eventos.
- Desde el 2026-07-30 hasta el 2026-10-07: **0 eventos** de ambos.
- Los eventos automáticos (Enhanced Measurement) siguen OK: `page_view`, `session_start`,
  `scroll`, `user_engagement`, `first_visit`, `form_start`.

## Diagnóstico

Solo se cortaron los **eventos custom** (los que emite el código del sitio). Los automáticos siguen
funcionando. Esto apunta a que un **deploy alrededor del 2026-07-30 removió o rompió** el/los
módulos que disparaban `property_viewed` y `click_whatsapp` (p. ej. `lib/analytics` o el componente
de ficha de propiedad / botón de WhatsApp).

## Pedido

1. Revisar el historial de deploys alrededor del 2026-07-29/30 y detectar qué cambió en el código de
   analytics.
2. Restaurar el disparo de:
   - `property_viewed` — al renderizar la ficha de una propiedad.
   - `click_whatsapp` — al hacer clic en cualquier CTA de WhatsApp.
3. Mantener la separación de eventos pedida antes (búsqueda, filtros, contacto real) según
   `LOCAL_REQUEST-webbuilder-roggero-ga4-eventos-claros-2026-08-07.md`.
4. Mantener la exclusión de tráfico interno por login/rol (admin/superadmin) sin afectar los eventos
   de visitantes externos.
5. **Validar en GA4 DebugView**: en incógnito (visitante externo) deben verse `property_viewed` y
   `click_whatsapp`; logueado como admin NO deben dispararse.

## Criterio de aceptación

- Al abrir una ficha en incógnito, GA4 registra `property_viewed`.
- Al tocar el botón de WhatsApp, GA4 registra `click_whatsapp`.
- En los informes mensuales siguientes, los cuadritos "Fichas vistas" y "Clics de WhatsApp" vuelven
  a mostrar valores reales (no 0).

## Seguridad

- No enviar PII a GA4 (no nombres, emails ni teléfonos).
- No registrar tokens ni claves; referenciar como `[credencial: NOMBRE]`.
