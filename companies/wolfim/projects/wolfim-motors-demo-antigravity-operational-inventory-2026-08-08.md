---
company: Wolfim
project: wolfim-motors-demo
status: ready-for-antigravity
created: 2026-08-08
phase: operational-inventory-evolution
execution-target: C:\Projects\wolfim-motors-demo
source: web-builder audit + chatgpt_prompt_filters.md
---

# Prompt para Antigravity — Evolución profesional del inventario interno

## Objetivo

Evolucionar el inventario y la ficha interna de Wolfim Motors Demo para convertirlos en un centro operativo útil para una agencia de autos: debe mostrar qué unidades requieren atención, qué las bloquea, quién es responsable, cuánto tiempo llevan en stock, cuánto capital tienen invertido y cuáles están listas para publicar o vender.

No se busca solamente agregar filtros. Se busca transformar los datos almacenados en decisiones y acciones operativas.

---

# 1. Proyecto y ubicación obligatoria

Trabajá exclusivamente sobre:

```text
C:\Projects\wolfim-motors-demo
```

No crees otro repositorio.

No reinicies la aplicación desde una plantilla.

No trabajes sobre Roggero & Roma ni sobre otro proyecto Wolfim.

No escribas en el vault de Obsidian. Al finalizar, entregá el reporte para que web-builder lo documente.

---

# 2. Protocolo inicial obligatorio

Antes de editar:

1. Abrí el proyecto indicado.
2. Leé completos:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `PROJECT_CONTEXT.md`
   - `README.md`
   - `MANUAL_ADMIN.md`
   - `package.json`
3. Ejecutá y reportá:

```bash
git status --short
git branch --show-current
git remote -v
git log -5 --oneline
```

4. Identificá archivos dirty y untracked preexistentes.
5. Preservá `.hermes/` y cualquier otro cambio local que no hayas creado.
6. Inspeccioná el estado real del código antes de asumir que este prompt coincide exactamente con la implementación.
7. Presentá un plan breve y luego ejecutalo de punta a punta.

## Operaciones prohibidas

No ejecutar:

```text
git reset
git clean
git checkout para descartar cambios
git restore sobre cambios preexistentes
git pull sin revisar contexto
force push
```

No hacer commit, push ni deploy sin autorización explícita de Juan.

---

# 3. Stack a preservar

El proyecto actual utiliza:

- Next.js 14 App Router.
- React 18.
- Tailwind CSS.
- MongoDB/Mongoose.
- NextAuth.
- Cloudinary.

Mantené el stack existente salvo necesidad técnica concreta y documentada.

No introduzcas un state manager global, una nueva base de datos ni una librería UI pesada para resolver filtros y agrupación.

No rediseñes el showroom público.

La identidad visual existente de Wolfim debe mantenerse, pero el backoffice puede evolucionar hacia un shell operativo más profesional y compacto.

---

# 4. Contexto funcional

Actualmente existen dos vistas dentro de `InternalStockTable.jsx`:

1. **Interno**: tabla densa orientada al backoffice.
2. **Showroom**: grid visual orientado a ventas/marketing.

Los filtros actuales son globales:

- búsqueda;
- estado interno;
- carrocería;
- visibilidad web.

El objetivo es que cada vista tenga herramientas adecuadas para su función.

La pantalla debe sentirse como una combinación coherente de:

- Linear: toolbar compacta, filtros claros y estados precisos;
- Airtable: vistas y agrupación explícitas;
- Pipedrive: responsabilidad, etapa y próxima actividad;
- Notion: progressive disclosure y estados vacíos útiles.

No copies literalmente esos productos. Usá sus principios de operación y claridad.

---

# 5. Diagnóstico ya validado

Tomá estos puntos como hipótesis verificadas por auditoría, pero confirmalos en el código actual antes de editar.

## 5.1 Estado de datos demo

En la auditoría había:

- 12 vehículos públicos.
- 12 registros `VehicleInternal`.
- 12 con costo de compra.
- 12 con imágenes y precio público.
- 0 con patente.
- 0 con VIN.
- 0 con fecha de ingreso.
- 0 con ubicación física.
- 0 con estado técnico.
- 0 con vendedor asignado.
- 0 con precio mínimo.
- 0 con margen objetivo.
- 1 con documentación iniciada.
- 0 con mantenimiento.
- 1 con checklist iniciado.

No borres ni sustituyas los 12 vehículos.

No uses información real de una agencia o cliente.

## 5.2 Inconsistencia de publicación

El modelo `Vehicle` usa el campo canónico:

```text
published
```

Pero algunas superficies usan:

```text
is_published
```

Revisar especialmente:

