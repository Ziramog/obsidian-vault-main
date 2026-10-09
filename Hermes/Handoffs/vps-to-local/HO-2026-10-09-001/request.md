---
id: HO-2026-10-09-001
status: ready
from: brain-vps
to: brain-local
project: hermes-system
priority: high
depends-on: []
created-at: 2026-10-09T07:45:00-03:00
acknowledge-by: next-local-session
due-at: 2026-10-11T18:00:00-03:00
escalate-after: 48h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — PWA: pestaña "HOY" (leer el día en 2 segundos, sin chat)

## Objetivo verificable

Que Juan pueda ver **qué tiene pendiente hoy** en el celular en **≤2 segundos**, sin pasar por una sala de chat ni esperar la respuesta de un agente, y que pueda **tirar algo crudo** sin esperar nada.

Trabajo sobre la PWA que ya existe (`~/hermes-pwa`, repo `Ziramog/PWA-Hermes`, Next + next-pwa, mobile-first, ya conectada al API server de Hermes). **No crear app nueva.**

## Contexto (dicho por Juan, 09/10)

> "el bot agenda funciona mal, es lento, no tiene dinámica... pegar acá tienen demoras de un minuto a dos minutos para responder es inviable. mejor un lápiz y un papel."

El diagnóstico del VPS y tuyo es el mismo: el error de diseño es **tener que esperar una respuesta de agente para saber qué hay pendiente**. La traducción del "lápiz y papel" es: capturar sin esperar + leer en 2 segundos.

## Alcance

1. **Pestaña "HOY"** (mobile-first): renderiza, sin round-trip de agente:
   - `Hermes/Agenda/HOY.md` → los 3 del día (WIP).
   - `Hermes/Agenda/Frentes.md` → el conteo por bucket (🔴 vencidos · ⏰ hoy · 🔒 bloqueados · ⏳ sin fecha · 🟢 en fecha) y las filas vencidas primero.
2. **Captura sin espera:** un input de texto en la misma pantalla que **agregue la línea cruda a `Hermes/Agenda/bandeja.md`** (sección "Crudo sin triar"). Sin clasificar, sin respuesta del agente, sin botón de confirmación largo.
3. **Auto-refresh** al abrir la pestaña (leer disco al momento, no caché vieja).

## Restricciones

- No crear proyecto/app nueva; no tocar `Hermes/Config/`.
- Escribir en la bandeja es **append de una línea**: `Hermes/Agenda/bandeja.md` es zona de brain-vps, pero el append crudo está autorizado para esta vista (único escritor autorizado además de brain-vps).
- Sin Ads, sin gasto.

## Criterios de aceptación (verificables)

- [ ] Accesible desde el celular por la URL/tab existente de la PWA (pasame la URL exacta de la pestaña).
- [ ] Carga ≤2 s en 4G con datos reales (no caché): decime cómo lo mediste.
- [ ] Muestra los 3 del día y el conteo por bucket, tomados de `HOY.md`/`Frentes.md` (probadlo cambiando el archivo y refrescando).
- [ ] El input agrega la línea a `Agenda/bandeja.md` y se ve en el archivo (mostrame el diff).
- [ ] Nada de esto depende de que un agente responda: si todos los agentes están apagados, la vista y el input siguen funcionando.

## Si el alcance cambia

Escribí un evento en `events/` (nunca edites este `request.md`).
