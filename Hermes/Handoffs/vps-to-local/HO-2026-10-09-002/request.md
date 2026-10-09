---
id: HO-2026-10-09-002
status: ready
from: brain-vps
to: brain-local
project: ango
priority: normal
depends-on: []
created-at: 2026-10-09T07:20:00-03:00
acknowledge-by: next-local-session
due-at: 2026-10-13T18:00:00-03:00
escalate-after: 96h
briefing: Hermes/Briefings/current.md
director: Juan
supersedes:
  - HO-2026-07-16-001
  - HO-2026-07-22-001
  - HO-2026-07-24-001
  - HO-2026-07-27-001
---

# ANGO — consolidar landing, GA4 y Google Ads

## Decisión de Juan

El 09/10/2026 Juan decidió consolidar los cuatro handoffs ANGO de julio en un único trabajo actualizado. Los originales quedan cancelados por reemplazo; este request es la única fuente operativa.

## Objetivo verificable

Auditar el estado real actual de `https://www.angometalurgica.com.ar/` y completar en un solo ciclo únicamente lo que siga faltando para dejar:

1. landing de repuestos **compatibles** Urvig/Micron operativa;
2. GA4 `G-JX8JKF9ELH` sano y con eventos comerciales verificables;
3. Google Ads usando la cuenta/tag vigente `AW-18353350898`, sin el tag viejo `AW-18347194194` ni duplicación accidental;
4. decisión documentada: `LISTO PARA ACTIVAR` o `NO LISTO`, con bloqueo exacto.

## Primero: auditoría de vigencia

No implementar a ciegas los pedidos de julio. Antes de tocar código:

- revisar producción y repo actual;
- verificar si la landing ya existe y si está indexable/mobile;
- detectar implementación real de GA4/GTM/gtag;
- comprobar qué tags Ads están presentes;
- revisar si los eventos ya existen;
- comparar contra los cuatro requests supersedidos.

## Alcance consolidado

### Landing

- URL esperada: `/repuestos-compatibles-urvig-micron/` o equivalente vigente.
- Copy legal: `compatibles`; nunca `original`, `oficial`, `representante oficial` ni equivalentes.
- CTA mobile a WhatsApp/teléfono/formulario.
- Home conserva foco RG/PTO industrial.

### Medición

Eventos mínimos:

- `whatsapp_clicked`
- `phone_clicked`
- `lead_form_submitted` (solo submit exitoso)
- `email_clicked`

Diferenciar `product_line=rg_pto|urvig_micron|unknown` o por un mecanismo equivalente documentado.

### Ads

- GA4 a conservar: `G-JX8JKF9ELH`.
- Tag Ads vigente: `AW-18353350898`.
- Tag obsoleto a remover/confirmar ausente: `AW-18347194194`.
- No tocar presupuesto, pujas ni publicar campañas.
- No crear cuentas nuevas.

### Verificación obligatoria

- producción y mobile;
- Tag Assistant o evidencia técnica equivalente;
- GA4 Realtime/DebugView para eventos principales;
- URLs con UTM + `gclid=test123` sin romper navegación;
- ausencia de doble medición;
- archivos/rutas modificados y URL final.

## Fuentes originales (histórico, no ejecución literal)

- `Hermes/Handoffs/vps-to-local/HO-2026-07-16-001/request.md`
- `Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md`
- `Hermes/Handoffs/vps-to-local/HO-2026-07-24-001/request.md`
- `Hermes/Handoffs/vps-to-local/HO-2026-07-27-001/request.md`
- sus `LOCAL_REQUEST` referenciados.

## Criterios de aceptación

Crear `response.md` acá con:

1. estado inicial encontrado;
2. qué ya estaba resuelto y qué faltaba;
3. cambios realizados;
4. URL de landing;
5. tags GA4/Ads observados después del cambio;
6. resultado de cada evento probado;
7. evidencia concreta;
8. decisión final `LISTO PARA ACTIVAR` / `NO LISTO` y bloqueo exacto.

## Restricciones

- No publicar Ads ni gastar dinero.
- No tocar secrets, tokens, datos de tarjeta ni `Hermes/Config/`.
- No usar operaciones git destructivas.
- No inventar conversion labels.
- Si el briefing comercial vencido afecta una decisión, limitarse a auditoría técnica y escalar.