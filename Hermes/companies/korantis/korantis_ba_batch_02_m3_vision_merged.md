# KORANTIS — M3 VISION MERGED REPORT (run02)

**Run ID:** korantis_ba_batch_02_m3_vision_merged_run02
**Parent run:** korantis_ba_batch_02_final_vision_queue_2026-06-06
**Model:** MiniMax-M3 (vision, base64 inline)
**Merge strategy:** structural concat, no re-inference
**Built at:** 2026-06-06T21:53:29+00:00
**Items in scope:** 52

## TL;DR

- **52 items en scope (post-sanitizer) · 30 M3-verified · 22 skipped at dimension gate (<512px).**
- **8 venues unicos** · **0 duplicados** por dedupe_hash / resolved_image_url / sha256.
- **22 items below_preferred_resolution** (max_dim entre 512 y 1023): usables para screening, no para hero/card sin revision.
- **7 venues con candidatos visuales** (al menos 1 M3-verified no rechazado).
- **1 venues sin candidato visual usable** (El Preferido de Palermo).
- **Cero imagenes aprobadas para publicacion.** validation_status universal: `imported_needs_validation`.

## Source chunks

| chunk | run_id | items | ok | skipped | below<1024 | started | finished |
|---|---|---|---|---|---|---|---|
| 1 | korantis_ba_batch_02_m3_vision_chunk_01_run02 | 25 | 21 | 4 | 13 | 2026-06-06T21:36:32+00:00 | 2026-06-06T21:40:33+00:00 |
| 2 | korantis_ba_batch_02_m3_vision_chunk_02_run02 | 25 | 7 | 18 | 7 | 2026-06-06T21:45:58+00:00 | 2026-06-06T21:47:17+00:00 |
| 3 | korantis_ba_batch_02_m3_vision_chunk_03_run02 | 2 | 2 | 0 | 2 | 2026-06-06T21:47:17+00:00 | 2026-06-06T21:47:44+00:00 |

## Distribution per venue

| venue | total | ok_photo | skipped | below<1024 (ok) |
|---|---|---|---|---|
| Apu Nena | 22 | 8 | 14 | 8 |
| Verne Club | 8 | 7 | 1 | 6 |
| Mishiguene | 7 | 5 | 2 | 0 |
| El Preferido de Palermo | 4 | 0 | 4 | 0 |
| Gran Bar Danzon | 3 | 3 | 0 | 3 |
| Oporto Almacén | 3 | 3 | 0 | 2 |
| Florería Atlántico | 3 | 3 | 0 | 3 |
| La Biela | 2 | 1 | 1 | 0 |

## Scene type distribution (M3-verified only)

| scene_type | count |
|---|---|
| product_food | 18 |
| hero_interior | 6 |
| gallery_atmosphere | 2 |
| logo | 1 |
| decorative | 1 |
| hero_exterior | 1 |
| crowd | 1 |

## Selected candidates per venue

### Apu Nena

