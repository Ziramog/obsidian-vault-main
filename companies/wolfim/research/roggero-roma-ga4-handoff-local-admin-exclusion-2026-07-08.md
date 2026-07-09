---
title: Roggero & Roma — Handoff local para excluir tráfico interno en GA4
client: Roggero & Roma
type: local-handoff
owner: wolfim-growth
created: 2026-07-08
status: ready-for-local
supersedes: roggero-roma-ga4-code-implementation-2026-07-07.md
measurement_id: G-PW4FH9WHQB
---

# Roggero & Roma — Handoff local para excluir tráfico interno en GA4

## Contexto

Este cambio **no se implementa desde VPS**. Va por **local**.

Problema confirmado:

- GA4 está midiendo parte del uso interno/admin.
- Hoy eso contamina sesiones, vistas, horarios y lectura comercial del sitio.
- Hay **3 usuarios internos** que usan el admin y **se loguean**.
- Por eso, **filtrar solo por IP no alcanza**.

## Objetivo

Excluir de GA4:

1. Todo tráfico bajo `/admin`.
2. Todo tráfico bajo `/superadmin`.
3. Toda navegación hecha por usuarios logueados con rol interno (`admin` o `superadmin`), incluso si navegan páginas públicas.

Mantener medido:

- tráfico público real
- usuarios anónimos
- usuarios públicos no internos
- navegación comercial normal del sitio

## Decisión técnica

La fuente de verdad para excluir tráfico interno debe ser el **login / rol del usuario**, no la IP.

Motivo:

- la IP cambia
- pueden entrar desde oficina, casa o celular
- el login sí identifica de forma estable a los 3 usuarios internos

## Implementación exacta

### 1. Crear helper único de elegibilidad de tracking

Crear o reutilizar un helper tipo `utils/analytics.js` o equivalente con estas funciones:

- `isAllowedTrackingHost(hostname)`
- `isInternalTrackingRole(role)`
- `shouldTrackPath(pathname)`
- `canTrackAnalytics({ host, pathname, role })`
- opcional: `cleanParams(params)` para no mandar valores vacíos

### Reglas del helper

#### `isInternalTrackingRole(role)`
Debe devolver `true` para:

- `admin`
- `superadmin`

Debe devolver `false` para:

- visitantes anónimos
- `client`
- cualquier rol público/no interno

#### `shouldTrackPath(pathname)`
Debe devolver `false` si la ruta:

- es exactamente `/admin`
- empieza con `/admin/`
- es exactamente `/superadmin`
- empieza con `/superadmin/`

Debe devolver `true` para el resto de rutas públicas.

#### `canTrackAnalytics({ host, pathname, role })`
Debe devolver `true` **solo si**:

- el host es válido para producción/local permitido
- la ruta es pública
- el usuario **no** tiene rol interno

## 2. Corregir el componente de GA4

Punto de control principal esperado: `components/GoogleAnalytics.jsx` o equivalente.

### Requisitos

- componente client-side
- usar `useSession()` para leer el rol del usuario logueado
- usar `usePathname()` y `useSearchParams()`
- cargar GA4 con `send_page_view: false`
- enviar `page_view` manual solo si `canTrackAnalytics(...) === true`
- incluir querystring en `page_path`

### Lógica esperada

#### Si el usuario es interno (`admin` / `superadmin`)
- no mandar `page_view`
- no mandar eventos custom
- si prefieren, devolver `null` o hacer early return del tracking

#### Si la ruta es `/admin` o `/superadmin`
- no mandar `page_view`
- no mandar eventos custom

#### Si el usuario es público o anónimo y la ruta es pública
- sí mandar `page_view`
- sí mandar eventos comerciales

## 3. Reusar la misma guardia para eventos custom

Si ya existen o se agregan eventos como:

- `click_whatsapp`
- `click_phone`
- `click_email`
- `property_viewed`
- `contact_form_submitted`
- `search_used`

Todos deben pasar por la misma guardia de elegibilidad.

O sea: **si el usuario es interno o la ruta es interna, no se manda nada a GA4**.

## 4. No mandar PII

No enviar a GA4:

- nombre
- email
- teléfono
- mensaje libre del usuario

Sí está bien enviar:

- `property_id`
- `property_type`
- `operation`
- `cta_location`
- `page_path`
- `page_location`

## 5. Criterio de negocio

La regla correcta para este cliente es:

> si una visita proviene de alguien del equipo operando el sistema, no debe contar como demanda comercial.

Eso aplica incluso si el admin entra al home, propiedades o fichas públicas estando logueado.

## Archivos esperados a tocar en local

Según la investigación previa, los puntos más probables son:

- `components/GoogleAnalytics.jsx`
- `utils/analytics.js` o `lib/analytics.js`
- cualquier helper existente que dispare `gtag('event', ...)`

Si ya hay tracking de WhatsApp/teléfono/formulario, pasarlo por la misma guardia.

## Criterios de aceptación

El cambio queda bien si se cumple esto:

1. **Usuario anónimo** navegando una página pública:
   - sí aparece `page_view`

2. **Usuario logueado con rol `admin`** navegando home / propiedades / ficha:
   - no aparece `page_view`
   - no aparecen eventos custom

3. **Usuario logueado con rol `superadmin`**:
   - tampoco aparece tracking

4. **Ruta `/admin`**:
   - no aparece tracking

5. **Ruta `/superadmin`**:
   - no aparece tracking

6. **Usuario público/no interno**:
   - sí sigue apareciendo tracking normal

## Validación en local

### Prueba 1 — visitante normal
- abrir sitio en incógnito
- navegar home + propiedades + una ficha
- validar en GA4 DebugView que entran `page_view`

### Prueba 2 — admin logueado
- loguearse con un usuario `admin`
- navegar home + propiedades + ficha + admin
- validar que **no** entren `page_view`
- validar que **no** entren eventos custom

### Prueba 3 — segundo rol interno
- repetir con `superadmin` si existe

### Prueba 4 — evento comercial
- desde incógnito o usuario público, disparar WhatsApp / CTA
- validar que el evento sí aparezca

### Prueba 5 — control de reporte
- esperar 24–48 h
- comparar si bajan vistas/sesiones internas y mejora la lectura comercial

## Importante

- No depender solo de IP.
- No resolver esto desde GA4 con filtros manuales únicamente.
- La exclusión correcta para este caso es **desde el código, usando estado de login/rol**.

## Nota operativa

No quedó ningún cambio aplicado desde VPS.
Cualquier prueba de implementación hecha acá fue descartada y eliminada.

## Referencias relacionadas

- `companies/wolfim/research/roggero-roma-ga4-code-implementation-2026-07-07.md`
- `companies/wolfim/research/roggero-roma-ga4-audit-2026-07-07.md`
- `companies/wolfim/research/roggero-roma-informe-mensual-analytics-cliente-2026-07-07.md`