- `components/admin/InternalStockTable.jsx`
- `app/api/admin/toggle-published/route.js`
- `app/admin/page.jsx`

Normalizá el contrato a `published`.

No dejes dos fuentes de verdad.

Si existen documentos legacy con `is_published`, diseñá compatibilidad/migración idempotente y documentá qué se encontró. No cambies accidentalmente el estado de publicación.

## 5.3 Campos existentes no conectados a la UI

El modelo interno tenía campos como:

- `engineNumber`;
- `physicalLocation`;
- `technicalStatus`;
- `assignedSeller`.

El formulario interno no permitía editarlos todos.

Conectá modelo, servidor y UI de manera coherente.

## 5.4 Checklist con contratos incompatibles

El schema esperaba aproximadamente:

```text
key
completed
notes
```

Mientras el componente manejaba aproximadamente:

```text
task
description
status
```

Definí un contrato canónico y migrá datos demo de forma segura.

No mantengas ambos contratos en paralelo salvo adaptador temporal claramente documentado.

## 5.5 Documentación

El modelo soportaba más información que la UI y había inconsistencias entre `received` y `verified`.

La carga de archivos usaba Cloudinary mediante URL pública.

No permitir documentos reales mientras no exista una estrategia privada verificable.

Para este alcance:

- deshabilitá o marcá claramente la carga de archivos como no disponible si continúa siendo pública;
- no inventes privacidad;
- no subas documentos reales;
- no expongas URLs de documentación fuera de rutas administrativas protegidas;
- documentá la decisión.

## 5.6 Mantenimiento

La UI permitía agregar/eliminar localmente, pero faltaban capacidades como:

- editar entradas existentes;
- proveedor/taller;
- notas;
- confirmación de eliminación;
- buena interacción touch.

Convertí el historial en CRUD funcional y persistente.

## 5.7 Autenticación demo

Durante la auditoría:

- `getSessionUser()` devolvía superadmin demo;
- middleware permitía todas las rutas;
- `/admin/internal-stock` respondía HTTP 200 sin login.

No guardes VIN, patentes, costos, notas o documentos reales con ese bypass activo.

La corrección de seguridad es prerrequisito del producto operativo.

---

# 6. Visión de producto

La pantalla de inventario debe permitir responder en menos de diez segundos:

1. ¿Qué vehículos necesitan atención?
2. ¿Qué bloquea a cada unidad?
3. ¿Quién es responsable?
4. ¿Cuál es la próxima acción y cuándo vence?
5. ¿Qué unidad está lista para publicar?
6. ¿Cuál lleva demasiado tiempo en stock?
7. ¿Cuánto capital está invertido?
8. ¿Qué margen potencial existe?
9. ¿Qué vehículos están ocultos aunque podrían venderse?
10. ¿Qué información está incompleta?

Cada mejora debe contribuir a una de esas respuestas.

No agregues campos, cards o filtros sin una utilidad operativa concreta.

---

# 7. Alcance obligatorio

Implementá las fases 0 a 4 descritas debajo.

No expandas el alcance a CRM completo, clientes, pagos o contabilidad.

---

# Fase 0 — Seguridad y contratos correctos

## 7.1 Autenticación y autorización

1. Retirá el bypass automático de `getSessionUser()`.
2. Retirá cualquier sesión demo superadmin inyectada desde cliente.
3. Configurá `/login` y logout reales usando la infraestructura NextAuth existente.
4. Protegé:
   - `/admin`;
   - `/admin/:path*`;
   - `/superadmin/:path*`;
   - APIs privadas;
   - Server Actions privadas.
5. Validá sesión y rol en servidor para cada mutación.
6. No confíes solamente en middleware, botones ocultos o estado React.
7. Roles mínimos:
   - `admin` puede operar inventario;
   - `superadmin` puede operar inventario y funciones superadmin;
   - rol insuficiente recibe 403;
   - no autenticado recibe 401 o redirect seguro según superficie.
8. El rol debe provenir del servidor/base de datos, no del request del cliente.

No imprimas credenciales ni valores de `.env.local`.

Si falta una credencial indispensable para verificar login, completá todo lo que pueda verificarse de forma segura y reportá exactamente el bloqueo. No inventes una sesión exitosa.

## 7.2 Publicación

1. Usá `published` como campo canónico.
2. Corregí filtros, dashboard, API, cards y queries.
3. Mantené `featured` como campo canónico para destacados.
4. Revalidá rutas correctas:
   - `/`;
   - `/autos`;
   - `/autos/[id]` o slug real;
   - admin.
5. No permitas que editar datos internos publique automáticamente.

## 7.3 Contratos y validación

1. Definí constantes/enums compartidos o módulos server-safe para:
   - estado interno;
   - origen;
   - estado técnico;
   - ubicación;
   - estado documental;
   - checklist;
   - prioridad;
   - tipo de próxima acción.
