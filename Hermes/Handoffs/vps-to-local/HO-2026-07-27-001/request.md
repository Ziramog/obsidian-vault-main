---
id: HO-2026-07-27-001
status: ready
from: brain-vps
to: brain-local
project: ango
priority: high
depends-on: []
created-at: 2026-07-27T10:58:30-03:00
acknowledge-by: next-local-session
due-at: 2026-07-28T12:00:00-03:00
escalate-after: 18h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — web-builder — reemplazar Google Ads tag por cuenta nueva ANGO

## Motivo

`ango-commercial` dejó un nuevo `LOCAL_REQUEST` porque la cuenta anterior de Google Ads quedó bloqueada en prepago/Banelco y Juan tuvo que crear una cuenta nueva con tarjeta pospago. Ahora hay que reemplazar el tag viejo por el nuevo sin romper GA4 ni duplicar medición.

Fuente obligatoria:

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-new-account-2026-07-27.md
```

## Objetivo verificable

Actualizar la implementación en producción para migrar de Google Ads tag viejo a cuenta nueva:

- viejo: `AW-18347194194`
- nuevo: `AW-18353350898`
- GA4 que debe seguir sano: `G-JX8JKF9ELH`

El resultado debe dejar claro si la campaña con cuenta nueva puede activarse o no.

## Contexto mínimo a leer antes de tocar nada

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-new-account-2026-07-27.md
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-aw-2026-07-24.md
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-ga4-ads-mediciones-2026-07-22.md
Hermes/Handoffs/vps-to-local/HO-2026-07-24-001/request.md
Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md
```

## Datos técnicos

### Tag viejo

```text
AW-18347194194
```

### Tag nuevo

```text
AW-18353350898
```

### GA4 a conservar

```text
G-JX8JKF9ELH
```

## Páginas a verificar

```text
https://www.angometalurgica.com.ar/
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/
```

## URLs de prueba

```text
https://www.angometalurgica.com.ar/?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads_new_account&utm_content=test&utm_term=test&gclid=test123
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads_new_account&utm_content=test&utm_term=test&gclid=test123
```

## Pasos concretos para web-builder

Ejecutar en este orden:

1. **Inspeccionar implementación actual en producción**
   - Confirmar que hoy la implementación es `gtag` directa y no GTM.
   - Ubicar dónde está declarado el tag viejo `AW-18347194194`.
   - Confirmar cómo convive hoy con GA4 `G-JX8JKF9ELH`.

2. **Migrar el tag Ads**
   - Reemplazar o reconfigurar la implementación para que el destino Google Ads activo sea `AW-18353350898`.
   - Evitar disparar a la vez el tag viejo y el nuevo salvo que haya una justificación explícita.
   - Mantener `window.gtag` y `dataLayer` funcionando.

3. **Mantener GA4 sano**
   - No tocar ni romper `G-JX8JKF9ELH`.
   - Verificar que siga cargando correctamente después del cambio.

4. **Preservar eventos y parámetros existentes**
   - Eventos:
     - `whatsapp_clicked`
     - `phone_clicked`
     - `lead_form_submitted`
     - `email_clicked`
   - Parámetros:
     - `product_line`
     - `cta_location`
     - `page_path`
     - `page_location`
     - `ad_group_intent` en CTAs clave
     - UTMs completas si vienen en URL

5. **Verificar separación por línea comercial**
   - Confirmar que siga diferenciándose:
     - `rg_pto`
     - `urvig_micron`

6. **Probar con URLs de test**
   - Abrir ambas páginas con `utm_*` y `gclid=test123`.
   - Verificar que navegación, formularios y CTAs no se rompan.

7. **Validar implementación real**
   - Confirmar presencia del tag nuevo `AW-18353350898`.
   - Confirmar ausencia del tag viejo `AW-18347194194`, o justificar si queda presente.
   - Confirmar que GA4 sigue presente.
   - Verificar con Tag Assistant o evidencia técnica equivalente.

8. **Probar eventos**
   - `whatsapp_clicked`: ok / falla
   - `phone_clicked`: ok / falla
   - `lead_form_submitted`: ok / falla / no hay formulario
   - `email_clicked`: ok / falla / no hay email

9. **Responder este handoff**
   - Crear `response.md` en esta carpeta.
   - Incluir el bloque pedido por ANGO con este formato mínimo:

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

## Criterios de aceptación

- El tag nuevo `AW-18353350898` queda implementado.
- El tag viejo `AW-18347194194` queda removido o justificado explícitamente.
- GA4 `G-JX8JKF9ELH` sigue funcionando.
- No hay duplicación accidental de tags.
- Los eventos comerciales siguen vivos.
- Se informa con claridad si la campaña puede activarse.

## Restricciones

- No tocar presupuesto ni campañas Google Ads.
- No guardar credenciales ni datos de tarjeta.
- No cambiar copy legal/comercial de Urvig/Micron.
- No reintroducir claims de original/oficial.
- No modificar `Hermes/Config/`.
- No hacer cambios destructivos.

## Respuesta esperada en este handoff

Publicar `response.md` en esta carpeta con evidencia concreta, archivos/rutas tocados y decisión final de activación.