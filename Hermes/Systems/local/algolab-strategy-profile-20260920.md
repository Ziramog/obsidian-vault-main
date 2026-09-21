# Perfil `algolab-strategy` — creación y configuración

**Fecha:** 2026-09-20
**Perfil ejecutado por:** brain-local (PC local)
**Origen del trabajo:** pedido directo de Juan (pasted brief, sin handoff formal)

---

## Resumen

Se creó el perfil local **`algolab-strategy`** como contraparte de
investigación/estrategia del perfil de ejecución `algolab`. El perfil razona y
diseña; no ejecuta.

---

## 1. Modelo y enrutamiento

| Rol | Proveedor | Modelo | Razonamiento |
|---|---|---|---|
| Principal | `alibaba-token-plan` | `qwen3.8-max` | thinking activo por defecto del modelo |
| Fallback #1 | `deepseek` | `deepseek-flash` | `high` (`agent.reasoning_overrides`) |

**Hallazgo relevante (credencial).** El key de Alibaba que ya existía en
`profiles/algolab/.env` estaba guardado como `DASHSCOPE_API_KEY`, pero **solo
autentica contra el endpoint Token Plan**
(`https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`).
Contra los endpoints DashScope normales devuelve HTTP 401 `invalid_api_key`.

- El provider `alibaba-token-plan` (plugin `plugins/model-providers/alibaba/`)
  declara `env_vars=("ALIBABA_TOKEN_PLAN_API_KEY", ...)`.
- Los perfiles de Hermes **no heredan credenciales** (islas por diseño), así que
  la credencial se aprovisionó en el `.env` del perfil nuevo como
  `ALIBABA_TOKEN_PLAN_API_KEY`, sin imprimir ni registrar el valor.
- Verificado en vivo: `POST /chat/completions` con `qwen3.8-max` → HTTP 200.

**Alias descartado.** El catálogo estático (`models_catalog_static.py`,
`_ALIBABA_TOKEN_PLAN_MODELS`) lista `qwen3.8-max-0902`, que **no existe** en el
endpoint (HTTP 404 `model_not_found`). El id correcto es `qwen3.8-max`.

**Razonamiento — no se inventó ningún parámetro.** Probado contra el endpoint:
`qwen3.8-max` es un modelo *thinking* (devuelve `reasoning_content` y
`reasoning_tokens` por defecto), y `enable_thinking: false` lo apaga. Pero el
transporte de Hermes solo emite parámetros de razonamiento para hosts
OpenRouter / Nous / GitHub / LM Studio / Ollama
(`agent/reasoning_params.py::_supports_reasoning_extra_body`), así que para este
host **no se envía ningún knob de effort**. Por eso `agent.reasoning_effort` no
se configuró para el principal y el effort `high` se fijó solo en el fallback
DeepSeek (que sí lo honra).

---

## 2. Toolsets habilitados (9 de 29)

```text
clarify, code_execution, file, memory, session_search, skills, terminal, todo, web
```

**No habilitados** (deliberado): `cronjob`, `browser`, `computer_use`,
`delegation`, `kanban`, `x_search`, `image_gen`, `tts`, `vision`, `connections`.

Objetivo: ninguna capacidad de control autónomo de SQX, ninguna capacidad de
crear/modificar jobs programados, sin subagentes que hereden la sesión.

---

## 3. Restricción técnica de ejecución — `approvals.deny`

```yaml
approvals:
  deny:
    - "*strategyquant*"
    - "*sqx64*"
    - "*sqx.exe*"
    - "*metatrader*"
    - "*terminal64*"
    - "*main[0-9]*"
    - "*sqx_builder*"
    - "*run_campaign*"
```

`tools/approval_floors.py::_match_user_deny_rule` corre **antes** de
`--yolo` / `approvals.mode=off` / cron-approve, y es la **primera** comprobación
de `check_all_command_guards` (`tools/approval.py:1167`). Es un bloqueo a nivel
de herramienta, no una convención de política.

**Verificado en vivo** (dos turnos reales del perfil):

- `terminal: echo StrategyQuant-DENYTEST-A` → bloqueado con el mensaje textual
  `BLOCKED: this command matches the user-defined deny rule '*strategyquant*'`.
- `terminal: echo CONTROL-OK` → ejecutado, salida `CONTROL-OK`.
- `execute_code` → bloqueado por `approvals.single_query_mode: deny` en corridas
  `-q` sin usuario presente.

**Trade-off documentado:** `*main[0-9]*` bloquea cualquier comando de terminal
que mencione `main09`, incluido un `tail` del log de campaña. Las lecturas deben
hacerse con `read_file` / `search_files`, que no pasan por esta guarda.

