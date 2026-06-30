# Meta Ads — Campaña Diagnóstico Wolfim

> **Estado:** Listo para publicar cuando las imágenes estén hechas.
> **Inversión:** $5 USD/día (~$150 USD/mes)
> **Destino:** https://www.wolfim.com/diagnostico

---

## Copy del anuncio

**Opción A (recomendada):**

```
Headline: Tu web tiene 3 errores que frenan consultas

Primary text:
La mayoría de las PyMEs pierde consultas por 3 errores 
básicos en su sitio web. 

Te hago un diagnóstico gratuito en 24 horas. 
Te digo exactamente qué falla y cómo se arregla. 
Sin cargo, sin compromiso.

👉 Pedilo acá
```

**Opción B (loss aversion):**

```
Headline: Si tu web tiene más de 3 años, probablemente 
esté perdiendo clientes.

Primary text:
Revisé +60 webs de PyMEs en Córdoba. El 80% tiene 
problemas que frenan consultas. WhatsApp invisible, 
datos viejos, sin certificado de seguridad.

Te digo cuáles tiene la tuya. Diagnóstico gratis en 24h.
```

---

## Imágenes

El archivo `ad-creative.html` en este handoff tiene los dos formatos listos para screenshotee:

| Formato | Tamaño | Dónde aparece |
|---------|--------|---------------|
| Feed | 1080×1080 | Feed de Facebook + Instagram |
| Stories | 1080×1920 | Stories + Reels |

**Instrucción para web-builder:** Abrir `ad-creative.html` en Chrome, usar DevTools (Ctrl+Shift+M) con las dimensiones exactas, y capturar cada bloque por separado.

---

## Configuración de campaña en Meta Ads Manager

### Paso 1 — Crear campaña

| Campo | Valor |
|-------|-------|
| Objetivo | **Tráfico** |
| Nombre | `Wolfim_Trafico_Diagnostico_PyME_2026-06` |
| Presupuesto | $5 USD/día |
| Tipo de presupuesto | Presupuesto diario |

### Paso 2 — Conjunto de anuncios

| Campo | Valor |
|-------|-------|
| Nombre | `Cordoba_PyMEs_30-60` |
| Ubicación | Argentina > Córdoba + 100km |
| Edad | 30-60 |
| Idioma | Español |
| Intereses incluidos | Pequeñas empresas, Emprendedores, Propietarios de negocios, Marketing digital |
| Excluir | Búsqueda de empleo, Recursos humanos |
| Ubicaciones | Feed, Stories, Reels (automáticas) |

### Paso 3 — Anuncio

| Campo | Valor |
|-------|-------|
| Formato | Imagen única |
| Imagen Feed | `ad-feed-1080x1080.png` (capturar del HTML) |
| Imagen Stories | `ad-stories-1080x1920.png` (capturar del HTML) |
| URL destino | `https://www.wolfim.com/diagnostico` |
| Texto principal | Copy Opción A (ver arriba) |
| Headline | ¿Tu web está perdiendo clientes? |
| Descripción | Diagnóstico gratuito en 24h |
| CTA | Más información |

---

## Qué medir (primeros 7 días)

| Métrica | Objetivo |
|---------|:--------:|
| CTR | > 1.5% |
| CPC | < $0.50 USD |
| Visitas a /diagnostico | > 30 en 7 días |
| Formularios completados | ≥ 3 en 7 días |
| Costo por lead | < $5 USD |

---

## Si no funciona (después de 7 días)

- **CTR < 1%** → probar Opción B de copy
- **CTR bueno pero pocos leads** → el problema es la landing, no el anuncio
- **CPC > $1** → ampliar intereses (quitar filtros de edad)
- **0 leads** → revisar si el formulario funciona, ajustar propuesta

---

## Checklist pre-lanzamiento

- [ ] Imágenes capturadas (1080×1080 + 1080×1920)
- [ ] Landing /diagnostico funcional (formulario manda datos)
- [ ] Cuenta Meta Ads activa con método de pago
- [ ] Copy revisado por Juan
- [ ] Campaña creada y publicada
