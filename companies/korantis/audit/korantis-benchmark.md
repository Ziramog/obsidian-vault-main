---
tags: [benchmark, ui-research, korantis, referencia-wolfim]
---

# Korantis — Auditoría visual & benchmark
**URL:** https://www.korantis.com
**Auditado:** 2026-06-03 por Hermes (M3)
**Contexto:** Juan lo pidió como referencia visual. Es un producto de discovery de lugares por mood/vibe, no por categoría.

## Resumen ejecutivo
Korantis es un **portfolio piece bello con un ángulo de marca fuerte, pero con fallas técnicas críticas y sin modelo de negocio visible.** Diseño 8/10. Producto funcional 3/10. Posicionamiento 9/10.

## Lo que es
"Find places by feeling" — discovery de bares/restaurantes/cafés en Buenos Aires filtrado por mood/vibe (no por categoría). El copy es literary/poético: "Bathed in the soft glow of hanging Edison bulbs, the air inside this charming venue hums with an inviting warmth..."

## Lo que funciona bien
- **Hero dark + dorado/cobre** elegante, atemporal, premium sin ser pretencioso.
- **Search bar con placeholder en serif italic** ("quiet cafe to work tonight..."). Comunica la propuesta antes de cualquier copy.
- **Tipografía dual:** serif elegante para nombres de lugares + sans para metadata. Contraste correcto, jerarquía clara.
- **Cards full-bleed verticales** con foto + dirección + copy atmosférico + 4-6 chips de mood (SOFT/WARM/BUSTLING/COZY/INTIMATE/QUIET/GOLDEN/AMBER).
- **Filtro de ciudad visible** (BUENOS AIRES ▼) — el default es BA.
- **Cero grid denso** — la curaduría manda. Es editorial, no directorio.

## Lo que está ROTO (crítico)
- **~50% de las imágenes NO cargan.** El HTML declara 20+ lugares pero 10 dan w=0/h=0/complete=false. Los rotos: Niño Gordo, Don Julio, Ciro Palermo, El Preferido, Parrilla Don Julio, El Boliche de Roberto, Mishiguene, Uptown, 878, Milion. **Son los top spots de BA.** Si scrolleás y te encontrás cajas negras, te vas.
- Las cards que SÍ cargan (CICHAUS, Florería Atlántico, Verne Club, Trade Sky Bar) se ven espectaculares. El gap entre las que cargan y las que no es gigante.
- **Causa probable:** Cloudinary como CDN, hotlink protection, URLs firmadas vencidas, o config rota de `next/image`. Las URLs que cargan son más nuevas o sin firma.

## Lo que FALTA (UX/negocio)
- **Cero CTA visible.** No hay "Sign up", "Save this place", "Get the app", "Subscribe". ¿Cómo monetiza?
- **Cero social proof.** Sin reseñas, sin ratings, sin "X people saved this".
- **Cero nav.** H1=KORANTIS, h2=[]. Sin "About", "How it works", nada.
- **Sin footer** (al menos en lo que se ve).
- **Sin mapa visible** (el tagline "find places" sugiere uno). Si existe, debajo del fold.
- **Filtros de mood/hora/precio/distancia no aparecen** en el hero. Están escondidos o no existen.

## Posicionamiento de marca
**9/10.** El ángulo "by feeling" es diferenciador real. Tripadvisor/Google filtran por categoría, Instagram por foto, ninguno por vibe. Es un hueco defendible.

---

## Benchmark Wolfim — qué tomar, qué no

### Nivel craft: Korantis = 10, Roggero & Roma = 6, target Wolfim = 8
Franco Roma ya tiene el lenguaje correcto (dark + dorado, cards full-bleed). Korantis está 2-3 niveles arriba en polish. **Target realista Wolfim = mitad de este nivel.** Aspirar a 10/10 en cada cliente es insostenible y caro.

### Lo que SÍ tomar para próximos clientes Wolfim
1. **Placeholder en search bar como propuesta.** "Busca un dept en Palermo...", "Necesito un café para trabajar 3hs...". Comunica el producto sin copy adicional.
2. **Chips de atributo en cards.** Para cualquier card (producto, propiedad, servicio), 3-5 chips que sinteticen el valor. Ej: para Franco: ILUMINADO / COCINA INTEGRAL / COCHERA / PETS OK.
3. **Filtro de ciudad/ubicación visible desde hero.** Un select dropdown. Comunica que el sitio entiende geografía.
4. **Tipografía dual (display + body).** Display serif para nombres destacados. Sans para metadata. Jerarquía clara.
5. **Cards verticales, no grid denso.** Más respiración, menos comparación. Editorial > marketplace.

