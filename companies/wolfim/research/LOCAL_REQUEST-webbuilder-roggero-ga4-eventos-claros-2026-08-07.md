---
title: LOCAL_REQUEST webbuilder — Roggero & Roma GA4 eventos claros
client: Roggero & Roma
type: LOCAL_REQUEST
requester: wolfim-growth
target_profile: web-builder
created: 2026-08-07
priority: high
status: ready-for-brain-vps-handoff
reason: reemplazar medición ambigua de form_start por eventos comerciales explícitos
---

# LOCAL_REQUEST — Roggero & Roma GA4 eventos claros

## Pedido

Implementar desde local una medición GA4 explícita para Roggero & Roma, separando búsquedas/filtros de propiedades de señales reales de contacto.

El objetivo es que el próximo informe no tenga eventos ambiguos tipo `form_start`, porque hoy GA4 mezcla buscador, filtros y formularios simples bajo el mismo nombre y genera confusión comercial.

## Contexto operativo

- No modificar desde VPS.
- Ejecutar desde local / repo real del sitio.
- Mantener la exclusión de tráfico interno por login/rol y rutas admin.
- No enviar PII a GA4: no mandar teléfono, email, nombre, mensajes, user_id personal ni datos identificables.
- Usar el Measurement ID actual desde variables/config existente. No hardcodear credenciales en el código.

## Problema actual

GA4 registra `form_start` como evento automático de "Inicio de formulario".

En el período 2026-07-07 a 2026-08-06 hubo 20 eventos, pero se reparten entre:

| Página | Eventos | Interpretación probable |
|---|---:|---|
| `/` | 8 | buscador de home y/o campo de WhatsApp/suscripción |
| `/properties` | 3 | buscador/filtros del catálogo |
| `/properties?operation=venta` | 3 | filtros del catálogo |
| otras URLs de `/properties` con filtros | 6 | búsquedas/filtros |

Conclusión: `form_start` no sirve para reporte comercial. No significa consulta ni lead; solo indica que alguien empezó a interactuar con algún formulario.

## Decisión comercial

No usar `form_start` en informes a Roggero hasta que esté separado en eventos propios.

Medir estas acciones con nombres claros:

1. búsqueda/filtro del catálogo;
2. vista de ficha de propiedad;
3. click de WhatsApp/contacto;
4. envío real de formulario, si existe;
5. suscripción/WhatsApp capture, si realmente existe como lead.

## Eventos a implementar

### 1. `property_search_submitted`

**Cuándo disparar:** cuando el usuario ejecuta explícitamente una búsqueda en el catálogo o home con botón Buscar / submit.

**No disparar:** cada vez que escribe una letra.

**Parámetros sugeridos:**

| Parámetro | Ejemplo | Nota |
|---|---|---|
| `search_term` | `potrero de garay` | Sin PII. Si hay duda, limpiar/truncar a 80 chars. |
| `property_type` | `Casa` | Si aplica. |
| `operation` | `venta` | Si aplica. |
| `sort` | `price-desc` | Si aplica. |
| `area_range` | `0-500` | Si aplica. |
| `source_page` | `/` o `/properties` | De dónde buscó. |
| `result_count` | `12` | Solo si está disponible sin costo extra. |

### 2. `property_filter_used`

**Cuándo disparar:** cuando el usuario aplica un filtro sin necesariamente hacer una búsqueda textual.

**Parámetros sugeridos:**

| Parámetro | Ejemplo |
|---|---|
| `filter_name` | `type` / `operation` / `sort` / `area` |
| `filter_value` | `Casa` / `venta` / `price-asc` |
| `source_page` | `/properties` |

Si el UX aplica todos los filtros con un único submit, puede omitirse este evento y usar solo `property_search_submitted`.

### 3. `property_viewed`

**Cuándo disparar:** cuando el usuario abre una ficha individual de propiedad.

Este evento ya apareció en GA4. Revisar si está bien implementado y completar parámetros.

**Parámetros sugeridos:**

| Parámetro | Ejemplo | Nota |
|---|---|---|
| `property_id` | id interno | OK si no es PII. |
| `property_title` | dirección/título público | OK si ya es público. |
| `property_type` | `Casa` | Si existe. |
| `operation` | `venta` / `alquiler` | Si existe. |
| `city` | `Alta Gracia` | Si existe. |
| `source_page` | `/properties` | Si se conoce. |

### 4. `property_contact_clicked`

**Cuándo disparar:** cuando el usuario hace click en una acción de contacto desde una propiedad.

Esto debe ser la señal comercial principal.

**Parámetros sugeridos:**

| Parámetro | Ejemplo |
|---|---|
| `contact_method` | `whatsapp` / `phone` / `email` |
| `cta_location` | `property_card` / `property_detail` / `floating_button` |
| `property_id` | id interno si aplica |
| `property_type` | `Casa` |
| `operation` | `venta` |

