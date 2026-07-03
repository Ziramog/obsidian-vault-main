# Skills Auto-Review — 2026-07-03

**Ejecutado por:** brain-vps (cron `skills-auto-review` e09c6c9ee0bd)
**Período analizado:** últimos 7 días (26 Jun — 3 Jul 2026)
**Modelo:** deepseek-v4-flash

---

## Resumen

| Métrica | Valor |
|---|---|
| Skills totales instalados | 110 (incluyendo 40 hub symlinks) |
| Skills propios (custom) evaluados | 15 |
| Skills usados en últimos 7 días | 7 |
| Parches aplicados | 3 (skills-auto-evolve + cron job) |
| Recomendaciones pendientes | 5 |
| Skills candidatos a revisar | 4 (bajo uso) |

---

## Skills propios — evaluación

### 1. hermes/skills-auto-evolve (hermes/)
**Último uso:** Hoy (esta misma ejecución) | **Estado:** ✅ Activo
**Evaluación:**
- Creado el 2-Jul-2026 durante sesión de Telegram con Juan
- Protocolo usaba `~/.hermes/sessions/` para búsqueda de sesiones → **PARCHE APLICADO**: ahora usa `session_search()`
- Sin errores reportados (muy nuevo)

### 2. hermes/hermes-vps-ops (hermes/)
**Último uso:** No cargado explícitamente en 7 días | **Estado:** 🟡 Activo, needs review
**Evaluación:**
- Skill extenso (2151 líneas, ~100 KB). Contiene referencias a múltiples herramientas y diagnósticos.
- Referencias a Tailscale systemd unit, Puppeteer, PM2 — probablemente vigentes.
- **Recomendación:** Podría dividirse en skills más pequeños o archivarse referencias de diagnósticos que ya no son relevantes. No aplicar patch sin revisión de Juan.

### 3. agenda-workflow
**Último uso:** 28-Jun-2026 (sesión de fix masivo) | **Estado:** ✅ Estable
**Evaluación:**
- Gran cantidad de fixes aplicados la semana pasada:
  - Bug de parseo `a.m.` → garbage tasks (FIXED)
  - `/mañana@Agenda_Hbot` no listaba (FIXED)
  - Consultas se guardaban como tareas (FIXED)
  - Fallback de alta demasiado permisivo (FIXED)
- Skill actualizado con guardrails anti-basura durante la sesión del 28-Jun
- **Estado:** Contenido actualizado, sin errores recurrentes detectados

### 4. obsidian
**Último uso:** Cargado en esta sesión | **Estado:** ✅ Estable
**Evaluación:**
- Contenido actualizado (V5, última actualización 2026-06-25)
- Sin errores reportados en el período
- Las rutas de vault y git commands están correctas
- Sin cambios necesarios

### 5. wolfim-email-outreach
**Último uso:** 29-Jun-2026 (aplicación RWS CV) | **Estado:** ✅ Estable
**Evaluación:**
- Usado en sesiones recientes para referencia de pipeline
- Contenido del skill actualizado con el pipeline completo
- Sin errores reportados
- Las credenciales de Resend API referenciadas están correctas

### 6. messaging/telegram-send-pipeline
**Último uso:** Uso continuo por crones | **Estado:** ✅ Estable
**Evaluación:**
- Funciona sin errores reportados
- Token y chat ID correctos en el skill
- Sin cambios necesarios

### 7. note-taking/obsidian-vault-daily-summary
**Último uso:** Uso continuo por crones daily | **Estado:** ✅ Estable
**Evaluación:**
- Plantilla y workflow correctos
- Sin errores reportados

### 8. hermes-orchestration
**Último uso:** No cargado en 7 días | **Estado:** 🟡 Referencia incorrecta en cron
**Evaluación:**
- El cron `skills-auto-review` referenciaba `hermes/orchestration` (ruta incorrecta). El skill existe como `hermes-orchestration` (top-level).
- **PARCHE APLICADO**: `jobs.json` corregido de `hermes/orchestration` → `hermes-orchestration`
- Contenido del skill actualizado (última modificación Jun-29)

### 9. cloud/google-drive-upload
**Último uso:** 28-Jun-2026 (subida de backup) | **Estado:** ✅ Estable
**Evaluación:**
- Funcionó correctamente para subir backup de 184 MB a Drive
- Sin errores reportados
- Contenido del skill correcto

### 10. ops/roggero-roma-backup
**Último uso:** Automático por cron semanal | **Estado:** ✅ Estable
**Evaluación:**
- Cron semanal funcionando (sábados 10 AM)
- MongoDB, Cloudinary y GitHub backup verificados
- Contenido actualizado con layout de DB verificado el 27-Jun

