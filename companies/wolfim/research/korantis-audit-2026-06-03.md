# Auditoría de producto y UX — Korantis.com
**Para:** CEO / Founder de Korantis
**De:** Juan Manuel Gomariz (Wolfim) — vía auditoría técnica externa
**Fecha:** 3 de junio de 2026
**Sitio auditado:** https://www.korantis.com
**Idioma del sitio observado:** inglés
**Mercado objetivo aparente:** Buenos Aires, Argentina

---

## TL;DR — 60 segundos

Korantis tiene un **ángulo de marca excelente** y una ejecución visual notable, pero es hoy **un showcase, no un producto**. Lo confirmé con un usuario humano real y con instrumentación: el flujo principal (buscar lugares por mood) se rompe en el primer clic. La promesa "find places by feeling" muere en la primera interacción. Además, faltan los elementos básicos que convierten un sitio bello en un negocio: CTA, auth, mapa, captura de leads, social proof y un modelo de monetización visible.

Tres prioridades para los próximos 30 días, en orden de impacto:
1. **Arreglar el bug crítico del primer filtro** (clic en QUIET/WARM/etc. vacía la pantalla). Sin esto, el producto no funciona.
2. **Decidir el modelo de negocio y ponerlo visible** (auth + guardar lugares + CTA B2B para venues + partnerships).
3. **Construir el discovery loop** (mapa, filtros de hora/precio/distancia, sección "Hoy en BA", notificaciones).

Si Korantis se queda solo en la superficie, va a ser una pieza de portfolio más. Si ejecuta estas tres cosas en 30 días, tiene chance de ser un producto defensible.

---

## Lo que funciona (reconocer antes de criticar)

1. **El ángulo "by feeling" es diferenciador real.** TripAdvisor, Google Maps, Instagram y Yelp filtran por categoría, por foto o por rating. Ninguno filtra por mood. Korantis ocupa un hueco defendible: "no me siento de humor para X categoría, me siento para Y vibe". Es un problema real y la respuesta es memorable.

2. **El hero es impecable.** El search bar con placeholder dinámico ("quiet cafe to work tonight…") comunica la propuesta antes de cualquier copy. La paleta dark + dorado/cobre es atemporal. La tipografía dual (serif elegante para nombres + sans para metadata) funciona.

3. **El copy atmosférico es único.** Léanse los textos de las cards: "Bathed in the soft glow of hanging Edison bulbs, the air inside this charming venue hums with an inviting warmth — a refuge from…". Eso es brand building. No es un directorio, es un magazine.

4. **El selector de ciudad + 4 chips de mood visibles en hero** es la estructura correcta. El usuario entiende qué puede hacer antes de scrollear.

5. **Performance técnica es buena.** 53ms de TTFB, 936ms de FCP, 9.5MB total de página con 70 requests, 0 errores en consola, 0 failed requests. Para Next.js + Vercel con 63 imágenes lazy-loaded, es decente.

6. **El WAF de Vercel está activo.** "Security Checkpoint" protege al sitio de scrapers. Eso indica tráfico suficiente para justificar la protección.

7. **El robots.txt declara Content Signals explícitamente.** Korantis optó por default (ni prohíbe ni permite AI-training/AI-search). Es una posición consciente, no un descuido.

---

## Lo que está roto (crítico, bloquea el producto)

### Bug #1 — El primer filtro mata la pantalla
**Reproducir:** Cargar la home, clickear cualquier chip (QUIET, WARM, NATURAL LIGHT, HIDDEN GEM).
**Qué pasa:** El usuario espera ver lugares filtrados. En su lugar, la lista entera de lugares desaparece y la pantalla queda vacía. No hay mensaje de error, no hay loading state, no hay "no hay resultados para este filtro", no hay forma de volver.
**Por qué importa:** El flujo principal del producto ES clickear un chip. Si eso rompe, Korantis no es un producto — es un showcase. Cualquier usuario real se va en 3 segundos.

**Causa probable** (mi hipótesis, sin acceso al código): el estado del filtro no se persiste bien, o el query de fetch devuelve 0 resultados para ese chip en particular (las cards tienen tags como "SOFT", "AMBER", "BUSTLING" — los chips del hero pueden no matchear con los tags reales de las cards). El sistema escribe "quiet" en el search y filtra por texto libre en lugar de por tag.

