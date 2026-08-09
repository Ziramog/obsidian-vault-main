---
company: Wolfim
project: wolfim-motors-demo
status: ready-for-antigravity
created: 2026-08-09
phase: fix-operational-inventory-after-review
execution-target: C:\Projects\wolfim-motors-demo
source-review: web-builder + independent subagent review
mode: demo-auth-preserved
---

# Prompt para Antigravity — Corrección de Inventario Operativo Wolfim Motors Demo

## Objetivo

Corregir la implementación actual del cockpit de inventario interno para que sea funcional, consistente y confiable como demo operativo, **sin tocar autenticación** y sin ampliar el alcance visual.

---

## Contexto del proyecto

Proyecto objetivo:

```text
C:\Projects\wolfim-motors-demo
```

Stack actual:

- Next.js 14.2.4 App Router
- React 18
- Tailwind CSS
- MongoDB / Mongoose
- NextAuth existente
- Cloudinary existente

Estado revisado:

- Rama observada: `main`
- Commit revisado: `a855e76`
- Commit base anterior: `32190aa`
- El proyecto debe permanecer en **modo demo**.

Importante:

- Juan ordenó explícitamente **no intervenir autenticación**.
- El acceso demo al backoffice **no es un bug**.
- No corregir, endurecer, reescribir ni cambiar auth en esta tarea.
- No tocar `middleware.js`, `utils/getSessionUser.js`, `utils/requireAdmin.js`, NextAuth providers/callbacks ni layout auth salvo que sea estrictamente necesario para no romper build, y en ese caso detenerse y reportar.

---

## Resultado esperado

Después de esta corrección, el demo debe permitir que una agencia responda rápido:

1. qué unidades requieren atención;
2. qué bloquea cada unidad;
3. quién es responsable;
4. cuál es la próxima acción;
5. qué unidades están listas para publicar;
6. qué stock envejeció;
7. qué capital/margen se muestra de forma financieramente segura;
8. qué unidades están visibles, ocultas o destacadas.

Pero esta tarea es de **estabilización**, no de rediseño grande.

---

## Restricciones obligatorias

### No tocar autenticación

No modificar:

- `middleware.js`
- `utils/getSessionUser.js`
- `utils/requireAdmin.js`
- configuración NextAuth
- providers NextAuth
- callbacks NextAuth
- política general de acceso demo

El modo demo abierto es una decisión de producto.

### No usar datos reales

No cargar ni generar:

- VIN reales;
- patentes reales;
- costos reales de clientes;
- documentación real;
- notas sensibles reales;
- datos de clientes reales.

Si se necesitan datos para demo, usar valores ficticios obvios.

### No operar producción

No hacer:

- deploy;
- push;
- merge;
- cambios en producción de Roggero;
- migraciones destructivas;
- `deleteMany()`;
- `git reset`;
- `git clean`;
- descarte de cambios locales.

No hacer commit ni push salvo autorización explícita de Juan.

### No reactivar upload documental público

Si la documentación no tiene storage privado verificado, mantener adjuntos reales deshabilitados. Es aceptable mostrar “No disponible” en demo. No subir documentos reales a Cloudinary público.

---

# Hallazgos a corregir

## P1 — El build ejecuta seed demo y modifica MongoDB

### Evidencia

Durante `npm run build`, el output mostró:

```text
Connected to MongoDB.
Vehicle 1 enriched.
Vehicle 2 enriched.
Vehicle 3 enriched.
Vehicle 4 enriched.
```

También aparece la ruta:

```text
○ /api/admin/seed-demo
```

Archivos relacionados:

- `app/api/admin/seed-demo/route.js`
- `scripts/seedDemoData.mjs`
- `scripts/seedDemoData.js` si existe localmente

### Impacto

Un build nunca debe modificar inventario ni tocar MongoDB con mutaciones de seed. Esto puede alterar datos demo o futuros datos reales accidentalmente.

### Tarea

1. Revisar `app/api/admin/seed-demo/route.js` y scripts de seed.
2. Eliminar cualquier efecto lateral al importar módulos.
3. Asegurar que el seed solo se ejecute por invocación manual explícita.
4. La ruta API, si se conserva, debe ser dinámica y no ejecutarse durante build.
5. Preferir que la lógica de seed esté en una función exportada pura y que solo se ejecute cuando se llama explícitamente desde CLI/API.
6. No ejecutar seed automáticamente en build, import, route evaluation o prerender.
7. Agregar una protección clara para demo si aplica, por ejemplo variable de entorno pública/privada de demo, pero sin tocar auth.
8. Mantener seed idempotente y no destructivo.

