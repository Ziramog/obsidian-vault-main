---
title: Diagnóstico técnico del sitio actual — Suelo Argentino
company: Suelo Argentino Negocios Inmobiliarios
url: https://sueloargentino.com
owner: wolfim-growth
created: 2026-07-31
method: inspeccion-publica-solo-lectura
status: verified
---

# Diagnóstico técnico del sitio actual

## Conclusión

`sueloargentino.com` es un sitio **WordPress**, no una plataforma inmobiliaria externa tipo Tokko ni un desarrollo SaaS a medida.

La gestión de propiedades está montada dentro del mismo WordPress mediante el tema inmobiliario **HomePress** y el plugin **uListing**. Las propiedades se guardan como un tipo de contenido personalizado `listing` dentro de WordPress.

## Stack detectado

| Capa | Tecnología | Evidencia pública |
|---|---|---|
| CMS | WordPress 5.7.15 | Assets de `/wp-includes/` y `/wp-content/` con versión `5.7.15`; API REST de WordPress activa |
| Tema | HomePress 1.3.2 | `/wp-content/themes/homepress/style.css` identifica nombre, autor y versión |
| Constructor visual | Elementor 3.1.4 | Assets y configuración pública de Elementor |
| Motor inmobiliario | uListing 1.7.2 | Assets del plugin y tipos REST `listing`, `listing_type`, `listing-category` y `listing-region` |
| Comparador/favoritos | uListing Compare 1.1.5 y uListing Wishlist 1.1.2 | Assets públicos cargados por el sitio |
| Servidor | LiteSpeed en Hostinger/hPanel | Cabeceras HTTP públicas |
| Backend | PHP 7.4.33 | Cabecera `X-Powered-By` |
| SEO | All in One SEO 4.1.6.2 | Metadatos y sitemap generados por el plugin |
| Formularios | Contact Form 7 y WPForms Lite | Assets públicos |
| WhatsApp | Joinchat / Creame WhatsApp Me | Assets públicos |
| Analítica | MonsterInsights instalado pero sin configurar | El HTML declara explícitamente que no existe código de seguimiento activo |

También aparece el namespace REST `idxbroker/v1`, por lo que IDX Broker parece instalado. Sin embargo, las propiedades visibles se publican como registros `listing` de uListing; no encontré evidencia pública de que el inventario dependa de una sincronización externa.

## Estado del inventario

- La API REST pública informa **115 propiedades publicadas**.
- La propiedad más reciente detectada fue cargada el **31 de julio de 2026**.
- El registro enviado por Juan existe como `listing` de WordPress con ID `19844`.
- Esto confirma que siguen usando activamente el panel actual para cargar propiedades.

## Problemas técnicos verificados

### 1. El frente público devuelve HTTP 500

Tanto la portada como la ficha de propiedad consultada devolvieron estado **HTTP 500**. El servidor llega a entregar HTML, pero comunica un error interno. Esto puede afectar disponibilidad, rastreo de Google y confianza técnica.

### 2. El sitemap también devuelve HTTP 500

El XML se genera, pero la respuesta llega con estado 500. Para buscadores no es un estado sano aunque el contenido exista.

### 3. Tecnología envejecida

- La rama WordPress 5.7 fue lanzada en marzo de 2021.
- El tema HomePress 1.3.2 expone una última modificación de abril de 2021.
- PHP 7.4.33 llegó a fin de vida oficial el 28 de noviembre de 2022.
- Elementor y varios plugins exponen versiones de 2021.

### 4. Analytics no está operativo

MonsterInsights está instalado, pero el propio HTML indica que no está configurado y que no existe código de seguimiento. Actualmente no hay evidencia de medición útil de visitas, propiedades o consultas.

## Implicación comercial para Wolfim

No hay que venderles solamente un cambio visual. El argumento real es:

> Suelo Argentino tiene un inventario activo y una marca vigente, pero opera sobre una instalación WordPress antigua que hoy devuelve errores 500 y no mide el comportamiento comercial. Wolfim puede migrar ese inventario a un portal propio más estable, administrable y medible sin perder `sueloargentino.com`.

La migración es viable, pero para conservar todos los campos, imágenes y relaciones de uListing conviene solicitar:

1. acceso de administrador a WordPress;
2. acceso a Hostinger/hPanel o una exportación completa;
3. acceso o control del dominio;
4. exportación de la base de datos y carpeta de medios;
5. validación de los campos personalizados usados por uListing.

Sin credenciales, la API pública permite recuperar títulos, URLs, fechas, imágenes destacadas y taxonomías, pero no garantiza todos los campos internos de cada propiedad.

## Fuentes consultadas

- https://sueloargentino.com/
- https://sueloargentino.com/listing/vende-casa-de-categoria-de-350-m2/
- https://sueloargentino.com/wp-json/
- https://sueloargentino.com/wp-json/wp/v2/types
- https://sueloargentino.com/wp-json/wp/v2/listing/19844
- https://sueloargentino.com/wp-json/wp/v2/listing?per_page=1&orderby=date&order=desc
- https://sueloargentino.com/wp-content/themes/homepress/style.css
- https://sueloargentino.com/sitemap.xml
- https://www.php.net/eol.php
- https://wordpress.org/documentation/wordpress-version/version-5-7