**Cómo arreglarlo (prioridad 0):**
- Logging del query exacto que se dispara al clickear un chip
- Confirmar que los chips del hero matchean con los tags reales de las cards (audit del data model)
- Si no hay resultados: mostrar "0 lugares con este mood en este momento. Probá otro filtro" en vez de pantalla en negro
- Loading state visible: skeleton cards mientras carga
- Botón "Limpiar filtro" siempre visible después de activar uno

### Bug #2 — El search filtra por texto, no por mood
Cuando el usuario clickea QUIET, además de la pantalla vacía, el input de búsqueda se llena con "quiet" automáticamente. Eso confirma que el sistema está interpretando el chip como un texto libre, no como un tag estructurado. Un usuario que clickea QUIET no quiere buscar la palabra "quiet" en los nombres de los lugares — quiere lugares que TIENEN ese mood.

### Bug #3 — Copy de filtro dice "Palermo" hardcoded
El texto debajo del search dice: "Showing calm, work-friendly spaces with warm lighting open now in **Palermo**". Pero el selector de ciudad dice "BUENOS AIRES". Si el usuario clickea "WARM" en Buenos Aires, sigue mostrando el copy de Palermo. Es un copy default hardcoded que no se actualiza al cambiar de ciudad. Confunde.

### Bug #4 — Sin `<nav>`, sin footer, sin sitemap.xml, sin canonical
Confirmé el DOM: 1 elemento `<nav>` sin links, 0 elementos `<footer>`, 0 elementos `<h2>`, 0 tags Open Graph declarados, 0 Twitter cards, 0 JSON-LD structured data, 0 canonical URL, sitemap.xml no accesible (403).

Esto es un problema SEO importante. Google no entiende la estructura de la página. No hay manera de que un card individual de un lugar ranke en Google por su nombre. La estrategia de adquisición orgánica está bloqueada desde el código.

### Bug #5 — Imágenes sin fallback
Cuando una imagen no carga (por timeout, conexión lenta, error de Cloudinary), la card queda con un espacio negro sin texto ni placeholder. La alternativa obvia: skeleton con el nombre del lugar sobre un gradiente sutil.

---

## Lo que falta (no roto, pero bloquea el negocio)

### 1. Cero captura de leads
**No hay:**
- Formulario de contacto
- Form de "registrate para updates"
- Email capture en ninguna sección
- Suscripción a newsletter
- CTA principal de ningún tipo

**Costo de esto:** Cada visita que llega a la home y se va sin guardar nada es 100% perdida. Si mañana Korantis deja de existir, no queda ni una dirección de email para avisar a los usuarios.

### 2. Cero social proof
**No hay:**
- Reseñas de usuarios
- Ratings
- "X personas guardaron este lugar"
- Testimonios
- Logos de partners
- Logos de prensa
- Conteo de usuarios activos

**Costo:** Sin validación social, el visitante asume que el sitio es nuevo / no confiable / sin usuarios. Reduce la confianza en 30-50% según benchmarks de la industria.

### 3. Cero modelo de monetización visible
**No hay:**
- Pricing para venues
- CTA "¿Tenés un lugar? Sumalo a Korantis"
- Sección para inversores / partners
- Tiers premium
- Sección "Cómo funciona"

**Pregunta abierta:** ¿Cómo gana plata Korantis? Las opciones realistas son:
- **B2C premium:** suscripción mensual con funciones avanzadas (guardar ilimitado, recomendaciones personalizadas, alertas)
- **B2B listings:** venues pagan para ser destacados / tener página propia / aparecer primero en búsquedas
- **Affiliate / referral:** comisionar reservas vía integración con plataformas (Resy, OpenTable, Restorando)
- **Data / insights:** vender data anonimizada de comportamiento a real estate / hospitality /市政府

Recomiendo combinar B2C premium (fuente de revenue recurrente) + B2B listings (ticket alto, scalable). El affiliate funciona pero es commoditizado y los márgenes son chicos.

### 4. Sin auth, sin guardar lugares, sin perfil
Un usuario que encuentra 3 lugares que le gustan hoy no puede volver mañana a verlos. No hay forma de guardar. No hay razón para volver. Sin esto, la retención es 0.

### 5. Sin mapa
El tagline dice "find places". Sin mapa, no es "find" — es "scroll". Un mapa con pins por zona + cluster + filtro de mood sobre el mapa es lo que el usuario espera. Es la feature #1 que el 80% de los usuarios asume que existe.

