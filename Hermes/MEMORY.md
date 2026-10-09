---
owner: brain-vps
last-reviewed: 2026-09-01
confidence: medium
status: active
source: mixed
---

# MEMORY.md — Estado de negocio

**Última actualización:** 2026-10-08 22:25 ART | **Víctor Abrile: USD 100 COBRADOS el 08/10 — honorarios por gestión publicitaria Argenprop + Meta; el costo de pauta lo abonó él por separado (es ingreso propio, NO presupuesto de pauta) → ítem nuevo de octubre** | Farias & Asociados: USD 399 cobrados el 06/10 (informado por Juan el 07/10) — ítem 🥇 del briefing cerrado | **Ingresos sep-2026 registrados por Juan el 24/09 (ver sección Flujo de caja)** · Semáforo: pendiente confirmación formal en kpis.md (vacío desde 25/06) · Cuota token-plan: recuperada el 22-23/09 (crons verificados OK el 24/09); cadena de fallback activa `qwen3.8-flash → deepseek-flash` · Backup Roggero: 100% OK local, offsite Drive roto — migración a R2 aprobada, pendiente bucket + API token · briefing vencido desde 25/06, refresh en curso con prioridades nuevas (cobro Faarias 🥇, Presol/Construvial 🥈, trading 🥉).

---

## Flujo de caja — septiembre 2026 (datos de Juan, 24/09) + octubre

| Concepto | Monto USD | Estado | Fecha |
|---|---|---|---|
| Wolfim — Farias & Asociados (portal web) | 399 | ✅ **Cobrado** (REG-WF-2026-10-06-FARIAS-001) | 06/10/2026 |
| Construvial — Presol semana 1 | 333 | Cobrado | 1ª sem sep-2026 |
| Construvial — Presol semana 2 | 333 | Pendiente de cobro | 2ª sem sep-2026 |
| ANGO (regular mensual) | 333/mes | Cobrado sep | mensual recurrente |
| Víctor Abrile | 266 | Cobrado | sep-2026 |
| Víctor Abrile — honorarios publicidad Argenprop + Meta | 100 | ✅ **Cobrado** | 08/10/2026 |

- **Cobrado oct-2026 (a la fecha): 499 USD** = 399 Farias & Asociados (portal web inmobiliario, acreditado 06/10/2026) + 100 Víctor Abrile (honorarios de gestión publicitaria Argenprop + Meta, cobrado 08/10/2026, informado por Juan). Mantenimiento Farias bonificado oct-2026 → mar-2027; desde abril 2027 USD 29/mes sin permanencia.
- Cobrado sep: 932 USD (333 Presol + 333 ANGO + 266 Víctor). Pendiente sep **al cierre del mes**: 733 USD (333 Presol sem 2 + 400 Farias, todavía sin cobrar al 30/09). **Actualizado al 08/10: ese pendiente queda en 333 USD** — Farias se acreditó el 06/10 por **USD 399** (`REG-WF-2026-10-06-FARIAS-001`; el "400" del briefing v2 era redondeo de la propuesta) y pasó a cobrado de octubre. Único pendiente de septiembre: Presol sem 2.
- Con Farias cobrado, el pendiente propio de Wolfim queda en **cero**: el cuello de botella deja de ser cobrar lo viejo.
- Víctor Abrile: cobrado en USD. **08/10/2026: USD 100 nuevos por honorarios de gestión publicitaria (Argenprop + Meta)** — ítem de octubre, el costo de pauta lo pagó él por separado. Queda abierto: si esos USD 100 son ítem nuevo o forman parte del recibo `REC-WF-2026-08-31-VICTOR-001` (ARS 178.860), que sigue sin acreditación registrada → confirmar con Juan.
- Presol: ampliar en companies/construvial/intelligence/ — empresa del grupo Presol, trabajo semanal recurrente.

---

## Backup Roggero & Roma — estado 2026-09-24

