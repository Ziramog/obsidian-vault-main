# Analytics Setup — Wolfim

**Estado:** Pendiente
**Prioridad:** Alta (incluirlo desde el launch o migración)
**Responsable:** web-builder (configuración) + Antigravity (implementación técnica)

---

## Paso 1 — Google Analytics 4

1. Crear propiedad GA4 en [analytics.google.com](https://analytics.google.com/)
2. Configurar data stream Web con URL del sitio
3. Copiar Measurement ID (G-XXXXXXXX)
4. Verificar flujo de datos con Realtime report

**Entregable:** Measurement ID para conectar con GTM y sitio

---

## Paso 2 — Google Tag Manager

1. Crear contenedor Web en [tagmanager.google.com](https://tagmanager.google.com/)
2. Copiar snippet GTM (código `<script>` + `<noscript>`) para instalar en el sitio
3. Configurar variables:
   - `{{Click URL}}`
   - `{{Click Text}}`
   - `{{Click Element}}`
4. Crear etiqueta Google Analytics: GA4 Event + Measurement ID
5. Crear disparadores (triggers):

| Trigger | Tipo | Evento |
|---|---|---|
| click_whatsapp | Click - Solo enlaces | Cuando URL contiene "wa.me" o "whatsapp.com" |
| click_phone | Click - Solo enlaces | Cuando URL contiene "tel:" |
| form_submit | Envío de formulario | Todos los formularios |
| click_maps | Click - Solo enlaces | Cuando URL contiene "maps.google" o "maps.app" |
| download_pdf | Click - Solo enlaces | Cuando URL contiene ".pdf" |
| scroll_75 | Scroll | 75% de profundidad |

6. Publicar contenedor

**Entregable:** Contenedor GTM publicado

---

## Paso 3 — Google Search Console

1. Agregar propiedad (URL del sitio) en [search.google.com/search-console](https://search.google.com/search-console/)
2. Verificar propiedad mediante:
   - Método recomendado: registro TXT en DNS
   - Alternativa: snippet HTML en el `<head>`
3. Conectar con GA4 (propiedad > Ajustes > Asociaciones de plataforma > Google Search Console)

**Entregable:** Propiedad verificada + asociación con GA4

---

## Paso 4 — Looker Studio

1. Ir a [lookerstudio.google.com](https://lookerstudio.google.com/)
2. Crear fuente de datos: GA4
3. Crear segunda fuente de datos: Search Console
4. Armar dashboard con páginas:

### Página 1 — Resumen mensual
- Gráfico: Visitantes vs Sesiones (línea, últimos 30 días)
- Tarjetas: Usuarios totales, Sesiones, Duración promedio, Tasa de rebote
- Filtro de fecha

### Página 2 — Canales de tráfico
- Gráfico de torta: Sesiones por canal (Organic, Direct, Referral, Social)
- Tabla: Canales × Usuarios × Sesiones × Tasa de conversión

### Página 3 — Eventos y conversiones
- Tabla: Evento × Recuento total
- Destacar: click_whatsapp, form_submit, click_phone
- Timeline diario de eventos

### Página 4 — SEO
- Tabla: Consultas × Impresiones × Clics × CTR × Posición promedio
- Gráfico: Posición promedio por consulta (barras)
- Destacar consultas con posición < 10

### Página 5 — Páginas populares
- Tabla: Ruta de página × Vistas × Usuarios × Tiempo en página
- Top 10 por vistas

### Página 6 — Recomendaciones
- Métricas de Sheets (leads reales, consultas calificadas)
- Observaciones del mes
- Acciones realizadas
- Recomendaciones para el próximo mes

**Entregable:** Dashboard compartible vía enlace (sin necesidad de cuenta Google para verlo)

---

## Paso 5 — Google Sheets (capa manual)

Crear plantilla en Sheets con columnas:

| Mes | Leads totales | Consultas calificadas | Visitas a lote | Interesados calientes | Ventas cerradas | Observaciones | Acciones realizadas | Recomendaciones |
|---|---|---|---|---|---|---|---|---|

Conectar al dashboard de Looker Studio como fuente de datos adicional.

---

## Paso 6 — Implementación en el sitio (Antigravity)

**Prompt resumido para Antigravity:**

```
Objetivo: Instalar GTM + configurar eventos de medición en el sitio de Wolfim.

Contexto: Sitio web existente (HTML/WordPress). Ya tenemos container GTM creado.

Tarea:
1. Agregar snippet de GTM al <head> y después del <body> en todas las páginas
2. Verificar que GTM loader.js carga sin errores
3. Los eventos se configuran desde GTM (no código), pero verificar que:
   - Los botones de WhatsApp tienen href="https://wa.me/..." o clase identificable
   - Los links de teléfono tienen href="tel:..."
   - El formulario tiene un <form> con action o id
   - Los links a Google Maps son reconocibles
   - Los PDFs tienen enlaces que terminan en .pdf
4. Si faltan atributos data o clases para que GTM los identifique, agregarlos

Restricciones: No modificar diseño ni layout. Solo agregar snippets y atributos data- si hace falta.
```

---

## Checklist de verificación

- [ ] GA4 recibiendo datos en Realtime
- [ ] GTM publicado y snippet instalado
- [ ] Search Console verificada + asociada a GA4
- [ ] Dashboard de Looker Studio armado y compartible
- [ ] Sheets creado con plantilla de leads
- [ ] Eventos de prueba disparándose (usar Preview de GTM)
- [ ] Enlace del dashboard enviado al cliente
