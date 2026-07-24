---
id: HO-2026-07-24-001
status: ready
from: brain-vps
to: brain-local
project: ango
priority: high
depends-on: []
created-at: 2026-07-24T15:14:30-03:00
acknowledge-by: next-local-session
due-at: 2026-07-25T12:00:00-03:00
escalate-after: 18h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — web-builder — Google Ads tag AW + validación medición ANGO

## Motivo

`ango-commercial` dejó un nuevo `LOCAL_REQUEST` porque ya existe campaña inicial de Google Ads en la cuenta de Antonio/ANGO y ahora hay que instalar/validar el **Google Ads tag AW** sin duplicar mediciones ni romper el esquema GA4 actual.

Fuente obligatoria:

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-aw-2026-07-24.md
```

## Objetivo verificable

Dejar correctamente implementado y probado el tag de Google Ads **AW-18347194194**, manteniendo GA4 sano, evitando duplicaciones y dejando claro si la campaña puede activarse o debe seguir pausada.

## Contexto mínimo a leer antes de tocar nada

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-google-ads-tag-aw-2026-07-24.md
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-ga4-ads-mediciones-2026-07-22.md
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-landing-repuestos-urvig-micron-2026-07-16.md
Hermes/Handoffs/vps-to-local/HO-2026-07-22-001/request.md
Hermes/Handoffs/vps-to-local/HO-2026-07-16-001/request.md
```

## Dato técnico recibido

Google tag / Conversion ID:

```text
AW-18347194194
```

Snippet provisto por Google Ads:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18347194194"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18347194194');
</script>
```

## URLs involucradas

```text
https://www.angometalurgica.com.ar/
https://www.angometalurgica.com.ar/repuestos-compatibles-urvig-micron/
```

## Pasos concretos para web-builder

Ejecutar en este orden, sin saltear validación:

1. **Inspeccionar implementación actual**
   - Ver si el sitio ya usa GTM.
   - Ver si ya existe `gtag` global o alguna instalación previa de Google Ads.
   - Ver cómo está instalado GA4 hoy.
   - Antes de agregar nada, confirmar que no se va a duplicar carga de tags.

2. **Elegir método correcto**
   - Si ya existe GTM activo: preferir **configurar Google tag en GTM**.
   - Si no existe GTM: usar **snippet directo** en `<head>`.
   - Documentar en `response.md` por qué se eligió ese camino.

3. **Si usa GTM**
   - Configurar Google tag / Google Ads tag con ID `AW-18347194194`.
   - Configurar **Conversion Linker** en todas las páginas.
   - Mantener GA4 existente.
   - Publicar contenedor.

4. **Si NO usa GTM**
   - Instalar el snippet base de Ads en el `<head>` de todas las páginas relevantes.
   - No eliminar GA4.
   - No duplicar un `gtag` ya existente.

5. **Revisar estrategia de conversiones**
   - Prioridad: **importar conversiones desde GA4** si ya están bien medidas.
   - Principales:
     - `lead_form_submitted`
     - `whatsapp_clicked`
     - `phone_clicked`
   - Secundarias/observación:
     - `email_clicked`
     - `catalog_downloaded`
     - `calculator_submitted`
     - `quote_form_started`
   - Solo usar conversion tags nativas de Google Ads si hace falta y si existen `conversion_label` reales.
   - **No inventar conversion labels.**

6. **Mantener separación por línea comercial**
   - Asegurar que siga diferenciándose:
     - `linea=rg_pto`
     - `linea=urvig_micron`
   - Si la diferenciación hoy depende de `page_path`, IDs, atributos o parámetros, dejarlo documentado.

7. **Probar con URLs de test**
   - Abrir home y landing con:

```text
?utm_source=google&utm_medium=cpc&utm_campaign=test_ango_ads&utm_content=test&utm_term=test&gclid=test123
```

8. **Verificar implementación real**
   - Confirmar que no se rompe navegación.
   - Confirmar que no se rompe el formulario.
   - Confirmar en Tag Assistant:
     - GA4 activo.
     - Google tag `AW-18347194194` o equivalente GTM.
     - Conversion Linker si corresponde.
   - Confirmar en GA4 DebugView/Realtime:
     - `whatsapp_clicked`
     - `phone_clicked`
     - `lead_form_submitted` si aplica

9. **Verificar estado para Ads**
   - Si se configuró algo nativo en Google Ads, revisar que la etiqueta no quede inactiva después de las pruebas.
   - Si falta algo para activar conversiones reales, especificarlo exactamente.

10. **Responder este handoff**
    - Crear `response.md` en esta carpeta.
    - Incluir:
      - método usado: GTM o snippet directo;
      - evidencia o confirmación verificable de Tag Assistant;
      - confirmación de eventos en GA4;
      - archivos/rutas tocados;
      - si faltan `conversion_label`, listar exactamente cuáles;
      - recomendación concreta: `campaña puede activarse` o `debe seguir pausada`.

## Criterios de aceptación

- El tag `AW-18347194194` queda implementado sin duplicar medición.
- GA4 sigue funcionando.
- Si hay GTM, se publica con Conversion Linker activo.
- Se verifican home + landing con parámetros de prueba.
- Se confirma visual/técnicamente el disparo correcto en Tag Assistant.
- Se confirma que los eventos comerciales siguen entrando a GA4.
- Se informa si Ads puede activarse o no.

## Restricciones

- No crear nuevas cuentas Google Ads.
- No cambiar presupuesto ni pujas.
- No modificar copy/compliance salvo corrección técnica mínima.
- No usar claims de original/oficial para Urvig/Micron.
- No pegar el snippet dos veces si ya hay GTM/gtag global.
- No escribir ni compartir credenciales, tokens ni datos de tarjeta.
- No modificar `Hermes/Config/`.
- No hacer cambios destructivos.

## Respuesta esperada en este handoff

Publicar `response.md` en esta carpeta con:

1. método usado (`GTM` o `snippet directo`);
2. evidencia/resultado de Tag Assistant;
3. confirmación de eventos en GA4;
4. archivos/rutas modificados;
5. si faltan `conversion_label`, cuáles son;
6. estado final recomendado:
   - `campaña puede activarse`, o
   - `campaña debe seguir pausada`.
