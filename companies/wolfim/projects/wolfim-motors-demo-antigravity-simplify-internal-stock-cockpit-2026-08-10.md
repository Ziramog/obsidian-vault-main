---
company: Wolfim
project: wolfim-motors-demo
status: ready-for-antigravity
created: 2026-08-10
phase: internal-stock-ux-correction
execution-target: Antigravity
source: Juan review + screenshot composer_2026-08-10_00-54-37-004_a23146.png
repo: C:\Projects\wolfim-motors-demo
branch-observed: main
last-observed-commit: 88bc957 fix(ui): resolve operational state contradictions in internal stock cockpit
---

# Wolfim Motors Demo — Simplificar cockpit de inventario interno

## Objetivo

Reordenar el listado interno de inventario para que sea **simple, operable y entendible por una persona externa**, separando claramente acciones directas y estado operativo.

El listado actual quedó técnicamente más correcto, pero visualmente demasiado confuso. Hay que simplificarlo.

Principio guía:

> El listado no debe explicar la base de datos. El listado debe responder rápido: está publicado, está destacado, en qué estado está, qué falta, quién lo tiene que mover y dónde entro a gestionarlo.

---

## Contexto del proyecto

Repo:

```text
C:\Projects\wolfim-motors-demo
```

Stack:

- Next.js 14.2.4 App Router
- React 18
- MongoDB / Mongoose
- Tailwind
- Modo demo deliberado

Rutas relevantes:

```text
/admin/internal-stock?view=internal
/admin/internal-stock?view=showroom
/admin/vehicles/[id]/edit?tab=operations
```

Últimos commits relevantes observados:

```text
88bc957 fix(ui): resolve operational state contradictions in internal stock cockpit
a2fef3b feat: add publish gate modal
8cef68f refactor: separate documentation and pre-publish checklist concepts
```

Importante:

- No tocar autenticación.
- No tocar middleware.
- No tocar NextAuth.
- No tocar permisos.
- No tocar showroom público salvo que sea estrictamente necesario.
- Mantener modo demo.

---

## Problema actual

La tabla interna actualmente muestra una columna:

```text
Estado & Origen
```

Y dentro puede aparecer algo como:

```text
EN PREP.
Acción vencida: workshop
Web: Visible con pendientes
Compra
```

Esto es inentendible para un usuario real.

Ahí están mezclados cuatro conceptos distintos:

1. Estado operativo interno.
2. Motivo de atención / pendiente.
3. Visibilidad pública en web.
4. Origen del stock.

Además, el texto muestra enums crudos como:

```text
workshop
```

Eso no debe aparecer en UI final.

---

## Diagnóstico de UX

### Lo que está mal

1. **`Estado & Origen` no debe existir como columna combinada.**
2. **`Web: Visible con pendientes` no debe mostrarse como frase larga dentro del estado.**
3. **`Acción vencida: workshop` muestra un enum técnico y no lenguaje humano.**
4. **Publicado y destacado no están suficientemente claros en el listado interno.**
5. **La operación principal debería estar disponible desde el listado interno:** publicar/ocultar y destacar/quitar destacado.
6. **Origen no merece estar mezclado con estado; debe ser un subdato del vehículo.**
7. **El listado se volvió explicativo en vez de operativo.**

---

## Resultado esperado

La tabla desktop debe tender a esta estructura:

```text
Vehículo | Web | Destacado | Estado | Pendientes | Legajo | Taller | Precio / Stock | Responsable | Acciones
```

No hace falta que sea exactamente este layout si hay limitaciones responsive, pero sí debe respetar esta separación conceptual.

Ejemplo deseado:

```text
Ferrari SF90 Spider
WM-3024 · Compra

Web: 👁 visible ⚠
Destacado: ☆
Estado: En preparación
Pendientes: Taller vencido
Legajo: 7/7
Taller: Sin registros
Precio: USD 15.000 · 61 días
Responsable: Demo Responsable QA
Acciones: Gestión
```

Ejemplo para unidad oculta:

```text
Mercedes-Benz G-Class AMG G 63
WM-1125 · S/D

Web: 👁 oculto
Destacado: ☆
Estado: Listo para publicar
Pendientes: Sin pendientes críticos
Legajo: No iniciado
Taller: Sin registros
Precio: USD 20.000 · 30 días
Responsable: Sin asignar
Acciones: Gestión
```

---

## Tarea específica

## 1. Eliminar la columna `Estado & Origen`

En:

```text
components/admin/InternalStockTable.jsx
```

Reemplazar la columna actual:

```text
Estado & Origen
```

por columnas/conceptos separados.

La columna no debe volver a mezclar:

```text
estado + atención + web + origen
```

---