- Cron sábado 10:00 OK; paso 1-4 (Mongo Atlas, Cloudinary 1390, GitHub mirror, tar+sha) sanos. Paso 5 Drive falla por `invalid_grant` (refresh token revocado ~agosto) → **sin offsite**.
- Causa del doble run de los sábados: crontab del sistema Y cron Hermes lanzan `backup.sh` a las 10:00. 5 duplicados (2,8 GB) borrados el 24/09 tras verificar sha256 de los keep; quedan 5 backups = 5,3 GB. Pendiente: desactivar el crontab del sistema (lo edita solo Juan o con aprobación explícita).
- Decisión de Juan: offsite a **Cloudflare R2** via rclone. **✅ IMPLEMENTADO 24/09**: remote `wolfim-r2` → bucket `wolfim-backups`. Paso 5 de backup.sh sube con reintentos+checksum+verificación y **alerta por Telegram si falla**; retención **últimos 3 backups en R2** (free tier 10 GB). Doble programador eliminado (crontab del sistema comentado, con backup). Prueba end-to-end OK: sha local = sha remoto.
- **Farias & Asociados**: carpeta `farias-asociados/` en el mismo bucket. Script `/home/hermes/roggero_backup/scripts/farias_backup.sh` (wrapper en `~/.hermes/scripts/farias-backup-wrapper.sh`) + cron Hermes `farias-backup-R2` sábados 10:00, retención 3. Hoy solo respalda datos (CSV/JSON propiedades, 5 KB); cuando el portal se active, agregar fuente Supabase/repo al script.

---

## Semáforo financiero

- Estado operativo histórico registrado: 🟢 ESCALA — junio cerró con Wolfim $1.000 USD + Ango $333 USD = $1.333 USD.
- Advertencia activa: `Hermes/Intelligence/kpis.md` sigue vencido desde 2026-06-25 y sin números formales de Juan. No se puede confirmar el semáforo real de septiembre.
- Regla prudente mientras no haya update formal: Wolfim prioritaria. Construvial/PRESOL solo como excepción por mandato documentado; no debe desplazar cierres Wolfim.
- Briefing vigente también está vencido; no hay autorización fresca para cambiar prioridades globales.

---

## Wolfim — Web Viejas / Email Outreach

**Estado:** ✅ El cron funciona, pero **la cola sigue agotada**. Última corrida verificada: 2026-09-02 10:02 ART.

### Pipeline
```text
dork_scout → wa_checker → enrich_leads → campaign.py / cron_campaign.py → cron diario
```

### Resultado latest — 2026-09-02
- Ejecutado: `python3 /home/hermes/workspace/scraping/cron_campaign.py`
- Salida real: `✅ Todos los leads han sido enviados. No hay más pendientes.`
- Verificación tracker conocida: 121 leads fuente; 107 registros en tracker, 97 `sent`, 10 `bounced`, 0 `failed`.
- Verificación inventario: 107 cubiertos por `sent`/`bounced`; 19 no componibles por reglas del script; 0 candidatos para próxima tanda.
- Riesgo inmediato: seguir corriendo sin inventario no genera oportunidad comercial nueva.

### Corrida histórica breve
- 09/02: cola agotada; 0 pendientes; cron_campaign.py OK (`Todos los leads han sido enviados`).
- 09/01: cola agotada; 0 pendientes; check-replies 10/14/18: `Sin novedades`.
- 08/31: cola agotada; 107 registros totales, 0 pendientes componibles; sin error visible en stdout.
- 08/30: cola agotada; 107 registros totales, 0 pendientes componibles; sin error visible en stdout.
- 08/29 y anteriores: canal llegó gradualmente a cola agotada; última tanda útil registrada 07/12 con 2 enviados.

### Configuración conocida
- Remitente: `Juan Gomariz <juan@wolfim.com>`; reply-to `juan@wolfim.com` → Cloudflare → `ingjuangomariz@gmail.com`.
- API: Resend (`[credencial: wolfim-outreach]`); logo `assets.wolfim.com/v2.svg`.
- Cron: `wolfim-campaign` diario 10am + `check-replies` lun-vie 10/14/18.
- Documentación: `Hermes/Projects/web-viejas-pipeline.md`.

---

## Pipeline comercial activo

