# Dashboard Looker Studio — Roggero & Roma

## Configuración general
- **Fuente 1:** Google Analytics 4 (propiedad roggeroyroma.com.ar)
- **Fuente 2:** Google Search Console (cuando esté activo)
- **Fuente 3:** Google Sheets (leads manuales)
- **Rango de fechas:** Últimos 28 días (con selector de fecha)
- **Filtro global:** Excluir tráfico de data centers (Council Bluffs, Warsaw, Aspen, Boardman)

---

## Página 1 — Resumen Mensual

| Elemento | Tipo | Dimensión/Métrica | Filtro |
|---|---|---|---|
| Título "Resumen Mayo 2026" | Texto | — | — |
| Fecha: selector | Control de rango | — | — |
| Tarjeta 1 | Scorecard | Usuarios activos | — |
| Tarjeta 2 | Scorecard | Nuevos usuarios | — |
| Tarjeta 3 | Scorecard | Engagement promedio | — |
| Tarjeta 4 | Scorecard | Eventos totales | — |
| Gráfico tendencia | Serie temporal (línea) | Fecha × Usuarios activos | — |
| Tabla resumen | Tabla | Fuente/medio × Sesiones × Usuarios × Tasa de rebote | — |

**Calculated field:**
```
Usuarios reales = Usuarios activos - COUNTIF(Ciudad IN LIST("Council Bluffs", "Warsaw", "Aspen", "Boardman"))
```

---

## Página 2 — Tráfico

| Elemento | Tipo | Dimensión/Métrica |
|---|---|---|
| Gráfico canales | Torta/Dona | Primer source/medio × Usuarios |
| Tabla canales | Tabla | Source/medio × Sesiones × Usuarios × Nuevos usuarios |
| Gráfico timeline | Serie temporal | Fecha × Sesiones (coloreado por source) |

---

## Página 3 — Contenido

| Elemento | Tipo | Dimensión/Métrica |
|---|---|---|
| Tabla páginas | Tabla con barra | Título de página × Vistas × Usuarios × Eventos × Bounce rate |
| Filtro | Control desplegable | Excluir "Admin —" del título |
| Top propiedades | Gráfico de barras | Título de página × Vistas |
| (filtro: solo propiedades individuales, excluir "Inicio" y "Propiedades ·" general) |

---

## Página 4 — SEO
*(cuando Search Console esté conectado)*

| Elemento | Tipo | Dimensión/Métrica |
|---|---|---|
| Tabla consultas | Tabla | Consulta de Google × Clics × Impresiones × CTR × Posición |
| Gráfico barras | Barras | Consulta × Posición (ordenado por clics) |
| Tarjeta | Scorecard | Clics totales de Google |
| Tarjeta | Scorecard | Impresiones totales |
| Tarjeta | Scorecard | CTR promedio |
| Tarjeta | Scorecard | Posición promedio |

---

## Página 5 — Leads (capa manual)

| Elemento | Tipo | Fuente |
|---|---|---|
| Tabla leads | Tabla | Sheets: Mes, Leads totales, Consultas calificadas, Visitas, Ventas |
| Gráfico tendencia | Barras | Mes × Leads totales + Consultas calificadas |
| Tarjeta | Scorecard | Total leads del período |
| Sección texto | Texto | Observaciones + Recomendaciones (desde Sheets) |

---

## Página 6 — Recomendaciones

| Elemento | Tipo |
|---|---|
| Título "Recomendaciones para [mes+1]" | Texto grande |
| Checklist visual | Texto con viñetas (desde Sheets o manual) |
| Acciones realizadas | Texto (desde Sheets) |

---

## Cómo crear los calculated fields clave

### Tasa de engagement
```
Tasa engagement = Usuarios activos / Eventos totales
```

### Promedio diario
```
Promedio diario = Usuarios activos / DAYS(Rango fin - Rango inicio)
```

### % Tráfico orgánico
```
% Orgánico = COUNT(Cuando source = "google") / COUNT(Todos) * 100
```
(mejor hacer esto en el gráfico de torta directamente)

---

## Compartir
1. Click en "Share" → "Enable link sharing"
2. Opción: "Anyone with the link can view"
3. Copiar enlace y enviar al cliente

---

## Notas
- Para la fuente de Google Sheets, necesitás publicar la sheet: File → Share → Publish to web → CSV
- Looker Studio actualiza cada ~12h por defecto. Se puede forzar refresco manual
- Si el cliente no tiene cuenta de Google, igual puede ver el dashboard con el link (solo lectura)
