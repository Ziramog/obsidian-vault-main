---
name: pc-ops
host: local
role: (rol previsto) Mantenimiento técnico de PC local — Windows, WSL, discos, red, backups
reads:
  - Hermes/Systems/local/
  - documentación de sistema
writes:
  - Hermes/Systems/local/
escalates-to: brain-local → Juan
status: not-implemented
superseded-by: pcbrain
created: 2026-06-25
ficha-actualizada: 2026-09-22
---

# pc-ops — Operaciones de PC Local · `status: not-implemented`

## Estado real (verificado 2026-09-22)

**Este perfil nunca se creó.** La evidencia:

| Verificación | Resultado |
|---|---|
| `profiles/pc-ops/` en la PC local | **no existe** (8 perfiles: brain-local, web-builder, web-auditor, pcbrain, algolab, algolab-strategy, algolab-darwin, trading-performance) |
| Wrapper en `~/.local/bin/` | **no existe** (sí existe `pcbrain.bat`) |
| Sesiones o cron propios | **ninguno** |
| Rastros en el filesystem | solo esta ficha en el vault |

**El rol está cubierto por `pcbrain`**, que sí tiene SOUL, workspace, protocolo operativo y
registro (`SYSTEM-INVENTORY.md`, `CHANGELOG.md`, `BACKUP-REGISTER.md`) y escribe sus
reportes en `Systems/Local-PC/`. Se mantienen como perfiles separados solo de nombre: no
hay un `pc-ops` al que delegar.

**Consecuencia pendiente (fuera de la zona de escritura de brain-local):**
`Hermes/Config/SOUL.md`, `Hermes/Config/AGENTS.md` y `Hermes/Config/ARCHITECTURE.md` siguen
listando `pc-ops` entre los perfiles activos, y `Hermes/Indexes/ownership-map.md`
(auto-generado) le asigna la propiedad de `Hermes/Systems/local/`. Corregir esas tablas
requiere decisión de Juan (son rutas de su zona) y el cambio llega al índice auto-generado
cuando corra el generador del VPS.

**Dos salidas posibles:**

1. **Marcar obsoleto** (recomendado): actualizar las tablas de `Hermes/Config/` para que el
   owner de `Systems/local/` sea `pcbrain` y eliminar `pc-ops` del listado de perfiles activos.
2. **Crear el perfil**: `hermes profile create pc-ops` con SOUL propio y zonas separadas —
   solo si se quiere dividir el mantenimiento del equipo (pcbrain) de otra función concreta.

Hasta que se decida (1) o (2), esta ficha queda como **documento de rol, no como perfil**.

---

## Contenido original del rol previsto (2026-06-25)

### Qué sería

El profile de mantenimiento de la PC local de Juan. Gestionaría Windows, WSL, discos, red,
Tailscale, backups locales y el entorno de desarrollo.

### Qué haría

- Diagnosticar problemas de sistema (discos llenos, procesos colgados, red).
- Mantener WSL y el entorno de desarrollo.
- Verificar backups locales.
- Monitorear salud del sistema.
- Documentar configuraciones en `Hermes/Systems/local/`.

### Qué NO haría

- **Acciones destructivas requieren aprobación de Juan.** Regla de los 5 minutos: si una
  acción es irreversible en 5 minutos, pregunto antes.
- No tocar el VPS (eso es brain-vps).
- No modificar código de proyectos.
- No instalar software sin aprobación.

### Protocolo de apertura

1. Leer `Hermes/Systems/local/` → estado conocido del sistema.
2. Ejecutar diagnóstico rápido.
3. Reportar anomalías.

### Protocolo de cierre

1. Documentar cambios en `Hermes/Systems/local/`.
2. Reportar a brain-local.
