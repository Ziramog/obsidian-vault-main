# Plan de migración — wolfim.com → app.wolfim.com

**Fecha:** 2026-05-03
**Estado:** Plan — sin ejecutar
**Responsable:** Juan (necesita acceso a Vercel y Cloudflare)

---

## Situación actual

- **wolfim.com** → Vercel + Cloudflare (Next.js, sitio actual)
- **app.wolfim.com** → No existe aún
- **Stack técnico:** wolfim-dashboard (baileysconnect/apps/web) = Next.js 14 en Vercel

---

## Pregunta crítica antes de ejecutar

**¿wolfim.com (raíz) y app.wolfim.com van a apuntar al mismo proyecto Next.js en Vercel?**
- SI = un solo proyecto en Vercel con dos dominios configurados
- NO = son dos proyectos distintos (wolfim.com = landing/webagency, app.wolfim.com = dashboard)

Según lo que dijiste, wolfim.com va a tener la landing de webagency y app.wolfim.com el dashboard. Si es así → **dos proyectos Vercel separados**.

---

## Opción A — Dos proyectos separados (recomendado si wolfim.com ≠ app.wolfim.com)

### Paso 1: Configurar app.wolfim.com en Vercel (dashboard)

1. Ir a **vercel.com → proyecto wolfim-dashboard (baileysconnect/apps/web)**
2. Ir a **Settings → Domains**
3. Agregar: `app.wolfim.com`
4. Vercel va a dar un valor CNAME: `cname.vercel-dns.com` (o similar, ver en el dashboard)
5. Ir a **Cloudflare → DNS** para wolfim.com
6. Agregar registro:
   - **Type:** CNAME
   - **Name:** app
   - **Target:** `cname.vercel-dns.com`
   - **Proxy:** DNS only (no proxy de Cloudflare si es CNAME de Vercel — o sí, depende de config)

### Paso 2: Configurar wolfim.com para la landing webagency

1. Crear proyecto Vercel nuevo para la landing
2. Agregar dominio `wolfim.com` al proyecto
3. Apuntar DNS de wolfim.com (raíz/apex) al proyecto nuevo

**Para el apex domain (wolfim.com sin www):** se necesita A record, no CNAME. En Cloudflare:
- **Type:** A
- **Name:** @ (o vacío)
- **Target:** Las IPs de Vercel (76.76.21.21 para Vercel)

### Paso 3: Verificar que no se rompe nada

1. Probar wolfim.com → debe seguir respondiendo igual que antes
2. Probar app.wolfim.com → debe mostrar el dashboard de wolfim
3. Esperar propagación DNS: hasta 24-48h, pero típicamente 5-30 min

---

## Opción B — Un solo proyecto con aliases

Si wolfim.com y app.wolfim.com van a servir contenido diferente pero del mismo repo:
- Vercel permite agregar múltiples dominios al mismo proyecto
- Usar rewrites o path-based routing para separar qué se sirve en cada dominio
- **Más complejo — no recomendado para empezar**

---

## DNS en Cloudflare — configuración esperada

### Para app.wolfim.com (subdomain):
```
Type: CNAME
Name: app
Target: cname.vercel-dns.com
Proxy status: DNS only (grey cloud) — hasta verificar que funciona, luego se puede activar Cloudflare proxy (orange)
TTL: Auto
```

### Para wolfim.com (apex domain):
```
Type: A
Name: @
Target: 76.76.21.21   ← IP de Vercel
Proxy status: Proxied (orange) o DNS only — depende de si hay conflicto con Cloudflare
TTL: Auto
```

---

## Checklist de ejecución

- [ ] Confirmar si wolfim.com y app.wolfim.com son proyectos Vercel separados
- [ ] Obtener el CNAME target de Vercel para app.wolfim.com
- [ ] Agregar app.wolfim.com como dominio en el proyecto wolfim-dashboard en Vercel
- [ ] Configurar CNAME en Cloudflare para app.wolfim.com
- [ ] Probar app.wolfim.com responde correctamente
- [ ] Probar wolfim.com no se rompió (si es proyecto diferente)
- [ ] Documentar URLs finales y quién tiene acceso

---

## Notas

- Vercel genera SSL automáticamente para dominios configurados
- La propagación DNS puede tardar hasta 48h pero típicamente es rápida
- No tocar los registros DNS existentes hasta tener el nuevo funcionando
- Backup: exportar configuración actual de Vercel y Cloudflare antes de cambiar

---

## Pendiente

- [ ] Acceso a Vercel (proyecto wolfim-dashboard)
- [ ] Acceso a Cloudflare (dominio wolfim.com)
- [ ] Confirmar si wolfim.com actual se mueve o se queda donde está
