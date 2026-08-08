---
company: Wolfim
project: wolfim-motors-demo
status: ready-for-antigravity
created: 2026-08-07
source-handoff: HO-2026-08-03-002
phase: P1-internal-stock
execution-target: C:\Projects\wolfim-motors-demo
---

# Wolfim Motors Demo — prompt definitivo para Antigravity
## P1: módulo interno privado de stock, documentación, mantenimiento y preparación

## Mandato de ejecución

Trabajá exclusivamente sobre el proyecto existente:

`C:\Projects\wolfim-motors-demo`

No crear otro proyecto, no clonar nuevamente Roggero & Roma y no reconstruir el showroom desde cero.

El showroom público fue confirmado comercialmente como **LISTO** por Juan. No debe rediseñarse ni convertirse nuevamente en un sprint P0.

La tarea activa es implementar de punta a punta un módulo interno privado sólido y clonable para concesionarias.

No detenerse después de crear modelos, componentes aislados, un plan o una maqueta. La tarea termina únicamente cuando:

- funciona el login real;
- las rutas privadas están protegidas;
- existe una vista interna de stock operativa;
- existe una ficha privada completa por vehículo;
- documentación, mantenimiento y checklist persisten;
- no se filtra ningún dato privado;
- build, lint, tests y browser QA fueron ejecutados;
- se entregó evidencia real.

No hacer commit, push ni deploy sin autorización explícita de Juan.

---

# 1. Objetivo

Extender Wolfim Motors Demo para que pueda presentarse comercialmente como:

> Showroom público listo + sistema interno privado para ordenar stock, documentación, mantenimiento, preparación, responsables y datos económicos de cada vehículo.

La aplicación debe quedar compuesta por dos capas claramente separadas.

## Capa pública

Lo que puede consultar un comprador:

- home;
- catálogo;
- filtros;
- ficha pública;
- fotos;
- precio;
- estado comercial público;
- WhatsApp;
- historia 9:16;
- metadata;
- OpenGraph;
- sitemap.

## Capa privada

Lo que puede consultar exclusivamente una persona autenticada con rol `admin` o `superadmin`:

- código interno;
- patente;
- VIN;
- número de motor;
- fecha y origen de ingreso;
- ubicación física;
- estado interno;
- responsable;
- estado técnico;
- notas internas;
- costo de compra/toma;
- margen objetivo;
- precio mínimo;
- documentación;
- vencimientos;
- mantenimiento;
- costos de preparación;
- checklist prepublicación.

---

# 2. Contexto técnico verificado

## Proyecto

- Ruta absoluta: `C:\Projects\wolfim-motors-demo`
- Repo: `https://github.com/Ziramog/wolfim-motors-demo.git`
- Rama inicial verificada: `main`

Stack:

- Next.js 14.2.4 App Router
- React 18
- JavaScript/JSX predominante
- TypeScript parcialmente configurado
- Tailwind CSS 3.4
- MongoDB
- Mongoose 8.5
- NextAuth 4.24
- Cloudinary
- Vercel Blob instalado
- Zod instalado
- Server Actions
- Vercel

## Estado técnico previo verificado

- `npm run build`: OK.
- `npx tsc --noEmit`: OK, pero el `tsconfig` actual incluye principalmente TS/TSX; no tomarlo como validación completa del código JS/JSX.
- `npm run lint`: no puede completarse porque `next lint` abre un prompt interactivo; falta configurar ESLint.
- Preview local accesible en `http://localhost:3000` durante la auditoría.
- Home pública visible.
- Catálogo `/autos` visible.
- Ficha pública visible.
- Hay 12 vehículos en la DB actual.
- WhatsApp por vehículo genera mensaje contextual.
- `/api/story/2024-ferrari-sf90-spider` devuelve HTTP 500.

## Problemas de seguridad verificados

### Bypass 1

`utils/getSessionUser.js` devuelve siempre un usuario demo superadmin hardcodeado.

### Bypass 2

`components/AuthProvider.jsx` inyecta siempre una `demoSession`, un `demo-admin-id` y rol `superadmin`. La UI cree que siempre hay una sesión válida.

### Bypass 3

`middleware.js` tiene `matcher: []`; por lo tanto no protege ninguna ruta.

### Bypass 4

El middleware contiene una excepción general para POST con header `next-action`. No debe quedar una autorización universal de Server Actions basada solamente en ese header.

### Endpoint expuesto

`app/api/admin/vehicles/route.js` devuelve vehículos sin validar sesión.

### Configuración pública con datos internos

`app/api/site-config/route.js` y su ruta duplicada devuelven públicamente `signatureBase64`, `exchangeRateARS` y campos que no son necesarios en el DTO público.

---

# 3. Reglas obligatorias del repositorio

Antes de modificar código:

1. Leer:
   - `AGENTS.md`
   - `PROJECT_CONTEXT.md`
   - `README.md`
   - `MANUAL_ADMIN.md`
   - `package.json`
   - `.gitignore`

2. Ejecutar y registrar:
   - `git status --short`
   - `git branch --show-current`
   - `git remote -v`

3. Informar cambios preexistentes antes de editar.

4. No ejecutar:
   - `git pull`
   - `git reset`
   - `git clean`
   - `git checkout` para descartar cambios
   - `git restore` para descartar cambios
   - force push
   - comandos que eliminen trabajo local

5. No modificar ni eliminar archivos dirty/untracked preexistentes sin entender su origen.

6. No mostrar ni imprimir:
   - `.env.local`
   - tokens
   - contraseñas
   - connection strings
   - secretos
   - credenciales OAuth

7. Mantener obligatoriamente `images.unoptimized = true` en la configuración de Next.js.

8. No tocar producción ni datos de Roggero & Roma.

9. No usar usuarios, imágenes, documentos, storage ni datos reales de clientes.

10. Presentar un plan de implementación por fases antes de editar, pero continuar luego con la ejecución completa sin detenerse en el plan.

---

# 4. Decisiones arquitectónicas obligatorias

## 4.1 No guardar datos privados dentro del documento público Vehicle

Implementar una colección separada uno-a-uno:

```text
Vehicle
    1 ───── 1
VehicleInternal
```

Crear:

`models/VehicleInternal.js`

El modelo público `Vehicle` debe seguir conteniendo exclusivamente:

- datos públicos;
- flags públicos;
- referencias técnicas necesarias para operar el showroom.

El nuevo modelo `VehicleInternal` debe almacenar todos los datos privados.

