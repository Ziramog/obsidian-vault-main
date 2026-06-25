# Handoffs — estructura de coordinación entre VPS y local

Cada handoff es una carpeta con archivos inmutables. No se edita `request.md` después de creado.

## Estructura

```
Hermes/Handoffs/
├── vps-to-local/
│   └── HO-YYYY-MM-DD-NNN/
│       ├── request.md       ← Creado por brain-vps. Inmutable.
│       ├── response.md      ← Creado por brain-local cuando completa.
│       └── events/           ← Línea de tiempo inmutable
│           ├── YYYY-MM-DDTHH-mm-created.md
│           ├── YYYY-MM-DDTHH-mm-ack.md
│           └── YYYY-MM-DDTHH-mm-done.md
├── local-to-vps/
│   └── (misma estructura)
└── archive/
```

## Formato request.md

```yaml
---
id: HO-YYYY-MM-DD-NNN
status: ready|acknowledged|done|cancelled
from: brain-vps|brain-local
to: brain-local|brain-vps
project: wolfim|ango|construvial|korantis|system
priority: high|medium|low
created-at: ISO8601
acknowledge-by: next-local-session|descripción
due-at: ISO8601
escalate-after: 4h|8h|24h
briefing: Hermes/Briefings/current.md
director: Juan
---
```

Body: objetivo verificable, contexto mínimo, rutas relevantes, restricciones, criterios de aceptación, riesgos, qué debe devolver el destino.

## Formato response.md

```yaml
---
id: HO-YYYY-MM-DD-NNN
status: done|cancelled
from: brain-local|brain-vps
to: brain-vps|brain-local
completed-at: ISO8601
---
```

Body: trabajo realizado, archivos tocados, tests/verificaciones, decisiones técnicas, bloqueos, siguientes pasos, si requiere decisión de Juan.

## Escalado

brain-vps revisa handoffs con `status: ready` al inicio de cada sesión. Si el tiempo desde `created-at` supera `escalate-after`, agrega entrada en `Hermes/Daily/` con flag de atención para Juan. No cancela ni reasigna el handoff.

## Archivado

Handoffs con `status: done` o `cancelled` con más de 30 días se mueven a `archive/`.
