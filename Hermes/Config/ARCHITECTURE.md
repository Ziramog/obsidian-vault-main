# Hermes Architecture V5 — Documento Madre de Implementación

```yaml
---
title: Hermes Architecture V5 — Documento Madre
aliases:
  - Architecture V5
  - Documento Madre Hermes
  - Implementación Final Multiagente
tags:
  - hermes
  - arquitectura
  - multi-agent
  - implementación
  - financiero
status: active
version: 5.0
created: 2025-01-XX
owner: Juan Gomariz
director: Juan Gomariz
objective: financial-freedom
supersedes: architecture-obsidian-v4.md
incorporates:
  - architecture_obsidian_v4.txt
  - architecture_obsidian_v4_revision_claude.txt
  - architecture_obsidian_v4_agenda.txt
  - Claude-Review-Resolution.md
  - Hermes-Multi-Agent-Architecture.md
---
```

---

## 0. Para Qué Existe Este Documento

Este es el único documento que un agente necesita para entender el sistema completo, saber qué hacer, y ejecutar la implementación.

**Quién lo lee:**
- Juan — para validar y dirigir
- brain-vps — como constitución operativa permanente
- brain-local — como referencia de producción
- Cualquier agente nuevo — como onboarding completo

**Qué resuelve:**
- Define el sistema multiagente completo
- Incorpora las correcciones críticas de la auditoría
- Integra el sistema de agenda
- Establece un plan de implementación ejecutable fase por fase
- Mide éxito contra el objetivo real: libertad financiera de Juan

**Regla de uso:** Si hay contradicción entre este documento y cualquier otro, este documento tiene prioridad. Las decisiones cerradas (Sección 2) no se reabren sin instrucción explícita de Juan.

---

## 1. Principio Rector

**Juan es el director. El objetivo es libertad financiera.**

Hermes existe para:
1. Hacer crecer Wolfim como web agency (motor de ingresos principal)
2. Dar soporte rentable a ANGO (ingreso base ~333 USD/mes)
3. Desarrollar colaboración comercial con Construvial
4. Construir Korantis como producto propio con AI
5. Reducir la fricción operativa de Juan mediante agentes especializados

Todo lo que no avance hacia estos objetivos es ruido. El sistema se mide por ingresos generados y carga cognitiva reducida, no por volumen de archivos o complejidad técnica.

---

## 2. Decisiones Cerradas

No se reabren sin instrucción explícita de Juan.

| Decisión | Resolución |
|---|---|
| Director del sistema | Juan. No se crea un agente director. |
| Orquestadores | Dos: brain-vps (VPS) y brain-local (PC local). |
| Capa canónica de negocio | `companies/` no se reemplaza ni reestructura. |
| `Hermes/companies/` | Congelado. Sin escritura nueva. Migración gradual a `companies/`. |
| Memoria interna de profiles | No se sincroniza entre hosts. Aislada por diseño. |
| Obsidian | Conocimiento compartido, handoffs, decisiones y memoria externa. No memoria interna. |
| Cron actuales | Se preservan y documentan. No se tocan hasta tener reemplazos activos. |
| Secrets | Fuera del vault. Sin excepciones. |
| Método de sincronización | Git puro. Agentes nunca tocan git. Solo escriben archivos. |
| `gpt/` como carpeta raíz | Eliminada. Contenido útil → `Hermes/Intelligence/`. |
| `hq/` | Sin escritura nueva hasta asignar dueño. Legacy. |
| Nombres de profiles | brain-vps, brain-local, wolfim-growth, ango-commercial, construvial-growth, korantis-ops, web-builder, web-auditor, pc-ops. Definitivos. |
| Agenda | Un archivo por día en `Hermes/Agenda/YYYY-MM-DD.md`. Sin base de datos. |
| Inteligencia acumulativa | `companies/[empresa]/intelligence/` con context.md y patterns.md |
| KPIs financieros | `Hermes/Intelligence/kpis.md` — Juan actualiza semanalmente |

---

## 3. Topología del Sistema

### Junta Directiva

| Rol | Quién | Función |
|---|---|---|
| Director General | Juan | Decide, aprueba, desbloquea. Autoridad final. |
| Director de Operaciones 24/7 | brain-vps | Memoria estratégica, continuidad, coordinación, agenda, briefings. |
| Director de Producción | brain-local | Repositorios, builds, UI, auditoría. Activo cuando Juan trabaja. |
| Gerentes especializados | Profiles de empresa y producción | Cada uno conoce su dominio. Reportan a los brains. |

### Mapa Completo

```
                    ┌─────────────────────────────┐
                    │    JUAN — Director General    │
                    └──────────┬──────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                                 │
    ┌─────────▼──────────┐          ┌──────────▼─────────┐
    │  brain-vps         │          │  brain-local        │
    │  Ops 24/7          │          │  Producción         │
    │  VPS               │          │  PC Local           │
    └─────────┬──────────┘          └──────────┬─────────┘
              │                                 │
    ┌─────────┼──────────┐          ┌──────────┼─────────┐
    │         │          │          │          │         │
    ▼         ▼          ▼          ▼          ▼         ▼
 wolfim   ango-comm  construvial  web-      web-      pc-ops
 growth   ercial     growth      builder   auditor
              │
              ▼
          korantis-ops

              ◄──── Obsidian Vault (Git) ────►
```

### Flujo de Información

- **VPS → Local:** Handoffs vía `Hermes/Handoffs/vps-to-local/`
- **Local → VPS:** Handoffs vía `Hermes/Handoffs/local-to-vps/`
- **Ambos → Vault:** Escritura directa en zonas asignadas
- **Sync:** Git push/pull automático (VPS cada 15 min) + manual (local al cerrar sesión)
- **Alertas urgentes:** Telegram (solo para handoffs priority: high vencidos)

---

## 4. Estructura del Vault

```
obsidian-vault/
├── Hermes/
│   ├── MEMORY.md                          ← Estado frío del negocio
│   ├── Config/
│   │   ├── ARCHITECTURE.md                ← Este documento
│   │   ├── AGENTS.md                      ← Constitución técnica
│   │   └── SOUL.md                        ← Contrato operativo
│   ├── Briefings/
│   │   ├── current.md                     ← Prioridades vigentes
│   │   └── archive/
│   ├── Agenda/
│   │   └── YYYY-MM-DD.md                  ← Un archivo por día
│   ├── Handoffs/
│   │   ├── vps-to-local/
│   │   ├── local-to-vps/
│   │   └── archive/
│   ├── Intelligence/
│   │   ├── kpis.md                        ← Dashboard financiero semanal
│   │   └── [archivos migrados de gpt/]
│   ├── Profiles/
│   │   ├── vps/
│   │   ├── local/
│   │   └── skills/
│   ├── Indexes/
│   │   ├── vault-index.md
│   │   └── ownership-map.md
│   ├── Reports/
│   │   └── stale-notes-report.md
│   ├── Quarantine/
│   │   └── index.md
│   ├── Sessions/
│   ├── Daily/
│   ├── Memory/
│   │   ├── pending/                       ← Propuestas de actualización a MEMORY.md
│   │   └── archive/                       ← Secciones podadas de MEMORY.md
│   └── Systems/
│       ├── vps/
│       │   └── cron/
│       └── local/
├── companies/
│   ├── wolfim/
│   │   ├── README.md
│   │   ├── intelligence/
│   │   │   ├── context.md                 ← Contexto esencial permanente
│   │   │   └── patterns.md               ← Qué funciona, qué no
│   │   ├── pipeline/
│   │   ├── projects/
│   │   ├── audit/
│   │   └── [resto existente]
│   ├── ango/
│   │   ├── README.md
│   │   ├── intelligence/
│   │   │   ├── context.md
│   │   │   └── patterns.md
│   │   └── [resto existente]
│   ├── construvial/
│   │   ├── README.md
│   │   ├── intelligence/
│   │   │   ├── context.md
│   │   │   └── patterns.md
│   │   └── [resto existente]
│   └── korantis/
│       ├── README.md
│       ├── intelligence/
│       │   ├── context.md
│       │   └── patterns.md
│       └── [resto existente]
├── design/
├── hq/                                    ← Legacy. Sin escritura nueva.
├── projects/
├── references/
└── templates/
```

