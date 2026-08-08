---
owner: wolfim-growth
validated-by: brain-vps
status: ready-for-web-builder
created: 2026-08-03
last-updated: 2026-08-07
type: LOCAL_REQUEST
scope-version: v2
company: Wolfim
target: brain-vps-to-web-builder
priority: high
official-handoff: Hermes/Handoffs/vps-to-local/HO-2026-08-03-002/request.md
related-plan: companies/wolfim/research/automotive-portal-plan-2026-08-03.md
related-product-module: companies/wolfim/research/automotive-portal-internal-stock-module-2026-08-07.md
merged-addendum: companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-internal-stock-addendum-2026-08-07.md
---

# LOCAL_REQUEST — Wolfim Motors: finalizar showroom y agregar módulo interno privado

## 1. Pedido ejecutivo

Continuar el proyecto existente **Wolfim Motors Demo**, cerrar el showroom público y desarrollar una primera versión funcional del módulo interno privado por vehículo.

No iniciar otro clon ni rehacer el proyecto desde cero sin una razón técnica bloqueante.

El producto debe quedar compuesto por dos capas claramente separadas:

1. **Showroom público:** catálogo y fichas para vender vehículos.
2. **Backoffice privado:** registro interno de stock, documentación, mantenimiento y tareas por unidad.

## 2. Estado actual informado por Juan

Juan confirmó el 2026-08-07 que:

- el showroom demo está aproximadamente **90% funcional**;
- el proyecto ya es **clonable**;
- la siguiente oportunidad de producto es sumar orden interno de stock;
- el objetivo no es construir otra maqueta, sino completar y extender lo que ya funciona.

Por lo tanto, web-builder debe comenzar por localizar e inspeccionar el proyecto existente en el entorno local.

Antes de modificar código debe registrar:

- ruta absoluta del proyecto;
- estado actual del repositorio/carpeta;
- URL preview existente, si la hay;
- funcionalidades completas;
- funcionalidades incompletas;
- build actual;
- deuda o restos de la reconversión inmobiliaria.

## 3. Objetivo comercial

Juan necesita un producto que pueda mostrar desde iPad/celular en visitas a concesionarias y decir:

> Este portal muestra el stock hacia afuera y también ordena cada unidad puertas adentro.

Wolfim no vende una web genérica. Vende un portal operativo para concesionarias:

- presencia y catálogo propios;
- consulta por vehículo;
- contenido compartible;
- administración de stock;
- ficha privada con información operativa.

## 4. Prioridad y secuencia

### P0 — Cerrar y estabilizar showroom público

Completar el 10% restante del demo actual y dejar un preview estable.

P0 no debe ser reemplazado por un rediseño general ni por una reconstrucción innecesaria.

### P1 — Módulo interno privado mínimo

Agregar una ficha privada funcional por vehículo, protegida por autenticación, con datos internos, documentación registrada, mantenimiento y checklist.

P1 es el siguiente sprint requerido y el principal diferencial nuevo.

### P2 — Evolución operativa

Dejar documentadas, pero no bloquear la entrega por:

- archivos privados reales con almacenamiento seguro;
- alertas de vencimiento;
- roles avanzados;
- reportes;
- exportaciones;
- integraciones con terceros.

## 5. Base técnica y continuidad

La base original disponible en VPS fue Roggero & Roma:

```text
/home/hermes/roggero_backup/
/home/hermes/roggero_backup/data/github/properties.git
```

Stack identificado en el request original:

- Next.js 14;
- MongoDB/Mongoose;
- Tailwind;
- NextAuth;
- Cloudinary;
- Google Maps;
- PDF;
- OpenAI.

Esa referencia explica el origen del demo, pero la fuente de verdad para esta tarea es el proyecto local ya desarrollado y reportado por Juan como 90% funcional.

No volver a clonar Roggero si el proyecto automotriz existente ya funciona.

## 6. Restricciones absolutas

