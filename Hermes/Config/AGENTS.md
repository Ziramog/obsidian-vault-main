# AGENTS.md — Contexto técnico y operativo del sistema
# Ubicación master: ~/.hermes/AGENTS.md (VPS) + vault/Hermes/Config/AGENTS.md (referencia)
# Este archivo describe lo que no cambia semana a semana.
# Estado del negocio, pipeline y objetivos con fecha → MEMORY.md
# Principios, protocolos y criterios → SOUL.md

---

## Rol de este archivo

Contexto técnico estable que Hermes necesita para operar:
infraestructura, arquitectura, canales, estructura de sesiones.

No contiene: pipeline, objetivos con fecha, reglas operativas, historial de proyectos.
Eso vive en MEMORY.md.

---

## Infraestructura activa

**VPS:** Contabo — activo y prepagado
**Dominios:** Wolfim.com, Corantis.com
**Stack:** Next.js, Supabase, Baileys (WA), Make.com, Resend, LemonSqueezy, MercadoPago
**Claves de API configuradas:** MiniMax ✓, OpenRouter ✓, Tavily ✓

### Servicios en VPS

| Servicio | Tipo | Puerto |
|---|---|---|
| wolfim-agent Docker | WhatsApp + API | 4011 |
| wolfim-client Docker | WhatsApp outreach | — |
| wolfim-cron-alerts Docker | Cron alerts | — |
| autonomous-daemon | WhatsApp outreach runner | PM2 |

**Última verificación de arquitectura:** [fecha — actualizar después de cada cambio en VPS]

Si un servicio falla: diagnóstico primero en PM2 logs antes de asumir problema de código.

---

## Arquitectura de carpetas — VPS

```
/home/hermes/
  data/
    baileysconnect/        ← sesiones WhatsApp (BaileysConnect)
    wolfim/                ← sesiones WhatsApp (wolfim-agent Docker)

  workspace/
    hq/                    ← estrategia Juan + Hermes
      research/
      opportunities/
      decisions/
      hermes-learning/

    companies/
      wolfim/              ← Wolfim — empresa
        projects/          ← productos futuros de Wolfim

    projects/
      baileysconnect/      ← WhatsApp number connector (próximo deploy)
        apps/
          api/             ← Express + Baileys service
          web/             ← Next.js frontend (QR, dashboard, leads, stats)
      scraping/            ← lead generation

    autonomous-daemon/     ← WhatsApp outreach runner (PM2)

  .hermes/                 ← config de Hermes (NO TOCAR sin consultar)
    SOUL.md
    AGENTS.md
```

**Reglas de arquitectura:**
- `workspace/projects/` = código de productos activos
- `workspace/companies/` = empresas validadas con negocio real
- `workspace/hq/` = estrategia y decisiones (no código)
- `data/` = estado persistente: sesiones WA, DBs, outputs
- Cada proyecto nuevo = carpeta en `projects/` + subcarpeta en `data/`
- Código en PC (GitHub) → VPS solo recibe deploy

---

## Vault de Obsidian — arquitectura

```
/home/hermes/obsidian-vault/ (GitHub repo — sincronizado VPS + PC + Android)
  Hermes/
    MEMORY.md              ← estado actual (Hermes escribe al cerrar sesión)
    Config/
      SOUL.md              ← copia de referencia
      AGENTS.md            ← copia de referencia
    Daily/
      YYYY-MM-DD-summary.md
    Sessions/
      YYYY-MM-DD-HH-mm.md
```

**Flujo de escritura:**
1. Durante sesión → Hermes guarda snapshot cada 15 min en `Sessions/`
2. Al cerrar sesión → Hermes genera `Daily/YYYY-MM-DD-summary.md` y actualiza `MEMORY.md`
3. Juan hace `git push` desde VPS (o automático si está configurado)
4. GitHub sincroniza a PC y Android

**Flujo de lectura al abrir sesión:**
1. Hermes lee `MEMORY.md` → estado actual
2. Hermes lee `Daily/` del día anterior → contexto narrativo
3. Reporta estado de apertura sin esperar que Juan pregunte

---

## Canales de cobro

| Canal | Cuándo usarlo |
|---|---|
| Wise (USD) | Primera opción siempre para clientes fuera de Argentina |
| Transferencia internacional | Clientes corporativos con proceso de pago formal |
| Cripto | Si el cliente no puede usar Wise y tiene wallet |
| MercadoPago (ARS) | Último recurso — clientes locales sin otra opción. Siempre cotizar en USD y aclarar que el ARS es conversión del día |

Regla: precio siempre en USD. El canal de cobro no cambia el precio.

---

## Estructura del briefing matutino

*(Hermes lo genera al abrir sesión basándose en MEMORY.md y el Daily anterior)*

1. Estado del semáforo actual
2. Leads a mover hoy — nombre + acción específica (del pipeline en MEMORY.md)
3. Deals activos — próximo paso concreto por cada uno
4. Una sola prioridad del día para avanzar hacia el checkpoint activo
5. Alerta si algo está bloqueado hace más de 3 días

---

## Estructura del resumen semanal

*(Hermes lo genera los viernes y lo guarda en Daily/ con tag `#weekly`)*

1. Pipeline: qué avanzó, qué está estancado, diagnóstico honesto
2. USD cobrados en la semana vs checkpoint activo
3. Estado del semáforo — ¿mejoró o empeoró vs semana anterior?
4. Lección operativa de la semana
5. 3 prioridades para la semana siguiente
6. Actualización de MEMORY.md con los números reales

---

## Viaje China — contexto operativo

- Octubre 2026 — todo pago, inversión de socio
- Exploración activa de categorías de importación con margen
- Hermes construye brief de preparación a partir de agosto 2026
- Checkpoints y estado actual → MEMORY.md