Esta separación es obligatoria porque actualmente varias rutas públicas consultan y serializan documentos completos de `Vehicle`. Una colección separada reduce el riesgo de exposición accidental.

## 4.2 Relación uno-a-uno

`VehicleInternal` debe contener:

```js
vehicle: {
  type: Schema.Types.ObjectId,
  ref: 'Vehicle',
  required: true,
  unique: true,
  index: true
}
```

Cada vehículo debe tener como máximo un registro interno.

## 4.3 Separación de estados

Mantener separados:

- `Vehicle.status`: estado comercial público.
- `VehicleInternal.internalStatus`: estado operativo interno.
- `Vehicle.published`: controla si el vehículo es visible públicamente.

Estado comercial público existente:

- disponible
- reservado
- vendido

Estado interno:

- `to_review`
- `in_preparation`
- `ready_to_publish`
- `published`
- `reserved`
- `sold`
- `delivered`

No sincronizar automáticamente ambos estados de manera irreversible.

Puede existir, por ejemplo:

```text
status público: disponible
internalStatus: in_preparation
published: false
```

## 4.4 Estrategia de lectura/escritura

Preferencia arquitectónica:

- lecturas internas desde Server Components protegidos;
- mutaciones mediante Server Actions protegidas;
- evitar agregar APIs privadas innecesarias;
- cualquier API privada existente o nueva debe validar sesión y rol;
- ninguna mutación debe confiar solamente en la UI o middleware.

---

# 5. Normalizar el modelo público Vehicle

El schema actual presenta inconsistencias:

- existe `featured`;
- varias rutas consultan `is_featured`;
- la UI usa `is_published`;
- `is_published` no está declarado en `VehicleSchema`.

Normalizar a estos nombres canónicos:

```js
featured: {
  type: Boolean,
  default: false,
  index: true
}

published: {
  type: Boolean,
  default: true,
  index: true
}
```

Eliminar del código activo el uso de:

- `is_featured`
- `is_published`

Actualizar:

- dashboard admin;
- tabla admin;
- toggle featured;
- toggle published;
- home;
- catálogo;
- resultados de búsqueda;
- ficha;
- sitemap;
- OpenGraph;
- story;
- contadores;
- filtros;
- revalidaciones.

## Migración de compatibilidad

La migración debe:

1. Leer documentos existentes sin destruirlos.
2. Si existe `is_published`, copiar su valor a `published`.
3. Si no existe, usar `published: true` para conservar visible el stock actual.
4. Si existe `is_featured` y no existe `featured`, copiarlo.
5. No borrar imágenes ni vehículos.
6. No usar `deleteMany()`.
7. Ser idempotente.
8. Poder ejecutarse más de una vez sin duplicar ni corromper datos.

---

# 6. Modelo VehicleInternal

Crear sub-schemas independientes con `{ _id: true }` para que documentación y mantenimiento puedan editarse/eliminarse por identificador.

## 6.1 Campos principales

```text
vehicle
internalStockCode
licensePlate
vin
engineNumber
internalNotes
internalStatus
entryDate
stockOrigin
physicalLocation
technicalStatus
assignedSeller
purchaseCost
targetMargin
minimumSalePrice
currency
documentationChecklist
maintenanceHistory
prePublishChecklist
migrationVersion
createdAt
updatedAt
```

## 6.2 Código interno

`internalStockCode` debe ser:

- requerido;
- trim;
- uppercase;
- único;
- indexado;
- no derivado únicamente del `_id`;
- legible, por ejemplo `WM-2026-001`.

## 6.3 Patente

`licensePlate` debe ser:

- opcional;
- trim;
- uppercase;
- unique sparse si la compatibilidad de datos lo permite;
- index sparse;
- privado.

No usar patentes reales en seeds. Usar valores evidentes de demo, por ejemplo `DEMO-A01`.

## 6.4 VIN

`vin` debe ser:

- opcional;
- trim;
- uppercase;
- unique sparse;
- index sparse;
- privado.

No usar VIN reales. El seed debe utilizar valores explícitamente ficticios.

## 6.5 Número de motor

`engineNumber` debe ser opcional, trim, uppercase y privado.

## 6.6 Estado interno

Enum obligatorio:

```text
to_review
in_preparation
ready_to_publish
published
reserved
sold
delivered
```

Default: `to_review`.

Labels UI:

```text
to_review → A revisar
in_preparation → En preparación
ready_to_publish → Listo para publicar
published → Publicado
reserved → Reservado
sold → Vendido
delivered → Entregado
```

## 6.7 Origen del stock

Enum:

```text
purchase
trade_in
consignment
other
```

Labels:

```text
purchase → Compra
trade_in → Toma / permuta
consignment → Consignación
other → Otro
```

## 6.8 Campos económicos

```text
purchaseCost
targetMargin
minimumSalePrice
currency
```

Reglas:

- Number finito;
- no aceptar negativos;
- `targetMargin` representa porcentaje;
- moneda centralizada, default sugerido `USD`;
- no mostrar en rutas públicas;
- no registrar en analytics;
- no incluir en logs;
- no incluir en mensajes de error públicos.

## 6.9 Notas internas

`internalNotes`:

- string;
- trim;
- máximo razonable, por ejemplo 5000 caracteres;
- no renderizar con `dangerouslySetInnerHTML`;
- no incluir en metadata, story, OpenGraph ni payload público.

---

# 7. Checklist documental

Crear sub-schema `DocumentationItem` con:

```text
_id
type
status
observation
issueDate
expirationDate
fileReference
customLabel
updatedAt
```

## Tipos obligatorios

```text
title
registration_card
form_08
domain_report
police_verification
debt_clearance
vtv_rto
invoice_or_contract
service_records
warranty
manuals
other
```

Labels en español:

```text
title → Título
registration_card → Cédula
form_08 → Formulario 08
domain_report → Informe de dominio
police_verification → Verificación policial
debt_clearance → Libre deuda
vtv_rto → VTV / RTO
invoice_or_contract → Factura o boleto
service_records → Comprobantes de service
warranty → Garantía
manuals → Manuales
other → Otros
```

## Estados obligatorios

```text
missing
pending
received
verified
not_applicable
```

Labels:

```text
missing → Faltante
pending → Pendiente
received → Recibido
verified → Verificado
not_applicable → No aplica
```

## Comportamiento

