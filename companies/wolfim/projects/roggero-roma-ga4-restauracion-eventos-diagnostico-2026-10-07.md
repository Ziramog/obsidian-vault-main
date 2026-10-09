---
type: DIAGNOSTICO_TECNICO
company: wolfim
client: roggero-roma
target: web-builder
created: 2026-10-07
status: root-cause-identificado / fix pendiente de aprobación
answers_to: LOCAL_REQUEST-webbuilder-roggero-restaurar-eventos-ga4-2026-10-07.md
repo: C:\Projects\property-pulse-nextjs  (github.com/Ziramog/properties, branch main)
site_prod: https://www.roggeroyroma.com
---

# Roggero & Roma — GA4: por qué se cortaron `property_viewed` y `click_whatsapp`

## Veredicto (una línea)

**El guard de tráfico interno bloquea el 100% de los eventos custom.** `isAllowedTrackingHost()`
en `utils/analytics.js` sólo permite hosts `.com.ar`, pero el sitio en producción vive en
`www.roggeroyroma.com`. `canTrackAnalytics()` devuelve `false` para todo visitante externo y
`trackEvent()` descarta el evento en silencio.

## Evidencia verificada (2026-10-07)

### 1. Código desplegado en producción (bundle real, no el repo)

Extraído del chunk servido hoy por `www.roggeroyroma.com` (`/_next/static/chunks/layout-*.js`):

```js
// canTrackAnalytics() tal como está en producción
function s(e){let{host:t,pathname:a,role:r}=e;
  return (!t || !!["roggeroyroma.com.ar","www.roggeroyroma.com.ar","localhost","127.0.0.1"].includes(t))
      && !!( /* path check: /admin, /superadmin, /api */ )
      && "admin"!==r && "superadmin"!==r}
```

```js
// GoogleAnalytics.jsx: misma lista PERO sí incluye .com
["localhost","roggeroyroma.com","www.roggeroyroma.com","roggeroyroma.com.ar","www.roggeroyroma.com.ar","127.0.0.1"]
  .includes(window.location.hostname)
```

Es decir: **dos listas de hosts duplicadas y divergentes**. La del componente permite `.com`
(por eso el script de gtag se carga y el fallo es invisible), la del util no.

### 2. Runtime en vivo (incógnito, visitante externo)

| Chequeo en `www.roggeroyroma.com` | Resultado |
|---|---|
| `typeof window.gtag` | `function` ✅ |
| `window.__ANALYTICS_SESSION_READY__` | `true` ✅ |
| `window.__USER_ROLE__` | `null` (visitante externo) ✅ |
| dataLayer tras cargar home | sólo `js`, `config`, `gtm.dom`, `gtm.load` — **sin `page_view`** |
| Abrir `/properties/<id>` | **0 pushes** de `property_viewed` |
| Click en CTA de WhatsApp (`wa.me/5493547563911`) | **0 pushes** de `click_whatsapp` |

Los tres pre-requisitos del guard están OK; lo único que falla es el host.

### 3. Dominio

- `https://roggeroyroma.com` → 200, redirige a `https://www.roggeroyroma.com` (host real).
- `https://roggeroyroma.com.ar` → **DNS resuelve a IPs de Vercel (64.29.17.65 / 216.198.79.65)
  pero TLS handshake falla y HTTP devuelve 404**: el `.com.ar` ya no está servido por el proyecto.
- El vault confirma producción en `www.roggeroyroma.com` desde 03/06/2026.

### 4. Informe del cliente (PDF 07/09 → 06/10)

El propio informe ya mostraba el síntoma: **0 fichas vistas / 0 clics de WhatsApp**, mientras
seguía reportando 152 usuarios, 203 sesiones y 650 vistas. Coincide exactamente con el diagnóstico.

## Línea de tiempo (por qué el corte fue el 30/07 y no antes)

