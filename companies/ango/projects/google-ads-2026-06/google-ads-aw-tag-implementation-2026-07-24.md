---
company: ANGO
project: google-ads-2026-06
type: implementation-report
status: production-verified-browser
created: 2026-07-24
owner: web-builder
source-handoff: Hermes/Handoffs/vps-to-local/HO-2026-07-24-001/request.md
repo: C:/Projects/ANGOWEB2/astro-site
commit: 99104d3
---

# ANGO — Google Ads AW tag implementation

## Resultado

Implementado y pusheado el Google Ads / AW tag:

```text
AW-18347194194
```

Commit:

```text
99104d3 feat: add Google Ads AW tag
```

Push confirmado a:

```text
https://github.com/Ziramog/angoweb.git main
```

## Método usado

Método: `snippet directo gtag.js`.

Motivo:

- El repo no tiene GTM instalado.
- Ya existía GA4 directo con `gtag.js` (`G-JX8JKF9ELH`).
- Para evitar duplicación, no se pegó un segundo snippet completo.
- Se mantuvo una sola instalación global de `gtag.js` y se configuraron dos destinos:

```js
gtag('config', 'G-JX8JKF9ELH');
gtag('config', 'AW-18347194194');
```

## Archivos modificados

```text
src/layouts/Layout.astro
docs/analytics-events.md
```

## Validación local

Build ejecutado:

```text
npm run build
```

Resultado:

```text
3 page(s) built
/calculadora/
/repuestos-compatibles-urvig-micron/
/index.html
```

QA browser local con URL de test:

```text
?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads&utm_content=test&utm_term=test&gclid=test123
```

Confirmado en `window.dataLayer`:

```text
config G-JX8JKF9ELH
config AW-18347194194
```

Eventos probados:

- `whatsapp_clicked` en home RG/PTO con `product_line=rg_pto`.
- `part_consulted` en landing Urvig/Micron con `product_line=urvig_micron`.
- `phone_clicked` ya sigue instrumentado desde la implementación GA4 previa.
- `lead_form_submitted` ya sigue instrumentado desde la implementación GA4 previa.

Consola browser:

```text
0 JS errors
```

## Validación producción

Producción actualizada después del push.

Verificación por `curl`:

```text
AW-18347194194 presente
G-JX8JKF9ELH presente
angoTrackEvent presente
```

Verificación browser en producción:

Home:

```text
https://www.angometalurgica.com.ar/?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads&utm_content=test&utm_term=test&gclid=test123
```

Confirmado:

```text
hasGA4Config: true
hasAdsConfig: true
configs: [G-JX8JKF9ELH, AW-18347194194]
```

Evento probado:

```text
whatsapp_clicked
product_line=rg_pto
utm_campaign=test_ango_ads
```

Landing Urvig/Micron:

```text
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads&utm_content=test&utm_term=test&gclid=test123
```

Confirmado:

```text
hasGA4Config: true
hasAdsConfig: true
```

Evento probado:

```text
part_consulted
product_line=urvig_micron
utm_campaign=test_ango_ads
```

Consola browser producción:

```text
0 JS errors
```

## Conversiones Ads

Recomendación técnica actual: importar conversiones desde GA4.

Principales:

```text
lead_form_submitted
whatsapp_clicked
phone_clicked
```

Secundarias / observación:

```text
email_clicked
catalog_downloaded
calculator_submitted
quote_form_started
part_consulted
```

## Conversion labels

No se configuraron conversion tags nativas de Google Ads porque no se recibieron `conversion_label` reales.

Faltan solo si se decide NO importar desde GA4 y usar conversiones nativas Ads:

```text
conversion_label para lead_form_submitted
conversion_label para whatsapp_clicked
conversion_label para phone_clicked
```

No inventar labels.

## Tag Assistant / GA4 DebugView

Desde Hermes se verificó producción por navegador, `dataLayer` y consola JS. No se pudo abrir sesión dentro de la cuenta Google/Tag Assistant de Antonio desde este entorno.

Pendiente de cuenta Google:

- Confirmar en Tag Assistant que aparecen `G-JX8JKF9ELH` y `AW-18347194194`.
- Confirmar en GA4 Realtime/DebugView que entran `whatsapp_clicked`, `phone_clicked` y `lead_form_submitted`.
- En Google Ads, importar desde GA4 las conversiones principales o, si se elige etiqueta nativa, pasar los `conversion_label` reales.

## Estado recomendado

Estado técnico del sitio: listo.

Recomendación operativa:

```text
Campaña puede activarse después del chequeo final de Tag Assistant/GA4 Realtime desde la cuenta de Antonio.
```

Si ese chequeo de cuenta no se hace hoy, mantener campaña pausada hasta validarlo.
