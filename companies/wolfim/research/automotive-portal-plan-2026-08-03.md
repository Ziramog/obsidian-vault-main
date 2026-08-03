---
owner: wolfim-growth
status: draft-for-juan
created: 2026-08-03
company: Wolfim
vertical: automotive
source:
  - companies/wolfim/intelligence/context.md
  - companies/wolfim/intelligence/patterns.md
  - companies/wolfim/Leads/index.md
  - companies/wolfim/Leads/Hots/paolini-automotores/propuesta.md
  - roggero_backup GitHub mirror main:car-agency.md
---

# Plan portal automotriz Wolfim — 2026-08-03

## Decisión ejecutiva

Sí: conviene clonar Roggero & Roma completo como punto de partida, igual que el criterio usado para Farias, y después adecuarlo a agencia de autos.

La idea correcta no es hacer una landing parcial: es tener un sitio completo **Wolfim Motors Demo** para mostrar con el iPad en reuniones comerciales. Se clona la estructura funcional completa y se transforma el motor de catálogo inmobiliario en un motor de catálogo automotor:

- `propiedades` → `vehículos`
- búsqueda por ciudad/tipo/operación → búsqueda por marca/modelo/año/precio/km
- ficha inmobiliaria → ficha técnica del auto
- WhatsApp por propiedad → WhatsApp por vehículo
- panel inmobiliario → panel de stock de la concesionaria
- SEO por propiedad → SEO por unidad y por marca/modelo/localidad

Esto le da a Juan un sitio modelo vendible rápido, apoyado en algo ya probado, y permite activar los 117 leads de concesionarias que ya están identificados en Supabase.

## Problema

Wolfim necesita un sitio modelo de portal para concesionarias que Juan pueda mostrar mientras vende, sin esperar a cerrar un cliente real para construir el primer caso.

## Opciones

### Opción A — Clon completo de Roggero & Roma y adaptación automotriz

Clonar la estructura completa del portal inmobiliario, como se hizo para Farias, y reconvertirla a agencia de autos.

**Pros:**
- Base real ya validada: catálogo, filtros, fichas, panel admin, imágenes, SEO, WhatsApp y analytics.
- Demo más contundente para vender con iPad: no se muestra una maqueta, se muestra un sitio completo.
- Mejor argumento comercial: “esto ya funciona en inmobiliarias; lo adaptamos a stock vehicular”.
- Permite vender portal, no solo landing.
- Acelera porque se reemplaza vertical/contenido en vez de diseñar todo desde cero.

**Contras:**
- Hay que limpiar referencias inmobiliarias y evitar cualquier dato/marca de Roggero.
- Requiere control técnico para no arrastrar complejidad innecesaria.
- Si se copia demasiado el layout, se percibe como plantilla reciclada.
- Hay que separar bien demo y producción para no tocar ni comprometer Roggero & Roma.

### Opción B — Demo estático rápido

Armar una landing/catálogo de autos con datos mockeados y sin panel real.

**Pros:**
- Muy rápido para mostrar.
- Sirve para WhatsApp, reunión presencial o link de venta.
- Bajo riesgo técnico.

**Contras:**
- No demuestra el valor central: panel para cargar autos.
- Puede parecer “otra web linda”, no un sistema comercial.
- Después hay que reconstruir la versión real.

### Opción C — Portal nuevo desde cero

Construir un producto automotor limpio, sin heredar código inmobiliario.

**Pros:**
- Arquitectura más ordenada para escalar a SaaS o multi-concesionaria.
- Evita deuda técnica del proyecto anterior.
- Permite diseñar 100% alrededor de autos.

**Contras:**
- Más lento.
- No responde a la necesidad comercial inmediata de Juan.
- Riesgo de parálisis: se vende menos mientras se diseña el “producto perfecto”.

## Recomendación

Recomiendo la opción A: clonar Roggero & Roma completo, aislarlo como demo Wolfim y después modificarlo fuerte a estética/estructura automotriz.

El objetivo no es “hacer otro Roggero con autos”. El objetivo es tener un **sitio completo de concesionaria modelo** para que Juan lo abra en el iPad y lo use como herramienta de cierre. Tiene que sentirse como producto real, no como wireframe.

## Producto vendible

Nombre interno recomendado: **Wolfim Auto Portal**.

Nombre comercial hacia el cliente: **Salón Virtual para Concesionarias**.

Frase de venta:

> “No reemplaza MercadoLibre ni GTM. Te da una web propia para que tu marca, tu stock y tus consultas no dependan solamente de portales externos.”

## MVP del sitio modelo

### Páginas públicas

1. Home de concesionaria
   - Hero con búsqueda por marca/modelo.
   - CTA directo a WhatsApp.
   - Últimos ingresos.
   - Sección “0km”, “Usados”, “Pickups/SUV”.
   - Bloque de confianza: años, operaciones, financiación, garantía.

