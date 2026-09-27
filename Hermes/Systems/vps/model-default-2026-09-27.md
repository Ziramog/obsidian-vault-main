---
type: vps-change
date: 2026-09-27
owner: brain-vps
status: applied
scope: default + 8 profiles del VPS
---

# Cambio de modelo default (main) — 2026-09-27

## Qué se cambió

Modelo default (main) de **los 9 profiles del VPS** (default/brain-vps + los 8 empresariales):

| Campo | Valor nuevo |
|---|---|
| `model.default` | `deepseek-v4.1-flash` |
| `model.provider` | `opencode-go` |
| `model.base_url` | `https://opencode.ai/zen/go/v1` |

**Antes:** default = `qwen3.8-max` (provider `custom`, Alibaba token-plan); almas-libres/gymhealth/jobseeker = `gpt-5.4`, wolfim-growth/rws = `gpt-5.5`, construvial-growth = `gpt-5.6-terra` (todos `openai-codex`), ango-comercial = `deepseek-v4-flash`, korantis-ops = `deepseek/deepseek-v4-flash` (ambos `opencode-go`).

Autorizado por Juan en sesión desktop del 2026-09-27.

## Cómo se aplicó

```bash
hermes [-p <profile>] config set model.provider opencode-go
hermes [-p <profile>] config set model.default deepseek-v4.1-flash
hermes [-p <profile>] config set model.base_url https://opencode.ai/zen/go/v1
hermes config set model.api_key ""        # solo el default (ver pitfall)
hermes gateway restart
```

Backups: `~/.hermes/config.yaml.bak.20260927_194648` y `~/.hermes/profiles/<p>/config.yaml.bak.20260927_194648` (8 archivos).

## Verificación (real, no inferida)

- `hermes profile list` → los 9 profiles muestran `deepseek-v4.1-flash`.
- One-shots reales OK: default, wolfim-growth, almas-libres, korantis-ops, ango-comercial (`PONG`).
- `~/.hermes/logs/gateway.log`: `Model context warmed: deepseek-v4.1-flash -> 1000000 tokens (detected)` tras el restart; Telegram en polling confirmado healthy.
- Los 13 cron jobs del profile default no fijan `model`/`provider` → heredan el default, así que también migraron sin tocar `jobs.json`.

## Pitfalls encontrados

1. `hermes config set model.provider <x>` **limpia** `model.base_url` (la ruta vieja pertenecía a otro provider). Hay que setear provider → default → base_url en ese orden.
2. El default tenía `model.api_key` inline (key de Alibaba) que **no se limpia** al cambiar de provider: viajaba a opencode-go y habría dado 401. Se vació explícitamente (`api_key: ''`), así gana `OPENCODE_GO_API_KEY` del `.env`.
3. Un `curl` crudo contra `opencode.ai/zen/go/v1` devuelve `400 MissingSessionID`: el relay exige `x-opencode-session`, header que Hermes agrega solo (`agent/opencode_affinity.py`). La única prueba válida es un `hermes chat -q` real.

## Pendientes / observaciones (no bloqueantes)

- ⚠️ El gateway del VPS es **standalone**: solo sirve el profile default. Los bots de los 8 profiles empresariales quedan mudos (sus configs igual quedaron actualizadas). Resolver con `hermes gateway migrate --multiplex` requiere antes darle a cada profile su propio bot de Telegram (hoy todos comparten el token del default).
- ⚠️ Conflictos de polling de Telegram: patrón viejo (1722 líneas históricas en `gateway.log`, desde mayo). Tras el restart bajó a 1 conflicto aislado; si vuelve a repetirse cada ~20s, buscar una segunda instancia haciendo `getUpdates` con el mismo token.
- 🔧 Ruido: todos los profiles escupen `Warning: Unknown toolsets: messaging` al arrancar — hay un toolset inexistente listado en las configs. No rompe nada.