---
id: HO-2026-07-06-001
status: ready
from: brain-vps
to: brain-local
project: wolfim
priority: high
depends-on: []
created-at: 2026-07-06T20:35:00-03:00
acknowledge-by: next-local-session
due-at: 2026-07-07T20:00:00-03:00
escalate-after: 48h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff: potenciar `/inmobiliarias` para campaña Meta → WhatsApp

## Objetivo verificable

Potenciar `https://www.wolfim.com/inmobiliarias` para que deje de vender solo “portal inmobiliario” y venda el producto real completo:

> **Portal inmobiliario premium + CRM/panel de mando para inmobiliarias**

Debe apoyar una campaña Meta Ads con WhatsApp directo a dueños de inmobiliarias. El caso modelo es `https://roggeroyroma.com`.

## Contexto comercial

La campaña Meta PyME genérica hacia `/diagnostico` generó 117 visitas y 0 leads reales. Se pausa. Nueva estrategia:

1. Meta Ads con objetivo Mensajes / WhatsApp.
2. Público: dueños/directores de inmobiliarias.
3. El anuncio muestra capacidades reales del producto.
4. WhatsApp abre conversación con Juan.
5. `/inmobiliarias` funciona como prueba de autoridad y detalle comercial después del primer contacto.

No implementar campaña ni publicar ads. Solo mejorar la página.

## Fuentes obligatorias

Hacer fetch/inspección antes de editar:

- `https://www.wolfim.com/inmobiliarias`
- `https://roggeroyroma.com`

Assets de referencia copiados en este handoff:

- `assets/home.png` — home inmersiva con buscador principal.
- `assets/destacadas.png` — propiedades destacadas + métricas.
- `assets/buscador.png` — buscador y grilla de propiedades.
- `assets/mapas.png` — vista mapa.
- `assets/clientes.png` — logos/clientes + prueba social.
- `assets/reseñas.png` — tablero/reseñas Google.
- `assets/panel.png` — panel de control interno.
- `assets/Edit.png` — edición/carga de propiedad.
- `assets/presupuestos.png` — emisión de propuesta/presupuesto.
- `assets/perfil.png` — perfil/configuración/plan.

## Mensaje de posicionamiento

### Antes
“Página web para inmobiliarias / portal con catálogo”.

### Ahora
“Sistema comercial para inmobiliarias: web premium pública + panel privado para administrar propiedades, generar consultas y operar desde el móvil”.

## Cambios solicitados

### 1. Hero más fuerte

Reemplazar/reforzar headline con una promesa más completa:

```text
Portal inmobiliario premium con CRM y panel de mando
```

Subheadline sugerido:

```text
Mostrá tus propiedades con calidad premium, recibí consultas por WhatsApp por cada inmueble y administrá tu catálogo desde un panel propio: agregar, editar, quitar propiedades y generar presupuestos desde el móvil.
```

CTA principal:

```text
Quiero un portal para mi inmobiliaria
```

CTA secundario:

```text
Ver caso Roggero & Roma
```

Mantener estilo Wolfim: editorial, fondo claro/off-white, negro, tipografía actual, sin nuevos colores innecesarios.

### 2. Nueva sección: “Dos partes del sistema”

Dividir el producto claramente:

#### A. Web pública premium
- home inmersiva con imagen/video
- catálogo visual
- fichas individuales
- buscador/filtros
- mapas
- reseñas de Google
- WhatsApp por propiedad
- SEO por ficha

#### B. Panel privado / CRM inmobiliario
- tablero de mando
- agregar, editar y quitar propiedades
- cargar fotos de alta calidad
- administrar destacadas
- emitir presupuestos/fichas desde móvil
- gestionar información comercial
- preparar enlaces compartibles por WhatsApp

### 3. Nueva sección visual con capturas reales

Crear un bloque tipo “Producto real en funcionamiento” o “Así se ve el sistema”.

Usar las capturas del handoff como cards/galería, no como imágenes gigantes sin contexto. Cada card debe tener título + beneficio.

Orden recomendado:

1. `home.png` — “Primera impresión premium”
2. `buscador.png` — “Buscador y catálogo propio”
3. `destacadas.png` — “Propiedades destacadas”
4. `mapas.png` — “Ubicación y mapas”
5. `reseñas.png` — “Reseñas de Google integradas”
6. `panel.png` — “Panel de control”
7. `Edit.png` — “Carga y edición de propiedades”
8. `presupuestos.png` — “Presupuestos desde móvil”

### 4. Nueva sección: “No es solo una web”

Copy sugerido:

```text
No es solo una web institucional. Es una herramienta comercial para ordenar propiedades, elevar la percepción de marca y convertir visitas en consultas concretas por WhatsApp.
```

Bullets:
- Menos consultas desordenadas.
- Más confianza antes del primer mensaje.
- Propiedades mejor presentadas.
- Equipo con control para actualizar el catálogo.
- Fichas listas para compartir con interesados.

### 5. Caso Roggero & Roma más potente

La sección actual del caso está bien pero queda corta. Reforzar con:

- screenshot hero/catálogo del caso
- “modelo real en producción”
- métricas visibles si salen de la web: propiedades, años, reseñas (no inventar; si los números no cargan o no son fiables, no mostrarlos como dato duro)
- link externo al caso

Copy:

```text
Roggero & Roma no recibió una plantilla genérica. Recibió un portal inmobiliario propio: catálogo, fichas, WhatsApp por propiedad, reseñas, mapas y administración interna.
```

### 6. Pricing / oferta

Mantener precio actual salvo instrucción explícita de Juan:

```text
Desde USD 450 + USD 39/mes
```

Pero cambiar nombre del plan a algo más fuerte:

```text
Portal + CRM Inmobiliario
```

Agregar aclaración:

```text
El alcance final depende de cantidad de propiedades, integraciones, carga inicial y nivel de automatización requerido.
```

### 7. CTA WhatsApp con mensaje específico

Usar mensaje:

```text
Hola Wolfim, tengo una inmobiliaria y quiero ver cómo podría quedar un portal con catálogo, panel y WhatsApp por propiedad.
```

## Restricciones

- No cambiar global branding de Wolfim.
- No romper otras páginas.
- No prometer “más ventas garantizadas”.
- No inventar métricas ni resultados comerciales.
- No publicar cambios sin build/verificación local.
- Si el repo no tiene estas imágenes, copiarlas desde `assets/` al lugar correcto del proyecto y optimizarlas si hace falta.

## Criterios de aceptación

- `/inmobiliarias` comunica claramente “portal + CRM/panel”, no solo “web”.
- La página usa capturas reales del producto/caso.
- Hay CTA visible a WhatsApp con mensaje específico.
- Mobile se ve bien.
- Build/lint pasan.
- Se informa en response.md: archivos tocados, URL local/prod si aplica, capturas antes/después y comandos ejecutados.