2. Catálogo de vehículos
   - Grid de unidades.
   - Filtros por marca, modelo, año, precio, km, combustible, transmisión y carrocería.
   - Orden por precio, año o ingreso reciente.
   - Estados: disponible, reservado, vendido.

3. Ficha individual del vehículo
   - Galería de fotos.
   - Precio ARS y opcional USD.
   - Año, km, combustible, transmisión, carrocería, color.
   - Equipamiento destacado.
   - Botón WhatsApp con mensaje prearmado: “Hola, vi el Toyota Corolla 2020 en la web. ¿Está disponible?”.
   - Botón “Compartir historia” que genere una pieza vertical 9:16 del vehículo para Instagram/Facebook Stories.
   - Vehículos similares.

### Compartir como historia Instagram/Facebook

Sí, es posible como feature comercial, pero hay que implementarlo con criterio realista:

1. **Robusto y universal:** generar una imagen vertical 9:16 por ficha, tipo story card, con foto del auto, marca/modelo/año, precio, CTA, logo de la concesionaria y QR/link a la ficha.
2. **Desde mobile/iPad:** usar Web Share API para abrir el share sheet nativo y que el usuario elija Instagram, Facebook, WhatsApp u otra app instalada.
3. **Fallback seguro:** si el share directo no está disponible, botón “Descargar historia” para que la concesionaria la suba manualmente a IG/FB.
4. **Link real:** Instagram Stories no permite desde web garantizar link sticker automático; se puede incluir QR visual y/o que el usuario agregue el sticker de link manualmente.
5. **No prometer autopublicación:** publicar directo en historias de IG/FB requiere integraciones nativas/API/permisos y no es necesario para el MVP comercial.

Valor comercial: cada vehículo se convierte en pieza lista para redes. Esto es fuerte para concesionarias porque el stock rota y necesitan publicar ingresos rápido sin diseñar una historia manual cada vez.

4. Página institucional simple
   - Quiénes somos.
   - Ubicación/showroom.
   - Horarios.
   - Contacto.

### Panel admin mínimo

1. Login.
2. Alta de vehículo.
3. Edición de vehículo.
4. Publicar/despublicar.
5. Marcar como reservado/vendido.
6. Subida múltiple de imágenes.
7. Vista previa antes de publicar.

### Datos demo

Crear una marca ficticia para evitar problemas: **Wolfim Motors Demo**.

Stock de demo recomendado:

- 12 a 15 vehículos.
- Mezcla de 0km y usados.
- Marcas comunes: Toyota, Volkswagen, Ford, Chevrolet, Renault, Fiat.
- Categorías: hatchback, sedán, SUV, pickup.
- Fotos mockeadas o libres, sin patentes reales visibles.
- Textos de ficha con tono comercial, no técnico pesado.

## Mapeo Roggero & Roma → Autos

| Roggero & Roma | Portal automotriz |
|---|---|
| Propiedad | Vehículo |
| Ciudad / zona | Marca / modelo / sucursal |
| Tipo de propiedad | Carrocería |
| Venta / alquiler | Disponible / reservado / vendido |
| Dormitorios / baños / m² | Año / km / combustible / transmisión |
| Mapa de propiedad | Ubicación del showroom o sucursal |
| Tasación de propiedad | Tomamos tu usado / permuta |
| Propiedades destacadas | Unidades destacadas / últimos ingresos |
| Ficha de propiedad | Ficha técnica del vehículo |
| WhatsApp por propiedad | WhatsApp por unidad |
| Panel de propiedades | Panel de stock |

## Alcance por fases

### Fase 0 — Clon seguro y limpieza

Objetivo: duplicar la base completa sin tocar producción de Roggero & Roma.

Entregables:
- Repo/proyecto demo aislado.
- Variables y credenciales separadas o mockeadas.
- Limpieza total de marca/datos Roggero.
- Confirmación de que el demo no usa datos privados de cliente.

### Fase 1 — Demo completo para vender con iPad

Objetivo: link que Juan pueda mostrar en reuniones y WhatsApp como si fuera un producto real.

Alcance:
- Home completa.
- Catálogo.
- Ficha individual.
- Panel admin heredado/adaptado si el clon lo permite sin fricción.
- Datos mock.
- Diseño premium automotor.
- CTA WhatsApp por vehículo.
- Compartir historia 9:16 por vehículo con Web Share API y fallback descarga.
- Deploy preview o subdominio demo.

Tiempo objetivo: 72 horas técnicas si se reutiliza el clon completo y se prioriza reconversión visual/contenido.

### Fase 2 — Producto entregable a cliente

Objetivo: versión lista para vender como proyecto real.

Alcance:
- Panel admin operativo.
- Carga/edición de vehículos.
- Publicar/despublicar.
- SEO por ficha.
- Sitemap.
- Analytics básico.
- Guía de uso simple para la concesionaria.

