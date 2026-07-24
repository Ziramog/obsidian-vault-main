---
type: LOCAL_REQUEST
status: ready-for-brain-vps-handoff
from: ango-commercial
to: brain-vps
requested-assignee: web-builder
company: ANGO
project: google-ads-2026-06
priority: high
created-at: 2026-07-24T15:10:15-03:00
reason: install-google-ads-tag-before-campaign-traffic
---

# LOCAL_REQUEST — ANGO Google Ads tag y mediciones Ads

## Contexto

Juan creó/envió la campaña inicial de Google Ads para ANGO desde la cuenta de Google de Antonio/ANGO.

La campaña usa Search para:

- Productos RG / tomas de fuerza con embrague / embragues industriales.
- Repuestos compatibles Urvig.
- Repuestos compatibles Micron.

Web-builder ya implementó las páginas y el seteo base de medición solicitado previamente. Ahora Google Ads entregó el Google tag de la cuenta/campaña.

## Google Ads tag recibido

Conversion ID / Google tag ID:

```text
AW-18347194194
```

Snippet entregado por Google Ads:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18347194194"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18347194194');
</script>
```

## Pedido para web-builder

Antes de mandar tráfico pago real, verificar e implementar correctamente el tag de Google Ads sin duplicar mediciones ni romper GA4.

### Implementación preferida

Si el sitio ya usa Google Tag Manager:

1. No pegar el snippet directo en el HTML si eso duplica tags.
2. Configurar en GTM:
   - Google tag / Google Ads tag con ID `AW-18347194194`.
   - Conversion Linker en todas las páginas.
   - Mantener GA4 existente.
3. Publicar contenedor GTM.
4. Verificar con Tag Assistant.

Si el sitio no usa GTM:

1. Instalar el snippet base de Google Ads en el `<head>` de todas las páginas.
2. No eliminar ni duplicar el GA4 existente.
3. Verificar con Tag Assistant.

## Conversiones a revisar

Google Ads puede medir conversiones de dos maneras. Definir la opción más limpia según implementación actual.

### Opción A — Importar conversiones desde GA4

Preferida si GA4 ya está midiendo bien.

Conversiones principales para importar en Google Ads:

- `lead_form_submitted`
- `whatsapp_clicked`
- `phone_clicked`

Conversiones secundarias/observación:

- `email_clicked`
- `catalog_downloaded`
- `calculator_submitted`
- `quote_form_started`

### Opción B — Google Ads conversion tags vía GTM

Usar solo si Google Ads exige etiquetas propias. Para esto hacen falta los `conversion_label` de cada acción de conversión. Juan todavía no los pasó; si Google Ads los muestra, pedirlos o leerlos desde la cuenta.

No inventar labels.

## Eventos/atributos esperados

Mantener separación por línea comercial:

```text
linea = rg_pto
linea = urvig_micron
```

Donde corresponda, enviar atributos útiles:

```text
page_type
cta_location
button_text
product_line
brand_context
```

Ejemplos:

- Clic WhatsApp en landing Urvig/Micron: `whatsapp_clicked`, `linea=urvig_micron`.
- Clic teléfono en home RG: `phone_clicked`, `linea=rg_pto`.
- Formulario enviado en landing Urvig/Micron: `lead_form_submitted`, `linea=urvig_micron`.

## URLs Ads involucradas

Home / RG / PTO:

```text
https://www.angometalurgica.com.ar/
```

Landing Urvig/Micron:

```text
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/
```

## Verificación obligatoria

Antes de marcar terminado:

1. Abrir home y landing Urvig/Micron con parámetros de prueba:

```text
?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads&utm_content=test&utm_term=test&gclid=test123
```

2. Confirmar que no se rompe navegación ni formularios.
3. Confirmar en Tag Assistant que disparan:
   - GA4.
   - Google tag `AW-18347194194` o GTM equivalente.
   - Conversion Linker si GTM está activo.
4. Confirmar en GA4 DebugView/Realtime eventos:
   - `whatsapp_clicked`.
   - `phone_clicked`.
   - `lead_form_submitted` si hay formulario.
5. Si se configuraron conversiones Google Ads nativas, confirmar en Google Ads que el estado de etiqueta no queda inactivo tras las pruebas.

## No hacer

- No crear nuevas cuentas Google Ads.
- No cambiar presupuesto ni pujas.
- No modificar textos legales/comerciales de las landings salvo corrección técnica mínima.
- No usar claims de original/oficial para Urvig/Micron.
- No pegar el snippet dos veces si ya hay GTM/gtag global.
- No escribir ni compartir credenciales, tokens ni datos de tarjeta.

## Resultado esperado

Responder a brain-vps/Juan con:

- Método usado: GTM o snippet directo.
- Captura o confirmación de Tag Assistant.
- Confirmación de eventos en GA4.
- Si faltan `conversion_label`, listar exactamente qué pide Google Ads.
- Recomendación de si la campaña puede activarse o debe quedar pausada.
