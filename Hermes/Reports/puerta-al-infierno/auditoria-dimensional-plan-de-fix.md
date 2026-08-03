# Auditoría dimensional — Puerta al Infierno

**Estado:** diagnóstico y plan; todavía sin modificar el PDF.
**Fuente de verdad:** plano de la hoja `Dimensionamiento de referencia` del anexo V5.

## 1. Error confirmado

Las fichas intercambian cotas horizontales y verticales:

| Fila actual | Valor actual | Orientación real en el plano | Corrección |
|---|---:|---|---|
| Altura máxima general | 14,033 m | Horizontal — ancho/desarrollo máximo superior | **Altura máxima general = 11,919 m** |
| Altura de referencia secundaria | 13,033 m | Horizontal — ancho/desarrollo superior secundario | **Altura de referencia secundaria = 11,618 m** |
| Desarrollo horizontal mayor | 11,919 m | Vertical — altura máxima | **Desarrollo horizontal mayor = 14,033 m** |
| Desarrollo horizontal secundario | 11,618 m | Vertical — altura secundaria | **Desarrollo horizontal secundario = 13,033 m** |

## 2. Matriz canónica leída del plano

### Cotas horizontales

| Nombre prudente según geometría | Valor |
|---|---:|
| Desarrollo horizontal máximo superior | 14,033 m |
| Desarrollo horizontal superior secundario | 13,033 m |
| Ancho exterior total en base | 12,260 m |
| Luz interior entre apoyos en base | 10,156 m |
| Ancho del núcleo inferior | 4,147 m |
| Ancho del núcleo superior | 3,993 m |

### Cotas verticales

| Nombre prudente según geometría | Valor |
|---|---:|
| Altura máxima general | 11,919 m |
| Altura de referencia secundaria | 11,618 m |
| Altura de referencia lateral superior | 9,160 m |
| Altura de referencia interior | 7,901 m |
| Altura lateral inferior | 7,555 m |
| Altura parcial del coronamiento | 3,717 m |

## 3. Otras etiquetas problemáticas

| Etiqueta actual | Valor | Problema | Etiqueta propuesta |
|---|---:|---|---|
| Cota lateral superior | 12,260 m | El plano la muestra horizontal en la base | Ancho exterior total en base |
| Cota lateral interior | 10,156 m | El plano la muestra horizontal entre apoyos | Luz interior entre apoyos en base |
| Profundidad / eje de referencia | 9,160 m | No es profundidad: la cota es vertical | Altura de referencia lateral superior |
| Referencia interior | 7,901 m | Es una cota vertical | Altura de referencia interior |
| Desarrollo inferior | 7,555 m | No es desarrollo horizontal: la cota es vertical | Altura lateral inferior |
| Cota superior parcial | 3,717 m | Correcta en orientación, pero demasiado ambigua | Altura parcial del coronamiento |

Las fichas actuales también omiten dos cotas horizontales visibles del núcleo: **3,993 m** y **4,147 m**.

## 4. Plan de corrección

1. **Congelar el plano:** no modificar geometría, trazos ni cotas del plano aprobado.
2. **Crear una matriz única de dimensiones:** usar las 12 cotas anteriores como fuente común para todas las fichas.
3. **Rehacer la ficha de “B. Descripción formal y dimensional”:**
   - separar `Cotas verticales` y `Cotas horizontales`;
   - corregir los cuatro valores invertidos;
   - renombrar las filas ambiguas;
   - incorporar 3,993 m, 4,147 m y 3,717 m.
4. **Rehacer la ficha junto al plano:** usar la misma matriz, en formato compacto, sin volver a interpretar valores manualmente.
5. **Mantener observaciones prudentes:** describir función geométrica; no afirmar estructura definitiva ni profundidad inexistente.
6. **Actualizar el PDF integrado:** sustituir únicamente las dos fichas; conservar plano, propuesta institucional y resto del anexo.
7. **Verificación obligatoria:**
   - comparar cada fila contra la orientación de la línea de cota del plano;
   - comprobar que ambas fichas sean idénticas en nombre y valor;
   - renderizar las hojas corregidas y revisar legibilidad, clipping y orden visual;
   - verificar que el resto del PDF permanezca sin cambios.

## 5. Criterio de aceptación

- Altura máxima: **11,919 m**.
- Desarrollo horizontal máximo: **14,033 m**.
- Ninguna cota horizontal debe llamarse altura.
- Ninguna cota vertical debe llamarse desarrollo horizontal o profundidad.
- Las dos fichas deben derivar de una sola matriz y coincidir fila por fila.