- Franco Roma — Roggero & Roma ✅ cerrado/cobrado. Backup VPS operativo. Publicación/DNS dependen de Juan/NIC.
- Víctor Abrile ✅ histórico cobrado: $450 USD total, **+ USD 100 el 08/10/2026 (honorarios de gestión publicitaria Argenprop + Meta, cobrados; el costo de pauta lo abonó él aparte)**. Además, 2026-08-31 quedó emitido recibo `REC-WF-2026-08-31-VICTOR-001` por ARS 178.860, todavía **sin acreditación registrada** (confirmar con Juan si los USD 100 de octubre lo tocan).
- Luis Farias — Farias & Asociados ✅ **cobrado USD 399** (portal web inmobiliario, acreditado 06/10/2026). Registro `REG-WF-2026-10-06-FARIAS-001`; mantenimiento bonificado hasta mar-2027, luego USD 29/mes.
- Madelen — Suelo Argentino 🔴 analizando propuesta desde 31/08; requiere follow-up si no vuelve.
- GAMA Inmobiliaria ❌ caído: sin respuesta.
- Conforti Propiedades, RIVAS Inmuebles y Ann 🆕 seguimiento pendiente.
- Inventario Wolfim 2026-08-31 para outreach manual inmobiliario: Mar del Plata 49 leads (24 WhatsApp confirmados), Pinamar 34 (18), Villa Gesell 30 (17). Total: 113 leads, 59 WA confirmados.
- Raypac / Leonardo Gastager 🟡 inbox 2026-09-01: cotización kit cámara 360° por USD 14.750 + IVA; requiere decisión de seguimiento.

**Patrón vigente:** Juan construye bien; el cuello de botella sigue siendo cerrar ventas. Si pasan 3+ días sin follow-up a leads, activar anti-parálisis comercial.

---

## Empresas

- Wolfim: foco principal mientras KPIs formales sigan vencidos. Web Viejas sin inventario; prioridad real es seguimiento/cierre.
- Ango: junio $333 cobrados. MONTECOR pagar importación sigue pendiente. Handoffs locales de landing/medición/Ads siguen sin cierre visible.
- Construvial: PRESOL pasó a **campaña activa** 2026-09-01: Juan tiene campaña de campo 2 semanas (auto + viáticos + fijo) para logística/cargas pesadas en corredores Río Tercero→Río Cuarto/Villa María/Córdoba. Paquete creado: plan, oferta, ficha, WhatsApp, planilla, paquete dirección/campo ampliado a 117 empresas (44 clase A, 73 teléfonos OK) + PDF final 35 páginas. Falta registrar monto/condición de pago y cerrar tarifa base/km, mínima, hora hidrogrúa, responsable WhatsApp y alcance áridos/volcador.
- Korantis: sin revenue; modo evidencia + scout. No desplazar a Wolfim.
- Almas Libres: profile activo; `HO-2026-08-03-001` pide MVP institucional + padrinazgo equino en preview, sin publicación hasta validar datos y activos.

---

## Handoffs / coordinación

- `local-to-vps`: `HO-2026-06-26-001` acknowledged; administrativamente archivable. `HO-2026-10-08-001` (ingreso Víctor USD 100) **ackado y aplicado** el 08/10 — asiento en Flujo de caja + briefing + Agenda 2026-10-08.
- `vps-to-local`: **10 en `status: ready`, todos con `due-at` vencido** (el más viejo 25/06). Triage propuesto a Juan: archivar `HO-2026-06-25-001` (test de circuito) y `HO-2026-06-27-001` (aviso Agenda V2); decidir si los 4 ANGO de julio siguen vivos; `HO-2026-08-03-002` (Wolfim Motors, high) es el único con valor comercial claro. Detalle en `Hermes/Agenda/2026-10-08.md`.
- `vps-to-local` activos/vencidos principales: `HO-2026-08-03-002` Wolfim Motors Demo (high); `HO-2026-08-03-001` Almas Libres MVP; `HO-2026-07-13-001` Sync V6 profiles locales; `HO-2026-07-16-001`, `HO-2026-07-22-001`, `HO-2026-07-24-001`, `HO-2026-07-27-001` ANGO.
- `Memory/pending`: `2026-07-12-sync-v6-architecture-update.md` y `2026-07-24-jobseeker-profile.md` esperan consolidación / decisión de Juan.

---

## Correcciones aprendidas vigentes

- Leads en pausa: verificar inventario real al inicio; el vault puede quedar más optimista que la cola real.
- Mockups AI no reemplazan venta concreta. Mostrar producto > mostrar idea.
- Datos de pago: Juan los pasa al cliente, no al revés.
- Recibos Wolfim: usar diseño fijo existente; no improvisar layouts nuevos ni variantes genéricas.
- No escribir secrets, tokens ni API keys en el vault.