Tiempo objetivo: 7 a 10 días de producción técnica.

### Fase 3 — Upsells

Funcionalidades para subir ticket:
- Descripciones IA por vehículo.
- Comparador lado a lado.
- PDF de presupuesto automático.
- Simulador de financiación.
- Importación CSV de stock.
- Integración MercadoLibre/GTM si el cliente lo justifica.
- Reporte mensual de vistas y consultas por unidad.
- Google Ads para “concesionaria + ciudad”, “autos usados + ciudad”, “pickup usada + ciudad”.

## Pricing comercial sugerido

Precios para validar/cerrar con Juan antes de enviar propuesta formal:

| Paquete | Setup sugerido | Mantenimiento | Para quién |
|---|---:|---:|---|
| Presencia + catálogo simple | USD 450 | USD 39/mes | Concesionaria chica con 10-25 unidades |
| Portal concesionaria | USD 650-850 | USD 49-79/mes | Agencia con stock activo y necesidad de panel |
| Portal + growth | USD 900+ | USD 99+/mes | Agencia que quiere SEO, reportes, Ads y automatización |

Regla comercial: no venderlo como “web”. Venderlo como “salón virtual con stock propio y consultas por unidad”.

## Argumento de venta

Dolores a tocar:

1. Tu stock vive repartido entre MercadoLibre, GTM, Instagram, Facebook y WhatsApp.
2. Cada auto nuevo se publica varias veces y se pierde orden.
3. Cuando alguien googlea “concesionaria en [ciudad]”, muchas veces encuentra portales antes que tu marca.
4. El cliente pregunta por WhatsApp sin contexto; con ficha propia consulta por una unidad concreta.
5. Una web propia mejora percepción: no sos solo un perfil en redes, sos una concesionaria con salón digital.

Promesa:

> “Te damos una web propia donde el cliente ve el stock, filtra, entra a la ficha del auto y consulta por WhatsApp con el vehículo ya identificado.”

## Plan comercial con leads existentes

Dato actual: hay 117 leads de concesionarias de autos en Supabase (`concesionarias_autos`) con outreach pendiente.

Secuencia recomendada:

1. Primero producir demo modelo.
2. Seleccionar 10 concesionarias de mayor potencial, idealmente con stock activo pero web floja o dependencia fuerte de portales/redes.
3. Auditar cada una antes de contactar: sitio propio, catálogo, WhatsApp, SEO local, dependencia de MercadoLibre/GTM/Instagram.
4. Contacto de Juan por WhatsApp o presencial si hay cercanía geográfica.
5. Primer mensaje no genérico: mencionar un hallazgo real y ofrecer mostrar “un modelo de salón virtual para concesionarias”.
6. Si responde, mostrar demo y anclar precio desde la conversación: desde USD 450 + mantenimiento.
7. Cierre ideal: 50% para empezar, 50% contra demo funcional/adaptación.

## Mensaje base para Juan

```text
Hola, soy Juan de Wolfim.

Estoy armando portales para concesionarias: una web propia donde se ve el stock, cada auto tiene su ficha y el cliente consulta por WhatsApp por la unidad exacta.

Vi que hoy ustedes muestran autos en [canal/sitio/red] y quería mostrarte un modelo ya armado para agencias de autos.

No reemplaza MercadoLibre ni Instagram: ordena tu marca y tu catálogo en un lugar propio.

¿Te lo paso para que lo veas?
```

Si responde positivo:

```text
Perfecto. La versión base arranca en USD 450 de setup + USD 39/mes de mantenimiento, con catálogo, fichas, WhatsApp por auto, hosting y soporte.

Si querés panel completo para cargar autos sin depender de nadie, lo cotizamos como portal de concesionaria según cantidad de stock y funciones.
```

## Definition of Done del demo

El modelo está listo para vender cuando:

- Juan puede abrir un link público y mostrarlo desde el iPad/celular.
- El sitio se percibe completo: home, catálogo, ficha, contacto y panel/admin visible o demostrable.
- Hay al menos 12 vehículos cargados.
- El catálogo filtra por marca, año, precio, km, combustible y carrocería.
- Cada ficha tiene botón WhatsApp con mensaje por vehículo.
- Cada ficha tiene botón “Compartir historia” y genera una placa 9:16 compartible/descargable.
- Se ve premium y diferente a una plantilla genérica.
- No aparece ninguna marca/dato de Roggero & Roma.
- Hay una captura o mini video para usar en WhatsApp.
- Existe una propuesta corta con precio base y mantenimiento.

## Próxima acción concreta

Escalar el `LOCAL_REQUEST` a brain-vps para que web-builder produzca el demo vendible.

Decisión que necesita Juan: aprobar que el demo salga como **Wolfim Motors Demo** o elegir nombre/marca ficticia distinta.
