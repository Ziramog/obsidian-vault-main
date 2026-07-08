---
title: Roggero & Roma — Implementación GA4 desde código
client: Roggero & Roma
type: technical-implementation-plan
owner: wolfim-growth
created: 2026-07-07
status: ready-for-handoff
source_audit: roggero-roma-ga4-audit-2026-07-07.md
---

# Roggero & Roma — Implementación GA4 desde código

## Objetivo

Dejar GA4 listo para un informe comercial mensual a Franco:

1. Medir tráfico público real.
2. No contaminar métricas con `/admin`, panel, edición ni testing interno.
3. Medir intención comercial: WhatsApp, formulario, teléfono/email.
4. Medir interés por propiedad/filtro.
5. Marcar conversiones/key events útiles.

## Diagnóstico actual confirmado vía API

- GA4 funciona y recibe datos.
- Measurement ID: `G-PW4FH9WHQB`.
- Property ID: `539918073`.
- Período 2026-06-28 → 2026-07-07:
  - 56 usuarios activos.
  - 89 sesiones.
  - 355 vistas brutas.
  - 83 vistas aprox. de admin/interno.
  - 0 key events.
  - 1 click saliente a WhatsApp + 1 evento `click_whatsapp` parcial.
  - `form_start` existe, `form_submit` no aparece.

## Decisión técnica recomendada

Usar **gtag.js directo**, no GTM, por ahora.

Motivo:

- El sitio ya tiene `GoogleAnalytics.jsx`.
- GA4 se carga desde `siteConfig.analyticsId`.
- Para este cliente alcanza con eventos explícitos en código.
- Es más rápido y controlado que migrar a GTM.

GTM puede evaluarse después si Wolfim quiere operar eventos desde UI sin deploy.

## Archivos esperados a tocar

Según evaluación previa del código:

| Archivo | Cambio |
|---|---|
| `components/GoogleAnalytics.jsx` | Desactivar pageview automático, excluir admin, enviar pageviews manuales limpias |
| `lib/analytics.js` o `utils/analytics.js` | Crear helper `trackEvent` y helpers específicos |
| `components/Navbar.jsx` | Trackear WhatsApp y teléfono |
| `components/Footer.jsx` | Trackear WhatsApp, mapa, formulario, Instagram si se desea |
| `components/PropertyGallery.jsx` | Trackear WhatsApp por propiedad y mapa por propiedad |
| Página/componente de detalle de propiedad | Trackear `property_viewed` |
| Componente de filtros/buscador | Trackear `search_used` / `filter_applied` |

## 1. Crear helper de Analytics

Crear `lib/analytics.js` o equivalente.

```js
export const isBrowser = () => typeof window !== 'undefined';

export function shouldTrackPath(pathname = '') {
  if (!pathname) return true;
  return !(
    pathname.startsWith('/admin') ||
    pathname.startsWith('/api')
  );
}

export function cleanParams(params = {}) {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) =>
      value !== undefined && value !== null && value !== ''
    )
  );
}

export function trackEvent(eventName, params = {}) {
  if (!isBrowser()) return;
  if (!window.gtag) return;

  const pathname = window.location?.pathname || '';
  if (!shouldTrackPath(pathname)) return;

  window.gtag('event', eventName, cleanParams({
    page_path: pathname,
    page_location: window.location?.href,
    ...params,
  }));
}

export function trackWhatsappClick(params = {}) {
  trackEvent('click_whatsapp', {
    cta_location: params.cta_location,
    context: params.context || 'general',
    property_id: params.property_id,
    property_type: params.property_type,
    operation: params.operation,
    location: params.location,
  });
}

export function trackPhoneClick(params = {}) {
  trackEvent('click_phone', {
    cta_location: params.cta_location,
    context: params.context || 'general',
  });
}

export function trackEmailClick(params = {}) {
  trackEvent('click_email', {
    cta_location: params.cta_location,
    context: params.context || 'general',
  });
}

export function trackMapClick(params = {}) {
  trackEvent('click_map', {
    cta_location: params.cta_location,
    context: params.context || 'general',
    property_id: params.property_id,
    property_type: params.property_type,
    operation: params.operation,
    location: params.location,
  });
}

export function trackPropertyViewed(property = {}) {
  trackEvent('property_viewed', {
    property_id: property._id || property.id,
    property_type: property.type,
    operation: property.operation,
    location: property.location || property.neighborhood || property.city,
    price_currency: property.currency,
  });
}

export function trackContactFormSubmitted(params = {}) {
  trackEvent('contact_form_submitted', {
    form_name: params.form_name || 'contact',
    form_location: params.form_location,
  });
}

export function trackSearchUsed(params = {}) {
  trackEvent('search_used', {
    search_type: params.search_type || 'property_filter',
    property_type: params.property_type,
    operation: params.operation,
    location: params.location,
    has_query: Boolean(params.query),
    query_length: params.query ? String(params.query).length : 0,
  });
}
```