## 2. Mover `Origen` debajo del vehículo

En la celda `Vehículo`, mostrar:

```text
Marca Modelo
Código interno · Origen
Patente si existe
```

Ejemplo:

```text
Ferrari SF90 Spider
WM-3024 · Compra
S/P
```

Mapeo de origen:

```js
purchase -> Compra
trade_in -> Permuta
consignment -> Consignación
other -> Otro
undefined/null -> S/D
```

Origen no debe aparecer dentro de Estado.

---

## 3. Crear columna `Web` con ojito clickeable

Agregar columna clara:

```text
Web
```

Debe mostrar un botón con ícono:

- `Eye` para visible.
- `EyeOff` para oculto.

Usar `lucide-react`, ya importado en el proyecto.

Estados visuales sugeridos:

```text
visible: verde
oculto: gris/rojo suave
visible con pendientes: amarillo con pequeño indicador ⚠
```

Pero no mostrar frases largas como:

```text
Web: Visible con pendientes
```

Preferir:

```text
Visible
Visible ⚠
Oculto
```

O simplemente ícono + label corto.

### Comportamiento obligatorio

Debe reutilizar la lógica existente:

- Si está oculto y se intenta publicar → abrir `PublishGateModal`.
- Si está visible y se intenta ocultar → confirmación simple.

No romper:

```text
components/admin/PublishGateModal.jsx
/api/admin/toggle-published
```

No duplicar endpoint.

---

## 4. Crear columna `Destacado` con estrella clickeable

Agregar columna clara:

```text
Destacado
```

Debe mostrar un botón con `Star`:

- estrella activa si `v.featured === true`;
- estrella inactiva si no está destacado.

Click debe usar la lógica existente:

```js
handleToggleFeatured(id)
```

Si hoy solo se puede destacar desde otra vista, llevarlo también al listado interno.

Estados visuales sugeridos:

```text
featured: estrella amarilla/azul activa
not featured: estrella gris
```

No usar texto largo.

---

## 5. Dejar `Estado` solo para estado operativo

Crear o mantener columna:

```text
Estado
```

Debe mostrar únicamente:

```js
internal.internalStatus
```

con label humano.

Mapeo sugerido:

```js
to_review -> A revisar
in_preparation -> En preparación
ready_to_publish -> Listo para publicar
published -> Publicado operativo
reserved -> Reservado
sold -> Vendido
delivered -> Entregado
```

Nota importante:

- Si es posible, evitar que `published` operativo se confunda con visibilidad web.
- Si se mantiene, mostrarlo como `Publicado operativo` o `En showroom`, pero no simplemente `Publicado` si al lado existe columna Web.

---

## 6. Crear columna `Pendientes`

Crear columna:

```text
Pendientes
```

Debe mostrar el motivo principal de atención en lenguaje humano.

No usar enums crudos.

Reglas sugeridas:

```js
if technicalStatus === 'blocked':
  Bloqueado
  o Bloqueado: [blockedReason corto]

else if priority === 'urgent':
  Prioridad urgente

else if nextActionAt vencida:
  [nextActionType traducido] vencido

else if published visible pero estado operativo no listo:
  Publicado con pendientes

else:
  Sin pendientes
```

Traducción de `nextActionType`:

```js
documentation -> Documentación
workshop -> Taller
content -> Contenido
cleaning -> Limpieza
pricing -> Precio
contact -> Contacto
review -> Revisión
other -> Otra acción
undefined/null -> Acción
```

Ejemplos correctos:

```text
Taller vencido
Documentación vencida
Prioridad urgente
Bloqueado: falta repuesto
Publicado con pendientes
Sin pendientes
```

Ejemplos incorrectos:

```text
Acción vencida: workshop
nextActionAt expired
Web: Visible con pendientes
```

---

## 7. Mantener `Legajo` simple

Columna:

```text
Legajo
```

Reglas:

```js
if docTotal === 0:
  No iniciado
else:
  X/Y
```

Color sugerido:

- verde si completo;
- amarillo si parcial;
- gris si no iniciado;
- rojo si faltan documentos críticos.

No mostrar:

```text
0 de 0 listos
```

---

## 8. Mantener `Taller` simple

Columna:

```text
Taller
```

Reglas:

```js
if maintenanceHistory.length === 0:
  Sin registros
else if pending/in_progress > 0:
  X pendientes
else:
  Al día
```

No mezclar taller con preparación comercial en la misma columna.

---

## 9. Revisar cards superiores

Cards actuales:

```text
Alertas Operativas
En Preparación
Visibles en Web
```

Simplificar labels si mejora legibilidad:

Opción recomendada:

```text
Alertas
Preparación
Showroom visible
```

Lógica:

### Alertas

