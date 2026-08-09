---
company: Wolfim
project: wolfim-motors-demo
status: ready-for-antigravity
created: 2026-08-09
phase: final-stabilization-after-antigravity-audit
execution-target: C:\Projects\wolfim-motors-demo
current-commit-reviewed: 0e1ba25
previous-commit: a855e76
reviewer: web-builder
mode: prompt-for-antigravity
priority: P1
---

# Prompt para Antigravity — Wolfim Motors Demo

## Objetivo

Cerrar la estabilización final del cockpit operativo de inventario interno, corrigiendo bugs de contratos, URL state, lint y repo hygiene detectados en la auditoría posterior al commit `0e1ba25`, sin ampliar alcance visual y sin tocar autenticación.

---

## Contexto del proyecto

Proyecto local:

```text
C:\Projects\wolfim-motors-demo
```

Stack observado:

- Next.js 14.2.4 App Router
- React 18
- Tailwind CSS
- MongoDB / Mongoose
- NextAuth existente
- Cloudinary existente

Commits relevantes:

```text
0e1ba25 fix: top cards and filters matching operational reality
 a855e76 feat: complete operational cockpit redesign and phase 4 of internal UI evolution
 32190aa feat: add descriptions to PrePublishChecklist items
```

Scripts actuales:

```json
{
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
}
```

---

## Restricciones absolutas

### No tocar autenticación

El proyecto debe seguir en **modo demo** por decisión explícita del dueño.

No modificar:

- `utils/getSessionUser.js`
- `utils/requireAdmin.js`
- `middleware.js`
- providers/callbacks de NextAuth
- lógica de acceso demo
- sesión demo

No reportar ni corregir el acceso abierto como bug.

Sí mantener advertencia conceptual: mientras siga demo, no usar datos reales.

### No ampliar alcance

No hacer:

- rediseño visual general;
- refactor masivo;
- CRM;
- leads pipeline;
- multitenancy;
- auth real;
- storage privado de documentos;
- deploy;
- cambios en producción.

### No tocar secretos

No leer, imprimir ni exponer `.env`, `.env.local`, tokens, URIs ni claves.

Si necesitás referenciar variables:

```text
[credencial: NOMBRE_VARIABLE]
```

### No operaciones destructivas

No ejecutar:

- `git reset`
- `git clean`
- `git checkout` para descartar cambios
- `pull` destructivo
- `force push`
- migraciones destructivas
- `deleteMany()` sobre vehículos demo

No hacer commit ni push salvo autorización explícita de Juan.

---

## Estado de auditoría actual

### Validaciones que pasan

- `npm run build`: PASS.
- `npx tsc --noEmit`: PASS.
- `/admin/internal-stock`: carga en navegador.
- CSS productivo servido correctamente.
- Botón `Gestión`: ahora abre `?tab=operations`.
- `?tab=internal`: ahora renderiza operaciones como alias.
- `q=[`: ya no rompe la página.
- Browser console en QA revisada: sin errores.

### Validaciones que fallan

- `npm run lint`: FAIL.

Salida observada:

```text
ESLint must be installed: npm install --save-dev eslint
```

- `npm test`: FAIL porque no existe script `test`.
- `?view=internal`: HTTP 200 pero pantalla queda sin tabla/listado.
- Contratos de `technicalStatus` y `nextActionType` siguen inconsistentes entre form/schema/action.
- Responsable operativo mostrado como nombre no se persiste realmente.
- `.hermes/desktop-attachments/chatgpt_prompt_filters.md` quedó dentro del repo.

---

# Tareas obligatorias

## 1. Arreglar contrato `technicalStatus`

### Problema

En `components/admin/VehicleInternalForm.jsx`, el formulario permite:

```text
needs_review
```

Pero en `models/VehicleInternal.js`, el enum actual observado es:

```js
['not_inspected', 'diagnosis', 'waiting_quote', 'scheduled', 'in_workshop', 'ready', 'blocked']
```

No incluye `needs_review`.

Como `updateVehicleInternal.js` ahora usa:

```js
runValidators: true
```

seleccionar “Requiere Revisión” puede hacer fallar el guardado.

### Corrección requerida

Definir un contrato único y usarlo igual en:

- `models/VehicleInternal.js`
- `components/admin/VehicleInternalForm.jsx`
- `app/actions/updateVehicleInternal.js`
- cualquier filtro, label o resumen que muestre estado técnico
- seeds/demo enrichment

