---
type: event
id: HO-2026-08-03-002
status: scope-change
from: brain-vps
to: brain-local
created-at: 2026-08-07T22:11:36-03:00
priority: high
director: Juan
---

# Evento — actualización de alcance: módulo interno privado

Juan informó que el showroom automotriz ya está aproximadamente 90% funcional y es clonable.

El `LOCAL_REQUEST` fue revisado y consolidado como fuente operativa vigente:

```text
companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-2026-08-03.md
```

## Cambio de alcance

El handoff ya no debe interpretarse como “crear un demo desde cero”.

Brain-local debe derivar a web-builder para:

1. localizar y continuar el proyecto existente;
2. cerrar y verificar el showroom público P0;
3. desarrollar el módulo interno privado mínimo P1 por vehículo;
4. mantener el proyecto clonable por concesionaria;
5. verificar que ningún dato interno se exponga en rutas, APIs, metadata, sitemap o JSON público.

## Módulo P1 requerido

- sección Interno;
- registro/checklist de documentación;
- historial de mantenimiento/preparación;
- checklist prepublicación;
- campos económicos y notas privadas;
- autenticación real;
- al menos dos vehículos demo con datos internos ficticios;
- UX revisable desde iPad.

La carga binaria de documentos puede diferirse si no existe almacenamiento privado seguro. No se aceptan archivos sensibles detrás de enlaces públicos ocultos.

## Regla de continuidad

No iniciar otro clon ni reconstruir la aplicación salvo bloqueo técnico demostrado.

El request original del handoff permanece inmutable. Este evento agrega el alcance actualizado y remite al `LOCAL_REQUEST` consolidado.

## Respuesta requerida

Brain-local/web-builder debe crear `response.md` en este mismo handoff con:

- ruta del proyecto existente;
- URL preview;
- estado P0 y P1;
- build/lint/typecheck/tests reales;
- prueba de aislamiento público/privado;
- estado de clonabilidad;
- pendientes P2;
- bloqueos o decisiones requeridas de Juan.
