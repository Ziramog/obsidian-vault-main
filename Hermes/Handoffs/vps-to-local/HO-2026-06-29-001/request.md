---
id: HO-2026-06-29-001
status: ready
from: wolfim-growth
to: web-builder
project: wolfim
priority: high
depends-on: []
created-at: 2026-06-29T18:30:00-03:00
acknowledge-by: next-local-session
due-at: 2026-07-01T18:00:00-03:00
escalate-after: 48h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff: Landing diagnóstico + página inmobiliarias para Wolfim

> **Objetivo:** Crear dos páginas nuevas en wolfim.com para alimentar campaña Meta Ads (lead gen) y SEO por vertical. **No se toca la landing actual ni ninguna página existente.**

---

## 🎯 Qué hay que construir

### Página 1 — `/diagnostico` (🔴 Prioridad alta)

Página de aterrizaje para tráfico de Meta Ads. Sin menú, sin navegación visible. Un solo objetivo: que el dueño de una PyME complete el formulario.

### Página 2 — `/inmobiliarias` (🟡 Prioridad normal)

Página de contenido para SEO. Orientada a inmobiliarias que buscan "página web para inmobiliarias". Con caso real, servicios, precios y CTA.

---

## 🎨 Diseño — Restricciones absolutas

**Heredar 100% el theme existente de wolfim.com.** Nada de colores nuevos.

```css
/* Variables del sitio — NO crear nuevas */
--black: #0A0A0A
--white: #F5F5F0
--gray-400: #707068
body bg: #fafaf8
font-display: "Space Grotesk"
font-body: "Inter"
font-mono: "JetBrains Mono"
film-grain global (heredado)
```

**Tono visual:** editorial, limpio, alto contraste, sin íconos de stock, sin fotos genéricas, sin gradientes de color.

---

## 📄 Página 1 — `/diagnostico`

### Estructura

```
┌─────────────────────────────────┐
│  Logo Wolfim (chico, arriba)    │
│                                 │
│  H1: ¿Tu web está perdiendo     │
│      clientes?                  │
│                                 │
│  P:  La mayoría de las PyMEs    │
│      pierde consultas por 3     │
│      errores básicos. Te digo   │
│      cuáles tiene la tuya.      │
│      Sin cargo. En 24h.         │
│                                 │
│  ┌─────────────────────────┐   │
│  │ Nombre                   │   │
│  │ Web (URL)                │   │
│  │ WhatsApp                 │   │
│  │ [Quiero el diagnóstico]  │   │
│  └─────────────────────────┘   │
│                                 │
│  Mini testimonio (opcional):    │
│  "Wolfim nos modernizó el       │
│   portal completo." — Roggero   │
│   & Roma, Río Tercero           │
│                                 │
│  (sin footer visible)           │
└─────────────────────────────────┘
```

### Copy exacto

**Headline:**
```
Tu web tiene 3 errores que frenan consultas
```

**Subtítulo:**
```
La mayoría de las PyMEs pierde consultas por 3 errores básicos en su sitio.
Te digo cuáles tiene la tuya. Sin cargo. En 24 horas.
```

**Placeholders del formulario:**
- Nombre
- Web de tu empresa (ej: tuempresa.com.ar)
- WhatsApp (con código de país)

**Botón CTA:**
```
Quiero el diagnóstico
```

**Mini testimonio (debajo del form, tipografía chica, gris):**
```
"Wolfim nos modernizó el portal completo. Las consultas se ordenaron desde el primer mes."
— Silvia Roggero de Roma, Río Tercero
```

**Meta title (SEO):**
```
Diagnóstico gratuito de tu web | Wolfim Studio
```

### Comportamiento del formulario

- **Validación client-side:** nombre requerido, URL con formato válido, WhatsApp con al menos 8 dígitos
- **Submit:** POST a endpoint que almacene el lead (ver sección Backend abajo)
- **Post-submit:** mostrar mensaje: "Recibido. Juan te escribe por WhatsApp en menos de 24h con el diagnóstico."
- **Sin redirección externa.** El usuario se queda en la página.

### Reglas visuales

- **Sin menú de navegación.** Solo logo arriba a la izquierda (link a wolfim.com)
- **Sin footer** (o footer reducido a 1 línea: "Wolfim Studio — Río Tercero, Córdoba")
- **Sin WhatsApp flotante** (distrae del formulario)
- **Mobile-first:** el 80%+ del tráfico viene de Meta Ads en mobile
- **Above the fold en mobile:** headline + subtítulo + formulario visible sin scroll
- **Fondo:** mismo #fafaf8 del sitio
- **Altura mínima:** 100vh

---

## 📄 Página 2 — `/inmobiliarias`

### Estructura

