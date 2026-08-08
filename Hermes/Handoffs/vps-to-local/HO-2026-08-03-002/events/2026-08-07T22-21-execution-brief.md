---
type: event
id: HO-2026-08-03-002
status: execution-brief
from: brain-vps
to: brain-local
created-at: 2026-08-07T22:21:28-03:00
priority: high
director: Juan
---

# Evento — elaboración operativa para web-builder

## Objetivo de esta nota

Este evento no reemplaza el `request.md` original ni el evento de scope change. Los complementa con una secuencia de ejecución más estricta para evitar deriva técnica.

Fuentes obligatorias y orden de prioridad:

1. `companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-2026-08-03.md`
2. `companies/wolfim/research/automotive-portal-internal-stock-module-2026-08-07.md`
3. `Hermes/Handoffs/vps-to-local/HO-2026-08-03-002/request.md`
4. `companies/wolfim/research/automotive-portal-plan-2026-08-03.md`

## Decisión operativa consolidada

No se pide una maqueta nueva.

Se pide:

1. localizar el proyecto existente de `Wolfim Motors Demo`;
2. estabilizar y cerrar el showroom público P0;
3. agregar el módulo interno privado P1 mínimo por vehículo;
4. verificar aislamiento real entre datos públicos y privados;
5. dejar el proyecto listo para clonarse por concesionaria.

## Secuencia obligatoria de ejecución

### Paso 1 — Auditoría inicial del proyecto existente

Antes de tocar código, registrar:

- ruta absoluta del proyecto;
- rama o estado de repo/carpeta;
- preview actual si ya existe;
- páginas/rutas operativas hoy;
- features P0 ya resueltas;
- features P0 incompletas;
- restos visibles de la reconversión inmobiliaria;
- estado real de build, lint, typecheck y tests.

Si el proyecto no aparece, demostrar búsqueda real antes de proponer reconstrucción.

### Paso 2 — Cierre del showroom público P0

El P0 debe quedar vendible para iPad/celular.

Checklist mínimo:

- home automotriz completa;
- catálogo responsive con filtros reales;
- ficha pública por vehículo;
- CTA WhatsApp por unidad;
- historia 9:16 funcionando con share o fallback descarga;
- branding Wolfim Motors Demo consistente;
- 12 a 15 vehículos demo visibles;
- cero restos públicos de inmobiliaria en labels, rutas, metadata, seeds, imágenes o textos.

No reabrir arquitectura por perfeccionismo. Cerrar el 10% restante y estabilizar.

### Paso 3 — Módulo privado P1 por vehículo

Implementar una primera capa privada real, no solo UI escondida.

Mínimo requerido:

- autenticación funcional;
- protección real de rutas privadas;
- ficha admin con secciones `Público`, `Interno`, `Documentación`, `Mantenimiento`, `Checklist`;
- al menos 2 vehículos demo con datos internos ficticios cargados;
- campos privados mínimos:
  - `internalStockCode`
  - `licensePlate`
  - `vin`
  - `engineNumber`
  - `internalNotes`
  - `internalStatus`
  - `entryDate`
  - `stockOrigin`
  - `physicalLocation`
  - `technicalStatus`
  - `assignedSeller`
  - `purchaseCost`
  - `targetMargin`
  - `minimumSalePrice`
- checklist documental con estados;
- historial de mantenimiento/preparación editable;
- checklist prepublicación visible y usable.

La carga binaria de documentos entra solo si ya existe almacenamiento privado seguro reutilizable. Si no, dejarlo documentado como P2. No se aceptan links públicos ocultos simulando privacidad.

### Paso 4 — Auditoría de exposición pública/privada

Validar con evidencia real que los datos internos no aparecen en:

- rutas públicas;
- HTML renderizado público;
- payloads JSON públicos;
- endpoints/API públicos;
- metadata SEO;
- sitemap;
- búsqueda interna pública;
- historia 9:16;
- previews compartibles.

Regla: si una sesión no autenticada puede leer costo, patente, VIN, notas internas o checklist documental, P1 no está listo.

### Paso 5 — Clonabilidad por concesionaria

Dejar centralizado y fácil de reemplazar:

- nombre comercial;
- logo;
- colores;
- WhatsApp;
- email;
- dirección/showroom;
- horarios;
- dominio/base URL;
- moneda;
- textos institucionales;
- SEO por defecto.

Entregar también:

- seed demo;
- instrucciones mínimas de clonado/adaptación;
- lista de variables de entorno requeridas sin valores secretos.

## Criterio de aceptación reforzado

El handoff se considera bien resuelto solo si brain-local/web-builder demuestra con output real:

- preview HTTP accesible;
- build OK;
- lint/typecheck OK o lista explícita de fallas bloqueantes;
- showroom público funcional;
- módulo privado funcional;
- prueba de aislamiento público/privado;
- ruta del proyecto;
- evidencia de clonabilidad;
- pendientes P2 claramente separados de P0/P1.

## Qué NO hacer

- no empezar otro clon porque “queda más prolijo”;
- no rehacer todo desde cero sin bloqueo técnico demostrado;
- no dejar el módulo privado como maqueta falsa;
- no mezclar datos reales de cliente;
- no declarar listo sin pruebas reales;
- no esconder deuda crítica detrás de un preview lindo.

## Formato de respuesta esperado

Además de `response.md`, la respuesta debe distinguir explícitamente:

### Estado general
- `P0 showroom`: LISTO / PARCIAL / NO LISTO
- `P1 interno`: LISTO / PARCIAL / NO LISTO

### Evidencia mínima
- ruta absoluta del proyecto;
- URL preview;
- build;
- lint/typecheck;
- tests si existen;
- auth verificada;
- prueba de acceso anónimo bloqueado a privado;
- prueba de que públicos no filtran privados.

### Producto
- qué puede mostrar Juan hoy en reunión presencial;
- qué falta todavía para venderlo a cliente real sin humo;
- qué queda como P2.

## Cierre ejecutivo

La prioridad no es “hacer software por orgullo técnico”.
La prioridad es que Juan pueda mostrar un portal de concesionaria que:

1. se vea vendible hacia afuera;
2. tenga argumento operativo hacia adentro;
3. no exponga nada privado;
4. se clone rápido para una agencia real.