- Cada vehículo debe iniciar con los tipos documentales mínimos.
- Permitir actualizar estado, observación y fechas.
- Para `other`, permitir `customLabel`.
- Mostrar documentos vencidos.
- Mostrar próximos a vencer si entra naturalmente en el alcance.
- Mostrar total, verificados, pendientes, faltantes, vencidos y porcentaje.

## Archivos privados

En P1 no implementar carga binaria salvo que exista almacenamiento privado real con:

- autenticación;
- autorización;
- bucket privado;
- URL temporal/firmada;
- validación MIME;
- validación de tamaño;
- expiración.

No usar:

- Cloudinary público;
- Vercel Blob público;
- links ocultos;
- URLs difíciles de adivinar;
- archivos dentro de `/public`.

En P1, `fileReference` es solamente una referencia textual opcional. La carga privada de PDF/imágenes queda P2.

---

# 8. Historial de mantenimiento y preparación

Crear sub-schema `MaintenanceEntry` con:

```text
_id
date
type
description
status
cost
provider
notes
createdAt
updatedAt
```

## Tipos

```text
mechanical_inspection
oil_filters
brakes
battery
tires
front_end
alignment_balancing
electrical_inspection
cosmetic_repair
detailing_wash
service
other
```

## Estados

```text
pending
in_progress
done
cancelled
```

## CRUD obligatorio

El administrador debe poder:

- crear entrada;
- editar entrada;
- eliminar entrada con confirmación;
- cambiar estado;
- registrar costo;
- registrar proveedor/taller;
- registrar notas.

Cada mutación debe:

- validar sesión;
- validar rol;
- validar ObjectId;
- validar que el vehículo existe;
- validar que el registro interno corresponde al vehículo;
- usar allow-list;
- no aceptar payload arbitrario;
- revalidar únicamente rutas necesarias;
- devolver errores seguros.

## Resumen

Mostrar:

- tareas pendientes;
- tareas en progreso;
- tareas realizadas;
- costo total de preparación;
- última actividad.

---

# 9. Checklist prepublicación

Guardar como array de items con claves estables:

```text
photos_uploaded
price_defined
documentation_reviewed
mechanical_reviewed
detailing_completed
description_approved
public_page_reviewed
story_generated
published_on_website
shared_on_social
published_external_portal
```

Cada item debe tener:

```text
key
completed
notes
updatedAt
```

Mostrar cantidad completada, total, porcentaje, barra de progreso y pendientes.

No bloquear automáticamente la publicación en P1. Permitir publicar mostrando una advertencia no bloqueante si faltan items.

---

# 10. Validación de inputs

Usar Zod, ya instalado.

Crear, por ejemplo:

`lib/validation/internalStock.js`

Schemas sugeridos:

```text
internalVehicleSchema
documentationItemSchema
maintenanceEntrySchema
prePublishChecklistSchema
internalStockFiltersSchema
```

Reglas:

- rechazar claves desconocidas;
- parsear números explícitamente;
- validar fechas;
- validar enums;
- validar ObjectId antes de consultar Mongo;
- limitar strings;
- no pasar `request.json()` o `FormData` directamente a `$set`;
- no construir filtros Mongo directamente desde parámetros del usuario;
- escapar búsquedas regex;
- evitar NoSQL injection;
- no silenciar errores con catch vacío.

---

# 11. Autenticación real

## 11.1 Eliminar modos demo inseguros

Modificar:

```text
utils/getSessionUser.js
components/AuthProvider.jsx
middleware.js
utils/authOptions.js
```

Eliminar:

- sesión superadmin hardcodeada;
- `demo-admin-id`;
- credenciales hardcodeadas;
- `matcher: []`;
- bypass universal por `next-action`;
- logs de email, token ID o rol innecesarios.

## 11.2 CredentialsProvider

Agregar CredentialsProvider a NextAuth.

Variables:

```text
DEMO_ADMIN_EMAIL
DEMO_ADMIN_PASSWORD
NEXTAUTH_SECRET
NEXTAUTH_URL
```

Reglas:

- valores solo en variables de entorno;
- no guardar contraseña en Mongo;
- no escribir valores en README;
- no imprimir valores;
- comparar credenciales en servidor;
- usar comparación segura;
- error genérico para credenciales incorrectas;
- si faltan variables, fallar de forma segura;
- no aceptar valores vacíos.

## 11.3 Usuario Mongo válido

El admin autenticado debe tener un `_id` Mongo válido.

Al iniciar sesión correctamente:

- buscar usuario por email;
- si no existe, crearlo con rol `admin`;
- si existe, reutilizarlo;
- no guardar password;
- devolver `_id` real en JWT/session.

Actualizar `UserSchema` para roles:

```text
client
admin
superadmin
```

## 11.4 GoogleProvider

Mantenerlo solo cuando existan:

```text
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
```

No romper build si faltan. Una cuenta nueva de Google entra como `client`, nunca admin automático.

## 11.5 Sesión

`getSessionUser()` debe:

- llamar `getServerSession(authOptions)`;
- devolver `null` sin sesión;
- devolver `_id`, email y rol con sesión válida;
- no fabricar datos;
- no loguear datos sensibles.

## 11.6 AuthProvider

`components/AuthProvider.jsx` debe dejar de pasar sesión demo y usar SessionProvider con sesión real.

## 11.7 Login UI

Crear `app/login/page.jsx` con:

- email;
- contraseña;
- submit;
- loading;
- botón deshabilitado durante submit;
- mensaje genérico de error;
- callbackUrl segura;
- responsive;
- touch targets mínimos de 44px;
- diseño Wolfim Motors;
- sin mostrar variables ni credenciales demo.

Navbar debe mostrar un único acceso claro `Ingresar`, no un botón repetido por provider.

## 11.8 Logout

Verificar que:

- `signOut()` elimine sesión;
- `/admin` vuelva a redirigir a `/login`;
- Back no permita operar una página privada cacheada;
- las páginas privadas sean dinámicas/no-store.

---

# 12. Autorización y protección por capas

## Roles permitidos

Módulo interno:

- `admin`
- `superadmin`

No permitido:

- `client`
- anónimo

## Páginas privadas

Proteger:

```text
/admin
/admin/*
/superadmin
/superadmin/*
/messages
/messages/*
/profile
/profile/*
```

## APIs privadas

Proteger:

```text
/api/admin/*
/api/superadmin/*
/api/user/*
```

Auditar además:

```text
/api/quotations/*
/api/site-config PATCH
/api/quotations/generate-ai
/api/quotations/upload-logo
```

