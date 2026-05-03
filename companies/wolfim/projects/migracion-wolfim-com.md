# Migración wolfim.com → app.wolfim.com

## Estado actual

- `wolfim.com` = dashboard WA automation (Vercel + Supabase + login) → conecta a `wolfim-agent` en VPS
- 0 clientes WA automation
- 1 cliente webagency (Franco Roma) — sin portal, sin pagos online
- Pagos WA automation: Mercado Libre + Lemon Squeezy (futuro, no urgente)
- Todo en GitHub

---

## Arquitectura objetivo

```
app.wolfim.com (Vercel)
└── Dashboard WA automation
    ├── Login clientes WA
    ├── Gestión de cuenta
    └── Pagos (Mercado Libre / Lemon Squeezy — cuando haya clientes)
    Conecta a wolfim-agent en VPS

wolfim.com (Vercel — proyecto separado)
├── Landing webagency (pública)
├── /login → portal clientes webagency
├── /dashboard → gestión de cuenta, pagos mantenimiento
└── Franco Roma se loguea y paga desde acá
```

---

## Plan de ejecución

### Fase 1 — Crear app.wolfim.com (migración pura)

1. En Vercel: crear nuevo proyecto `app.wolfim.com` apuntando al mismo repo GitHub de wolfim.com
2. En Cloudflare: agregar registro CNAME `app` → Vercel (proxy activo)
3. Verificar que `app.wolfim.com` responde igual que `wolfim.com` hoy
4. **No tocar wolfim.com todavía**

### Fase 2 — Reconvertir wolfim.com a webagency

1. En el repo de wolfim.com: reemplazar dashboard WA por landing webagency
2. Construir portal clientes webagency:
   - Login con Supabase Auth (mismo que ya tienen)
   - Dashboard simple: ver estado del proyecto, historial de pagos
   - Sistema de pagos: **Stripe** (rápido de integrar con Supabase) o **Mercado Pago** (más conocido en Latam)
   - Franco Roma como cliente inicial (login creado, accede a su cuenta)
3. Desplegar y verificar

### Fase 3 — Pagos WA automation (futuro, sin prisa)

1. Cuando aparezca el primer cliente WA:
   - Integrar Stripe o Mercado Pago en `app.wolfim.com`
   - Plan básico: $X setup + $Y/mes mantenimiento
   - Conectar con `wolfim-agent` en VPS

---

## Decisiones pendientes

| Decisión | Opciones | Recomendación |
|---|---|---|
| Payment provider webagency | Stripe / Mercado Pago | Stripe (supabase billing nativo, 1 día de集成) |
| Precio mantenimiento webagency | ¿$25/mes como Franco? | Confirmar con Juan |
| Repo para app.wolfim.com | Mismo repo + deploy separado | Mismo repo, 2 deploys Vercel |
| Dominio extra en Vercel | app.wolfim.com como alias | Sí, agregar dominio en Vercel |

---

## Tiempo estimado

- Fase 1: 30 min (configurar Vercel + Cloudflare)
- Fase 2: 2-4 horas (landing + portal + pagos webagency)
- Fase 3: cuando aparezca cliente WA

---

## Orden de ejecución

1. ✅ Documentar plan (este archivo)
2. ⏳ Juan confirma plan
3. ⏳ Ejecutar Fase 1 (app.wolfim.com)
4. ⏳ Ejecutar Fase 2 (wolfim.com → webagency)
5. ⏳ Franco Roma accede a portal y paga mantenimiento online