| Fecha | Commit | Efecto |
|---|---|---|
| 2026-07-07 | `23bb332` feat: complete advanced GA4 tracking | Se implementan los eventos. `utils/analytics.js` **no tenía allowlist de hosts** → disparaban en cualquier host. |
| 2026-07-09 | `beac27e` fix: exclude internal traffic from GA4 | Se agrega `isAllowedTrackingHost()` con **sólo `.com.ar`** y `canTrackAnalytics()` pasa a gatear `trackEvent()`. |
| ~2026-07-29/30 | deploy de `main` en Vercel (incluye `beac27e`; mismo push que `23a607f` semantic search) | El código nuevo llega a producción → **todos los eventos custom dejan de enviarse**. |
| 2026-07-29 / 28 | última data de `property_viewed` / `click_whatsapp` en GA4 | ✅ coincide con el deploy, no con la fecha del commit. |

Conclusión: el bug se escribió el 09/07 pero recién se publicó a fines de julio. El desfase de
3 semanas entre commit y corte de datos es la firma del deploy, no del código.

## Alcance real del daño (no son sólo 2 eventos)

`trackEvent()` es el embudo único. Se descartan **todos**:

`property_viewed`, `click_whatsapp`, `click_phone`, `click_maps`, `click_social`, `search_used`,
`form_submit` — **y también el `page_view` manual** de `GoogleAnalytics.jsx` (usa el mismo
`canTrackAnalytics`).

## Hallazgos secundarios

1. **Listas de hosts duplicadas** en `utils/analytics.js` y `components/GoogleAnalytics.jsx`
   (causa raíz del fallo silencioso). → unificar en una sola fuente.
2. **Fallo invisible**: `trackEvent()` hace `return` sin log. Nadie se enteró durante 2 meses.
3. **`.com.ar` roto**: el dominio alternativo no sirve el sitio (TLS/404). No es parte del pedido,
   pero conviene avisar a Franco/Marcos si lo están usando en algún lado.
4. **Posible doble conteo de `page_view`** (a confirmar, no verificado): con el guard roto, las
   ~650 vistas del informe parecen venir de la *Enhanced Measurement* de GA4 (page_view en cambios
   de history). Al arreglar el guard vuelve a disparar además el `page_view` manual → el volumen
   puede duplicarse. Ver "Validación" punto 4.
5. **Nombres**: el pedido del 07/08 nombraba `property_contact_clicked`; el repo implementó
   `click_whatsapp`. El informe del cliente usa el cuadrito "Clics de WhatsApp" → **mantener
   `click_whatsapp`** y no renombrar (renombrar rompería la serie histórica).

## Opciones de fix

### Opción A — parche mínimo
Agregar `'roggeroyroma.com'` y `'www.roggeroyroma.com'` a la lista de `utils/analytics.js`.
- ✅ 2 líneas, riesgo cero, restaura todo ya.
- ❌ Deja la duplicación → puede volver a pasar en el próximo cambio de dominio.

### Opción B — fuente única (RECOMENDADA)
Exportar `TRACKING_HOSTS` desde `utils/analytics.js`, incluir los 4 hosts de producción
(`.com`, `www.com`, `.com.ar`, `www.com.ar`) + `localhost`/`127.0.0.1`, e importarla en
`GoogleAnalytics.jsx` (borrar la lista local). Sumar un `console.warn` una vez por host cuando el
guard descarta por host, para que nunca más falle en silencio.
- ✅ Mismo esfuerzo que A, elimina la causa raíz y agrega visibilidad.
- ✅ No toca la exclusión de admin/superadmin ni las rutas `/admin`, `/superadmin`, `/api`.
- ❌ Ninguno relevante.

### Opción C — B + robustez a futuro
Como B, pero con override por env `NEXT_PUBLIC_GA_ALLOWED_HOSTS` (lista separada por comas) para
poder sumar un dominio nuevo sin deploy de código, y/o matching por sufijo.
- ✅ Inmune a futuras migraciones de dominio.
- ❌ Más superficie; conviene sólo si prevén mover dominios otra vez.

**Recomendación: Opción B.** C queda como mejora posterior si el cliente cambia de dominio seguido.
No agregar hosts `*.vercel.app` a la allowlist: contaminaría GA4 con tráfico de previews.

---

# PROMPT PARA ANTIGRAVITY

## Objetivo

Restaurar el envío de los eventos custom de GA4 en el sitio de Roggero & Roma corrigiendo el
allowlist de hosts del guard de analytics, sin tocar la exclusión de tráfico interno.