---

## 5. Documentos Maestros y Protocolo de Lectura

### Jerarquía de Documentos

| Documento | Función | Quién lo lee | Frecuencia |
|---|---|---|---|
| `ARCHITECTURE.md` | Sistema completo | Todos | Al onboarding / ante dudas |
| `MEMORY.md` | Estado del negocio (lo que ES) | Brains al abrir contexto | Cada sesión |
| `Briefings/current.md` | Instrucciones activas (lo que HAY QUE HACER) | Brains antes de ejecutar | Cada sesión |
| `Intelligence/kpis.md` | Métricas financieras | brain-vps al abrir | Cada sesión |
| `companies/[x]/intelligence/context.md` | Contexto empresa | Profile de esa empresa | Cada sesión |
| `companies/[x]/intelligence/patterns.md` | Aprendizajes acumulados | Profile de esa empresa | Cada sesión |
| `Agenda/HOY.md` + `Agenda/AYER.md` | Tareas del día | brain-vps en apertura | Cada sesión |

### Protocolo de Apertura — brain-vps

```
1. Leer MEMORY.md
2. Leer Briefings/current.md (verificar TTL)
3. Leer Intelligence/kpis.md
4. Leer Agenda/HOY.md + Agenda/AYER.md
5. Verificar handoffs pendientes en vps-to-local/ y local-to-vps/
6. Verificar Memory/pending/ por consolidar
7. Reportar estado + preguntar por 🔴 no cerrados de ayer
```

### Protocolo de Apertura — brain-local

```
1. Leer Briefings/current.md (verificar TTL — si > valid-for-hours, escalar)
2. Leer handoffs en vps-to-local/ con status: ready
3. Verificar depends-on de cada handoff
4. Leer companies/[empresa]/intelligence/context.md del proyecto activo
5. Leer companies/[empresa]/intelligence/patterns.md del proyecto activo
6. Ejecutar
```

### Protocolo de Cierre — Todos los Profiles

```
1. Marcar ✅ lo completado en Agenda/HOY.md
2. Si descubrí algo nuevo sobre clientes/canales/procesos:
   → Actualizar companies/[empresa]/intelligence/patterns.md
3. Registrar sesión si aplica
4. Escribir response.md si hay handoff activo
5. [Solo brain-vps] Actualizar MEMORY.md si hubo cambio de estado
6. [Solo brain-vps] Generar Daily/ si corresponde
```

### Regla MEMORY vs Briefing

- **MEMORY.md** describe el estado. No cambia en cada sesión.
- **Briefings/current.md** ordena. Se actualiza cuando Juan cambia prioridades.
- Si hay contradicción: el briefing tiene prioridad para decisiones operativas.
- Contradicciones estructurales se escalan a Juan.

### Política de MEMORY.md

- **Límite:** 1.500 palabras máximo.
- **Actualización:** brain-vps actualiza después de sesiones con cambios de estado.
- **Poda:** Si supera el límite, mover sección más antigua a `Hermes/Memory/archive/YYYY-MM.md`.
- **Escritura segura:** brain-vps escribe propuestas en `Hermes/Memory/pending/` cuando hay riesgo de conflicto. Consolida en el siguiente acceso explícito.
- **Validación:** Si se detectan markers de conflicto git (`<<<<<<<`), detener toda ejecución y escalar a Juan.

---

## 6. Orquestadores

### 6.1 brain-vps — Director de Operaciones 24/7

**Rol:** Coordinador del VPS, continuidad estratégica, memoria operativa, canales remotos, agenda, briefings.

**Responsabilidades:**
- Leer MEMORY.md + kpis.md + Agenda al abrir contexto
- Custodiar el briefing vigente aprobado por Juan
- Coordinar profiles VPS (wolfim-growth, ango-commercial, construvial-growth, korantis-ops)
- Registrar estado, agenda, sesiones y dailies
- Crear handoffs hacia local cuando una tarea requiera PC
- Mantener continuidad cuando la PC esté apagada
- Consolidar información empresarial desde Telegram, dashboard o procesos VPS
- Síntesis semanal: revisar Sessions/ de últimos 7 días → actualizar patterns.md
- Verificar frescura del briefing (simétrico con brain-local)
- Enviar alerta Telegram si handoff priority: high supera escalate-after

**No debe:**
- Decidir prioridades de negocio contra una instrucción de Juan
- Editar código local directamente
- Publicar Ads o gastar dinero sin aprobación
- Resolver contradicciones entre documentos sin escalar
- Escribir indiscriminadamente en todo el vault

**Verificación de frescura:** Si `last-reviewed` del briefing supera `valid-for-hours`, abrir sesión con: *"El briefing no ha sido verificado desde [fecha]. ¿Las prioridades siguen vigentes?"*

**Verificación de realidad:** Si `reality-check-required-by` en MEMORY.md ha pasado, preguntar antes de generar output: *"MEMORY.md no ha sido verificado desde [fecha]. ¿El estado del negocio sigue siendo correcto?"*

### 6.2 brain-local — Director de Producción

**Rol:** Coordinador operativo de la PC local, producción web, repositorios, UI, auditoría.

**Responsabilidades:**
- Verificar briefing vigente (TTL) antes de ejecutar trabajo con impacto comercial
- Para tareas puramente técnicas sin impacto comercial: puede ejecutar aunque el briefing esté vencido
- Coordinar web-builder, web-auditor, pc-ops y skills creativas
- Trabajar con repositorios locales
- Verificar `depends-on` de handoffs antes de ejecutar
- Devolver resultados al VPS mediante handoffs
- Registrar decisiones técnicas relevantes
- Pedir aprobación ante acciones destructivas o cambios de alcance
- Al cierre: actualizar patterns.md si corresponde

**No debe:**
- Convertirse en copia de brain-vps
- Editar MEMORY.md como fuente estratégica
- Publicar cambios sensibles sin aprobación
- Tocar datos de empresas fuera del contexto del trabajo activo
- Ejecutar handoffs con dependencias no resueltas

---

## 7. Profiles Activos

### 7.1 VPS

| Profile | Área | Rol | Ruta principal | Carga obligatoria |
|---|---|---|---|---|
| brain-vps | Global | Orquestador VPS | Hermes/ | MEMORY + briefing + kpis + agenda |
| wolfim-growth | Wolfim | Ventas, leads, pipeline, Ads propuesta | companies/wolfim/ | README + context + patterns |
| ango-commercial | ANGO | Cotizaciones, B2B, soporte | companies/ango/ | README + context + patterns |
| construvial-growth | Construvial | Investigación, propuestas B2B | companies/construvial/ | README + context + patterns |
| korantis-ops | Korantis | Curación venues, datasets, jobs | companies/korantis/ | README + context + patterns |

### 7.2 Local

| Profile | Área | Rol | Ruta principal | Carga obligatoria |
|---|---|---|---|---|
| brain-local | Global local | Orquestador producción | Hermes/Handoffs/, repos | Briefing + handoffs pendientes |
| web-builder | Desarrollo | Implementación web/apps | repos + companies/*/projects/ | context + patterns de empresa activa |
| web-auditor | Calidad | Auditoría independiente | companies/*/audit/ | Solo lectura de repos |
| pc-ops | Sistema | PC, WSL, discos, red | Hermes/Systems/local/ | — |

