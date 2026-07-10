# Handoff local — Mejoras GA4 para wolfim.com

**Fecha:** 2026-07-09  
**Para:** brain-local / web-builder / Juan trabajando en la página  
**Desde:** wolfim-growth  
**Sitio:** `https://www.wolfim.com`  
**GA4 Property ID:** `539238403`  
**Measurement ID:** `G-D7E290M8PW`  
**Auditoría base:** `companies/wolfim/research/wolfim-ga4-audit-2026-07-09.md`

---

## Objetivo

Ordenar GA4 para que Wolfim pueda medir oportunidades comerciales reales sin ensuciar la lectura con clicks propios, eventos duplicados o conversiones mal definidas.

Hoy GA4 **está instalado y recibe datos**, pero marca **0 conversiones** porque los key events configurados no coinciden con los eventos reales que dispara la web.

---

## Estado actual verificado

### Instalación

- `wolfim.com` redirige a `www.wolfim.com` correctamente.
- GA4 instalado con `gtag.js` directo.
- Measurement ID detectado en producción: `G-D7E290M8PW`.
- No hay GTM detectado.
- No se detectó doble instalación del tag.

Snippet actual detectado:

```js
gtag('config', 'G-D7E290M8PW');
```

### Datos últimos 30 días completos

Rango auditado: `2026-06-09` a `2026-07-08`.

| Métrica | Valor |
|---|---:|
| Usuarios activos | 249 |
| Sesiones | 353 |
| Vistas | 553 |
| Eventos | 1.618 |
| Key events / conversiones | 0 |
| Engagement rate | 33,14% |
| Bounce rate | 66,86% |

### Eventos reales detectados

| Evento | Cantidad | Usuarios |
|---|---:|---:|
| `page_view` | 553 | 249 |
| `scroll` | 190 | 95 |
| `click_project` | 18 | 4 |
| `view_pricing` | 8 | 7 |
| `click_whatsapp` | 6 | 2 |
| `form_start` | 4 | 1 |
| `form_submit_diagnostico` | 3 | 1 |
| `click_service` | 2 | 2 |
| `whatsapp_click` | 2 | 1 |

### Key events actualmente configurados en GA4

Estos existen, pero **no se disparan**:

- `close_convert_lead`
- `qualify_lead`
- `purchase`

Conclusión: la web dispara eventos útiles, pero GA4 está mirando otros nombres.

---

## Nota importante sobre clicks propios

Juan aclaró que algunos clicks a WhatsApp pueden ser propios.

Por eso el objetivo no es decir “6 leads”, sino separar:

1. **Interacciones reales registradas** — lo que GA4 ve.
2. **Leads calificados reales** — lo que Juan confirma manualmente.
3. **Tráfico interno/test** — clicks hechos por Juan o por el equipo.

No tomar `click_whatsapp` como venta ni como lead cerrado. Tomarlo como **intención de contacto**.

---

## Prioridad 1 — Unificar eventos de WhatsApp

Hoy hay dos nombres:

- `click_whatsapp`
- `whatsapp_click`

Esto fragmenta la lectura.

### Decisión recomendada

Usar solo:

```text
click_whatsapp
```

Eliminar o dejar de emitir:

```text
whatsapp_click
```

### Evento recomendado

```js
gtag('event', 'click_whatsapp', {
  cta_location: 'hero',
  cta_text: 'Hablemos por WhatsApp',
  page_context: 'home',
  whatsapp_number: '5493513157202'
});
```

No incluir datos personales del usuario ni contenido sensible.

---

## Prioridad 2 — Marcar conversiones/key events correctos en GA4

En GA4 Admin, marcar como key events:

### Conversión principal

```text
form_submit_diagnostico
```

Motivo: envío de formulario = intención comercial fuerte.

### Conversión secundaria

```text
click_whatsapp
```

Motivo: click de contacto directo. Puede incluir clicks propios, por eso leerlo como señal, no como venta.

### Micro-conversión opcional

```text
view_pricing
```

