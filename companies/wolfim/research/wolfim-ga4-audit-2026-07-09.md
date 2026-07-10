# Auditoría GA4 — wolfim.com

**Fecha:** 2026-07-09 21:35 ART  
**Propiedad GA4:** `wolfim.com`  
**Property ID:** `539238403`  
**Measurement ID:** `G-D7E290M8PW`  
**Rango auditado:** 2026-06-09 a 2026-07-08, últimos 30 días completos.

---

## 1. Acceso confirmado

El service account de Hermes ya ve la cuenta GA4 de Wolfim.

- Cuenta: `WOLFIM`
- Propiedad: `wolfim.com`
- Data stream: `WOLFIM Website`
- URL default: `https://www.wolfim.com`
- Zona horaria: `America/Buenos_Aires`
- Moneda: `USD`

---

## 2. Instalación técnica pública

El sitio público carga GA4 correctamente.

- `https://wolfim.com` redirige a `https://www.wolfim.com/`
- Se detecta un solo measurement ID: `G-D7E290M8PW`
- No se detectó GTM (`GTM-...`)
- Implementación actual: `gtag.js` directo
- Snippet detectado:

```js
gtag('config', 'G-D7E290M8PW');
```

**Lectura:** la medición básica está activa. Pageviews y eventos automáticos llegan. No hay evidencia de duplicación de tag.

---

## 3. Resumen últimos 30 días

| Métrica | Valor |
|---|---:|
| Usuarios activos | 249 |
| Usuarios totales | 249 |
| Usuarios nuevos | 247 |
| Sesiones | 353 |
| Sesiones con engagement | 117 |
| Vistas de página | 553 |
| Eventos totales | 1.618 |
| Key events / conversiones | 0 |
| Engagement rate | 33,14% |
| Bounce rate | 66,86% |

**Lectura comercial:** el sitio está recibiendo tráfico real, pero GA4 todavía no está configurado para mostrar conversiones útiles. El problema no es que no haya eventos: el problema es que los eventos comerciales no están marcados como key events.

---

## 4. Eventos detectados

| Evento | Cantidad | Usuarios | Key events |
|---|---:|---:|---:|
| `page_view` | 553 | 249 | 0 |
| `session_start` | 358 | 249 | 0 |
| `first_visit` | 247 | 245 | 0 |
| `user_engagement` | 219 | 33 | 0 |
| `scroll` | 190 | 95 | 0 |
| `click_project` | 18 | 4 | 0 |
| `click` | 8 | 3 | 0 |
| `view_pricing` | 8 | 7 | 0 |
| `click_whatsapp` | 6 | 2 | 0 |
| `form_start` | 4 | 1 | 0 |
| `form_submit_diagnostico` | 3 | 1 | 0 |
| `click_service` | 2 | 2 | 0 |
| `whatsapp_click` | 2 | 1 | 0 |

### Problema principal

Actualmente están configurados como conversiones/key events:

- `close_convert_lead`
- `qualify_lead`
- `purchase`

Pero esos eventos **no aparecen** en los últimos 30 días.

Los eventos reales que sí tienen intención comercial son:

- `click_whatsapp`
- `whatsapp_click`
- `form_submit_diagnostico`
- `form_start`
- `view_pricing`

**Conclusión:** GA4 está midiendo, pero el tablero comercial está mal conectado. Hay contactos/interacciones, pero GA4 marca 0 conversiones.

---

## 5. Tráfico por canal

| Canal | Fuente / Medio | Sesiones | Usuarios | Engaged sessions | Vistas |
|---|---|---:|---:|---:|---:|
| Paid Social | `meta / paid_social` | 149 | 150 | 24 | 174 |
| Direct | `(direct) / (none)` | 141 | 40 | 79 | 314 |
| Organic Search | `google / organic` | 38 | 38 | 3 | 38 |
| Referral | `vercel.com / referral` | 8 | 5 | 5 | 9 |
| Organic Social | `facebook.com / referral` | 5 | 5 | 4 | 5 |
| Organic Social | `m.facebook.com / referral` | 5 | 5 | 0 | 5 |
| Organic Search | `bing / organic` | 4 | 4 | 0 | 4 |
| AI Assistant | `chatgpt.com / ai-assistant` | 1 | 1 | 1 | 1 |
| Organic Social | `instagram.com / referral` | 1 | 1 | 1 | 1 |
| Organic Social | `l.instagram.com / referral` | 1 | 1 | 0 | 1 |
| Referral | `lucxspace.com / referral` | 1 | 1 | 0 | 1 |

### Lectura comercial

- Meta Ads está trayendo el mayor volumen de sesiones: 149.
- Directo tiene menos usuarios, pero mucha más profundidad: 141 sesiones, 314 vistas.
- Google orgánico existe, pero con baja profundidad: 38 sesiones, 38 vistas.
- Hay tráfico de `vercel.com`, probablemente interno/técnico. Conviene excluirlo o no leerlo como lead real.

---

## 6. Páginas principales

| Página | Vistas | Usuarios | Sesiones | Key events |
|---|---:|---:|---:|---:|
| `/` | 312 | 96 | 185 | 0 |
| `/diagnostico` | 208 | 157 | 169 | 0 |
| `/inmobiliarias` | 31 | 6 | 15 | 0 |
| `/Juan_AI_CV` | 2 | 1 | 3 | 0 |

### Lectura comercial

`/diagnostico` está funcionando como landing real: 157 usuarios y 169 sesiones. Pero como sus eventos no son conversiones, GA4 no refleja el valor comercial de la campaña.

---

## 7. Landing pages

