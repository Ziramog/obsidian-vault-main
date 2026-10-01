# ROLE PATCH — `@strategyalgo` = TUTOR + STRATEGIST + ORCHESTRATOR (curso StatOasis)

**Fecha:** 2026-10-01 05:41 -04:00
**Ejecutor:** brain-local (PC local)
**Autorización:** GO explícito de Juan — *«GO — ROLE PATCH ONLY. DO NOT REDESIGN CURRENT ARCHITECTURE.»*
**Alcance aplicado:** sólo instrucciones de rol. Cero cambios en MCP, sqxcli, CFG, datos o campañas.

---

## 1. Mapeo de nombres (verificado, no asumido)

`@strategyalgo` es el nombre que usa Juan en el chat; el **perfil real** se llama `algolab-strategy`.

| Alias | Perfil real | Evidencia |
|---|---|---|
| `@strategyalgo` | `algolab-strategy` | `profile.yaml`: *"AlgoLab research director … execution stays with the algolab profile"*; `SOUL.md` §1 tabla de roles: `algolab-strategy` = Research Director |
| `@algolab` | `algolab` | `SOUL.md`: *"algolab is the technical laboratory operator"*; `profile.yaml`: *"Algorithmic trading lab … for StrategyQuant X (SQX)"* |

Grep de la cadena literal `strategyalgo` en todo `profiles/` → **0 coincidencias** (es una etiqueta de conversación, no de disco).

---

## 2. Archivos modificados (2) + backups (2)

| Archivo | Antes (sha256) | Después (sha256) | Δ |
|---|---|---|---|
| `…\profiles\algolab-strategy\SOUL.md` | `53a44edb…aeaa62` | `18049db7…8aab25` | +2449 bytes, 203→267 líneas |
| `…\profiles\algolab\SOUL.md` | `1e29ff01…f3bee5` | `be5c106a…23b2` | +1587 bytes, 1227→1264 líneas |

Backups (convención ya existente en ambos perfiles: `SOUL.pre_method_lock_*.md`, `SOUL.before-audit.md`):

```
algolab-strategy/SOUL.pre_statoasis_tutor_20261001_053947.md   8997 b   sha256 53a44edb…aeaa62  (= SOUL.md original)
algolab/SOUL.pre_statoasis_tutor_20261001_053947.md           23513 b   sha256 1e29ff01…f3bee5  (= SOUL.md original)
```

**Intactos (hash idéntico al baseline tomado antes de empezar):**

```
1171c677…b69da8b  algolab-strategy/config.yaml
56db257b…63333a81  algolab/config.yaml
ecd5af54…4def867e  algolab-strategy/profile.yaml
50a304ef…3a41ec0  algolab/profile.yaml
```

---

## 3. Cláusulas añadidas

### 3.1 `algolab-strategy/SOUL.md` — nueva sección `# 2. STATOASIS COURSE — ACTIVE TUTOR MODE` (líneas 69-131)

- Declara el rol durante el curso: `TUTOR + STRATEGIST + ORCHESTRATOR`.
- **Duties (10 puntos):** track del módulo/video; explicar qué enseña StatOasis y por qué; separar
  `STATOASIS_SOURCE` / `COURSE_EXAMPLE·PRESET` / `ALGOLAB_ADAPTATION`; traducir a conceptos y settings de
  SQX; decir qué mirar/probar en SQX; **pedirle a `algolab` el estado real por la infraestructura MCP +
  sqxcli ya existente**; comparar `EXPECTED_FROM_STATOASIS` vs `ACTUAL_IN_SQX`; explicar diferencias;
  recomendar el próximo paso del curso; diseñar el experimento y presentarlo para GO.
- **Limits of this mode:** proactivo en enseñanza/interpretación/planificación, **nunca autónomo en
  ejecución material**. Prohibido: lanzar campañas/Builder/Optimizer/Retest sin GO; rediseñar StatOasis en
  silencio; ser asistente pasivo («pasame la próxima clase»); exigir a Juan que explique el estado de SQX
  cuando `algolab` puede inspeccionarlo; pedir capturas por defecto cuando MCP/sqxcli puede dar el estado;
  tocar la arquitectura MCP/sqxcli, arrancar SQX o modificar artefactos de experimentos.
- **Economic north star:** `APRENDER SQX + REPRODUCIR STATOASIS + CREAR ESTRATEGIAS VÁLIDAS → PORTFOLIO
  OPERABLE → GANAR DINERO`, con el vehículo (capital propio / The5ers / Darwinex / otro) decidido después
  por evidencia.

El resto del archivo quedó igual: la sección previa `# 2. DIRECTORIAL DISCIPLINE — METHOD LOCK` se renumeró a
**`# 3.`** (único cambio fuera de la inserción; contenido sin tocar).

### 3.2 `algolab/SOUL.md` — nueva sección `# 41. Modo curso StatOasis — soporte técnico al director` (líneas 1231-1264)

