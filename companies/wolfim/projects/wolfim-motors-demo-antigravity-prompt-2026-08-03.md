---
company: Wolfim
project: wolfim-motors-demo
status: ready-for-antigravity
created: 2026-08-03
source-handoff: HO-2026-08-03-002
execution-route: A-hybrid
preview-target: vercel-public-preview
---

# Wolfim Motors Demo — prompt para Antigravity

## Decisión técnica

Se eligió **Ruta A híbrida**: exportar de forma segura la base de Roggero & Roma, reutilizar solo su arquitectura y componentes útiles, y reconstruir el dominio público como portal automotor desacoplado de MongoDB, Cloudinary, Auth y datos de cliente. El admin real queda fuera de V0.

Base inspeccionada: `C:\Projects\property-pulse-nextjs`.
Destino aprobado: `C:\Projects\wolfim-motors-demo`.
Deploy aprobado: **Vercel Preview público**, nunca producción en esta fase.

## Prompt listo para copiar/pegar

```text
OBJETIVO

Construir y desplegar un demo público, completo y vendible de portal automotriz llamado “Wolfim Motors Demo”, usando una copia aislada de la base Next.js existente, pero reemplazando por completo el dominio inmobiliario, la marca y la infraestructura de cliente. El resultado debe poder mostrarse desde celular, iPad y desktop como un producto real de concesionaria.

No entregues un plan ni una landing parcial. Implementá el V0 completo, ejecutá build y QA real, desplegá un Vercel Preview público y devolvé evidencia concreta.

CONTEXTO DEL PROYECTO

Equipo Windows.

Base técnica de referencia, solo lectura:
- Ruta absoluta: C:\Projects\property-pulse-nextjs
- Stack confirmado: Next.js 14.2.4 App Router, React 18, Tailwind CSS 3, JavaScript/JSX.
- La base contiene catálogo, filtros, fichas, galería, responsive y panel admin inmobiliario.
- Al momento de la auditoría estaba en rama `preview` y tenía `.hermes/` sin trackear. Volvé a verificar el estado antes de copiar.
- La base conserva acoplamiento fuerte a `Property`, `/properties`, MongoDB/Mongoose, NextAuth, Cloudinary, mapas y marca Roggero & Roma.
- Hay hardcodes de marca, dominio, teléfonos, emails, GA4, Cloudinary y contenido inmobiliario. Ninguno puede sobrevivir en el demo.
- No modificar ni desplegar la base original.

Proyecto destino:
- Ruta obligatoria: C:\Projects\wolfim-motors-demo
- La ruta no existía al momento de la auditoría. Si ahora existe, inspeccioná su contenido antes de tocarla y no pises trabajo ajeno.
- Nombre del proyecto y marca pública: Wolfim Motors Demo.
- Contacto comercial configurable: WhatsApp Wolfim `5493513157202` mediante una única configuración, nunca repetido en componentes.
- El sitio es una demostración conceptual: los vehículos, precios, showroom y datos comerciales son ficticios.

DECISIÓN DE ARQUITECTURA — RUTA A HÍBRIDA

1. Crear una copia/exportación aislada desde `C:\Projects\property-pulse-nextjs` hacia `C:\Projects\wolfim-motors-demo`.
2. No copiar `.git`, `.env`, `.env.*`, `node_modules`, `.next`, `.vercel`, `.hermes`, caches, capturas, videos, auditorías, migraciones ni activos/datos reales del cliente.
3. Preferir exportar solo archivos trackeados y necesarios; inicializar un repo local nuevo en el destino. No crear repo GitHub salvo que sea estrictamente necesario y no reutilizar remotes del proyecto original.
4. Verificar antes y después que `C:\Projects\property-pulse-nextjs` conserva exactamente el mismo `git status` y no fue modificado.
5. Reutilizar únicamente primitives útiles: estructura Next.js, layout, responsive, patrones de catálogo/card/galería, loading y utilidades genéricas.
6. Para V0, eliminar la dependencia de MongoDB, Mongoose, NextAuth, Cloudinary, Google Maps, reseñas, mensajes, propuestas/PDF y panel admin. No alcanza con ocultar links: las rutas y imports runtime no deben interferir con build ni preview.
7. El catálogo V0 debe funcionar desde un seed local data-driven. El admin real queda documentado como V1 y no debe retrasar esta entrega.

TAREA ESPECÍFICA

FASE 0 — AISLAMIENTO Y LIMPIEZA SEGURA

- Inspeccionar estado Git, scripts y estructura de la fuente.
- Crear el destino aislado con las exclusiones anteriores.
- Cambiar `package.json` a `wolfim-motors-demo`.
- Remover dependencias que queden realmente sin uso; conservar `qrcode` para la historia 9:16.
- Crear `.env.example` sin valores sensibles. Como mínimo:
  - `NEXT_PUBLIC_SITE_URL=`
  - `NEXT_PUBLIC_DEMO_WHATSAPP=5493513157202`
- Crear README explícito: “Demo comercial de Wolfim Studio. No es una concesionaria real ni un proyecto cliente”.
- Crear `ASSETS.md` con origen/licencia/atribución de cada fotografía incorporada.
- No copiar ninguna credencial ni leer/imprimir valores de `.env` de la fuente.

FASE 1 — MODELO DE DATOS Y SEED

Crear una única fuente local, por ejemplo `data/vehicles.js`, con 15 vehículos ficticios. No duplicar cards a mano.

Modelo mínimo por vehículo:
- `id`
- `slug`
- `brand`
- `model`
- `version`
- `year`
- `kilometers`
- `fuel`
- `transmission`
- `bodyType`
- `color`
- `condition`: `0km` o `usado`
- `status`: `disponible`, `reservado` o `vendido`
- `priceArs`
- `priceUsd` opcional
- `featured`
- `images`
- `equipment`
- `description`
- `createdAt`

Seed:
- 15 unidades.
- Mezcla de Toyota, Volkswagen, Ford, Chevrolet, Renault y Fiat.
- Mezcla de hatchback, sedán, SUV y pickup.
- Mezcla de 0km y usados.
- Incluir los tres estados comerciales.
- Datos y precios plausibles pero claramente demo; no usar patentes, VIN, teléfonos o historias reales.
- Usar fotografías libres o con licencia compatible, descargadas al proyecto para evitar CORS y canvas contaminado. Revisar visualmente que no muestren patentes legibles.
- Cada vehículo debe tener galería operativa. Se pueden reutilizar algunas tomas de interior/detalle si la licencia lo permite, pero cada cover debe corresponder visualmente al tipo de vehículo.

FASE 2 — SISTEMA VISUAL ORIGINAL

No conservar la estética de inmobiliaria ni copiar branding de BMW u otra automotriz. Tomar solo principios de diseño automotor premium: precisión, fotografía protagonista, geometría limpia y ritmo dark/light.

Dirección:
- Full-bleed automotive hero con fotografía oscura y legible.
- Tipografía: Space Grotesk para display, Inter para UI/cuerpo y JetBrains Mono para datos técnicos. Usar `next/font` o fuentes locales.
- Sin serif inmobiliaria, sin Cormorant/PT Serif, sin naranja heredado de Roggero.
- Paleta sugerida:
  - fondo oscuro `#0B0D10`
  - superficie `#16191D`
  - blanco cálido `#F5F5F2`
  - texto claro `#F7F8FA`
  - texto secundario `#A6ADB8`
  - acento interactivo `#2F6BFF`
  - disponible `#2DAA68`
  - reservado `#F2A93B`
  - vendido `#68707C`
