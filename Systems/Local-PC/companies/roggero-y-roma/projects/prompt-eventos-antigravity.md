# Prompt para Antigravity — Eventos de conversión GA4 (Roggero & Roma)

---

## Objetivo
Agregar eventos de conversión (`click_whatsapp`, `click_phone`, `click_maps`, `form_submit`) en el sitio de Roggero & Roma usando gtag.js directo. Sin modificar diseño ni layout.

---

## Contexto del proyecto

**Sitio:** Next.js 14 (App Router) — `C:\Projects\property-pulse-nextjs`
**Stack:** JSX, Tailwind CSS, MongoDB, NextAuth, next/script
**GA4:** Instalado via `components/GoogleAnalytics.jsx` que carga gtag.js con `analyticsId` dinámico desde DB. `window.gtag` está disponible globalmente en componentes `'use client'`.
**Deploy:** Vercel (los cambios requieren commit + push)

**Archivo clave:** `app/layout.jsx` (línea 104) — `<GoogleAnalytics analyticsId={...} />` ya está cargando gtag.

---

## Tarea específica

Agregar eventos gtag en **4 componentes** existentes. Todos son `'use client'`, así que `window.gtag` ya está disponible.

### 1. `components/Navbar.jsx`

**a) WhatsApp — escritorio (cerca de línea 154)**
Encontrar:
```jsx
<a href={`https://wa.me/${contactPhone.replace(/\D/g, '')}`} target="_blank" rel="noopener noreferrer" className="w-9 h-9 ..." aria-label="WhatsApp">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_whatsapp', {
      component: 'navbar_desktop',
      number: contactPhone.replace(/\D/g, ''),
    });
  }
}}
```

**b) Teléfono — mobile (cerca de línea 312)**
Encontrar:
```jsx
<a href={`tel:${contactPhone.replace(/\D/g, '')}`} className="flex items-center justify-center w-10 h-10 ..." aria-label="Llamar">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_phone', {
      component: 'navbar_mobile',
    });
  }
}}
```

**c) WhatsApp — mobile (cerca de línea 322)**
Encontrar:
```jsx
<a href={`https://wa.me/${contactPhone.replace(/\D/g, '')}`} target="_blank" rel="noopener noreferrer" className="flex items-center justify-center w-10 h-10 ..." aria-label="WhatsApp">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_whatsapp', {
      component: 'navbar_mobile',
      number: contactPhone.replace(/\D/g, ''),
    });
  }
}}
```

---

### 2. `components/Footer.jsx`

**a) Maps — dirección oficina (cerca de línea 70)**
Encontrar:
```jsx
<a href="https://www.google.com/maps/place/Silvia+Roggero+de+Roma+Negocios+Inmobiliarios/@..." target="_blank" rel="noopener noreferrer" className="flex items-start gap-[5px] text-[13px] ...">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_maps', {
      component: 'footer',
      type: 'office_address',
    });
  }
}}
```

**b) WhatsApp — número principal (cerca de línea 86)**
Encontrar:
```jsx
<a href={`https://wa.me/${contactPhone.replace(/\D/g, '')}`} className="text-[13px] text-white font-light hover:text-white/70 transition-colors">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_whatsapp', {
      component: 'footer',
      number: contactPhone.replace(/\D/g, ''),
    });
  }
}}
```

**c) WhatsApp — número secundario (cerca de línea 89)**
Encontrar:
```jsx
<a href="https://wa.me/5493547509413" className="text-[13px] text-white font-light hover:text-white/70 transition-colors">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_whatsapp', {
      component: 'footer',
      number: '5493547509413',
    });
  }
}}
```

**d) WhatsApp — icono social (cerca de línea 219)**
Encontrar:
```jsx
<a href={generateWhatsAppLink({ context: 'general' })} target="_blank" rel="noopener noreferrer" className="flex items-center justify-center w-[40px] h-[40px] ..." aria-label="WhatsApp">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_whatsapp', {
      component: 'footer',
      context: 'general',
    });
  }
}}
```

**e) Formulario newsletter (dentro de `handleSubscribe`, aprox línea 28)**
Antes de `setIsSubmitting(true)` (después de validar que `whatsappNumber` existe), agregar:
```js
if (typeof window !== 'undefined' && window.gtag) {
  window.gtag('event', 'form_submit', {
    component: 'footer',
    form_type: 'newsletter_whatsapp',
  });
}
```
**Importante:** No modificar la lógica del submit (ya hace fetch a `/api/subscribe`). Solo agregar el gtag antes del fetch.

**f) Maps — mobile (versión mobile del maps, cerca de línea 266)**
Encontrar:
```jsx
<a href="https://www.google.com/maps/place/Silvia+Roggero+de+Roma+Negocios+Inmobiliarios/@..." target="_blank" rel="noopener noreferrer" className="flex items-start gap-2 text-[13px] text-white/60 ...">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_maps', {
      component: 'footer_mobile',
      type: 'office_address',
    });
  }
}}
```

ADVERTENCIA: Footer.jsx tiene versión desktop y version mobile del mismo contenido. Verificar que se está modificando la variante correcta de cada elemento (desktop está dentro de `hidden md:block`, mobile dentro de `block md:hidden`).

---

### 3. `components/PropertyGallery.jsx`

**a) Maps — link a Google Maps (cerca de línea 139)**
Encontrar:
```jsx
<a href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(...)}`}
   target="_blank" rel="noopener noreferrer"
   className="inline-flex items-center gap-2 text-[#b8b8b8] ...">
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_maps', {
      component: 'property_gallery',
      property_id: property?._id || '',
      property_name: property?.name || '',
    });
  }
}}
```

