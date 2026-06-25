# 📚 Arquitectura del Vault de Obsidian

> **Ubicación:** `/home/hermes/obsidian-vault/` (master)
> **Synced a:** GitHub (Ziramog/obsidian-vault-main) → PC + Android
> **Última revisión arquitectónica:** 2026-06-24
> **Documentos maestros:** `Hermes/MEMORY.md` (estado), `Hermes/Config/SOUL.md` (principios), `Hermes/Config/AGENTS.md` (infraestructura)

---

## 🧠 Filosofía del vault

Este vault es la **memoria externa del sistema Hermes + Juan**. No es un repositorio de apuntes personales ni un wiki genérico. Cumple tres funciones:

| Función | Qué contiene | Quién escribe |
|---------|-------------|---------------|
| **Estado del negocio** | Números, semáforo, pipeline, acciones pendientes | Hermes al cerrar sesión |
| **Memoria operativa** | Sesiones, decisiones, patrones detectados, agenda | Hermes durante la sesión |
| **Conocimiento por empresa** | Clientes, productos, research, finanzas | Hermes + Juan |

**Regla de oro:** Si no está en el vault, no pasó. Si está desactualizado, está roto.

---

## 🗺️ Mapa completo del vault

```
obsidian-vault/
│
├── 📂 Daily/                          ← Resúmenes diarios (1 archivo/día)
│   └── YYYY-MM-DD-summary.md
│
├── 📂 Hermes/                         ← 🏆 NÚCLEO OPERATIVO
│   ├── 📄 MEMORY.md                   ← Estado maestro del negocio (se lee SIEMPRE al abrir)
│   ├── 📂 Agenda/                     ← Tareas del día (formato 🔴🟡🟢)
│   ├── 📂 Config/                     ← Documentos que NO CAMBIAN
│   │   ├── 📄 SOUL.md                 ← Contrato operativo, principios, protocolos
│   │   ├── 📄 AGENTS.md               ← Arquitectura técnica (VPS, stack, canales)
│   │   └── 📂 Remote-Access/          ← Setup y troubleshooting de Tailscale
│   ├── 📂 Daily/                      ← Briefings diarios generados al cerrar sesión
│   ├── 📂 Intelligence/               ← Investigaciones de mercado / inteligencia
│   ├── 📂 Projects/                   ← Documentación de proyectos activos
│   ├── 📂 Sessions/                   ← ÚNICA ubicación autorizada de sesiones
│   │   ├── YYYY-MM-DD.md             ← Sesiones completas (antes de mayo 2026)
│   │   └── YYYY-MM-DD-HH-mm.md       ← Snapshots cada 15 min (desde mayo 2026)
│   └── 📂 companies/                  ← Data operativa por empresa (corporativa)
│       ├── 📂 wolfim/                 ← Clientes, leads, datos de Wolfim
│       ├── 📂 korantis/               ← Runs, reports, handoffs de Korantis
│       └── 📂 construvial/            ← Catálogos y specs
│
├── 📂 companies/                      ← 📋 CONOCIMIENTO POR EMPRESA
│   ├── 📂 ango/                       ← Metalúrgica (padre)
│   │   ├── 📄 README.md               ← Resumen, contacto, producto
│   │   ├── 📂 brand/
│   │   ├── 📂 clients/
│   │   ├── 📂 finances/
│   │   ├── 📂 projects/
│   │   └── 📂 research/              ← Investigación de patentes, mercado
│   ├── 📂 construvial/               ← Construcción (amigo)
│   │   ├── 📄 README.md
│   │   ├── 📄 PLAN.md
│   │   ├── 📂 Informes/
│   │   ├── 📂 brand/
│   │   ├── 📂 clients/
│   │   ├── 📂 finances/
│   │   ├── 📂 projects/
│   │   ├── 📂 propuesta_2026/
│   │   └── 📂 research/
│   ├── 📂 korantis/                   ← Venue intelligence (proyecto)
│   │   ├── 📄 README.md
│   │   ├── 📄 scraping-policy.md
│   │   ├── 📂 audit/
│   │   ├── 📂 data/
│   │   ├── 📂 references/
│   │   │   └── 📂 ba-venues/
│   │   ├── 📂 scraping-outputs/
│   │   └── 📂 tmp-files/
│   └── 📂 wolfim/                     ← 🥇 EMPRESA PRINCIPAL
│       ├── 📄 README.md               ← Resumen, status, modelo de negocio
│       ├── 📂 brand/                  ← Marca, logo, identidad
│       │   ├── 📄 BRAND.md
│       │   ├── 📄 producto-y-ventas.md
│       │   ├── 📂 propuestas/
│       │   └── 📂 scripts/
│       ├── 📂 clients/                ← 🏆 CLIENTES (un index.md por cliente)
│       │   ├── 📂 ann/
│       │   ├── 📂 conforti-propiedades/
│       │   ├── 📂 franco-roma/        ← ✅ Cerrado
│       │   ├── 📂 gamma/
│       │   ├── 📂 luis-farias/        ← 🔥 Propuesta enviada
│       │   ├── 📂 paolini-automotores/
│       │   └── 📂 rivas-inmuebles/
│       ├── 📂 finances/               ← Revenue tracker, gastos
│       │   └── 📄 revenue-tracker.md
│       ├── 📂 google-ads/             ← Templates y campañas
│       ├── 📂 leads/                  ← Leads generados (batch por campaña)
│       │   ├── 📂 web-vieja-2026/
│       │   └── 📂 web-vieja-2026-v2/
│       ├── 📂 pipeline/               ← Pipeline de ventas
│       ├── 📂 projects/               ← Productos/servicios de Wolfim
│       │   ├── 📄 webagency.md
│       │   ├── 📄 portfolio-servicios.md
│       │   ├── 📄 deploy-wolfim-ag.md
│       │   ├── 📄 migracion-wolfim-com.md
│       │   └── 📂 korantis/
│       ├── 📂 research/               ← Investigación de competencia y mercado
│       │   ├── 📂 competencia/
│       │   │   ├── 📂 2clics/
│       │   │   ├── 📂 estudiodmg/
│       │   │   └── 📂 ruatta-automotores/
│       │   ├── 📂 hermes-research/
│       │   └── 📂 inmobiliarias-cordoba-2026/
│       └── 📂 services/               ← Servicios ofrecidos
│           └── 📄 mantenimiento-base.md
│
├── 📂 design/                         ← 🎨 DESIGN SYSTEM REFERO
│   └── 📂 refero/
│       ├── 📄 README.md
│       ├── 📄 mcp.md
│       ├── 📂 companies/
│       ├── 📂 page-types/
│       ├── 📂 ui-elements/
│       ├── 📂 ux-flows/
│       └── 📂 ux-patterns/
│
├── 📂 gpt/                            ← Outputs de GPT (análisis, planes)
│   ├── 📄 LOOP-outreach.md
│   └── 📄 WHATSAPP-BRIDGE-PLAN.md
│
├── 📂 hq/                             ← 🏛️ CUARTEL GENERAL (estrategia y decisiones)
│   ├── 📂 analyses/                   ← Análisis del negocio
│   ├── 📂 finances/                   ← Finanzas generales
│   ├── 📂 inbox/                      ← Bandeja de entrada
│   ├── 📂 leads/                      ← Leads generales
│   ├── 📂 sessions/                   ← ⚠️ LEGACY — migrar a Hermes/Sessions/
│   ├── 📂 skill-reports/              ← Reports diarios de skills
│   ├── 📂 vault-migration/            ← Plan de migración del vault
│   └── 📄 x2brain.md
│
├── 📂 projects/                       ← Proyectos externos
│   └── 📂 startup-incubator/
│
├── 📂 references/                     ← Referencias permanentes
│   ├── 📄 concesionarias-vertical.md
│   ├── 📄 mnemosyne-memory.md
│   └── 📄 yc-companies-directory.md
│
└── 📂 templates/                      ← Templates reutilizables
    └── 📂 propuestas/
```

