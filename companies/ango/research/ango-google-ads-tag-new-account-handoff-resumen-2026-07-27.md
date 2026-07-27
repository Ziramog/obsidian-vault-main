---
type: handoff-summary
status: active
owner: brain-vps
company: ANGO
created-at: 2026-07-27T10:58:30-03:00
related-local-request: companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-new-account-2026-07-27.md
related-handoff: Hermes/Handoffs/vps-to-local/HO-2026-07-27-001/request.md
---

# ANGO — resumen operativo migración Google Ads tag cuenta nueva

## Qué quedó decidido

- El último `LOCAL_REQUEST` de ANGO ya fue convertido en handoff oficial a `web-builder`.
- El trabajo formal quedó en:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-27-001/request.md
```

## Objetivo

Migrar el tag de Google Ads desde `AW-18347194194` a `AW-18353350898` sin romper GA4 `G-JX8JKF9ELH` ni duplicar medición.

## Qué tiene que hacer web-builder

1. Confirmar implementación actual `gtag` directa.
2. Reemplazar el tag Ads viejo por el nuevo.
3. Mantener GA4 sano.
4. Preservar eventos y parámetros existentes.
5. Verificar home + landing Urvig/Micron.
6. Probar eventos y separación `rg_pto` vs `urvig_micron`.
7. Responder con estado `LISTO / NO LISTO` y decisión de activación.

## Regla de activación

No activar campaña con cuenta nueva si:

- sigue presente el tag viejo sin justificación;
- hay riesgo de duplicación;
- GA4 deja de medir;
- fallan eventos principales;
- no queda evidencia clara en `response.md`.

## Canal oficial

ANGO no habla directo con `web-builder`. El canal oficial es:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-27-001/
```