Motivo: usuario vio precios/oferta. Útil para CRO, no para contar leads.

### No usar como conversión por ahora

```text
purchase
close_convert_lead
qualify_lead
```

Esos nombres no se disparan en producción. Si se quieren usar, deben conectarse a acciones reales del sitio o del CRM. Mientras no existan, ensucian el dashboard.

---

## Prioridad 3 — Verificar número de WhatsApp

GA4 detectó clicks hacia dos números:

```text
5493513157202
5491173858454
```

Acción requerida:

- Confirmar cuál es el número oficial para Wolfim.
- Si `5491173858454` es viejo o no corresponde, reemplazar todos los links por `5493513157202`.

Búsqueda sugerida en repo local:

```bash
rg "5491173858454|5493513157202|wa.me|whatsapp" .
```

---

## Prioridad 4 — Crear helper único de tracking

No repartir `gtag()` sueltos por componentes. Crear un helper único.

Ejemplo:

```ts
// src/lib/analytics.ts

type AnalyticsParams = Record<string, string | number | boolean | undefined>;

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
  }
}

export function trackEvent(eventName: string, params: AnalyticsParams = {}) {
  if (typeof window === 'undefined') return;
  if (typeof window.gtag !== 'function') return;

  window.gtag('event', eventName, {
    ...params,
    page_path: window.location.pathname,
  });
}
```

Uso:

```ts
trackEvent('click_whatsapp', {
  cta_location: 'pricing_card',
  cta_text: 'Consultar Presencia Comercial',
  plan_name: 'presencia_comercial',
  whatsapp_number: '5493513157202',
});
```

---

## Prioridad 5 — Taxonomía de eventos recomendada

Mantener pocos eventos y buenos parámetros.

| Evento | Cuándo dispara | Parámetros mínimos |
|---|---|---|
| `click_whatsapp` | Click en cualquier link `wa.me` / WhatsApp | `cta_location`, `cta_text`, `page_context`, `whatsapp_number` |
| `form_start` | Usuario empieza formulario | `form_name`, `page_context` |
| `form_submit_diagnostico` | Formulario diagnóstico enviado OK | `form_name`, `page_context` |
| `view_pricing` | Usuario ve sección precios/planes | `page_context` |
| `click_pricing_plan` | Click en una tarjeta/plan | `plan_name`, `cta_location` |
| `click_project` | Click en caso/trabajo reciente | `project_name`, `project_type` |
| `click_service` | Click en servicio | `service_name` |

Evitar crear nombres distintos para cada botón. El contexto va en parámetros.

---

## Prioridad 6 — Custom dimensions en GA4

Crear custom dimensions para poder leer los parámetros en reportes.

Admin → Custom definitions → Create custom dimension.

| Nombre GA4 | Scope | Event parameter |
|---|---|---|
| CTA location | Event | `cta_location` |
| CTA text | Event | `cta_text` |
| Page context | Event | `page_context` |
| WhatsApp number | Event | `whatsapp_number` |
| Form name | Event | `form_name` |
| Plan name | Event | `plan_name` |
| Project name | Event | `project_name` |
| Service name | Event | `service_name` |

Hoy no hay custom dimensions configuradas.

---

## Prioridad 7 — Modo debug para no ensuciar datos

Como Juan está trabajando en la página, separar pruebas de producción.

### Opción simple

Agregar parámetro `debug_mode` cuando se esté testeando:

```js
gtag('event', 'click_whatsapp', {
  cta_location: 'test',
  debug_mode: true
});
```

### Opción mejor

No disparar eventos si el ambiente no es producción:

```ts
const isProd = window.location.hostname === 'www.wolfim.com';
if (!isProd) return;
```

### Opción para excluir tráfico interno

Crear comparación/audiencia en GA4 para filtrar:

- tráfico con `debug_mode = true`
- tráfico desde dominios de preview/development
- tráfico desde `vercel.com / referral`

No usar clicks de prueba como leads.

---

## Prioridad 8 — Medición de `/diagnostico`

