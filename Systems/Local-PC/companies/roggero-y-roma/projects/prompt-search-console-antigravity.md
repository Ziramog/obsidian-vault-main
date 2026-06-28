# Prompt para Antigravity — Conectar Search Console a Roggero & Roma

---

## Objetivo
Verificar la propiedad en Google Search Console y asociarla con GA4 para empezar a ver datos de SEO (palabras clave, posición, CTR, impresiones).

---

## Paso 1 — Verificar propiedad en Search Console (vía Web)

**Esto se hace desde la UI de Google, no requiere código. Pero verificá que el sitio esté listo.**

El sitio ya tiene en `app/layout.jsx`:
```jsx
export const metadata = {
  ...
  robots: {
    index: true,
    follow: true,
  },
};
```
✅ El sitio permite indexación. No hay bloqueo en `robots.txt` ni meta noindex.

**Instrucciones textuales para Juan (no código):**
1. Ir a https://search.google.com/search-console
2. Agregar propiedad → "URL prefix" → `https://roggeroyroma.com.ar`
3. Elegir método de verificación:

**Opción recomendada (sin tocar código): DNS TXT**
- Copiar el registro TXT que da Search Console
- Agregarlo como registro TXT en el DNS del dominio
- Esto no requiere deploy ni cambios en el sitio

**Opción alternativa si no tiene acceso al DNS: HTML tag**
- Copiar el meta tag de verificación
- Insertarlo en `app/layout.jsx` dentro del `<head>` (detalle abajo)

---

## Paso 2 — Si se necesita el meta tag (alternativa)

Si elige HTML tag, agregar en `app/layout.jsx` dentro de `export const metadata`:

```jsx
export const metadata = {
  ...
  other: {
    'google-site-verification': 'EL_CODIGO_QUE_DA_SEARCH_CONSOLE',
  },
};
```

No modificar nada más. No tocar `layout.jsx` para otra cosa.

---

## Paso 3 — Asociar Search Console con GA4

**Esto se hace desde la UI de GA4. Pasos para Juan:**
1. Ir a https://analytics.google.com/
2. Admin → Property → Property Settings → Adjust settings
3. Asociaciones de plataforma → Google Search Console → Vincular
4. Seleccionar la propiedad verificada
5. Configurar los stream(s) web asociados

---

## Paso 4 — Verificar que lleguen datos

- Search Console muestra datos históricos de hasta 3 días después de la verificación
- En GA4, ir a Reports → Acquisition → Search Console overview (aparece cuando la asociación está activa)
- En Looker Studio, se puede agregar Search Console como fuente de datos

---

## Restricciones

- NO modificar archivos del sitio a menos que sea estrictamente necesario (solo si se usa el método HTML tag)
- NO tocar `layout.jsx` si se usa DNS TXT
- NO modificar configuraciones de GA4 existentes
- NO tocar los eventos recién agregados

---

## Criterios de aceptación

- [ ] Search Console muestra la propiedad verificada
- [ ] GA4 tiene la asociación con Search Console activa
- [ ] Aparecen datos en Acquisition → Search Console overview (puede tardar hasta 48h en aparecer)
- [ ] No hay errores de build ni cambios no deseados
- [ ] El sitio sigue indexándose correctamente