**b) WhatsApp — botón "Contáctanos" (cerca de línea 212-223)**
Encontrar:
```jsx
<a
  href={`https://api.whatsapp.com/send?phone=5493547563911&text=${encodeURIComponent(...)}`}
  target="_blank"
  rel="noopener noreferrer"
  className="block w-full text-white text-[15px] ..."
>
  Contáctanos
</a>
```
Agregar `onClick`:
```jsx
onClick={() => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'click_whatsapp', {
      component: 'property_gallery',
      property_id: property?._id || '',
      property_name: property?.name || '',
      number: '5493547563911',
    });
  }
}}
```

---

### 4. `components/FeaturedPropertyCard.jsx` (opcional — verificar)

Este componente renderiza cards en el listado de propiedades. Cada card es un `<Link>` que navega a la property page. No tiene acción de WhatsApp directa — el WhatsApp está en la página de detalle. **No modificar a menos que tenga un botón de WhatsApp explícito.** Si tiene uno (revisar), agregar el mismo patrón.

---

## Archivos a modificar (lista definitiva)

| Archivo | Eventos a agregar |
|---|---|
| `components/Navbar.jsx` | 3 eventos: WhatsApp desktop, Phone mobile, WhatsApp mobile |
| `components/Footer.jsx` | 6 eventos: Maps desktop, WhatsApp ppal, WhatsApp sec, WhatsApp icono, Newsletter form, Maps mobile |
| `components/PropertyGallery.jsx` | 2 eventos: Maps, WhatsApp "Contáctanos" |

**No tocar:**
- `app/layout.jsx` — no necesita cambios
- `components/GoogleAnalytics.jsx` — no modificar
- `utils/whatsapp.js` — no modificar
- Cualquier archivo de admin, API o modelos

---

## Restricciones

1. NO modificar diseño, layout, colores, clases CSS ni contenido visible
2. NO romper la funcionalidad existente (los links y formularios deben seguir funcionando exactamente igual)
3. NO cambiar imports ni estructura de componentes
4. Todos los eventos deben usar `typeof window !== 'undefined' && window.gtag` como guard (por si gtag no cargó aún)
5. NO usar `useEffect` ni hooks adicionales — usar `onClick` inline
6. Mantener el orden de atributos: los atributos existentes primero, `onClick` al final justo antes de `>`
7. Para el form del newsletter: NO interrumpir el flujo — el gtag va ANTES del fetch, no después

---

## Criterios de aceptación

- [ ] En GA4 Realtime aparecen los eventos al hacer click (puede tardar hasta 30 seg)
- [ ] Todos los links de WhatsApp, teléfono, y maps siguen funcionando igual que antes
- [ ] El formulario de newsletter sigue enviando datos correctamente
- [ ] No hay errores en la consola del navegador relacionados con gtag
- [ ] No hay errores de type/lint en el build (`npm run build`)
- [ ] Los eventos llevan parámetros útiles: `component`, `number`, `property_name` donde corresponda

---

## Notas adicionales

- Los eventos aparecerán en GA4 como eventos personalizados. Se pueden usar directamente en Looker Studio después.
- Para identificar cada fuente: el parámetro `component` indica exactamente qué botón generó el evento (`navbar_desktop`, `navbar_mobile`, `footer`, `property_gallery`, etc.)
- Después de este cambio, en el próximo informe mensual se podrá mostrar "Clicks a WhatsApp: X" con datos reales.