### Criterio de aceptación

Al ejecutar:

```bash
npm run build
```

no debe aparecer ningún mensaje tipo:

```text
Vehicle X enriched
Seed completed
Inserted
Updated
```

Y no debe haber mutaciones a MongoDB durante el build.

---

## P1 — “Gestión” y alta redirigen a una pestaña eliminada

### Evidencia

Enlaces actuales:

- `components/admin/InternalStockTable.jsx:333`
- `components/admin/InternalStockTable.jsx:469`
- `app/actions/addVehicle.js:75`

Usan:

```text
?tab=internal
```

Pero las pestañas actuales válidas son:

- `public`
- `summary`
- `operations`

Archivo relacionado:

- `components/admin/VehicleAdminTabs.jsx`

### Impacto

Al hacer clic en “Gestión” o al terminar un alta, la ficha abre con cabecera y tabs, pero sin contenido operativo visible.

### Tarea

1. Cambiar todos los enlaces internos de gestión a:

```text
?tab=operations
```

2. Cambiar la redirección posterior al alta para abrir la pestaña operativa correcta.
3. En `VehicleAdminTabs.jsx`, validar el tab recibido.
4. Si `tab` no es válido, usar fallback seguro:

```text
summary
```

o

```text
operations
```

según convenga para gestión interna.

5. Aceptar temporalmente `tab=internal` como alias hacia `operations` para no romper URLs anteriores.

### Criterio de aceptación

- Desde `/admin/internal-stock`, clic en “Gestión” abre ficha con contenido visible.
- `/admin/vehicles/[id]/edit?tab=internal` no queda vacío; debe redirigir o mapear a operaciones.
- Después de crear un vehículo, la pantalla no queda en tab vacío.

---

## P1 — Contrato incompatible de `technicalStatus`

### Evidencia

Archivos:

- `components/admin/VehicleInternalForm.jsx:64-67`
- `models/VehicleInternal.js:116-120`
- `app/actions/updateVehicleInternal.js:41-44`
- seeds demo

Problema detectado:

- El formulario envía valores como `ok` y `needs_review`.
- El schema admite valores como:
  - `not_inspected`
  - `diagnosis`
  - `waiting_quote`
  - `scheduled`
  - `in_workshop`
  - `ready`
  - `blocked`
- Los seeds usan `in_workshop`, `ready`, `not_inspected`.
- `findOneAndUpdate` no usa `runValidators`, por lo que pueden persistir valores fuera del schema.

### Impacto

La UI puede mostrar un estado distinto al persistido, o reemplazar estados válidos por valores inválidos al guardar.

### Tarea

1. Elegir un contrato canónico único para `technicalStatus`.
2. Recomiendo conservar los valores más operativos del schema:

```js
not_inspected
needs_review
diagnosis
waiting_quote
scheduled
in_workshop
ready
blocked
```

Si se usa `needs_review`, agregarlo explícitamente al schema.

3. Alinear:

- schema;
- seed;
- formulario;
- filtros;
- tabla;
- top cards;
- summary;
- server action.

4. Agregar `runValidators: true` en los updates Mongoose donde corresponda.
5. Normalizar datos heredados/idempotentes:

```text
ok -> ready
operational -> ready
needs_review -> needs_review
in_workshop -> in_workshop
blocked -> blocked
```

Ajustar mapping según valores reales encontrados en la DB, pero sin borrar registros.

### Criterio de aceptación

- El select muestra exactamente los valores admitidos por el schema.
- Guardar y refrescar conserva el mismo estado.
- No se persisten valores fuera del enum.
- Los seeds no generan estados que el formulario no pueda representar.

---

## P1 — Captura operativa incompleta o no persistente

### Evidencia

Archivos:

- `components/admin/VehicleInternalForm.jsx`
- `app/actions/updateVehicleInternal.js`
- `models/VehicleInternal.js`

Problemas:

- `blockedReason` aparece en formulario pero no se persiste.
- Campos que alimentan cockpit/KPIs no tienen controles claros o no se guardan:
  - `assignedSeller`
  - `priority`
  - `nextActionType`
  - `nextActionNote`
  - `nextActionAt`
  - `expenses`
  - `engineNumber`

### Impacto

El cockpit muestra métricas de atención, responsable, próxima acción y bloqueo, pero el usuario no puede administrar de forma confiable los datos que las alimentan.