2. Validá payloads server-side mediante allowlist y validadores del proyecto.
3. No persistas objetos completos recibidos del cliente sin normalización.
4. Evitá nombres duplicados o contratos incompatibles.

---

# Fase 1 — Modelo operativo y captura de datos

## 8.1 Estados internos

Preservá compatibilidad con los estados existentes y definí un orden de workflow explícito, por ejemplo:

```text
to_review
in_preparation
ready_to_publish
published
reserved
sold
delivered
```

No los ordenes alfabéticamente en la UI. Ordenalos según el proceso operativo.

## 8.2 Estado técnico

Convertí `technicalStatus` en un valor estructurado y filtrable. Propuesta:

```text
not_inspected
diagnosis
waiting_quote
scheduled
in_workshop
ready
blocked
```

Los labels visibles deben estar en español.

## 8.3 Ubicación

Convertí `physicalLocation` en catálogo estructurado/configurable. Defaults demo:

```text
showroom
workshop
detailing
warehouse
consignment
delivered
other
```

No uses free text como única fuente si se necesita filtrar y agrupar.

## 8.4 Responsable

1. Usá `assignedSeller` como referencia a un usuario válido.
2. No dupliques el nombre como fuente de verdad.
3. Mostrá nombre/email apropiado mediante populate/projection segura.
4. Permití `Sin asignar`.
5. Permití editar responsable desde la ficha y mediante quick action segura desde la lista.

## 8.5 Próxima acción

Agregá al modelo interno un bloque estructurado equivalente a:

```text
nextActionType
nextActionNote
nextActionAt
priority
blockedReason
```

Tipos iniciales sugeridos:

```text
documentation
workshop
photos
pricing
content
contact
review
other
```

Prioridades:

```text
low
normal
high
urgent
```

Reglas:

- una unidad no entregada puede estar sin próxima acción, pero debe aparecer como alerta;
- una acción vencida debe resaltarse;
- no ocultes automáticamente una unidad por estar vencida;
- no uses `internalNotes` como sustituto de próxima acción.

## 8.6 Fechas y auditoría mínima

Agregar o reutilizar:

```text
entryDate
lastActivityAt
updatedBy
```

Cada mutación administrativa relevante debe actualizar `lastActivityAt` y, si la sesión lo permite, `updatedBy`.

No implementes una auditoría enterprise. Para este alcance alcanza con una timeline operativa mínima o eventos relevantes persistidos de manera acotada.

## 8.7 Costos y rentabilidad

Preservá:

```text
purchaseCost
minimumSalePrice
targetMargin
currency
```

Agregar un ledger de gastos estructurado si no existe, con entradas equivalentes a:

```text
id
category
amount
currency
date
provider
notes
```

Categorías demo:

```text
transport
paperwork
mechanical
detailing
tires
commission
taxes
other
```

Calcular, preferentemente como valores derivados:

```text
investedCapital = purchaseCost + gastos aplicables
potentialGrossMargin = publicPrice - investedCapital
potentialMarginPercent
stockAgeDays
readinessPercent
openBlockersCount
```

No exponer datos económicos públicamente.

Definí una regla clara para monedas mixtas. No sumes ARS y USD como si fueran la misma moneda. Si no existe cotización configurable, mostrarlas por separado y documentar la limitación.

## 8.8 Documentación

Definí un contrato canónico por ítem que soporte:

```text
key
label
status
notes
issuedAt
expiresAt
verifiedAt
verifiedBy
fileReference opcional
```

Estados sugeridos:

```text
pending
missing
received
verified
not_applicable
expired
```

Requisitos:

- edición de status;
- notas;
- fechas relevantes;
- cálculo de completitud consistente;
- indicador de vencimiento;
- sin URLs públicas de archivos;
- feedback de guardado;
- persistencia al refrescar.

## 8.9 Mantenimiento

Cada entrada debe permitir:

```text
id estable
date
description
mileage opcional
provider opcional
cost
currency
status
notes
```

Implementar:

- crear;
- editar;
- eliminar con confirmación;
- persistir;
- ordenar por fecha;
- feedback de guardado;
- controles accesibles en touch, sin depender de hover.

## 8.10 Prepublicación

Definí un único contrato. Propuesta:

```text
key
label
description
completed
notes
completedAt
completedBy
```

Ítems mínimos:

- documentación revisada;
- mantenimiento revisado;
- limpieza/detailing;
- fotografías;
- precio;
- descripción;
- contacto/WhatsApp;
- revisión final.

No publiques automáticamente cuando llegue a 100%.

## 8.11 Reglas de completitud por etapa