- Acento solo en CTA, foco y estados; no usar gradientes decorativos genéricos.
- Geometría mayormente recta, radios contenidos de 0–8 px. Evitar glassmorphism y colecciones de tarjetas redondeadas tipo template IA.
- Fotografía y tipografía deben sostener la percepción premium.
- Motion breve y funcional; respetar `prefers-reduced-motion`.
- Contraste AA, foco visible, navegación por teclado y labels reales.

FASE 3 — RUTAS PÚBLICAS

Implementar como mínimo:

1. `/` — Home
- Header responsive con wordmark textual/original “Wolfim Motors Demo”.
- Navegación: Inicio, Stock, 0km, Usados, Showroom.
- Hero automotor con búsqueda por marca/modelo y CTA “Ver stock”.
- Últimos ingresos y unidades destacadas.
- Accesos a 0km, usados, SUV y pickups.
- Bloque comercial “Tomamos tu usado” como CTA demostrativo, sin tasación falsa.
- Bloque de confianza sin inventar años, ventas, financiación aprobada ni garantías. Usar beneficios de producto: “Stock ordenado”, “Ficha por unidad”, “Consulta directa”.
- CTA WhatsApp visible.
- Footer con aviso “Demo comercial de Wolfim Studio — datos y vehículos ficticios”.

