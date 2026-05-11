# Plan Construvial — 3 fases

**Última actualización:** 2026-05-11
**Estado:** Fase 0 completa (investigación inicial)

---

## Posicionamiento
Proveer **maquinaria + obra civil** a empresas que YA son subcontratistas de petroleras/mineras.
No apuntar directo a YPF/Veladero — la cadena es:
```
Minera/Petrolera → Proveedor directo → Subcontratista = CONSTRUVIAL
```

---

## Fase 1 — Investigación de mercado

**Objetivo:** 50 empresas con DB completa

### a) Mapear subcontratistas Oil & Gas — Neuquén/Vaca Muerta
- [ ] Empresas que já fazem servicios para YPF/Shell/Total en la zona
- [ ] Empresas de transporte pesado y logistica para Vaca Muerta
- [ ] Empresas de montaje y civil para la industria

### b) Mapear subcontratistas Mining — San Juan/Catamarca
- [ ] Empresas de servicios para Veladero/Bering/Andina
- [ ] Empresas de transporte y logistica minera
- [ ] Empresas de construcción civil para mining

### c) Análisis de licitaciones
- [ ] Buscar licitaciones públicas recientes que involucren estas empresas
- [ ] Identificar qué están construyendo ahora

**Tools:** Serper + Firecrawl + Scrapling
**Deadline:** 2026-05-18

---

## Fase 2 — DB construida

**Objetivo:** DB con 50 empresas mínimo

### Campos por empresa:
- Nombre
- Zona (Neuquén / San Juan / Catamarca)
- Vertical (Oil & Gas / Mining)
- Qué provee actualmente
- Empresa cliente actual (si se sabe)
- Teléfono
- Email
- web
- Estado: fria / tibia / caliente

### Clasificación:
- 🔥 Caliente: empresa en operación activa, necesita lo que Construvial ofrece
- 🟡 Tibia: empresa que podría necesitar
- ❄️ Fría: solo informativa

**Deadline:** 2026-05-25

---

## Fase 3 — Análisis competitivo

**Objetivo:** Identificar ventajas y gaps

### Temas a investigar:
- [ ] Who else alquila carretones con grúa en Neuquén/San Juan/Catamarca?
- [ ] Qué precios manejan?
- [ ] Qué tiene Construvial que la competencia no?

### Deliverable:
- Matriz de competencia
- Matriz de oportunidades

**Deadline:** 2026-06-01

---

## Lead inicial DB (Fase 0 — mayo 2026)

**Archivo:** `leads_oil_gas_mining.csv`
**Total:** 21 empresas descubiertas

| Empresa | Ciudad | Vertical | Teléfono | Email |
|---|---|---|---|---|
| CISA | Neuquén | Oil & Gas | +54 299 468-1434 | mortiz@ci-sa.com.ar |
| Sigma SA | San Juan | Mining | +54 264 430-7000 | mailsigma@sigmasa.com |
| Dumandzic | San Juan/Catamarca | Mining | +54 264 469-5935 | info@dumandzic.com |
| CASEMICA | Catamarca | Mining | +54 446 497-2574 | minera_petrea@live.com.ar |
| Altamore | Neuquén | Oil & Gas | - | - |
| SACDE | Neuquén | Oil & Gas | - | - |
| Ops SRL | Neuquén | Oil & Gas | - | - |
| Velitec | Neuquén | Oil & Gas | - | iortega@velitec.com.ar |
| Green Oil | Neuquén | Oil & Gas | - | info@greenoilservices.com |
| Alas Ingeniería | San Juan | Mining | - | info@alas-ingenieria.com.ar |
| RAM | San Juan | Mining | (sin tel) | info@ramobrasyservicios.com.ar |
| Global Minera | Catamarca | Mining | - | - |
| Julio Nacusi | San Juan | Mining | (sin tel) | recepción@ingjulionacusi.com.ar |

---

## Reglas de operación
- Solo investigación — sin outreach hasta que Juan lo active explícitamente
- Sin credenciales de API inventadas — usar solo keys confirmadas
- Datos guardados en vault + CSV en workspace