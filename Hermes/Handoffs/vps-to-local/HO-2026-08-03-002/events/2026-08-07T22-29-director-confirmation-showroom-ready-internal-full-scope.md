---
type: event
id: HO-2026-08-03-002
status: director-confirmed-full-execution
from: brain-vps
to: brain-local
created-at: 2026-08-07T22:29:12-03:00
priority: high
director: Juan
acknowledge-by: next-local-session
---

# Evento — showroom confirmado listo + ejecución completa del módulo interno

## Confirmación de Juan

Juan confirmó expresamente:

- el showroom público está **LISTO**;
- no debe tratarse P0 como trabajo pendiente ni como bloqueo;
- web-builder debe avanzar **a fondo y sin freno** sobre el módulo interno privado.

Esta confirmación supersede cualquier instrucción anterior que exigiera completar o revalidar el showroom antes de comenzar P1.

El showroom solo debe recibir pruebas de regresión para asegurar que los cambios internos no rompan catálogo, fichas, filtros, WhatsApp o Compartir historia. No rediseñar ni reabrir P0.

## Foco activo único

Construir un módulo interno privado sólido para que el producto pueda venderse como:

> Showroom público listo + sistema interno para ordenar stock, documentación, mantenimiento, preparación y datos económicos por vehículo.

No entregar una demo superficial del módulo. El resultado debe servir como base real clonable para una concesionaria.

## Autonomía de web-builder

Web-builder queda autorizado a resolver sin esperar nuevas aprobaciones las decisiones técnicas reversibles y sin costo necesarias para completar el módulo, incluyendo:

- arquitectura interna dentro del proyecto existente;
- modelo de datos;
- rutas privadas;
- componentes y navegación;
- validaciones;
- migraciones no destructivas;
- seeds ficticios;
- tests;
- nombres técnicos y tipos de campos;
- UX de desktop y tablet/iPad;
- refactors necesarios para separar correctamente DTO público y modelo privado.

Para decisiones menores, usar defaults razonables, implementarlos y documentarlos. No frenar el avance esperando aprobación estética o de naming interno.

## Alcance obligatorio — módulo interno completo

### 1. Acceso y seguridad

- Login real.
- Logout real.
- Rutas y endpoints privados protegidos del lado servidor o por el mecanismo seguro del stack existente.
- Una sesión anónima no puede leer ni mutar información interna.
- Credenciales fuera del repo y del vault.
- Sin datos privados en HTML público, payloads públicos, metadata, sitemap, JSON-LD, historias 9:16 o logs de analytics.

### 2. Vista interna de stock

Crear una vista de operación, no solo fichas aisladas.

Columnas mínimas:

- código interno;
- vehículo;
- patente/dominio;
- fecha de ingreso;
- días en stock;
- ubicación;
- estado interno;
- resumen documental;
- mantenimiento/tareas pendientes;
- responsable;
- acción para abrir la ficha.

Búsqueda y filtros mínimos:

- código interno;
- marca/modelo;
- patente;
- VIN;
- estado interno;
- documentación incompleta;
- mantenimiento pendiente;
- responsable;
- ubicación.

Agregar contadores simples por estado: a revisar, en preparación, listo para publicar, publicado, reservado, vendido y entregado.

### 3. Ficha privada por vehículo

Organizar como tabs, secciones o navegación equivalente:

1. `Ficha pública`
2. `Interno`
3. `Documentación`
4. `Mantenimiento`
5. `Checklist`

La UX debe funcionar en desktop y ser revisable/operable desde iPad.

### 4. Datos internos y económicos

Incluir y persistir como mínimo:

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
- costo de compra o toma;
- margen objetivo;
- precio mínimo aceptable.

Los campos económicos, identificación registral, estado técnico y notas son privados por defecto.

### 5. Documentación

Implementar checklist documental por vehículo con:

- tipo;
- estado;
- observación;
- fecha de emisión opcional;
- fecha de vencimiento opcional;
- nombre de archivo o referencia opcional.

Tipos mínimos:

- título;
- cédula;
- formulario 08;
- informe de dominio;
- verificación policial;
- libre deuda;
- VTV/RTO;
- factura o boleto;
- comprobantes de service;
- garantía;
- manuales;
- otros.

Estados mínimos:

- faltante;
- pendiente;
- recibido;
- verificado;
- no aplica.

#### Archivos privados

Si el proyecto ya cuenta con almacenamiento privado seguro y reversible, implementar carga de PDF/imágenes con acceso autenticado y URL temporal/firmada.

Si requiere contratar un servicio, habilitar un bucket pago o incorporar una credencial que Juan todavía no suministró, no improvisar ni exponer archivos. Dejar el modelo y la interfaz preparados y registrar exactamente el bloqueo en `response.md`.

No se aceptan enlaces públicos ocultos como sustituto de almacenamiento privado.

### 6. Mantenimiento y preparación