Contrato recomendado:

```js
const TECHNICAL_STATUS_OPTIONS = [
  'not_inspected',
  'needs_review',
  'diagnosis',
  'waiting_quote',
  'scheduled',
  'in_workshop',
  'ready',
  'blocked'
];
```

Labels sugeridos:

```text
not_inspected  → No inspeccionado
needs_review   → Requiere revisión
diagnosis      → En diagnóstico
waiting_quote  → Esperando presupuesto
scheduled      → Turno asignado
in_workshop    → En taller
ready          → Listo operativo
blocked        → Bloqueado
```

### Requisitos

- Si se conserva `needs_review` en UI, debe existir en schema.
- Si se elimina de UI, no debe aparecer en ningún select ni seed.
- Preferencia: **agregar `needs_review` al schema** porque es útil operativamente.
- Mantener `runValidators: true`.
- No guardar strings vacíos para enum.
- Si el form recibe vacío, usar default válido o `$unset` según corresponda.

### Criterio de aceptación

- Seleccionar “Requiere revisión” y guardar no rompe.
- Refrescar ficha conserva el valor.
- `npx tsc --noEmit` pasa.
- `npm run build` pasa.

---

## 2. Arreglar contrato `nextActionType`

### Problema

En `components/admin/VehicleInternalForm.jsx`, el formulario ofrece:

```text
cleaning
```

Pero en `models/VehicleInternal.js`, el enum observado es:

```js
['documentation', 'workshop', 'photos', 'pricing', 'content', 'contact', 'review', 'other']
```

No incluye `cleaning`.

Además el formulario puede enviar:

```text
nextActionType = ''
```

y el action lo intenta persistir como string vacío.

Con validators activos, esto puede fallar.

### Corrección requerida

Unificar contrato en schema, form y seeds.

Contrato recomendado:

```js
const NEXT_ACTION_TYPES = [
  'documentation',
  'workshop',
  'content',
  'cleaning',
  'pricing',
  'contact',
  'review',
  'other'
];
```

Labels sugeridos:

```text
documentation → Documentación / gestoría
workshop      → Taller / repuestos
content       → Fotos / video
cleaning      → Limpieza / detailing
pricing       → Precio / publicación
contact       → Contactar tercero
review        → Revisión interna
other         → Otro
```

### Requisitos

- Agregar `cleaning` al schema si sigue en UI.
- No mezclar `photos` y `content` para el mismo concepto salvo que ambos tengan sentido y estén documentados.
- Recomendación: usar `content` para “Fotos / Video” y no usar `photos` en UI.
- Cuando no haya próxima acción, no guardar `''`.
- Si el select queda en “Seleccionar...”, usar `$unset: { nextActionType: 1 }` o no setear el campo.

### Criterio de aceptación

- Elegir “Limpieza / Detailing” y guardar no falla.
- Dejar “Seleccionar...” y guardar no falla.
- Refrescar conserva correctamente el estado.
- No hay enum validation errors.

---

## 3. Resolver responsable operativo sin tocar auth

### Problema

La UI muestra:

```text
Vendedor Asignado (Nombre)
```

El input usa:

```text
assignedSellerName
```

Pero `VehicleInternal` no tiene ese campo en el schema.

Resultado probable:

- Mongoose lo ignora por strict mode;
- la UI promete un responsable que no se persiste;
- al guardar, el action puede borrar `assignedSeller` porque el form no envía `assignedSeller`.

Fragmento observado en `updateVehicleInternal.js`:

```js
const assignedSeller = formData.get('assignedSeller');
if (assignedSeller && assignedSeller !== '') {
  data.assignedSeller = assignedSeller;
} else {
  data.$unset = { ...data.$unset, assignedSeller: 1 };
}
```

Pero el formulario visible no controla `assignedSeller`; controla `assignedSellerName`.

### Corrección requerida

Como el proyecto sigue en demo y no se debe tocar auth/user management, usar responsable por nombre simple.

Agregar a `models/VehicleInternal.js`:

```js
assignedSellerName: {
  type: String,
  trim: true,
  maxLength: 120
}
```

Actualizar:

- `components/admin/VehicleInternalForm.jsx`
- `app/actions/updateVehicleInternal.js`
- `components/admin/InternalStockTable.jsx`
- `components/admin/VehicleSummaryTab.jsx` si muestra responsable
- grouping por responsable
- filtros/cards si usan responsable