No romper rutas públicas intencionales como `/p/[token]`, pero impedir mutaciones administrativas sin sesión.

## Helper obligatorio

Crear `utils/requireAdmin.js` o equivalente.

Debe diferenciar:

- sin sesión → 401;
- sesión sin rol → 403;
- admin/superadmin → continúa.

Para páginas Server Component:

- redirigir a `/login`;
- conservar callbackUrl segura.

Para APIs:

- JSON 401/403;
- no HTML redirect.

Para Server Actions:

- error seguro antes de conectar o mutar.

## Defensa en profundidad

No confiar solamente en middleware. También validar en:

- Server Actions;
- API Routes;
- layouts/pages privadas;
- crear/editar/eliminar vehículo;
- publicar/despublicar;
- featured;
- mantenimiento;
- documentación;
- checklist;
- configuración;
- exportaciones.

## Auditoría de getSessionUser

Buscar todos los consumidores y clasificarlos.

Deben exigir admin:

- alta, edición y eliminación de vehículo;
- toggle published/featured;
- custom labels;
- cotizaciones administrativas;
- configuración;
- mantenimiento;
- documentación;
- checklist;
- datos internos.

Deben tolerar sesión opcional o cliente, según comportamiento actual:

- bookmarks;
- navegación pública;
- páginas guardadas;
- mensajería pública.

No reemplazar todos los consumidores por `requireAdmin()` sin revisar intención.

---

# 13. Layout privado

`app/admin/layout.jsx` actualmente es Client Component y no realiza guard server-side.

Separar en:

```text
app/admin/layout.jsx            → Server Component con requireAdmin()
components/admin/AdminShell.jsx → Client Component visual
```

El layout server debe:

- verificar sesión;
- impedir render privado sin auth;
- marcar ruta dinámica;
- evitar cache compartida;
- entregar al shell solo datos mínimos.

Aplicar criterio equivalente en superadmin.

---

# 14. DTO público obligatorio

Crear `utils/publicVehicleDto.js` con allow-list, no block-list.

## Campos públicos permitidos

```text
id
slug
brand
model
version
year
kilometers
fuel
transmission
bodyType
color
engine
drivetrain
condition
status
customLabel
priceArs
priceUsd
featured
published
images[].url
equipment
description
createdAt
updatedAt
```

## Campos que no deben salir

```text
owner
images[].public_id
__v
VehicleInternal
internalStockCode
licensePlate
vin
engineNumber
internalNotes
internalStatus
entryDate
stockOrigin
physicalLocation
technicalStatus
assignedSeller
purchaseCost
targetMargin
minimumSalePrice
documentationChecklist
maintenanceHistory
prePublishChecklist
migrationVersion
```

Usar doble defensa:

1. Projection Mongo con campos públicos.
2. DTO allow-list antes de serializar.

No serializar un documento completo con `JSON.parse(JSON.stringify(vehicle))` ni spread indiscriminado hacia Client Components públicos.

Crear DTOs especializados si hace falta:

```text
publicVehicleCardDto
publicVehicleDetailDto
publicStoryVehicleDto
adminVehicleDto
publicSiteConfigDto
```

---

# 15. Auditar todas las rutas públicas

Aplicar projection + DTO a:

```text
app/page.jsx
app/autos/page.jsx
app/autos/search-results/page.jsx
app/autos/[id]/page.jsx
app/autos/[id]/opengraph-image.jsx
app/api/story/[id]/route.jsx
app/sitemap.js
app/profile/page.jsx
app/autos/saved/page.jsx
components/StoryShareButton.jsx
components/VehicleCard.jsx
components/FeaturedVehicleCard.jsx
components/ProfileVehicles.jsx
components/JsonLd.jsx
```

Revisar cualquier uso de:

```text
Vehicle.find
Vehicle.findOne
Vehicle.findById
convertToSerializeableObject
JSON.stringify(vehicle)
{ ...vehicle }
```

## Vehículos no publicados

Rutas públicas solo con `published: true`.

Un vehículo con `published: false` no debe aparecer en:

- home;
- catálogo;
- búsqueda;
- sitemap;
- OpenGraph;
- story pública;
- metadata;
- JSON-LD.

La ficha pública de un vehículo no publicado debe responder 404 para anónimos. Un preview admin debe ser privado y separado.

---

# 16. Corregir Compartir historia 9:16

Corregir:

```text
app/api/story/[id]/route.jsx
components/StoryShareButton.jsx
```

## Endpoint

Definir:

```js
const size = {
  width: 1080,
  height: 1920
}
```

La respuesta debe:

- devolver HTTP 200;
- `Content-Type: image/png`;
- medir 1080x1920;
- usar solo DTO público;
- rechazar no publicados;
- usar `NEXT_PUBLIC_SITE_URL` o config equivalente;
- incluir URL o QR válido;
- incluir branding configurable;
- incluir marca/modelo/año;
- incluir precio o CTA;
- incluir estado público;
- no usar contacto hardcodeado incorrecto.

La dependencia `qrcode` ya existe. Usarla si es viable para un QR real de la ficha pública.

## Botón cliente

Antes de crear File, verificar `response.ok` y `Content-Type`.

En dispositivos compatibles:

- crear File PNG;
- comprobar `navigator.canShare({ files })`;
- abrir share sheet;
- manejar cancelación sin error crítico.

Fallback desktop:

- Blob;
- Object URL;
- `<a download>`;
- click programático;
- revocar Object URL.

Probar al menos:

- `/api/story/2024-ferrari-sf90-spider`
- una segunda unidad.

---

# 17. Configuración pública vs privada

## Problema actual

`/api/site-config` expone `signatureBase64`, `exchangeRateARS` y datos administrativos.

## Solución

Separar `publicSiteConfigDto` y `privateSiteConfigDto`.

El GET público solo puede devolver:

```text
siteName
shortName
logoUrl
heroTitle
heroSubtitle
aboutTitle
aboutSubtitle
aboutText
footerDescription
contactEmail
contactPhoneDisplay
contactPhoneE164
contactAddress
businessHours
socialLinks
whatsappDefaultMessage
currency
baseUrl
seoTitle
seoDescription
accentColor
analyticsId público si corresponde
facebookPixelId público si corresponde
```

No devolver públicamente:

```text
signatureBase64
exchangeRateARS
internal config
private storage config
auth config
secrets
```

Consolidar la duplicación entre `/api/site-config` y `/api/site-config/site-config` después de verificar consumidores.

