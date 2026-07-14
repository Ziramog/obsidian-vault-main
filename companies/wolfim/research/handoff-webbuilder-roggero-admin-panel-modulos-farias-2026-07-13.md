---
title: Handoff WebBuilder — relevar admin panel Roggero & Roma para propuesta Farias
from: wolfim-growth
to: brain-vps / web-builder
company: Wolfim
client_target: Farias & Asociados
reference_project: Roggero & Roma
created: 2026-07-13
status: requested
priority: high
purpose: detallar módulos reales del admin panel desde código para propuesta comercial seria
---

# Handoff WebBuilder — Admin panel Roggero & Roma → Propuesta Farias

## Contexto comercial

Luis Farias pidió presupuesto para conversar con su amigo/socio. Juan le mostró `lamontaña.lat` como demo visual de calidad Wolfim, pero la propuesta real es para **Farias & Asociados**.

La base funcional correcta es **Roggero & Roma**: portal inmobiliario premium con catálogo, fichas, filtros, contacto, reseñas y administración.

Desde wolfim-growth ya relevamos el sitio público, pero para hacer una propuesta seria necesitamos que web-builder lea el código del proyecto y detalle **qué incluye realmente el admin panel**.

## Pedido a web-builder

Leer el código del proyecto Roggero & Roma y devolver un informe modular del admin panel, separando:

1. **Módulos ya implementados y funcionando.**
2. **Módulos parcialmente implementados.**
3. **Módulos que existen en código pero no están activos.**
4. **Módulos que habría que construir para Farias.**
5. **Dependencias técnicas / riesgos / esfuerzo relativo.**

## Preguntas concretas a responder

### 1. Propiedades / catálogo

- ¿Cómo se crean propiedades desde el admin?
- ¿Qué campos tiene una propiedad?
- ¿Permite editar/borrar/publicar/despublicar?
- ¿Permite destacar propiedades en home?
- ¿Maneja estados comerciales? Ej: nueva, precio mejorado, última unidad, oportunidad, amoblada.
- ¿Permite ordenar propiedades?
- ¿Permite categorías/tipos? Ej: casa, departamento, terreno, campo, comercial.
- ¿Permite operación venta/alquiler?
- ¿Permite cargar precio como número y/o “consultar”?
- ¿Permite moneda?

### 2. Fotos / galería

- ¿Cómo se cargan imágenes?
- ¿Usa Cloudinary u otro storage?
- ¿Permite ordenar fotos?
- ¿Permite foto principal/cover?
- ¿Hay límite o compresión?
- ¿Se puede cargar desde mobile sin romper experiencia?

### 3. Fichas individuales

- ¿Cada propiedad genera URL pública propia?
- ¿El slug se genera automático o manual?
- ¿Tiene preview antes de publicar?
- ¿Qué datos salen en la ficha?
- ¿Tiene botón de compartir?
- ¿Tiene WhatsApp por propiedad o solo contacto general?
- ¿El mensaje de WhatsApp sale prellenado con la propiedad?

### 4. Buscador y filtros

- ¿Qué filtros están implementados realmente?
- ¿Ciudad/zona?
- ¿Tipo?
- ¿Precio?
- ¿Dormitorios?
- ¿Baños?
- ¿Superficie?
- ¿Estado?
- ¿Código interno?
- ¿Vista en mapa?

### 5. Mapa / ubicación

- ¿Se cargan coordenadas o dirección?
- ¿Permite ubicación aproximada?
- ¿Qué proveedor usa para mapa?
- ¿Hay costos/API keys?
- ¿Se puede ocultar dirección exacta?

### 6. Presupuestos PDF desde mobile — módulo nuevo propuesto por Juan

Juan quiere agregar para Farias:

> Posibilidad de crear presupuestos en PDF para enviar a clientes desde mobile.

Relevar si algo parecido ya existe o si habría que construirlo.

Detallar módulo ideal:

