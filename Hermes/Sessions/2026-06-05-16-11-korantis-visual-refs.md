# Session 2026-06-05 16:11 — Korantis visual references (Ninina/Verne/Mishiguene)

## Pedido
Juan pasó 9 URLs de imágenes de referencia (3 venues BA × 3 c/u). Pidió descarga a disco.

## Acción
- Verificado que las URLs NO están en el scout JSON batch 01 (que tenía solo TripAdvisor/Difford's Guide). Las 9 son de **sitios oficiales** → material premium.
- HEAD check: las 9 responden 200.
- Descargadas a `companies/korantis/references/ba-venues/` con naming `NN_venue_slug.jpg`.
- Magic bytes validados: todas JPG/JFIF ✅.
- Dimensiones verificadas con PIL: rango 767² → 3063² (resolución alta, material usable como referencia).
- Generado `README.md` con manifiesto completo (URL → archivo → dimensiones → tamaño).

## Estado
✅ 9/9 descargadas. Sin bloqueos. Sin uso de cuota (curl plain, sin chrome).

## Modo
Exploración (evidence-gathering para Korantis) — permitido en 🟡 según regla activa.

## Semáforo
🟡 sin cambio. Hoy se esperaba cobro Franco $300 → semáforo a 🟠. Aún no reportado por Juan.

## Próxima acción
- Si Franco cobró → semáforo a 🟠 → mantener Korantis en modo evidence (sin outreach).
- Si NO cobró → 🟡 se mantiene → Korantis en stand-by evidencia hasta nuevo aviso.

## Archivos creados
- `companies/korantis/references/ba-venues/` (dir nuevo)
- `companies/korantis/references/ba-venues/01..09_*.jpg` (9 archivos, ~2.7 MB total)
- `companies/korantis/references/ba-venues/README.md` (manifiesto)

## Patrones detectados
- Ninguno nuevo. Juan está curando referencia visual de calidad para Korantis — actividad evidence, no comercial. Consistente con modo 🟡.
