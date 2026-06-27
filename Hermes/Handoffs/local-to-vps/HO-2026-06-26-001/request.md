---
id: HO-2026-06-26-001
status: ready
from: brain-local
to: brain-vps
project: system
priority: medium
created-at: 2026-06-26T21:15:00-03:00
acknowledge-by: next-vps-session
escalate-after: 48h
briefing: Hermes/Briefings/current.md
director: Juan
---

## Skills instalados localmente — disponibles para perfiles

Se instalaron los siguientes skills del hub de Hermes en los perfiles locales. Quedan a disposición del VPS cuando necesiten coordinación.

### Perfil web-auditor
- `audit` (seojuice) — auditoría SEO
- `audit-speed` (seojuice) — auditoría de velocidad

### Perfil web-builder
- `web-development` — implementación web frontend

### Perfil brain-local
- `digital-marketing` — estrategias de marketing digital (canales, funnels, experimentos)
- `abstract-strategy` — abstracción estratégica
- `ansible-automation` — automatización de servidores con Ansible

### GitHub
- `gh` CLI autenticado con cuenta Ziramog
- Token scopes: repo, workflow, read:org, gist
- Disponible para búsquedas y operaciones read-only en repos

### x_search
- Toolset habilitado pero requiere credenciales xAI (XAI_API_KEY o SuperGrok OAuth)
- Sin configurar aún

### Regla de seguridad
- **No se comitea ni pushea a producción sin autorización explícita de Juan**
- Esta regla está en memoria de brain-local

### Próximos pasos
- Los skills están listos para usarse cuando lleguen handoffs que los requieran
- Si wolfim-growth necesita digital-marketing, avisame y lo coordinamos