Implementá indicadores claros, sin bloquear de forma arbitraria.

Al ingresar:

- código;
- fecha de ingreso;
- origen;
- costo;
- ubicación;
- responsable.

Antes de publicar:

- precio público;
- fotos;
- descripción mínima;
- documentación mínima;
- revisión técnica;
- contacto;
- checklist.

Mostrá qué falta y permití que un admin continúe con advertencia cuando la regla no sea crítica. Publicar debe seguir siendo una decisión explícita.

---

# Fase 2 — Inventario como cockpit operativo

## 9.1 Vistas

Renombrá conceptualmente:

- `Interno` → `Operaciones` o mantené Interno si el copy existente lo exige, pero que su función sea inequívoca;
- `Showroom` → vista comercial/marketing.

No mezcles los filtros principales de ambas vistas.

## 9.2 Estructura visual

La pantalla debe contener:

1. encabezado compacto;
2. indicadores operativos clickeables;
3. presets/vistas rápidas;
4. búsqueda;
5. filtros;
6. agrupación;
7. orden;
8. resultados;
9. estados de carga, vacío y error.

Evitá cards decorativas grandes que consuman espacio sin aportar decisión.

## 9.3 Indicadores superiores

Mostrar, según permisos y datos disponibles:

- requieren atención;
- listos para publicar;
- documentación faltante;
- en taller;
- sin responsable;
- stock mayor a 60/90 días;
- ocultos pero listos;
- capital invertido por moneda.

Cada indicador debe activar el filtro correspondiente o abrir una vista clara.

No mezcles monedas en un único total sin conversión confiable.

## 9.4 Vistas rápidas de Operaciones

Implementar presets:

```text
Necesitan atención
A revisar
En taller
Listos para publicar
Ocultos pero listos
Sin responsable
Documentación faltante
Stock +60 días
Sin precio mínimo
Todos
```

Los presets pueden estar definidos por configuración local del producto. Guardado personalizado por usuario puede quedar para backlog si requiere un nuevo sistema complejo.

## 9.5 Vistas rápidas de Showroom

Implementar presets:

```text
Visibles
Ocultos
Listos para publicar
Ocultos pero completos
Sin precio
Sin fotos suficientes
Destacados
Reservados
Vendidos
```

## 9.6 Filtros de Operaciones

### Principales

- estado interno;
- atención/bloqueo;
- responsable;
- antigüedad;
- ubicación.

### Secundarios

- origen;
- estado técnico;
- visibilidad web;
- estado público;
- carrocería;
- moneda;
- costo completo/incompleto;
- margen por debajo de objetivo;
- documentación completa/incompleta;
- mantenimiento pendiente;
- prioridad;
- próxima acción vencida.

### Búsqueda

Debe buscar por:

- código interno;
- patente;
- VIN;
- marca;
- modelo;
- versión.

La búsqueda debe estar normalizada para mayúsculas/minúsculas y espacios razonables.

## 9.7 Filtros de Showroom

### Principales

- visibilidad;
- estado comercial;
- marca;
- carrocería;
- condición.

### Secundarios

- destacado;
- rango de precio;
- año;
- kilometraje;
- combustible;
- transmisión;
- cantidad de fotos;
- con/sin descripción;
- con/sin precio;
- ficha completa/incompleta.

### Búsqueda

- marca;
- modelo;
- versión;
- año;
- código como soporte secundario.

No priorices VIN o patente en la vista comercial.

## 9.8 Orden

Operaciones:

```text
Más antiguos
Más recientes
Próxima acción
Mayor inversión
Menor preparación
Última actividad
Código interno
```

Showroom:

```text
Más recientes
Precio mayor/menor
Año
Kilometraje
Ficha más incompleta
Destacados primero
```

## 9.9 Agrupación

Agregar selector compacto:

```text
Agrupar por: [campo]
```

Permitir `Sin agrupar`.

### Operaciones

- estado interno;
- bloqueo principal;
- responsable;
- estado técnico;
- ubicación;
- antigüedad;
- origen.

### Showroom

- visibilidad;
- estado comercial;
- marca;
- carrocería;
- condición;
- destacado;
- rango de precio.

No implementar grouping de dos niveles en este alcance.

## 9.10 Render agrupado desktop

Usar una tabla única con encabezados de grupo insertados, o una arquitectura equivalente que mantenga alineación.

Cada header de grupo debe mostrar:

- label;
- cantidad;
- resumen útil según grupo;
- control expandir/colapsar.

Ejemplo:

```text
EN PREPARACIÓN · 4 UNIDADES · 2 BLOQUEADAS · 48 DÍAS PROMEDIO
```

Ordenar estados según workflow, no alfabéticamente.