### Lo que NO tomar
1. **Calidad de fotografía extrema.** Korantis tiene 1 foto profesional por lugar, tomada por fotógrafo. Wolfim no puede pagar eso para cada cliente. Solución: guidelines al cliente + 1 sesión incluida.
2. **Copy literario/poético.** Funciona para Korantis (mood) pero es **malo** para Wolfim (los clientes de Franco, Paolini, etc. no escriben así). Copy funcional: "3 dormitorios, 2 baños, 120m², cochera doble."
3. **Sin CTA.** Korantis se lo puede permitir porque es showcase. Wolfim no — cada cliente necesita WhatsApp visible, formulario de contacto, lead capture desde el primer scroll.
4. **Sin social proof visible.** Inaceptable para Wolfim. Cada cliente debe tener reseñas de Google, testimonios, logos de propiedades vendidas/alquiladas.
5. **Dependencia de Cloudinary sin fallback.** Imágenes rotas = 0% de conversión. Wolfim DEBE tener fallback de imagen + lazy loading robusto.

---

## Feedback accionable para Korantis (si Juan quisiera pasarlo)

### Bugs críticos (matar hoy)
1. **Auditar Cloudinary.** ¿Las URLs firmadas vencen? ¿Hay buckets privados mal configurados? ¿`next/image` no está configurado con `unoptimized` o dominios remotos permitidos?
2. **Fallback visual.** Toda card debe tener skeleton o placeholder elegante mientras carga. Si la imagen falla, mostrar gradiente con el nombre del lugar.
3. **Lazy loading explícito.** `next/image` con `loading="lazy"` + `placeholder="blur"` con blurDataURL generado.

### UX (matar esta semana)
4. **CTA primario visible.** "¿Qué vibe buscás hoy?" + botón "Empezar". O "Guardar lugares" si requiere auth.
5. **Filtros de mood en hero.** Chips clicables: COZY / LIVELY / INTIMATE / ROMANTIC / WORK-FRIENDLY. Selección múltiple.
6. **Mapa.** Un mapa de BA con pins. Si el usuario no ve dónde está cada lugar, "find places" miente.
7. **Nav mínima.** Logo + 2 links: "Discover" + "About" + "Sign in".

### Negocio (matar este mes)
8. **Auth + guardar lugares.** Sin esto, no hay retención ni datos.
9. **Sección "Hoy en BA"** — curaduría diaria. Genera recurrencia.
10. **Modelo de monetización visible.** Para usuarios: premium sin ads. Para venues: listings destacados, eventos exclusivos.
11. **CTA para venues:** "¿Tenés un lugar? Sumalo a Korantis" → captura leads B2B.

### Si Korantis fuera cliente Wolfim
**Diagnóstico honesto:** 8/10 diseño, 3/10 producto. El sitio es una pieza de portfolio, no un negocio.
**Plan de remediación priorizado:**
- Sprint 1 (3-5 días): fix imágenes rotas + fallback + lazy loading. → 8/10 producto
- Sprint 2 (1 semana): auth + guardar lugares + mapa + filtros mood. → 6/10 producto
- Sprint 3 (1 semana): modelo negocio + partnerships con venues. → negocio viable

**Precio justo si fuera pitch:** $2,500-3,500 USD setup + $200-300/mes mantenimiento + add-ons (mapa interactivo, auth, sistema de recomendaciones).

---

## Lecciones para Wolfim
1. **El ángulo "by feeling" funciona porque ocupa un hueco.** Cualquier cliente Wolfim debe tener un ángulo claro que lo diferencie de la competencia obvia (Google, Zonaprop, Argenprop).
2. **Portfolio piece ≠ negocio.** No entregar un sitio "bello pero hueco" sin captura de leads ni CTA. Cada sitio Wolfim debe generar al menos 1 lead/mes verificable.
3. **Las imágenes rotas matan la confianza más rápido que un copy malo.** Presupuesto SIEMPRE para fotografía o guidelines claras al cliente.
4. **Dark + dorado es un lenguaje probado.** Pero hay que cuidarlo: si el cliente no tiene fotografía profesional, la oscuridad esconde la falta de calidad. Para clientes low-budget, recomendar paleta clara + acentos en color de marca.
5. **Chips de atributo son low-effort/high-impact.** Implementar en TODOS los templates de card.

## Referencias
- Capturas: `/home/hermes/tmp/korantis_hero.png`, `korantis_full.png`, `korantis_scroll1.png`, `korantis_footer.png`
- Output del audit original en sesión 2026-06-03
- Cliente Wolfim de referencia para patrón: [[franco-roma]]