## Contexto del proyecto

- Repo: `C:\Projects\property-pulse-nextjs` (Next.js App Router, `main`, deploy Vercel).
- Producción: `https://www.roggeroyroma.com` (con `roggeroyroma.com` redirigiendo a `www`).
- GA4: `G-PW4FH9WHQB`, inyectado por `components/GoogleAnalytics.jsx` con
  `send_page_view: false` y `page_view` manual.
- Todos los eventos pasan por `trackEvent()` en `utils/analytics.js`, que aplica
  `canTrackAnalytics({ host, pathname, role })`.
- **Bug**: `isAllowedTrackingHost()` sólo permite `.com.ar`, pero el sitio vive en
  `www.roggeroyroma.com` → `canTrackAnalytics` devuelve `false` y se descarta todo evento.
  Verificado en el bundle de producción el 2026-10-07.

## Tarea específica

1. En `utils/analytics.js`, definir y exportar una constante única:

   ```js
   export const TRACKING_HOSTS = [
     'roggeroyroma.com',
     'www.roggeroyroma.com',
     'roggeroyroma.com.ar',
     'www.roggeroyroma.com.ar',
     'localhost',
     '127.0.0.1',
   ];
   ```

2. Reescribir `isAllowedTrackingHost(hostname)` para que use `TRACKING_HOSTS.includes(hostname)`.

3. En `canTrackAnalytics()`, cuando el descarte sea por host, emitir un aviso **una sola vez por
   hostname por sesión** (flag a nivel de módulo), para que el fallo no vuelva a ser silencioso:

   ```js
   console.warn(`[analytics] host no permitido: ${host} — evento descartado`);
   ```

   Debe seguir devolviendo `false` igual.

4. En `components/GoogleAnalytics.jsx`: importar `TRACKING_HOSTS` desde `@/utils/analytics` y
   eliminar el array `allowedHosts` local (tanto en el `useEffect` como en el early-return de
   render). No debe quedar ninguna lista de hosts duplicada en el repo.

5. No cambiar nombres de eventos ni parámetros.

## Archivos a tocar

- `utils/analytics.js` (allowlist + warn)
- `components/GoogleAnalytics.jsx` (importar la lista, borrar la duplicada)

## Restricciones

- NO tocar la exclusión por rol (`admin` / `superadmin`) ni las rutas `/admin`, `/superadmin`, `/api`.
- NO agregar hosts de preview/Vercel a la allowlist.
- NO renombrar eventos ni parámetros (`click_whatsapp`, `property_viewed`, etc. se mantienen).
- NO enviar PII a GA4.
- NO hardcodear el Measurement ID: sigue viniendo de `siteConfig.analyticsId`.
- NO tocar los cambios sin commitear que ya hay en `components/PropertyEditForm.jsx`,
  `PropertyAddForm.jsx` y `PropertyDetails.jsx` (son de otro trabajo: amenities).

## Criterios de aceptación

1. En el bundle/HTML servido, `canTrackAnalytics` acepta `roggeroyroma.com` y `www.roggeroyroma.com`.
2. En **incógnito** (visitante externo) sobre `www.roggeroyroma.com`:
   - abrir una ficha `/properties/<id>` → `property_viewed` en GA4 DebugView, con `property_id`;
   - tocar el botón de WhatsApp → `click_whatsapp` en DebugView, con `cta_location`;
   - navegar `/properties` y aplicar filtro → `search_used`.
3. Logueado como `admin` o `superadmin`: **ningún** evento custom en DebugView.
4. Sin regresión de PII: ningún parámetro con teléfono, email, nombre o mensaje.
5. Los cuadritos "Fichas vistas" y "Clics de WhatsApp" del próximo informe mensual vuelven a
   mostrar valores ≠ 0.

## Validación post-deploy (a cargo de Wolfim, no de Antigravity)

