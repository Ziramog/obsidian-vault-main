# Deploy — wolfim-ag.vercel.app → wolfim.com

**Meta:** Migrar la landing webagency (wolfim-ag.vercel.app) a wolfim.com, con precios actualizados y estructura de planes.

---

## 1. Precios a mostrar en la landing

| Plan        | Setup USD | Mantenimiento USD/mes |
| ----------- | --------- | --------------------- |
| Landing     | $200      | $29                   |
| Profesional | $300      | $29                   |
| depCatálogo | $450      | $49                   |
| Ecommerce   | $450      | $89                   |

Los precios van en la sección de planes (no en la home).

---

## 2. Estructura de navegación (nueva)

```
Páginas Web / Posicionamiento Google / Mantenimiento y Hosting / WhatsApp Automation
```

**Qué va en cada sección:**
- **Páginas Web:** 4 planes (Landing / Profesional / Catálogo / Ecommerce) con precios y features
- **Posicionamiento Google:** Google Ads como servicio separado + SEO
- **Mantenimiento y Hosting:** Los 3 tiers de mantenimiento ($29 / $49 / $89)
- **WhatsApp Automation:** Servicio de bots WA (código o玄份? — deja de momento como está)

---

## 3. Add-ons (sección separada, no tabla comparativa)

- Reservas online: +$100-150 USD
- Google Ads setup: +$150 USD
- SEO premium: +$75 USD

Add-ons visibles solo en contacto o en sección dedicada — no en la сравнительная tabla.

---

## 4. Copy clave a mantener

- "Creamos Depredadores" (o similar)
- "50% adelantado para empezar"
- Botón WhatsApp directo en todos los planes

---

## 5. Deploy steps (Claude Code)

1. Clonar el repo de wolfim-ag (o usar el existente en GitHub)
2. Actualizar `/servicios` con los precios nuevos de la tabla arriba
3. Crear sección "Planes" con los 4 planes base y precios
4. Crear sección "Mantenimiento" con los 3 tiers
5. Agregar CNAME en Cloudflare apuntando wolfim.com → Vercel
6. Deployar en Vercel con dominio wolfim.com
7. Verificar que todo ande en wolfim.com

---

## 6. Notas

- Mantener el stack actual (Next.js + Vercel)
- No romper nada del dashboard WA que está en wolfim.com actualmente — eso se migra después a app.wolfim.com
- Franco Roma es cliente existente de webagency — no cambiar nada de su proyecto
- Payment provider para webagency: decisión pendiente (Stripe o Mercado Pago)