### Nota sobre PII

No mandar a GA4:

- nombre
- email
- teléfono
- mensaje completo del usuario
- dirección exacta si pudiera identificar a una persona privada

Para propiedad pública está bien mandar `property_id`, tipo, operación y zona.

## 2. Corregir `GoogleAnalytics.jsx`

Problema actual probable: `send_page_view: true` mide también admin y puede duplicar pageviews.

Cambiar a:

1. Cargar `gtag` con `send_page_view: false`.
2. Enviar pageviews manuales solo si la ruta no es `/admin`.
3. Usar `pathname + searchParams` reales.

Patrón para Next.js App Router:

```jsx
'use client';

import Script from 'next/script';
import { useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { shouldTrackPath } from '@/lib/analytics';

export default function GoogleAnalytics({ measurementId }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (!measurementId) return;
    if (typeof window === 'undefined') return;
    if (!window.gtag) return;
    if (!shouldTrackPath(pathname)) return;

    const query = searchParams?.toString();
    const pagePath = query ? `${pathname}?${query}` : pathname;

    window.gtag('event', 'page_view', {
      page_path: pagePath,
      page_location: window.location.href,
      page_title: document.title,
    });
  }, [measurementId, pathname, searchParams]);

  if (!measurementId) return null;

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
        strategy="afterInteractive"
      />
      <Script id="ga4-init" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          window.gtag = gtag;
          gtag('js', new Date());
          gtag('config', '${measurementId}', { send_page_view: false });
        `}
      </Script>
    </>
  );
}
```

Si el sitio usa Pages Router, adaptar a `router.asPath`.

## 3. Trackear WhatsApp

En cada link de WhatsApp, agregar `onClick`.

### Navbar general

```jsx
import { trackWhatsappClick } from '@/lib/analytics';

<a
  href={`https://wa.me/${contactPhone}`}
  onClick={() => trackWhatsappClick({
    cta_location: 'navbar_desktop',
    context: 'general',
  })}
>
  WhatsApp
</a>
```

Mobile:

```jsx
onClick={() => trackWhatsappClick({
  cta_location: 'navbar_mobile',
  context: 'general',
})}
```

### Footer

```jsx
onClick={() => trackWhatsappClick({
  cta_location: 'footer',
  context: 'general',
})}
```

### WhatsApp por propiedad

En `PropertyGallery.jsx` o donde esté el CTA:

```jsx
onClick={() => trackWhatsappClick({
  cta_location: 'property_gallery',
  context: 'property',
  property_id: property._id || property.id,
  property_type: property.type,
  operation: property.operation,
  location: property.location || property.neighborhood || property.city,
})}
```

## 4. Trackear ficha de propiedad vista

En la página/componente de detalle:

```jsx
'use client';

import { useEffect } from 'react';
import { trackPropertyViewed } from '@/lib/analytics';

export default function PropertyDetail({ property }) {
  useEffect(() => {
    if (!property) return;
    trackPropertyViewed(property);
  }, [property?._id || property?.id]);

  return (...);
}
```

Evento: `property_viewed`.

No marcarlo como conversión principal; usarlo como señal de interés.

## 5. Trackear formulario enviado

No medir el click en submit. Medir solo cuando el submit fue exitoso.

```jsx
import { trackContactFormSubmitted } from '@/lib/analytics';

async function handleSubmit(e) {
  e.preventDefault();

  const result = await submitContactForm(formData);

  if (result?.ok) {
    trackContactFormSubmitted({
      form_name: 'footer_contact',
      form_location: 'footer',
    });
  }
}
```

Evento recomendado: `contact_form_submitted`.

Si se prefiere alinearse con Enhanced Measurement de GA4, también se puede usar `form_submit`, pero para reporting comercial prefiero `contact_form_submitted`.

## 6. Trackear teléfono/email

```jsx
import { trackPhoneClick, trackEmailClick } from '@/lib/analytics';