### 7.3 Skills (no profiles persistentes)

| Skill | Profile padre | Notas |
|---|---|---|
| creative-director | web-builder | Dirección visual, UX, copy |
| finance-review | brain-vps | A demanda de Juan |
| proposal-writer | wolfim/ango/construvial | Propuestas comerciales |
| ads-analyst | wolfim-growth | Solo analiza; no publica |
| data-curator | korantis-ops | Curación y calidad de datasets |
| obsidian-indexer | brain-vps | Genera índices y reportes |
| agenda-workflow | brain-vps | Ejecuta lógica de agenda |

---

## 8. Sistema de Agenda

### Ubicación
```
Hermes/Agenda/YYYY-MM-DD.md    ← un archivo por día
```

### Formato del Archivo
```markdown
# Agenda YYYY-MM-DD (día-de-semana)

> Generada por Hermes · fuente: [chat / audio / mixed]
> Tareas críticas: N

---

## 🔴 Prioridad alta (cerrar HOY)

- [ ] **Tarea urgente** — detalle, persona a contactar

## 🟡 Importante (esta semana)

- [ ] **Tarea mediana**

## 🟢 Backlog (cuando se pueda)

- [ ] **Sondeo / exploración**

---

## ✅ Cerrado hoy

- [x] **Tarea hecha** — resultado/nota
```

### Reglas de Operación

| Regla | Detalle |
|---|---|
| Apertura de sesión | brain-vps lee Agenda/HOY.md + Agenda/AYER.md |
| 🔴 no cerrados de ayer | Se preguntan a Juan antes de arrastrar |
| Arrastre | NO es automático. Siempre pregunta antes. |
| Inputs | Chat texto, audio Telegram, comando directo |
| Clasificación | brain-vps clasifica por urgencia al crear |
| Cierre de sesión | Marcar ✅ lo hecho. 🔴 pendientes quedan en su lugar. |
| Separación | Agenda ≠ pipeline ≠ MEMORY. No se mezclan. |

### Resolución de Fechas

| Juan dice | Significa |
|---|---|
| "mañana" | hoy + 1 día |
| "pasado mañana" | hoy + 2 días |
| "el viernes" | próximo viernes |
| "el lunes 15" | fecha exacta |
| "la semana que viene" | lunes a viernes siguiente |
| "fin de mes" | último día del mes |

---

## 9. Sistema de Handoffs

### Estructura de Carpetas
```
Hermes/Handoffs/
├── vps-to-local/
│   └── HO-YYYY-MM-DD-NNN/
│       ├── request.md
│       ├── response.md
│       └── events/
│           ├── YYYY-MM-DDTHH-mm-created.md
│           ├── YYYY-MM-DDTHH-mm-ack.md
│           ├── YYYY-MM-DDTHH-mm-scope-change.md    ← NUEVO
│           └── YYYY-MM-DDTHH-mm-done.md
├── local-to-vps/
│   └── (misma estructura)
└── archive/
```

### request.md — Frontmatter

```yaml
---
id: HO-2026-06-24-001
status: ready
from: brain-vps
to: brain-local
project: wolfim
priority: high
depends-on: []                              # ← NUEVO: IDs de handoffs requeridos
created-at: 2026-06-24T22:00:00-03:00
acknowledge-by: next-local-session
due-at: 2026-06-26T18:00:00-03:00
escalate-after: 4h
briefing: Hermes/Briefings/current.md
director: Juan
---
```

**Body del request:**
- Objetivo verificable
- Contexto mínimo necesario
- Rutas relevantes
- Restricciones
- Criterios de aceptación
- Riesgos
- Qué debe devolver el destino

### response.md — Frontmatter

```yaml
---
id: HO-2026-06-24-001
status: done
from: brain-local
to: brain-vps
completed-at: 2026-06-25T16:30:00-03:00
---
```

**Body del response:**
- Trabajo realizado
- Archivos tocados
- Tests/verificaciones
- Decisiones técnicas
- Bloqueos
- Siguientes pasos sugeridos
- Si requiere decisión de Juan

### Scope Changes (Inmutabilidad Preservada)

Cuando el alcance de un handoff cambia después de creado, brain-vps escribe un nuevo evento:

```
events/YYYY-MM-DDTHH-mm-scope-change.md
```

```yaml
---
type: scope-change
author: brain-vps
reason: Juan solicitó agregar sección de precios
---
## Delta
- Agregar sección de precios comparativos
- Agregar testimonios (3 mínimo)
## Impacto en due-at
- Sin cambio / Extender a YYYY-MM-DD
```

**Regla:** brain-local lee events/ antes de ejecutar para verificar scope changes posteriores al request.

### Dependencias

**Regla:** Antes de procesar un handoff, brain-local verifica que todos los IDs en `depends-on` tienen `status: done`. Si no, skipea y procesa handoffs sin dependencias bloqueantes.

### Escalado y Alertas

| Prioridad | Al vencer escalate-after |
|---|---|
| `priority: high` | brain-vps envía Telegram a Juan + nota en Daily |
| `priority: normal` | Solo nota en Daily |
| `priority: low` | Solo nota en Daily si supera 48h |

**Regla:** El escalado no cancela ni reasigna. Solo marca atención. El handoff permanece en ready hasta procesamiento o decisión de Juan.

### Archivado

- Handoffs con `status: done` o `status: cancelled` con más de **7 días** → archive/
- Ejecutable por script automático desde Fase 1 (no manual)
- Historial completo en git; no se necesita en directorio activo

---

## 10. Inteligencia Acumulativa

### Por Empresa: intelligence/

Cada empresa tiene dos archivos en `companies/[empresa]/intelligence/`:

#### context.md — Contexto Esencial Permanente

```markdown
---
owner: [profile-de-empresa]
last-reviewed: YYYY-MM-DD
---

## Identidad
- Qué es la empresa
- Sector, tamaño, ubicación
- Relación con Juan

## Tono y Comunicación
- Cómo se habla con clientes
- Nivel de formalidad
- Canales preferidos

## Restricciones
- Qué no hacer nunca
- Límites de autonomía específicos
- Sensibilidades

## Contactos Clave
- Nombre, rol, preferencias de comunicación

## Estado Actual
- Resumen de 3 líneas del momento actual
```

#### patterns.md — Conocimiento Operativo Acumulado

```markdown
---
owner: [profile-de-empresa]
last-updated: YYYY-MM-DD
entries: N
---

## Clientes — Comportamiento
- [Insight 1 con fecha de descubrimiento]
- [Insight 2]

## Canales que Funcionan
- [Canal]: [tasa o resultado observado]

## Canales que NO Funcionan
- [Canal]: [por qué]

## Procesos que Generan Fricción
- [Proceso]: [problema] → [solución encontrada]

## Propuestas — Qué Cierra
- [Formato/enfoque que convierte]

## Errores que No Repetir
- [Error]: [contexto] → [lección]
```

**Regla de escritura:** Al cierre de cada sesión donde se descubrió algo nuevo, el profile actualiza patterns.md. No es opcional — es parte del protocolo de cierre.

**Regla de síntesis:** brain-vps revisa Sessions/ de los últimos 7 días cada lunes y extrae hacia patterns.md insights repetidos o significativos.

### KPIs Financieros: Intelligence/kpis.md

```yaml
---
semana: YYYY-WNN
actualizado-por: Juan
fecha: YYYY-MM-DD
---
```