| Landing page | Sesiones | Usuarios | Engaged sessions | Key events |
|---|---:|---:|---:|---:|
| `/` | 168 | 92 | 75 | 0 |
| `/diagnostico` | 162 | 157 | 30 | 0 |
| `(not set)` | 15 | 4 | 3 | 0 |
| `/inmobiliarias` | 9 | 4 | 8 | 0 |
| `/Juan_AI_CV` | 1 | 1 | 1 | 0 |

**Dato fuerte:** `/diagnostico` trae casi tantos ingresos como la home, pero con menor engagement. Hay que mirar si la landing está filtrando rápido o si falta tracking fino de clicks/formulario.

---

## 8. Dispositivos

| Dispositivo | Sesiones | Usuarios | Engaged sessions | Vistas |
|---|---:|---:|---:|---:|
| Mobile | 228 | 176 | 66 | 333 |
| Desktop | 142 | 77 | 65 | 218 |
| Tablet | 2 | 1 | 1 | 2 |

**Lectura:** Mobile trae más volumen; desktop tiene proporcionalmente mejor engagement. Las campañas y CTAs tienen que estar revisadas primero en móvil.

---

## 9. Países

| País | Sesiones | Usuarios | Vistas |
|---|---:|---:|---:|
| Argentina | 285 | 179 | 481 |
| United States | 59 | 60 | 61 |
| Germany | 2 | 2 | 3 |
| Otros | 8 | 8 | 8 |

**Lectura:** Argentina concentra el tráfico útil. Estados Unidos aparece con navegación muy superficial; no debería condicionar decisiones comerciales.

---

## 10. Interacciones comerciales por página

| Evento | Página | Cantidad | Usuarios |
|---|---|---:|---:|
| `click_project` | `/` | 18 | 4 |
| `view_pricing` | `/` | 8 | 7 |
| `click` | `/` | 4 | 2 |
| `click` | `/diagnostico` | 4 | 2 |
| `click_whatsapp` | `/diagnostico` | 4 | 2 |
| `form_start` | `/diagnostico` | 4 | 1 |
| `form_submit_diagnostico` | `/diagnostico` | 3 | 1 |
| `click_service` | `/` | 2 | 2 |
| `click_whatsapp` | `/` | 2 | 1 |
| `whatsapp_click` | `/` | 2 | 1 |

### Problemas detectados

1. Hay dos nombres para WhatsApp:
   - `click_whatsapp`
   - `whatsapp_click`

   Esto fragmenta la medición.

2. Además existe el evento automático `click`, que también registra links a WhatsApp. Eso puede generar lecturas duplicadas o confusas si se mezcla con eventos manuales.

3. `form_submit_diagnostico` existe y es valioso, pero no está marcado como conversión.

---

## 11. Links de WhatsApp detectados por GA4

| Link | Eventos | Usuarios |
|---|---:|---:|
| `wa.me/5493513157202?...diagnóstico gratuito...` | 4 | 2 |
| `wa.me/5491173858454?...interesado en un sitio web` | 1 | 1 |
| `wa.me/5491173858454?...consultar por un proyecto` | 1 | 1 |
| `wa.me/5493513157202?...Presencia Comercial` | 1 | 1 |
| `wa.me/5493513157202?...solución...` | 1 | 1 |

### Alerta

Aparecen dos números distintos:

- `5493513157202`
- `5491173858454`

Hay que confirmar si ambos son correctos. Si `5491173858454` es viejo o no corresponde, hay fuga de leads.

---

## 12. Prioridades de corrección

### Prioridad 1 — Marcar conversiones correctas

Configurar como key events en GA4:

- `form_submit_diagnostico`
- `click_whatsapp`
- `view_pricing` opcional, como micro-conversión

Y decidir qué hacer con:

- `whatsapp_click` → idealmente dejar de emitirlo o unificarlo con `click_whatsapp`.

### Prioridad 2 — Unificar naming

Usar una sola convención:

- `click_whatsapp`
- `form_submit_diagnostico`
- `view_pricing`
- `click_project`
- `click_service`

Evitar duplicar `whatsapp_click`.

### Prioridad 3 — Registrar parámetros custom

Crear dimensiones personalizadas en GA4 para poder leer mejor cada evento:

- `cta_location`
- `cta_text`
- `service_name`
- `project_name`
- `plan_name`
- `form_name`
- `whatsapp_number`
- `page_context`

Hoy GA4 no tiene custom dimensions configuradas.

### Prioridad 4 — Revisar número de WhatsApp

Confirmar si `5491173858454` debe seguir en producción. Si no, cambiar todo a `5493513157202`.

### Prioridad 5 — Excluir/refinar tráfico técnico

`vercel.com / referral` aparece con 8 sesiones. No es grave, pero para reportes comerciales conviene no mezclarlo con clientes reales.

---

## 13. Diagnóstico final

GA4 de Wolfim **sí está instalado y recibiendo datos**, pero todavía no sirve como tablero comercial completo porque:

1. Las conversiones configuradas no coinciden con los eventos reales.
2. WhatsApp está medido con nombres duplicados.
3. Hay eventos útiles, pero no están marcados como key events.
4. Faltan custom dimensions para saber qué CTA, servicio o plan generó la acción.
5. Hay que verificar si todos los links de WhatsApp apuntan al número correcto.

**Conclusión comercial:** Wolfim ya tiene datos suficientes para medir campañas, especialmente `/diagnostico`, pero primero hay que ordenar conversiones. Sin eso, GA4 va a seguir diciendo “0 conversiones” aunque haya formularios y clicks reales.