Mostrar `Sin asignar`/`Sin datos` al final.

## 9.11 Columnas de Operaciones

Rediseñá la tabla para priorizar acción, no acumulación de campos.

Columnas recomendadas:

1. Vehículo e identificación.
2. Estado/ubicación.
3. Pendiente principal.
4. Preparación.
5. Antigüedad/última actividad.
6. Financiero.
7. Responsable/próxima acción.
8. Acciones.

En `Pendiente principal`, derivar mensajes como:

```text
3 documentos faltantes
Taller pendiente
Sin responsable
Precio mínimo faltante
Acción vencida
Listo para publicar
```

No obligues al usuario a inferir el bloqueo combinando cinco columnas.

## 9.12 Cards Showroom

Cada card debe mostrar:

- imagen principal;
- marca/modelo/versión/año;
- precio;
- kilometraje;
- visibilidad;
- destacado;
- completitud pública;
- cantidad de fotos;
- preview público;
- editar;
- publicar/ocultar con confirmación y feedback.

No mostrar datos internos sensibles en las cards.

## 9.13 Quick actions

Desde la vista Operaciones permitir, con autorización server-side:

- cambiar estado;
- asignar responsable;
- cambiar ubicación;
- registrar próxima acción;
- abrir gestión.

No permitir edición inline de VIN, patente, costos o notas sensibles sin entrar a la ficha.

Las acciones deben tener:

- loading;
- error;
- rollback visual o re-fetch;
- confirmación cuando corresponda;
- controles touch accesibles.

---

# Fase 3 — Estado y arquitectura React

## 10.1 URL como fuente de verdad

Usá parámetros de URL allow-listed para estado comprometido:

```text
view
q
preset
internalStatus
attention
seller
age
location
technicalStatus
published
featured
bodyType
group
sort
page
```

Ejemplo:

```text
/admin/internal-stock?view=internal&attention=documents&age=60-plus&group=internalStatus&sort=days-desc
```

Beneficios obligatorios:

- refresh preserva estado;
- Back/Forward funciona;
- enlaces del dashboard abren vistas reales;
- filtros pueden compartirse;
- no existen estados contradictorios invisibles.

## 10.2 Estado local

Usar estado local solamente para:

- drawer abierto/cerrado;
- grupos colapsados;
- texto de búsqueda previo al debounce;
- draft de filtros mobile;
- menús transitorios.

`useReducer` es aceptable para el draft del drawer, pero no debe reemplazar los URL params como fuente de verdad.

## 10.3 Búsqueda

- debounce razonable, aproximadamente 250–350 ms;
- navegación con `router.replace`/`startTransition` o patrón equivalente;
- reset de `page` al cambiar filtros;
- accesibilidad de loading;
- no ejecutar una request por cada render accidental.

## 10.4 Queries

Para producto clonable:

1. Parseá `searchParams` en servidor.
2. Validá contra allowlists.
3. Construí query Mongo explícita.
4. Usá projections/DTOs mínimos.
5. Implementá paginación.
6. Calculá agregados necesarios en servidor.
7. No envíes VIN, notas, documentos o costos a la vista Showroom si no los necesita.
8. No hagas matching O(n²) entre colecciones si puede resolverse con mapa o aggregate controlado.

No sobreoptimices los 12 registros demo, pero dejá una arquitectura apta para cientos de unidades.

---

# Fase 4 — Ficha interna profesional

## 11.1 Tabs

Agregar un tab inicial de resumen. Orden recomendado:

```text
Resumen
Ficha pública
Interno / Finanzas
Documentación
Taller
Checklist
Actividad
```

Se puede adaptar el copy a la UI existente, pero el resumen debe ser la primera vista operativa.

## 11.2 Header

Mostrar:

- vehículo;
- código;
- patente;
- estado interno;
- visibilidad;
- responsable;
- ubicación;
- días en stock.

Acciones rápidas:

- cambiar estado;
- asignar responsable;
- crear próxima acción;
- agregar mantenimiento;
- publicar/ocultar;
- ver ficha pública.

## 11.3 KPIs por unidad

Mostrar cuatro bloques compactos:

### Capital

- compra;
- gastos;
- total invertido.

### Margen

- precio público;
- precio mínimo;
- margen potencial;
- objetivo.

### Preparación

- documentos;
- taller;
- checklist;
- contenido/fotos.

### Tiempo

- días en stock;
- última actividad;
- próxima acción.

## 11.4 Qué falta

Agregar un bloque prominente derivado de reglas:

```text
Requiere atención
- Falta responsable
- 3 documentos faltantes
- Taller pendiente
- Precio mínimo faltante
- Próxima acción vencida
```

Debe distinguir:

- bloqueo crítico;
- advertencia;
- información faltante;
- listo.

No muestres todos los estados como rojo.

## 11.5 Actividad

Implementar timeline operativa mínima para eventos relevantes:

- cambio de estado;
- cambio de responsable;
- mantenimiento agregado/editado/eliminado;
- documentación actualizada;
- checklist actualizado;
- publicación/ocultamiento;
- próxima acción.

Cada evento debe tener:

- fecha;
- tipo;
- resumen;
- usuario cuando esté disponible.

No incluyas secretos ni datos sensibles completos en logs o eventos.

## 11.6 Prevención de pérdida de cambios

- feedback visible al guardar;
- estados loading/success/error;
- evitar doble submit;
- advertencia razonable si se navega con cambios no guardados, donde aplique;
- persistencia comprobada después de refrescar.

---

# 12. Responsive obligatorio

## Desktop grande

Toolbar en una línea cuando exista ancho real:

```text
[Buscar] [Filtros] [Agrupar] [Ordenar] [+ Nuevo]
```

Debajo, presets compactos.

## iPad/tablet

No usar cuatro selects comprimidos.

Dos filas:

```text
Fila 1: [Buscar] [Filtros N] [+ Nuevo]
Fila 2: [presets con scroll] [Agrupar] [Ordenar]
```

Usar side sheet o panel de filtros en tablet si mejora la experiencia.

No activar el layout desktop completo simplemente desde `md` si no cabe.

## Mobile

Mostrar:

```text
[Buscar]
[Operaciones | Showroom]
[Filtros N] [Ordenar/Agrupar]
[chips activos con scroll]
```

Filtros en bottom sheet/drawer con:

- secciones claras;
- draft local;
- `Limpiar`;
- `Ver N vehículos` sticky.

Resultados como cards operativas agrupadas, no mini-tabla horizontal.

No depender de hover para acciones.

## Viewports de QA

Probar al menos:

```text
375 × 812
768 × 1024
1024 × 768
1440 × 900
```

---

# 13. Accesibilidad y UX

1. Inputs con `label` correctamente asociado.
2. Botones icon-only con `aria-label`.
3. Focus visible.
4. Menús operables con teclado.
5. Estados no diferenciados solo por color.
6. Contraste suficiente.
7. Anuncios accesibles de loading/error/success cuando aplique.
8. Targets touch adecuados.
9. Confirmación para acciones destructivas.
10. Empty states que expliquen cómo resolver el filtro vacío.
11. Mostrar cantidad de filtros activos.
12. `Limpiar filtros` debe ser siempre accesible.

---

# 14. Datos demo y migración

## Reglas

1. No ejecutar `deleteMany()` sobre vehículos.
2. No borrar los 12 registros existentes.
3. No reemplazar imágenes ni precios públicos.
4. No usar datos reales.
5. Migraciones idempotentes.
6. Incluir `--dry-run` o mecanismo equivalente cuando la migración toque datos.
7. Mostrar conteos antes/después.
8. Documentar rollback.
9. No imprimir connection strings.

## Dataset demo

Enriquecer de forma idempotente al menos 4 vehículos con datos ficticios suficientes para demostrar:

1. unidad en taller con acción vencida;
2. unidad lista para publicar pero oculta;
3. unidad con documentación faltante y sin responsable;
4. unidad con stock envejecido y margen bajo.

Usar valores obviamente ficticios.

No utilizar VIN, matrículas, nombres o documentos de personas reales.

Los 8 vehículos restantes pueden conservar datos mínimos, pero deben mostrar estados de completitud honestos.

## Defaults de producto

Usar:

```text
Antigüedad: 0–30, 31–60, 61–90, +90 días
Vista inicial: Necesitan atención
Agrupación operativa inicial: Estado interno
Próxima acción: alerta si falta en unidades no entregadas
Ubicaciones: catálogo configurable
Responsables: usuarios reales
Adjuntos: deshabilitados hasta storage privado verificable
```

Si un default contradice datos existentes o una regla del proyecto, preservá el dato y documentá la adaptación.

---

# 15. Seguridad y privacidad

Datos privados que nunca deben aparecer públicamente:

- costo de compra;
- precio mínimo;
- margen;
- gastos;
- VIN;
- patente, salvo decisión explícita futura;
- número de motor;
- ubicación interna;
- responsable;
- documentación;
- archivos;
- notas internas;
- mantenimiento privado;
- checklist interno;
- próxima acción;
- actividad interna.

Verificar ausencia en:

- `/`;
- `/autos`;
- ficha pública;
- APIs públicas;
- HTML inicial;
- RSC payload;
- metadata;
- Open Graph;
- sitemap;
- robots;
- story/share;
- errores cliente;
- consola;
- logs.