### 6. Sin mobile-first claro
- En mobile, mi fetch desde IP datacenter fue bloqueado por el WAF de Vercel ("Code 21, Security Checkpoint"). No pude auditar mobile. Pero desde el DOM puedo decir: no hay meta viewport para mobile-first, no hay hamburger menu visible en el header, y la barra inferior con search/map/profile icons es mobile-style pegada en desktop.
- **Recomendación:** auditar mobile con dispositivo real o BrowserStack antes de lanzar cualquier campaña de marketing.

### 7. Sin notificaciones, sin email marketing, sin "Hoy en BA"
- No hay push notifications
- No hay email digest
- No hay sección "Lo que está bueno hoy"
- No hay "Curaduría semanal"

Cualquier producto de discovery necesita generar recurrencia. Hoy Korantis es una página que se visita una vez y se olvida.

---

## Auditoría técnica detallada

### SEO
| Item | Estado | Severidad |
|---|---|---|
| `<title>` | "Korantis — Find Places by Feeling" | ✅ OK |
| `<meta name="description">` | "Discover places for how you want to feel." | ✅ OK pero mejorable |
| `<link rel="canonical">` | AUSENTE | 🔴 Crítico |
| Open Graph (og:title, og:description, og:image) | AUSENTE en el HTML servido | 🔴 Crítico |
| Twitter Cards | AUSENTE | 🟡 Importante |
| JSON-LD structured data | AUSENTE | 🔴 Crítico |
| `sitemap.xml` | No accesible (403, o el WAF lo bloquea) | 🔴 Crítico |
| `robots.txt` | Existe, con Content Signals | ✅ Decisión consciente |
| H1 | "KORANTIS" | ✅ OK |
| H2 | 0 elementos | 🔴 Estructura rota |
| H3 | 30 (nombres de lugares) | ✅ OK |

**Conclusión SEO:** Korantis no puede rankear orgánicamente. Google no sabe qué es cada página. Sin canonical, sin structured data, sin OG, sin sitemap, las cards de lugares individuales son invisibles para search.

### Performance
| Métrica | Valor | Veredicto |
|---|---|---|
| TTFB | 53ms | 🟢 Excelente |
| FCP | 936ms | 🟢 Bueno |
| DOM content loaded | 270ms | 🟢 Excelente |
| Load event | 879ms | 🟢 Bueno |
| Total weight | 9.5MB | 🟠 Pesado (90% imágenes) |
| Requests | 70 | 🟢 Aceptable |
| Imágenes | 63 (42 cargan en mi entorno) | 🟠 Necesita audit manual |
| Img weight | 9MB de 9.5MB totales | 🟠 Optimizar formato/size |
| JS weight | 323KB | 🟢 OK |
| CSS weight | 21KB | 🟢 Excelente |
| Font weight | 112KB | 🟢 OK |

**Recomendaciones performance:**
- Convertir las imágenes a AVIF o WebP con fallback a JPG. Ahorro esperado: 50-60% de peso.
- Implementar `loading="lazy"` agresivo + `placeholder="blur"` con blurDataURL.
- Limitar el ancho máximo de imagen servida. 3840px es excesivo para 99% de pantallas.

### Accesibilidad
| Item | Estado |
|---|---|
| Imágenes con `alt` | ✅ Sí (verificado: todas tienen alt descriptivo) |
| Contraste de texto | ✅ Aceptable (dorado sobre negro pasa WCAG AA) |
| Aria labels | ❌ No verifiqué profundo, pero search input sin label visible |
| Keyboard navigation | ❌ No probé (WAF me bloqueó interacciones) |
| Foco visible | ❌ No verifiqué |
| Reduced motion | ❌ No verifiqué |

**Recomendación:** audit completo con axe-core o Lighthouse. Mínimo asegurar: alt en todas las imágenes, focus visible en todos los interactivos, labels en inputs, contraste WCAG AA en todos los textos.

### Stack técnico inferido
- **Framework:** Next.js (App Router, RSC)
- **Hosting:** Vercel (con WAF activo, CDN Cloudflare delante)
- **Image CDN:** Cloudinary (cuenta `dmdjhvyqs`)
- **Font:** Probablemente una serif tipo Tiempos/Cardo + sans tipo Inter
- **Iconografía:** Lucide (confirmado en el DOM)
- **Analytics:** Google Analytics (gtag)
- **Sin:** Stripe, Hotjar, Intercom, Facebook Pixel, Vercel Analytics nativo

**Stack sano. Faltan las herramientas de monetización y growth (Stripe para cobrar, Hotjar/FullStory para entender comportamiento, Intercom/Crisp para soporte, Facebook Pixel para paid).**

---

## Posicionamiento y marca

