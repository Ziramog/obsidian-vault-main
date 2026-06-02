# Análisis de referencia — Ruatta Automotores

**URL:** https://www.ruattaautomotores.com.ar/
**Rubro:** Concesionaria multimarca (autos 0km + usados + motos) en Río Tercero, Córdoba
**Antigüedad empresa:** 30+ años en el rubro
**Fecha del análisis:** 2 de junio de 2026
**Para:** Benchmark de propuesta Wolfim → clientes concesionarios (Paolini, etc.)

---

## 1. Stack técnico

| Capa | Detalle |
|---|---|
| **Framework** | Next.js (App Router, React Server Components) |
| **Hosting** | Vercel (header `Server: Vercel`) |
| **Tipografía** | Custom (no Google Fonts directo, usan next/font local) |
| **CSS** | 1 archivo CSS compilado (Next.js) |
| **Imágenes** | 14 assets únicos, formato JPG/PNG, lazy loading activo (18 ocurrencias) |
| **Tamaño HTML inicial** | ~49 KB (sin hidratar — Next.js envía RSC) |
| **HSTS** | Activo (max-age 63072000) |
| **X-Frame-Options** | No presente (vulnerable a clickjacking, baja prioridad) |
| **CSP** | No presente |

**Lo que esto significa para Wolfim:**
- ✅ El stack que Wolfim ya usa (Next.js + Vercel) es exactamente el mismo. Ruatta es 100% replicable.
- ✅ No usan nada propietario ni frameworks raros. Es Next.js puro.
- ⚠️ Podríamos sumar cosas que Ruatta NO tiene: sitemap.xml, robots.txt, Schema.org más completo (LocalBusiness + reviews), Google Search Console, Google Analytics.

---

## 2. SEO (lo que Ruatta hace bien y lo que falta)

### ✅ Lo que hacen bien
- **Title** descriptivo y con keywords: "Ruatta Automotores | Agencia multimarca en Río Tercero"
- **Meta description** específica: incluye ciudad, productos, dirección
- **Canonical URL** declarado
- **Open Graph** completo (10 tags) — para compartir en redes se ve bien
- **Twitter Cards** configuradas
- **Schema.org AutoDealer** — el más importante para Google. Le dice a Google que es una concesionaria.
- **Viewport** mobile-friendly
- **Robots: index, follow** correcto
- **HSTS** activo

### ❌ Lo que falta o es débil
- **0 H1** detectados — el H1 suele estar en el hero pero no se ve en el HTML estático (probablemente está dentro de un componente RSC). **Oportunidad**: agregar un H1 con keywords fuerte tipo "Concesionaria en Río Tercero — Autos y motos 0km y usados"
- **Sin sitemap.xml** — Google lo descubre más lento. Hay que generarlo.
- **Sin robots.txt** — al menos debería existir.
- **Sin Google Analytics / Tag Manager** — no miden nada. Oportunidad clara.
- **Sin Google Search Console** declarado.
- **Sin Schema.org LocalBusiness** — sólo tienen AutoDealer. Falta el address completo, horarios, teléfono, geo coordenadas.
- **Canonical apunta a `ruattaautomotores.com`** (sin www) pero el sitio responde en `.com.ar` — inconsistencia. **Oportunidad**: revisar y unificar.

---

## 3. Estructura de contenido (lo que muestra la home)

1. **Hero** — tagline "Calidad que te mueve" + carrusel de imágenes full-width (frente del local, autos)
2. **Sección motos** — "Línea completa de motocicletas" con 3 categorías: Touring, Trail, Custom/Cruiser, Sport/Touring
3. **Marcas** — Volkswagen, Toyota, BMW, Chevrolet, Jeep, Mercedes-Benz (logos de marca)
4. **Unidades destacadas** — sección que carga dinámicamente ("Cargando destacados…" sugiere API/fetch)
5. **Historia familiar** — "30 años en el rubro" + foto familia + texto emotivo
6. **Trust badges** — "+25 años", "Financiación flexible", "Vehículos verificados"
7. **Proceso 3 pasos** — "Elegí / Financiá / Retirá" + CTA "Encontranos"
8. **Footer** — datos de contacto completos, horarios, dirección

**Lo que esto significa:**
- Estructura clásica de landing de concesionaria. Probada.
- Sección "Unidades destacadas" cargada dinámicamente = la home tiene API/fetch de catálogo. **Para Wolfim: el panel admin tiene que poder gestionar este stock**.

---

## 4. Tracking y conversiones

| Elemento | Ruatta | Wolfim debería sumar |
|---|---|---|
| Google Analytics | ❌ | ✅ desde día 1 |
| Google Tag Manager | ❌ | ✅ |
| Facebook Pixel | ✅ | ✅ (si cliente pauta Meta Ads) |
| WhatsApp Business link | ✅ | ✅ |
| Schema.org AutoDealer | ✅ | ✅ |
| Schema.org LocalBusiness | ❌ | ✅ (más completo) |
| Sitemap.xml | ❌ | ✅ |
| Robots.txt | ❌ | ✅ |
| HSTS | ✅ | ✅ (gratis en Vercel) |
| Meta OG image custom | ✅ (auto_ruta.jpg 1200x630) | ✅ |
| Hotjar / Microsoft Clarity | ❌ | opcional, agregable |