### 11. outreach/whatsapp-outreach-ops
**Último uso:** No usado en 7 días | **Estado:** 🟡 Standby
**Evaluación:**
- Sin actividad reciente. El pipeline de WhatsApp no está activo.
- Contenido del skill extenso (1362 líneas). Posiblemente desactualizado en algunas referencias.
- **Recomendación:** Revisar si sigue siendo necesario mantenerlo tan detallado, o si puede simplificarse.

### 12. commercial/evidence-scout
**Último uso:** No usado en 7 días | **Estado:** 🟡 Standby
**Evaluación:**
- Sin uso reciente. Skill especializado para research de venues.
- Contenido parece actualizado (referencias de Jun-2026).
- No modificar sin uso activo.

### 13. commercial/wolfim-commercial-ops
**Último uso:** No usado en 7 días | **Estado:** 🟡 Standby
**Evaluación:**
- Sin uso reciente.
- No hay errores conocidos.

### 14. hermes/usage-analytics
**Último uso:** No usado en 7 días | **Estado:** 🟡 Standby
**Evaluación:**
- Skill funcional pero sin demanda reciente.
- Contenido correcto.

### 15. inbox-triage
**Último uso:** No usado en 7 días | **Estado:** 🟡 Standby
**Evaluación:**
- Sin uso en período analizado. Los crones de check-replies usan otro mecanismo.

---

## Parches aplicados (automáticos, <30% cada skill)

| # | Skill/Archivo | Cambio | Razón |
|---|---|---|---|
| 1 | `skills-auto-evolve` | `~/.hermes/sessions/` → `session_search()` | El método anterior buscaba en archivos planos; el moderno usa SQLite FTS5 |
| 2 | `~/.hermes/cron/jobs.json` | `hermes/orchestration` → `hermes-orchestration` | El cron cargaba un skill con nombre incorrecto, generando warning en cada ejecución |
| 3 | `~/.hermes/cron/jobs.json` (prompt) | `Busca en ~/.hermes/sessions/` → `Busca con session_search()` | Coherencia con el skill actualizado |

---

## Errores detectados en sesiones recientes

### 🔴 Agenda bot — garbage tasks (27-28 Jun)
- **Síntoma:** `/mañana@Agenda_Hbot`, `/pendiente`, `Tareas` se guardaban como tareas en lugar de listar
- **Causa raíz:** El fallback de alta era demasiado permisivo — cualquier texto no reconocido se guardaba como tarea
- **Fixes aplicados en sesión:** Múltiples parches al código del bot, actualización de guardrails en skill agenda-workflow
- **Estado:** ✅ Resuelto

### 🟡 Hermes update session (2 Jul)
- Juan aprobó `hermes update` desde Telegram. Se ejecutó correctamente.
- Se creó el skill `skills-auto-evolve` y el cron `skills-auto-review`
- Sin errores en la ejecución.

### 🟢 Sin errores críticos
- No se detectaron patrones de error repetidos (2+ ocurrencias) en los últimos 7 días
- Los crones de check-replies, campaign, health-check y vault-sync funcionan sin errores
- Gateway y Telegram estables

---

## Recomendaciones pendientes (escalar a Juan)

| # | Propuesta | Tipo | Impacto |
|---|---|---|---|
| 1 | **Archivar `usage-analytics`** si no se va a usar en próximas semanas — es mantenimiento sin propósito | Eliminación (>30%) | Bajo |
| 2 | **Simplificar `whatsapp-outreach-ops`** — 1362 líneas para un pipeline en standby. Archivar referencias históricas, mantener solo lo operativo | Simplificación (>30%) | Medio |
| 3 | **Dividir `hermes-vps-ops`** — 2151 líneas, 100 KB es difícil de mantener. Separar en: crash-recovery, pm2-setup, tailscale, puppeteer | Reestructuración (>30%) | Medio |
| 4 | **Considerar crear skill para el pipeline de backup-hermes** — Actualmente documentado en `hermes-vps-ops` como referencia pero tiene su propio cron, script y flujo completo | Creación de skill | Bajo |
| 5 | **Actualizar cron `skills-auto-review` a schedule semanal fijo** — Actualmente `0 13 * * 0` (domingo 10:00 ART). Verificar si Juan prefiere otro horario | Ajuste de cron | Bajo |

---

## Próxima revisión sugerida

**Sugerida:** 2026-07-10 (próximo viernes)
**Nota:** Si no hay actividad relevante en skills en la semana, considerar pasar a revisión quincenal.

---

## Acción prioritaria para Juan

**Revisar recomendaciones #1 y #2** — decidir si archivar `usage-analytics` y simplificar `whatsapp-outreach-ops`. Son skills en standby que mantienen carga cognitiva sin propósito actual. La decisión libera espacio mental y reduce falsos positivos en futuras revisiones.
