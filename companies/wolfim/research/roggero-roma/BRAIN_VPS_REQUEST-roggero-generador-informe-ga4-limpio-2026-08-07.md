---
type: BRAIN_VPS_REQUEST
company: wolfim
client: roggero-roma
target: brain-vps
owner: wolfim-growth
created: 2026-08-07
priority: high
status: pending
---

# Roggero & Roma — corregir generador mensual GA4 de forma permanente

## Motivo

El generador histórico mezcló métricas crudas de GA4 con filtros parciales:

- los totales generales incluían sesiones de autenticación, hosting/previews y panel administrativo;
- algunas tablas públicas ocultaban rutas admin, pero usuarios, sesiones, vistas, fuentes, países, dispositivos y horarios seguían saliendo de consultas crudas;
- el informe podía ocultar fuentes técnicas en la tabla y mantenerlas dentro del total;
- se sumaban `totalUsers` de varias URLs de filtros, duplicando personas;
- se comparaban métricas anteriores crudas con métricas actuales depuradas.

Esto produjo cifras internamente inconsistentes y una lectura confusa para el cliente.

## Artefacto auditado de referencia

Generador validado:

`companies/wolfim/research/roggero-roma/generate_roggero_analytics_auditado_final_2026-08-07.py`

Preset específico validado:

`companies/wolfim/research/roggero-roma/wolfim_report_preset_auditado.py`

PDF verificado:

`companies/wolfim/research/roggero-roma/roggero_roma_informe_analytics_auditado_final_2026-07-07_2026-08-06.pdf`

## Cambio requerido

Actualizar o reemplazar el generador mensual canónico de Roggero & Roma para que use una única metodología.

### 1. Filtro limpio común

Aplicar el mismo filtro a todas las consultas client-facing:

- excluir fuentes de autenticación y hosting/previews;
- excluir rutas `/admin` y `/superadmin`;
- excluir títulos administrativos como `Admin`, `Panel de Control` y `Editar Propiedad`;
- no mezclar resultados crudos y filtrados en el mismo informe.

El filtro debe aplicarse a:

- usuarios;
- sesiones;
- vistas;
- engagement y rebote;
- fuentes;
- países;
- dispositivos;
- horarios;
- páginas y propiedades;
- eventos comerciales.

### 2. Totales client-facing

Mostrar únicamente la base depurada:

- usuarios medidos;
- sesiones depuradas;
- vistas depuradas;
- páginas por sesión calculadas con vistas y sesiones del mismo filtro;
- engagement calculado con el mismo filtro.

No mostrar fuentes técnicas ni mantenerlas escondidas dentro del total.

### 3. Filtros de propiedades

No sumar `totalUsers` entre URLs.

Para cada filtro, ejecutar una consulta agregada independiente con `pagePathPlusQueryString CONTAINS <valor>` y obtener usuarios únicos para ese conjunto.

Aclarar que una persona puede aparecer en más de una categoría si usó distintos filtros.

### 4. Comparaciones entre períodos

No comparar métricas con metodologías diferentes.

Si se muestran números anteriores y actuales:

- aplicar exactamente el mismo filtro a ambos períodos;
- usar períodos consecutivos y sin solapamiento;
- verificar la misma cantidad de días.

El informe anterior `2026-06-08` a `2026-07-07` y el actual `2026-07-07` a `2026-08-06` comparten el 07/07. No usar esa combinación para una comparación numérica directa.

### 5. Eventos client-facing

Incluir únicamente eventos comprensibles y trazables:

- fichas de propiedades vistas;
- clics de WhatsApp;
- futuros eventos explícitos de búsqueda, filtros y contacto.

No incluir:

- `form_start`;
- nombres técnicos de eventos como subtítulos;
- afirmaciones de consultas o leads basadas únicamente en clics.

### 6. Presentación

- usar español en países y etiquetas;
- no mostrar ubicación incorrecta de Wolfim;
- evitar tablas partidas o títulos truncados a mitad de palabra;
- no afirmar “visitantes reales” de forma absoluta;
- no mostrar comparaciones “antes” si la metodología no es homogénea.

## Valores de aceptación para 2026-07-07 a 2026-08-06

Con el filtro auditado utilizado el 2026-08-07:

| Métrica | Valor esperado |
|---|---:|
| Usuarios medidos | 89 |
| Sesiones depuradas | 138 |
| Vistas depuradas | 916 |
| Google orgánico | 60 sesiones |
| Páginas por sesión | 6,64 |
| Engagement rate | 58,7% |
| Vistas desde Argentina | 888 |
| Casa | 28 personas / 215 vistas |
| Venta | 21 personas / 105 vistas |
| Terreno | 6 personas / 28 vistas |
| Fichas vistas | 67 |
| Clics de WhatsApp | 3 |

Estos valores sirven como prueba de regresión para confirmar que el generador canónico reproduce la versión auditada.

## Pruebas obligatorias

1. Generar el PDF para el período de aceptación.
2. Verificar que las métricas coincidan con la tabla anterior.
3. Extraer texto del PDF y confirmar ausencia de:
   - fuentes técnicas;
   - `form_start`;
   - `property_viewed` como etiqueta visible;
   - totales crudos;
   - comparaciones anteriores incompatibles.
4. Confirmar que filtros y propiedades no estén partidos entre páginas.
5. Ejecutar `profile-write-check.py` sobre archivos destinados a otros profiles.

## Seguridad

- No registrar IDs, tokens, claves ni contenido de credenciales en documentación o logs.
- Referenciar cualquier credencial únicamente como `[credencial: NOMBRE_VARIABLE]`.

## Cierre esperado

Brain-vps debe confirmar:

- generador canónico actualizado;
- comando o cron que lo utiliza;
- ejecución de la prueba de regresión;
- ruta del PDF de prueba;
- resultado del chequeo de texto y maquetación.
