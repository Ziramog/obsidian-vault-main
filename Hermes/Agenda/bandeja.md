---
owner: brain-vps
type: bandeja-de-entrada
rule: acá NO se interpreta. Se guarda crudo y se triagea después.
append-protocol: append-only al final del archivo, una línea por captura
line-format: "- YYYY-MM-DDTHH:MM-03:00 · [origen] · texto crudo (una sola línea)"
updated-at: 2026-10-09T08:20:00-03:00
---

# bandeja.md — captura cruda

**Para qué sirve:** es el lápiz y papel del sistema. Juan tira acá lo que se le cruce — texto o audio transcripto, crudo, mal escrito, sin orden — y **se va sin esperar respuesta**. Nadie le pide que lo clasifique.

**Qué pasa después:** brain-vps lo lee y lo convierte en frente con **dueño y fecha** en `Frentes.md`, o devuelve **una pregunta** si no se entiende. Nunca se descarta en silencio.

## Protocolo de escritura (para la pestaña "HOY" de la PWA)

1. **Destino único:** este archivo. Nada de colas `agenda_*.md` ni endpoints con estado propio.
2. **Append al final del archivo**, una línea por captura. La sección `## Crudo sin triar` está **al final** justo para eso: agregar una línea al EOF alcanza — no hay que parsear ni reescribir nada.
3. **Formato de línea:**
   `- 2026-10-09T08:12-03:00 · [pwa] · texto crudo tal cual`
   - Fecha/hora ART con offset `-03:00`.
   - `[origen]` = `pwa`, `bot`, `voz` o `chat`.
   - **Una sola línea:** si el texto trae saltos de línea, se reemplazan por ` / `.
   - Máximo 2.000 caracteres; si es más, se corta y se agrega `…(cortado)`.
4. **Nunca editar ni borrar** lo ya escrito (append-only). brain-vps mueve lo triado a *Triado*.
5. **Sin secretos:** este archivo es del vault. No escribir tokens, claves ni contraseñas; si aparece uno, se marca y se avisa.
6. Sin señal: se guarda local y se vuelca al reconectar — pero el destino sigue siendo **este archivo**, no un almacenamiento paralelo.
7. La escritura **no depende de ningún agente**: si todos los agentes están apagados, la captura igual entra.

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

> ⚠️ De estos 5, **3 no son tareas** ("listar comandos" era una consulta y cayó como tarea nueva). Es la falla concreta del bot: no debe perder ni mal-clasificar lo que Juan dice → frente **S4**.

---

## Crudo sin triar

<!-- APPEND ACÁ: una línea por captura, al final de este archivo. -->
