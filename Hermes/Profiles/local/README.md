---
tipo: indice
ambito: Hermes/Profiles/local
actualizado: 2026-09-22
mantenido-por: brain-local
---

# Perfiles locales — catálogo

Fichas de rol de los perfiles que corren en la **PC local de Juan** (DESKTOP-3V091DM).
Una ficha describe rol, límites y zonas de lectura/escritura; **no** replica la
configuración ni la memoria interna del perfil (eso está aislado por diseño, ver
`Hermes/Config/ARCHITECTURE.md`).

## Perfiles activos

| Ficha | Rol | Modelo | cwd / workspace | Estado |
|---|---|---|---|---|
| [brain-local](brain-local.md) | Orquestador de producción local | alibaba / qwen3.7-max | perfil | activo |
| [web-builder](web-builder.md) | Implementación técnica (código, builds) | alibaba / qwen3.7-max | perfil | activo |
| [web-auditor](web-auditor.md) | Auditoría técnica independiente | alibaba / qwen3.7-max | perfil | activo |
| [pcbrain](pcbrain.md) | Administrador del equipo Windows | opencode-go / glm-5.2 | `profiles/pcbrain/workspace` | activo |
| [algolab](algolab.md) | Laboratorio técnico quant (SQX/MT5) | openai-codex / gpt-5.6-sol | `C:/Users/ingju/algolab-workspace` | activo |
| [algolab-strategy](algolab-strategy.md) | Research Director AlgoLab | openai-codex / gpt-5.6-sol | `profiles/algolab-strategy/workspace` | activo |
| [algolab-darwin](algolab-darwin.md) | Research Director línea Darwinex | openai-codex / gpt-5.6-sol | `C:/Users/ingju/algolab-workspace/darwin-research` | activo |
| [trading-performance](trading-performance.md) | Coach de proceso y journal (trading manual) | alibaba / qwen3.7-max | `profiles/trading-performance/workspace` | activo |

## Documentos de rol sin perfil

| Ficha | Estado | Nota |
|---|---|---|
| [pc-ops](pc-ops.md) | `not-implemented` | nunca se creó; su alcance lo cubre `pcbrain` |

## Verificación de este catálogo

Contrastado el 2026-09-22 contra el filesystem: `profiles/*/SOUL.md`, `config.yaml`
(modelo/provider vía `hermes -p <perfil> config get model`), `cwd`, contenido de cada
workspace y cron propio. Los 8 perfiles de disco tienen ficha; `pc-ops` figura como rol
documentado sin implementación.

**Pendiente fuera de la zona de brain-local:** `Hermes/Config/SOUL.md`, `AGENTS.md` y
`ARCHITECTURE.md` todavía listan `pc-ops` entre los perfiles activos, y
`Hermes/Indexes/ownership-map.md` (auto-generado) le asigna `Hermes/Systems/local/`.
Actualizar esas tablas es decisión de Juan.

## Cómo se mantiene

- Al crear, cambiar de alcance o retirar un perfil local → actualizar su ficha y esta tabla.
- Las fichas se escriben en `Hermes/Profiles/local/`; brain-local es el responsable local.
- Los perfiles del VPS viven en `Hermes/Profiles/vps/` y los skills compartidos en
  `Hermes/Profiles/skills/`.