Regla de interacción simétrica: `algolab-strategy` tutoriza; `algolab` sigue siendo **ejecutor técnico de SQX**
y responde con hechos, no con decisiones metodológicas.

- Pedido típico: *«necesito saber cómo está configurado X»* → devuelve `ACTUAL SQX STATE` (symbol / TF / fechas
  / blocks / rules / orders / exits / template / ranking / costs / proyecto y databank de origen), **leído, no
  recordado**.
- Usa la infraestructura **ya existente**: MCP de SQX en `http://127.0.0.1:8080/mcp`, `sqcli.exe` headless,
  cliente `scripts/sqx_mcp.py`. *«Esa arquitectura no se modifica.»*
- No interpreta el método StatOasis ni explica el curso al operador.
- Lectura vs escritura: inspeccionar (`list_projects`, `list_databanks`, `list_strategies`,
  `get_strategy_stats`, lectura de `.cfx`/`settings.xml`/`data.db`) es lectura; `run_project`, `loadconfig`,
  Start, Retest, Optimizer y toda mutación exigen **GO explícito** de Juan.
- No abre la GUI ni lanza el motor para responder una consulta de estado; declara lo que no pudo certificar.

---

## 4. Las cuatro confirmaciones pedidas

1. **Archivos modificados:** `profiles/algolab-strategy/SOUL.md` y `profiles/algolab/SOUL.md` (2 archivos +
   2 backups). Ningún otro archivo del sistema fue escrito.
2. **Cláusulas añadidas:** las de §3.1 y §3.2 (más la renumeración `#2 → #3` en el primero).
3. **`@strategyalgo` es ahora `TUTOR + STRATEGIST + ORCHESTRATOR` para StatOasis:** **sí**, verificado por
   *live turn* del perfil (§5-H), no sólo por el archivo.
4. **MCP/sqxcli intacto:** **sí** — ver §6 (hashes + mtimes sin cambios, 0 archivos modificados hoy en el
   workspace operativo).

---

## 5. Evidencia cruda

**A) Cláusulas presentes en el archivo**

```
$ grep -n "STATOASIS COURSE — ACTIVE TUTOR MODE\|TUTOR + STRATEGIST + ORCHESTRATOR\|EXPECTED_FROM_STATOASIS\|# 3. DIRECTORIAL DISCIPLINE" algolab-strategy/SOUL.md
69:# 2. STATOASIS COURSE — ACTIVE TUTOR MODE
74:TUTOR + STRATEGIST + ORCHESTRATOR
97:EXPECTED_FROM_STATOASIS
133:# 3. DIRECTORIAL DISCIPLINE — METHOD LOCK

$ grep -n "Modo curso StatOasis\|ACTUAL SQX STATE\|arquitectura no se modifica" algolab/SOUL.md
1231:# 41. Modo curso StatOasis — soporte técnico al director
1242:ACTUAL SQX STATE
1254:  arquitectura no se modifica.
```

**B) Tamaños post-patch**

```
$ wc -l algolab-strategy/SOUL.md algolab/SOUL.md
  267 algolab-strategy/SOUL.md
 1264 algolab/SOUL.md
```

**C) Configuración de los perfiles intacta (comparado contra el baseline previo)**

```
$ sha256sum algolab-strategy/config.yaml algolab/config.yaml algolab-strategy/profile.yaml algolab/profile.yaml
1171c677854d4be72be0684247cca175078380edc059b57a205c4257fb69da8b *algolab-strategy/config.yaml
56db257b4f60f56a581ad3f6c07155cf23173b72f0c07221034e02ce36333a81 *algolab/config.yaml
ecd5af544bebece6cd5b781644fe92bc4b1416696861259490fb9ad34def867e *algolab-strategy/profile.yaml
50a304ef094b0e8cb10448a7750271fb90197f9beff9c4e2e30d557a13a41ec0 *algolab/profile.yaml
```
(idénticos al baseline tomado a las 05:39, antes de tocar nada)

**D) Backups verificados por hash (copia == original pre-patch)**

```
$ sha256sum algolab-strategy/SOUL.pre_statoasis_tutor_20261001_053947.md algolab/SOUL.pre_statoasis_tutor_20261001_053947.md
53a44edb0bac6a6732adb271cc950389f55d367849b8a6048f9681313aaeaa62 *…algolab-strategy/SOUL.pre_statoasis_tutor_20261001_053947.md
1e29ff01278afe194a6ce05e73ce611eb900f13370f698aec1b59f7447f3bee5 *…algolab/SOUL.pre_statoasis_tutor_20261001_053947.md
```

**E) MCP / sqxcli — archivos sin cambios**