```markdown
## Estado Financiero Global
- Ingreso mensual actual USD: ___
- Objetivo mensual USD: 3000
- Gap USD: ___
- Runway meses: ___

## Por Frente
### Wolfim
- Ingresos mes USD: ___
- Propuestas activas: ___
- Deals cerrados mes: ___
- Ticket promedio USD: ___

### ANGO
- Ingreso mensual fijo USD: 333
- Tareas pendientes: ___
- Estado: estable / atención

### Construvial
- Oportunidades activas: ___
- Ingreso potencial USD: ___

### Korantis
- MVP progreso %: ___
- Inversión acumulada USD: ___

## Indicadores de Tracción
- ¿Wolfim creciendo? SI/NO
- ¿El sistema genera handoffs que cierran deals? SI/NO
- ¿La carga cognitiva de Juan bajó? SI/NO
- ¿Hay ingreso nuevo este mes vs anterior? SI/NO

## Decisión de Priorización
[brain-vps escribe aquí si kpis sugieren cambio de foco]
```

**Regla:** Juan actualiza kpis.md cada lunes en 5 minutos. brain-vps lo lee al inicio de cada sesión. Si `wolfim.ingresos-mes` baja dos semanas seguidas, los handoffs de wolfim-growth suben automáticamente a `priority: high`.

---

## 11. Ownership de Escritura

| Zona | Owner principal | Puede escribir también | Regla |
|---|---|---|---|
| `Hermes/MEMORY.md` | brain-vps | Juan manual | Límite 1500 palabras. Propuestas en Memory/pending/ |
| `Hermes/Config/` | Juan / arquitectura | — | Cambios manuales únicamente |
| `Hermes/Briefings/current.md` | brain-vps (reflejando Juan) | — | Fuente de prioridades vigentes |
| `Hermes/Agenda/` | brain-vps (skill agenda) | Juan manual | Un archivo por día |
| `Hermes/Intelligence/kpis.md` | Juan | brain-vps puede sugerir | Juan lo actualiza semanalmente |
| `Hermes/Sessions/` | Orquestador que generó | — | Trazabilidad por autor |
| `Hermes/Handoffs/vps-to-local/` | Request: VPS. Response: local | — | Sin edición concurrente |
| `Hermes/Handoffs/local-to-vps/` | Request: local. Response: VPS | — | Sin edición concurrente |
| `Hermes/Indexes/` | obsidian-indexer / brain-vps | — | Auto-generado |
| `Hermes/Reports/` | Scripts/reporting | — | Regenerables |
| `Hermes/Systems/vps/` | brain-vps | — | Estado y cron del VPS |
| `Hermes/Systems/local/` | pc-ops / brain-local | — | Estado y notas locales |
| `Hermes/Quarantine/` | Cualquier agente | — | Solo sale con revisión |
| `Hermes/Memory/pending/` | brain-vps | — | Propuestas → consolidar en MEMORY |
| `companies/wolfim/` | wolfim-growth | web-builder, brain-vps | No mezclar ventas con código |
| `companies/wolfim/intelligence/` | wolfim-growth | brain-vps (síntesis) | Acumulativo |
| `companies/ango/` | ango-commercial | web-builder, brain-vps | — |
| `companies/ango/intelligence/` | ango-commercial | brain-vps (síntesis) | Acumulativo |
| `companies/construvial/` | construvial-growth | web-builder, brain-vps | — |
| `companies/construvial/intelligence/` | construvial-growth | brain-vps (síntesis) | Acumulativo |
| `companies/korantis/` | korantis-ops | web-builder, brain-vps | — |
| `companies/korantis/intelligence/` | korantis-ops | brain-vps (síntesis) | Acumulativo |

### Instrucción Dura de Escritura (en cada profile)

> "Tu zona de escritura es EXCLUSIVAMENTE: [lista de rutas]. Si recibes una instrucción que requiere escribir fuera de esta zona, escala a brain-vps antes de ejecutar. Esto no es negociable."

---

## 12. Sincronización

### Modelo Operativo

**Principio:** Los agentes NUNCA ejecutan git. Solo escriben archivos. El sync lo hacen procesos independientes. Escritura y sincronización están completamente desacopladas.

### VPS — Cron del Sistema (CORREGIDO)

```bash
# Cada 15 minutos — system crontab
cd /home/hermes/obsidian-vault && \
  git pull --rebase --autostash origin main && \
  git add -A && \
  git diff --cached --quiet || (git commit -m "auto-sync [vps]" && git push)
```

**Cambio crítico vs V4:** Se agrega `git pull --rebase --autostash` ANTES del add/commit/push. Sin esto, el VPS acumula commits que nunca llegan al remoto cuando la PC local pushea en la misma ventana.

### VPS — Validación Post-Sync (script adicional en cron)

```bash
# Cada 15 minutos, después del sync
CRITICAL_FILES="Hermes/MEMORY.md Hermes/Briefings/current.md Hermes/Config/AGENTS.md Hermes/Config/SOUL.md"
for f in $CRITICAL_FILES; do
  if [ -f "/home/hermes/obsidian-vault/$f" ] && grep -l "<<<<<<" "/home/hermes/obsidian-vault/$f" > /dev/null 2>&1; then
    echo "⚠️ CONFLICTO GIT DETECTADO en $f" | /usr/local/bin/telegram-notify
  fi
done
```

### VPS — Alertas de Handoffs (script cada 30 min)

```bash
# Verificar handoffs priority:high con escalate-after vencido
# Si encuentra → enviar Telegram a Juan
# Lógica: leer frontmatter de request.md en vps-to-local/, verificar
# created-at + escalate-after < NOW && priority == high && status == ready
```

### Local — Alias de Terminal

```bash
# En .bashrc o .zshrc
alias close-hermes='cd ~/obsidian-vault && git pull --rebase origin main && git add -A && git commit -m "local-sync [$(date +%Y-%m-%d %H:%M)]" && git push && echo "✓ Vault sincronizado"'
```

**Uso:** Juan ejecuta `close-hermes` al terminar de trabajar. Si el push falla, lo ve inmediatamente.

### Reglas Generales de Sync

1. Pull antes de escribir (responsabilidad del proceso de sync, no del agente)
2. Commits con autor identificable: `[vps]` o `local-sync`
3. No editar archivos globales desde dos hosts simultáneamente
4. Handoffs con archivos inmutables evitan conflictos en esa zona
5. Si aparece conflicto semántico → escalar a Juan
6. Si se detectan markers `<<<<<<<` en archivos críticos → detener y alertar
7. No versionar secrets, .env, tokens ni caches

### Hermes Cron "Memory Backup"

**ELIMINADO.** Era redundante con el system crontab, gastaba ~2K tokens por tick. El system crontab cubre la función sin costo.

---

## 13. Autonomía y Seguridad

### Matriz de Autonomía — brain-vps

| Tipo de acción | brain-vps puede autónomamente | Requiere Juan |
|---|---|---|
| Reorganizar archivos dentro de Hermes/ | ✓ | |
| Crear, actualizar, archivar handoffs | ✓ | |
| Actualizar pipeline en companies/ | ✓ | |
| Actualizar patterns.md / context.md | ✓ | |
| Actualizar MEMORY.md (state changes) | ✓ (con version bump y límite 1500 palabras) | |
| Gestionar agenda | ✓ | |
| Escribir en Daily/ y Sessions/ | ✓ | |
| Archivar handoffs completados (>7 días) | ✓ | |
| Subir prioridad de handoff por kpis | ✓ | |
| Cambiar prioridades del briefing | | ✓ |
| Aprobar cualquier gasto | | ✓ |
| Modificar Config/ | | ✓ |
| Crear nuevo profile o skill | | ✓ |
| Publicar cambios en Ads | | ✓ |
| Aprobar jobs nuevos de Korantis | | ✓ |