### Requisitos

- `assignedSellerName` debe persistir.
- No borrar `assignedSeller` si el formulario no lo controla.
- Mantener `assignedSeller` como campo futuro opcional, pero no tocar auth ni usuarios.
- Si hay `assignedSellerName`, mostrarlo en la tabla en lugar de “Sin asignar”.
- Si no hay responsable, mostrar “Sin asignar”.
- Grouping por responsable debe usar `assignedSellerName || 'Sin asignar'`.

### Criterio de aceptación

Flujo obligatorio:

1. Abrir una unidad.
2. Escribir un nombre en “Vendedor Asignado”.
3. Guardar.
4. Refrescar.
5. Confirmar que el nombre sigue visible.
6. Volver a `/admin/internal-stock`.
7. Confirmar que la tabla muestra el nombre.
8. Probar agrupación por responsable.

---

## 4. Normalizar `view=internal`

### Problema

La URL:

```text
/admin/internal-stock?view=internal
```

devuelve HTTP 200 pero queda sin tabla/listado.

La implementación todavía usa internamente:

```text
interno
```

El prompt original pedía contrato en inglés / URL estable:

```text
internal
showroom
```

### Corrección requerida

Usar como contrato canónico:

```text
view=internal
view=showroom
```

Aceptar alias legacy:

```text
view=interno → internal
```

### Requisitos

Actualizar consistentemente:

- `app/admin/internal-stock/page.jsx`
- `components/admin/InternalStockTable.jsx`
- `components/admin/StockFilters.jsx`
- botones `INTERNO` / `SHOWROOM`
- lógica condicional de vista
- links internos
- presets/cards si preservan view

### Criterio de aceptación

Todas estas URLs deben renderizar listado funcional:

```text
/admin/internal-stock
/admin/internal-stock?view=internal
/admin/internal-stock?view=interno
/admin/internal-stock?view=showroom
```

Para `view=internal` y `view=interno`, ambas deben mostrar la vista interna con tabla/cards, no solo filtros.

---

## 5. Reparar lint real

### Problema

`npm run lint` falla con:

```text
ESLint must be installed: npm install --save-dev eslint
```

Existe `.eslintrc.json`:

```json
{
  "extends": "next/core-web-vitals"
}
```

Pero `package.json` no tiene `eslint` ni `eslint-config-next`.

Además `next.config.mjs` contiene:

```js
eslint: {
  ignoreDuringBuilds: true,
}
```

Eso hace que `npm run build` saltee lint:

```text
Skipping linting
```

### Corrección requerida

Configurar lint de forma real y honesta.

Opción recomendada:

1. Agregar devDependencies compatibles con Next 14.2.4:

```json
"eslint": "^8.57.0",
"eslint-config-next": "14.2.4"
```

2. Mantener `.eslintrc.json` si funciona.
3. Ejecutar:

```bash
npm install
npm run lint
```

4. Corregir errores reales de lint si aparecen.
5. Remover `eslint.ignoreDuringBuilds=true` salvo que haya una razón explícita y documentada. Para esta tarea, la expectativa es que build no esconda lint.

### No permitido

No cambiar el script a algo falso como:

```json
"lint": "echo ok"
```

No dejar `ignoreDuringBuilds=true` como workaround silencioso.

No desactivar reglas solo para pasar sin revisar.

### Criterio de aceptación

Debe pasar:

```bash
npm run lint
npm run build
```

Y el build no debería imprimir “Skipping linting” por configuración propia del proyecto.

---

## 6. Quitar `.hermes` del repo

### Problema

El commit auditado incluyó un archivo local de Hermes:

```text
.hermes/desktop-attachments/chatgpt_prompt_filters.md
```

Ese archivo no pertenece al repo de la app.

### Corrección requerida

- Remover `.hermes/desktop-attachments/chatgpt_prompt_filters.md` del tracking del repo.
- Agregar `.hermes/` a `.gitignore` si no está ignorado.
- No borrar archivos fuera del repo.
- Si el archivo existe localmente, puede quedar local ignorado; no debe quedar versionado.

### Criterio de aceptación

```bash
git status --short
```

no debe mostrar `.hermes/desktop-attachments/chatgpt_prompt_filters.md` como tracked/modified/staged.

Y:

```bash
git ls-files .hermes
```

