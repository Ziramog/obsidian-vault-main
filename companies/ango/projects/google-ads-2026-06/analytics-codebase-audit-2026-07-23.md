---
company: ANGO
project: google-ads-2026-06
type: codebase-audit
status: ready-for-antigravity-prompt
created: 2026-07-23
owner: web-builder
source-handoff: Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md
repo: C:\Projects\ANGOWEB2\astro-site
---

# ANGO — auditoría de medición GA4 / Google Ads

## Fuente revisada

El vault local todavía no tenía materializado `HO-2026-07-22-001` en working tree porque `main` está detrás de `origin/main`. Para no mezclar sync con cambios locales, leí los archivos desde `origin/main`:

- `Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md`
- `companies/ango/research/LOCAL_REQUEST-webbuilder-ango-ga4-ads-mediciones-2026-07-22.md`
- `companies/ango/research/ango-ga4-ads-mediciones-handoff-resumen-2026-07-22.md`

## Estado actual

| Componente | Estado | Evidencia |
|---|---|---|
| GA4 directo | No instalado | No hay `gtag`, `googletagmanager`, `dataLayer` ni Measurement ID real en `src/`. |
| GTM | No instalado | No hay `GTM-` ni snippet en `Layout.astro`. |
| Eventos reales a GA4 | No instalados | La landing Urvig/Micron solo despacha `CustomEvent('ango:conversion-intent')`; no llega a GA4/GTM. |
| CTAs con IDs estables | Parcial | La landing Urvig/Micron ya tiene varios `id` y `data-event`; la home no. |
| Formularios trackeables | Parcial | Hay formularios, pero sin envío a GA4. |
| Teléfono click-to-call | Defectuoso | En `repuestos-compatibles-urvig-micron.astro:258` el `tel:` está enmascarado como `tel:+549****9006`. |
| PDF catálogo | Existe sin evento | `Models.astro:56` descarga `/Catalogo_Tecnico_RG_ANGO.pdf`. |
| Search Console / Ads linking | No verificable desde código | Requiere acceso a cuentas Google de ANGO. |

## Elementos trackeables encontrados

### Home / RG-PTO

| Elemento | Archivo | Estado |
|---|---|---|
| WhatsApp hero | `src/components/Hero.astro:14` | Sin `id` / `data-event`. |
| Formulario selección PTO | `src/components/Specs.astro:43` | Submit abre WhatsApp en mobile o mailto en desktop; sin evento GA4. |
| PDF catálogo RG | `src/components/Models.astro:56` | Sin evento `catalog_downloaded`. |
| WhatsApp repuestos RG / reacondicionamiento | `src/components/Spares.astro:28`, `:45` | Sin `id` / `data-event`. |
| WhatsApp FAB global | `src/layouts/Layout.astro:39` | Tiene `id="wa-fab"`, sin parámetros de línea. |
| Calculadora | `src/pages/calculadora.astro` | No mide `calculator_started` ni `calculator_submitted`. |
| Footer teléfono/email | `src/components/Footer.astro` | Texto plano; no hay `tel:` ni `mailto:` clickeable en footer. |

### Landing Urvig/Micron

| Elemento | Archivo | Estado |
|---|---|---|
| WhatsApp hero | `src/pages/repuestos-compatibles-urvig-micron.astro:65-70` | Tiene `id`, `data-event`, `data-location`; falta envío a GA4. |
| Catálogo piezas | `src/pages/repuestos-compatibles-urvig-micron.astro:141-151` | Tiene `part_consulted` y códigos; falta GA4. |
| Formulario cotización | `src/pages/repuestos-compatibles-urvig-micron.astro:181`, `:356-383` | El submit abre WhatsApp; debe medir solo en submit válido, no por click del botón. |
| Botón submit | `src/pages/repuestos-compatibles-urvig-micron.astro:232` | Tiene `data-event="lead_form_submitted"`, riesgo: el listener genérico mide click aunque el form sea inválido. |
| Teléfono | `src/pages/repuestos-compatibles-urvig-micron.astro:258` | `tel:` enmascarado; corregir antes de Ads. |
| Email | `src/pages/repuestos-compatibles-urvig-micron.astro:259` | Tiene `mailto:` y `data-event`; falta GA4. |
| Sticky mobile CTA | `src/pages/repuestos-compatibles-urvig-micron.astro:271-281` | Tiene ID y datos; falta GA4. |

## Opciones técnicas

### Opción A — GA4 directo con gtag.js

**Alcance:** agregar snippet GA4 en `Layout.astro` condicionado por `PUBLIC_GA4_MEASUREMENT_ID`; crear helper liviano para eventos; instrumentar CTAs/formularios existentes.

**Riesgos:** requiere deploy para cambiar eventos; si el Measurement ID no está seteado, los eventos deben fallar silenciosamente. No resuelve por sí solo la vinculación con Google Ads ni Search Console.

