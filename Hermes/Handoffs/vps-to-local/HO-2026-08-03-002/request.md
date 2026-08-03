---
id: HO-2026-08-03-002
status: ready
from: brain-vps
to: brain-local
project: wolfim
priority: high
depends-on: []
created-at: 2026-08-03T13:05:16-03:00
acknowledge-by: next-local-session
due-at: 2026-08-05T18:00:00-03:00
escalate-after: 36h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — web-builder — demo portal automotriz vendible para Wolfim

## Motivo

`wolfim-growth` dejó un `LOCAL_REQUEST` para construir un demo completo de portal automotriz que Juan pueda mostrar en reuniones comerciales desde iPad/celular.

Fuente obligatoria:

```text
companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-2026-08-03.md
```

Relacionado:

```text
companies/wolfim/research/automotive-portal-plan-2026-08-03.md
```

## Objetivo verificable

Entregar un **demo vendible, completo y navegable** llamado **Wolfim Motors Demo** con preview HTTP verificable en mobile, iPad y desktop.

El entregable prioritario NO es una landing parcial. Tiene que sentirse como producto real de concesionaria:

- home automotriz;
- catálogo de vehículos;
- ficha individual por vehículo;
- contacto/showroom;
- CTA WhatsApp por vehículo;
- generación de historia vertical 9:16 por ficha;
- seed demo de 12 a 15 vehículos ficticios;
- build/deploy verificados con output real.

## Contexto comercial

Wolfim necesita un modelo visible para vender vertical automotriz.

Datos confirmados del request de origen:

- Existe oportunidad comercial con 117 leads de concesionarias en Supabase: `concesionarias_autos`.
- Existe antecedente comercial de Paolini Automotores en:
  `companies/wolfim/Leads/Hots/paolini-automotores/`
- Wolfim ya muestra automotriz como vertical posible y tiene caso visible S&P Cars en el sitio público.
- Juan quiere mostrar el demo en venta presencial con iPad.

## Base técnica sugerida

Fuente disponible en VPS para referencia funcional:

```text
/home/hermes/roggero_backup/
/home/hermes/roggero_backup/data/github/properties.git
```

Stack visto en el request:

- Next.js 14
- MongoDB / Mongoose
- Tailwind
- NextAuth
- Cloudinary
- Google Maps
- PDF
- OpenAI

También existe en ese repo:

```text
car-agency.md
```

## Decisión de ejecución

Priorizar **clon funcional + reconversión automotriz** si la base de Roggero & Roma acelera salida real.

Regla de producto para este handoff:

1. **V0 obligatorio** = sitio público demo completo + catálogo seeded + share-story + contacto.
2. **Admin real** NO bloquea V0. Solo incluirlo en esta primera entrega si reutilizarlo desde la base acelera y no retrasa el preview.
3. Si el repo de Roggero sirve, aislarlo en proyecto/repo nuevo y limpiar toda marca, datos y referencias del cliente.
4. Si no sirve o mete deuda fuerte, crear proyecto nuevo con el menor costo posible, pero manteniendo el alcance comercial del demo.

## Restricciones

- No tocar producción de Roggero & Roma.
- No usar datos reales, imágenes reales ni marca real de Roggero & Roma en el demo.
- No exponer credenciales ni leerlas en UI/logs.
- No publicar servicios pagos ni contratar nada externo sin aprobación de Juan.
- El demo debe quedar como **Wolfim Motors Demo** o naming equivalente Wolfim, no como marca cliente real.
- Si se usa fork/copia, dejar claro en README que es demo Wolfim y no proyecto cliente.
- No escribir código ni activos dentro del vault compartido.

## Alcance funcional obligatorio — V0

### 1. Home

Debe incluir:

- hero automotor;
- búsqueda por marca/modelo;
- últimos ingresos o vehículos destacados;
- CTA WhatsApp visible;
- percepción premium y vendible.

### 2. Catálogo `/vehicles` o `/autos`

Debe incluir:

- grid de vehículos;
- filtros por marca, modelo, año, precio, km, combustible, transmisión y carrocería;
- sorting por precio, año o recientes;
- estados visuales: disponible, reservado, vendido.

### 3. Ficha individual

Debe incluir:

- galería;
- precio;
- año, km, combustible, transmisión, carrocería y color;
- equipamiento;
- CTA WhatsApp con mensaje prearmado por vehículo;
- botón **Compartir historia**.

### 4. Contacto / showroom

Debe incluir:

- ubicación ficticia;
- horarios;
- WhatsApp;
- formulario simple si ya viene en la base o se puede montar rápido.

### 5. Datos demo

- 12 a 15 vehículos ficticios.
- Mezcla de 0km y usados.
- Fotos libres o generadas; nunca con patentes visibles.
- Ninguna referencia a propiedades/inmobiliaria.

## Feature obligatoria — Compartir historia

En cada ficha debe existir botón **Compartir historia** con este comportamiento:

- genera placa vertical 9:16;
- incluye foto del vehículo;
- incluye marca/modelo/año;
- incluye precio;
- incluye CTA;
- incluye logo Wolfim / branding demo;
- incluye QR o link a la ficha;
- en mobile/iPad intenta Web Share API / share sheet nativo;
- fallback: descargar imagen si no hay share nativo compatible.

No prometer autopublicación directa a historias. Eso queda fuera del MVP.

## Mapeo funcional esperado

| Base inmobiliaria | Portal automotriz |
|---|---|
| Property | Vehicle |
| Properties page | Vehicles / autos page |
| City/type/operation filters | Brand/model/year/price/km filters |
| Beds/baths/area icons | Year/km/fuel/transmission/body icons |
| Property detail | Vehicle detail |
| Property admin | Stock admin |
| WhatsApp property CTA | WhatsApp vehicle CTA |
| Valuation CTA | Trade-in / tomar usado CTA |
| Google Maps property | Showroom location |

## Criterios de aceptación

- Preview HTTP accesible en desktop, mobile e iPad.
- Se percibe como sitio completo, no como landing o maqueta.
- No quedan textos, labels ni estructuras visibles de inmobiliaria.
- No aparece Roggero & Roma ni datos de ese cliente.
- Hay catálogo con al menos 12 autos visibles.
- Hay filtros operativos.
- Hay ficha individual por auto.
- WhatsApp arma mensaje con marca/modelo/año del vehículo.
- Cada ficha permite generar/compartir una historia 9:16.
- Visualmente se percibe como concesionaria premium, no inmobiliaria reciclada.
- Build/deploy verificados con output real.

## Pasos concretos para web-builder

1. Leer el `LOCAL_REQUEST` completo.
2. Inspeccionar si la base de Roggero acelera realmente el V0.
3. Elegir una de estas rutas y justificarla:
   - **Ruta A:** clonar/aislar base existente y reconvertirla.
   - **Ruta B:** proyecto nuevo con componentes mínimos y seed demo.
4. Construir el preview funcional sin tocar producción de Roggero.
5. Verificar build, lint/typecheck y preview real.
6. Dejar documentado qué quedó listo para venta presencial y qué no.

## Respuesta esperada en este handoff

Crear `response.md` en esta carpeta con este formato mínimo:

```text
Estado: LISTO / PARCIAL / NO LISTO

Ruta elegida:
- A (clon/reconversión) / B (proyecto nuevo)
- Justificación breve:

Proyecto:
- Ruta absoluta local:
- Repo o carpeta creada:
- Stack usado:

Preview:
- URL preview:
- Verificado en desktop: sí / no
- Verificado en mobile/iPad: sí / no

V0 entregado:
- Home: sí / no
- Catálogo: sí / no
- Ficha individual: sí / no
- WhatsApp por vehículo: sí / no
- Share story 9:16: sí / no
- Contacto/showroom: sí / no
- Seed de 12-15 autos: sí / no

Admin:
- Incluido en esta entrega: sí / no
- Si no: qué faltó y por qué

Limpieza de base:
- Marca Roggero removida: sí / no
- Restos de inmobiliaria: sí / no
- Riesgos detectados:

Validación técnica:
- Build: ok / falla
- Lint/typecheck: ok / falla
- Deploy/preview: ok / falla

Pendientes antes de vender a cliente real:
- ...
```

## Nota estratégica

La prioridad de este handoff es **mostrar producto y cerrar venta**. Si hay trade-off entre perfección técnica y demo vendible hoy, priorizar demo vendible hoy, siempre sin romper la limpieza de marca ni dejar algo engañoso.