---
title: Meta Ads Launch — Wolfim Diagnóstico
company: wolfim
date: 2026-07-03
status: ready-to-create
landing: https://www.wolfim.com/diagnostico
budget: 5 USD/day
owner: Juan
---

# Meta Ads Launch — Wolfim Diagnóstico

## Objetivo de negocio

Conseguir leads de dueños de PyMEs/negocios con sitio web débil, viejo o mal orientado a consultas.

La campaña NO vende una web directamente. Vende una acción de baja fricción:

> Diagnóstico gratuito: detectar 3 errores que frenan consultas.

---

## Pre-launch check

- Landing live: `https://www.wolfim.com/diagnostico`
- H1 live: `Tu web tiene 3 errores que frenan consultas`
- Formulario: nombre + web + WhatsApp
- Submit frontend: `POST /api/leads`
- Éxito: muestra mensaje de gracias
- WhatsApp: fallback/secundario, no submit principal
- Creatividades listas:
  - `creative/ad-feed-safe-1080x1350.png`
  - `creative/ad-reels-safe-1080x1920.png`
- Nota 2026-07-03: se regeneraron versiones safe porque Meta recortaba la línea “En 24 horas” en Reels.

---

## Campaña

| Campo | Valor |
|---|---|
| Plataforma | Meta Ads Manager |
| Objetivo | Leads si permite usar sitio web/formulario; si no, Tráfico |
| Nombre campaña | `WOLFIM_DIAGNOSTICO_LEADS_CBA_2026-07-03` |
| Compra | Subasta |
| Presupuesto | USD 5/día |
| Estrategia | Menor costo |
| Estado inicial | Publicar si método de pago está OK |

### Decisión objetivo

**Opción preferida:** Leads / conversiones en sitio web si el evento `Lead` está disponible.

**Opción segura si Meta no detecta evento:** Tráfico hacia landing.

No bloquear el lanzamiento por Pixel si no está 100% listo. Con USD 5/día, primero buscamos señales reales.

---

## Conjunto de anuncios

| Campo | Valor |
|---|---|
| Nombre ad set | `CBA_PYMES_DUENOS_30-60_ADVANTAGE` |
| Conversión / destino | Sitio web |
| URL | `https://www.wolfim.com/diagnostico` |
| Presupuesto | Usar presupuesto de campaña |
| Inicio | Inmediato |
| Ubicación | Argentina — Córdoba + alrededores |
| Edad | 30-60 |
| Género | Todos |
| Idioma | Español |
| Ubicaciones | Advantage+ placements, pero revisar que Feed + Stories/Reels estén activos |
| Optimización | Landing page views si campaña es Tráfico; Leads si campaña es Leads |

### Segmentación recomendada

#### Primera opción — Broad controlado

Usar público amplio con límites:

- Argentina, Córdoba y alrededores.
- Edad 30-60.
- Sin intereses restrictivos o con Advantage detailed targeting activado.

Motivo: Meta necesita margen para aprender. El copy filtra por dolor.

#### Si Meta exige/intereses o el público queda demasiado amplio

Agregar intereses como orientación, no como filtro ultra cerrado:

- Emprendimiento
- Pequeñas empresas
- Marketing digital
- Comercio minorista
- Negocio local
- Administradores de páginas de Facebook, si aparece disponible

No usar solo “diseño web”, porque atrae otros diseñadores/agencias.

---

## Anuncio principal

| Campo | Valor |
|---|---|
| Nombre anuncio | `A1_Checklist_3Errores_1080x1350` |
| Formato | Imagen única |
| Imagen principal | `ad-feed-safe-1080x1350.png` |
| Imagen stories/reels | `ad-reels-safe-1080x1920.png` |
| URL destino | `https://www.wolfim.com/diagnostico` |
| CTA | Más información |

### Primary text

```text
La mayoría de las PyMEs pierde consultas por errores básicos en su sitio web.

Te hago un diagnóstico gratuito en 24 horas: reviso tu web y te digo 3 mejoras concretas para que transmita más confianza y genere más consultas.

Sin cargo. Sin compromiso.
```

### Headline

```text
Tu web tiene 3 errores que frenan consultas
```

### Description

```text
Diagnóstico gratuito en 24h
```

---

## UTM recomendadas

URL final con UTMs:

```text
https://www.wolfim.com/diagnostico?utm_source=meta&utm_medium=paid_social&utm_campaign=diagnostico_pymes_cba_2026_07&utm_content=checklist_3_errores
```

---

## Métricas primeras 72 horas

No optimizar antes de 72h salvo que haya error técnico.

| Métrica | Objetivo inicial |
|---|---:|
| CTR link | > 1.2% |
| CPC | < USD 0.50 |
| Landing page views | > 20 |
| Leads Supabase | >= 1-3 |
| CPL inicial | < USD 10 |
| Calidad lead | negocio real + web revisable + WhatsApp válido |

---

## Regla de decisión a las 72h

### Si hay clics pero no leads

Problema probable: landing/formulario/propuesta. Revisar:

- Formulario funciona en mobile.
- `/api/leads` guarda correctamente.
- Botón no manda a WhatsApp antes de guardar.
- Mensaje demasiado poco claro.

### Si CTR bajo

Problema probable: creatividad/copy. Probar variante B:

```text
Tu web puede estar espantando clientes
```

### Si leads malos

Problema probable: targeting demasiado amplio o copy demasiado genérico. Agregar filtro de público o cambiar copy hacia “negocios con web”.

---

## Próxima variante para test

No lanzar todavía. Guardar para después de 72h.

```text
Tu web puede estar espantando clientes

Te digo qué corregir.
Diagnóstico gratuito en 24h.
```

---

## Checklist final antes de publicar

- [ ] Hacer un lead de prueba y confirmar que aparece en Supabase.
- [ ] Confirmar método de pago Meta activo.
- [ ] Subir imagen feed 1080x1350.
- [ ] Subir imagen stories 1080x1920.
- [ ] Usar URL con UTMs.
- [ ] Publicar con USD 5/día.
- [ ] No tocar durante primeras 72h salvo error técnico.