Cuenta:

```js
technicalStatus === 'blocked'
priority === 'urgent'
nextActionAt vencida
```

### Preparación

Cuenta:

```js
internalStatus in ['to_review', 'in_preparation', 'reserved']
```

### Showroom visible

Cuenta:

```js
published !== false
```

---

## 10. Vista mobile

No dejar mobile como versión vieja.

La card mobile debe mostrar la misma jerarquía simple:

```text
Vehículo
Código · Origen

Web [ojo]
Destacado [estrella]
Estado
Pendientes
Legajo
Taller
Precio / Stock
Responsable
Gestión
```

No meter `Estado y Origen` como bloque combinado en mobile.

---

## 11. Vista showroom

En:

```text
/admin/internal-stock?view=showroom
```

Mantener cards actuales de showroom, pero verificar:

- botón visible/oculto sigue funcionando;
- oculto → abre modal de publicación;
- visible → confirmación simple para ocultar;
- destacado sigue siendo claro si aparece en card.

Si se agrega estrella en la vista interna, no hace falta cambiar showroom salvo bug.

---

## Archivos probablemente a tocar

```text
components/admin/InternalStockTable.jsx
components/admin/StockTopCards.jsx
components/admin/StockFilters.jsx
app/admin/internal-stock/page.jsx
```

Revisar si aplica:

```text
components/admin/PublishGateModal.jsx
models/VehicleInternal.js
```

No tocar salvo necesidad real:

```text
middleware.js
utils/requireAdmin.js
app/api/auth/*
components/AuthProvider.jsx
```

---

## Restricciones

- No tocar auth.
- No tocar middleware.
- No tocar permisos.
- No cambiar modo demo.
- No hacer deploy.
- No borrar datos.
- No migraciones destructivas.
- No tocar `.env.local`.
- No imprimir secrets.
- No rediseñar showroom público.
- No cambiar estructura de base de datos salvo necesidad mínima justificada.
- No hacer commit/push sin autorización explícita.

---

## Criterios de aceptación

En:

```text
/admin/internal-stock?view=internal
```

Debe quedar claro a simple vista:

1. Si la unidad está publicada/visible en web.
2. Si está destacada.
3. Cuál es su estado operativo.
4. Qué pendiente principal tiene, si existe.
5. Qué origen tiene, sin mezclarlo con estado.
6. Cómo está el legajo.
7. Cómo está taller.
8. Quién es responsable.
9. Dónde entrar a gestión.

La tabla no debe mostrar frases mezcladas como:

```text
EN PREP.
Acción vencida: workshop
Web: Visible con pendientes
Compra
```

Debe verse más parecido a:

```text
Vehículo: Ferrari SF90 Spider / WM-3024 · Compra
Web: 👁 Visible ⚠
Destacado: ☆
Estado: En preparación
Pendientes: Taller vencido
Legajo: 7/7
Taller: Sin registros
Precio: USD 15.000 · 61 días
Responsable: Demo Responsable QA
Acciones: Gestión
```

---

## Validaciones técnicas obligatorias

Ejecutar:

```bash
git diff --check
npx tsc --noEmit
npm run lint
npm run build
```

Si existe:

```bash
npm test
```

Si no existe, reportar:

```text
npm test no disponible: missing script
```

---

## Browser QA obligatorio

Levantar server:

```bash
npm run start
```

Probar:

```text
/admin/internal-stock?view=internal
/admin/internal-stock?view=showroom
/admin/internal-stock?view=internal&preset=attention
/admin/internal-stock?view=internal&preset=preparation
/admin/internal-stock?view=internal&published=yes
```

Confirmar:

- La tabla interna no usa `Estado & Origen`.
- Hay columna o control claro para `Web` con ojito.
- Hay columna o control claro para `Destacado` con estrella.
- Publicar desde ojito abre `PublishGateModal`.
- Ocultar desde ojito pide confirmación simple.
- Destacar/quitar destacado funciona y persiste visualmente.
- `workshop` no aparece crudo en UI.
- `documentation`, `content`, `cleaning`, `pricing`, etc. no aparecen crudos en UI.
- `0 de 0 listos` no aparece.
- Mobile no conserva el bloque `Estado y Origen` combinado.
- Consola browser sin errores JS.

---

## Resultado esperado final

Un cockpit simple y completo:

```text
Alertas | Preparación | Showroom visible

Vehículo | Web | Destacado | Estado | Pendientes | Legajo | Taller | Precio / Stock | Responsable | Acciones
```

El usuario debe entender la lógica sin conocer los campos internos de MongoDB.

El criterio final es de claridad:

> Si Juan no entiende el listado en 10 segundos, un usuario externo tampoco lo va a entender.
