# Google Cloud — Control de Consumo de APIs

> Documento creado: 2026-07-01
> Motivo: Korantis consumió ~$150 USD en Places API (New) por bug en búsqueda de venues
> Objetivo: que TODOS los proyectos se mantengan dentro de la cuota gratis ($0/mes)

---

## 1. Situación actual

### Cuenta de Google Cloud
- **Email:** [credencial: GOOGLE_CLOUD_EMAIL]
- **Projects existentes:**

| Project ID | Contenido | Estado |
|---|---|---|
| Korantis | Places API (New) — búsqueda de venues | ✅ Separado |
| La Montaña | [a documentar] | ✅ Separado |
| **Project grupal** | Roggero & Roma + otros sitios con Maps JavaScript API | ⚠️ Comparten cuota |

### Incidente: Korantis $150 USD
- **Fecha:** [a documentar]
- **Causa:** Bug en pipeline de búsqueda de venues → loop infinito de requests a Places API (New)
- **Consumo:** ~$150 USD (estimado ~8,800+ requests extras sobre la cuota gratis)
- **Lección:** Sin quotas duras ni budget alerts, un bug puede consumir presupuesto ilimitado

---

## 2. Nuevo modelo de pricing (desde Marzo 2025)

Google cambió de un crédito universal de $200/mes a **cuotas gratis por SKU** (por tipo de API).

### Cuota gratis por API (categoría Essentials)

| API | Gratis/mes | Costo después de gratis | Costo unitario |
|---|---|---|---|
| Maps JavaScript API | 10,000 loads | $7 USD / 1,000 loads | $0.007/load |
| Places API (New) | 10,000 requests | $17 USD / 1,000 requests | $0.017/request |
| Geocoding API | 10,000 requests | $5 USD / 1,000 requests | $0.005/request |
| Directions API | 10,000 requests | $5 USD / 1,000 requests | $0.005/request |
| Routes API | 10,000 elements | $5 USD / 1,000 elements | $0.005/element |

### Regla clave
> **Las 10,000 requests se comparten entre TODAS las apps/sitios que usen esa API dentro del MISMO Project de Google Cloud.**

Si Roggero & Roma y otros sitios están en el mismo Project, comparten las 10,000 de Maps JavaScript API.

### Diferencia con el modelo viejo

| | Viejo (antes de Marzo 2025) | Nuevo (actual) |
|---|---|---|
| Crédito | $200 USD universales | 10,000 requests por SKU |
| Compartido | Todas las APIs del proyecto | Cada API tiene su propia cuota |
| Exceso | Se factura del crédito común | Se factura por SKU |

---

## 3. Arquitectura recomendada

### Regla: un Project de Google Cloud por producto/sitio importante

```
tu-email@gmail.com (Google Cloud Account)
│
├── Project: korantis-prod
│   └── Places API (New) → 10,000 requests/mes propias
│
├── Project: la-montaña
│   └── [sus APIs] → 10,000 requests/mes propias
│
├── Project: roggero-y-roma-prod        ← NUEVO (aislar del grupo)
│   └── Maps JavaScript API → 10,000 loads/mes propios
│
├── Project: wolfim-sites-grupo
│   ├── Sitio A → comparten 10,000 de Maps JS
│   └── Sitio B → comparten 10,000 de Maps JS
│
└── [otros proyectos]
```

### ¿Por qué separar?
- Un bug en un sitio NO afecta a los demás
- Cuotas independientes = 10,000 por cada uno
- Budget alerts por separado
- Visibilidad clara de qué consume qué

---

## 4. Plan de protección — 3 capas

### Capa 1: Quotas duras (BLOQUEO — lo más importante)

En cada Project de Google Cloud:

1. Ir a **APIs & Services → Enabled APIs**
2. Seleccionar la API (ej: Places API New)
3. Ir a **Quotas**
4. Establecer límite diario:

| Cuota mensual gratis | Límite diario seguro | Margen |
|---|---|---|
| 10,000/mes | **300/día** | 9,000/mes (10% margen) |
| 10,000/mes | **330/día** | 9,900/mes (1% margen) |

> **Recomendado: 300/día** para tener margen de seguridad.

5. Si se supera → Google corta la API automáticamente → **$0 de factura**

### Capa 2: Budget Alerts (ALERTA TEMPRANA)

En cada Project:

1. Ir a **Billing → Budgets & Alerts**
2. Crear budget:
   - **Nombre:** `[proyecto]-api-safety`
   - **Monto:** $1 USD
   - **Alertas:** 50% ($0.50) y 100% ($1.00)
   - **Notificación:** Email + (opcional) Slack/Pub/Sub
3. Recibir alerta ANTES de que escale

### Capa 3: Protección en código (PREVENCIÓN)

Para cada app que use APIs de Google Maps:

#### a) Cache de resultados
```javascript
// Ejemplo: Places API con cache
const placeCache = new Map();

async function searchVenues(query) {
  const cacheKey = `places:${query.toLowerCase().trim()}`;
  
  if (placeCache.has(cacheKey)) {
    return placeCache.get(cacheKey); // ← 0 requests a la API
  }
  
  const result = await placesApi.search(query);
  placeCache.set(cacheKey, result);
  return result;
}
```

#### b) Rate limiting
```javascript
// Máximo 10 requests por minuto
const rateLimiter = {
  tokens: 10,
  lastRefill: Date.now(),
  
  canMakeRequest() {
    const now = Date.now();
    const elapsed = now - this.lastRefill;
    this.tokens = Math.min(10, this.tokens + elapsed / 6000);
    this.lastRefill = now;
    
    if (this.tokens >= 1) {
      this.tokens -= 1;
      return true;
    }
    return false;
  }
};
```

