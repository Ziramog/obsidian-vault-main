---
title: Roggero & Roma — Auditoría GA4 inicial
type: analytics-audit
client: Roggero & Roma
property_id: 539918073
measurement_id: G-PW4FH9WHQB
owner: wolfim-growth
created: 2026-07-07
period: 2026-06-28_to_2026-07-07
status: complete
raw_data: roggero-roma-ga4-audit-2026-07-07.raw.json
---

# Roggero & Roma — Auditoría GA4 inicial

## Acceso verificado

- **Propiedad GA4:** `roggeroyroma.com.ar`
- **Property ID:** `539918073`
- **Stream:** `www.roggeroyroma.com.ar`
- **Measurement ID:** `G-PW4FH9WHQB`
- **URL del stream:** `https://www.roggeroyroma.com.ar`
- **Industria configurada:** Real Estate
- **Zona horaria:** America/Buenos_Aires
- **Moneda:** USD
- **Rol disponible:** Viewer / solo lectura

## Período analizado

**2026-06-28 → 2026-07-07**

Es un corte parcial desde la implementación anotada de Analytics. No es todavía el mes completo.

## Resumen numérico bruto

| Métrica | Valor |
|---|---:|
| Usuarios totales | 57 |
| Usuarios activos | 56 |
| Usuarios nuevos | 46 |
| Sesiones | 89 |
| Sesiones con engagement | 35 |
| Vistas de página | 355 |
| Vistas por sesión | 3.99 |
| Eventos totales | 600 |
| Eventos por sesión | 6.74 |
| Engagement rate | 39.3% |
| Bounce rate | 60.7% |
| Duración promedio de sesión | 179.8 s |
| Key events / conversiones | 0 |

## Evolución diaria

| Fecha | Usuarios activos | Sesiones | Vistas | Eventos | Key events |
|---|---:|---:|---:|---:|---:|
| 2026-06-28 | 1 | 2 | 3 | 8 | 0 |
| 2026-06-29 | 10 | 15 | 64 | 114 | 0 |
| 2026-06-30 | 9 | 14 | 66 | 115 | 0 |
| 2026-07-01 | 7 | 9 | 63 | 95 | 0 |
| 2026-07-02 | 12 | 12 | 36 | 68 | 0 |
| 2026-07-03 | 3 | 4 | 15 | 29 | 0 |
| 2026-07-04 | 5 | 6 | 19 | 34 | 0 |
| 2026-07-05 | 8 | 9 | 9 | 26 | 0 |
| 2026-07-06 | 7 | 13 | 60 | 86 | 0 |
| 2026-07-07 | 3 | 5 | 20 | 25 | 0 |

## Fuentes de tráfico

| Canal | Fuente / medio | Sesiones | Usuarios activos | Vistas | Engaged sessions | Key events |
|---|---|---:|---:|---:|---:|---:|
| Direct | `(direct) / (none)` | 40 | 33 | 56 | 4 | 0 |
| Referral | `accounts.google.com / referral` | 21 | 6 | 111 | 12 | 0 |
| Organic Search | `google / organic` | 14 | 12 | 75 | 12 | 0 |
| Referral | `vercel.com / referral` | 5 | 1 | 39 | 2 | 0 |
| Organic Search | `ar.search.yahoo.com / referral` | 4 | 2 | 57 | 4 | 0 |
| Unassigned | `(not set)` | 4 | 4 | 14 | 0 | 0 |
| Organic Search | `bing / organic` | 1 | 1 | 2 | 1 | 0 |
| Organic Social | `facebook.com / referral` | 1 | 1 | 1 | 0 | 0 |

### Lectura comercial

- Hay tráfico real de Google orgánico: **14 sesiones desde google / organic**.
- Hay tráfico directo relevante: **40 sesiones**.
- `accounts.google.com` y `vercel.com` probablemente mezclan uso interno/dev/admin, no deberían venderse a Franco como demanda real.
- Facebook aparece, pero todavía mínimo: **1 sesión**.

## Dispositivo

| Dispositivo | Usuarios activos | Sesiones | Vistas | Eventos | Key events |
|---|---:|---:|---:|---:|---:|
| Desktop | 41 | 58 | 250 | 412 | 0 |
| Mobile | 16 | 32 | 105 | 188 | 0 |