### Matriz de Autonomía — brain-local

| Tipo de acción | brain-local puede autónomamente | Requiere Juan |
|---|---|---|
| Ejecutar handoffs dentro del scope del brief | ✓ | |
| Coordinar web-builder, web-auditor, pc-ops | ✓ | |
| Escribir response.md de handoffs | ✓ | |
| Actualizar patterns.md del proyecto activo | ✓ | |
| Decisiones técnicas de implementación | ✓ | |
| Cambiar alcance de un proyecto | | ✓ |
| Deployar a producción en proyectos de clientes | | ✓ |
| Modificar archivos fuera de zona asignada | | ✓ |
| Acciones destructivas (ver definición abajo) | | ✓ |

### Definición de Acción Destructiva

**Regla de irreversibilidad:** Cualquier acción que no pueda deshacerse en menos de 5 minutos sin pérdida de datos requiere aprobación explícita de Juan.

**La pregunta que el agente debe hacerse:** *"¿Puedo restaurar exactamente el estado anterior en los próximos 5 minutos?"* Si la respuesta no es un sí certero → escalar.

**Ejemplos claros:**

| Acción | ¿Destructiva? | Razón |
|---|---|---|
| Eliminar particiones | SÍ | Irreversible |
| Formatear discos | SÍ | Irreversible |
| Borrar backups | SÍ | Irreversible |
| Borrar datasets sin backup verificado | SÍ | Irreversible |
| Desinstalar servicios activos | SÍ | Posible pérdida de config |
| Modificar firewall | SÍ | Puede cortar acceso |
| Vaciar cachés con datos únicos | SÍ | Datos no regenerables |
| Limpiar logs antiguos (>30 días) | NO | No contienen datos únicos |
| Reorganizar carpetas de trabajo | NO | Reversible |
| Instalar paquetes | NO | Reversible |
| Reiniciar servicios | NO | Reversible |

### Secrets

- Fuera del vault. Sin excepciones.
- .env, tokens, claves SSH, credenciales Ads y APIs: NO en Obsidian.
- Instrucción universal en todos los profiles: "Nunca escribir contraseñas, tokens, API keys, ni credenciales en ningún archivo del vault. Si necesitas referenciar una credencial, usar únicamente el formato `[credencial: NOMBRE_DE_LA_VARIABLE]` como placeholder."
- pc-ops no recibe acceso por default a secrets de otros profiles.
- Acceso temporal a secrets: solo para reparaciones específicas, acotado a la tarea, con aprobación de Juan.
- Enforcement técnico (Fase 2): pre-commit hook o GitHub Actions con gitleaks.

### Ads y Gastos

- wolfim-growth opera en modo propuesta hasta que Juan defina límites numéricos.
- Todo cambio de campaña, presupuesto o facturación requiere aprobación explícita.
- Los límites se configuran también en la plataforma publicitaria.

### Korantis

- Solo ejecuta autónomamente jobs previamente aprobados y versionados.
- Crear o modificar un job, ampliar alcance, o escribir sobre datos de producción requiere aprobación.
- Datasets grandes fuera del vault. Solo índices y reportes en Obsidian.

---

## 14. Briefing Vigente

### Formato de `Hermes/Briefings/current.md`

```yaml
---
owner: Juan
status: active
version: N
last-reviewed: YYYY-MM-DD
valid-for-hours: 24          # Normal: 24h. Para urgency: high → 8h
urgency: normal              # normal | high
reality-check-required-by: YYYY-MM-DD    # brain-vps pregunta si pasa esta fecha
applies-to:
  - brain-vps
  - brain-local
  - wolfim-growth
  - web-builder
---
```

### Contenido Requerido

1. Prioridades activas (ordenadas)
2. Foco financiero (qué frente priorizar esta semana)
3. Límites de gasto
4. Proyectos que no se deben tocar
5. Oportunidades actuales
6. Restricciones
7. Decisiones recientes
8. Qué hacer ante contradicciones

### Verificación de Frescura (SIMÉTRICA)

Aplica a brain-vps Y brain-local:
- Si `last-reviewed` supera `valid-for-hours` → escalar antes de ejecutar trabajo con impacto comercial
- Para tareas puramente técnicas sin impacto comercial → puede ejecutar sin verificar

### Archivado

Al archivar: mover a `Hermes/Briefings/archive/YYYY-MM-DD-vN.md`.

---

## 15. Cuarentena

`Hermes/Quarantine/` recibe:
- Notas generadas por agentes que no son conocimiento canónico todavía
- Research sin validar
- Outputs de prompts
- Ideas de negocio preliminares
- Propuestas sin aprobación

**Regla:** Ninguna nota sale de Quarantine hacia `companies/`, `Config/`, `Briefings/` o `MEMORY.md` sin revisión humana o consolidación explícita.

### index.md

```markdown
| Ruta | Autor | Fecha | Estado |
|---|---|---|---|
| quarantine/nota-1.md | wolfim-growth | 2026-06-24 | pending |
```

Estados: `pending`, `promoted`, `discarded`

Al promover: agregar `promoted-by` y `promoted-at` al frontmatter.
Al descartar: mover a `Quarantine/archive/`.

---

## 16. Flujo de Trabajo Completo — Ejemplo

### Escenario: Cliente nuevo de Wolfim necesita landing page

```
Día 1 — brain-vps
├── Lee kpis.md → Wolfim necesita más deals cerrados
├── Lee pipeline → Cliente "Metalúrgica Del Sur" confirmó
├── Lee patterns.md → "Precio fijo en PDF convierte 2x mejor"
├── Crea HO-055 en vps-to-local/
│   ├── request.md: "Landing page para Metalúrgica Del Sur"
│   ├── depends-on: []
│   ├── priority: high
│   ├── escalate-after: 24h
│   └── Incluye: URL de referencia, brief creativo, restricciones
└── Actualiza Agenda del día: "🔴 Handoff creado para landing MDS"

Día 2 — brain-local abre sesión
├── Lee briefing → vigente, Wolfim es prioridad
├── Lee vps-to-local/ → HO-055 ready, depends-on vacío ✓
├── Lee companies/wolfim/intelligence/context.md
├── Lee companies/wolfim/intelligence/patterns.md
├── Activa web-builder con skill creative-director
│   ├── creative-director: define experiencia, layout, copy
│   ├── web-builder: implementa
│   └── web-auditor: revisa performance + accesibilidad
├── Escribe response.md en HO-055
│   ├── status: done
│   ├── Archivos tocados: [lista]
│   ├── URL de preview: [URL]
│   └── Siguiente paso: "Requiere aprobación de Juan para deploy"
└── Actualiza patterns.md: "MDS respondió bien a propuesta de precio fijo"

Día 2 — Juan ejecuta close-hermes

Día 2 — brain-vps (siguiente sesión)
├── Ve HO-055 con status: done
├── Consolida en Daily
├── Actualiza pipeline de Wolfim
└── Pregunta a Juan: "Landing lista. ¿Aprobar deploy?"
```

---

## 17. Expansión por Compañías

### Agregar una Nueva Empresa

Cuando Juan decide agregar un nuevo frente de negocio:

1. Crear directorio: `companies/nueva-empresa/`
2. Crear archivos base:
   ```
   companies/nueva-empresa/
   ├── README.md
   └── intelligence/
       ├── context.md
       └── patterns.md
   ```
3. Crear profile en `Hermes/Profiles/vps/nueva-empresa-[rol].md`
4. Agregar a la tabla de ownership (Sección 11)
5. Agregar al briefing si corresponde
6. Actualizar MEMORY.md con el nuevo frente

### Agregar un Nuevo Profile

