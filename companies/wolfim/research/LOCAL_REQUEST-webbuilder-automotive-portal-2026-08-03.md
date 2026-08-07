---
owner: wolfim-growth
status: pending-brain-vps
created: 2026-08-03
type: LOCAL_REQUEST
company: Wolfim
target: brain-vps-to-web-builder
priority: high
related-plan: companies/wolfim/research/automotive-portal-plan-2026-08-03.md
related-addendum: companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-internal-stock-addendum-2026-08-07.md
---

# LOCAL_REQUEST — Demo portal automotriz Wolfim

## Pedido

Crear un demo completo y vendible de portal para concesionarias de autos, clonando Roggero & Roma como base funcional completa si brain-vps/web-builder lo valida técnicamente, igual que el criterio usado para Farias.

No se pide una landing parcial. Se pide un sitio modelo completo llamado **Wolfim Motors Demo** para que Juan lo muestre con el iPad en reuniones comerciales.

## Contexto comercial

Wolfim ya muestra automotriz como vertical posible y tiene caso visible S&P Cars en el sitio público.

También existe una oportunidad comercial concreta:

- 117 leads de concesionarias en Supabase: `concesionarias_autos`.
- Paolini Automotores ya tuvo borrador de propuesta en `companies/wolfim/Leads/Hots/paolini-automotores/`.
- Juan necesita mostrar un sitio modelo mientras vende.

## Base técnica sugerida

Fuente disponible en VPS:

- Backup de Roggero & Roma: `/home/hermes/roggero_backup/`
- Git mirror: `/home/hermes/roggero_backup/data/github/properties.git`
- Rama principal: `main`
- Stack visto en `package.json`: Next.js 14, MongoDB/Mongoose, Tailwind, NextAuth, Cloudinary, Google Maps, PDF, OpenAI.
- Documento existente en repo: `car-agency.md`, con especificación de vehicle schema y páginas.

Criterio de ejecución pedido por Juan:

- Clonar proyecto completo.
- Aislarlo en repo/proyecto demo nuevo.
- Limpiar marca, datos y referencias de Roggero.
- Transformarlo a **Wolfim Motors Demo**.
- Adecuarlo a agencia de autos, no a inmobiliaria.

Usar esa base como punto de partida funcional completo, no como clon visual final.

## Restricciones

- No usar datos reales, imágenes reales ni marca de Roggero & Roma en el demo.
- No tocar producción de Roggero & Roma.
- No exponer credenciales ni leerlas en UI/logs.
- El demo debe usar marca ficticia o marca Wolfim: propuesta inicial `Wolfim Motors Demo`.
- Si se usa fork/copia, dejar claro en el README que es demo Wolfim y no proyecto cliente.
- No publicar cambios pagos ni contratar servicios externos sin aprobación de Juan.

## Alcance V0 — Sitio completo demo vendible

Entregable prioritario: link público o preview que Juan pueda mostrar desde iPad/celular como producto real.

Páginas requeridas:

1. Home
   - Hero automotor.
   - Búsqueda por marca/modelo.
   - Últimos ingresos.
   - CTA WhatsApp.

2. Catálogo `/vehicles` o `/autos`
   - Grid de vehículos.
   - Filtros por marca, modelo, año, precio, km, combustible, transmisión y carrocería.
   - Sorting por precio, año o recientes.

3. Ficha individual
   - Galería.
   - Precio.
   - Año, km, combustible, transmisión, carrocería, color.
   - Equipamiento.
   - WhatsApp por vehículo con mensaje prearmado.
   - Botón “Compartir historia” para generar una imagen vertical 9:16 del auto.

4. Contacto/showroom
   - Ubicación ficticia.
   - Horarios.
   - WhatsApp y formulario simple.

Datos demo:

- 12 a 15 vehículos ficticios.
- Mezcla de 0km y usados.
- Fotos libres o generadas, sin patentes visibles.
- Estados: disponible, reservado, vendido.

Feature social requerida:

- En cada ficha, botón “Compartir historia”.
- Debe generar una placa 9:16 con foto del vehículo, marca/modelo/año, precio, CTA, logo y QR/link a la ficha.
- En mobile/iPad, intentar compartir vía Web Share API usando el share sheet nativo.
- Fallback: descargar imagen si Instagram/Facebook no están disponibles como destino.
- No prometer autopublicación directa a historias; eso requiere permisos/API nativa y queda fuera del MVP.

## Alcance V1 — Producto vendible a cliente real

Agregar:

- Login admin.
- Alta/edición/baja de vehículos.
- Publicar/despublicar.
- Marcar reservado/vendido.
- Subida múltiple de imágenes.
- SEO por ficha.
- Sitemap.
- Analytics básico.
- Guía de uso para concesionaria.
- Ficha interna privada por vehículo con notas, documentación, estado técnico y checklist prepublicación.
- Separación estricta entre datos públicos y datos privados.

## Alcance V2 — Portal operativo interno

Agregar si el cliente lo justifica:

- Historial de mantenimiento por vehículo.
- Documentación adjunta por unidad.
- Costos de preparación y margen objetivo.
- Alertas de vencimientos de VTV/RTO/documentación.
- Roles/permisos para admin, vendedor y preparación/taller.
- Reportes de stock y tareas pendientes.

## Mapeo funcional

| Roggero & Roma | Portal automotriz |
|---|---|
| Property | Vehicle |
| Properties page | Vehicles/autos page |
| City/type/operation filters | Brand/model/year/price/km filters |
| Beds/baths/area icons | Year/km/fuel/transmission/body icons |
| Property detail | Vehicle detail |
| Property admin | Stock admin |
| WhatsApp property CTA | WhatsApp vehicle CTA |
| Valuation CTA | Trade-in / tomar usado CTA |
| Google Maps property | Showroom location |

## Criterios de aceptación V0

- Link público accesible en mobile, iPad y desktop.
- Se percibe como sitio completo, no como landing o maqueta.
- No quedan textos de propiedades/inmobiliaria.
- No aparece Roggero & Roma ni datos de ese cliente.
- Hay catálogo con al menos 12 autos visibles.
- Hay filtros operativos.
- Hay ficha individual por auto.
- El botón WhatsApp arma mensaje con marca/modelo/año del vehículo.
- Cada ficha permite generar/compartir una historia 9:16 del vehículo.
- Visualmente se percibe como concesionaria premium, no inmobiliaria reciclada.
- Build/deploy verificado con output real.

## Criterios de aceptación V1

- Admin permite cargar y editar vehículos.
- Carga de imágenes funciona.
- Publicar/despublicar funciona.
- Estado disponible/reservado/vendido funciona.
- SEO/sitemap incluye fichas de vehículos.
- Analytics básico mide vista de ficha y click WhatsApp.
- Guía de uso entregada.

## Preguntas de implementación para brain-vps/web-builder

1. ¿Conviene forkear el repo de Roggero o crear repo nuevo copiando solo módulos?
2. ¿El demo sale en subdominio `autos.wolfim.com`, `demo-autos.wolfim.com` o preview Vercel?
3. ¿V0 incluye admin real o se prioriza catálogo público con seed mock?

## Recomendación de wolfim-growth

Priorizar clon completo + reconversión automotriz.

La necesidad inmediata de Juan es vender con un modelo visible y completo. Un demo parcial sirve menos para venta presencial; con iPad conviene mostrar home, catálogo, ficha y admin/panel como si fuera una concesionaria real.