2. `/autos` — Catálogo
- Grid responsive con las 15 unidades.
- Búsqueda por marca/modelo/versión.
- Filtros operativos por marca, modelo, año, rango de precio, km máximo, combustible, transmisión, carrocería, condición y estado.
- Sorting por precio ascendente/descendente, año y recientes.
- Estado de filtros sincronizado con query string.
- Conteo de resultados, chips activos y acción “Limpiar filtros”.
- Drawer de filtros usable en mobile/iPad.
- Cards con cover, marca/modelo/versión, año, km, transmisión, precio y badge de estado.
- `vendido` sigue visible pero con CTA comercial adaptado; nunca presentarlo como disponible.
- Empty state útil.

3. `/autos/[slug]` — Ficha individual
- `generateStaticParams` desde el seed local.
- Galería accesible y usable con touch.
- Marca, modelo, versión, año y estado.
- Precio ARS; USD solo cuando exista.
- Km, combustible, transmisión, carrocería y color.
- Equipamiento.
- Descripción comercial.
- Vehículos similares.
- CTA WhatsApp con mensaje exacto basado en la unidad: “Hola, vi el [marca] [modelo] [versión] [año] en Wolfim Motors Demo. ¿Está disponible?”.
- Botón principal “Compartir historia”.
- Metadata y OpenGraph específicos por vehículo.

4. `/contacto` — Showroom
- Datos ficticios y visualmente creíbles, con microcopy visible “Datos demostrativos”.
- Dirección ficticia que no se presente como ubicación real de Wolfim.
- Horarios.
- WhatsApp.
- Formulario simple opcional solo si tiene comportamiento real: puede validar y preparar una consulta en WhatsApp. No mostrar éxito si no se realizó ninguna acción.
- No usar Google Maps ni API keys en V0; usar un bloque editorial de ubicación/showroom.

FASE 4 — FEATURE “COMPARTIR HISTORIA”

Crear un componente reutilizable, por ejemplo `StoryShareButton`, en cada ficha.

Comportamiento obligatorio:
1. Generar en browser una imagen PNG real de 1080 × 1920 px.
2. Incluir:
   - foto principal con crop controlado;
   - marca, modelo, versión y año;
   - precio;
   - badge de estado;
   - CTA “Conocé esta unidad”;
   - branding “Wolfim Motors Demo”;
   - QR que apunte a la URL pública exacta de la ficha.
3. Usar `qrcode`, ya disponible en la base, y Canvas API o una solución local estable. Evitar dependencias innecesarias.
4. Las imágenes deben ser same-origin/locales para no romper la exportación del canvas.
5. Convertir a `Blob`/`File` con nombre estable, por ejemplo `wolfim-motors-toyota-corolla-2022-story.png`.
6. En HTTPS mobile/iPad:
   - comprobar `navigator.share`;
   - comprobar `navigator.canShare({ files })` cuando exista;
   - abrir el share sheet nativo con el PNG.