Usá DTOs/projections por allowlist. No cargues documentos completos y luego borres campos en cliente.

## Sentinel de privacidad

Cargá valores ficticios distintivos en un registro demo, por ejemplo:

```text
internalStockCode: PRIV-OPS-8841
VIN ficticio: TESTVINOPS8841
patente ficticia: ZZ999ZZ
nota: SENTINEL_INTERNAL_ONLY_8841
costo distintivo demo
```

Buscá esos valores en todas las superficies públicas y reportá que no aparecen.

No uses esos ejemplos si chocan con validaciones legales; adaptalos manteniendo su carácter inequívocamente ficticio.

---

# 16. Fuera de alcance

No implementar ahora:

- CRM completo de leads;
- pipeline de oportunidades;
- WhatsApp automation;
- facturación;
- contabilidad;
- pagos;
- financiación;
- clientes reales;
- contratos;
- reservas con datos personales;
- multitenancy completo;
- OCR;
- integración con organismos;
- tracking GPS;
- auditoría enterprise;
- documentos privados reales;
- reportes financieros contables;
- conversión automática de monedas sin fuente confiable.

Podés documentarlos como backlog P2.

---

# 17. Archivos esperables

Inspeccioná nombres reales antes de editar. Es probable que debas tocar o crear equivalentes a:

```text
components/admin/InternalStockTable.jsx
components/admin/VehicleAdminTabs.jsx
components/admin/VehicleInternalForm.jsx
components/admin/DocumentationChecklist.jsx
components/admin/MaintenanceHistory.jsx
components/admin/PrePublishChecklist.jsx
app/admin/internal-stock/page.jsx
app/admin/vehicles/[id]/edit/page.jsx
app/admin/layout.jsx
app/admin/page.jsx
app/api/admin/toggle-published/route.js
app/api/admin/toggle-featured/route.js
app/actions/updateVehicleInternal.js
app/actions/updateVehicleDocumentation.js
app/actions/updateVehicleMaintenance.js
app/actions/updateVehicleChecklist.js
models/Vehicle.js
models/VehicleInternal.js
models/User.js
utils/getSessionUser.js
utils/requireAdmin.js
middleware.js
```

Probablemente necesites componentes pequeños para:

- toolbar;
- filter drawer;
- active chips;
- group header;
- operational summary;
- vehicle overview;
- activity timeline;
- quick actions.

No fragmentes en decenas de componentes sin beneficio. Separá cuando reduzca complejidad y permita pruebas.

---

# 18. Estrategia de implementación

Ejecutá en este orden:

1. Inspección y baseline.
2. Auth y autorización.
3. Contratos canónicos/migración.
4. Modelo operativo.
5. Formularios y persistencia.
6. Query/DTO del inventario.
7. URL state.
8. Filtros por vista.
9. Agrupación y orden.
10. Responsive.
11. Resumen de ficha.
12. Datos demo idempotentes.
13. QA técnico.
14. QA de navegador.
15. Documentación.

No construyas primero una UI nueva sobre contratos rotos.

---

# 19. Pruebas técnicas

Ejecutá los scripts reales disponibles y reportá código de salida.

Como mínimo:

```bash
git diff --check
npm run lint
npx tsc --noEmit
npm run build
npm test
```

Si `npm test` no existe, informalo como `NOT CONFIGURED`; no lo declares PASS.

Si agregás:

```text
npm run typecheck
```

Ejecutalo también.

El lint debe ser no interactivo. No relajes reglas globalmente para ocultar errores.

No declares PASS sin output real.

---

# 20. Pruebas funcionales

## Autenticación

- `/admin` anónimo.
- `/admin/internal-stock` anónimo.
- Server Action anónima.
- API privada anónima.
- rol insuficiente.
- admin válido.
- superadmin válido.
- logout.

## Inventario

- búsqueda por código;
- búsqueda por marca/modelo;
- búsqueda por patente ficticia;
- filtro por estado;
- filtro por atención;
- filtro por responsable;
- filtro por antigüedad;
- filtros Showroom;
- presets;
- limpiar filtros;
- Back/Forward;
- refresh conserva estado;
- URL compartible;
- sort;
- agrupación;
- colapsar/expandir;
- empty state;
- paginación si aplica.

## Ficha

- resumen;
- editar datos internos;
- asignar vendedor;
- cambiar ubicación;
- cambiar estado técnico;
- crear próxima acción;
- detectar vencimiento;
- agregar/editar/eliminar mantenimiento;
- documentación;
- checklist;
- costos;
- margen;
- persistencia al refrescar;
- timeline.

## Publicación

- toggle usa `published`;
- visible aparece públicamente;
- oculto no aparece públicamente;
- editar interno no cambia publicación;
- destacado continúa funcionando.

