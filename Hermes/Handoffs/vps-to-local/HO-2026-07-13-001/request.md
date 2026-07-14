---
id: HO-2026-07-13-001
status: ready
from: brain-vps
to: brain-local
project: hermes-system
priority: high
depends-on: []
created-at: 2026-07-13T21:21:23-03:00
acknowledge-by: next-local-session
due-at: 2026-07-14T12:00:00-03:00
escalate-after: 12h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — Propagar directiva Sync V6 a profiles locales

## Motivo

Juan corrigió explícitamente que las reglas sistémicas no pueden depender de que él las repita profile por profile. El incidente 2026-07-13 fue: archivos escritos por `wolfim-growth` con trailing whitespace bloquearon Sync V6 (`git diff --cached --check`) y el handoff no llegó a GitHub/local hasta corrección manual.

brain-vps ya propagó la regla a profiles VPS. Falta hacer lo mismo en local.

## Objetivo verificable

Actualizar los SOUL reales / configuración equivalente de los profiles locales para que carguen la directiva obligatoria de escritura y Sync V6:

- `brain-local`
- `web-builder`
- `web-auditor`
- `pc-ops`

## Documentos ya versionados en el vault

Leer primero:

```text
Hermes/Systems/vps/profile-write-directive-2026-07-13.md
Hermes/Systems/vps/scripts/profile-write-check.py
Hermes/Profiles/local/brain-local.md
Hermes/Profiles/local/web-builder.md
Hermes/Profiles/local/web-auditor.md
Hermes/Profiles/local/pc-ops.md
```

## Instrucción a aplicar en SOUL/config local

Cada profile local debe tener una regla equivalente:

1. No escribir trailing whitespace en `.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`, `.toml`.
2. No usar dos espacios al final de línea para saltos Markdown. Usar línea en blanco o `<br>`.
3. Si una salida es para otro profile, otro host o Juan, debe pasar `profile-write-check.py` o chequeo equivalente antes de cerrar.
4. Si requiere coordinación VPS ↔ local, usar handoff oficial:
   - entrada: `Hermes/Handoffs/vps-to-local/`
   - devolución: `Hermes/Handoffs/local-to-vps/`
5. No cerrar como “listo” si el chequeo falla o si hay duda de visibilidad en GitHub.
6. brain-local debe propagar esta regla a web-builder, web-auditor y pc-ops. Juan no debe repetirla manualmente.

## Implementación esperada

1. Abrir el vault local actualizado desde GitHub.
2. Identificar dónde viven los SOUL reales de los profiles locales en la PC.
3. Parchear `brain-local`, `web-builder`, `web-auditor`, `pc-ops`.
4. Si las rutas absolutas del script difieren en Windows/local, crear wrapper o documentar comando equivalente en `Hermes/Systems/local/`.
5. Ejecutar chequeo contra los archivos modificados.
6. Publicar `response.md` en este handoff con:
   - rutas reales modificadas;
   - comando de verificación ejecutado;
   - resultado del sync local (`dirty=0 ahead=0 behind=0` o equivalente);
   - si hubo adaptación de rutas, documentarla.

## Criterios de aceptación

- Los 4 profiles locales cargan la directiva en arranque.
- Hay prueba real de verificación, no solo declaración.
- El resultado está subido a GitHub y visible para brain-vps.
- Si algo no se puede modificar por estar fuera de acceso, escalar en `response.md` con bloqueo concreto.

## Restricciones

- No modificar `Hermes/Config/`.
- No tocar secrets, tokens ni `.env`.
- No hacer cambios destructivos.
- No usar `git reset --hard`, `git clean`, ni `push --force`.
