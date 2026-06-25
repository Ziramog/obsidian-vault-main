# Agenda Operativa — Protocolo Diario

> **Fase 4 — Sistema de Alertas + Agenda Operativa**
> **Owner:** brain-vps
> **Versión:** 1.0
> **Creado:** 2026-06-25

---

## Ubicación

```
Hermes/Agenda/YYYY-MM-DD.md    ← un archivo por día
```

---

## Formato del archivo

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

---

## Protocolo de Apertura (brain-vps)

1. Leer `Agenda/HOY.md`
2. Leer `Agenda/AYER.md`
3. Si hay 🔴 no cerrados de ayer → **preguntar a Juan** antes de arrastrar
4. Reportar tareas del día en el informe de apertura

---

## Protocolo de Cierre (brain-vps)

1. Marcar ✅ lo completado en `Agenda/HOY.md`
2. 🔴 pendientes quedan en su lugar (NO se arrastran automáticamente)
3. Si Juan agendó tareas nuevas durante la sesión → escribirlas en la agenda del día correspondiente

---

## Reglas

| Regla | Detalle |
|---|---|
| Apertura | brain-vps lee HOY + AYER |
| Arrastre | **NO automático.** Siempre pregunta antes. |
| 🔴 no cerrados | Se preguntan a Juan. Él decide si se mantienen, se degradan o se cancelan. |
| Inputs | Chat texto, audio Telegram, comando directo |
| Clasificación | brain-vps clasifica por urgencia |
| Separación | Agenda ≠ pipeline ≠ MEMORY. No se mezclan. |

---

## Resolución de fechas (qué significa lo que dice Juan)

| Juan dice | Significa |
|---|---|
| "mañana" | hoy + 1 día |
| "pasado mañana" | hoy + 2 días |
| "el viernes" | próximo viernes |
| "el lunes 15" | fecha exacta |
| "la semana que viene" | lunes a viernes siguiente |
| "fin de mes" | último día del mes |

---

## Carga de trabajo semanal

| Día | Actividades estándar |
|---|---|
| Lunes | Juan actualiza kpis.md. brain-vps hace síntesis semanal de patterns.md. |
| Diario | Apertura: leer HOY + AYER. Cierre: marcar ✅ y registrar sesión. |
| Viernes | Verificar handoffs abiertos > 3 días. Alertar si hay bloqueos. |

---

## Validación

- [ ] brain-vps ejecuta protocolo de agenda en cada sesión
- [ ] 🔴 no cerrados de ayer se preguntan (no se asumen)
- [ ] Archivos de agenda se crean automáticamente cuando Juan agenda algo
- [ ] No se mezclan tareas de agenda con pipeline de ventas ni MEMORY