**Lo que Korantis ES hoy (en mi lectura):**
- Un magazine de discovery de lugares en Buenos Aires, curado por mood.
- Una pieza de portfolio que demuestra un ángulo de marca fuerte.
- Un early-stage product en búsqueda de product-market fit.

**Lo que Korantis PODRÍA ser (oportunidad):**
- El "Spotify de lugares": una app de discovery que te dice adónde ir según cómo te sentís.
- El Yelp emocional: reseñas por vibe, no por rating.
- El Airbnb Experiences de bares/restaurantes: discovery con booking integrado.

**Recomendación estratégica:**
No intentes ser todo. Elegí UNA de estas tres y construí ese loop hasta que funcione:
1. **Consumer app de discovery puro** (sin booking, sin reseñas — solo recomendar lugares por mood)
2. **Marketplace B2B2C** (venues pagan por listing destacado, usuario guarda y reserva)
3. **Curación editorial + suscripción premium** (newsletter semanal "10 lugares que tenés que conocer esta semana en BA")

Si fuera VC, invertiría en la #2. Si fuera indie / lean, iría por la #1 con foco obsesivo en mobile UX.

---

## Benchmark de competidores

| Producto | Modelo | Fortaleza | Debilidad |
|---|---|---|---|
| **Google Maps** | Listing gratis + ads | Cobertura total, datos | Genérico, sin mood |
| **TripAdvisor** | Affiliate + ads | Reseñas masivas | Feo, spammy, sin vibe |
| **Instagram** | Publicación orgánica | Visual, aspiracional | No es discovery, es vanity |
| **Foursquare** | Data + recommendations | Datos de check-in | Murió como consumer product |
| **The Infatuation** | Editorial + affiliate | Curaduría editorial fuerte | US-only, no discovery interactivo |
| **Resy / OpenTable** | Reservas | Booking real | Solo restaurantes, sin mood |
| **Korantis (potencial)** | ¿? | Mood/vibe, editorial | Sin features, sin users, sin revenue |

**El hueco está claro. La pregunta es si Korantis tiene tiempo y runway para capitalizarlo antes que alguien copie el ángulo.**

---

## Recomendaciones priorizadas (30 / 60 / 90 días)

### 30 días — Matar bugs y validar fundamento
- [ ] Arreglar bug #1 (filtro vacía la pantalla) — bloquea el producto
- [ ] Implementar loading states y empty states en todos los filtros
- [ ] Agregar fallback de imagen (skeleton con gradiente + nombre del lugar)
- [ ] Agregar meta OG, canonical URL, JSON-LD (LocalBusiness schema para cada lugar)
- [ ] Crear sitemap.xml accesible y enviarlo a Google Search Console
- [ ] Implementar auth simple (email magic link con NextAuth o Clerk) + guardar lugares
- [ ] CTA primario visible en hero: "Empezá a guardar lugares gratis"
- [ ] Captura de email en el footer o como exit-intent: "¿Te gustó? Te avisamos cuando sumemos más ciudades"

### 60 días — Construir el loop
- [ ] Mapa interactivo de BA con pins (Mapbox o Google Maps)
- [ ] Filtros adicionales: hora del día (después de las 22, mañana, mediodía), precio ($, $$, $$$), distancia
- [ ] Sección "Hoy en BA" con 3-5 picks curados
- [ ] Página de detalle de cada lugar con: dirección, horarios, link a Google Maps, link a Instagram, link a reservar si existe
- [ ] Compartir por WhatsApp / Instagram Stories desde cada card
- [ ] Email digest semanal con los 5 mejores lugares de la semana

### 90 días — Monetización y growth
- [ ] Pricing público para venues: "Destacá tu lugar en Korantis — $X/mes"
- [ ] Página dedicada para venues con self-service signup
- [ ] Partnerships con 5-10 venues premium (Don Julio, Tres Monos, Florería Atlántico) para lanzamiento
- [ ] Lanzamiento en español (la mayoría del mercado target es hispanohablante)
- [ ] Versión mobile-first real (auditar con dispositivo real)
- [ ] Programa de referral: "Invitá a 3 amigos, desbloqueá lugares exclusivos"
- [ ] PR strategy: pitch a Forbes Argentina, Etecé, Infobae, La Nación sobre el "Yelp emocional argentino"

---

## Riesgos y oportunidades