**Visión:** mejor opción ahora. El sitio es Astro estático, pocos eventos, y el objetivo inmediato es no lanzar Ads a ciegas.

### Opción B — GTM + GA4

**Alcance:** instalar contenedor GTM, configurar tags/triggers en UI, usar selectores/data attributes.

**Riesgos:** más fricción y depende de acceso a Tag Manager. Mayor riesgo de mala configuración si se apura. Igual requiere crear/publicar contenedor y testear en Preview.

**Visión:** buena fase 2 cuando ANGO ya tenga cuenta Google operativa y quiera administrar eventos sin deploy.

## Recomendación

Implementar **Fase 1 con GA4 directo** en el repo y dejar todo preparado para Ads:

1. Juan/Antonio crean o confirman propiedad GA4 de ANGO.
2. Setear `PUBLIC_GA4_MEASUREMENT_ID=G-XXXXXXXXXX` en el entorno de deploy.
3. Antigravity instrumenta eventos con `gtag` seguro/no-op.
4. Verificar `page_view`, `whatsapp_clicked`, `phone_clicked`, `lead_form_submitted` en Realtime/DebugView.
5. Luego vincular GA4 con Google Ads e importar conversiones.

## URLs finales con UTM

Mantener la convención única de campaña definida:

```text
utm_source=google
utm_medium=cpc
utm_campaign=ango_search_compatibles_rg_2026
utm_content={adgroupid}
utm_term={keyword}
```

URLs sugeridas:

```text
Grupo Urvig:
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/?utm_source=google&utm_medium=cpc&utm_campaign=ango_search_compatibles_rg_2026&utm_content={adgroupid}&utm_term={keyword}

Grupo Micron:
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/?utm_source=google&utm_medium=cpc&utm_campaign=ango_search_compatibles_rg_2026&utm_content={adgroupid}&utm_term={keyword}

Grupo RG / PTO:
https://www.angometalurgica.com.ar/?utm_source=google&utm_medium=cpc&utm_campaign=ango_search_compatibles_rg_2026&utm_content={adgroupid}&utm_term={keyword}
```

La separación Urvig/Micron/RG debe salir de `page_path`, `product_line`, `cta_location` y, cuando corresponda, `ad_group_intent`.

## Prompt para Antigravity

### Objetivo

Instalar GA4 directo y eventos de conversión en ANGO para lanzar Google Ads con medición real.

### Contexto del proyecto

- Proyecto: ANGO Metalúrgica.
- Repo local absoluto: `C:\Projects\ANGOWEB2\astro-site`.
- Stack: Astro 6, salida static, `@astrojs/cloudflare`.
- Sitio live: `https://www.angometalurgica.com.ar/`.
- Landing Urvig/Micron live: `https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/`.
- No hay GA4/GTM instalado actualmente.
- La landing Urvig/Micron tiene `data-event` y `CustomEvent('ango:conversion-intent')`, pero eso no envía nada a GA4.
- No tocar secrets ni `.env`. Usar `PUBLIC_GA4_MEASUREMENT_ID` y dejar el código en no-op si falta.

### Tarea específica

1. En `src/layouts/Layout.astro`, instalar GA4 directo solo si existe `import.meta.env.PUBLIC_GA4_MEASUREMENT_ID`:
   - cargar `https://www.googletagmanager.com/gtag/js?id=...` con `async`;
   - inicializar `window.dataLayer`, `window.gtag` y `gtag('config', measurementId)`;
   - no hardcodear el ID real en el repo si no está confirmado.
2. Crear un helper cliente seguro para eventos, por ejemplo `src/scripts/analytics.js`, que exponga una función global o evento listener:
   - si `window.gtag` no existe, no romper;
   - enviar `gtag('event', eventName, params)`;
   - incluir siempre `page_path`, `page_location`, `cta_location`, `product_line` cuando aplique;
   - leer UTMs desde `URLSearchParams` e incluir `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`.
3. Instrumentar home / RG-PTO:
   - `src/components/Hero.astro`: WhatsApp hero con `id="cta-whatsapp-rg-hero"`, evento `whatsapp_clicked`, `product_line="rg_pto"`, `cta_location="home_hero"`.
   - `src/components/Specs.astro`: form `tomaFuerzaForm` debe disparar `quote_form_started` al primer foco/cambio y `lead_form_submitted` solo cuando el submit válido arma WhatsApp/mailto. Usar `form_name="rg_pto_quote"`, `product_line="rg_pto"`.
   - `src/components/Models.astro`: PDF `/Catalogo_Tecnico_RG_ANGO.pdf` debe disparar `catalog_downloaded`, `product_line="rg_pto"`, `cta_location="rg_catalog"`.
   - `src/components/Spares.astro`: WhatsApp de stock y reacondicionamiento con IDs y `whatsapp_clicked`, `product_line="rg_pto"`.
   - `src/layouts/Layout.astro`: FAB global debe disparar `whatsapp_clicked`; definir `product_line` por path: `urvig_micron` si `location.pathname` incluye `repuestos-compatibles-urvig-micron`, si no `rg_pto` en home, si no `unknown`.
   - `src/components/Footer.astro`: convertir teléfono y email en links clickeables estables si no altera diseño: `tel:+5493571699006` y `mailto:contacto@angometalurgica.com.ar`; medir `phone_clicked` y `email_clicked`.