<a href={`tel:${contactPhone}`} onClick={() => trackPhoneClick({ cta_location: 'navbar_mobile' })}>
  Llamar
</a>

<a href={`mailto:${email}`} onClick={() => trackEmailClick({ cta_location: 'footer' })}>
  Email
</a>
```

## 7. Trackear mapas

Footer:

```jsx
onClick={() => trackMapClick({
  cta_location: 'footer',
  context: 'office',
})}
```

Propiedad:

```jsx
onClick={() => trackMapClick({
  cta_location: 'property_gallery',
  context: 'property',
  property_id: property._id || property.id,
  property_type: property.type,
  operation: property.operation,
  location: property.location || property.neighborhood || property.city,
})}
```

## 8. Trackear búsquedas/filtros

Cuando el usuario aplica filtros o búsqueda:

```jsx
import { trackSearchUsed } from '@/lib/analytics';

function applyFilters(filters) {
  // lógica existente

  trackSearchUsed({
    search_type: 'property_filter',
    property_type: filters.type,
    operation: filters.operation,
    location: filters.location,
    query: filters.term,
  });
}
```

Si se dispara en cada cambio, usar debounce o solo trackear al hacer submit/click en buscar.

## 9. Key events en GA4

Después del deploy y de verificar que los eventos llegan, marcar como key events:

| Evento | Marcar como key event |
|---|---|
| `click_whatsapp` | Sí |
| `contact_form_submitted` | Sí |
| `click_phone` | Opcional |
| `property_viewed` | No, solo microseñal |
| `search_used` | No |
| `click_map` | No |

Con rol Viewer no se puede configurar desde Hermes. Requiere Editor o hacerlo manualmente en GA4.

## 10. Custom dimensions recomendadas

Para que GA4 permita cruzar reportes por propiedades/filtros, crear custom dimensions event-scoped:

| Nombre UI | Event parameter |
|---|---|
| CTA location | `cta_location` |
| Context | `context` |
| Property ID | `property_id` |
| Property type | `property_type` |
| Operation | `operation` |
| Location | `location` |
| Form name | `form_name` |
| Form location | `form_location` |
| Search type | `search_type` |
| Has query | `has_query` |

No crearía `property_title` como custom dimension si hay muchas propiedades; puede aumentar cardinalidad. Para reportes, usar `pageTitle` + `pagePath` o cruzar `property_id` con base propia.

## 11. Validación post-deploy

### En navegador

1. Abrir sitio público en incógnito.
2. Ver consola:
   - `typeof window.gtag` debe ser `function`.
3. Click en WhatsApp.
4. En GA4 Realtime / DebugView confirmar `click_whatsapp`.
5. Abrir ficha de propiedad y confirmar `property_viewed`.
6. Enviar formulario de prueba y confirmar `contact_form_submitted`.
7. Entrar a `/admin` y confirmar que no genera pageviews públicas.

### Por API después de 10-30 minutos

Consultar eventos:

- `click_whatsapp`
- `property_viewed`
- `contact_form_submitted`
- `click_phone`
- `search_used`

## 12. Criterio de aceptación

La implementación queda lista cuando:

- [ ] GA4 sigue recibiendo `page_view` públicas.
- [ ] `/admin` no contamina el reporte público.
- [ ] `click_whatsapp` llega con `cta_location` y, si corresponde, `property_id`.
- [ ] `contact_form_submitted` aparece al enviar formulario exitoso.
- [ ] `property_viewed` aparece al abrir ficha.
- [ ] `search_used` aparece al aplicar filtros.
- [ ] `click_whatsapp` y `contact_form_submitted` están marcados como key events.
- [ ] El próximo reporte puede mostrar tráfico + propiedades + intentos de contacto.

## Mensaje para Franco después de implementar

> Franco, ya dejamos mejor medida la web: no solo vemos visitas, sino también qué propiedades mira la gente y cuándo intenta contactarse por WhatsApp o formulario. Con eso el informe mensual va a servir para tomar decisiones comerciales, no solo para ver números.
