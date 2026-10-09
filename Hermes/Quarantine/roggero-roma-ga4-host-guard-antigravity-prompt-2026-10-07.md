---
type: ANTIGRAVITY_PROMPT
company: wolfim
client: roggero-roma
target: antigravity
repo: C:\Projects\property-pulse-nextjs
commit-base: 729f3be
origen: LOCAL_REQUEST-webbuilder-roggero-restaurar-eventos-ga4-2026-10-07
estado: listo-para-ejecutar
zona: Hermes/Quarantine
---

# Restaurar eventos custom de GA4 (allowlist de hosts del guard de analytics)

## Objetivo

Restaurar el envío de los eventos custom de GA4 del sitio de Roggero & Roma corrigiendo el
allowlist de hosts del guard de analytics, sin tocar la exclusión de tráfico interno.

## Contexto del proyecto

- Repo: `C:\Projects\property-pulse-nextjs` (Next.js 14.2.4 App Router, rama `main`, deploy Vercel).
- Sitio productivo: `https://www.roggeroyroma.com` (`roggeroyroma.com` redirige a `www`).
- GA4 `G-PW4FH9WHQB`, inyectado por `components/GoogleAnalytics.jsx` con `send_page_view: false`
  y `page_view` manual. El ID no se hardcodea: viene de `siteConfig.analyticsId`.
- Todos los eventos pasan por `trackEvent()` en `utils/analytics.js`, que aplica
  `canTrackAnalytics({ host, pathname, role })`.
- **Bug verificado en el bundle de producción el 2026-10-07**: `isAllowedTrackingHost()` sólo
  permite hosts `.com.ar` (`roggeroyroma.com.ar`, `www.roggeroyroma.com.ar`, `localhost`,
  `127.0.0.1`), pero el sitio vive en `www.roggeroyroma.com`. Resultado: `canTrackAnalytics()`
  devuelve `false` para todo visitante externo y `trackEvent()` descarta **en silencio**
  `property_viewed`, `click_whatsapp`, `click_phone`, `click_maps`, `click_social`, `search_used`,
  `form_submit` y también el `page_view` manual.
- `components/GoogleAnalytics.jsx` tiene una **segunda lista de hosts duplicada** que sí incluye
  `.com`, así que el script de gtag se carga igual y el fallo es invisible en el navegador.

## Tarea

### Bloque 1 — Fuente única de hosts permitidos (`utils/analytics.js`)

1. Definir y exportar una constante única:

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

2. Reescribir `isAllowedTrackingHost(hostname)` para que sea
   `TRACKING_HOSTS.includes(hostname)`. Eliminar el array local `allowedHosts` que está dentro de
   esa función.

3. En `canTrackAnalytics()`, cuando el descarte sea **por host**, emitir un aviso una sola vez por
   `hostname` por sesión (flag a nivel de módulo), para que el fallo no vuelva a ser silencioso:

```js
console.warn(`[analytics] host no permitido: ${host} — evento descartado`);
```

   Debe seguir devolviendo `false`. No cambiar el comportamiento de los otros dos chequeos
   (path y rol).

### Bloque 2 — Eliminar la lista duplicada (`components/GoogleAnalytics.jsx`)

4. Importar `TRACKING_HOSTS` desde `@/utils/analytics` y usarla en los **dos** lugares donde hoy
   está el array local `allowedHosts`:
   - dentro del `useEffect` (hoy la lista no se usa ahí, pero verificar que no quede una copia),
   - en el early-return de render: `if (!TRACKING_HOSTS.includes(hostname)) return null;`.

5. No debe quedar ninguna lista de hosts duplicada en el repo.

### Bloque 3 — Sin cambios de contrato

6. No renombrar eventos ni parámetros. `property_viewed`, `click_whatsapp`, `click_phone`,
   `click_maps`, `click_social`, `search_used`, `form_submit` se mantienen tal cual.

Los bloques 1 y 2 van juntos en un solo cambio: separados, el componente sigue con su lista vieja.

## Archivos a tocar

