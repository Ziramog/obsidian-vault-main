---
type: handoff-summary
status: active
owner: brain-vps
company: ANGO
created-at: 2026-07-24T15:14:30-03:00
related-local-request: companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-aw-2026-07-24.md
related-handoff: Hermes/Handoffs/vps-to-local/HO-2026-07-24-001/request.md
---

# ANGO — resumen operativo Google Ads tag AW

## Qué quedó decidido

- El nuevo `LOCAL_REQUEST` de ANGO ya fue convertido en handoff oficial a `web-builder`.
- El trabajo formal quedó en:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-24-001/request.md
```

## Objetivo

Implementar y validar el Google Ads tag `AW-18347194194` sin duplicar tags ni romper GA4.

## Qué tiene que hacer web-builder

1. Inspeccionar si hoy ANGO usa GTM o snippet directo.
2. Elegir el método correcto sin duplicar `gtag`.
3. Instalar/configurar `AW-18347194194`.
4. Mantener GA4 sano.
5. Verificar Tag Assistant.
6. Verificar eventos GA4:
   - `whatsapp_clicked`
   - `phone_clicked`
   - `lead_form_submitted`
7. Confirmar si conviene importar conversiones desde GA4 o si faltan `conversion_label` reales.
8. Responder el handoff con evidencia y recomendación final.

## Regla de activación

No activar tráfico pago real si:

- el tag Ads quedó duplicado;
- GA4 dejó de medir bien;
- la etiqueta Ads no valida en Tag Assistant;
- faltan datos críticos para conversiones y no están explicitados.

## Canal oficial

ANGO no habla directo con `web-builder`. El canal oficial sigue siendo:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-24-001/
```