Implementar CRUD completo de entradas internas con:

- fecha;
- tipo;
- descripción;
- estado;
- costo;
- proveedor/taller;
- notas.

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

Estados:

- pendiente;
- en progreso;
- realizado;
- cancelado.

### 7. Checklist prepublicación

Incluir:

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

Mostrar progreso simple. No bloquear automáticamente la publicación salvo que la arquitectura existente lo permita de forma segura y clara.

### 8. Operación del vehículo

El módulo debe permitir:

- crear vehículo;
- editar vehículo;
- publicar/despublicar;
- cambiar estado público;
- cambiar estado interno por separado;
- editar datos privados sin filtrar esos cambios al público;
- mantener al menos dos unidades demo completas con información interna ficticia.

### 9. Clonabilidad

Mantener la estrategia de un proyecto/deploy aislado por concesionaria.

Centralizar:

- branding;
- contacto;
- dominio/base URL;
- moneda;
- SEO por defecto;
- configuración de storage y auth;
- estados y defaults del módulo interno cuando corresponda.

Actualizar README con:

- instalación;
- variables requeridas sin valores secretos;
- migraciones;
- seed demo;
- procedimiento de clonado;
- rollback si se modifica persistencia.

## Mejoras P1+ autorizadas si no requieren gasto ni frenan el núcleo

Web-builder puede incorporar directamente si encajan naturalmente en la arquitectura:

- indicadores de documentación vencida o próxima a vencer;
- alertas visuales internas;
- orden por días en stock;
- historial básico de cambios con fecha;
- resumen de costos de preparación;
- exportación simple CSV del stock interno;
- estados y badges operativos.

No convertir el sprint en CRM, contabilidad, multi-tenancy o sistema de facturación.

## Protección de datos y migraciones

Antes de modificar esquema o persistencia:

1. identificar dónde viven los datos actuales;
2. conservar los vehículos demo existentes;
3. realizar backup/export si hay riesgo de modificación;
4. preferir migraciones aditivas y reversibles;
5. documentar migración y rollback;
6. no compartir DB, storage o usuarios entre concesionarias;
7. no usar datos reales de Roggero & Roma ni de otra empresa.

## Únicos motivos válidos para frenar y escalar

Web-builder no debe detenerse por decisiones técnicas menores.

Debe escalar solamente si aparece alguno de estos casos:

- gasto o contratación de servicio;
- acción irreversible o migración destructiva sin rollback seguro;
- necesidad de usar datos reales de cliente;
- credencial faltante imprescindible;
- publicación en producción o dominio real;
- contradicción directa con ownership o con una decisión de Juan.

Mientras eso no ocurra, avanzar y decidir.

## Validación obligatoria

Además de build, lint y typecheck:

1. abrir admin sin sesión y confirmar bloqueo;
2. iniciar sesión con credencial demo configurada fuera del repo;
3. abrir vista interna de stock y probar búsquedas/filtros;
4. crear o editar un vehículo;
5. editar un campo público y verificar el resultado público;
6. editar costo, VIN y nota interna y confirmar que no aparecen públicamente;
7. crear, editar y eliminar una entrada de mantenimiento;
8. cambiar el estado de un documento;
9. cambiar ítems del checklist;
10. revisar endpoints y payloads públicos;
11. revisar sitemap, metadata y JSON público;
12. probar viewport desktop, mobile y tablet/iPad;
13. ejecutar regresión del showroom público sin rediseñarlo.

Si no existen tests automatizados, documentar pruebas manuales con resultados reales. Si existen, ampliarlos para cubrir auth y separación pública/privada.

## Respuesta requerida

Crear:

```text
Hermes/Handoffs/vps-to-local/HO-2026-08-03-002/response.md
```

Debe incluir:

- ruta absoluta del proyecto;
- URL preview;
- estado inicial encontrado;
- arquitectura del módulo interno;
- funcionalidades implementadas;
- migraciones y rollback;
- aislamiento público/privado verificado;
- build, lint, typecheck y tests reales;
- pruebas manuales realizadas;
- archivos principales tocados;
- estado de clonabilidad;
- mejoras P1+ incorporadas;
- pendientes reales;
- bloqueos que requieran decisión de Juan.

## Definition of Done vigente

El showroom se considera confirmado por Juan y no es el entregable pendiente.

El handoff queda terminado cuando:

- el módulo interno funciona de extremo a extremo;
- la vista de stock sirve operativamente;
- la ficha privada reúne interno, documentación, mantenimiento y checklist;
- auth y aislamiento están verificados;
- no se filtran datos privados;
- las migraciones son seguras y documentadas;
- la UX es utilizable desde iPad;
- el proyecto sigue siendo clonable;
- existe `response.md` con evidencia real.

## Instrucción final a brain-local

Derivar este handoff a web-builder en la próxima sesión local. No pedir una nueva definición de alcance: la dirección ya fue confirmada por Juan en este evento.
