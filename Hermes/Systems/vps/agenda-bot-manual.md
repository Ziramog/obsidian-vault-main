---
type: manual
product: Agenda Telegram Bot
owner: brain-vps
updated-at: 2026-06-27T19:35:00-03:00
status: active
---

# Manual de uso — Bot Agenda

Bot: `@Agenda_Hbot`

Objetivo: capturar, consultar y mantener la agenda diaria de Juan desde Telegram usando como fuente única de verdad los archivos:

```txt
Hermes/Agenda/YYYY-MM-DD.md
```

---

## 1. Regla de uso

Escribí como hablarías normalmente.

Ejemplos válidos:

```txt
mañana 9 llamar a GAMA
miércoles que viene 14 pasar a ver ANGO
fin de mes pagar monotributo
recordámelo a las 10 pagar monotributo
mañana: llamar a GAMA, ver ANGO, pasar presupuesto
/agendar rojo mañana 9 llamar a GAMA
```

---

## 2. Qué entiende el bot

### Fechas

- `hoy`
- `mañana`
- `pasado mañana`
- `en 3 días`
- `lunes`, `martes`, `viernes`, etc.
- `martes o miércoles`
- `miércoles que viene`
- `el otro miércoles`
- `la semana que viene`
- `fin de mes`
- `primer lunes de julio`
- `mie 26`
- `26/7`
- `vie 4 de julio`

### Horas / reminders

- `9`
- `9:30`
- `recordámelo a las 10 ...`
- `después de las 15`
- `a la tarde`
- `después de comer`
- `antes de las 12`

### Listas múltiples

```txt
mañana: llamar a GAMA, ver ANGO, pasar presupuesto
```

```txt
mañana
- llamar a GAMA
- ver ANGO
- pasar presupuesto
```

```txt
mañana llamar a GAMA y después ver ANGO y también pasar presupuesto
```

### Prioridad explícita

- `rojo`, `roja`, `red`, `alta`
- `amarillo`, `amarilla`, `yellow`, `importante`
- `verde`, `green`, `backlog`, `baja`

Ejemplo:

```txt
/agendar rojo mañana 9 llamar a GAMA
/agendar verde cuando pueda probar idea
```

---

## 3. Lista de comandos

## Consulta rápida

### `/hoy`
Muestra agenda de hoy.

### `/mañana`
Muestra agenda de mañana.

### `/esta-semana`
Resumen simple de próximos 7 días.

### `/pendientes`
Vista plana de todas las tareas abiertas desde hoy hacia adelante.

### `/revisar`
Muestra próximos recordatorios activos.

### `/foco`
Devuelve la primera tarea abierta prioritaria del día.

### `/detalle ag-YYYYMMDD-NNN`
Muestra metadatos completos de una tarea.

Ejemplo:

```txt
/detalle ag-20260628-001
```

Respuesta esperada:
- título
- detalle
- sección
- estado
- reminder
- canal
- source

---

## Alta de tareas

### Texto natural

```txt
mañana 9 llamar a GAMA
```

### `/agendar ...`
Alta explícita con o sin prioridad.

```txt
/agendar rojo mañana 9 llamar a GAMA
/agendar amarillo viernes 11 pasar presupuesto
/agendar verde cuando pueda probar idea
```

---

## Mantenimiento de tareas

### `/hecho ag-YYYYMMDD-NNN`
Marca tarea como hecha.

### `/cancelar ag-YYYYMMDD-NNN`
Marca tarea como cancelada.

### `/editar ag-YYYYMMDD-NNN nuevo texto`
Cambia el título de la tarea sin recrearla.

Ejemplo:

```txt
/editar ag-20260628-001 llamar a GAMA por presupuesto y WhatsApp
```

### `/posponer ag-YYYYMMDD-NNN 11:00`
Mueve reminder dentro del mismo día.

### `/mover ag-YYYYMMDD-NNN mañana 11:00`
Mueve tarea a otra fecha y opcionalmente cambia hora.

Ejemplos:

```txt
/mover ag-20260628-002 fin de mes 15:00
/mover ag-20260628-002 miércoles que viene
```

### `/prioridad ag-YYYYMMDD-NNN rojo|amarillo|verde`
Reubica tarea en la sección correspondiente.

Ejemplo:

```txt
/prioridad ag-20260628-001 rojo
```

### `/limpiar`
Limpia el archivo del día actual removiendo tareas canceladas o ya cerradas de las secciones activas.

Uso recomendado:
- al final del día
- después de una tanda grande de cierres/cancelaciones

---

## 4. Reglas operativas

### Deduplicación
Si mandás dos veces la misma tarea abierta para el mismo día, la segunda no se crea.

Respuesta típica:

```txt
SKIP duplicate: Tarea duplicada: ag-20260628-001 — llamar a GAMA
```

### Fuente única de verdad
Todo termina escrito en:

```txt
Hermes/Agenda/YYYY-MM-DD.md
```

No hay base de datos separada.

### Botón Start
Si el bot parece no responder, primero verificar que el chat con `@Agenda_Hbot` esté abierto y que ya se haya hecho `/start`.

---

## 5. Flujo diario recomendado

## Mañana

1. Abrir Telegram
2. Ejecutar:

```txt
/hoy
/pendientes
/foco
```

3. Agregar tareas nuevas del día:

```txt
mañana 9 llamar a GAMA
hoy 14 enviar presupuesto
```

## Durante el día

- marcar hechos:

```txt
/hecho ag-...
```

- mover o posponer:

```txt
/posponer ag-... 16:00
/mover ag-... mañana 10:00
```

- editar texto si cambia el contexto:

```txt
/editar ag-... llamar a GAMA por presupuesto y cobranzas
```

## Cierre del día

1. Revisar abiertos:

```txt
/hoy
/revisar
```

2. Limpiar ruido:

```txt
/limpiar
```

---

## 6. Casos recomendados de escritura

### Mejor forma

```txt
mañana 9 llamar a GAMA
fin de mes pagar monotributo
miércoles que viene 14 pasar a ver ANGO
```

### Para varias juntas

```txt
mañana: llamar a GAMA, ver ANGO, pasar presupuesto
```

### Para prioridad explícita

```txt
/agendar rojo mañana 9 llamar a GAMA
```

### Para backlog

```txt
/agendar verde cuando pueda probar idea
```

---

## 7. Límites actuales

Todavía no hace automatización condicional real tipo:

```txt
si no responde mañana avisame pasado
```

Eso hoy se aproxima como follow-up simple, no como motor de reglas.

---

## 8. Resumen corto de comandos

```txt
/hoy
/mañana
/esta-semana
/pendientes
/revisar
/foco
/detalle ag-YYYYMMDD-NNN
/agendar rojo|amarillo|verde ...
/hecho ag-YYYYMMDD-NNN
/cancelar ag-YYYYMMDD-NNN
/editar ag-YYYYMMDD-NNN nuevo texto
/posponer ag-YYYYMMDD-NNN 11:00
/mover ag-YYYYMMDD-NNN mañana 11:00
/prioridad ag-YYYYMMDD-NNN rojo|amarillo|verde
/limpiar
```

---

## 9. Archivo del manual

Este manual vive en:

```txt
Hermes/Systems/vps/agenda-bot-manual.md
```
