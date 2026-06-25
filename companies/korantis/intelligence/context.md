---
company: Korantis
owner: korantis-ops
status: early-validation
version: 1
last-reviewed: 2026-06-25
---

# Context — Korantis

> **Propósito:** Información que no cambia con cada campaña. Lo que cualquier profile nuevo necesita saber antes de actuar.

## Identidad

- **Qué hace:** Producto de venue discovery curado para Buenos Aires. La hipótesis: hay un gap entre listings genéricos (Google Maps, Yelp) y guías editoriales premium (Michelin, 50 Best). Korantis ocupa el medio: descubrimiento con curación, pero con la profundidad visual y contextual del editorial.
- **A quién sirve:** Usuarios que buscan venues con calidad editorial pero sin el elitismo de las guías tradicionales. Mercado: Buenos Aires como primer mercado de validación.
- **Propuesta de valor:** Venues seleccionados manualmente con evidencia visual verificada. No es un directorio genérico. Cada venue tiene fotos reales, contexto y datos curados.
- **URL:** korantis.com (dominio registrado, NO deployed aún)
- **Fundador:** Juan Gomariz (único dueño, proyecto propio)
- **Fase:** Early validation — recolección de evidencia, sin producto publicado, sin clientes, sin revenue.

## Tono

- **Voz de marca:** Startup/producto, editorial con profundidad. No genérico como Maps. No pretencioso como Michelin. Descubrimiento auténtico.
- **Lo que SÍ decimos:** "Encontramos esto." Curaduría humana con respaldo visual. Datos verificables (source_url obligatorio).
- **Lo que NO decimos:** "Los mejores." Rankings subjetivos sin criterios claros. Reseñas sin evidencia.

## Restricciones

- **No hacer:** NO crear ni modificar jobs de scraping sin aprobación explícita de Juan. NO gastar créditos de API sin presupuesto aprobado. NO publicar el producto sin autorización.
- **No prometer:** Fechas de lanzamiento. Cobertura geográfica más allá de Buenos Aires.
- **Límites de presupuesto:** Sin presupuesto activo. Solo ejecución de jobs previamente aprobados. Transport por defecto: curl simple (no Playwright/Chrome). Escalar a headless Chrome solo si curl falla (política documentada en scraping-policy.md).

## Contactos

| Nombre | Rol | Canal | Notas |
|---|---|---|---|
| Juan Gomariz | Fundador, único dueño | [pendiente - Juan completa] | Decisiones de producto, presupuesto, validación. |

## Estado Actual

- **Semáforo:** Modo evidencia — solo jobs aprobados, sin revenue.
- **Ingresos mensuales:** $0 (no monetizado).
- **Pipeline:** Sin pipeline comercial.
- **Último hito:** Soft Scout Batch 01 completado (2026-06-05): 25 venues de Buenos Aires con evidencia web + visual. 56 image candidates identificados. 8 HERO candidates verificados (Ninina, Verne Club, Milion, Oporto, Gran Bar Danzon, Don Julio, Niño Gordo, Uptown).
- **Próximo paso:** [pendiente - Juan completa] Instalar curl_cffi para desbloquear TripAdvisor, re-run de 3 venues bloqueados, validar 42 imágenes pendientes.