---

## 📊 Volumen del vault

| Métrica | Valor |
|---------|-------|
| **Carpetas raíz** | 10 (`Daily`, `Hermes`, `companies`, `design`, `gpt`, `hq`, `projects`, `references`, `templates`) |
| **Total archivos .md** | ~220 |
| **Sesiones Hermes/Sessions/** | ~30 |
| **Sesiones hq/sessions/ (legacy)** | ~60 (pendientes de migrar) |
| **Dailys** | ~50 |
| **Clientes documentados** | 7 (Franco, Luis, Rivas, Conforti, Gamma, Ann, Paolini) |
| **Empresas activas** | 3 (Wolfim, Ango, Construvial) + 1 proyecto (Korantis) |

---

## 📐 Estructura por tipo de documento

### 📄 README.md — Puerta de entrada de cada empresa
Cada empresa tiene un `README.md` en su carpeta raíz que funciona como ficha técnica:

```markdown
# [Nombre Empresa]
## Resumen
- Qué hace, desde cuándo, ubicación
## Producto/Servicio principal
- Lo que venden
## Datos comerciales
- Contacto, garantía, envíos
## Estructura de carpetas
- Mapa de la carpeta
```

### 📄 index.md — Carpeta de cliente
Cada cliente de Wolfim tiene un `index.md` en `companies/wolfim/clients/{cliente}/` que contiene:
- Datos de contacto
- Historial de interacciones
- Estado del deal
- Próxima acción

### 📄 MEMORY.md — Estado maestro del negocio
Se lee al **abrir cada sesión**. Contiene:
- Semáforo financiero (🔴🟡🟠🟢)
- Proyecto activo y su pipeline
- Configuración técnica actual
- Última actualización con fecha

### 📄 YYYY-MM-DD-summary.md — Daily Summary
Generado al **cerrar cada sesión**. Contiene:
1. Empresa(s) trabajadas y estado
2. Semáforo al cierre
3. Acciones comprometidas con responsable y fecha
4. Leads tocados o pendientes
5. Patrones detectados
6. Próxima acción prioritaria

### 📄 YYYY-MM-DD-HH-mm.md — Snapshot de sesión
Guardado cada **15 min durante la sesión**. Contiene:
- Empresa activa
- Decisiones tomadas
- Acciones comprometidas
- Bloqueos detectados

---

## 🔄 Flujos de escritura

### Durante una sesión
```
Cada 15 min → Hermes/Sessions/YYYY-MM-DD-HH-mm.md
```

### Al cerrar sesión
```
1. Hermes/Daily/YYYY-MM-DD-summary.md   (narrativa del día)
2. Hermes/MEMORY.md                       (estado actualizado)
3. git add -A && git commit && git push   (sync a GitHub)
```

### Al abrir sesión
```
1. Leer Hermes/MEMORY.md                  → estado actual
2. Leer Hermes/Daily/{ayer}-summary.md    → contexto narrativo
3. Reportar estado sin esperar pregunta
```

---

## ⚠️ Problemas conocidos (tech debt)

| Problema | Impacto | Plan |
|----------|---------|------|
| **`hq/sessions/`** tiene ~60 archivos que duplican `Hermes/Sessions/` | Confusión sobre dónde están las sesiones | Migrar a `Hermes/Sessions/` y eliminar `hq/sessions/` |
| **`Hermes/Sessions/`** tiene formato mixto (archivos planos + carpetas con snapshots) | Inconsistencia de naming | Estandarizar a `YYYY-MM-DD-HH-mm.md` |
| **`companies/wolfim/leads/`** tiene leads individuales que también están en Supabase | Duplicación de datos | Los .md son referencia; Supabase es fuente de verdad |
| **`Hermes/companies/`** duplica estructura de `companies/` | Dos árboles de empresas | Unificar en `companies/` y eliminar `Hermes/companies/` |

---

## 🧭 Cómo navegar el vault

| Si querés... | Andá a... |
|--------------|-----------|
| Estado actual del negocio | `Hermes/MEMORY.md` |
| Reglas operativas y contrato | `Hermes/Config/SOUL.md` |
| Arquitectura técnica (VPS, stack) | `Hermes/Config/AGENTS.md` |
| Tareas del día | `Hermes/Agenda/YYYY-MM-DD.md` |
| Última sesión | `Hermes/Daily/{ayer}-summary.md` |
| Clientes de Wolfim | `companies/wolfim/clients/{cliente}/index.md` |
| Finanzas de Wolfim | `companies/wolfim/finances/revenue-tracker.md` |
| Pipeline de ventas | `companies/wolfim/pipeline/index.md` |
| Research de competencia | `companies/wolfim/research/competencia/` |
| Información de Ango | `companies/ango/README.md` |
| Información de Construvial | `companies/construvial/README.md` |
| Design system Refero | `design/refero/README.md` |
| Proyecto startup-incubator | `projects/startup-incubator/` |
| Acceso remoto VPS | `Hermes/Config/Remote-Access/README.md` |

---

## 🔐 Sync y respaldo

| Destino | Frecuencia | Método |
|---------|------------|--------|
| GitHub (Ziramog/obsidian-vault-main) | Cada 15 min | Cron VPS: `git add -A && git commit -m "auto-sync" && git push` |
| PC de Juan | Bajo demanda | Pull desde GitHub |
| Android (Obsidian) | Bajo demanda | Pull desde GitHub |

> **Regla:** El VPS es la fuente de verdad. GitHub es el medio. PC y Android son consumidores.

---

## 📌 Convenciones de nomenclatura

| Elemento | Formato | Ejemplo |
|----------|---------|---------|
| Daily Summary | `YYYY-MM-DD-summary.md` | `2026-06-24-summary.md` |
| Snapshot de sesión | `YYYY-MM-DD-HH-mm.md` | `2026-06-24-15-30.md` |
| Agenda | `YYYY-MM-DD.md` | `2026-06-24.md` |
| Carpeta de cliente | `{nombre-apellido}/` | `franco-roma/` |
| Index de cliente | `index.md` | `clients/franco-roma/index.md` |
| Research | `{tema}-{fecha}.md` | `inmobiliarias-cordoba-2026/INFORME-...md` |
| Proyecto | `{nombre-proyecto}.md` | `webagency.md` |
| README de empresa | `README.md` | `companies/wolfim/README.md` |

---

*Documento generado el 2026-06-24. Mantener actualizado si la estructura del vault cambia significativamente.*