- No tocar producción de Roggero & Roma.
- No usar marca, datos, imágenes, propiedades, usuarios ni documentos reales de Roggero & Roma.
- No copiar secretos, tokens, credenciales ni archivos `.env` del cliente.
- No mostrar secretos en UI, logs, capturas o `response.md`.
- Referenciar credenciales solo como `[credencial: NOMBRE_VARIABLE]`.
- No contratar servicios ni generar gastos sin aprobación de Juan.
- No publicar documentos privados reales en el demo.
- No escribir código ni activos de la aplicación dentro del vault.
- No eliminar funcionalidad que ya está operativa sin justificarlo.
- No declarar “listo” sin build y preview reales.

## 7. Estrategia de clonabilidad

El modelo comercial actual es **un proyecto/deploy aislado por concesionaria**, no un SaaS multi-tenant.

Fuera de alcance en esta fase:

- multi-tenancy;
- billing automático;
- alta automática de agencias;
- panel maestro de Wolfim para muchos clientes.

El clon debe poder adaptarse a una nueva concesionaria sin búsqueda/reemplazo global por todo el código.

Centralizar como configuración:

- nombre comercial;
- logo;
- colores;
- WhatsApp;
- email;
- dirección;
- horarios;
- redes;
- dominio/base URL;
- moneda;
- textos institucionales;
- coordenadas del showroom;
- datos SEO por defecto.

Entregar:

- archivo de configuración o esquema equivalente;
- seed de vehículos demo;
- instrucciones de clonado/adaptación;
- lista de variables de entorno requeridas sin valores secretos.

## 8. Alcance público P0

### 8.1 Home

Debe incluir:

- hero automotor;
- búsqueda por marca/modelo;
- vehículos destacados o últimos ingresos;
- CTA WhatsApp;
- identidad Wolfim Motors Demo;
- navegación completa;
- percepción visual de concesionaria premium.

### 8.2 Catálogo

Ruta preferida: `/autos` o `/vehicles`, manteniendo una sola convención.

Debe incluir:

- grid responsive;
- filtros por marca;
- modelo;
- año;
- rango de precio;
- kilometraje;
- combustible;
- transmisión;
- carrocería;
- sorting por precio, año o más recientes;
- estados disponible, reservado y vendido;
- empty state claro cuando no hay resultados.

### 8.3 Ficha pública por vehículo

Debe incluir:

- galería;
- marca;
- modelo;
- versión;
- año;
- kilometraje;
- combustible;
- transmisión;
- carrocería;
- color;
- equipamiento;
- precio o “consultar” si corresponde;
- estado público;
- CTA WhatsApp con vehículo identificado;
- botón Compartir historia;
- URL única por vehículo;
- metadata SEO pública sin datos internos.

### 8.4 Contacto/showroom

Debe incluir:

- ubicación ficticia o claramente demo;
- horarios;
- WhatsApp;
- email/formulario si ya está implementado;
- mapa solo con datos ficticios/configurados.

### 8.5 Datos demo

- 12 a 15 vehículos ficticios.
- Mezcla de 0 km y usados.
- Estados disponible, reservado y vendido.
- Fotos libres/generadas con uso permitido.
- Sin patentes visibles.
- Sin personas identificables.
- Sin marcas o datos del proyecto inmobiliario original.

## 9. Compartir historia 9:16

Cada ficha pública debe generar una placa vertical 9:16 con:

- foto del vehículo;
- marca/modelo/año;
- precio o CTA;
- logo/branding configurado;
- llamada a la acción;
- QR o link a la ficha.

Comportamiento:

- en mobile/iPad usar Web Share API cuando esté disponible;
- fallback a descarga de imagen;
- no prometer autopublicación directa en Instagram/Facebook;
- no generar una historia con URL rota o QR inválido;
- verificar al menos una historia descargada y una compartida mediante fallback soportado.

## 10. Admin y autenticación

El backoffice debe requerir login.

Para esta primera versión alcanza un rol administrador único, siempre que:

- las rutas privadas estén protegidas del lado servidor o con el mecanismo seguro del stack existente;
- no baste con ocultar componentes en frontend;
- una sesión no autenticada no pueda leer ni mutar datos internos;
- el logout invalide el acceso al backoffice;
- el demo no incluya credenciales reales en código o documentación.

Referencias permitidas:

```text
[credencial: DEMO_ADMIN_USER]
[credencial: DEMO_ADMIN_PASSWORD]
[credencial: DATABASE_URL]
[credencial: CLOUDINARY_OR_STORAGE_KEY]
```

## 11. Modelo funcional de vehículo

Separar campos públicos y privados de forma explícita.

### 11.1 Campos públicos mínimos

```text
id
slug
brand
model
version
year
mileage
price
priceOnRequest
fuelType
transmission
bodyType
color
features[]
images[]
publicStatus
featured
published
createdAt
updatedAt
```

Estados públicos:

```text
available
reserved
sold
```

### 11.2 Campos privados mínimos P1

```text
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
maintenanceHistory[]
prePublishChecklist
```

Estados internos sugeridos:

```text
to_review
in_preparation
ready_to_publish
published
reserved
sold
delivered
```

Origen de stock sugerido:

```text
purchase
trade_in
consignment
other
```

## 12. UX del módulo privado P1

En edición/detalle admin de un vehículo, organizar:

1. **Ficha pública**
2. **Interno**
3. **Documentación**
4. **Mantenimiento**
5. **Checklist**

Puede resolverse con tabs, secciones o navegación equivalente. Debe ser usable en desktop y revisable en iPad.

### 12.1 Interno

Campos requeridos:

- código interno de stock;
- patente/dominio;
- VIN/chasis;
- número de motor;
- fecha de ingreso;
- origen del stock;
- ubicación física;
- estado interno;
- responsable/vendedor;
- estado técnico general;
- notas internas;
- costo de compra/toma;
- margen objetivo;
- precio mínimo aceptable.

Patente, VIN/chasis y número de motor son privados por defecto.

Los campos económicos son privados y nunca deben aparecer en la ficha pública.

### 12.2 Documentación

P1 debe permitir registrar estado y observaciones de:

- título;
- cédula;
- formulario 08;
- informe de dominio;
- verificación policial;
- libre deuda de infracciones/patentes;
- VTV/RTO;
- factura o boleto;
- comprobantes de service;
- garantía;
- manuales;
- otros.

Estado sugerido por documento:

```text
missing
pending
received
verified
not_applicable
```

Cada registro debe admitir:

- tipo;
- estado;
- observación;
- fecha de emisión opcional;
- fecha de vencimiento opcional;
- nombre de archivo o referencia opcional.

### 12.3 Archivos privados

Para P1, el registro/checklist documental es obligatorio.

La carga binaria de PDF/imágenes solo entra en P1 si el proyecto ya tiene almacenamiento privado seguro reutilizable.

Si se implementan archivos:

- almacenamiento privado;
- acceso autenticado;
- URL temporal o firmada;
- validación de tipo/tamaño;
- sin bucket público;
- sin indexación;
- sin archivos reales en seed/demo.

Si no se implementan archivos en P1, dejar interfaz/modelo preparado y documentarlo como P2. No simular seguridad con enlaces públicos ocultos.

### 12.4 Mantenimiento y preparación

P1 debe permitir crear, editar y eliminar entradas internas con:

```text
date
type
description
status
cost
provider
notes
```

Tipos sugeridos:

- revisión mecánica;
- aceite/filtros;
- frenos;
- batería;
- cubiertas;
- tren delantero;
- alineación/balanceo;
- revisión eléctrica;
- reparación estética;
- detailing/lavado;
- service;
- otro.

Estados sugeridos:

```text
pending
in_progress
done
cancelled
```

### 12.5 Checklist prepublicación

Debe contemplar:

- fotos cargadas;
- precio definido;
- documentación revisada;
- mecánica revisada;
- lavado/detailing realizado;
- descripción aprobada;
- ficha pública revisada;
- historia generada;
- publicado en web;
- compartido en redes;
- publicado en portal externo si corresponde.

Mostrar avance de manera simple, sin bloquear publicación automáticamente salvo que ya exista esa lógica.

### 12.6 Vista interna de stock

Para que el módulo sirva realmente como ordenamiento y no solo como ficha aislada, P1 debe incluir una vista interna de stock.

Tabla o lista mínima:

- código interno;
- vehículo;
- patente/dominio;
- fecha de ingreso;
- días en stock calculados;
- ubicación;
- estado interno;
- estado documental resumido;
- tareas/mantenimiento pendientes;
- responsable;
- acción para abrir ficha.

Filtros mínimos:

- búsqueda por código, marca/modelo, patente o VIN;
- estado interno;
- documentación incompleta;
- mantenimiento/tareas pendientes;
- responsable;
- ubicación.

Puede incluir contadores simples como disponibles, en preparación, listos para publicar, reservados y vendidos. No se requiere dashboard analítico complejo.

## 13. Privacidad y separación público/privado

Regla crítica:

> Ningún campo interno debe salir por rutas, APIs, payloads, metadata, sitemap, JSON público o pre-render accesible sin autenticación.

Validar específicamente que no se expongan:

- costo de compra;
- margen;
- precio mínimo;
- patente/dominio;
- VIN/chasis;
- número de motor;
- notas internas;
- estado técnico privado;
- responsable;
- documentación;
- mantenimiento;
- checklist interno;
- URLs de archivos privados.

No alcanza con no renderizar los campos. El backend/API debe devolver solo el DTO público en rutas públicas.

## 14. SEO y analytics

### SEO

- fichas públicas publicadas incluidas en sitemap;
- vehículos no publicados excluidos;
- rutas admin excluidas;
- metadata automotriz coherente;
- sin referencias inmobiliarias;
- canonical/base URL configurable.

### Analytics básico

Si ya existe analytics, registrar al menos:

- vista de ficha;
- click WhatsApp por vehículo;
- uso de Compartir historia;
- envío de formulario.

No registrar datos privados del backoffice ni contenido de documentos/notas.

## 15. Fuera de alcance actual

No bloquear la entrega por:

- multi-tenancy;
- CRM completo;
- facturación;
- contabilidad;
- app móvil nativa;
- publicación automática en Instagram/Facebook;
- integración MercadoLibre/GTM;
- alertas automáticas;
- permisos avanzados por equipo;
- reportes financieros;
- importación masiva;
- IA para descripciones;
- firma digital de documentos.

Estos puntos pueden documentarse como evolución posterior.

## 16. Protección del proyecto y de los datos

Antes de cambiar esquemas, seed o persistencia:

- identificar dónde vive la información actual;
- evitar migraciones destructivas;
- conservar los 12 a 15 vehículos demo existentes;
- realizar backup/export si una migración puede modificar datos;
- mantener compatibilidad o documentar migración;
- no mezclar datos de dos concesionarias;
- no reutilizar usuarios, bases o storage reales de Roggero.

Si el proyecto actual usa datos mock, mantener el seed separado y repetible. Si usa base persistente, documentar migraciones y rollback.

## 17. Criterios de aceptación P0

- Se continúa el proyecto existente; no se genera un clon duplicado sin justificación.
- Preview HTTP accesible en desktop, mobile e iPad.
- Home completa.
- Catálogo con 12 a 15 vehículos.
- Filtros y sorting operativos.
- Ficha individual operativa.
- WhatsApp incluye marca/modelo/año o identificador del vehículo.
- Compartir historia genera placa 9:16 usable.
- Contacto/showroom operativo o claramente demo.
- No quedan textos, labels, rutas visibles ni branding de inmobiliaria.
- No aparece Roggero & Roma ni información de ese cliente.
- No hay botones principales muertos.
- Build aprobado.
- Lint/typecheck aprobado o fallos preexistentes documentados con evidencia.
- Preview/deploy verificado con output real.

## 18. Criterios de aceptación P1

- Login requerido para acceder al módulo interno.
- Existe admin de vehículos funcional.
- Existe vista interna de stock con búsqueda, filtros y resumen de pendientes.
- Se puede crear y editar un vehículo.
- Se puede publicar/despublicar.
- Estados público e interno funcionan por separado.
- Existe sección Interno.
- Existe checklist documental por vehículo.
- Existe historial de mantenimiento CRUD.
- Existe checklist prepublicación.
- Datos económicos y notas internas no aparecen públicamente.
- Una sesión no autenticada no puede acceder a datos internos por UI ni endpoint.
- Al menos dos vehículos demo incluyen información interna ficticia para mostrar el flujo.
- Ningún documento real se usa en el demo.
- La UX interna puede mostrarse desde iPad.
- Build, lint/typecheck y pruebas relevantes pasan.