```
$ sha256sum "C:/Users/ingju/Desktop/SQX_144_Full/sqcli.exe" "C:/Users/ingju/algolab-workspace/scripts/sqx_mcp.py" "C:/Users/ingju/algolab-workspace/scripts/mcp_probe2.py"
fb8a8dd071de0bbe16e4ab5f101fff2bb4e37f7bb4e84af9933dd93b95e6b5a7  …\SQX_144_Full\sqcli.exe      (mtime 2026-05-20 03:03)
8d1054b31f3b209d184b61bd53ee269a1ad72cbc160b138a8f8bb3b622aeda5d  …\scripts\sqx_mcp.py         (mtime 2026-09-06 17:32)
bcaec1cd45643f02b36d83b4654ab30b3ab40c76a0008c1171285ca3d17d320e  …\scripts\mcp_probe2.py

$ for d in scripts tools knowledge config reports rules; do echo -n "$d: "; find "C:/Users/ingju/algolab-workspace/$d" -maxdepth 3 -type f -newermt "2026-10-01 00:00" | wc -l; done
scripts: 0
tools: 0
knowledge: 0
config: 0
reports: 0
rules: 0
```

**F) Estado del endpoint MCP de SQX en el momento de medir (05:41)**

```
$ netstat -ano | grep "8080"
  TCP    127.0.0.1:57027        127.0.0.1:8080         SYN_SENT        71452
  TCP    [::1]:57021            [::1]:8080             SYN_SENT        71452

$ netstat -ano | grep -i "LISTENING" | grep "8080"
(vacío — no hay listener en 8080)

$ tasklist | grep -i -E "java|sqcli|strategyquant"
StrategyQuantX_ui.exe   81348/15564/71452/29296/38464   (UI Electron de SQX arriba)
sqcli.exe               (ausente — motor headless APAGADO)
```

Lectura honesta: la **UI** de SQX está corriendo; el **motor headless (`sqcli.exe`) no**, y el servidor MCP de
SQX **no está aceptando conexiones** en 8080 en ese instante (el propio proceso de red de la UI aparece en
`SYN_SENT` contra 8080). Esto **no** fue provocado por este trabajo (no arranqué ni detuve nada) y no invalida
el parche: es el estado del motor en ese minuto, y conviene re-medirlo cuando Juan abra SQX de verdad.

**G) Sólo se tocaron los dos SOUL.md**

```
$ ls -la --time-style=long-iso algolab/ algolab-strategy/ | grep "2026-10-01" | grep -v "^d"
-rw-r--r-- 25100 2026-10-01 05:40 SOUL.md            (algolab)
-rw-r--r-- 11446 2026-10-01 05:40 SOUL.md            (algolab-strategy)
-rw-r--r--  8965 2026-10-01 05:30 auth.json          (escritura propia del perfil, previa: 05:30)
-rw-r--r--  6914 2026-10-01 05:30 provider_models_cache.json  (idem)
-rw-r--r--  82747392 2026-10-01 05:28 state.db        (idem)
-rw-r--r--   6068792 2026-10-01 05:28 state.db-wal    (idem)
```
(`auth.json`, `provider_models_cache.json`, `state.db*` son escrituras del propio runtime de Hermes a las
05:28/05:30, anteriores a mi primera escritura de las 05:40.)

**H) Live turn de verificación del rol (el perfil lee su SOUL.md al abrir sesión)**

```
$ hermes -p algolab-strategy chat -Q --max-turns 3 -q "Sin usar herramientas. Responde exactamente 3 lineas: ..."
session_id: 20261001_054115_40f490
TUTOR + STRATEGIST + ORCHESTRATOR
STATOASIS COURSE — ACTIVE TUTOR MODE
@algolab debe devolver el estado real actual de SQX, inspeccionado mediante la infraestructura existente MCP + sqxcli.
```

---

## 6. Rollback (1 comando por archivo)

```
cp "C:/Users/ingju/AppData/Local/hermes/profiles/algolab-strategy/SOUL.pre_statoasis_tutor_20261001_053947.md" \
   "C:/Users/ingju/AppData/Local/hermes/profiles/algolab-strategy/SOUL.md"
cp "C:/Users/ingju/AppData/Local/hermes/profiles/algolab/SOUL.pre_statoasis_tutor_20261001_053947.md" \
   "C:/Users/ingju/AppData/Local/hermes/profiles/algolab/SOUL.md"
```
(revierte byte a byte: hashes de los backups = hashes originales)

---

## 7. No hecho / pendiente

- **No** se tocó MCP, `sqxcli.exe`, `scripts/`, CFX, bancos, datasets, cron ni `config.yaml` de ningún perfil.
- **No** se arrancó SQX, ni Builder, ni Optimizer, ni campaña. Cero evaluaciones.
- **No** se reescribió el SOUL completo ni se introdujo framework metodológico nuevo: inserción mínima + una
  renumeración.
- **Pendiente (fuera del alcance mínimo pedido):** la ficha del catálogo en el vault
  (`Hermes/Profiles/local/algolab-strategy.md`) todavía describe el rol sin el modo tutor; se puede actualizar
  en una pasada del catálogo si Juan lo quiere.
- Los `SOUL.md` son internos de cada perfil: **no viajan por el vault ni por git** (aislamiento por diseño).
  Esta copia del informe sí queda en `Hermes/Systems/local/`.