---

# 18. Vista interna de stock

Crear:

`app/admin/internal-stock/page.jsx`

Agregar acceso `Stock interno` desde `app/admin/page.jsx` y navegación admin.

## Datos por fila

- miniatura;
- código interno;
- marca/modelo/versión/año;
- patente;
- fecha de ingreso;
- días en stock;
- ubicación;
- estado interno;
- estado público;
- publicado/no publicado;
- resumen documental;
- mantenimiento pendiente;
- responsable;
- acción Ver ficha.

## Días en stock

Calcular desde `entryDate` hasta fecha actual. Si falta: `Sin fecha`. No guardar contador diario en DB.

## Búsqueda

- código interno;
- marca;
- modelo;
- versión;
- patente;
- VIN.

Escapar búsquedas regex.

## Filtros

- estado interno;
- documentación incompleta;
- documentación vencida;
- mantenimiento pendiente;
- responsable;
- ubicación;
- publicado/no publicado;
- estado público.

## Orden

- más días en stock;
- ingresos recientes;
- código interno;
- marca/modelo;
- estado interno.

Default: más días en stock.

## Contadores

- A revisar;
- En preparación;
- Listo para publicar;
- Publicado;
- Reservado;
- Vendido;
- Entregado.

Los contadores deben basarse en el total, no solamente en la página actual.

## Paginación

- default 25;
- máximo 100.

## Responsive

Desktop: tabla.

Tablet/iPad:

- tabla compacta o cards;
- sin depender de hover;
- acciones visibles;
- targets de 44px.

Mobile:

- cards;
- filtros colapsables/drawer;
- sin overflow crítico.

---

# 19. Ficha privada por vehículo

Mantener `/admin/vehicles/[id]/edit` y organizarla por tabs:

```text
public
internal
documentation
maintenance
checklist
```

Labels:

```text
Ficha pública
Interno
Documentación
Mantenimiento
Checklist
```

Persistir tab en URL con `?tab=`.

## Ficha pública

Mantener formulario actual y corregir:

- `featured` vs `is_featured`;
- `published` vs `is_published`;
- labels legacy;
- `AMOBLADA`;
- textos “propiedad”.

Agregar `Ver ficha pública` solo si está publicada.

## Interno

Editar:

- código;
- patente;
- VIN;
- motor;
- ingreso;
- origen;
- ubicación;
- estado interno;
- responsable;
- estado técnico;
- notas;
- costo;
- margen;
- precio mínimo;
- moneda.

Marcar visualmente `Información privada` y separar costos internos de precios públicos.

## Documentación

- checklist;
- estado;
- observaciones;
- fechas;
- referencia;
- badges;
- resumen;
- vencidos.

## Mantenimiento

- listado cronológico;
- crear;
- editar;
- eliminar;
- estado;
- costo;
- proveedor;
- notas;
- resumen.

## Checklist

- items requeridos;
- progreso;
- notas;
- fecha actualización;
- advertencia antes de publicar si quedan pendientes.

## UX de formularios

- deshabilitar botón durante submit;
- `Guardando...`;
- evitar doble envío;
- mostrar success solo tras persistir;
- reactivar en error;
- conservar datos en error;
- mensajes específicos pero seguros;
- no redirigir inesperadamente;
- formularios separados por tab.

---

# 20. Server Actions

Crear acciones separadas, por ejemplo:

```text
app/actions/updateVehiclePublic.js
app/actions/updateVehicleInternal.js
app/actions/updateDocumentationItem.js
app/actions/createMaintenanceEntry.js
app/actions/updateMaintenanceEntry.js
app/actions/deleteMaintenanceEntry.js
app/actions/updatePrePublishChecklist.js
```

También pueden agruparse en `app/actions/internalStock/`.

Cada acción debe:

1. Ejecutar `requireAdmin()`.
2. Validar con Zod.
3. Validar ObjectId.
4. Consultar vehículo.
5. Consultar/crear registro interno correcto.
6. Usar allow-list.
7. No aceptar `vehicleId` del formulario como única prueba de pertenencia.
8. Persistir.
9. Revalidar rutas mínimas.
10. Devolver resultado serializable seguro.

No usar `findByIdAndUpdate(id, body)` con body completo del cliente.

---

# 21. Operaciones del vehículo

Debe ser posible:

- crear;
- editar;
- publicar;
- despublicar;
- cambiar estado público;
- cambiar estado interno;
- marcar featured;
- abrir ficha pública;
- abrir ficha interna;
- eliminar con confirmación.

## Alta

Al crear Vehicle:

1. Crear Vehicle público.
2. Crear/upsert VehicleInternal asociado.
3. Asignar `internalStockCode`.
4. Crear documentación default.
5. Crear checklist default.
6. Si falla la segunda parte, manejar rollback seguro o estado parcial; no declarar éxito falso.

No guardar `owner: demo-admin-id`. Debe ser ObjectId Mongo válido.

## Eliminación

- verificar admin;
- eliminar imágenes según pipeline existente;
- eliminar VehicleInternal asociado;
- evitar huérfanos;
- no silenciar fallos parciales.

---

# 22. Migración y seed

## No usar seed destructivo

El seed actual contiene `Vehicle.deleteMany()`. No ejecutarlo contra DB actual.

## Migración idempotente

Crear `scripts/migrate-internal-stock.mjs` con:

- dry run por defecto;
- `--apply` para aplicar.

Informar solamente:

- cantidad de vehículos;
- cantidad con internal record;
- cantidad a crear;
- cantidad a migrar;
- cantidad con faltantes críticos;
- cero secretos.

## Identificar DB

Antes de aplicar:

- confirmar DB del demo Wolfim Motors;
- no imprimir URI;
- no aplicar si apunta a Roggero/cliente real;
- si no puede confirmarse, detener escritura DB y reportar bloqueo.

## Backup

Antes de modificar datos existentes:

- exportar colecciones afectadas a carpeta local ignorada;
- no commitear backup;
- no mostrar contenido sensible;
- documentar ruta y fecha.

Agregar a `.gitignore` si hace falta:

```text
.local-backups/
.qa-artifacts/
```

## Internal records

Crear VehicleInternal para cada vehículo existente con defaults seguros.

## Seed interno demo

Crear `scripts/seed-internal-demo.mjs`:

- idempotente;
- no borra vehículos;
- carga datos ficticios en al menos dos vehículos existentes;
- usa slugs conocidos;
- no usa VIN, patente, costos o personas reales;
- no sobrescribe modificaciones humanas salvo flag explícito;
- soporta dry run.

