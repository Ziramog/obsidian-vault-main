---
id: HO-2026-07-16-001
status: ready
from: brain-vps
to: brain-local
project: ango
priority: high
depends-on: []
created-at: 2026-07-16T21:24:14-03:00
acknowledge-by: next-local-session
due-at: 2026-07-17T18:00:00-03:00
escalate-after: 24h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — web-builder — landing ANGO repuestos compatibles Urvig/Micron

## Motivo

Juan no escribe directo a web-builder por protocolo ANGO. `ango-commercial` dejó el brief formal `LOCAL_REQUEST` para que `brain-vps` cree el handoff oficial hacia local/web-builder.

Fuente obligatoria:

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-landing-repuestos-urvig-micron-2026-07-16.md
```

## Objetivo verificable

Construir una landing dedicada para **repuestos compatibles Urvig/Micron** y dejar la home actual de ANGO como destino válido para **embragues RG / tomas de fuerza industriales**, entregando **URL de preview o producción** y **rutas/archivos modificados**.

## Contexto mínimo a leer antes de tocar nada

```text
companies/ango/research/LOCAL_REQUEST-webbuilder-ango-landing-repuestos-urvig-micron-2026-07-16.md
companies/ango/projects/google-ads-2026-06/campana-definitiva-google-ads-ango-2026-07-16.md
companies/ango/intelligence/google-ads-keyword-planner-2026-analisis.md
companies/ango/intelligence/context.md
companies/ango/intelligence/patterns.md
companies/ango/research/assets/ango-web-current-home-2026-07-16.png
```

## Lo que hay que hacer

1. Crear una página dedicada para búsquedas de alta intención sobre repuestos compatibles Urvig/Micron.
2. Mantener la home actual de ANGO enfocada en RG / PTO industrial.
3. Si se toca la home, corregir wording para evitar confusión entre línea RG y compatibles Urvig/Micron.
4. Respetar la aclaración comercial/legal: **compatibles**, no originales ni representación oficial.
5. Dejar CTA claro a WhatsApp/teléfono/formulario y comportamiento mobile-first.
6. Preparar la página para uso con Google Ads (URL estable + UTM compatible).
7. Si no se implementa tracking ahora, dejar IDs/classes claros para luego conectar GA4/Google Ads.

## Requisitos técnicos mínimos

- URL sugerida: `/repuestos-compatibles-urvig-micron`
- Alternativas aceptables: `/repuestos-urvig-micron` o `/repuestos-compatibles`
- SEO title + meta description orientados a repuestos compatibles Urvig/Micron
- H1 único: `Repuestos compatibles para Urvig y Micron`
- Botón WhatsApp visible en mobile
- Formulario corto o CTA equivalente
- Carga rápida en mobile
- No bloquear indexación salvo decisión explícita
- No usar claims como `original`, `oficial`, `distribuidor oficial`, `representante oficial`, `service oficial`

## Criterios de aceptación

- Existe landing dedicada para Urvig/Micron
- La home sigue siendo destino válido para productos RG/PTO
- La landing no usa claims prohibidos
- La landing pide modelo/foto/compatibilidad en forma clara
- Funciona bien en mobile
- Hay CTA directo a WhatsApp/teléfono/formulario
- Se entrega URL de preview o producción
- Se indican archivos/rutas modificados

## Restricciones

- No modificar `Hermes/Config/`
- No tocar secrets, tokens ni `.env`
- No hacer cambios destructivos
- No usar `git reset --hard`, `git clean` ni `push --force`
- Si hay dudas de copy/compliance sobre `original/oficial`, prevalece el brief `LOCAL_REQUEST`

## Respuesta esperada en este handoff

Publicar `response.md` en esta carpeta con:

- URL de preview o producción
- archivos/rutas modificados
- notas sobre home vs landing
- cualquier bloqueo concreto si algo impide terminar