7. Fallback obligatorio: descargar el PNG.
8. Nunca prometer publicación automática en Instagram/Facebook.
9. Mostrar estados “Generando…”, éxito/fallback y error recuperable.
10. Verificar por código o prueba automatizada que el PNG generado mide exactamente 1080 × 1920.

FASE 5 — CONFIGURACIÓN, SEO Y SEGURIDAD DEL DEMO

- Centralizar nombre, WhatsApp, email demo, horarios, showroom y URL base en un único config.
- No dejar datos de Roggero/Roma, Farias ni otro cliente en código, assets, metadata, comentarios, docs o UI.
- Eliminar GA4/Pixel heredados; no medir con IDs de clientes.
- No usar MongoDB, Cloudinary, Blob, OAuth, Google Maps, OpenAI ni servicios pagos en V0.
- No incluir secretos.
- `robots` debe dejar el demo fuera de indexación: `noindex, nofollow` y robots.txt coherente. Es un demo comercial ficticio, no una concesionaria real.
- Sitemap puede incluir las rutas demo para QA, pero no debe contradecir el noindex.
- Agregar favicon/OG propios y originales del demo.
- Todos los links externos con `rel="noopener noreferrer"` cuando corresponda.
- Agregar hooks estables (`data-event`, `data-location`, `data-vehicle`) a WhatsApp, filtros y share-story, sin afirmar que analytics está configurado.

ARCHIVOS A TOCAR / CREAR EN EL DESTINO

La estructura final puede variar, pero probablemente incluya:
- `package.json`
- `app/layout.jsx`
- `app/page.jsx`
- `app/autos/page.jsx`
- `app/autos/[slug]/page.jsx`
- `app/contacto/page.jsx`
- `app/robots.js`
- `app/sitemap.js`
- `assets/styles/globals.css`
- `config/site.js`
- `data/vehicles.js`
- `components/automotive/*`
- `components/StoryShareButton.jsx`
- `public/images/vehicles/*`
- `public/images/brand/*`
- `.env.example`
- `README.md`
- `ASSETS.md`

Eliminar o dejar fuera del runtime final las rutas/módulos inmobiliarios heredados:
- `/properties`
- `/admin`
- `/superadmin`
- `/messages`
- `/profile`
- `/p/[token]`
- mapas, reseñas, quotations/PDF, subscribers, Mongo models, Auth y actions/APIs de propiedades.

RESTRICCIONES

- No modificar `C:\Projects\property-pulse-nextjs`.
- No tocar ni desplegar Roggero & Roma.
- No copiar `.git`, env vars, DB, usuarios, assets, reseñas, propiedades, contactos ni credenciales del cliente.
- No reutilizar el remote GitHub `Ziramog/properties`.
- No reutilizar proyectos Vercel de Roggero, Farias o Wolfim principal.
- No desplegar con `--prod`; solo Vercel Preview.
- No comprar servicios ni activar APIs pagas.
- No crear admin falso que parezca funcional. El admin queda para V1.
- No dejar botones muertos.
- No usar imágenes con patentes legibles.
- No copiar logos o identidad visual de automotrices; los nombres de marcas/modelos se usan solo como datos ficticios de catálogo.
- No sacrificar mobile/iPad por desktop.

VERIFICACIÓN OBLIGATORIA

Antes del deploy:
1. Instalar dependencias en el destino.
2. Ejecutar `npm run lint` si el script existe y es compatible.
3. Ejecutar `npx tsc --noEmit` si la configuración lo permite.
4. Ejecutar `npm run build`; debe terminar con exit code 0.
5. Ejecutar el build o servidor local y verificar con browser real:
   - desktop 1440 × 900;
   - iPad 1024 × 1366;
   - mobile 390 × 844.