## 19. Criterios de clonabilidad

- Branding y datos de contacto centralizados.
- Seed demo separado de la UI.
- No hay “Wolfim Motors” hardcodeado de forma dispersa.
- README explica cómo crear un clon para otra concesionaria.
- README lista variables de entorno sin valores.
- Nuevo clon puede configurarse sin tocar la lógica del portal.
- Una concesionaria no comparte base de datos, storage o usuarios con otra por accidente.

## 20. Pruebas mínimas requeridas

Además de build/lint/typecheck:

1. Abrir home, catálogo y una ficha pública.
2. Aplicar al menos dos filtros y un sorting.
3. Probar CTA WhatsApp de un vehículo.
4. Generar una historia 9:16 y verificar que sea legible.
5. Intentar abrir admin sin sesión y confirmar bloqueo.
6. Iniciar sesión con credencial demo configurada fuera del repo.
7. Editar un campo público y verificar reflejo público.
8. Editar una nota/costo interno y confirmar que no se expone públicamente.
9. Abrir la vista interna de stock y probar búsqueda/filtros.
10. Crear una entrada de mantenimiento.
11. Cambiar estado de un documento.
12. Cambiar un ítem del checklist.
13. Buscar públicamente patente, VIN, costo y notas internas y confirmar ausencia.
14. Revisar sitemap/metadata y confirmar ausencia de rutas/datos privados.
15. Verificar responsive en viewport mobile y tablet/iPad.

Si existen tests automatizados, ampliarlos. Si no existen, documentar pruebas manuales con resultados reales.

## 21. Entregables

Web-builder debe entregar:

- proyecto actualizado en su zona local de ownership;
- URL preview;
- ruta absoluta local;
- identificación de repo/carpeta;
- build/lint/typecheck reales;
- resultado de pruebas;
- README actualizado;
- lista de variables requeridas;
- alcance P0/P1 terminado;
- pendientes P2;
- capturas de home, catálogo, ficha pública y módulo interno si el flujo local de handoff las admite.

## 21. Respuesta requerida en el handoff oficial

Crear `response.md` en:

```text
Hermes/Handoffs/vps-to-local/HO-2026-08-03-002/response.md
```

Formato mínimo:

```text
Estado: LISTO / PARCIAL / BLOQUEADO

Proyecto existente:
- Ruta absoluta:
- Repo/carpeta:
- Stack:
- URL previa encontrada:
- Estado inicial verificado:

Trabajo realizado:
- P0 showroom:
- P1 módulo interno:
- Clonabilidad:
- Seguridad/privacidad:

Preview:
- URL:
- Desktop verificado: sí/no
- Mobile verificado: sí/no
- iPad/tablet verificado: sí/no

Funcionalidades públicas:
- Home:
- Catálogo:
- Filtros/sorting:
- Ficha:
- WhatsApp:
- Historia 9:16:
- Contacto:

Módulo interno:
- Login:
- Interno:
- Documentación:
- Mantenimiento:
- Checklist:
- Archivos privados: implementado/diferido

Aislamiento:
- Roggero removido:
- Restos inmobiliarios:
- Datos privados no expuestos:
- DTO/API pública revisada:

Clonabilidad:
- Config central:
- Seed:
- README:
- Variables:

Validación técnica:
- Build:
- Lint:
- Typecheck:
- Tests automatizados:
- Pruebas manuales:

Archivos principales tocados:
- ...

Pendientes P2:
- ...

Bloqueos o decisiones requeridas de Juan:
- ...
```

## 22. Regla de cierre

La tarea no se considera terminada por haber escrito componentes.

Se considera terminada cuando:

- el preview funciona;
- P0 está verificado;
- el módulo P1 privado funciona;
- los datos internos no se exponen;
- el proyecto sigue siendo clonable;
- `response.md` contiene evidencia real de ejecución.
