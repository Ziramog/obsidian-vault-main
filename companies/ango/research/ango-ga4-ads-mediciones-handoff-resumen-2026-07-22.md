---
type: handoff-summary
status: active
owner: brain-vps
company: ANGO
created-at: 2026-07-22T18:25:00-03:00
related-local-request: companies/ango/research/LOCAL_REQUEST-webbuilder-ango-ga4-ads-mediciones-2026-07-22.md
related-handoff: Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md
---

# ANGO — resumen operativo para medición GA4 / Google Ads

## Qué quedó decidido

- El `LOCAL_REQUEST` de `ango-commercial` ya fue convertido en handoff oficial a local/web-builder.
- El trabajo quedó formalizado en:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md
```

## Objetivo

Dejar lista la medición técnica para lanzar Google Ads ANGO con evidencia real, no a ciegas.

## Qué tiene que hacer web-builder

1. Validar URLs finales de:
   - home / sección RG-PTO;
   - landing Urvig/Micron.
2. Confirmar acceso a GA4 / Google Ads bajo activo de ANGO.
3. Implementar GA4 directo o GTM + GA4.
4. Medir y probar:
   - `whatsapp_clicked`
   - `phone_clicked`
   - `lead_form_submitted`
   - `email_clicked`
5. Separar conversiones por línea:
   - `urvig_micron`
   - `rg_pto`
6. Dejar UTMs listas para Google Ads.
7. Entregar evidencia real en `response.md` del handoff.

## Regla operativa

ANGO no habla directo con `web-builder`. El canal oficial para esta implementación es el handoff:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/
```

## Bloqueo crítico a vigilar

No lanzar Google Ads hasta que estén medidos y verificados al menos:

- `whatsapp_clicked`
- `phone_clicked`
- `lead_form_submitted`

Si falta acceso a cuentas o la landing definitiva todavía no está publicada, `web-builder` debe dejar el bloqueo exacto y el próximo paso concreto dentro de `response.md`.