`/diagnostico` es la landing con mayor interés de campaña.

Datos reales últimos 30 días:

| Métrica | Valor |
|---|---:|
| Sesiones landing `/diagnostico` | 162 |
| Usuarios | 157 |
| Vistas página `/diagnostico` | 208 |
| Clicks WhatsApp desde `/diagnostico` | 4 |
| Form starts | 4 |
| Form submits | 3 |

### Implementar tracking específico

Formulario:

```ts
trackEvent('form_start', {
  form_name: 'diagnostico_web',
  page_context: 'diagnostico',
});
```

```ts
trackEvent('form_submit_diagnostico', {
  form_name: 'diagnostico_web',
  page_context: 'diagnostico',
});
```

WhatsApp diagnóstico:

```ts
trackEvent('click_whatsapp', {
  cta_location: 'diagnostico_landing',
  cta_text: 'Quiero mi diagnóstico gratuito',
  page_context: 'diagnostico',
  whatsapp_number: '5493513157202',
});
```

---

## Prioridad 9 — UTM de campañas

Para Meta Ads, usar UTMs consistentes.

Formato recomendado:

```text
utm_source=meta
utm_medium=paid_social
utm_campaign=diagnostico_web_pymes_jul_2026
utm_content={{creative_name_or_variant}}
utm_term={{audience_or_adset}}
```

No cambiar nombres entre campañas sin documentarlo.

---

## Checklist de implementación

### Código

- [ ] Confirmar número oficial de WhatsApp.
- [ ] Reemplazar números viejos si corresponde.
- [ ] Crear helper `trackEvent()`.
- [ ] Unificar WhatsApp en `click_whatsapp`.
- [ ] Eliminar/dejar de emitir `whatsapp_click`.
- [ ] Trackear `form_start`.
- [ ] Trackear `form_submit_diagnostico` solo cuando el envío fue exitoso.
- [ ] Trackear `view_pricing` una sola vez por sesión/sección visible.
- [ ] Trackear `click_pricing_plan` si hay tarjetas de planes.
- [ ] Trackear `click_project` con `project_name`.
- [ ] Trackear `click_service` con `service_name`.
- [ ] Evitar eventos en preview/dev o marcarlos con `debug_mode`.

### GA4 Admin

- [ ] Marcar `form_submit_diagnostico` como key event.
- [ ] Marcar `click_whatsapp` como key event secundario.
- [ ] Opcional: marcar `view_pricing` como micro-conversión.
- [ ] Crear custom dimensions.
- [ ] Revisar/eliminar key events que no se usan: `purchase`, `qualify_lead`, `close_convert_lead`.
- [ ] Crear reporte/Explore simple: landing page × evento × fuente.

### Verificación

- [ ] Abrir GA4 DebugView.
- [ ] Probar home: click en WhatsApp.
- [ ] Probar `/diagnostico`: iniciar formulario.
- [ ] Probar `/diagnostico`: enviar formulario real o de test.
- [ ] Verificar que cada acción aparece una sola vez.
- [ ] Verificar parámetros: `cta_location`, `form_name`, `page_context`, etc.
- [ ] Verificar que no aparece `whatsapp_click` nuevo.

---

## Criterio de éxito

Después del cambio, GA4 debería poder responder:

1. ¿Cuántas consultas reales generó `/diagnostico`?
2. ¿Cuántas fueron por formulario y cuántas por WhatsApp?
3. ¿Qué campaña/fuente trajo esas consultas?
4. ¿Qué plan o CTA genera más intención?
5. ¿Qué clicks fueron prueba interna y cuáles son tráfico útil?

Si no responde esas 5 preguntas, la medición sigue incompleta.

---

## Nota para el informe comercial

No presentar `click_whatsapp` como lead cerrado. Presentarlo como:

> “Clicks de intención hacia WhatsApp”.

Y aclarar que algunos pueden ser pruebas internas mientras Juan trabaja en la página.

El lead real se confirma cuando llega la conversación o el formulario con datos válidos.
