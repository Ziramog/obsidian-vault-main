---
tags: [wolfim, sitio-oficial, auditoria, web-presence]
audited: 2026-06-03
auditor: hermes (M3)
---

# Auditoría wolfim.com — 03/06/2026

**URL:** https://www.wolfim.com
**Audit:** Juan pidió auditoría de su propio sitio como CEO.
**Comparativa:** vs [[korantis-audit-2026-06-03]] y benchmarks internos.

## Veredicto global: **8.5/10**

Wolfim.com es un sitio premium real, no un showcase. Es un negocio funcionando, no un prototipo. Comparado con el 90% de "diseñadores web" en Argentina, está 3-4 escalones arriba.

## Lo que funciona

1. **Hero brutal y memorable.** "WOLFIM /M9l879W37RZ" con código de serie y visual de cabeza humana hecha de código/wireframe. Posicionamiento claro: arquitecto de sistemas, no diseñador de mockups.

2. **Estructura narrativa profesional.** 9 secciones numeradas (01-09) con título + subtítulo. Storytelling de servicio premium, no landing genérica.

3. **Portfolio honesto y real.** 4 proyectos: Roggero & Roma, S&P Cars, Construvial, Korantis.com. Korantis como case study es inteligente (muestra músculo técnico) pero puede ser percibido como auto-promo. Mostrar como "plataforma propia" o "R&D interno".

4. **Pricing público y valiente.** "$200, $300, $450, $450+" con qué incluye cada tier. Filtra mejor que cualquier formulario. La mayoría de competidores NO publican precios.

5. **WhatsApp pre-armado.** `wa.me/5491173858454?text=Hola%20Wolfim%2C%20estoy%20interesado%20en%20un%20sitio%20web` — reduce fricción. Solo apretar enviar.

6. **Performance excelente.** TTFB 8ms (Vercel edge), FCP 1476ms, 12 requests, 0 errores, 0 failed. Single-page app limpia.

7. **Bilingüe EN/ES.** Switcher visible en header. Abre mercado LATAM + anglo.

## Lo que falla (de menor a mayor)

1. **H1 con código de serie confunde al visitante nuevo.** "WOLFIM /M9l879W37RZ — DISEÑO WEB PREMIUM & SISTEMAS DIGITALES". El código no se explica. Mover a elemento secundario o etiquetar como "system ID" del branding.

2. **Stats de "Construido con Inteligencia" sin contexto.** "97%", "3.2x", "40%", "1.0" — sin fuente ni comparación. Si tenés data real, agregala. Si no, cambialas por datos defendibles.

3. **Sección de resultados sin nombres de proyectos.** Las stats deberían estar atadas a casos reales. "3.2x" suelto es marketing vacuo.

4. **Falta social proof verificable.** Sin logos de clientes extra, sin testimonios con nombre+cargo+resultado, sin ratings de Google/Clutch/LinkedIn. Para servicio premium a $450+, esto es un gap serio.

5. **Sin formulario de contacto.** Solo WhatsApp. Para clientes corporativos grandes, WhatsApp es perceived unprofessional. Sugerencia: form corto en sección contacto + email `hello@wolfim.com` más visible.

6. **Footer con links vacíos.** "© 2024", LinkedIn/Twitter/GitHub sin hrefs scrapeables, sin sitemap, sin Privacy/Terms.

7. **Reloj "01:16:29" en header es un misterio.** Si es branding intencional (sistemas vivos, tiempo real), genial. Si no, confunde.

8. **Copyright dice 2024.** Estás en 2026. Detalle menor pero grita "no se actualiza".

9. **H1 con newline character en código:** `WOLFIM\n/J1JW87VRG3K\n— DISEÑO WEB PREMIUM & SISTEMAS DIGITALES`. Bug menor de copy.

10. **Sección final (Construyamos tu próximo sitio web) solo WhatsApp y email.** Sin calendar embed (Cal.com, Calendly). Para servicio premium, ofrecer agendar call de 30 min convierte mejor que WhatsApp frío.

## Datos técnicos

| Métrica | Valor | Veredicto |
|---|---|---|
| Status | HTTP 200 | ✅ |
| Server | Vercel (con Cloudflare CDN) | ✅ |
| TTFB | 8ms | 🟢 Excelente |
| FCP | 1476ms | 🟢 Bueno |
| Requests | 12 | 🟢 Excelente |
| Total weight | 52MB (50MB en "other" = fonts/sourcemaps) | 🟠 Optimizable |
| Errores en consola | 0 | ✅ |
| Failed requests | 0 | ✅ |
| Title | "Wolfim Studio — Premium Web Design & Digital Systems" | ✅ |
| Meta description | 252 chars, ES, bien redactado | ✅ |
| Canonical | https://wolfim.com/ | ✅ |
| Open Graph | og:title, og:description, og:image, og:url presentes | ✅ |
| H1 | 1 (con código) | ⚠️ Confuso |
| H2 | 9 (numerados 01-09) | ✅ |
| H3 | 20 | ✅ |
| Nav | 1 con 5 links internos | ✅ |
| Footer | 1 (vacío de links scrapeables) | ⚠️ |
| Forms | 0 | ⚠️ |
| WhatsApp CTA | 3 instancias, todas pre-armadas | ✅ |
| Email | mailto:hello@wolfim.com | ✅ |
| Social links | 0 scrapeables | ⚠️ |
| Bilingüe | EN/ES switcher en header | ✅ |
| Stack | Next.js + Vercel | ✅ |

## Top 3 para arreglar esta semana

1. **Agregar 2-3 testimonios con nombre + empresa + resultado concreto** en "Qué recibís" o nueva sección "Lo que dicen los clientes". 10 min si tenés los datos, 2 horas si tenés que pedirlos.

2. **Actualizar footer:** © 2026, links reales a LinkedIn/Twitter/GitHub con hrefs, links a Privacy Policy y Términos. 30 minutos.

3. **Decidir si las stats de "Construido con Inteligencia" tienen data real o no.** Si sí, agregar fuente + nombre del proyecto al lado. Si no, cambiar a algo defendible.

## Comparativa rápida

| Aspecto | Wolfim.com | Korantis.com |
|---|---|---|
| Craft visual | 8.5/10 | 8/10 |
| Claridad de propuesta | 9/10 | 9/10 |
| CTA visible | ✅ Sí, fuerte | ❌ No hay |
| Pricing público | ✅ Sí | ❌ No |
| Captura de leads | ⚠️ Solo WhatsApp | ❌ No hay |
| Modelo de negocio | ✅ Claro (setup + mantenimiento) | ❌ Inexistente |
| Funciona el flujo principal | ✅ Sí | ❌ No (bug filtro) |

## Pregunta incómoda

Si Wolfim está a este nivel (8.5/10, pricing público, portfolio honesto, performance top), ¿por qué tenés 1 cliente activo y 0 leads atacables con datos? El sitio no es el cuello de botella. El cuello de botella está en otro lado — outreach, follow-up, datos de contacto, propuesta. No es algo que yo pueda arreglar con código.

## Referencias
- [https://www.wolfim.com](https://www.wolfim.com)
- [[MEMORY]] — estado actual del negocio
- [[franco-roma]] — cliente activo
- [[korantis-audit-2026-06-03]] — auditoría del otro producto