- seleccionar una o varias propiedades;
- cargar datos del interesado/clientes;
- elegir plantilla de presupuesto;
- generar PDF desde celular;
- descargar o compartir por WhatsApp;
- incluir logo Farias, datos de contacto y propiedades seleccionadas;
- opcional: notas comerciales, vigencia, condiciones, financiación;
- guardar histórico de presupuestos generados.

Responder:

- ¿Es viable con la arquitectura actual?
- ¿Qué componentes ya existen reutilizables?
- ¿Qué faltaría construir?
- ¿Es módulo simple, medio o complejo?
- ¿Conviene venderlo incluido o como add-on?

### 7. Módulo reseñas de Google — módulo nuevo propuesto por Juan

Juan quiere agregar:

> Módulo de reseñas de Google: mostrar reseñas, permitir elegir cuáles mostrar, etc.

Relevar si Roggero ya tiene integración/carga de reseñas o si son hardcodeadas/manuales.

Detallar módulo ideal:

- importar reseñas de Google Business Profile o cargarlas manualmente;
- listar reseñas en admin;
- activar/desactivar cuáles se muestran;
- ordenar reseñas destacadas;
- mostrar nombre, texto, estrellas, foto si existe;
- evitar mostrar reseñas malas o irrelevantes;
- actualizar periódicamente si hay API disponible.

Responder:

- ¿Actualmente las reseñas vienen de Google real, JSON, DB o hardcode?
- ¿Se puede administrar desde panel?
- ¿Qué habría que construir para Farias?
- ¿La API de Google Reviews requiere credenciales/costos?
- ¿Conviene versión v1 manual y versión v2 automática?

### 8. Usuarios / roles / seguridad

- ¿Hay login de admin?
- ¿Roles? admin/superadmin/cliente.
- ¿Puede una inmobiliaria tener usuario propio?
- ¿Hay protección para rutas `/admin` o `/superadmin`?
- ¿Cómo se excluye tráfico admin de Analytics?

### 9. Analytics / reporting

- ¿Qué eventos se miden actualmente?
- ¿Se miden vistas por propiedad?
- ¿Se miden clicks WhatsApp/formulario?
- ¿Se puede generar reporte mensual de propiedades más vistas?
- ¿Qué faltaría para vender “informe mensual simple” a Farias?

### 10. Contenido institucional

- ¿El admin permite editar textos de home/historia/footer o está hardcodeado?
- ¿Permite editar teléfonos, email, dirección y redes?
- ¿Permite editar métricas de home?
- ¿Permite editar bloques “propietarios / inversores / alquileres”?

## Formato de respuesta requerido

Por favor devolver un informe en Markdown con esta estructura:

```md
# Roggero Admin Panel — Relevamiento para Farias

## Resumen ejecutivo

## Módulos confirmados
| Módulo | Existe | Estado | Evidencia en código | Comentario comercial |

## Módulos propuestos para Farias
| Módulo | Incluido recomendado | Esfuerzo | Riesgo | Vender como |

## Campos de propiedad detectados

## Flujo admin detectado

## Módulo PDF presupuestos desde mobile

## Módulo reseñas Google

## Recomendación comercial para propuesta Farias

## Riesgos / límites para no prometer de más

## Archivos/rutas del código revisadas
```

## Resultado esperado para wolfim-growth

Con ese informe, wolfim-growth arma una propuesta comercial seria para Farias & Asociados, separando:

- portal base incluido;
- módulos premium incluidos;
- add-ons opcionales;
- precio defendible;
- alcance que no prometa más de lo que web-builder puede entregar.

## Nota comercial

Para Farias, los dos módulos diferenciales que Juan quiere evaluar son:

1. **Presupuestos PDF desde mobile** — herramienta de venta directa para enviar a interesados.
2. **Reseñas de Google administrables** — prueba social controlada desde el panel.

Estos módulos pueden justificar mejor el precio y diferenciar Wolfim de una web inmobiliaria genérica o una plataforma tipo 2clics.
