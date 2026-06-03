---
tags: [producto-propio, wolfim-ecosystem, stand-by, producto-vision]
status: stand-by
created: 2026-06-03
founder: juan-gomariz
---

# Korantis — Find Places by Feeling

**Tagline:** "Discover places for how you want to feel"
**URL:** https://www.korantis.com
**Status:** Stand-by (producto R&D propio de Wolfim)
**Founder:** Juan Manuel Gomariz
**Construido en:** hueco durante ausencias de 22 días (11/05–02/06) — pocas horas
**Propósito:** expandir Wolfim al mundo. "No tiene techo."
**Stack:** Next.js App Router (RSC) + Vercel + Cloudinary CDN + Cloudflare WAF

## Concepto

Motor de búsqueda de restaurantes, bares y cafeterías filtrado por **mood / vibe**, no por categoría. Único en BA. Diferenciador claro vs Google Maps, TripAdvisor, Instagram, Foursquare.

**Auditoría externa del sitio:** [[korantis-audit-2026-06-03]]
**Benchmark visual:** [[korantis-benchmark]]

## Estado del producto (al 03/06/2026)

### Lo que funciona
- **Ángulo de marca:** el "by feeling" es un hueco defendible, no copiable trivialmente
- **Hero dark + dorado/cobre:** atemporal, premium, memorable
- **Copy atmosférico:** "Bathed in the soft glow of hanging Edison bulbs…" — editorial, único
- **Tipografía dual:** serif elegante para nombres + sans para metadata
- **Performance técnica:** TTFB 53ms, FCP 936ms, 0 errores
- **WAF activo:** Vercel Security Checkpoint prendido → tráfico suficiente para proteger
- **Robots.txt con Content Signals:** decisión consciente sobre AI-training/search

### Bugs críticos (bloquean el producto)
1. **Click en chip de mood vacía la pantalla.** Probado con Playwright: cualquier click en QUIET/WARM/NATURAL LIGHT/HIDDEN GEM → lista de lugares desaparece, pantalla en negro. Es el flujo principal del producto, está roto.
2. **Filtro de mood = texto libre, no tag.** El input se llena con "quiet" en vez de filtrar por tag "QUIET". Indica mismatch entre los chips del hero y los tags reales de las cards.
3. **Copy de filtro dice "Palermo" hardcoded** aunque el selector diga "BUENOS AIRES". No se actualiza al cambiar de ciudad.
4. **Sin `<nav>` con links, sin `<footer>`, sin sitemap.xml, sin canonical URL, sin Open Graph, sin JSON-LD structured data, 0 H2.** SEO bloqueado completamente.
5. **Imágenes sin fallback visual.** Cuando una no carga, queda espacio negro.

### Lo que falta (negocio)
- 0 captura de leads (no hay form, no hay email capture, no hay newsletter)
- 0 social proof (sin reseñas, sin ratings, sin "X personas guardaron esto")
- 0 modelo de monetización visible
- 0 auth, 0 guardar lugares, 0 perfil de usuario
- 0 mapa (pero el tagline dice "find places")
- 0 notificaciones, 0 email digest
- 0 sección "Hoy en BA" o curaduría recurrente
- Sin Stripe, Hotjar, Intercom, FB Pixel, Vercel Analytics

### Inventario al 03/06/2026
- **Lugares en DB:** 30+ (Don Julio, Tres Monos, Florería Atlántico, Verne Club, Trade Sky Bar, etc.)
- **Mood tags observados:** SOFT, WARM, AMBER, GOLDEN, GREEN, BUSTLING, COZY, INTIMATE, QUIET, ATMOSPHERIC, CALM, SOCIAL, SLOW, NATURAL LIGHT, HIDDEN GEM
- **Imágenes declaradas:** 63 (~42 cargan en mi entorno headless, pero en navegador real sí funcionan)
- **Largo de la home:** ~15,825px (single-page larga, no multi-página)

## Por qué está en stand-by

SOUL marca que con semáforo 🔴 Crítico en Wolfim, trabajo en producto secundario es señal de alerta. Korantis no es un cliente ni genera USD hoy. Su lugar correcto es:

- ✅ Construir R&D mientras Wolfim tiene caja (🟠 Transición o superior)
- ❌ Construir en lugar de vender cuando Wolfim está en rojo
- ❌ Construir R&D cuando hay leads sin atender (Franco $300 mañana, Comforti/Rivas/Gamma sin datos)

## Decisión pendiente: ¿qué es Korantis?

Tres caminos posibles, en orden de madurez del producto:

### A) Korantis como Wolfim-v2 (reemplazo a largo plazo)
- Construir el loop completo: auth + guardar + mapa + filtros + recurrencia + monetización
- Timeline realista: 6-12 meses con funding o side income
- Riesgo: 12 meses sin revenue = bankruptcy
- Requisito: Wolfim generando $1k+ USD/mes en paralelo

### B) Korantis como case study de portfolio
- Mantener el sitio como showcase de las capacidades de Wolfim
- No invertir más en features, solo arreglar bugs críticos
- Usarlo en pitches a clientes premium: "no solo hago webs, también construyo productos"
- Timeline: 1-2 sprints de fix, después archivar
- Requisito: ya mostrado en wolfim.com como proyecto #004

### C) Korantis como proyecto personal / hobby
- Mantener el sitio vivo con cariño, sin presión de monetización
- Iterar en ratos libres
- Sin timeline, sin presión
- Requisito: que Juan no se frustre cuando pasen meses sin features nuevas

**Recomendación:** arrancar con B (case study + fix bugs críticos), mantener la puerta abierta a A si Wolfim llega a generar caja, descartar C porque no encaja con el perfil de Juan.

## Próximos pasos cuando se reactive

### Fixes críticos (1 sprint de 3-5 días)
- [ ] Arreglar bug del primer filtro (mismatch chips/tags)
- [ ] Implementar empty state y loading state
- [ ] Agregar fallback de imagen
- [ ] CTA primario: "Empezá a guardar lugares gratis" (aunque sea mock por ahora)
- [ ] Meta OG + canonical + JSON-LD + sitemap

### Si se elige el camino A (producto real)
- [ ] Auth con NextAuth o Clerk
- [ ] Guardar lugares + perfil
- [ ] Mapa interactivo (Mapbox o Google Maps)
- [ ] Filtros: hora, precio, distancia
- [ ] Sección "Hoy en BA"
- [ ] Pricing para venues B2B

## Referencias
- [[korantis-audit-2026-06-03]] — auditoría CEO-a-CEO completa
- [[korantis-benchmark]] — benchmark visual vs Wolfim
- [[wolfim-com-audit-2026-06-03]] — auditoría de wolfim.com (en comparación)
- [[SOUL]] — reglas sobre trabajo en empresa secundaria
- [[MEMORY]] — estado actual del negocio
- [https://www.korantis.com](https://www.korantis.com)

## Notas personales
- Korantis es el proyecto soñado de Juan. No es racional en términos de ROI inmediato.
- Tiene que quedar en stand-by hasta que Wolfim tenga caja. Mientras tanto, el sitio vive como case study de portfolio y como recordatorio de "lo que se puede hacer".
- Cada vez que Juan pida trabajar en Korantis, verificar semáforo Wolfim primero.
- Si semáforo 🔴 o 🟡 → no se toca Korantis, se trabaja leads.
- Si semáforo 🟠 → 1 hora/semana de mantenimiento de Korantis, nada más.
- Si semáforo 🟢 → recién ahí Korantis puede recibir trabajo activo.
