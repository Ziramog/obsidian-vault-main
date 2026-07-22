---
id: HO-2026-07-22-001
status: ready
from: brain-vps
to: brain-local
project: ango
priority: high
depends-on: []
created-at: 2026-07-22T18:21:00-03:00
acknowledge-by: next-local-session
due-at: 2026-07-23T12:00:00-03:00
escalate-after: 18h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — web-builder — GA4, Google Ads y mediciones ANGO

## Motivo

`ango-commercial` dejó el brief formal `LOCAL_REQUEST` porque este profile no habla directo con `web-builder`. `brain-vps` convierte ese pedido en handoff oficial hacia local.

Fuente obligatoria:

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-ga4-ads-mediciones-2026-07-22.md
```

## Objetivo verificable

Dejar lista la infraestructura de medición para lanzar Google Ads de ANGO sin entrar a ciegas, entregando evidencia real de implementación y prueba.

Al finalizar, `web-builder` debe devolver evidencia de:

1. GA4 instalado y recibiendo eventos.
2. Google Ads conectado o preparado para conexión.
3. Conversiones principales creadas o documentadas para importar.
4. Eventos probados en DebugView / Realtime.
5. URLs finales y UTMs definidos para cada grupo de anuncios.
6. Selectores o IDs estables para CTAs y formulario.

## Contexto mínimo a leer antes de tocar nada

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-ga4-ads-mediciones-2026-07-22.md
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-landing-repuestos-urvig-micron-2026-07-16.md
companies/ango/projects/google-ads-2026-06/campana-definitiva-google-ads-ango-2026-07-16.md
companies/ango/intelligence/google-ads-keyword-planner-2026-analisis.md
companies/ango/intelligence/context.md
companies/ango/intelligence/patterns.md
Hermes/Handoffs/vps-to-local/HO-2026-07-16-001/request.md
```

## Páginas / destinos a medir

1. **RG / embragues / PTO industriales**
   - Dominio conocido: `https://www.angometalurgica.com.ar/`
   - Validar URL final exacta con Juan o repo local.
2. **Compatibles Urvig/Micron**
   - Slug sugerido previo: `/repuestos-compatibles-urvig-micron`
   - Validar URL final exacta antes de configurar Ads.

## Eventos GA4 requeridos

### Principales

```text
whatsapp_clicked
phone_clicked
lead_form_submitted
email_clicked
```

### Secundarios útiles

```text
catalog_downloaded
calculator_started
calculator_submitted
model_viewed
quote_form_started
```

## Definiciones clave

- `whatsapp_clicked`: click real sobre CTA de WhatsApp.
  - Parámetros sugeridos: `page_path`, `cta_location`, `product_line`, `ad_group_intent`
  - Valores esperados `product_line`: `urvig_micron`, `rg_pto`, `unknown`
- `phone_clicked`: click sobre enlace `tel:`
- `email_clicked`: click sobre `mailto:` o CTA de email
- `lead_form_submitted`: submit exitoso de formulario
  - Si hay varios formularios, diferenciar al menos:
    - `form_name=rg_pto_quote`
    - `form_name=urvig_micron_quote`
    - `form_name=calculator_quote`

## Conversiones Google Ads sugeridas

### Principales

```text
lead_form_submitted
whatsapp_clicked
phone_clicked
```

### Secundarias / observación

```text
email_clicked
catalog_downloaded
calculator_submitted
```

No optimizar inicialmente por pageviews ni scroll.

## UTM estándar

Base sugerida:

```text
utm_source=google
utm_medium=cpc
utm_campaign=ango_search_compatibles_rg_2026
utm_content={adgroupid}
utm_term={keyword}
```

Alternativa aceptable si queda documentada por grupo:

```text
utm_campaign=ango_search_urvig_2026
utm_campaign=ango_search_micron_2026
utm_campaign=ango_search_rg_pto_2026
```

## Requisitos de implementación

1. Todos los CTAs importantes deben tener IDs/classes estables.
2. WhatsApp debe tener evento diferenciado por página o línea de producto.
3. Teléfono debe usar `tel:` correcto para mobile.
4. Formularios deben disparar evento solo al envío exitoso.
5. Descarga de catálogo debe tener evento propio si existe.
6. Si se usa GTM, documentar container, tags y triggers creados.
7. Si se instala GA4 directo sin GTM, documentar dónde quedó el snippet.
8. No romper performance mobile.
9. No exponer IDs, tokens o credenciales en archivos públicos.

## Propiedad de cuentas

Preferencia operativa:

```text
Cuenta Google / Google Ads / GA4: Gmail de Antonio / ANGO
Juan/Wolfim: acceso administrador operativo
```

No crear propiedades bajo Gmail personal de Juan si se puede evitar. Si falta acceso, dejar pasos exactos para que Juan/Antonio creen u otorguen permisos.

## Chequeo obligatorio antes de entregar

`web-builder` debe verificar con evidencia real:

- GA4 DebugView o Realtime mostrando eventos.
- click real de WhatsApp medido.
- click real de teléfono medido.
- envío real o test de formulario medido.
- descarga de catálogo medida si existe.
- navegación desde URL con UTM preservando parámetros.

## Criterios de aceptación

- No lanzar Google Ads hasta que estén medidos al menos `whatsapp_clicked`, `phone_clicked` y `lead_form_submitted`, o una alternativa documentada.
- Las conversiones diferencian Urvig/Micron vs RG/PTO.
- Las URLs finales quedan listas con UTM.
- Los eventos aparecen en GA4 Realtime/DebugView.
- Google Ads queda conectado a GA4 o con pasos concretos para importación.
- Se entrega evidencia real, no solo declaración.
- Se informan archivos/rutas modificados en repo y cualquier bloqueo concreto.

## Restricciones

- No modificar `Hermes/Config/`.
- No tocar secrets, tokens ni `.env`.
- No hacer cambios destructivos.
- No usar `git reset --hard`, `git clean` ni `push --force`.
- Si falta acceso a cuentas, escalar con instrucciones exactas y bloqueo verificable.

## Respuesta esperada en este handoff

Publicar `response.md` en esta carpeta con:

1. URLs finales medidas.
2. Propiedad GA4 usada o pendiente de acceso.
3. Si se usó GTM: container, tags y triggers creados.
4. Lista de eventos implementados.
5. Lista de conversiones marcadas para Google Ads.
6. Evidencia de prueba real: capturas, logs o descripción verificable.
7. Archivos/rutas modificados en repo.
8. Bloqueos pendientes, si los hubiera.
