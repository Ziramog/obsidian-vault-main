---
owner: brain-vps
type: bandeja-de-entrada
rule: acá NO se interpreta. Se guarda crudo y se triagea después.
updated-at: 2026-10-09T07:45:00-03:00
---

# bandeja.md — captura cruda

**Para qué sirve:** es el lápiz y papel del sistema. Tirás acá lo que se te cruce — texto o audio transcripto, crudo, mal escrito, sin orden — y **te vas sin esperar respuesta**. Nadie te va a pedir que lo clasifiques.

**Qué pasa después:** brain-vps lo lee y lo convierte en frente con **dueño y fecha** en `Frentes.md`, o te devuelve **una pregunta** si no se entiende. Nunca se descarta en silencio.

**Reglas:**
- No se borra nada de acá: lo triado se mueve a la sección "Triado", con su id.
- Si algo quedó ilegible o cortado, se marca `❓` y se pregunta — no se adivina.
- Esto **no** es la lista del día. La lista del día se lee en `HOY.md` (2 segundos, sin chat).

---

## Crudo sin triar

- *(nada pendiente)*

---

## Triado

### 2026-10-09 — entraron por el bot de Telegram

| id | Texto crudo tal como llegó | Resultado |
|---|---|---|
| ag-20261009-001 | "Cotizacion para Palmero Ango cerrar el lunes" | → frente **ANGO — cotización Palmero**, due 2026-10-12 |
| ag-20261009-002 | "victor publicidad comenzar argenprop y meta martes que viene" | → frente **Wolfim — publicidad Víctor**, due 2026-10-13 |
| ag-20261009-003 | "agenda" | ❓ falta contexto (¿revisarla, arreglarla, mostrarla?) |
| ag-20261009-004 | "listar comandos" | ✅ respondido: lista de comandos enviada en el chat |
| ag-20261009-005 | "semana que viene" | ❓ audio cortado: ¿qué cosa es para la semana que viene? |

> ⚠️ De estos 5, **3 no son tareas** ("listar comandos" era una consulta y cayó como tarea nueva). Es la falla concreta del bot: no debe perder ni mal-clasificar lo que decís → frente **S4**.