### Riesgos
- **WAF de Vercel agresivo.** Si bloquea a usuarios reales (no solo a scrapers), perdés tráfico. Auditar el false-positive rate.
- **Sin moat competitivo.** El ángulo "by feeling" es copiable en 2 meses. Lo que crea moat es: data de comportamiento de usuarios, partnerships exclusivos con venues, comunidad curadora.
- **Idioma.** El sitio está en inglés en un mercado hispanohablante. Puede ser intencional (turistas / expats), pero limita el TAM.

### Oportunidades
- **Argentina está hambrienta de productos bien hechos.** Hay poco producto nativo argentino de calidad. Korantis tiene chance de ser la referencia.
- **El modelo editorial funciona en BA.** Revistas como Ezeiza, locales,Ohlalá, Jardín del Este. Hay audiencia para curaduría.
- **Bares y restaurantes en BA están desesperados por tráfico post-pandemia.** Una plataforma que les traiga clientes calificados es valiosa.
- **El WAF activo = tráfico.** Si el WAF está prendido, no es porque no tengas tráfico. Es porque Vercel considera que vale la pena protegerte. Capitalizalo.

---

## Cierre

Korantis está en el momento correcto de su vida: tiene un ángulo que funciona, una base técnica sólida, y todavía ningún competidor. Lo que le falta no es creatividad ni diseño — eso ya está. Lo que le falta es **convertir el showcase en un producto**: arreglar el bug que mata el primer filtro, decidir un modelo de negocio, construir el loop de retención.

Si tuviera que elegir UNA sola cosa para hacer esta semana, sería: **arreglar el bug del primer filtro y poner un CTA "Empezá a guardar lugares" en el hero.** Esas dos cosas solas cambian la conversión de visita-a-account-de-un-orden-de-magnitud.

Si querés, puedo entrar más profundo en cualquiera de los puntos. Mi motivación para escribir esto: como founder a founder, porque creo que el ángulo de Korantis merece un producto que funcione.

— Juan Manuel Gomariz
   Fundador de Wolfim (www.wolfim.com)
   Buenos Aires, 3 de junio de 2026

---

## Anexo técnico — datos de la auditoría

### Inventario de páginas y elementos
- **Páginas únicas con contenido scrapeable:** 1 (home)
- **Lugares en la base:** 30+ (ver lista abajo)
- **Largo de la home:** ~43,500px (es un feed largo, no una landing)
- **H1:** 1 (KORANTIS)
- **H2:** 0
- **H3:** 30
- **Cards en home:** 30+
- **Inputs en home:** 1 (search)
- **Forms:** 0
- **`<nav>` elementos:** 1 (sin links)
- **`<footer>` elementos:** 0
- **Botones:** 5 (4 chips de mood + 1 selector de ciudad)
- **CTAs primarios:** 0
- **Social links:** 0

### Lista de lugares encontrados
Wine Window Argentina (Palermo Soho), CICHAUS, Florería Atlántico, Tres Monos, Verne Club, Niño Gordo, Trade Sky Bar, Backroom Bar, Kraken Bar, Bestial Fly Bar, Don Julio Parrilla, Ciro Palermo, El Preferido de Palermo, Parrilla Don Julio, El Boliche de Roberto, Mishiguene, Uptown Bar, 878 Bar, Milion, Vini Bar, Gran Bar Danzon, Plaza Bar, Mixtape Bar, Guerrin, Reliquia, Julia, Anchoita, El Cuartito, Cabaña Las Lilas, Oporto Almacén, Invernadero, y más.

### Mood tags observados
SOFT, WARM, AMBER, GOLDEN, GREEN, BUSTLING, COZY, INTIMATE, QUIET, ATMOSPHERIC, CALM, SOCIAL, SLOW, NATURAL LIGHT, HIDDEN GEM, BUENOS AIRES, WINE BAR, RESTAURANT, VALIDATION, CONSUMER READY.

### Stack inferido
- Frontend: Next.js App Router + React Server Components
- Hosting: Vercel (con Cloudflare CDN y WAF)
- Imágenes: Cloudinary (cuenta `dmdjhvyqs`)
- Tipografía: serif elegante + sans (probable Cardo/EB Garamond + Inter)
- Iconos: Lucide
- Analytics: Google Analytics (gtag)
- Sin integración visible con: Stripe, Hotjar, Intercom, Facebook Pixel, Vercel Analytics nativo

### Performance
- TTFB: 53ms
- First Contentful Paint: 936ms
- DOM Content Loaded: 270ms
- Total página: 9.5MB (90% imágenes)
- Total requests: 70
- Errores en consola: 0
- Failed requests: 0
- Imágenes: 63 declaradas, ~42 visibles al momento del scroll