no debe listar archivos.

---

## 7. Limpiar trailing whitespace en archivos tocados

### Problema

La auditoría detectó trailing whitespace en el commit anterior.

### Corrección requerida

Limpiar espacios finales solamente en archivos tocados por esta corrección.

No reformatear todo el proyecto.

### Criterio de aceptación

```bash
git diff --check
```

Debe pasar sin output.

---

## 8. Corregir semántica de la card “Listos”

### Problema

La card superior muestra algo como:

```text
LISTOS 12
```

Pero varias unidades tienen:

```text
Sin ingreso
Sin asignar
S/P
0 de 0 docs
```

Eso puede ser engañoso: “listos” no significa lo mismo que “visibles/publicados en web”.

### Corrección requerida

Elegir una de estas dos opciones, priorizando claridad:

#### Opción recomendada para scope corto

Renombrar la card según la métrica real.

Si el contador está basado en `published !== false`, entonces la card debe llamarse:

```text
VISIBLES WEB
```

o:

```text
PUBLICADOS
```

Y el link debe apuntar consistentemente a:

```text
/admin/internal-stock?published=yes
```

#### Opción más operativa

Si se mantiene el label “LISTOS”, entonces el contador debe calcular realmente unidades listas operativamente.

Criterios mínimos posibles:

- `internalStatus` en `ready_to_publish` o `published`;
- sin `blockedReason` activo;
- `technicalStatus === 'ready'`;
- no tener `nextActionAt` vencida;
- no estar vendida/entregada si la card es de publicación.

Para este fix final, recomiendo **renombrar la card** si no van a implementar una readiness real completa.

### Criterio de aceptación

El label de la card debe coincidir con la query que abre.

Ejemplos válidos:

```text
PUBLICADOS 12 → ?published=yes
```

No válido:

```text
LISTOS 12 → cuenta publicados aunque no estén operativamente listos
```

---

## 9. Revisar seed demo standalone sin ejecutar mutaciones peligrosas

### Problema

Existen dos scripts:

```text
scripts/seedDemoData.mjs
scripts/seedDemoData.js
```

Riesgos observados:

- duplicación de lógica;
- posible incompatibilidad ESM/CommonJS;
- `seedDemoData.js` guarda `targetMargin: 5000`, incompatible con el formulario que lo trata como porcentaje;
- logs y mutaciones directas.

### Corrección requerida

Dejar un único mecanismo claro de seed demo, idempotente y manual.

Recomendación:

- Mantener solo una variante que funcione con el módulo actual del proyecto.
- Si se mantiene `.mjs`, eliminar o ignorar la `.js` duplicada.
- Corregir `targetMargin` a porcentaje válido, por ejemplo `15`.
- Usar los contratos nuevos de `technicalStatus` y `nextActionType`.
- No ejecutar seed durante `build`.
- No ejecutar seed automáticamente al importar un módulo.

### Criterio de aceptación

- `npm run build` no debe imprimir logs de enrichment/seed.
- El seed debe estar documentado como manual.
- No debe haber dos scripts contradictorios para la misma tarea.

Importante: no ejecutar mutaciones contra datos reales. Este proyecto sigue en demo; mantener datos ficticios.

---

## 10. Mantener documentos privados desactivados

Si el módulo de documentación tiene uploads deshabilitados/no disponibles, eso está bien para este demo.

No reactivar upload documental público a Cloudinary como solución rápida.

Mientras no exista storage privado verificado:

- no permitir documentos reales;
- no subir DNI, cédulas, títulos, informes o documentación sensible;
- mantener referencias ficticias o estados manuales.

---

# Archivos probablemente a tocar

Revisar y tocar solo si corresponde:

```text
models/VehicleInternal.js
components/admin/VehicleInternalForm.jsx
app/actions/updateVehicleInternal.js
app/admin/internal-stock/page.jsx
components/admin/InternalStockTable.jsx
components/admin/StockFilters.jsx
components/admin/StockTopCards.jsx
components/admin/VehicleSummaryTab.jsx
app/admin/page.jsx
app/actions/addVehicle.js
app/api/admin/seed-demo/route.js
scripts/seedDemoData.mjs
scripts/seedDemoData.js
package.json
package-lock.json
.eslintrc.json
next.config.mjs
.gitignore
```

No tocar auth salvo que sea estrictamente lectura para confirmar que no se modifica.