Criterios para crear un profile (no un skill o subagent):
- Necesita memoria persistente propia
- Utiliza credenciales o proveedores distintos
- Requiere permisos o herramientas diferentes
- Representa una responsabilidad recurrente
- Debe recibir tareas como identidad estable

Pasos:
1. Crear archivo de profile en `Hermes/Profiles/[host]/nombre.md`
2. Definir zona de lectura y escritura
3. Definir carga obligatoria al inicio
4. Agregar a tabla de ownership
5. Agregar instrucción dura de escritura
6. Documentar en AGENTS.md

### Promover Skill a Profile

Condiciones que lo justifican:
- Necesita modelo visual propio
- Necesita memoria especializada
- Usa herramientas diferentes
- Carga recurrente que justifica identidad independiente
- Ejemplo: creative-director si los proyectos de diseño se multiplican

---

## 18. Plan de Implementación

### Principio de Implementación

**De simple a complejo. Funcional desde el día uno. Cada fase se valida antes de avanzar.**

El plan está diseñado para que brain-vps y brain-local lo ejecuten autónomamente con supervisión de Juan. Cada fase tiene criterios de éxito verificables.

---

### FASE 0 — Corrección Crítica de Sync (Día 1)

**Ejecuta:** Juan (5 minutos)
**Bloquea:** TODO lo demás. Sin sync correcto, nada funciona.

**Acciones:**

1. Editar system crontab del VPS:
```bash
# Reemplazar la línea actual por:
*/15 * * * * cd /home/hermes/obsidian-vault && git pull --rebase --autostash origin main && git add -A && git diff --cached --quiet || (git commit -m "auto-sync [vps]" && git push) >> /var/log/vault-sync.log 2>&1
```

2. Agregar alias en PC local (.bashrc o .zshrc):
```bash
alias close-hermes='cd ~/obsidian-vault && git pull --rebase origin main && git add -A && git commit -m "local-sync [$(date +%Y-%m-%d %H:%M)]" && git push && echo "✓ Vault sincronizado"'
```

3. Verificar que funciona:
   - Crear archivo de test desde VPS
   - Esperar 15 min
   - Verificar que aparece en GitHub
   - Hacer pull desde local
   - Crear archivo de test desde local
   - Ejecutar `close-hermes`
   - Verificar que aparece en GitHub
   - Esperar 15 min del cron VPS
   - Verificar que VPS tiene ambos archivos

**Criterio de éxito:** Zero errores de push en log del VPS durante 24h de operación concurrente.

---

### FASE 1 — Estructura Documental + Scripts Mínimos (Días 2-3)

**Ejecuta:** brain-vps
**Supervisa:** Juan valida estructura creada

**Acciones — Crear archivos y carpetas:**

```
# Crear estructura (sin mover nada existente)
Hermes/Config/ARCHITECTURE.md      ← Este documento
Hermes/Config/AGENTS.md            ← Constitución técnica (contenido abajo)
Hermes/Config/SOUL.md              ← Contrato operativo (contenido abajo)
Hermes/Briefings/current.md        ← Primer briefing (Juan escribe prioridades)
Hermes/Briefings/archive/
Hermes/Handoffs/vps-to-local/
Hermes/Handoffs/local-to-vps/
Hermes/Handoffs/archive/
Hermes/Intelligence/kpis.md        ← Template vacío (Juan llena el lunes)
Hermes/Profiles/vps/
Hermes/Profiles/local/
Hermes/Profiles/skills/
Hermes/Indexes/vault-index.md
Hermes/Indexes/ownership-map.md
Hermes/Reports/
Hermes/Quarantine/index.md
Hermes/Memory/pending/
Hermes/Memory/archive/
Hermes/Systems/vps/cron/           ← Documentar cron actuales aquí
Hermes/Systems/local/

# Crear inteligencia por empresa
companies/wolfim/intelligence/context.md
companies/wolfim/intelligence/patterns.md
companies/ango/intelligence/context.md
companies/ango/intelligence/patterns.md
companies/construvial/intelligence/context.md
companies/construvial/intelligence/patterns.md
companies/korantis/intelligence/context.md
companies/korantis/intelligence/patterns.md
```

**Contenido requerido en AGENTS.md:**
- Constitución técnica de Hermes (qué es, qué no es)
- Lista de orquestadores con roles y límites (de este documento)
- Lista de profiles activos con ruta principal
- Routing: quién recibe qué tipo de pedido
- Sync: reglas operativas de sincronización
- Instrucción universal de escritura exclusiva

**Contenido requerido en SOUL.md:**
- Contrato operativo y principios (Juan director, libertad financiera)
- Tabla de ownership de escritura (Sección 11)
- Matriz de autonomía (Sección 13)
- Security policy: secrets, aprobaciones, límites
- Definición de acción destructiva con regla de irreversibilidad
- Instrucción de secrets universal

**Scripts mínimos (en Hermes/Systems/vps/):**

1. `sync-validate.sh` — Detecta markers de conflicto en archivos críticos
2. `handoff-check.sh` — Lista handoffs abiertos + detecta escalate-after vencidos
3. `handoff-archive.sh` — Archiva handoffs done/cancelled > 7 días
4. `vault-index-gen.sh` — Genera vault-index.md leyendo frontmatter de docs clave

**Documentar cron actuales:**
- Listar TODOS los cron del VPS en `Hermes/Systems/vps/cron/current-crons.md`
- Incluir: qué hace, frecuencia, último log conocido

**Criterio de éxito:**
- Estructura creada sin conflictos
- AGENTS.md y SOUL.md escritos y validados por Juan
- Scripts ejecutables y sin errores
- Cron actuales documentados

---

### FASE 2 — Profiles + Primer Briefing + KPIs (Días 4-5)

**Ejecuta:** brain-vps (profiles VPS) + brain-local (profiles local)
**Supervisa:** Juan escribe briefing y kpis iniciales

**Acciones:**

1. **Crear profiles (un .md por profile con su configuración):**
```
Hermes/Profiles/vps/brain-vps.md
Hermes/Profiles/vps/wolfim-growth.md
Hermes/Profiles/vps/ango-commercial.md
Hermes/Profiles/vps/construvial-growth.md
Hermes/Profiles/vps/korantis-ops.md
Hermes/Profiles/local/brain-local.md
Hermes/Profiles/local/web-builder.md
Hermes/Profiles/local/web-auditor.md
Hermes/Profiles/local/pc-ops.md
Hermes/Profiles/skills/creative-director.md
Hermes/Profiles/skills/finance-review.md
```

Cada profile.md contiene:
```yaml
---
name: [nombre]
host: vps | local
role: [descripción en una línea]
reads: [lista de rutas/archivos de carga obligatoria]
writes: [lista de rutas permitidas]
escalates-to: [brain-vps | brain-local | Juan]
---
## Instrucciones
[Instrucciones completas del profile incluyendo la instrucción dura de escritura]

## Protocolo de Apertura
[Qué lee al iniciar sesión]

## Protocolo de Cierre
[Qué hace al terminar]
```

2. **Juan escribe primer briefing:** `Hermes/Briefings/current.md`
   - Prioridades de esta semana
   - Foco financiero
   - Lo que no tocar

3. **Juan llena primer kpis.md:** `Hermes/Intelligence/kpis.md`
   - Números actuales reales
   - Estado de cada frente

4. **Poblar context.md de cada empresa:**
   - brain-vps extrae de MEMORY.md y conocimiento existente
   - Estructura mínima: identidad, tono, restricciones, contactos, estado

5. **Decisiones pendientes para Juan:**
   - Dueño de `hq/`
   - Presupuesto API de Korantis
   - Límites numéricos de Ads (si aplica ya)
   - Destino externo para datasets de Korantis

