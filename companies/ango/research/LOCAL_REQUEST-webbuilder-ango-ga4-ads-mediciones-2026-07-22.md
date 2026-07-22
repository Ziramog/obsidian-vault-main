---
type: LOCAL_REQUEST
status: ready-for-brain-vps-handoff
from: ango-commercial
to: brain-vps
requested-assignee: web-builder
company: ANGO
project: google-ads-2026-06
priority: high
created-at: 2026-07-22T18:17:40-03:00
approval-source: Juan
requires-local: true
blocking-before-ads-launch: true
---

# LOCAL_REQUEST — web-builder — GA4, Google Ads y mediciones ANGO

## Pedido de Juan

Juan confirmó que ANGO va a largar Google Ads y que la web ya tiene listas las páginas para:

1. embragues / tomas de fuerza ANGO RG;
2. repuestos compatibles Urvig/Micron.

Antes de publicar campañas, necesita que `web-builder` realice el seteo técnico de medición:

- GA4;
- Google Tag Manager si corresponde;
- vinculación con Google Ads;
- conversiones y eventos medibles;
- verificación real de que los eventos disparan.

## Contexto de campaña

Documento definitivo de campaña:

```text
companies/ango/projects/google-ads-2026-06/campana-definitiva-google-ads-ango-2026-07-16.md
```