6. Probar:
   - home;
   - catálogo con múltiples combinaciones de filtros y sorting;
   - acceso directo a una ficha;
   - WhatsApp con marca/modelo/versión/año;
   - generación de PNG 1080 × 1920;
   - fallback de descarga;
   - share nativo cuando el navegador lo soporte;
   - contacto/showroom;
   - navegación mobile;
   - sin overflow horizontal;
   - sin CTA fijo tapando controles;
   - sin imágenes rotas;
   - consola sin errores nuevos.
7. Hacer un scan amplio, excluyendo solo dependencias/build, y exigir cero referencias críticas a:
   - Roggero / Roma / Silvia;
   - `roggeroyroma.com.ar`;
   - `properties-srs5.vercel.app`;
   - inmobiliaria / propiedad / properties en UI/runtime;
   - teléfonos/emails/direcciones anteriores;
   - `dunkbcery`;
   - `property_pulse_unsigned`;
   - `G-PW4FH9WHQB`;
   - imágenes/logos de R&R o Farias.
8. Confirmar que la fuente original conserva el mismo `git status`.

DEPLOY VERCEL PREVIEW PÚBLICO

Con build y QA local aprobados:
- Usar la sesión Vercel ya autenticada; nunca pedir, imprimir ni guardar tokens.
- Crear o vincular un proyecto Vercel nuevo y exclusivo llamado `wolfim-motors-demo`.
- Confirmar antes del deploy que no apunta a ningún proyecto existente de cliente.
- Ejecutar deploy de Preview, no producción. No usar `--prod`.
- La URL debe ser pública y abrir en incógnito sin login de Vercel.
- Volver a probar en la URL pública: `/`, `/autos`, una ficha, `/contacto`, filtros, WhatsApp y generación/descarga/share de historia.
- Si la CLI no está autenticada o Vercel bloquea el preview público, reportar el bloqueo exacto; no improvisar credenciales ni afirmar que quedó desplegado.

CRITERIOS DE ACEPTACIÓN

- Existe `C:\Projects\wolfim-motors-demo` como proyecto aislado.
- La fuente Roggero permanece intacta.
- Home, catálogo, ficha y contacto/showroom funcionan.
- Hay exactamente 15 vehículos ficticios visibles desde una única fuente de datos.
- Todos los filtros y sort funcionan y se reflejan en URL.
- WhatsApp identifica la unidad concreta.
- Cada ficha genera un PNG real de 1080 × 1920 con foto, datos, precio, CTA, branding y QR.
- Web Share API funciona donde está disponible y descarga funciona como fallback.
- No hay rastros de inmobiliaria ni datos/infraestructura de Roggero/Farias.
- No depende de DB, Auth, Cloudinary, Maps ni servicios pagos.
- Se percibe como concesionaria premium, no como inmobiliaria reciclada ni template IA genérico.
- Build aprobado con output real.
- QA aprobado en mobile, iPad y desktop.
- Vercel Preview público accesible en incógnito.
- No hubo deploy de producción.

FORMATO DE RESPUESTA FINAL

Devolvé un reporte corto y factual:

Estado: LISTO / PARCIAL / NO LISTO

Proyecto:
- Ruta absoluta:
- Fuente original intacta: sí/no
- Repo local nuevo: sí/no

V0:
- Home:
- Catálogo y filtros:
- Ficha individual:
- WhatsApp por vehículo:
- Share story 9:16:
- Contacto/showroom:
- Seed de 15 autos:
- Admin V0: no, diferido a V1

Validación:
- `npm run lint`:
- `npx tsc --noEmit`:
- `npm run build`:
- Desktop:
- iPad:
- Mobile:
- Consola:
- Scan de referencias antiguas:

Vercel:
- Proyecto nuevo:
- URL Preview pública:
- Verificada en incógnito:
- Producción modificada: no

Pendientes reales:
- Solo lo que efectivamente no haya podido verificarse.
```
