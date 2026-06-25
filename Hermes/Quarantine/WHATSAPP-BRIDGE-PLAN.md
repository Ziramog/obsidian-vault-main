# WhatsApp Bridge — VPS Baneado → Sistema Funcional

## Situación

Baileys en VPS → inestable / no conecta / mensajes no salen

> **Causa real:** IP de datacenter + patrón bot → sesión marcada. No es "IP baneada pura", es entorno + comportamiento.

---

## Plan en 4 Fases

### Fase 1 — Recuperar Sesión (rápido)

```bash
rm -rf auth_info_baileys/
```

En el teléfono: cerrar dispositivos vinculados.

Esperar: 30–60 min. Reconectar con QR nuevo.

> Si en VPS sigue fallando → pasar a fase 2.

---

### Fase 2 — Mover el Sender Fuera del VPS (clave)

**Opción C (recomendada):** Bridge VPS → PC

```
Hermes (VPS)
  → API
Notebook (tu casa)
  → Baileys
  → envía WA
```

**Resultado:** IP residencial → baja riesgo → sistema vuelve a funcionar.

**Requisitos:**
- Notebook siempre prendida
- Proceso con pm2
- Conexión con Tailscale

---

### Fase 3 — Hacerlo Estable (evitar manual)

Implementar sí o sí:

| Mecanismo | Detalle |
|---|---|
| Cola + estados | `pending → sending → sent → failed` |
| Retries | máx 2–3 |
| Delay humano | 10–25s entre mensajes |
| Guardar `message_id` | tracking real |
| Logs en DB | saber qué pasó |

> Así dejás de intervenir manualmente.

---

### Fase 4 — Escalar Sin Romper

Ruta recomendada:

| Prioridad | Opción | Cuándo |
|---|---|---|
| Ahora | Bridge (notebook) | Recover rápido |
| Después | Proxy mobile | 24/7 estable |
| Ingresos | API oficial (YCloud) | Cuando haya cash |

---

## Canales — No Depender Solo de WA

```
scraping
  → Hermes decide canal:
      ├── WA (testing)
      ├── form web (muy efectivo)
      └── email (backup)
```

---

## Loop Final

```
SCRAPE → DB → OUTREACH → RESULT → HERMES → OBSIDIAN → OPTIMIZE → repeat
```

---

## Errores Que Rompían

- ❌ Enviar directo sin estados
- ❌ Sin retries
- ❌ VPS como sender WA
- ❌ No saber si el mensaje salió

---

## Conclusión

- ✅ El VPS no es lugar para WhatsApp
- ✅ Separar "cerebro" (Hermes) de "sender" (WA)
- ✅ Notebook = solución práctica ahora
- ✅ Después migrás a algo más automático

---

## Próximo Paso

**Implementar:**
```
Hermes queue → API → notebook → Baileys sender
```

Con eso:
- Dejás el envío manual
- Recuperás control
- Podés escalar sin romper todo

---

## Estados del Bridge

| Componente | Status | Notas |
|---|---|---|
| VPS Hermes | ✅ | Cerebro |
| Bridge API | ⏳ | Pendiente implementar |
| Notebook Baileys | ⏳ | Pendiente configurar |
| YCloud (backup) | ✅ | Sender alternativo |
