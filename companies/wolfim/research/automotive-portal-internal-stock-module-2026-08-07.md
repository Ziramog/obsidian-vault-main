---
owner: wolfim-growth
status: draft-for-juan
created: 2026-08-07
company: Wolfim
vertical: automotive
type: product-module
related:
  - companies/wolfim/research/automotive-portal-plan-2026-08-03.md
  - companies/wolfim/research/LOCAL_REQUEST-webbuilder-automotive-portal-2026-08-03.md
---

# Módulo interno privado — ordenamiento de stock y documentación

## Decisión comercial

La idea es muy buena y sube el valor del portal.

El portal no debe venderse solo como vidriera pública. Puede venderse como:

> Showroom digital público + sistema interno privado para ordenar stock, mantenimiento y documentación de cada vehículo.

Esto cambia el producto de “web para mostrar autos” a “herramienta de trabajo para la concesionaria”.

## Por qué importa

Muchas concesionarias tienen el stock repartido entre:

- publicaciones de Instagram/Facebook;
- MercadoLibre/GTM;
- planillas;
- fotos en celulares;
- carpetas físicas;
- papeles/documentación;
- conversaciones de WhatsApp;
- datos técnicos que solo recuerda una persona.

Eso genera desorden, riesgo y pérdida de tiempo.

El módulo interno permite que cada vehículo tenga dos capas:

1. **Vista pública:** lo que ve el comprador.
2. **Vista privada:** lo que usa la concesionaria para operar y controlar el stock.

## Frase de venta

```text
Además de mostrar los autos hacia afuera, el portal puede servirles puertas adentro: cada vehículo tiene su ficha interna con documentación, mantenimiento, estado técnico, observaciones y tareas pendientes.

Entonces no solo venden mejor; también ordenan el stock y reducen el desorden interno.
```

## Diferenciador comercial

La mayoría de agencias puede contratar una web o publicar en portales.

Pocas tienen un lugar propio donde cada unidad esté ordenada con:

- ficha pública;
- ficha interna;
- historial;
- documentación;
- mantenimiento;
- estado comercial;
- costos;
- tareas pendientes;
- responsable.

Ese es el diferencial fuerte para vender a agencias más serias o con más rotación de stock.

## Qué datos tendría cada vehículo

### Datos públicos

- Marca.
- Modelo.
- Versión.
- Año.
- Kilometraje.
- Precio.
- Fotos.
- Combustible.
- Transmisión.
- Color.
- Equipamiento destacado.
- Estado: disponible, reservado o vendido.
- Botón WhatsApp por vehículo.
- Botón compartir historia.

### Datos privados

- Costo de compra o toma.
- Margen objetivo.
- Precio mínimo aceptable.
- Estado técnico general.
- Observaciones internas.
- Responsable comercial.
- Fecha de ingreso al stock.
- Origen: compra, consignación, permuta o toma.
- Ubicación física: salón, depósito, taller, lavadero, sucursal.
- Estado comercial: a revisar, listo para publicar, publicado, reservado, vendido, entregado.

## Registro de mantenimiento y preparación

Cada vehículo podría tener historial interno de:

- cambio de aceite;
- filtros;
- frenos;
- batería;
- cubiertas;
- tren delantero;
- alineación/balanceo;
- revisión mecánica;
- revisión eléctrica;
- detailing/lavado;
- reparación estética;
- service pendiente;
- fecha y costo de cada trabajo;
- proveedor/taller;
- comprobante o factura adjunta.

## Documentación privada por vehículo

Documentos posibles:

- título;
- cédula;
- formulario 08;
- informe de dominio;
- verificación policial;
- libre deuda de infracciones/patentes;
- VTV/RTO;
- factura o boleto;
- comprobantes de service;
- garantía;
- manuales;
- fotos de documentación;
- cualquier PDF o imagen interna.

Importante: nada de esto debe estar visible al público.

## Checklist interno por unidad

Antes de publicar un vehículo, la agencia puede marcar:

- fotos cargadas;
- precio definido;
- documentación revisada;
- mecánica revisada;
- lavado/detailing hecho;
- descripción aprobada;
- ficha pública revisada;
- historia generada;
- publicado en web;
- compartido en redes;
- publicado en MercadoLibre/GTM si corresponde.

## Permisos y privacidad

Separar claramente campos públicos y privados.

Regla técnica:

> Todo dato interno debe requerir login y rol autorizado. Nunca debe renderizarse en páginas públicas ni quedar expuesto por SEO, sitemap o metadata.

Roles posibles:

- Admin: ve todo.
- Vendedor: ve datos comerciales y estado.
- Taller/preparación: ve mantenimiento y checklist técnico.
- Solo lectura: consulta documentación sin editar.

## MVP recomendado

Contexto actualizado: si el showroom demo ya está funcional aproximadamente en un 90% y es clonable, conviene avanzar con el módulo interno mínimo como siguiente sprint.

La prioridad cambia así:

1. cerrar/publicar showroom público;
2. agregar ficha interna privada mínima;
3. usarlo como diferencial comercial para vender paquete superior.

### V0 demo público

Mantener foco actual:

- home;
- catálogo;
- ficha pública;
- WhatsApp;
- historia 9:16;
- panel visible o demostrable.

### V1 cliente real

Agregar ficha interna simple:

- campos privados por vehículo;
- documentación adjunta;
- notas internas;
- estado comercial;
- checklist prepublicación.

### V2 módulo operativo

Agregar sistema más completo:

- historial de mantenimiento;
- costos por vehículo;
- alertas de vencimientos;
- roles/permisos;
- reportes de stock;
- vencimientos de documentación;
- exportación PDF o Excel.

## Cómo venderlo sin complicar

No venderlo como software pesado al inicio.

Frase simple:

```text
Primero armamos el showroom digital. Si después quieren usarlo también para ordenar el stock puertas adentro, sumamos la ficha interna de cada vehículo: documentación, mantenimiento, estado técnico y tareas pendientes.
```

## Paquetes sugeridos

| Paquete | Qué incluye | Ticket sugerido |
|---|---|---:|
| Showroom público | Web, catálogo, fichas, WhatsApp, historias | USD 450 setup + USD 39/mes |
| Portal concesionaria | Showroom + panel para cargar stock | USD 650-850 setup + USD 49-79/mes |
| Portal operativo | Portal + ficha interna/documentación/checklist | USD 900-1200 setup + USD 79-129/mes |
| Portal growth | Operativo + campañas + reportes | USD 1200+ setup + USD 129+/mes |

Los precios son anclas internas; validar con Juan antes de enviar propuesta formal.

## Nueva pregunta de diagnóstico

Agregar a la reunión:

```text
Además de mostrar los autos al público, ¿hoy cómo ordenan internamente la documentación, mantenimiento y estado de cada unidad?
```

Si responden que usan planillas, carpetas o WhatsApp, abrir valor:

```text
Ahí también puede ayudar el portal: cada auto puede tener su parte pública para vender y su parte privada para ordenar documentación, mantenimiento y tareas internas.
```

## Recomendación final

Incorporarlo como diferencial y upsell, no como requisito para el primer demo.

Para vender ahora:

1. Mostrar showroom público.
2. Mostrar panel de stock.
3. Contar que la evolución natural es ficha interna privada por vehículo.
4. Si el cliente muestra dolor operativo, cotizar Portal Operativo.

Esto puede subir el ticket y diferenciar fuerte frente a agencias que solo ofrecen webs o campañas.
