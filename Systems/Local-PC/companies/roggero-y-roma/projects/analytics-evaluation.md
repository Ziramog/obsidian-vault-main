# Evaluación de analytics — Roggero & Roma

> Basado en revisión del código fuente: 26 junio 2026

---

## Estado actual

### ✅ Lo que ya funciona

| Componente | Estado | Detalle |
|---|---|---|
| GA4 (gtag.js) | ✅ ACTIVO | `GoogleAnalytics.jsx` — carga gtag con Measurement ID dinámico desde `siteConfig.analyticsId` |
| Facebook Pixel | ✅ ACTIVO | Mismo componente, con `siteConfig.facebookPixelId` |
| PageView tracking | ✅ ACTIVO | `send_page_view: true` y `page_path` update en SPA navigations |
| Site config | ✅ | `analyticsId` y `facebookPixelId` vienen de DB via `getSiteConfig()` |

### ❌ Lo que falta

| Componente | Estado | Impacto |
|---|---|---|
| **Google Tag Manager** | ❌ NO | Se usa gtag.js directo. No hay GTM. |
| **Eventos de conversión** | ❌ NO | No se trackea ningún evento (ni siquiera un click genérico) |
| **Search Console** | ❌ NO | No está conectado |
| **Looker Studio** | ❌ NO | No hay dashboard |
| **Google Sheets (leads)** | ❌ NO | No hay planilla |

---

## Elementos trackeables en el código

### WhatsApp (3 variantes distintas)

| Ubicación | Link | Cómo detectarlo |
|---|---|---|
| `Navbar.jsx:154` — Escritorio | `https://wa.me/${contactPhone}` | URL contiene `wa.me/` |
| `Navbar.jsx:322` — Mobile | `https://wa.me/${contactPhone}` | URL contiene `wa.me/` |
| `Footer.jsx:86,89` | `https://wa.me/${contactPhone}`, `https://wa.me/5493547509413` | URL contiene `wa.me/` |
| `Footer.jsx:219` | `generateWhatsAppLink({ context: 'general' })` | Función que genera `wa.me/` |
| `PropertyGallery.jsx:213` | `https://api.whatsapp.com/send?phone=5493547563911` | URL contiene `api.whatsapp.com` |

**Nota:** Hay 3 números diferentes:
- `contactPhone` (Navbar, Footer) → viene de DB
- `5493547509413` (Footer hardcodeado)
- `5493547563911` (PropertyGallery + whatsapp.js utility)

### Teléfono

| Ubicación | Link |
|---|---|
| `Navbar.jsx:312` — Mobile | `tel:${contactPhone}` |

### Mapas

| Ubicación | Link |
|---|---|
| `PropertyGallery.jsx:139-141` (cada propiedad) | `https://www.google.com/maps/search/?api=1&query=...` |
| `Footer.jsx:70` | `https://www.google.com/maps/place/...` (fijo oficina) |

### Formularios

| Ubicación | Tipo |
|---|---|
| `Footer.jsx:166,336` — Newsletter | Formulario de suscripción con input tel + submit |
| `admin/` — Admin panel | Formularios de alta/edición (no comerciales) |

### PDF / Descargas
- ❌ No se encontraron enlaces a PDF en el código

---

## Decisión técnica: ¿GTM o gtag.js directo?

| Aspecto | GTM | gtag.js directo |
|---|---|---|
| Tiempo de implementación | 2-3h (instalar + migrar + configurar eventos) | 30min (agregar eventos en código) |
| Flexibilidad futura | Alta — configuración desde UI sin tocar código | Baja — cada nuevo evento requiere deploy |
| Dependencia del dev | Setup inicial + snippet | Cada evento requiere modificar componente |
| Recomendado para | Clientes que pueden querer ajustar eventos solos | Sitios estáticos sin cambios frecuentes |

**Recomendación:** Como Roggero & Roma usa Next.js con deploy (Vercel), agregar eventos directo con gtag.js es más rápido y no requiere migración. Pero si el plan es que a futuro vos o el cliente puedan configurar eventos sin deploy, GTM es mejor.

---

## Plan de acción propuesto

### Opción A — Rápida (gtag.js directo, 30 min)
1. Agregar `gtag('event', 'click_whatsapp', ...)` en Navbar, Footer y PropertyGallery
2. Agregar `gtag('event', 'click_map', ...)` en PropertyGallery y Footer
3. Agregar `gtag('event', 'form_submit', ...)` en Footer newsletter
4. Agregar `gtag('event', 'click_phone', ...)` en Navbar mobile

### Opción B — Profesional (GTM, 2-3h)
1. Crear contenedor GTM
2. Migrar de gtag.js directo a GTM (GTM puede cargar gtag)
3. Configurar triggers y eventos en GTM
4. Publicar contenedor

---

## Archivos a tocar (para cualquiera de las dos opciones)

| Archivo | Qué tiene |
|---|---|
| `app/layout.jsx` | Layout raíz — añadir snippet GTM si se elige Opción B |
| `components/GoogleAnalytics.jsx` | Componente actual de analytics — migrar a GTM o extender con eventos |
| `components/Navbar.jsx` | WhatsApp link (líneas 154, 322) + tel (line 312) |
| `components/Footer.jsx` | WhatsApp (86, 89, 219) + Maps (70) + Form (166, 336) |
| `components/PropertyGallery.jsx` | WhatsApp CTA (213) + Maps link (139) |
| `components/FeaturedPropertyCard.jsx` | (No tiene eventos directos, el link va a la property page) |
