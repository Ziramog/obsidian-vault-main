---
company: ANGO
type: technical-close
source: web-builder
status: site-ready-payment-blocked
created-at: 2026-07-24T16:09:46-03:00
owner: ango-commercial
project: google-ads-2026-06
---

# ANGO Google Ads — cierre técnico web-builder

## Estado técnico del sitio

Web-builder informó estado **LISTO** para activar Google Ads desde el punto de vista del sitio y mediciones.

## Implementación confirmada

- Método: `gtag` directo.
- Google Ads tag: confirmado.
- Google Ads tag ID: `AW-18347194194`.
- Presente en producción en:
  - `/`
  - `/repuestos-compatibles-urvig-micron/`
- GA4 confirmado: `G-JX8JKF9ELH`.
- `window.gtag` activo.
- `dataLayer` contiene:
  - `config G-JX8JKF9ELH`
  - `config AW-18347194194`
- Conversion Linker: no aplica porque no hay GTM.
- Atribución Ads: por Google tag directo con `AW-18347194194`, leyendo `gclid` desde URL y seteando cookies/atribución propia de Google.
- Eventos preservan UTMs:
  - `utm_source`
  - `utm_medium`
  - `utm_campaign`
  - `utm_content`
  - `utm_term`

## Eventos probados

- `whatsapp_clicked`: ok.
  - Home: `product_line=rg_pto`, `cta_location=home_hero`.
  - Landing: `product_line=urvig_micron`, `cta_location=hero`.
- `phone_clicked`: ok.
  - Home/footer: `product_line=rg_pto`, `cta_location=footer_contact`.
  - Landing: `product_line=urvig_micron`, `cta_location=final_phone`.
- `lead_form_submitted`: ok.
  - Home: `product_line=rg_pto`, `cta_location=home_rg_quote_form`.
  - Landing: `product_line=urvig_micron`, `cta_location=compatibility_form`.
- `email_clicked`: ok.
  - Home/footer: `product_line=rg_pto`, `cta_location=footer_contact`.
  - Landing: `product_line=urvig_micron`, `cta_location=final_email`.

## Separación por línea comercial

- `rg_pto`: ok.
- `urvig_micron`: ok.

Parámetros disponibles:

- `product_line`
- `cta_location`
- `page_path`
- `page_location`
- `ad_group_intent` en CTAs clave
- UTMs completas cuando están en URL

## Footer.astro

- No afecta medición ni CTAs.
- El patch fallido no dejó código roto.
- Fue un intento de reemplazo sobre una cadena que en output aparece enmascarada.
- El botón de teléfono del footer existe y dispara `phone_clicked`.
- El email del footer existe y dispara `email_clicked`.
- No afecta WhatsApp, teléfono, email ni medición.

## Validación funcional

- Botón WhatsApp: ok.
- Botón teléfono: ok.
- Formularios: ok.
- Email click: ok.
- Navegación landing: ok.
- Consola JS: 0 errores.
- Producción incluye commit `99104d3 feat: add Google Ads AW tag`.

## Decisión técnica

Desde el sitio, se puede activar campaña.

Pendientes técnicos del sitio: ninguno.

Recomendado: mirar en la cuenta de Antonio GA4 Realtime mientras se hace un click de prueba para confirmar visualmente la recepción.

## Advertencia por cuenta nueva de Ads

El tag `AW-18347194194` corresponde a la cuenta/campaña de Google Ads donde se generó originalmente.

Juan informó que la forma de pago quedó bloqueada en prepago y que necesitará crear una cuenta nueva para poder usar pospago con tarjeta. Si se crea una cuenta Google Ads nueva, revisar si Google entrega un nuevo Google tag `AW-...`.

Si la cuenta nueva entrega otro `AW`, web-builder deberá reemplazar o agregar correctamente el nuevo tag y no dejar medición apuntando solo a la cuenta vieja.

Si la cuenta nueva solo importa conversiones desde GA4, igual se recomienda vincular GA4 con la cuenta nueva, activar auto-tagging y validar eventos antes de publicar.