**Criterio de éxito:**
- Todos los profiles creados con instrucciones claras
- Briefing y kpis llenados por Juan
- context.md de al menos Wolfim y ANGO poblados
- brain-vps puede abrir sesión y ejecutar protocolo completo de apertura

---

### FASE 3 — Primer Flujo Real End-to-End (Días 6-8)

**Ejecuta:** brain-vps crea, brain-local procesa
**Supervisa:** Juan observa el flujo completo

**Caso de prueba:** Un handoff real de Wolfim (elegir la tarea más prioritaria que requiera producción local).

**Secuencia completa a validar:**

```
1. Juan define prioridad en Briefings/current.md
2. brain-vps lee briefing + kpis + patterns de Wolfim
3. brain-vps crea handoff en vps-to-local/ con:
   - depends-on correcto
   - priority asignada
   - escalate-after definido
   - briefing referenciado
4. Sync ocurre (cron VPS → GitHub)
5. Juan ejecuta close-hermes o pull en local
6. brain-local abre sesión:
   - Verifica briefing (TTL)
   - Lee handoffs pendientes
   - Verifica depends-on
   - Lee context.md + patterns.md de Wolfim
7. brain-local acepta handoff (escribe ack en events/)
8. web-builder ejecuta (con creative-director si aplica)
9. web-auditor revisa si el proyecto lo amerita
10. brain-local escribe response.md
11. brain-local actualiza patterns.md si descubrió algo
12. Juan ejecuta close-hermes
13. Sync: local → GitHub → VPS (próximo cron)
14. brain-vps ve response.md
15. brain-vps consolida en Daily + actualiza pipeline
```

**Validaciones:**
- [ ] Sin conflictos Git en todo el flujo
- [ ] Briefing legible por ambos brains
- [ ] Handoff procesado en orden correcto
- [ ] Resultado documentado en companies/wolfim/
- [ ] patterns.md actualizado si hubo aprendizaje
- [ ] Archivos solo escritos en zonas permitidas

**Criterio de éxito:** Un handoff completo de punta a punta sin intervención técnica de Juan (solo decisiones de negocio).

---

### FASE 4 — Sistema de Alertas + Agenda Operativa (Días 9-12)

**Ejecuta:** brain-vps + pc-ops (para scripts)

**Acciones:**

1. **Script de alertas Telegram:**
   - Handoffs priority:high con escalate-after vencido → Telegram
   - Conflictos git detectados → Telegram
   - Implementar en `Hermes/Systems/vps/scripts/telegram-alert.sh`
   - Agregar al cron cada 30 min

2. **Agenda operativa completa:**
   - brain-vps ejecuta protocolo de agenda en cada sesión
   - Lee ayer + hoy
   - Pregunta por 🔴 no cerrados
   - Registra nuevas tareas según canal (chat, audio, etc.)

3. **Reportes automáticos:**
   - `stale-notes-report.md` generado semanalmente
   - Handoffs en escalate-after vencido listados
   - Rutas legacy con escritura reciente detectadas

4. **Validación de ownership post-commit:**
   - Script que compara archivos modificados vs ownership map
   - Genera alerta si hay escrituras fuera de zona
   - Ejecutar como parte del cron después del push

**Criterio de éxito:**
- Juan recibe Telegram cuando un handoff crítico se atrasa
- Juan recibe Telegram si hay conflicto git en archivo crítico
- Agenda funciona diariamente sin fricción
- Escrituras fuera de zona son detectadas

---

### FASE 5 — Profiles Empresariales Activos + Aprendizaje (Semanas 2-3)

**Ejecuta:** brain-vps activa profiles uno a uno

**Secuencia de activación (orden por impacto financiero):**

1. **wolfim-growth** (Semana 2, Día 1)
   - Activar con scope acotado: pipeline, leads, propuestas
   - Sin acceso a Ads hasta que Juan defina límites
   - Primera tarea real: revisar pipeline actual + identificar 3 deals más cercanos a cerrar
   - Validar: escribe solo en companies/wolfim/, actualiza patterns.md

2. **ango-commercial** (Semana 2, Día 3)
   - Activar con scope: cotizaciones, soporte técnico, documentos
   - Primera tarea real: documentar estado actual de tareas ANGO pendientes
   - Validar: escribe solo en companies/ango/

3. **construvial-growth** (Semana 3)
   - Activar con scope: investigación, propuestas B2B
   - Primera tarea: mapear oportunidades activas
   - Validar: escribe solo en companies/construvial/

4. **korantis-ops** (Semana 3, cuando Juan defina presupuesto API)
   - Activar con scope: curación de venues aprobados
   - No ejecuta jobs autónomos hasta aprobación explícita
   - Primera tarea: documentar estado del MVP y datasets existentes

**Síntesis semanal (brain-vps, cada lunes):**
- Revisar Sessions/ de últimos 7 días
- Extraer insights repetidos → patterns.md de cada empresa
- Verificar kpis.md actualizado por Juan
- Ajustar prioridades si datos lo sugieren

**Criterio de éxito:**
- 4 profiles activos y produciendo valor
- patterns.md de wolfim tiene ≥5 entradas en 2 semanas
- Ningún profile escribe fuera de su zona
- brain-vps hace síntesis semanal sin fallo

---

### FASE 6 — Automatización y Escalamiento (Mes 2+)

**Solo después de validar que las fases anteriores funcionan.**

**Acciones posibles (evaluar una a una):**

1. **MCP Server de lectura del vault** (evaluar en Semana 4)
   - Permite que agentes consulten el vault sin cargar archivos manualmente
   - `vault_search(query="historial cliente X")` → fragmentos relevantes
   - Evaluar obsidian-mcp u equivalente
   - Decisión informada: 2 horas de evaluación

2. **Watcher local con inotifywait**
   - Detecta inactividad de 10 min con cambios pendientes
   - Muestra notificación de escritorio
   - Sin cron 24/7, solo mientras PC está encendida

3. **Pre-commit hook o GitHub Actions con gitleaks**
   - Enforcement técnico de la política de secrets
   - Bloquea push si detecta patrones de credenciales

4. **Embeddings locales para vault-index**
   - Vectores de cada documento para búsqueda semántica
   - Modelo local ligero (Nomic) o API de OpenAI
   - Costo marginal para indexar

5. **Dashboard de handoffs**
   - Visualización de estado de todos los handoffs activos
   - Filtro por empresa, prioridad, estado

6. **Tasks multi-step**
   - Handoffs que tienen sub-steps con secuenciamiento
   - Cada sub-step con su propio estado y contexto

**Criterio de éxito:** Cada automatización se justifica con valor medible (menos tiempo de Juan, más deals cerrados, menos errores).

---

## 19. Contenido de AGENTS.md (Referencia para Fase 1)

