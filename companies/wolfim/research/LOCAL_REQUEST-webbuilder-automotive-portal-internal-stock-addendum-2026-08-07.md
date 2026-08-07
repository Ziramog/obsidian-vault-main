---
owner: wolfim-growth
status: pending-brain-vps
type: LOCAL_REQUEST_ADDENDUM
created: 2026-08-07
company: Wolfim
target: brain-vps-to-web-builder
priority: medium
parent-request: companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-2026-08-03.md
related:
  - companies/wolfim/research/automotive-portal-internal-stock-module-2026-08-07.md
  - companies/wolfim/research/automotive-portal-plan-2026-08-03.md
---

# LOCAL_REQUEST_ADDENDUM — módulo interno privado de stock/documentación

## Contexto

Juan propuso ampliar el portal automotriz para que no sea solo showroom público, sino también herramienta interna de la concesionaria.

La idea: cada vehículo debe poder tener una vista pública y una vista privada.

## Pedido para brain-vps/web-builder

No frenar el V0 comercial si ya está en marcha.

Incorporar este concepto como diseño de producto y, si el tiempo técnico lo permite, dejar una primera versión demostrable o estructura preparada.

## Prioridad del desarrollo

### Mantener V0 como prioridad

V0 sigue siendo:

- home;
- catálogo;
- ficha pública;
- WhatsApp por vehículo;
- historia 9:16;
- link público para vender con iPad/celular.

### Agregar en V1/V2

Agregar módulo privado de stock:

- campos internos por vehículo;
- documentación adjunta;
- estado técnico;
- notas internas;
- checklist prepublicación;
- historial de mantenimiento;
- costos o tareas de preparación;
- vencimientos/documentación;
- roles/permisos.

## Requisito de privacidad

Todo lo interno debe estar detrás de login.

No debe aparecer en:

- páginas públicas;
- metadata;
- sitemap;
- SEO;
- JSON público;
- pre-render estático accesible sin auth.

## Campos sugeridos para modelo Vehicle

Además de campos públicos del vehículo, contemplar campos privados como:

```text
internalNotes
internalStatus
purchaseCost
minimumSalePrice
targetMargin
entryDate
stockOrigin
physicalLocation
technicalStatus
maintenanceHistory[]
documents[]
prePublishChecklist
assignedSeller
```

Documentos sugeridos:

```text
title
cedula
formulario08
informeDominio
verificacionPolicial
libreDeuda
vtvRto
serviceReceipts
warranty
manuals
other
```

## UX sugerida

En admin de vehículo:

1. Tab “Ficha pública”.
2. Tab “Interno”.
3. Tab “Documentación”.
4. Tab “Mantenimiento”.
5. Tab “Checklist”.

En la ficha pública no mostrar nada interno.

## Criterio comercial

Esto no debe venderse como software pesado de entrada.

Debe presentarse como evolución del portal:

> Showroom público + ficha interna privada por vehículo para ordenar documentación, mantenimiento y estado del stock.

## Aceptación mínima si se implementa en demo

- En admin existe tab o sección “Interno”.
- Un vehículo demo muestra notas internas/documentación/checklist.
- La ficha pública no muestra esa información.
- El build/deploy sigue funcionando.
- README o notas técnicas aclaran qué quedó implementado y qué queda para V2.