**Límite de la garantía:** `approvals.deny` cubre la superficie de comandos.
No es una ACL de sistema de archivos. Un `write_file` sobre una ruta del
workspace operativo no lo frena nada a nivel kernel — eso queda cubierto por
SOUL.md y el `AGENTS.md` del workspace, es decir, por contrato.

---

## 4. Conocimiento compartido (solo lectura)

- **Lectura:** `C:\Users\ingju\algolab-workspace` y su subárbol, incluido
  `algolab-v2-sqx-master` (reports, manifests, audits, lab ledger `LAB.md`).
- **Escritura:** `profiles/algolab-strategy/workspace` (cwd del perfil, con su
  propio `AGENTS.md`).
- No se duplicó ningún artefacto del lab.

---

## 5. Comunicación bot-to-bot con `algolab`

Mecanismo soportado por el build: **`message_agent`** desde el Bot Chat canónico.

El gate (`tools/bot_mode_dm.py::message_agent_authorized`) exige tres cosas:
`agent.bot_mode_protocol: true` (default), una sesión titulada exactamente
`Bot Chat`, y **al menos un perfil del instalación con** `ui_meta: {hermes-bots: …}`
en su `profile.yaml`. No existía ninguno, así que se escribió ese bloque en el
`profile.yaml` del perfil nuevo (documentado en el propio archivo: el plugin de
escritorio lo escribe solo, el CLI no).

Sesión canónica creada: `20260920_190627_215afd`, título `Bot Chat`.
Verificado: la herramienta está disponible y el roster local incluye `@algolab`,
`@brain-local`, `@pcbrain`, `@web-builder`, `@web-auditor`,
`@trading-performance`, `@hermes`.

**No se envió ningún mensaje a `algolab`** durante la creación — un DM dispara
un turno real en el perfil de ejecución mientras MAIN09 corre.

---

## 6. Archivos creados / modificados

| Ruta | Acción |
|---|---|
| `profiles/algolab-strategy/` | creado (`hermes profile create`) |
| `.../config.yaml` | modificado vía CLI (modelo, fallback, overrides, toolsets, cwd, approvals.deny) |
| `.../SOUL.md` | reemplazado por la identidad de Research Director |
| `.../profile.yaml` | descripción + marca `ui_meta.hermes-bots` |
| `.../workspace/AGENTS.md` | creado (contrato lectura/escritura y prohibiciones) |
| `.../.env` | `ALIBABA_TOKEN_PLAN_API_KEY`, `DEEPSEEK_API_KEY` (valores nunca impresos) |
| `.../backups/*.bak-20260920-190455` | snapshot previo de config.yaml / SOUL.md / profile.yaml |
| `C:\Users\ingju\.local\bin\algolab-strategy.bat` | wrapper creado por el CLI |

Nada fuera de `profiles/algolab-strategy/` fue modificado. El workspace de
AlgoLab no recibió ninguna escritura (verificado con `find -newermt`).

---

## 7. Reversión

```bash
hermes profile delete algolab-strategy                 # borrado completo del perfil
hermes -p algolab-strategy config unset approvals.deny # solo quitar el bloqueo de comandos
hermes -p algolab-strategy config unset platform_toolsets.cli
```

Los backups en `profiles/algolab-strategy/backups/` revierten config.yaml,
SOUL.md y profile.yaml al estado inmediatamente posterior a la creación.

---

## 8. Caveats abiertos

1. **`auxiliary.*` quedó en `auto`** → los roles auxiliares (compression, vision,
   title) heredan el modelo principal. Si algún rol necesita otra cosa, se fija
   por rol.
2. **MoA apagado** (`moa.active_preset: ''`). El preset built-in `default`
   apunta a `openrouter:anthropic/claude-opus-4.8` y referencias que no tienen
   credencial — config muerta, pero está off, así que nunca corre.
3. **`security.tirith_enabled: true`** (default del CLI) con el binario `tirith`
   presumiblemente ausente + `tirith_fail_open: true` = sin chequeo efectivo.
   Es el default de todo perfil nuevo, no algo introducido acá.
4. **Aislamiento de escritura a nivel FS:** no existe en este build para
   herramientas locales. Ver §3.
5. **`execute_code` con guarda de `single_query_mode`**: en una sesión
   interactiva con usuario presente la guarda puede aprobar; el `user deny` sigue
   siendo la primera comprobación de la cadena, pero no se probó el camino
   `terminal()` *dentro* de execute_code en modo interactivo.