### Lectura comercial

- En este corte domina desktop, pero parte puede ser uso interno/admin.
- No asumir todavía que el público final es desktop hasta excluir administración y tráfico interno.

## Páginas públicas más vistas

| Página / filtro | Título | Vistas | Usuarios activos |
|---|---|---:|---:|
| `/` | Inicio | 72 | 37 |
| `/?type=Casa` | Propiedades | 17 | 11 |
| `/properties` | Propiedades | 10 | 5 |
| `/?type=Casa&page=2` | Propiedades | 8 | 6 |
| `/?type=Terreno` | Propiedades | 8 | 2 |
| `/` | Propiedades | 7 | 4 |
| `/properties/6a1e1efc09dc76e1323c940b` | Fernando Ferrari 86, B° Pellegrini · Córdoba | 5 | 2 |
| `/?type=Campo` | Propiedades | 4 | 1 |
| `/?type=Casa&page=3` | Propiedades | 4 | 4 |
| `/properties?page=5` | Propiedades | 4 | 2 |
| `/properties?page=6` | Propiedades | 4 | 2 |
| `/properties?type=Casa` | Propiedades | 4 | 2 |

## Tráfico interno / admin detectado

GA4 está midiendo también pantallas del panel administrativo.

| Clasificación | Vistas |
|---|---:|
| Páginas públicas aproximadas | 272 |
| Admin / panel / edición aproximado | 83 |
| Total | 355 |

Principales páginas internas detectadas:

| Página / título | Vistas |
|---|---:|
| Panel de Control | 17 |
| Admin — Propiedades | 13 |
| Editar Propiedad | 10 |
| `/admin` — Admin Propiedades | 10 |
| `/admin` — Editar Propiedad | 8 |

### Lectura comercial

Antes de mandar informe a Franco, conviene separar o excluir admin/internal. Si no, se inflan páginas vistas y sesiones que no representan demanda comercial.

## Eventos detectados

| Evento | Conteo | Usuarios | Key event |
|---|---:|---:|---:|
| `page_view` | 355 aprox. | 56 | 0 |
| `session_start` | 86 aprox. | 55 | 0 |
| `user_engagement` | 71 aprox. | 22 | 0 |
| `first_visit` | 46 | 46 | 0 |
| `scroll` | 31 | 17 | 0 |
| `form_start` | 8 | 7 | 0 |
| `click` | 2 | 2 | 0 |
| `click_whatsapp` | 1 | 1 | 0 |

## Clicks salientes detectados

| Evento | URL | Conteo | Usuarios |
|---|---|---:|---:|
| `click` | `https://wa.me/5493547563911` | 1 | 1 |
| `click` | `https://www.instagram.com/roggeroyroma` | 1 | 1 |
| `click_whatsapp` | sin linkUrl capturado | 1 | 1 |

## Formularios

GA4 registra `form_start`, pero no aparece `form_submit`.

| Página | Título | Form starts | Usuarios |
|---|---|---:|---:|
| `/` | Inicio | 3 | 3 |
| `/admin` | Editar Propiedad | 2 | 1 |
| `/` | Agregar Propiedad | 1 | 1 |
| `/` | Propiedades | 1 | 1 |
| `/?type=Inmueble+Comercial` | Propiedades | 1 | 1 |

### Lectura comercial

Hay señales de intención, pero incompletas:

- `form_start` existe.
- No hay `form_submit`.
- WhatsApp aparece parcialmente.
- No hay conversiones/key events reales.

## Key events / conversiones configuradas

GA4 tiene estas key events configuradas:

| Key event | Estado |
|---|---|
| `close_convert_lead` | configurado, 0 eventos |
| `qualify_lead` | configurado, 0 eventos |
| `purchase` | configurado, 0 eventos |

### Diagnóstico

Las key events configuradas son genéricas y no están alineadas con el sitio inmobiliario. Para Roggero & Roma deberían ser:

- `click_whatsapp`
- `form_submit` o `contact_form_submitted`
- `phone_clicked`
- opcional: `property_viewed` como microconversión, no key event principal

Con rol Viewer no puedo modificar esto desde Hermes. Hace falta acceso Editor o que Juan lo configure en GA4/GTM.

## Geografía