1. GA4 → Admin → DebugView (o Realtime) con incógnito en `www.roggeroyroma.com`.
2. Repetir el mismo recorrido logueado como admin → debe estar vacío.
3. Comparar `page_view` vs `session_start` de los 2-3 días posteriores al fix contra el promedio
   previo. **Si `page_view` se duplica**, apagar en GA4 la Enhanced Measurement
   "Page changes based on browser history events" (queda el `page_view` manual, que es el correcto
   para el informe). Si no se duplica, no tocar nada.
4. Re-verificar que `roggeroyroma.com.ar` sigue sin servir el sitio y avisar a Franco/Marcos si
   alguien lo está usando como URL pública.

---

# RESULTADO DE LA EJECUCIÓN (2026-10-07)

Aplicado con el CLI de Antigravity (`agy.exe`, proyecto `property-pulse-nextjs`), en dos pasos:
`--mode plan` (plan revisado) y luego `--mode accept-edits`.

- Prompt ejecutado: `Hermes/Quarantine/roggero-roma-ga4-host-guard-antigravity-prompt-2026-10-07.md`
- Commit: **`1e1cd15`** en rama **`fix/ga4-tracking-hosts`** (base `729f3be`).
- Archivos: `utils/analytics.js` (+27/-8), `components/GoogleAnalytics.jsx` (+5/-3).
- No se pusheó: **el fix todavía no está en producción** → GA4 sigue en 0 hasta el deploy de `main`.
- Los 3 archivos con cambios de amenities (`PropertyEditForm.jsx`, `PropertyAddForm.jsx`,
  `PropertyDetails.jsx`) quedaron sin commitear y **no** entran en este commit.
- El repo quedó parado en la rama `fix/ga4-tracking-hosts`.

Criterios verificados por web-builder (no por Antigravity):

| Criterio | Resultado |
|---|---|
| `TRACKING_HOSTS` única; sin `allowedHosts` ni `.com.ar` en el componente | ✅ grep vacío |
| Los 4 hosts productivos permitidos | ✅ true |
| `/properties/<id>` en `www.roggeroyroma.com` | ✅ true |
| Ruta `/admin` / rol `admin` / host ajeno | ✅ false, false, false (+warn una vez) |

Pendiente: decisión de Juan sobre el push a `main` (deploy producción) y, después, la validación
en GA4 DebugView.

---

# DEPLOY Y VERIFICACIÓN END-TO-END (2026-10-07, 19:47 hs)

Juan aprobó el push. `git merge --ff-only` + `git push origin main` → **`origin/main` = `1e1cd15`**.

Deploy de Vercel verificado contra el sitio en vivo (no contra el repo):

- Chunk del layout cambió de `layout-9458207d1867a7f1.js` a **`layout-2272692414ffb05c.js`**.
- El bundle servido contiene la lista nueva:
  `["roggeroyroma.com","www.roggeroyroma.com","roggeroyroma.com.ar","www.roggeroyroma.com.ar","localhost","127.0.0.1"]`
  junto con el `Set` del warn → es el código nuevo, no una copia vieja cacheada.

Prueba en `www.roggeroyroma.com` (incógnito, visitante externo, `__USER_ROLE__ = null`):

| Acción | Resultado en `dataLayer` |
|---|---|
| Navegar a una ficha | `page_view` + **`property_viewed`** con `property_id`, `property_type`, `operation`, `location` |
| Click en CTA de WhatsApp | **`click_whatsapp`** con `contact_channel`, `cta_location`, `context` |

Recepción confirmada en GA4 (requests reales a `google-analytics.com/g/collect`, `tid=G-PW4FH9WHQB`):

```
en=page_view
en=property_viewed&ep.property_id=69fa3b194acb27ba6ab44f0e&ep.property_type=Inmueble Comercial
                  &ep.operation=venta&ep.location=Alta Gracia
```

- Sin PII en ningún parámetro ✅
- Una sola `page_view` por navegación en esta medición: el doble conteo temido **no se observó** en
  el cliente. Igual conviene comparar `page_view` vs `session_start` en el próximo informe.
- La exclusión por rol/ruta se verificó por lógica (test Node: `/admin` → false, rol `admin` →
  false), no en navegador: no se logueó una cuenta admin.

Estado final: **fix en producción y midiendo**. La validación en GA4 DebugView queda a cargo de
wolfim-growth.