---

# QA obligatorio

Ejecutar en este orden.

## 1. Estado Git inicial

```bash
git status --short
git branch --show-current
git log -3 --oneline --decorate
```

Reportar si hay cambios preexistentes antes de tocar.

## 2. Quality gates

```bash
git diff --check
npx tsc --noEmit
npm run lint
npm run build
```

Criterios:

- `git diff --check`: PASS.
- `npx tsc --noEmit`: PASS.
- `npm run lint`: PASS real, no bypass.
- `npm run build`: PASS y sin ejecutar seed.

## 3. QA browser productivo local

Después de build:

```bash
npm run start
```

Verificar:

```text
http://localhost:3000/admin/internal-stock
http://localhost:3000/admin/internal-stock?view=internal
http://localhost:3000/admin/internal-stock?view=interno
http://localhost:3000/admin/internal-stock?view=showroom
http://localhost:3000/admin/internal-stock?q=%5B
http://localhost:3000/admin/internal-stock?preset=attention
```

### Resultados esperados

- Todas responden HTTP 200.
- `view=internal` muestra listado, no pantalla vacía.
- `view=interno` funciona como alias.
- `view=showroom` muestra vista showroom.
- `q=[` no rompe.
- Preset de atención filtra sin romper búsqueda.

## 4. QA de ficha y persistencia

Abrir una unidad desde el botón `Gestión`.

Verificar:

- URL termina en `?tab=operations`.
- `?tab=internal` también renderiza operaciones como alias.
- Cambiar `technicalStatus` a `needs_review`.
- Cambiar `nextActionType` a `cleaning`.
- Escribir `assignedSellerName`, por ejemplo `Demo Responsable`.
- Guardar.
- Refrescar.
- Confirmar persistencia visual.
- Volver al inventario.
- Confirmar que la tabla muestra el responsable.
- Probar agrupación por responsable.

No usar datos reales.

## 5. Repo hygiene

Verificar:

```bash
git ls-files .hermes
git status --short
```

Esperado:

- `.hermes` no aparece como tracked.
- no hay prompts/contextos locales versionados.

---

# Criterios de aceptación finales

El trabajo se considera terminado solo si se cumple todo:

- No se modificó auth ni acceso demo.
- `technicalStatus` está alineado form/schema/action/seed.
- `nextActionType` está alineado form/schema/action/seed.
- No se guardan strings vacíos inválidos en enums.
- Responsable por nombre se persiste y se muestra.
- Guardar ficha no borra `assignedSeller` futuro si el form no lo controla.
- `view=internal` renderiza listado funcional.
- `view=interno` funciona como alias o redirecciona a `internal`.
- Botón `Gestión` abre operaciones.
- `tab=internal` sigue funcionando como alias.
- `npm run lint` pasa de verdad.
- `npm run build` pasa sin seed y sin esconder lint por `ignoreDuringBuilds`.
- `.hermes` no queda versionado.
- `git diff --check` pasa.
- La card “Listos” no miente: o se renombra a la métrica real o cambia su lógica.
- No se reactivan uploads documentales públicos.
- No se hace deploy.
- No se hace commit/push salvo autorización explícita de Juan.

---

# Formato de respuesta esperado de Antigravity

Al terminar, responder con:

```md
# Resultado — Wolfim Motors Demo final fixes

## Cambios realizados
- ...

## Archivos modificados
- ...

## Auth/demo
- Confirmo que no modifiqué autenticación ni acceso demo.

## Validaciones
- git diff --check: PASS/FAIL
- npx tsc --noEmit: PASS/FAIL
- npm run lint: PASS/FAIL
- npm run build: PASS/FAIL

## QA browser
- /admin/internal-stock: PASS/FAIL
- ?view=internal: PASS/FAIL
- ?view=interno: PASS/FAIL
- ?view=showroom: PASS/FAIL
- q=[: PASS/FAIL
- Gestión → operations: PASS/FAIL
- tab=internal alias: PASS/FAIL
- save/refresh responsable: PASS/FAIL

## Pendientes o riesgos
- ...
```

No devolver solamente “listo”; incluir evidencia de comandos y QA.

---

# Recordatorio final

Esta es una corrección quirúrgica. No rediseñar. No tocar auth. No ampliar producto.

El objetivo es que el cockpit operativo quede consistente, verificable y suficientemente sólido para demo con datos ficticios.