- total items: 22 · ok_photo: 8 · skipped: 14
- **best_hero_candidate:** _none_
- **best_card_candidate:** _none_
- **best_gallery_candidates:** _none_
- rejected (8):
    - `product_food` · decision=`reference_only` · max_dim=853 · risk=['below_preferred_resolution', 'face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=720 · risk=['below_preferred_resolution', 'face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=720 · risk=['below_preferred_resolution', 'face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=720 · risk=['below_preferred_resolution', 'face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=720 · risk=['below_preferred_resolution', 'face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=720 · risk=['below_preferred_resolution', 'face_release_needed']
    - ... and 2 more

### Florería Atlántico

- total items: 3 · ok_photo: 3 · skipped: 0
- **best_hero_candidate:** `hero_interior` · max_dim=620 · role=`candidate_for_hero_or_card` · risk=['below_preferred_resolution', 'face_release_needed', 'low_contrast_review_needed'] · below<1024=True
    - url: https://www.theworlds50best.com/bars/filestore/jpg/Floreria Atlantico-interior_W50BB24-PROFILE.jpg...
- **best_card_candidate:** _none_
- **best_gallery_candidates:** _none_
- rejected (1):
    - `product_food` · decision=`reference_only` · max_dim=620 · risk=['below_preferred_resolution', 'face_release_needed']

### Gran Bar Danzon

- total items: 3 · ok_photo: 3 · skipped: 0
- **best_hero_candidate:** _none_
- **best_card_candidate:** `gallery_atmosphere` · max_dim=950 · role=`candidate_for_gallery` · risk=['below_preferred_resolution', 'face_release_needed', 'low_contrast_review_needed']
- **best_gallery_candidates:** _none_
- rejected (1):
    - `product_food` · decision=`reference_only` · max_dim=996 · risk=['below_preferred_resolution', 'face_release_needed']

### La Biela

- total items: 2 · ok_photo: 1 · skipped: 1
- **best_hero_candidate:** `hero_exterior` · max_dim=1240 · role=`candidate_for_hero_with_venue_verification` · risk=['face_release_needed'] · below<1024=False
    - url: https://img1.wsimg.com/isteam/ip/9d33b93b-c5c2-4a38-b843-6b534b3cf1de/La%20Biela-21abf06.png/:/cr=t:3.51%25,l:0%25,w:100...
- **best_card_candidate:** _none_
- **best_gallery_candidates:** _none_

### Mishiguene

- total items: 7 · ok_photo: 5 · skipped: 2
- **best_hero_candidate:** _none_
- **best_card_candidate:** _none_
- **best_gallery_candidates:** _none_
- rejected (4):
    - `product_food` · decision=`reference_only` · max_dim=2500 · risk=['face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=1024 · risk=['face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=1024 · risk=['face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=1024 · risk=['face_release_needed']

### Oporto Almacén

- total items: 3 · ok_photo: 3 · skipped: 0
- **best_hero_candidate:** `hero_interior` · max_dim=1500 · role=`candidate_for_hero_or_card` · risk=['face_release_needed'] · below<1024=False
    - url: https://www.oportoalmacen.com.ar/images/main-oporto.jpg...
- **best_card_candidate:** _none_
- **best_gallery_candidates:** _none_
- rejected (2):
    - `product_food` · decision=`reference_only` · max_dim=800 · risk=['below_preferred_resolution', 'face_release_needed']
    - `product_food` · decision=`reference_only` · max_dim=800 · risk=['below_preferred_resolution', 'face_release_needed']

### Verne Club

- total items: 8 · ok_photo: 7 · skipped: 1
- **best_hero_candidate:** `hero_interior` · max_dim=920 · role=`candidate_for_hero_or_card` · risk=['below_preferred_resolution', 'face_release_needed'] · below<1024=True
    - url: https://www.theworlds50best.com/discovery/filestore/jpg/Verne Club-Buenos Aires-Argentina-2.jpg...
- **best_card_candidate:** `gallery_atmosphere` · max_dim=920 · role=`candidate_for_gallery` · risk=['below_preferred_resolution', 'face_release_needed', 'low_contrast_review_needed']
- **best_gallery_candidates:** _none_
- rejected (5):
    - `product_food` · decision=`reference_only` · max_dim=1591 · risk=['face_release_needed']
    - `hero_interior` · decision=`candidate` · max_dim=920 · risk=['below_preferred_resolution', 'face_release_needed']
    - `hero_interior` · decision=`candidate` · max_dim=920 · risk=['below_preferred_resolution', 'face_release_needed']
    - `hero_interior` · decision=`candidate` · max_dim=920 · risk=['below_preferred_resolution', 'face_release_needed', 'low_contrast_review_needed']
    - `product_food` · decision=`reference_only` · max_dim=920 · risk=['below_preferred_resolution', 'face_release_needed']

## Venues sin candidato visual usable

- **El Preferido de Palermo** — all items skipped at dimension gate (<512px) (total=4, skipped=4, ok_photo=0)

## Problemas detectados del pipeline

1. **Sanitizer no hizo HEAD/GET de dimensiones.** El 42% de la queue (22/52) cae por debajo de 512px en runtime, a pesar de haber pasado el sanitizer. M2.7 prevision pasó URLs sin validar tamaño real.
2. **Apu Nena concentra 22/52 (42%)** de la queue, con 14 thumbs <512px de `static.wixstatic.com` que sirven `~mv2.jpg` en pequeñas dimensiones por default.
3. **El Preferido de Palermo: 4/4 thumbs <512px** desde `cloudimg.io` — el CDN responde con versiones pequeñas sin parámetro de resize explícito.
4. **Wix URL con `enc_avif` en el path**: el server responde con `image/webp` cuando Accept lo pide (no avif); magic bytes confirmaron WEBP, lo que PIL acepta. Sin rechazos por avif en este run.
5. **Sources no propias**: 100% de los items son `official_website` con `rights_hint=venue_controlled` (per input), pero la presencia de caras en M3 (`has_identifiable_faces=True`) activa `face_release_needed` en el decision layer, independientemente de rights.
6. **No hubo re-fetch step** entre M2.7 prevision y M3 vision. Si M2.7 hubiera reportado thumbs antes, podríamos haber bajado el size de la queue o pedido versiones full-res antes de gastar M3 calls.
7. **API key en `config.yaml` es placeholder literal** (string enmascarado de 13 chars con `...` literales); la key real está en `~/.hermes/.env` como `MINIMAX_API_KEY`. El runner ya lo resuelve, pero el config debería corregirse. _No se imprime el valor de la key en este reporte por política de no-exposición._

## Recomendación para Codex

- **NO mergear con captioning / copy pipeline todavía.** Ningún item tiene `publication_status=approved_for_publication`.
- **Tratar el set de 30 M3-verified como screening output, no como input creativo.**
- **Para cada `best_hero_candidate`**: pedir versión full-res al sitio (parámetros `w=`, `h=` o fetch directo) si `below_preferred_resolution=True`, antes de considerarlo para producción.
- **Para venues sin candidato usable** (los 4 venues con 100% thumbs): decidir si se re-scrapea o se descartan del scope.
- **Verificar `face_release_needed` antes de usar cualquier hero/card con caras detectadas.**
- **Mantener `validation_status=imported_needs_validation` en el siguiente paso (editorial M2.7 o copy)** — no saltar a validado solo por pasar M3.

## Recomendación para mejorar M2.7 sanitizer/resolver antes del próximo batch

1. **Agregar paso HEAD/GET con validación de dimensiones reales** después de resolver cada `resolved_image_url`. Si `max(w,h) < 1024`, marcar como `low_resolution` y resolver una versión full-res o excluir del queue.
2. **Detectar y rechazar URLs con `enc_avif` en el path** (Wix convierte a avif cuando el cliente lo acepta) o forzar Accept a `image/jpeg,image/png,image/webp` y re-derivar `content_type` real del header del server, no del URL path.
3. **Resolver versiones full-res para CDNs** que sirven thumbs por default: `cloudimg.io` (acepta `?w=`, `?h=`), `static.wixstatic.com` (quitar `/v1/fit/w_X,h_Y/`), `imgix`-based.
4. **No incluir el mismo venue más de N veces** en una queue (N=3 razonable) cuando M2.7 detecta que las URLs alternativas son del mismo origen. Apu Nena tenía 22 — eso es sobremuestreo.
5. **Mantener `width/height/content_length` reales en el item de queue**, no dejar 0/0/0 como actualmente.
6. **Mover el gate de min_dimension 512 al sanitizer**, no al M3 runner. Items <512 no deberían llegar a M3: gastan 1 HTTP call + 1 vision call para nada.
7. **Limpiar la API key en `config.yaml`**: el valor actual es un placeholder literal. Reemplazar por `key: ${MINIMAX_API_KEY}` o leer solo de `.env`.

## Audit trail

- **run01 was renamed to run02 after successful real M3 execution because the runner had hardcoded run01 suffix. No M3 calls were repeated.**
- 3 chunks renombrados (chunk_01/02/03_run01 → _run02) con rewrite de run_id interno.
- Merge estructural construido: 2026-06-06T21:53:29+00:00.
- NO re-inferencia. NO llamadas M3 nuevas. NO web scouting. NO queue expansion.
- API key leida de `~/.hermes/.env` (MINIMAX_API_KEY) en memoria, nunca escrita a logs/disco/reporte.