#### c) Circuit breaker
```javascript
// Cortar si hay 5 errores seguidos
const circuitBreaker = {
  failures: 0,
  threshold: 5,
  isOpen: false,
  resetTimeout: 60000, // 1 minuto
  
  recordFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.isOpen = true;
      console.error('🔴 Circuit breaker ABIERTO — API cortada');
      setTimeout(() => {
        this.isOpen = false;
        this.failures = 0;
      }, this.resetTimeout);
    }
  },
  
  canProceed() {
    return !this.isOpen;
  }
};
```

#### d) Contador de requests (logging)
```javascript
// Log de cada request con costo estimado
function logApiCall(apiName, costEstimate) {
  const today = new Date().toISOString().split('T')[0];
  const log = `[${today}] ${apiName}: $${costEstimate.toFixed(4)}`;
  console.log(log);
  // Opcional: enviar a Telegram si se acerca al límite
}
```

---

## 5. Checklist para aislar un proyecto

### Template: aislar [SITIO] del Project grupal

- [ ] **1. Crear Project nuevo en Google Cloud**
  - Console → Select a project → NEW PROJECT
  - Nombre: `[sitio]-prod`
  - Billing: asociar la misma cuenta de facturación
  - NO necesitás otra email

- [ ] **2. Habilitar APIs necesarias**
  - APIs & Services → Enable APIs
  - Habilitar solo las APIs que el sitio necesita
  - Ejemplo: Maps JavaScript API, Places API (New), Geocoding API

- [ ] **3. Crear API Key nueva**
  - APIs & Services → Credentials → Create Credentials → API Key
  - **Restringir por HTTP Referrer** (dominios del sitio):
    - `roggeroyroma.com/*`
    - `www.roggeroyroma.com/*`
    - `localhost:3000/*` (desarrollo)
  - **Restringir por API** (solo las APIs habilitadas en este Project)

- [ ] **4. Configurar Quotas**
  - Para cada API habilitada → Quotas
  - Límite diario: 300 requests/día
  - Verificar que "Quota exceeded" = error 429 (no factura)

- [ ] **5. Crear Budget Alert**
  - Billing → Budgets & Alerts
  - Nombre: `[sitio]-api-safety`
  - Monto: $1 USD
  - Alertas: 50% y 100%

- [ ] **6. Actualizar la key en el sitio**
  - Reemplazar API key vieja por la nueva en `.env` / config
  - Testear que el mapa/API funciona con la key nueva
  - Deploy

- [ ] **7. En el Project grupal viejo**
  - Si nadie más usa esa key → eliminarla
  - Si otros sitios la usan → dejarla, pero el sitio migrado ya usa la suya

- [ ] **8. Verificar**
  - Abrir el sitio → mapa carga correctamente
  - En Google Cloud → ver que las requests aparecen en el Project nuevo
  - En el Project viejo → las requests del sitio migrado ya no aparecen

---

## 6. Monitoreo continuo

### Dashboard de Google Cloud
- **APIs & Services → Dashboard** → ver requests por API por día
- **Billing → Reports** → ver costo por SKU por día

### Cron de verificación (opcional)
Se puede crear un cron en Hermes que revise el consumo:
- Consultar Google Cloud Monitoring API
- Si requests del día > 250 → alerta Telegram
- Si requests del mes > 8,000 → alerta Telegram urgente

### Métricas a trackear

| Métrica | Alerta amarilla | Alerta roja |
|---|---|---|
| Requests/día | > 250 | > 300 (quota corta) |
| Requests/mes | > 8,000 | > 9,500 |
| Costo estimado | > $0.50 | > $1.00 |
| Errores 429 (quota exceeded) | > 0 | > 10/día |

---

## 7. Proyectos afectados — acciones pendientes

### Korantis
- [x] Separado en su propio Project
- [ ] Verificar quotas configuradas (Places API New: 300/día)
- [ ] Budget alert de $1 USD
- [ ] Código: verificar cache y rate limiting en pipeline de venues

### Roggero & Roma
- [ ] Crear Project `roggero-y-roma-prod`
- [ ] Habilitar Maps JavaScript API
- [ ] Crear API key restringida a roggeroyroma.com
- [ ] Quota: 300 loads/día
- [ ] Budget alert: $1 USD
- [ ] Actualizar key en el código
- [ ] Testear sitio
- [ ] Eliminar key vieja del Project grupal

### La Montaña
- [ ] Documentar qué APIs usa
- [ ] Verificar quotas configuradas
- [ ] Budget alert: $1 USD

### Otros sitios en Project grupal
- [ ] Listar todos los sitios
- [ ] Evaluar cuáles necesitan aislamiento
- [ ] Priorizar por volumen de tráfico

---

## 8. Referencias

- [Google Maps Platform Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- [Google Cloud Budgets & Alerts](https://cloud.google.com/billing/docs/how-to/budgets)
- [Google Cloud Quotas](https://cloud.google.com/docs/quotas)
- [Google Maps API Security Best Practices](https://developers.google.com/maps/api-security-best-practices)
- [New billing model March 2025](https://www.storelocatorwidgets.com/blogpost/20499/New_Google_Maps_API_free_credit_system_from_March_1st_2025)

---

## 9. Notas

- **NO necesitás otra cuenta de email** para crear Projects nuevos. Todo se hace desde la misma cuenta Google Cloud.
- **Cada Project tiene 10,000 requests gratis por API.** Separar = multiplicar la cuota gratis.
- **Las quotas duras son la protección #1.** Budget alerts son el backup. El código es la prevención.
- **Migrar de a un proyecto.** Si algo falla, es fácil rollback.
- **Las API keys viejas no se borran solas.** Hay que eliminarlas manualmente del Project viejo.