```
┌─────────────────────────────────┐
│  Nav (misma que landing actual) │
│                                 │
│  Hero:                          │
│  H1: Portal inmobiliario        │
│      para inmobiliarias         │
│  P:  Sin depender de portales   │
│      externos. Con catálogo,    │
│      fichas, filtros y consultas│
│      por WhatsApp.              │
│  CTA: Ver caso real ↓           │
│                                 │
│  ─────────────────────────────  │
│                                 │
│  Caso: Roggero & Roma           │
│  Imagen del sitio (si hay)      │
│  "Rediseño completo de portal   │
│   inmobiliario. Catálogo de     │
│   propiedades, fichas, mapas,   │
│   reseñas, contacto por WA."    │
│                                 │
│  ─────────────────────────────  │
│                                 │
│  Qué incluye:                   │
│  • Home institucional           │
│  • Catálogo de propiedades      │
│  • Fichas individuales          │
│  • Filtros y buscador           │
│  • WhatsApp por propiedad       │
│  • Formulario de contacto       │
│  • Panel CMS autoadministrable  │
│  • SEO por ficha                │
│                                 │
│  ─────────────────────────────  │
│                                 │
│  Precio: Desde USD 450          │
│  Mantenimiento: USD 39/mes      │
│                                 │
│  CTA: Quiero un portal así → WA│
│                                 │
│  Footer (mismo que landing)     │
└─────────────────────────────────┘
```

### Copy

**Headline:**
```
Portal inmobiliario para inmobiliarias
```

**Subtítulo:**
```
Un portal propio con catálogo de propiedades, fichas individuales, filtros, buscador y consultas directas por WhatsApp. Sin depender de portales externos.
```

**Meta title (SEO):**
```
Página web para inmobiliarias — Portal con catálogo | Wolfim Studio
```

**Meta description:**
```
Portal inmobiliario con catálogo de propiedades, fichas, filtros, WhatsApp y CMS. Caso real: Roggero & Roma. Desde USD 450.
```

**CTA principal:**
```
Quiero un portal para mi inmobiliaria → (link WhatsApp con texto pre-armado)
```

### Reglas

- Misma nav que la landing actual
- Sección de pricing con mismo formato que la landing actual
- Mismo footer que la landing actual
- Sin imágenes de stock. Foto de Roggero & Roma si existe en el repo, sino solo tipografía.

---

## 🔧 Backend — manejo de leads

El formulario de `/diagnostico` necesita un endpoint mínimo.

**Opción más simple (recomendada para arrancar):**
- POST a `/api/leads` (API route de Astro o Next.js, según lo que ya use el proyecto)
- Almacenar en Supabase (Wolfim ya tiene proyecto)
- Tabla: `leads` con columnas `name`, `website`, `whatsapp`, `source` ('meta_ads_diagnostico'), `created_at`

**Si no querés tocar backend ahora:**
- El formulario puede enviar los datos a una Google Sheet vía Google Forms (embed o fetch)
- O directamente abrir WhatsApp de Juan con el texto pre-armado: "Hola Juan, quiero el diagnóstico. Mi web es [URL]. Soy [Nombre]."

**Decisión de Juan requerida** — ver sección final.

---

## ✅ Criterios de aceptación

### `/diagnostico`

- [ ] URL `wolfim.com/diagnostico` carga en < 2s (mobile)
- [ ] Mismas fuentes, colores y film grain que la landing actual
- [ ] Sin menú de navegación visible
- [ ] Formulario funcional (submit → mensaje de éxito o redirección)
- [ ] Mobile: formulario visible sin scroll
- [ ] PageSpeed mobile ≥ 85
- [ ] Meta title y description configurados
- [ ] OG image configurada

### `/inmobiliarias`

- [ ] URL `wolfim.com/inmobiliarias` carga correctamente
- [ ] Misma nav y footer que landing actual
- [ ] Meta title y description con keyword
- [ ] Estructura: hero → caso → qué incluye → precio → CTA
- [ ] Sin lorem ipsum, sin placeholders

---

## ⚠️ Lo que NO hay que hacer

- ❌ No tocar `index.astro` ni la landing actual
- ❌ No modificar `pricing` ni `process`
- ❌ No crear archivos CSS nuevos (usar variables del theme existente)
- ❌ No usar imágenes de stock
- ❌ No agregar dependencias nuevas al proyecto si no son estrictamente necesarias
- ❌ No deployar sin que Juan revise

---

## 📋 Para Juan — decisiones antes de build

1. **Backend del formulario:** ¿API route en Astro → Supabase, Google Sheet, o abrir WhatsApp directo?
2. **Imagen de Roggero & Roma** para la página `/inmobiliarias`: ¿hay captura en el repo o usamos solo tipografía?
3. **Prioridad:** ¿hacemos solo `/diagnostico` primero y validamos, o las dos juntas?

---

## 🔗 Archivos de referencia en el vault

- `companies/wolfim/intelligence/context.md` — identidad, productos, precios
- `companies/wolfim/intelligence/plan-ads-seo-2026-06-29.md` — estrategia completa
- `companies/wolfim/brand/` — logos y assets