Valores claramente ficticios:

```text
DEMO-A01
DEMO-A02
DEMO-VIN-001
DEMO-VIN-002
Vendedor Demo
Taller Demo
```

## Rollback

Documentar:

- qué crea/modifica;
- cómo revertir migración recién aplicada;
- por qué no hacer rollback destructivo después de uso real;
- cómo restaurar backup.

---

# 23. Clonabilidad por concesionaria

Modelo comercial:

`un proyecto + deploy + DB + storage + usuarios por concesionaria`

No implementar multi-tenancy.

## Configuración central

Crear una estrategia coherente entre:

```text
config/dealership.js
models/SiteConfig.js
utils/getSiteConfig.js
```

Los defaults pueden vivir en config; Mongo puede sobrescribir campos editables.

No duplicar defaults incompatibles entre Navbar, Footer, Layout, SiteConfig, getSiteConfig, story, metadata, robots, WhatsApp y sitemap.

## Campos centralizados

- siteName;
- shortName;
- logo;
- colores;
- WhatsApp display;
- WhatsApp E.164;
- email;
- dirección;
- horarios;
- redes;
- base URL;
- moneda;
- copy institucional;
- SEO;
- coordenadas;
- analytics IDs;
- auth mode;
- storage mode.

## Contacto

Actualmente existen números diferentes. Unificar mediante configuración.

Para Wolfim usar:

`WhatsApp E.164: 5493513157202`

No hardcodearlo en múltiples componentes.

## Navbar

`app/layout.jsx` pasa props de contacto, pero `Navbar.jsx` no los recibe. Corregir para usar configuración central.

## Robots y sitemap

Eliminar dominio hardcodeado `https://vehicles-srs5.vercel.app` y usar `NEXT_PUBLIC_SITE_URL` o base URL configurada.

Actualizar rutas legacy `/vehicles` a `/autos` donde corresponda.

## Next config

Mantener `images.unoptimized = true`.

Auditar y remover, si no se usa, remote pattern `roggeroyroma.com.ar`. No eliminar dominios actuales sin comprobar uso.

## SiteConfig

Normalizar `customPropertyLabels` / `customVehicleLabels` a `customVehicleLabels`, migrando valores existentes.

Eliminar defaults inmobiliarios como `Vendemos Inmuebles` y `AMOBLADA` en flujos activos.

---

# 24. Cache y privacidad

Páginas privadas:

```js
export const dynamic = 'force-dynamic'
export const revalidate = 0
```

o equivalente.

- APIs privadas con `no-store` si corresponde.
- Después de logout, Back no debe permitir operar datos privados.
- No usar robots como seguridad real.
- No exponer datos privados en RSC, props serializadas ni caches compartidas.

---

# 25. Analytics y logs

No enviar a analytics:

- patente;
- VIN;
- motor;
- costos;
- margen;
- precio mínimo;
- notas;
- documentación;
- mantenimiento;
- responsable.

Si analytics global corre en toda la app, excluir `/admin`, `/superadmin` y `/messages`.

Eliminar logs que impriman email, token ID, user ID innecesario, rol o contenido interno.

Errores técnicos sin datos privados.

---

# 26. Limpieza de restos inmobiliarios

Buscar en archivos trackeados, excluyendo dependencias/build:

```text
Roggero
Roma
Property Pulse
property
properties
propiedad
propiedades
inmueble
inmobiliaria
AMOBLADA
/vehicles
```

Corregir obligatoriamente:

- textos visibles;
- rutas activas;
- metadata;
- README;
- PROJECT_CONTEXT;
- MANUAL_ADMIN;
- SiteConfig;
- labels;
- admin activo;
- comentarios engañosos;
- next config;
- robots;
- sitemap.

No borrar archivos legacy grandes sin verificar imports y uso. Si queda un artefacto no usado, documentar y confirmar que no se renderiza.

---

# 27. ESLint y calidad estática

Configurar ESLint no interactivo compatible con Next 14.2.4, por ejemplo:

- ESLint 8.x
- eslint-config-next 14.2.4
- `.eslintrc.json` extendiendo `next/core-web-vitals`

No resolver fallos con:

- `eslint-disable` masivo;
- `@ts-ignore`;
- `@ts-nocheck`;
- catch vacío;
- eliminación de tests.

Agregar scripts claros:

```json
{
  "lint": "next lint",
  "typecheck": "tsc --noEmit"
}
```

El typecheck actual no valida profundamente todo JS/JSX. Complementar con ESLint, Zod y tests.

---

# 28. Tests automatizados mínimos

Agregar tests para la frontera pública/privada. Vitest es aceptable si no existe framework.

Agregar `test: vitest run` o equivalente.

## Tests obligatorios

### publicVehicleDto

Dado un objeto con `owner`, `public_id`, `vin`, `licensePlate`, `purchaseCost`, `internalNotes` y `maintenanceHistory`, el DTO público no devuelve ninguno.

### publicSiteConfigDto

No devuelve `signatureBase64`, `exchangeRateARS` ni config privada.

### Validación interna

Probar:

- enums válidos/inválidos;
- números negativos;
- strings largos;
- fechas inválidas;
- claves desconocidas;
- costos/margen/precio;
- documentación;
- mantenimiento.

### Resúmenes

Probar:

- progreso checklist;
- documentación pendiente/vencida;
- días en stock;
- mantenimiento pendiente;
- costos.

No declarar “tests” si solo se ejecutó build.

---

# 29. QA técnico obligatorio

Ejecutar al final:

```bash
git diff --check
npm run lint
npm run typecheck
npm test
npm run build
```

Registrar comando, exit code, resultado y warnings. No afirmar que pasó si no se ejecutó.

---

# 30. QA anónima de seguridad

Usar sesión limpia sin cookies.

## Públicas esperadas

```text
GET / → 200
GET /autos → 200
GET /autos/[slug publicado] → 200
GET /api/story/[slug publicado] → 200 image/png
GET /sitemap.xml → 200
GET /robots.txt → 200
```

## Privadas sin sesión

```text
GET /admin → redirect a /login
GET /admin/internal-stock → redirect a /login
GET /admin/vehicles/[id]/edit → redirect a /login
GET /superadmin → bloqueo
GET /api/admin/vehicles → 401 JSON
GET /api/superadmin/export → 401 JSON
PATCH/POST internos → 401 JSON
```