- `utils/analytics.js`
- `components/GoogleAnalytics.jsx`

## Entorno de ejecución

- Nodo que sirve al usuario: el deploy de Vercel de `main` sobre `www.roggeroyroma.com`.
- Ejecutar todo en el nodo local, repo `C:\Projects\property-pulse-nextjs`.
- Shell: git-bash (MSYS) sobre Windows. Los paths para binarios nativos van con `/` nativo
  (`C:/Projects/...`), no con `/c/...`.
- Variables de entorno: ninguna requerida para este cambio. No leer ni escribir `.env*`.
- **No ejecutar `git`** (ni add, ni commit, ni checkout, ni push): el commit y el push los maneja
  el operador fuera de esta sesión.
- No ejecutar `npm run build`, `npm run dev` ni `npm start`.

## Restricciones

- NO tocar la exclusión por rol (`admin` / `superadmin`) ni las rutas `/admin`, `/superadmin`, `/api`.
- NO agregar hosts de preview ni dominios `*.vercel.app` al allowlist.
- NO renombrar eventos ni parámetros.
- NO enviar PII a GA4.
- NO hardcodear el Measurement ID.
- NO tocar los cambios sin commitear que ya existen en `components/PropertyEditForm.jsx`,
  `components/PropertyAddForm.jsx` y `components/PropertyDetails.jsx` (son de otro trabajo:
  amenities). Deben quedar exactamente como están.
- NO crear archivos nuevos dentro del repo. Cualquier script de verificación va temporal y se borra.

## Criterios de aceptación

Ejecutar cada comando y pegar la salida completa en el reporte. Omitir uno invalida la entrega.

1. Fuente única y sin duplicados:

```
grep -n "TRACKING_HOSTS" utils/analytics.js components/GoogleAnalytics.jsx
grep -rn "roggeroyroma.com.ar" components/GoogleAnalytics.jsx   # debe salir vacío (exit 1)
grep -rn "allowedHosts" utils/analytics.js components/GoogleAnalytics.jsx  # debe salir vacío
```

2. Prueba funcional del guard (happy path y casos negativos). Esperado exacto:
   `true / true / false / false / false`:

```
node -e "const fs=require('fs');let s=fs.readFileSync('utils/analytics.js','utf8').replace(/export /g,'');eval(s);const hosts=['roggeroyroma.com','www.roggeroyroma.com','roggeroyroma.com.ar','www.roggeroyroma.com.ar','localhost','127.0.0.1'];console.log(hosts.every(h=>isAllowedTrackingHost(h)));console.log(canTrackAnalytics({host:'www.roggeroyroma.com',pathname:'/properties/6abfbad72f088d924f671197',role:null}));console.log(canTrackAnalytics({host:'www.roggeroyroma.com',pathname:'/admin',role:null}));console.log(canTrackAnalytics({host:'www.roggeroyroma.com',pathname:'/properties',role:'admin'}));console.log(canTrackAnalytics({host:'evil.example.com',pathname:'/properties',role:null}));"
```

3. Solo dos archivos modificados (además de los 3 que ya estaban sucios antes de empezar):

```
git status --porcelain
git diff --stat -- utils/analytics.js components/GoogleAnalytics.jsx
```

4. Reportar el diff completo de los dos archivos (`git diff -- utils/analytics.js components/GoogleAnalytics.jsx`).

## Modo de entrega

- Rama: se trabaja sobre `main` local. **Sin commit y sin push desde esta sesión**: el operador
  revisa el diff, commitea y decide el deploy.
- Dejar el árbol en el estado "2 archivos modificados por este cambio + 3 archivos ya sucios antes".

## Fuera de alcance (no hacer)

- La verificación en GA4 DebugView sobre `www.roggeroyroma.com` la hace Wolfim después del deploy:
  incógnito → abrir ficha → `property_viewed`; click WhatsApp → `click_whatsapp`; logueado como
  admin → ningún evento.
- El posible doble conteo de `page_view` (Enhanced Measurement vs el `page_view` manual) se evalúa
  después del deploy comparando `page_view` contra `session_start`.