### Tarea

Agregar o reparar captura y persistencia para:

#### Responsable

- Campo: `assignedSeller`
- En demo puede ser:
  - select con usuarios existentes si ya hay usuarios;
  - fallback textual seguro `assignedSellerName` solo si no hay usuarios.
- No implementar auth ni gestión de usuarios.

#### Prioridad

Campo sugerido:

```text
priority: low | normal | high | urgent
```

Debe poder editarse desde la ficha.

#### Próxima acción

Campos:

```text
nextActionType
nextActionNote
nextActionAt
```

Debe poder definirse desde la ficha operativa.

#### Motivo de bloqueo

Campo:

```text
blockedReason
```

Debe persistir.

#### Número de motor

Campo:

```text
engineNumber
```

Debe ser editable como dato demo/ficticio.

#### Gastos

Si ya existe `expenses`, permitir una captura mínima segura:

- concepto/categoría;
- monto;
- moneda;
- fecha;
- nota.

Si esto requiere demasiado cambio, dejar estructura preparada y no falsear métricas financieras.

### Criterio de aceptación

Para al menos un vehículo demo:

1. editar responsable/prioridad/próxima acción/motivo de bloqueo;
2. guardar;
3. refrescar;
4. verificar que los valores persisten en UI;
5. verificar que el inventario refleja esos valores.

---

## P1 — DTO parcialmente sin serializar

### Evidencia

Archivo:

- `app/admin/internal-stock/page.jsx`

Warnings observados:

```text
Only plain objects can be passed to Client Components from Server Components
```

Quedan ObjectIds/fechas/subdocumentos sin normalizar, por ejemplo:

- `vehicle.owner`
- `_id` de imágenes
- `updatedBy`
- `maintenanceHistory`
- subdocumentos internos

### Impacto

Next 14 puede advertir, fallar hidratación o romper render según datos presentes.

### Tarea

1. Crear un DTO explícito allowlist para `InternalStockTable`.
2. No pasar documentos Mongo completos al cliente.
3. Convertir todos los IDs a string.
4. Convertir fechas a ISO string.
5. Normalizar arrays anidados:
   - images;
   - documentationChecklist;
   - prePublishChecklist;
   - maintenanceHistory;
   - expenses.
6. Evitar exponer campos no necesarios.

### Criterio de aceptación

Al navegar a `/admin/internal-stock`, los logs del servidor no deben mostrar warnings de objetos no planos.

---

## P2 — Filtro “Requieren atención” se pierde al buscar

### Evidencia

Archivo:

- `app/admin/internal-stock/page.jsx:72-90`

Problema:

- `attention=true` define `matchStage.$or`.
- La búsqueda posterior redefine `matchStage.$or`.

### Impacto

Si el usuario entra desde “Requieren atención” y busca, puede ver unidades que no requieren atención.

### Tarea

Componer filtros con `$and`:

```js
const andConditions = [];

if (attention) {
  andConditions.push({ $or: [ ...condicionesAtencion ] });
}

if (q) {
  andConditions.push({ $or: [ ...condicionesBusqueda ] });
}

if (andConditions.length) {
  matchStage.$and = andConditions;
}
```

Mantener filtros simples como published/featured/bodyType/status en el mismo match.

### Criterio de aceptación

- `?attention=true&q=ferrari` solo muestra Ferraris que requieren atención.
- No mezcla resultados fuera del preset.

---

## P2 — Búsqueda usa regex sin escapar

### Evidencia

Archivo:

- `app/admin/internal-stock/page.jsx:82-89`

### Impacto

Entradas como:

```text
[
.
*
```

pueden alterar resultados o causar error MongoDB.

### Tarea

Escapar input antes de construir `$regex`:

```js
function escapeRegex(value) {
  return String(value).replace(new RegExp('[.*+?^${}()|\\[\\]\\\\]', 'g'), '\\$&');
}
```

Verificar la regex exacta en JS, porque el patrón anterior debe escribirse correctamente.

### Criterio de aceptación

Buscar `[` no rompe la página. Debe devolver cero resultados o resultados literales, no HTTP 500.

---

## P2 — Tarjetas superiores cuentan una cosa y enlazan otra

### Evidencia

Archivos:

- `app/admin/internal-stock/page.jsx:164-172`
- `components/admin/StockTopCards.jsx:18-31`

Problema:

