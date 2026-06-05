# Sesión Korantis Scout — 2026-06-05

**Contexto:** Ejecución de scout test aislado para Korantis (curated venue discovery product) sobre 10 venues de Buenos Aires.

## Reglas operativas aplicadas

1. **Política de scraping:** Usar `curl` plain como default, `google-chrome --headless` solo si curl retorna <500 bytes.
2. **Política de imágenes soft:** Incluir candidatos con `needs_validation` y `reference_only` para validación posterior.
3. **No inventar datos:** Todo hecho debe tener `source_url`.
4. **No escribir a DBs externas:** Es un scout test aislado.

## Trabajo completado

### 1. Scout Runs
- **Run strict (política dura):** 0 image_candidates utilizables, todos logos/badges en `unsafe_or_rejected_findings`.
- **Run soft (política flexible):** 25 image_candidates (3 hero, 11 needs_validation, 14 reference_only).
- **Batch 01 ejecutado:** 25 BA venues con 56 image candidates, top HERO: Ninina, Verne Club, Milion, Oporto.

### 2. Venues analizadas
**10 venues iniciales:** Crisol Café, Melbourne Café, Anchoita, Apu Nena, Cabaña Las Lilas, Corte Comedor, Julia, Reliquia, Roux, Uptown Bar.

**Métricas clave (soft run):**
- official_websites_found: 5/10
- reservation_links_found: 5/10  
- menu_links_found: 4/10
- price_hints_found: 7/10
- image_candidates_found: 25
- venues_with_possible_interior_images: 6/10

### 3. Top image candidates (vision-verified)
- **Uptown Bar:** 3 GOLDMINE interior shots (NYC subway themed) — hero_candidate
- **Anchoita:** HERO_CANDIDATE (exposed brick, copper bar, wine bottles)
- **Roux:** HERO_CANDIDATE (full dining room, white tablecloths)
- **Corte Comedor:** GALLERY_INTERIOR (owner-uploaded caption, teal/wood palette)

### 4. Transport diagnostic ejecutado
25 tests (5 transports × 5 URLs):
- `curl` works for 80% of cases (Michelin, 50 Best, editorial pages)
- TA + IG blocked (needs curl_cffi/residential proxy)
- `google-chrome` necesita `TMPDIR=/home/hermes/.chrome_tmp` en este VPS

### 5. Archivos generados y movidos a Obsidian

**En `companies/korantis/`:**
- `scraping-outputs/` → JSONs completos de scout runs
- `audit/` → benchmark, auditorías anteriores
- `tmp-files/` → screenshots para referencia
- `scraping-policy.md` → política de scraping 7 puntos
- `run-log-2026-06-05.md` → timeline completo del día

**JSONs principales:**
- `korantis_ba_hermes_soft_scout_batch_01_2026-06-05.json` (177.8 KB, 25 venues)
- `korantis_ba_soft_scout_test_10_2026-06-05.json` (72.8 KB, 10 venues soft)
- `korantis_ba_scout_test_10_2026-06-05.json` (38.2 KB, 10 venues strict)

## Bloqueos encontrados

1. **TripAdvisor rate-limited** → necesita proxy
2. **Uptown sitio down** → `uptownba.com` unreachable
3. **Editorial pages JS-rendered** → Michelin, 50 Best, Airial, Wanderlog
4. **Instagram Meta bloqueo** → solo profile links, no image assets
5. **Google Images thumbnails** → no usar como image candidates

## Decisiones clave

1. **Soft policy adoptada:** Incluir imágenes `needs_validation` en lugar de rechazar todo. Otro pipeline las validará.
2. **Política registrada en Obsidian:** `scraping-policy.md` con flow de decisión y cost matrix.
3. **Korantis como empresa propia:** Ya no vive bajo Wolfim, tiene su carpeta `companies/korantis/`.
4. **TripAdvisor CDN pattern descubierto:** `dynamic-media-cdn.tripadvisor.com/media/photo-o/...` como fuente útil (needs_validation).

## Next Steps sugeridos

1. **Validar derechos** de 11 fotos `needs_validation` (TripAdvisor + MalevaMag)
2. **Facial release** donde hay gente identificable
3. **Reintentar uptownba.com** con detective work
4. **Pedir press kit** a Las Lilas / Julia / Reliquia (caliber Michelin/50 Best)
5. **Instalar curl_cffi** para unblock TA (~2-3 min)

## Links internal
- [[companies/korantis/scraping-policy]]
- [[companies/korantis/run-log-2026-06-05]]
- [[Hermes/MEMORY#Korantis — ahora empresa propia (no proyecto Wolfim)]]

---

**Sesión cerrada:** 2026-06-05 11:12
**Semáforo durante la sesión:** 🟡 (supervivencia)
**Modo operativo:** Ejecución (scout test)
**Próxima acción:** Esperar decisión de Juan sobre opciones (a) reintentar, (b) pedir material oficial, o (c) cerrar.