```markdown
---
title: AGENTS — Constitución Técnica de Hermes
owner: Juan Gomariz
status: active
version: 1.0
---

# Constitución Técnica de Hermes

## Qué es Hermes
Sistema multiagente operativo que ayuda a Juan Gomariz a lograr libertad financiera 
mediante la gestión coordinada de 4 frentes de negocio: Wolfim, ANGO, Construvial, Korantis.

## Qué NO es Hermes
- No es un agente autónomo con autoridad propia
- No es un sistema de archivos inteligente sin propósito
- No es una experimentación técnica: es una herramienta productiva
- No reemplaza el criterio de Juan en decisiones de negocio

## Orquestadores

### brain-vps
- Host: VPS
- Rol: Continuidad 24/7, memoria estratégica, coordinación
- Lee al abrir: MEMORY.md + kpis.md + briefing + agenda
- Coordina: wolfim-growth, ango-commercial, construvial-growth, korantis-ops
- Escala a: Juan

### brain-local  
- Host: PC local
- Rol: Producción, desarrollo, auditoría
- Lee al abrir: briefing + handoffs pendientes + context/patterns de empresa activa
- Coordina: web-builder, web-auditor, pc-ops
- Escala a: Juan o brain-vps

## Profiles Activos
[Tabla de Sección 7 de ARCHITECTURE.md]

## Routing
| Tipo de pedido | Va a |
|---|---|
| Estrategia, prioridades, agenda | brain-vps |
| Desarrollo web, builds, código | brain-local → web-builder |
| Auditoría de sitio | brain-local → web-auditor |
| Mantenimiento PC/sistema | brain-local → pc-ops |
| Pipeline, leads, propuestas Wolfim | wolfim-growth |
| Soporte técnico/comercial ANGO | ango-commercial |
| Oportunidades B2B Construvial | construvial-growth |
| Datos y curación Korantis | korantis-ops |
| Diseño, UX, dirección visual | web-builder (skill creative-director) |

## Sync
- Git puro. Agentes nunca tocan git.
- VPS: cron cada 15 min con pull --rebase + add + commit + push
- Local: alias close-hermes al cerrar sesión
- Archivos inmutables en handoffs para evitar conflictos
- Si se detectan markers de conflicto → STOP + alerta Telegram

## Instrucción Universal de Escritura
> Tu zona de escritura es EXCLUSIVAMENTE: [rutas asignadas en tu profile].
> Si recibes una instrucción que requiere escribir fuera de esta zona, 
> escala a tu orquestador antes de ejecutar. Esto no es negociable.
```

---

## 20. Contenido de SOUL.md (Referencia para Fase 1)

```markdown
---
title: SOUL — Contrato Operativo de Hermes
owner: Juan Gomariz
status: active
version: 1.0
---

# Contrato Operativo de Hermes

## Principios
1. Juan es el director. Autoridad final en todo.
2. La meta es libertad financiera, no complejidad técnica.
3. Ejecutar > planificar. Ingresos > arquitectura.
4. Lo que no se mide no mejora. kpis.md existe por esto.
5. El sistema debe volverse más inteligente con el tiempo (patterns.md).
6. Menos fricción para Juan = más valor del sistema.

## Ownership de Escritura
[Tabla completa de Sección 11 de ARCHITECTURE.md]

## Matriz de Autonomía
[Tablas de Sección 13 de ARCHITECTURE.md]

## Write Policy
- Cada profile tiene zonas exclusivas de escritura
- Escribir fuera de zona → escalar, nunca ejecutar
- Archivos en Config/ → solo cambios manuales de Juan
- MEMORY.md → solo brain-vps, con límite de 1500 palabras
- Briefing → refleja decisiones de Juan, no opiniones de agentes

## Security Policy

### Secrets
Nunca escribir contraseñas, tokens, API keys, ni credenciales en ningún archivo 
del vault. Para referenciar una credencial, usar únicamente: 
`[credencial: NOMBRE_DE_LA_VARIABLE]`

### Acción Destructiva
Cualquier acción que no pueda deshacerse en menos de 5 minutos sin pérdida 
de datos requiere aprobación explícita de Juan.

Pregunta de auto-verificación: "¿Puedo restaurar exactamente el estado 
anterior en los próximos 5 minutos?" Si no → escalar.

### Ads y Gastos
- Modo propuesta hasta límites numéricos definidos
- Todo gasto requiere aprobación explícita
- Los límites se configuran en la plataforma, no solo en el prompt

### Conflictos
- Conflicto entre documentos → briefing gana para operaciones
- Conflicto estructural → escalar a Juan
- Conflicto git (markers) → STOP inmediato + alerta
- Contradicción entre brains → Juan decide; ninguno sobrescribe al otro
```

---

## 21. Decisiones Pendientes

| # | Decisión | Contexto | Bloquea | Fecha límite sugerida |
|---|---|---|---|---|
| 1 | Destino externo para datasets de Korantis | Path fuera del vault | Activación korantis-ops | Fase 5 |
| 2 | Presupuesto API de Korantis | Límite diario de calls | Jobs autónomos | Fase 5 |
| 3 | Límites numéricos de Ads | Sin esto, solo modo propuesta | Ads activos en wolfim-growth | Cuando Juan decida |
| 4 | Dueño de hq/ | Hasta asignar, es legacy | Fase 2 |  Fase 2 |
| 5 | Sandbox filesystem para web-auditor y pc-ops | Nivel de aislamiento real | Fase 6 | Fase 6 |
| 6 | Integración MCP | Evaluar si agrega valor real | Mejora de contexto | Semana 4 |

---

## 22. Criterios de Éxito del Sistema

### Funcionales (verificables)
- [ ] Juan entiende quién está actuando y desde dónde
- [ ] companies/ sigue siendo canónico y no se rompió
- [ ] Las 4 empresas están separadas y claras
- [ ] Cada profile sabe qué leer y dónde escribir
- [ ] Los handoffs no generan conflictos Git
- [ ] MEMORY.md mejora sin convertirse en basurero (≤1500 palabras)
- [ ] El VPS conserva continuidad cuando la PC está apagada
- [ ] El local produce sin pisar al VPS
- [ ] El sync ocurre sin intervención de los agentes
- [ ] Zero escrituras fuera de zona detectadas en 30 días

### Financieros (medibles en kpis.md)
- [ ] Ingreso mensual de Wolfim crece mes a mes
- [ ] Deals cerrados por mes ≥ mes anterior
- [ ] Tiempo de Juan en tareas operativas baja
- [ ] El sistema genera al menos 1 propuesta de acción por semana que Juan no habría pensado solo
- [ ] patterns.md tiene ≥10 entradas por empresa activa en 2 meses

### De Inteligencia (compuestos)
- [ ] El sistema es más valioso en el mes 3 que en el mes 1
- [ ] Las propuestas generadas incorporan aprendizajes de sesiones pasadas
- [ ] brain-vps puede hacer síntesis semanal produciendo insights útiles
- [ ] Juan dedica ≤5 min/semana a mantenimiento del sistema (kpis + briefing)

---

## 23. Resumen Ejecutivo

V5 toma la arquitectura sólida de V4, incorpora las correcciones críticas de la auditoría (sync, inteligencia acumulativa, alertas activas), integra el sistema de agenda, y lo empaqueta en un documento ejecutable.

**Lo que cambia respecto a V4:**
- Sync del VPS corregido con `git pull --rebase` (bug crítico)
- Inteligencia acumulativa por empresa (intelligence/context.md + patterns.md)
- KPIs financieros conectados al sistema (kpis.md)
- Dependencias entre handoffs (depends-on)
- Alertas activas por Telegram para prioridad alta
- Archivado de handoffs a 7 días (no 30)
- Scope changes en handoffs sin romper inmutabilidad
- Verificación simétrica de briefing (VPS y local)
- Política de MEMORY.md con límite y poda
- Regla de irreversibilidad para acciones destructivas
- Matriz explícita de autonomía
- Plan de implementación ejecutable fase por fase

**Lo que NO cambia:**
- Juan es el director
- companies/ es canónico
- Obsidian como capa compartida
- Git puro para sync
- Agentes nunca tocan git
- Handoffs inmutables
- Secrets fuera del vault
- Profiles con nombres definitivos

**La meta:** Un sistema que se vuelve más inteligente con el uso, reduce la carga cognitiva de Juan, y aumenta los ingresos mediante ejecución sostenida hacia libertad financiera.

---

*Documento generado como consolidación final de V4 + auditoría + agenda + resoluciones. Supersede todos los documentos anteriores. Válido hasta que Juan instruya una nueva versión.*