| País / ciudad | Usuarios activos | Sesiones | Vistas |
|---|---:|---:|---:|
| Singapore / Singapore | 15 | 15 | 15 |
| Argentina / not set | 13 | 28 | 200 |
| Argentina / Cordoba | 5 | 6 | 17 |
| United States / Council Bluffs | 5 | 5 | 5 |
| Argentina / Buenos Aires | 4 | 5 | 14 |
| Argentina / Rio Tercero | 3 | 16 | 79 |
| France / Paris | 3 | 3 | 3 |

### Lectura comercial

- Argentina concentra buena parte del engagement real.
- Singapore / Council Bluffs / Paris pueden ser bots, previews, herramientas, crawlers o tráfico técnico. No usar esos datos como demanda inmobiliaria.
- Río Tercero probablemente puede ser Juan/testing interno.

## Diagnóstico principal

### Lo bueno

1. GA4 está conectado y recibiendo datos.
2. El stream correcto está activo: `G-PW4FH9WHQB`.
3. Hay señales de tráfico real: directo + Google orgánico.
4. Ya aparece al menos 1 click a WhatsApp.
5. Ya hay información útil de páginas/filtros vistos: Casas, Terrenos, Propiedades.

### Lo débil

1. GA4 mezcla público + admin + testing interno.
2. No hay conversiones comerciales reales configuradas.
3. Hay key events genéricas (`purchase`, `qualify_lead`, `close_convert_lead`) que no se disparan.
4. `form_start` aparece, pero no `form_submit`.
5. `click_whatsapp` existe solo parcialmente y sin propiedades útiles como propiedad, ubicación o página.
6. No hay evidencia de Search Console conectada en este acceso.

## Qué NO mostrar todavía a Franco sin limpiar

- No mostrar “355 vistas” como demanda pura: incluye admin/interno.
- No mostrar geografía global como mercado real: hay tráfico de Singapore/USA/Paris probablemente no comercial.
- No hablar de conversiones: hoy son 0 key events.
- No mostrar panel/admin en páginas vistas.

## Qué SÍ se puede mostrar si Franco pide avance ahora

Mensaje prudente:

> “Ya tenemos Analytics recibiendo datos. En los primeros días vemos tráfico directo, tráfico desde Google y navegación por propiedades/filtros. Antes del informe mensual vamos a separar tráfico interno y dejar mejor medidos los contactos por WhatsApp/formulario para que el reporte sea comercial, no solo técnico.”

## Acciones recomendadas antes del 28/07

| Prioridad | Acción | Motivo |
|---|---|---|
| 🔴 | Excluir o separar `/admin` y pantallas internas | Evitar inflar reporte al cliente |
| 🔴 | Medir `click_whatsapp` en todos los CTAs con `page_path`, `property_id`, `property_title` | Saber qué propiedad genera consulta |
| 🔴 | Medir `form_submit` real | Hoy solo hay `form_start` |
| 🔴 | Marcar `click_whatsapp` y `form_submit` como key events | Medir conversiones reales |
| 🟡 | Medir `property_viewed` para fichas de propiedad | Ranking de interés por inmueble |
| 🟡 | Conectar Search Console | Saber consultas de Google |
| 🟡 | Crear vista/reporte Looker o plantilla PDF mensual | Entregable claro para Franco |

## Handoff técnico sugerido

Para `web-builder` / local:

1. No cargar GA4 en rutas `/admin` o enviar un parámetro `traffic_type=internal` para poder excluirlo.
2. Agregar helper `trackEvent(name, params)` alrededor de `gtag`.
3. Eventos mínimos:
   - `property_viewed`
   - `click_whatsapp`
   - `phone_clicked`
   - `email_clicked`
   - `contact_form_submitted`
   - `search_used`
4. En WhatsApp por propiedad enviar:
   - `property_id`
   - `property_title`
   - `operation`
   - `property_type`
   - `location`
   - `page_path`
5. En GA4 marcar como key events:
   - `click_whatsapp`
   - `contact_form_submitted`

## Criterio comercial para el reporte mensual

El informe a Franco tiene que mostrar:

1. Tráfico público limpio.
2. Top propiedades/filtros vistos.
3. Contactos reales o intentos de contacto.
4. Qué hacer el mes siguiente.

No vender GA4. Vender control comercial del sitio.