No aceptar como prueba solamente que la UI oculta Admin. Probar URLs directas.

---

# 31. QA autenticada

Con credenciales fuera del repo:

1. Abrir `/login`.
2. Probar credenciales incorrectas.
3. Probar correctas.
4. Entrar a `/admin`.
5. Entrar a `/admin/internal-stock`.
6. Buscar por código.
7. Buscar por marca/modelo.
8. Buscar por patente.
9. Filtrar por estado.
10. Filtrar documentación incompleta.
11. Abrir ficha privada.
12. Editar ubicación.
13. Editar responsable.
14. Editar estado interno.
15. Editar costo.
16. Editar VIN.
17. Editar nota interna.
18. Actualizar documento.
19. Crear mantenimiento.
20. Editar mantenimiento.
21. Eliminar mantenimiento.
22. Cambiar checklist.
23. Editar campo público.
24. Verificar reflejo público.
25. Publicar/despublicar.
26. Confirmar que despublicado desaparece de público.
27. Cerrar sesión.
28. Reintentar ficha privada.
29. Confirmar bloqueo.

---

# 32. Prueba de no filtración

En un vehículo demo usar sentinel:

```text
VIN-DEMO-NO-PUBLICAR-001
PATENTE-DEMO-PRIVADA-001
NOTA-INTERNA-NO-PUBLICAR-001
COSTO-PRIVADO-123456
```

Con sesión anónima buscar valores en:

- HTML home;
- catálogo;
- ficha;
- RSC;
- respuestas de red;
- APIs públicas;
- JSON-LD;
- metadata;
- OpenGraph;
- sitemap;
- story;
- source.

Resultado esperado: cero coincidencias públicas.

No basta con que no aparezcan visualmente.

---

# 33. QA responsive

Verificar:

```text
1440x900   desktop
1024x1366  iPad Pro portrait
768x1024   iPad portrait
390x844    mobile
```

En cada viewport:

- login;
- dashboard;
- stock;
- filtros;
- tabla/cards;
- tabs;
- formularios;
- documentación;
- mantenimiento;
- checklist;
- botones;
- modales;
- scroll;
- fixed elements;
- overflow.

No depender de hover para acciones principales.

Capturas locales en `.qa-artifacts/`, ignoradas por git y con datos ficticios.

---

# 34. Regresión P0

No rediseñar P0.

## Home

- carga;
- hero/video;
- destacados;
- navegación;
- contacto.

## Catálogo

- carga;
- filtros;
- sorting;
- empty state;
- solo publicados;
- stock accesible.

Si existe límite de seis sin paginación/load-more y deja unidades inaccesibles, corregirlo mínimamente sin rediseñar.

## Ficha

- galería;
- precio;
- specs;
- WhatsApp;
- story;
- metadata;
- sin datos privados.

## WhatsApp

Mensaje con marca, modelo, versión y año. Usar número centralizado correcto.

## Historia

- 1080x1920;
- HTTP 200;
- image/png;
- legible;
- QR/link;
- descarga fallback;
- share sheet cuando corresponda.

---

# 35. P1+ permitido después del núcleo

Solo cuando P1 esté completo:

- badges de vencimientos;
- próximo vencimiento;
- ordenar por días en stock;
- costo total de preparación;
- CSV simple;
- historial básico de cambios;
- badges operativos.

No retrasar por esto auth, seguridad, persistencia, aislamiento, stock, ficha, documentación, mantenimiento o checklist.

---

# 36. Fuera de alcance

No implementar:

- multi-tenancy;
- billing;
- CRM completo;
- contabilidad;
- facturación;
- app nativa;
- MercadoLibre;
- GTM;
- publicación automática social;
- roles taller/vendedor avanzados;
- permisos por campo;
- firma digital;
- storage privado pago;
- reportes avanzados;
- alertas automáticas;
- importación masiva;
- OCR;
- documentos reales.

Documentar como P2.

---

# 37. Archivos esperados

La lista exacta puede variar, pero probablemente incluya:

## Seguridad

```text
components/AuthProvider.jsx
components/Navbar.jsx
utils/authOptions.js
utils/getSessionUser.js
utils/isAdmin.js
utils/requireAdmin.js
middleware.js
app/login/page.jsx
app/admin/layout.jsx
components/admin/AdminShell.jsx
app/superadmin/layout.jsx
```

## Modelos

```text
models/Vehicle.js
models/VehicleInternal.js
models/User.js
models/SiteConfig.js
```

## DTO y validación

```text
utils/publicVehicleDto.js
utils/publicSiteConfigDto.js
lib/validation/internalStock.js
lib/internalStock/constants.js
lib/internalStock/summaries.js
```

## Admin

```text
app/admin/page.jsx
app/admin/internal-stock/page.jsx
components/admin/InternalStockTable.jsx
components/admin/InternalStockFilters.jsx
components/admin/InternalStockCounters.jsx
app/admin/vehicles/page.jsx
components/admin/AdminVehicleTable.jsx
app/admin/vehicles/[id]/edit/page.jsx
components/admin/VehicleAdminTabs.jsx
components/admin/VehicleInternalForm.jsx
components/admin/DocumentationChecklist.jsx
components/admin/MaintenanceHistory.jsx
components/admin/PrePublishChecklist.jsx
```

## Acciones

```text
app/actions/addVehicle.js
app/actions/updateVehicle.js
app/actions/deleteVehicle.js
app/actions/updateVehiclePublic.js
app/actions/updateVehicleInternal.js
app/actions/updateDocumentationItem.js
app/actions/createMaintenanceEntry.js
app/actions/updateMaintenanceEntry.js
app/actions/deleteMaintenanceEntry.js
app/actions/updatePrePublishChecklist.js
```

## Público/API

```text
app/page.jsx
app/autos/page.jsx
app/autos/search-results/page.jsx
app/autos/[id]/page.jsx
app/autos/[id]/opengraph-image.jsx
app/api/story/[id]/route.jsx
components/StoryShareButton.jsx
app/sitemap.js
app/robots.js
app/layout.jsx
components/Footer.jsx
app/api/admin/vehicles/route.js
app/api/admin/toggle-featured/route.js
app/api/admin/toggle-published/route.js
app/api/site-config/route.js
app/api/site-config/site-config/route.js
app/api/superadmin/*
app/api/user/*
app/api/quotations/*
```

## Migración, calidad y docs