4. Instrumentar landing Urvig/Micron:
   - `src/pages/repuestos-compatibles-urvig-micron.astro`: conectar todos los `data-event` existentes a GA4 real.
   - Corregir el bug crítico `href="tel:+549****9006"` a `href="tel:+5493571699006"`.
   - El botón `#lead-form-submit` NO debe disparar `lead_form_submitted` por click genérico si el form es inválido. Medir `lead_form_submitted` dentro del handler `submit`, después de que la validación HTML haya pasado y justo antes de abrir WhatsApp.
   - Mantener `part_consulted` para clicks por repuesto, con parámetros `part`, `urvig_code`, `micron_code`, `product_line="urvig_micron"`.
   - Todos los WhatsApp de esta página deben enviar `product_line="urvig_micron"`.
5. Instrumentar calculadora:
   - `src/pages/calculadora.astro`: medir `calculator_started` al primer cambio de inputs/selects.
   - Medir `calculator_submitted` cuando `calcular()` corre con datos válidos y muestra resultado. Parámetros sugeridos: `hp`, `rpm`, `equipment_type`, `selected_model`, `status`.
6. Preparar documentación técnica en un archivo del repo, por ejemplo `docs/analytics-events.md`, con:
   - eventos implementados;
   - parámetros;
   - URLs finales con UTM;
   - conversión principal/secundaria sugerida para Google Ads;
   - pasos manuales pendientes para conectar GA4 con Google Ads.
7. No implementar GTM en esta fase salvo que Juan entregue un `GTM-XXXXXXX` y confirme usar GTM ahora.

### Archivos a tocar

- `C:\Projects\ANGOWEB2\astro-site\src\layouts\Layout.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\scripts\analytics.js` o equivalente nuevo
- `C:\Projects\ANGOWEB2\astro-site\src\components\Hero.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\components\Specs.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\components\Models.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\components\Spares.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\components\Footer.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\pages\repuestos-compatibles-urvig-micron.astro`
- `C:\Projects\ANGOWEB2\astro-site\src\pages\calculadora.astro`
- `C:\Projects\ANGOWEB2\astro-site\docs\analytics-events.md`

### Restricciones

- No modificar diseño visual ni copy comercial salvo el `tel:` defectuoso.
- No tocar `.env`, secrets, tokens ni credenciales.
- No hardcodear IDs de cuenta si Juan no confirmó Measurement ID.
- Los eventos deben fallar silenciosamente si GA4 no cargó.
- No disparar conversiones por render ni por click inválido de formulario.
- No romper WhatsApp, mailto, descarga de PDF ni calculadora.
- No cambiar datos de contacto sin confirmación de Juan.

### Criterios de aceptación

- `npm run build` pasa sin errores.
- En el HTML generado aparece el snippet GA4 solo cuando hay `PUBLIC_GA4_MEASUREMENT_ID`.
- Con GA4 configurado, Realtime/DebugView muestra:
  - `page_view`;
  - `whatsapp_clicked` en home y landing;
  - `phone_clicked`;
  - `email_clicked`;
  - `lead_form_submitted` para formulario RG/PTO y formulario Urvig/Micron;
  - `catalog_downloaded` al descargar PDF;
  - `calculator_started` y `calculator_submitted` en calculadora.
- Los eventos diferencian `product_line=rg_pto` y `product_line=urvig_micron`.
- Las URLs con UTM cargan sin perder parámetros.
- El `tel:` de la landing Urvig/Micron queda real: `tel:+5493571699006`.
- No hay errores JS en consola.
- `docs/analytics-events.md` queda completo para conectar Google Ads e importar conversiones.

## Bloqueos externos

Para cumplir el handoff al 100% falta acceso o dato externo:

1. Measurement ID GA4 de propiedad ANGO (`G-XXXXXXXXXX`) o acceso para crearla desde Gmail de Antonio / ANGO.
2. Acceso Google Ads de ANGO para vincular GA4 e importar conversiones.
3. Verificación real en GA4 DebugView/Realtime después del deploy con el Measurement ID cargado.

Sin esos accesos, Antigravity puede dejar el sitio instrumentado, pero no puede probar recepción real en GA4.