Handoff previo de landing Urvig/Micron:

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-landing-repuestos-urvig-micron-2026-07-16.md
```

Análisis de Keyword Planner:

```text
companies/ango/intelligence/google-ads-keyword-planner-2026-analisis.md
```

## Objetivo verificable

Dejar lista la infraestructura de medición para lanzar Google Ads sin entrar a ciegas.

Al finalizar, web-builder debe entregar evidencia de:

1. GA4 instalado y recibiendo eventos.
2. Google Ads conectado o preparado para conexión.
3. Conversiones principales creadas o documentadas para importar.
4. Eventos probados en modo debug / tiempo real.
5. URLs finales y UTMs definidos para cada grupo de anuncios.
6. Selectores o IDs estables para CTAs y formulario.

## Propiedad de cuentas

La campaña y medición deben quedar como activo de ANGO.

Preferencia operativa:

```text
Cuenta Google / Google Ads / GA4: Gmail de Antonio / ANGO
Juan/Wolfim: acceso administrador operativo
```

No crear propiedades bajo Gmail personal de Juan si puede evitarse.

Si web-builder no tiene acceso a la cuenta final, debe dejar instrucciones exactas para que Juan otorgue acceso o cree los recursos desde el Gmail de Antonio.

## Páginas a medir

### Página RG / embragues / PTO industriales

Destino para:

```text
Grupo 3: Productos RG / PTO Industrial
```

Dominio conocido:

```text
https://www.angometalurgica.com.ar/
```

Validar URL final exacta con Juan o repo local.

### Página repuestos compatibles Urvig/Micron

Destino para:

```text
Grupo 1: Compatibles Urvig
Grupo 2: Compatibles Micron
```

Slug sugerido en handoff anterior:

```text
/repuestos-compatibles-urvig-micron
```

Validar URL final exacta antes de configurar Ads.

## Eventos GA4 requeridos

### Eventos principales de conversión

Crear y testear estos eventos:

```text
whatsapp_clicked
phone_clicked
lead_form_submitted
email_clicked
```

### Eventos secundarios útiles

Si el sitio lo permite, agregar:

```text
catalog_downloaded
calculator_started
calculator_submitted
model_viewed
quote_form_started
```

## Definición de cada evento

### `whatsapp_clicked`

Dispara cuando el usuario toca cualquier CTA de WhatsApp.

Parámetros sugeridos:

```text
page_path
cta_location
product_line
ad_group_intent
```

Valores esperados para `product_line`:

```text
urvig_micron
rg_pto
unknown
```

### `phone_clicked`

Dispara cuando el usuario toca un enlace `tel:`.

Debe funcionar especialmente en mobile.

### `email_clicked`

Dispara cuando el usuario toca `mailto:` o CTA de email.

### `lead_form_submitted`

Dispara cuando se envía formulario de presupuesto/contacto.

Si hay varios formularios, diferenciar:

```text
form_name=rg_pto_quote
form_name=urvig_micron_quote
form_name=calculator_quote
```

### `catalog_downloaded`

Dispara cuando se descarga el catálogo técnico RG.

No es conversión principal, pero sirve para intención técnica.

### `calculator_started` / `calculator_submitted`

Para la calculadora de toma de fuerza.

Importante para el grupo RG/PTO industrial.

## Conversiones Google Ads sugeridas

Marcar como conversiones principales:

```text
lead_form_submitted
whatsapp_clicked
phone_clicked
```

Marcar como conversiones secundarias / observación:

```text
email_clicked
catalog_downloaded
calculator_submitted
```

No optimizar inicialmente por vistas de página ni scroll.

## UTM estándar

Usar esta base para URLs finales:

```text
utm_source=google
utm_medium=cpc
utm_campaign=ango_search_compatibles_rg_2026
utm_content={adgroupid}
utm_term={keyword}
```

Si se prefiere mayor legibilidad por grupo:

```text
utm_campaign=ango_search_urvig_2026
utm_campaign=ango_search_micron_2026
utm_campaign=ango_search_rg_pto_2026
```

Pero evitar mezclar dos convenciones sin documentarlo.

## URLs finales esperadas por grupo

| Grupo Google Ads | URL destino | Evento/conversión principal |
|---|---|---|
| Compatibles Urvig | página repuestos Urvig/Micron con ancla o copy Urvig visible | whatsapp_clicked / lead_form_submitted |
| Compatibles Micron | página repuestos Urvig/Micron con ancla o copy Micron visible | whatsapp_clicked / lead_form_submitted |
| Productos RG / PTO Industrial | home o sección RG/PTO | lead_form_submitted / calculator_submitted / phone_clicked |

## Requisitos de implementación web

1. Todos los CTAs importantes deben tener IDs/classes estables.
2. WhatsApp debe tener evento diferenciado por página o producto.
3. Teléfono debe usar `tel:` correcto para mobile.
4. Formularios deben disparar evento solo al envío exitoso, no al click en enviar si falla validación.
5. Descarga de catálogo debe tener evento propio.
6. Si se usa GTM, versionar nombres de tags/triggers/events en la respuesta.
7. Si se instala GA4 directo sin GTM, documentar dónde quedó el snippet.
8. No romper performance mobile.
9. No exponer IDs, tokens o credenciales en archivos públicos.

## Chequeo obligatorio antes de entregar

web-builder debe verificar con evidencia real:

- GA4 DebugView o Realtime mostrando eventos;
- click real de WhatsApp medido;
- click real de teléfono medido;
- envío real o test de formulario medido;
- descarga de catálogo medida si existe;
- navegación desde URL con UTM preservando parámetros.

## Datos de contacto observados en web actual

Validar antes de implementar:

```text
Teléfono: +54 9 3571 699006
Email: contacto@angometalurgica.com.ar
Web: www.angometalurgica.com.ar
```

No cambiar datos de contacto sin confirmación de Juan.

## Respuesta esperada de web-builder

Publicar respuesta en el handoff oficial o en el archivo que brain-vps indique, con:

1. URLs finales de las páginas.
2. Propiedad GA4 usada o pendiente de acceso.
3. ID de medición GA4, solo si no es secreto y corresponde documentarlo.
4. Si se usó GTM: container usado y tags/triggers creados.
5. Lista de eventos implementados.
6. Lista de conversiones marcadas para Google Ads.
7. Evidencia de prueba real: capturas, logs o descripción verificable.
8. Archivos/rutas modificadas en repo.
9. Bloqueos pendientes, si los hubiera.

## Criterios de aceptación

- No lanzar Google Ads hasta que estén medidos al menos `whatsapp_clicked`, `phone_clicked` y `lead_form_submitted` o una alternativa documentada.
- Las conversiones diferencian Urvig/Micron vs RG/PTO.
- Las URLs finales están listas con UTM.
- Los eventos aparecen en GA4 Realtime/DebugView.
- Google Ads queda conectado a GA4 o con pasos concretos para importación de conversiones.
- Juan puede saber qué canal generó cada consulta.

## Notas para brain-vps

Según directiva Sync V6, ango-commercial no habla directo con web-builder. Este archivo es el brief `LOCAL_REQUEST` dentro de zona ANGO para que brain-vps cree o valide el handoff oficial en:

```text
Hermes/Handoffs/vps-to-local/
```