**Diferenciador claro:** Ruatta NO mide nada. El cliente que compre Wolfim va a tener analytics desde el día 1. Eso es un argumento de venta concreto.

---

## 5. Lo que se puede copiar / adaptar para Paolini

### ✅ Copyable directo (estructura probada)
- Hero con carrusel full-width
- Sección de marcas
- Sección "Unidades destacadas" con carga dinámica
- Trust badges (+X años, financiación, verificación)
- Proceso 3 pasos (Elegí / Financiá / Retirá)
- Footer con datos completos

### 🆕 Mejorable vs. Ruatta
- H1 con keywords locales fuerte ("Concesionaria en La Falda — Autos 0km y usados")
- Schema.org LocalBusiness con horarios + teléfono + geo
- Sitemap.xml + robots.txt
- Google Analytics + Tag Manager
- Canonical URL limpio
- Meta OG image específica de la concesionaria
- Schema.org Review / AggregateRating si juntan testimonios
- Botón flotante de WhatsApp con mensaje pre-armado

### 🎯 Argumentos comerciales para la propuesta a Paolini
1. **"Lo mismo que Ruatta, pero mejor"** — Ruatta es Río Tercero, Paolini puede ser **el referente del valle de Punilla** con una web mejor.
2. **"Lo medimos todo"** — analytics desde el día 1.
3. **"Salís de GTM"** — catálogo propio, no dependés de plataformas genéricas.
4. **"SEO local primero"** — alguien en La Falda, Huerta Grande, Villa Giardino, Valle Hermoso, Capilla del Monte que googlea "concesionaria" te encuentra a vos primero.

---

## 6. Especificaciones de implementación Wolfim

### Stack (todo lo que Wolfim ya tiene)
- Next.js (App Router)
- Vercel hosting
- Supabase (DB para inventario de autos)
- Tailwind / CSS modules
- next/image con placeholder blur
- next/font Inter

### Lo que falta construir (si todavía no está en Wolfim)
- Panel admin para cargar/editar autos
- API de inventario (GET/POST/PUT/DELETE)
- Schema.org LocalBusiness + AutoDealer dinámico
- Sitemap dinámico (Next.js `app/sitemap.ts`)
- Google Analytics + GTM integration
- OG image dinámico (next/og)

---

## 7. Checklist propuesta Wolfim para cliente tipo Ruatta/Paolini

- [ ] Hero con fotos del local + tagline
- [ ] Carrusel de marcas representadas
- [ ] Sección de unidades destacadas (carga dinámica desde Supabase)
- [ ] Historia / familia / años de trayectoria
- [ ] Trust badges (años, financiación, verificación)
- [ ] Proceso 3 pasos con CTA WhatsApp
- [ ] Sección lubricentro / service (si aplica)
- [ ] Footer con contacto completo + horarios + mapa embebido
- [ ] Botón flotante WhatsApp
- [ ] Schema.org AutoDealer + LocalBusiness
- [ ] Sitemap.xml + robots.txt
- [ ] Google Analytics + Tag Manager
- [ ] OG image custom 1200x630
- [ ] SEO local: H1 con keywords, title, description, alt text
- [ ] Mobile responsive (obligatorio)

---

## 8. URL y contactos del referente

- **Web:** https://www.ruattaautomotores.com.ar/
- **Dirección:** Av. Gral. Savio 2605, Río Tercero, Córdoba, CP 5850
- **Horarios:** Lun a vie 9-18 h, Sáb 9-13 h
- **Rubro:** Autos y motos 0km multimarca + usados
- **Marcas representadas:** VW, Toyota, BMW, Chevrolet, Jeep, Mercedes
- **30 años en el rubro**

---

## 9. Aplicación directa a la propuesta de Paolini

Paolini tiene:
- Lubricentro oficial Ford/Chevrolet → sección extra
- Dos sucursales (Av España 601 y 1138) → destacar en footer
- 0km multimarca + usados
- Multitienda digital (GTM, IG, FB, WhatsApp) → dolor claro

Ruatta es mejor benchmark que Paolini porque:
- Ambos son concesionarias multimarca en Córdoba
- Ruatta es más grande (30 años) pero Paolini tiene la ventaja competitiva del lubricentro
- Ruatta muestra motos además de autos — Paolini podría sumar

**Acción concreta para Wolfim:**
Cuando se presente la propuesta a Paolini, mencionar el benchmark Ruatta: *"Concesionarias como Ruatta en Río Tercero ya tienen presencia digital profesional. Paolini puede tener lo mismo y mejor en el valle de Punilla."*