**Importante:** no mandar el número de teléfono ni el mensaje de WhatsApp como parámetro.

### 5. `whatsapp_lead_submitted`

**Cuándo disparar:** solo si el formulario de "Tu nro. de WhatsApp" realmente captura un dato o dispara una acción de contacto.

**No usar para:** el buscador/filtros.

**Parámetros sugeridos:**

| Parámetro | Ejemplo |
|---|---|
| `form_location` | `home` / `footer` / `properties` |
| `lead_type` | `whatsapp_callback` |

**Importante:** no mandar el teléfono ingresado.

### 6. `contact_form_submitted`

**Cuándo disparar:** solo si hay un formulario real de contacto enviado correctamente.

**Parámetros sugeridos:**

| Parámetro | Ejemplo |
|---|---|
| `form_location` | `contact_page` / `property_detail` |
| `lead_type` | `general_contact` / `property_inquiry` |
| `property_id` | solo si aplica |

## Eventos que NO deben usarse en informes comerciales

| Evento | Motivo |
|---|---|
| `form_start` | Ambiguo. Mezcla buscador, filtros y campos sueltos. |
| `click` | Demasiado genérico. No dice intención real. |
| `scroll` | Métrica de comportamiento, no señal comercial. |

## Recomendación GA4 Admin

Si Juan o quien tenga acceso a GA4 puede hacerlo, revisar:

`Admin → Data streams → Web stream → Enhanced measurement → Form interactions`

Opción recomendada:

- Desactivar **Form interactions** si genera `form_start`/`form_submit` automáticos ambiguos.
- Mantener page views, scroll y outbound clicks si no generan ruido.

Si no se desactiva, el generador de informes debe ignorar `form_start`.

## Custom dimensions a crear en GA4

Crear definiciones personalizadas event-scoped para poder reportar por propiedad/filtro/contacto.

| Nombre visible | Scope | Event parameter |
|---|---|---|
| Property ID | Event | `property_id` |
| Property Type | Event | `property_type` |
| Operation | Event | `operation` |
| Contact Method | Event | `contact_method` |
| CTA Location | Event | `cta_location` |
| Form Location | Event | `form_location` |
| Lead Type | Event | `lead_type` |
| Search Term | Event | `search_term` |

Si hay límite de dimensiones, priorizar:

1. `property_id`
2. `contact_method`
3. `cta_location`
4. `property_type`
5. `operation`
6. `form_location`

## Guardia de tráfico interno

Mantener o implementar una guardia común antes de enviar cualquier evento:

```js
canTrackAnalytics({ pathname, userRole, isLoggedIn })
```

Debe devolver `false` si:

- ruta empieza con `/admin`;
- ruta empieza con `/superadmin`;
- usuario logueado tiene rol `admin` o `superadmin`;
- entorno es development/test si corresponde.

La misma guardia tiene que aplicar a:

- page views;
- `property_viewed`;
- búsquedas/filtros;
- WhatsApp/clicks;
- formularios.

## Ejemplo de wrapper esperado

```js
export function trackEvent(eventName, params = {}) {
  if (!canTrackAnalytics(/* contexto actual */)) return;
  if (typeof window === 'undefined') return;
  if (typeof window.gtag !== 'function') return;

  window.gtag('event', eventName, {
    ...params,
    debug_mode: process.env.NODE_ENV !== 'production',
  });
}
```

No copiar textual si el proyecto ya tiene helper propio; adaptar al patrón actual del repo.

## Validación obligatoria

Validar en GA4 DebugView o Realtime.

### Caso 1 — usuario público en incógnito

- Home: ejecutar búsqueda.
- Esperado: `property_search_submitted`.
- No depender de `form_start`.

### Caso 2 — catálogo `/properties`

- Aplicar filtro tipo Casa / Venta.
- Esperado: `property_search_submitted` o `property_filter_used`.

### Caso 3 — ficha de propiedad

- Abrir una propiedad.
- Esperado: `property_viewed` con `property_id`.

### Caso 4 — WhatsApp/contacto

- Click en WhatsApp desde ficha o card.
- Esperado: `property_contact_clicked` con `contact_method=whatsapp` y ubicación.

### Caso 5 — admin logueado

- Loguearse como admin/superadmin.
- Navegar home, catálogo y admin.
- Esperado: no se envía ningún evento GA4.

## Criterio de aceptación

- El próximo informe puede mostrar búsquedas/filtros sin mencionar `form_start`.
- Las señales de contacto quedan separadas de la navegación exploratoria.
- No se envía PII a GA4.
- El tráfico interno queda excluido para page views y eventos custom.
- Hay evidencia de DebugView o Realtime para cada evento implementado.

## Nota para brain-vps

Este archivo está marcado como `LOCAL_REQUEST` y queda dentro de zona Wolfim. Brain-vps debe crear o validar el handoff oficial hacia web-builder en `Hermes/Handoffs/vps-to-local/` según Sync V6.