```text
scripts/migrate-internal-stock.mjs
scripts/seed-internal-demo.mjs
package.json
package-lock.json
.eslintrc.json
vitest.config.*
tests/*
.env.example
.gitignore
README.md
PROJECT_CONTEXT.md
MANUAL_ADMIN.md
next.config.mjs
```

---

# 38. Restricciones absolutas

- No crear otro clon.
- No rehacer showroom.
- No tocar producción Roggero.
- No usar datos/usuarios/documentos reales.
- No imprimir secretos.
- No commitear `.env.local`.
- No usar `deleteMany()` en migración P1.
- No publicar archivos privados en Cloudinary/Blob público.
- No esconder datos privados solo con CSS.
- No confiar solo en robots.
- No confiar solo en middleware.
- No enviar documentos Mongo completos a clientes públicos.
- No usar block-list como única protección.
- No dejar sesión demo.
- No dejar `matcher: []`.
- No permitir Server Actions anónimas por `next-action`.
- No hacer commit, push o deploy.
- No declarar LISTO sin pruebas reales.

---

# 39. Definition of Done

## Seguridad

- [ ] Sesión demo eliminada de AuthProvider.
- [ ] Bypass eliminado de getSessionUser.
- [ ] Middleware activo.
- [ ] Login real.
- [ ] Logout real.
- [ ] Admin anónimo bloqueado.
- [ ] APIs privadas bloqueadas.
- [ ] Server Actions privadas protegidas.
- [ ] Roles consistentes.
- [ ] Client no ve interno.
- [ ] Páginas privadas no-store.

## Datos

- [ ] Vehicle normalizado a `featured` + `published`.
- [ ] VehicleInternal separado.
- [ ] Relación uno-a-uno.
- [ ] Migración idempotente.
- [ ] Seed no destructivo.
- [ ] 12 vehículos preservados.
- [ ] 2 vehículos con datos internos ficticios completos.
- [ ] Delete cascade interno.

## Módulo interno

- [ ] Vista de stock.
- [ ] Búsqueda.
- [ ] Filtros.
- [ ] Contadores.
- [ ] Días en stock.
- [ ] Resumen documental.
- [ ] Resumen mantenimiento.
- [ ] Responsable.
- [ ] Ficha privada.
- [ ] Tab pública.
- [ ] Tab interno.
- [ ] Tab documentación.
- [ ] Tab mantenimiento.
- [ ] Tab checklist.
- [ ] CRUD mantenimiento.
- [ ] Estados documentales.
- [ ] Progreso checklist.
- [ ] Publicar/despublicar.

## Privacidad

- [ ] DTO público allow-list.
- [ ] DTO SiteConfig público.
- [ ] Owner no público.
- [ ] Cloudinary public_id no público.
- [ ] VIN no público.
- [ ] Patente no pública.
- [ ] Costos no públicos.
- [ ] Notas no públicas.
- [ ] Documentos no públicos.
- [ ] Mantenimiento no público.
- [ ] Checklist no público.
- [ ] Sitemap limpio.
- [ ] Metadata limpia.
- [ ] OpenGraph limpio.
- [ ] Story limpia.
- [ ] RSC limpio.
- [ ] Sentinel scan cero resultados.

## P0

- [ ] Home funciona.
- [ ] Catálogo funciona.
- [ ] Ficha funciona.
- [ ] WhatsApp funciona.
- [ ] Story 1080x1920 funciona.
- [ ] QR/link funciona.
- [ ] No rediseño.

## Clonabilidad

- [ ] Contacto/branding centralizados.
- [ ] WhatsApp unificado.
- [ ] Base URL/moneda/SEO configurables.
- [ ] Robots/sitemap configurables.
- [ ] Auth variables documentadas.
- [ ] Sin restos activos Roggero.
- [ ] README de clonado.
- [ ] DB/storage/users separados por concesionaria.

## Calidad

- [ ] `git diff --check` OK.
- [ ] `npm run lint` OK.
- [ ] `npm run typecheck` OK.
- [ ] `npm test` OK.
- [ ] `npm run build` OK.
- [ ] Desktop/iPad/mobile OK.
- [ ] Sin errores nuevos de consola.
- [ ] Sin 500 inesperados.
- [ ] No commit.
- [ ] No push.
- [ ] No deploy.

---

# 40. Salida requerida de Antigravity

No escribir dentro del vault de Obsidian.

Crear dentro del repo:

`docs/P1_INTERNAL_STOCK_IMPLEMENTATION.md`

El reporte y la respuesta final deben contener:

## Estado general

```text
P0 showroom: LISTO / PARCIAL / NO LISTO
P1 interno: LISTO / PARCIAL / NO LISTO
Aislamiento privado: VERIFICADO / NO VERIFICADO
Clonabilidad: LISTA / PARCIAL / NO LISTA
```

## Estado inicial

- ruta;
- rama;
- git status;
- preview;
- build inicial;
- lint inicial;
- typecheck inicial;
- problemas encontrados.

## Arquitectura final

- auth;
- modelos;
- VehicleInternal;
- DTO público;
- acciones;
- rutas;
- migración;
- rollback;
- cache;
- clonabilidad.

## Funcionalidades implementadas

- login/logout;
- stock/filtros;
- ficha;
- documentación;
- mantenimiento;
- checklist;
- publicación;
- seed;
- story.

## Seguridad

- rutas anónimas probadas;
- 401/403;
- datos sentinel;
- HTML;
- RSC;
- API;
- sitemap;
- metadata;
- OpenGraph;
- story.

## Validación técnica

Incluir output real resumido:

```text
git diff --check:
npm run lint:
npm run typecheck:
npm test:
npm run build:
```

## Browser QA

Para cada viewport:

```text
Ruta:
Acción:
Esperado:
Resultado:
Console:
```

## Migración

- dry run;
- backup;
- apply;
- cantidad vehículos;
- records internos;
- seed demo;
- rollback.

## Archivos tocados

Lista completa.

## Pendientes P2

Lista real, sin mezclar defectos P1.

## Bloqueos

Solo:

- credencial indispensable faltante;
- DB no identificable;
- storage pago;
- migración destructiva;
- deploy requerido;
- contradicción directa.

## Honestidad del reporte

Indicar explícitamente:

- qué quedó completo;
- qué quedó parcial;
- qué no pudo probarse;
- errores exactos;
- cualquier decisión pendiente de aprobación.

## Cierre

Terminar con un bloque listo para que web-builder/brain-local copie a `response.md` del handoff, sin secretos ni datos internos reales.