- “En proceso” cuenta `in_preparation + to_review`, pero enlaza solo `in_preparation`.
- “Listos” cuenta `ready_to_publish + published`, pero enlaza solo `ready_to_publish`.

### Impacto

El usuario ve un número y al hacer clic recibe una cantidad menor o distinta.

### Tarea

Elegir una de estas dos soluciones:

#### Opción recomendada

Hacer que cada tarjeta abra un preset explícito:

```text
?preset=attention
?preset=in_process
?preset=ready
```

Y que el backend traduzca cada preset a sus condiciones reales.

#### Opción mínima

Cambiar los conteos para que coincidan exactamente con el filtro linkeado.

### Criterio de aceptación

El número visible en cada tarjeta coincide con el listado que abre.

---

## P2 — Dashboard principal conserva contratos obsoletos

### Evidencia

Archivos:

- `app/admin/page.jsx:33,70-71`
- `app/admin/internal-stock/page.jsx:23-25,65-68`
- `components/admin/StockFilters.jsx`

Problemas:

- Dashboard usa `is_featured` aunque el modelo usa `featured`.
- Links generan query params como:
  - `status=active`
  - `is_featured=true`
- Inventario espera:
  - `published=yes|no`
  - `featured=yes|no`

Además, `StockFilters.jsx` recibe `currentFeatured` pero no ofrece control para modificarlo.

### Tarea

1. Alinear dashboard con el contrato nuevo:

```text
published=yes|no
featured=yes|no
```

2. Usar `featured`, no `is_featured`.
3. Agregar filtro visual para destacados si el parámetro existe.
4. Si se conservan aliases viejos, mapearlos explícitamente y limpiar URL en navegación.

### Criterio de aceptación

- Click en tarjeta de publicados/visibles filtra correctamente.
- Click en destacados filtra correctamente.
- No quedan referencias funcionales a `is_featured` o `is_published` para el inventario nuevo.

---

## P2 — Métrica financiera mezcla monedas

### Evidencia

Archivo:

- `components/admin/VehicleSummaryTab.jsx`

Problema:

`purchaseCost` se suma con gastos de moneda propia y se muestra usando una sola moneda.

Ejemplo incorrecto:

```text
USD 15.000 + ARS 100.000 = USD 115.000
```

### Impacto

La métrica “Invertido” no es confiable.

### Tarea

Elegir solución segura:

#### Opción recomendada para demo

Mostrar inversión separada por moneda:

```text
Invertido USD: ...
Invertido ARS: ...
```

No convertir moneda si no hay tipo de cambio confiable.

#### Opción alternativa

Si hay conversión, debe ser explícita y mostrar tipo de cambio usado. No inventarlo.

### Criterio de aceptación

No se suman monedas distintas en un único total engañoso.

---

## P2 — Seed guarda margen inválido

### Evidencia

Archivos:

- `app/api/admin/seed-demo/route.js:103-106`
- `scripts/seedDemoData.mjs:104-107`
- `components/admin/VehicleInternalForm.jsx:128-129`

Problema:

El seed guarda:

```text
targetMargin: 5000
```

pero el formulario lo define como porcentaje con máximo 100.

### Tarea

1. Definir si `targetMargin` es porcentaje o monto.
2. Para esta etapa, recomiendo porcentaje:

```text
0 a 100
```

3. Ajustar seed a valores válidos, por ejemplo:

```text
12
15
18
```

4. Si se necesita margen en dinero, crear otro campo futuro y no mezclar semánticas.

### Criterio de aceptación

Los valores demo no bloquean validación HTML ni contradicen el label del formulario.

---

## P2 — Lint no funciona como quality gate

### Evidencia

`npm run lint` abre configuración interactiva o no está configurado para CI.

### Tarea

1. Configurar ESLint mínimo para Next.js si no existe.
2. Evitar prompts interactivos en CI/local.
3. Si hay muchos errores heredados, documentar baseline y no mezclar con esta corrección.
4. Al menos dejar `npm run lint` ejecutable de forma no interactiva.

### Criterio de aceptación

```bash
npm run lint
```

termina con exit code determinístico y sin asistente interactivo.

---

# Archivos probablemente a tocar

Prioritarios:

```text
app/api/admin/seed-demo/route.js
scripts/seedDemoData.mjs
scripts/seedDemoData.js
components/admin/InternalStockTable.jsx
components/admin/VehicleAdminTabs.jsx
components/admin/VehicleInternalForm.jsx
components/admin/VehicleSummaryTab.jsx
components/admin/StockTopCards.jsx
components/admin/StockFilters.jsx
app/admin/internal-stock/page.jsx
app/admin/page.jsx
app/actions/addVehicle.js
app/actions/updateVehicleInternal.js
models/VehicleInternal.js
```