## Responsive

Probar todos los viewports requeridos.

## Privacidad

Buscar todos los sentinels en superficies públicas.

---

# 21. Criterios de aceptación

## Fundación

- no existe superadmin demo automático;
- admin requiere login real;
- mutaciones privadas verifican rol en servidor;
- documentos públicos deshabilitados o reemplazados por storage privado verificable;
- `published` es la fuente canónica;
- contratos Mongoose/UI/Actions coinciden.

## Operaciones

- la vista inicial muestra qué necesita atención;
- filtros principales son específicos de Operaciones;
- agrupación funciona y respeta orden de workflow;
- búsqueda incluye código, patente, VIN y vehículo;
- se puede identificar responsable, ubicación y próxima acción;
- stock envejecido es visible;
- bloqueos se entienden sin abrir la ficha;
- capital/margen se muestran sin mezclar monedas;
- quick actions persisten y están autorizadas.

## Showroom

- tiene filtros propios;
- no muestra datos internos sensibles;
- permite encontrar ocultos/incompletos/listos;
- cards preservan calidad visual;
- publicación y destacado funcionan.

## Ficha

- Resumen es la primera vista;
- muestra KPIs;
- muestra `Qué falta`;
- próxima acción editable;
- mantenimiento CRUD;
- documentación consistente;
- checklist consistente;
- actividad visible;
- datos persisten después de refresh.

## Responsive

- desktop profesional y denso;
- iPad no comprime cuatro selects;
- mobile usa drawer y cards;
- no depende de hover;
- sin overflow horizontal accidental.

## Calidad

- build PASS;
- typecheck PASS;
- lint no interactivo;
- sin errores de consola relevantes;
- sin secretos;
- sin datos privados públicos;
- sin commit/push/deploy.

---

# 22. Documentación

Actualizar en el repositorio:

- `PROJECT_CONTEXT.md`: arquitectura final y contratos.
- `README.md`: setup relevante si cambió.
- `MANUAL_ADMIN.md`: uso operativo de inventario, filtros, grouping, ficha, auth y limitación de adjuntos.
- `AGENTS.md`: solamente si existe una nueva regla duradera del proyecto.

No documentes valores de credenciales.

No escribas directamente en Obsidian.

---

# 23. Formato obligatorio de respuesta final

Entregá exactamente estas secciones:

## 1. Resumen ejecutivo

Qué valor operativo quedó implementado.

## 2. Inspección inicial

- ruta;
- rama;
- git status;
- archivos preexistentes;
- baseline de lint/typecheck/build;
- seguridad encontrada;
- datos encontrados.

## 3. Plan aplicado

Orden real y cualquier desviación.

## 4. Arquitectura final

- auth;
- modelos;
- contratos;
- queries;
- DTOs;
- URL state;
- filtros;
- grouping;
- métricas;
- timeline;
- responsive.

## 5. Funcionalidades implementadas

Separar:

- Operaciones;
- Showroom;
- ficha;
- documentación;
- mantenimiento;
- checklist;
- seguridad.

## 6. Archivos modificados/creados

Lista y propósito.

## 7. Migración

- dry run;
- apply;
- conteos antes/después;
- compatibilidad;
- rollback;
- demo data.

## 8. Pruebas técnicas

Comando, código de salida y resultado real.

## 9. QA de navegador

Ruta, viewport, resultado y evidencia resumida.

## 10. Seguridad y privacidad

- auth;
- autorización;
- storage documental;
- sentinel público/privado;
- datos económicos.

## 11. Criterios de aceptación

Marcar cada uno:

```text
PASS
PARTIAL
NOT TESTED
FAIL
```

## 12. Riesgos o pendientes

Errores exactos y decisiones que necesitan aprobación.

## 13. Backlog P2

Solo lo no implementado.

## 14. Cómo ejecutar localmente

Comandos reales, sin secretos.

## 15. Estado Git final

```bash
git status --short
git diff --stat
git diff --check
```

Confirmar que no se hizo commit, push ni deploy.

## 16. Bloque listo para `response.md`

Resumen autocontenido para que web-builder pueda documentar el resultado.

---

# 24. Regla final

No te detengas después de crear componentes o escribir un plan.

La tarea está terminada solamente cuando:

- la implementación funciona;
- los datos persisten;
- filtros y agrupación fueron ejercitados;
- la ficha interna genera información accionable;
- auth y privacidad fueron verificadas;
- responsive fue probado;
- build/typecheck/lint fueron ejecutados;
- el estado Git final fue informado.

Si algo no puede completarse, no inventes un PASS. Reportá el error exacto, el impacto y el siguiente paso seguro.
