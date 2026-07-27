---
type: LOCAL_REQUEST
status: ready-for-brain-vps-handoff
from: ango-commercial
to: brain-vps
requested-assignee: web-builder
company: ANGO
project: google-ads-2026-06
priority: high
created-at: 2026-07-27T10:46:22-03:00
reason: new-google-ads-account-created-for-card-postpay
---

# LOCAL_REQUEST — ANGO reemplazar Google Ads tag por cuenta nueva

## Contexto

Juan tuvo que crear una cuenta nueva de Google Ads porque la cuenta anterior quedó bloqueada en modalidad prepago/Banelco y no permitía cambiar a pospago con tarjeta.

La cuenta/campaña anterior tenía instalado y verificado:

```text
AW-18347194194
```

La cuenta nueva generó un nuevo Google Ads tag:

```text
AW-18353350898
```

## Pedido

Actualizar la implementación de medición Google Ads en producción para usar la cuenta nueva.

## Snippet entregado por Google Ads para cuenta nueva

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18353350898"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18353350898');
</script>
```

## Requerimiento técnico

Como no hay GTM y la implementación es `gtag` directo:

1. Reemplazar o migrar el destino Google Ads viejo `AW-18347194194` por el nuevo `AW-18353350898`.
2. Mantener GA4 activo sin cambios:

```text
G-JX8JKF9ELH
```

3. Evitar duplicar tags o disparar dos Ads tags si no es intencional.
4. Mantener `window.gtag` y `dataLayer` funcionando.
5. Mantener eventos existentes:
   - `whatsapp_clicked`
   - `phone_clicked`
   - `lead_form_submitted`
   - `email_clicked`
6. Mantener parámetros:
   - `product_line`
   - `cta_location`
   - `page_path`
   - `page_location`
   - `ad_group_intent` en CTAs clave
   - UTMs completas si están en URL

## Páginas a verificar

```text
https://www.angometalurgica.com.ar/
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/
```

URLs de prueba:

```text
https://www.angometalurgica.com.ar/?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads_new_account&utm_content=test&utm_term=test&gclid=test123
```

```text
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads_new_account&utm_content=test&utm_term=test&gclid=test123
```

## Criterio de aceptación

Responder con:

```text
Estado: LISTO / NO LISTO

Implementación:
- Método: gtag directo
- Google Ads tag nuevo AW-18353350898: confirmado / no confirmado
- Google Ads tag viejo AW-18347194194: removido / sigue presente / justificación
- GA4 G-JX8JKF9ELH: confirmado / no confirmado
- Riesgo de duplicación: sí / no

Eventos probados:
- whatsapp_clicked: ok / falla
- phone_clicked: ok / falla
- lead_form_submitted: ok / falla / no hay formulario
- email_clicked: ok / falla / no hay email

Separación por línea:
- rg_pto: ok / no
- urvig_micron: ok / no

Decisión:
- Se puede activar campaña con cuenta nueva: sí / no
- Pendientes antes de activar:
```

## No hacer

- No tocar presupuesto ni campañas Google Ads.
- No guardar credenciales ni datos de tarjeta.
- No cambiar copy legal/comercial de Urvig/Micron.
- No reintroducir claims de original/oficial.