Solo si hace falta para lint:

```text
.eslintrc.json
eslint.config.js
package.json
```

No tocar auth:

```text
middleware.js
utils/getSessionUser.js
utils/requireAdmin.js
app/api/auth/[...nextauth]/route.js
```

---

# QA obligatorio

Ejecutar y reportar output real:

```bash
git status --short
git diff --check
npm run lint
npx tsc --noEmit
npm run build
npm test
```

Si `npm test` no existe, reportar:

```text
npm test: no existe script de test
```

No inventar resultado.

## QA browser obligatorio

Levantar servidor limpio:

1. Detener procesos Next viejos en puerto 3000.
2. Ejecutar build limpio.
3. Ejecutar:

```bash
npm run start
```

4. Verificar que CSS devuelve HTTP 200.
5. Probar:

```text
/admin/internal-stock
/admin/internal-stock?attention=true
/admin/internal-stock?attention=true&q=ferrari
/admin/internal-stock?view=internal
/admin/internal-stock?view=interno
/admin/internal-stock?view=showroom
/admin/vehicles/[id]/edit?tab=internal
/admin/vehicles/[id]/edit?tab=operations
```

## QA funcional obligatorio

En un vehículo demo:

1. Entrar desde botón “Gestión”.
2. Confirmar que abre contenido operativo, no tab vacío.
3. Editar:
   - estado técnico;
   - ubicación;
   - prioridad;
   - responsable o responsable demo;
   - próxima acción;
   - motivo de bloqueo;
   - fecha de próxima acción.
4. Guardar.
5. Refrescar.
6. Confirmar persistencia visual.
7. Confirmar que el inventario refleja los cambios.
8. Confirmar que la tarjeta “Requieren atención” abre un listado consistente.

## QA de build side effects

Antes y después de `npm run build`, verificar que no se ejecutó seed.

Como mínimo, el output de build no debe mostrar mutaciones. Si se puede, agregar una verificación de conteo o timestamp sin imprimir secretos.

---

# Criterios finales de aceptación

La corrección se considera lista si:

- `npm run build` pasa sin ejecutar seed ni mutar DB.
- `npx tsc --noEmit` pasa.
- `npm run lint` queda configurado o se reporta claramente si hay baseline heredado.
- El botón “Gestión” no abre tab vacío.
- El alta no redirige a tab vacío.
- `tab=internal` tiene fallback seguro.
- `view=internal` y/o `view=interno` no dejan listado vacío.
- `technicalStatus` tiene contrato único entre schema, seed, form y action.
- `blockedReason` se persiste.
- Responsable/prioridad/próxima acción son editables o se documenta explícitamente si alguno queda fuera, con razón técnica.
- Los DTOs enviados a componentes cliente son plain objects sin warnings de Mongoose/ObjectId.
- Atención + búsqueda se combinan correctamente.
- La búsqueda escapa regex.
- Top cards muestran conteos que coinciden con lo que abren.
- Dashboard usa `published`/`featured`, no contratos obsoletos.
- La métrica financiera no mezcla monedas.
- No se tocó autenticación.
- No se reactivó upload público de documentación.
- No hubo commit/push/deploy sin autorización.

---

# Output esperado de Antigravity

Al terminar, devolver un resumen con este formato:

```markdown
## Resumen de corrección

### Cambios realizados
- ...

### Archivos modificados
- ...

### Verificaciones ejecutadas
| Comando | Resultado |
|---|---|
| git diff --check | ... |
| npm run lint | ... |
| npx tsc --noEmit | ... |
| npm run build | ... |
| npm test | ... |

### QA browser
- /admin/internal-stock: ...
- Gestión desde inventario: ...
- tab=internal fallback: ...
- view internal/interno/showroom: ...
- save → refresh: ...

### Decisiones respetadas
- Auth demo preservada: sí/no
- Upload documental público no reactivado: sí/no
- Sin commit/push/deploy: sí/no

### Riesgos restantes
- ...
```

---

## Nota final

Esta tarea es una estabilización de la entrega de Antigravity. No rediseñar el showroom público, no convertirlo en CRM completo y no resolver autenticación todavía. El objetivo es que el demo operativo sea coherente, confiable y útil para mostrar a una agencia sin cargar datos reales.
