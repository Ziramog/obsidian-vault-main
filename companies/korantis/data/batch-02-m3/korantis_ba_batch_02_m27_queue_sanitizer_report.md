# Korantis BA Batch 02 - Queue Sanitizer Report

- Generated: 2026-06-06T18:29:20.730780+00:00
- Source queue: `korantis_ba_batch_02_m27_final_vision_queue.json`
- Target vision model: MiniMax-M3
- Sanitizer scope: M3-supported image formats only

## Sanity rule set

Allowed content types:
- `image/jpeg`
- `image/jpg`
- `image/png`
- `image/webp`

Rejection triggers (any one is enough):
- `content_type` includes `image/svg+xml`
- `resolved_image_url` ends with `.svg`
- `original_image_url` ends with `.svg`
- URL contains `.svg?`
- `content_type` not in allowed set (rejects `image/gif`, `image/avif`, `image/*`, `application/octet-stream`)
- URL matches `logo|icon|map|payment|menu|avatar|favicon|sprite|placeholder`
- `width < 1024 AND height < 1024` ONLY when both dimensions are known and both < 1024 (unknown dims are flagged, not rejected)
- `resolved_image_url` missing or empty
- `source_url` missing or empty

## Counts

| Metric | Value |
|---|---|
| Original queue size | 75 |
| Sanitized queue size | 52 |
| Removed | 23 |
| Rejected - SVG (URL or content_type) | 23 |
| Rejected - unsupported content type | 0 |
| Rejected - low resolution (w<1024 AND h<1024, both known) | 0 |
| Rejected - missing source_url | 0 |
| Rejected - missing resolved_image_url | 0 |
| Rejected - logo/icon/map/payment/menu/avatar | 0 |
| Flagged - unknown dimensions (kept in sanitized queue) | 52 |

## Rejected by venue

| Venue | Rejected |
|---|---|
| Mishiguene | 10 |
| Verne Club | 8 |
| Florería Atlántico | 5 |

## Rejected SVG URLs

- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2017.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2018.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2019.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2020.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2021.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2022.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/50-best-2023.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/Chefs-Choice-2019.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/LA-Liste.svg
- https://mishiguenerestaurant.com/wp-content/uploads/2023/11/Identita-golose.svg
- https://www.theworlds50best.com/filestore/svg/MENU-BUTTON-CLOSE-WHITE.svg
- https://www.theworlds50best.com/filestore/svg/50BEST-DISCOVERY-MARK-WHITE.svg
- https://www.theworlds50best.com/filestore/svg/50BEST-DISCOVERY-MARK-BLACK.svg
- https://www.theworlds50best.com/filestore/svg/menu-button-black.svg
- https://www.theworlds50best.com/filestore/svg/MENU-BUTTON-CLOSE.svg
- https://www.theworlds50best.com/filestore/svg/left-arrow-v2.svg
- https://www.theworlds50best.com/filestore/svg/right-arrow-v2.svg
- https://www.theworlds50best.com/filestore/svg/50BEST-MARK-BLACK.svg
- https://www.theworlds50best.com/filestore/svg/50BEST-BARS-WHITE.svg
- https://www.theworlds50best.com/filestore/svg/50BEST-MARK-WHITE.svg
- https://www.theworlds50best.com/filestore/svg/expand-arrow.svg
- https://www.theworlds50best.com/filestore/svg/menu-button.svg
- https://www.theworlds50best.com/filestore/svg/50BEST-MARK-ACCOLADES.svg

## Rejected - unsupported content type (detail)

- (none)

## Rejected - low resolution (detail)

- (none)

## Rejected - logo/icon/map/payment/menu/avatar (detail)

- (none)

## Flagged - unknown dimensions (kept)

| venue_name | width | height | resolved_image_url |
|---|---|---|---|
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/uploads/2023/11/header_1608743105.png |
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/plugins/revslider/public/assets/assets/dummy.png |
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/uploads/2023/11/DSC0482-1024x683.jpg |
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/uploads/2023/11/Copia-de-LA8A5510-682x1024.jpg |
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/uploads/2023/11/Copia-de-LA8A1536-683x1024.jpg |
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/uploads/2023/11/Copia-de-LA8A1489-1024x683.jpg |
| Mishiguene | 0 | 0 | https://mishiguenerestaurant.com/wp-content/uploads/2023/11/Copia-de-LA8A5280.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/Verne Club-Buenos Aires-Argentina-1.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/Verne Club-Buenos Aires-Argentina-2.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/Verne Club-Buenos Aires-Argentina-3.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpeg/GrandDabbang-BuenosAires-Argentina01.jpeg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/Nicky_Harrison_Bartender.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/Don-Julio-Buenos-Aires-Argentina-03.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/restaurant-awaiting-1.jpg |
| Verne Club | 0 | 0 | https://www.theworlds50best.com/discovery/filestore/jpg/cochinchina-ba (2).jpg |
| Gran Bar Danzon | 0 | 0 | https://granbardanzon.com.ar/wp-content/uploads/2020/08/quienes-somos-gran-BAR-DANZON-1.jpg |
| Gran Bar Danzon | 0 | 0 | https://granbardanzon.com.ar/wp-content/uploads/2020/08/FEED-I-BASA-4.jpg |
| Gran Bar Danzon | 0 | 0 | https://granbardanzon.com.ar/wp-content/uploads/2020/08/FEED-I-BASA-7.png |
| Oporto Almacén | 0 | 0 | https://www.oportoalmacen.com.ar/images/main-oporto.jpg |
| Oporto Almacén | 0 | 0 | https://www.oportoalmacen.com.ar/images/main-calendario-00.jpg |
| Oporto Almacén | 0 | 0 | https://www.oportoalmacen.com.ar/images/main-calendario-01.jpg |
| La Biela | 0 | 0 | https://img1.wsimg.com/isteam/ip/9d33b93b-c5c2-4a38-b843-6b534b3cf1de/300183307_378796617743638_2434181242857306856_.jpg/:/rs=h:105,cg:true,m/qt=q:95 |
| La Biela | 0 | 0 | https://img1.wsimg.com/isteam/ip/9d33b93b-c5c2-4a38-b843-6b534b3cf1de/La%20Biela-21abf06.png/:/cr=t:3.51%25,l:0%25,w:100%25,h:92.97%25/rs=w:1240,h:620,cg:true |
| Florería Atlántico | 0 | 0 | https://www.theworlds50best.com/bars/filestore/jpg/Floreria Atlantico-cocktail_W50BB24-PROFILE-hero.jpg |
| Florería Atlántico | 0 | 0 | https://www.theworlds50best.com/bars/filestore/jpg/Floreria Atlantico-interior_W50BB24-PROFILE.jpg |
| Florería Atlántico | 0 | 0 | https://www.theworlds50best.com/bars/filestore/jpg/Floreria Atlantico-team_W50BB24-PROFILE.jpg |
| El Preferido de Palermo | 0 | 0 | https://axwwgrkdco.cloudimg.io/v7/__gmpics3__/dd31a9e70a8b437299a0aff6f6b743a8.jpg |
| El Preferido de Palermo | 0 | 0 | https://axwwgrkdco.cloudimg.io/v7/__gmpics3__/360fa7605889471c90a2b93fba68968f.jpeg |
| El Preferido de Palermo | 0 | 0 | https://axwwgrkdco.cloudimg.io/v7/__gmpics3__/62bd1338f01f40bbb584d84e4ac166dd.jpeg |
| El Preferido de Palermo | 0 | 0 | https://axwwgrkdco.cloudimg.io/v7/__gmpics3__/9e55927cfd354e599e080558c2d70713.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/22db839dd0a94a1c9dd91dafe2617dc1.png/v1/fill/w_20,h_20,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Google%20Places.png |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/81af6121f84c41a5b4391d7d37fce12a.png/v1/fill/w_20,h_20,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Instagram.png |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/23fd2a2be53141ed810f4d3dcdcd01fa.png/v1/fill/w_20,h_20,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Facebook.png |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_13b2fe16a33d464283df54a2376a4dd8~mv2.jpg/v1/fill/w_147,h_83,al_c,q_80,usm_0.66_1.00_0.01,blur_2,enc_avif,quality_auto/57a016_13b2fe16a33d464283df54a2376a4dd8~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_ac8c21db6b4c41c382e77385bdc1e058~mv2.jpg/v1/fill/w_123,h_184,al_c,q_80,usm_0.66_1.00_0.01,blur_2,enc_avif,quality_auto/57a016_ac8c21db6b4c41c382e77385bdc1e058~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_9fc86113cb184ac481ab7acd1ce87262~mv2.jpg/v1/fill/w_300,h_300,fp_0.56_0.45,q_90,enc_avif,quality_auto/57a016_9fc86113cb184ac481ab7acd1ce87262~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_27bdedf30f484e2bb28474d625c78d87~mv2.jpg/v1/fill/w_300,h_300,q_90,enc_avif,quality_auto/57a016_27bdedf30f484e2bb28474d625c78d87~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_32bee979798d40c9bbb77809b629fe38~mv2.jpg/v1/fill/w_300,h_300,fp_0.39_0.31,q_90,enc_avif,quality_auto/57a016_32bee979798d40c9bbb77809b629fe38~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_3832ad66b6d54f3ea25c6b4873fe9b35~mv2.jpg/v1/fill/w_300,h_300,q_90,enc_avif,quality_auto/57a016_3832ad66b6d54f3ea25c6b4873fe9b35~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_fdc209b8a6684229802041eb4b96c4ff~mv2.jpg/v1/fill/w_300,h_300,fp_0.25_0.75,q_90,enc_avif,quality_auto/57a016_fdc209b8a6684229802041eb4b96c4ff~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_1d8d7e29dd834e25b282a5af8e2a98db~mv2.jpg/v1/fill/w_300,h_300,fp_0.12_0.48,q_90,enc_avif,quality_auto/57a016_1d8d7e29dd834e25b282a5af8e2a98db~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_02e3e7b3daed44f3b58b010a8206d1e4~mv2.jpg/v1/fill/w_300,h_300,q_90,enc_avif,quality_auto/57a016_02e3e7b3daed44f3b58b010a8206d1e4~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_b7f0c0abba8e4d34807615a959cf3266~mv2.jpg/v1/fill/w_300,h_300,q_90,enc_avif,quality_auto/57a016_b7f0c0abba8e4d34807615a959cf3266~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_64ad91e35df5406d858d2af3d5c4eff0~mv2.jpg/v1/fill/w_300,h_300,q_90,enc_avif,quality_auto/57a016_64ad91e35df5406d858d2af3d5c4eff0~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_bc3900de27c341f7874193d9e5a54e43~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_bc3900de27c341f7874193d9e5a54e43~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_ba2dc6001ebc4dac96c2730f76823280~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_ba2dc6001ebc4dac96c2730f76823280~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_23c798acb2374ff8bbc95b65b88e1a39~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_23c798acb2374ff8bbc95b65b88e1a39~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_aa17ba228ac741f9a27f5592da771522~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_aa17ba228ac741f9a27f5592da771522~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_68a0366f7f2147c7a0c63cd2c6d23a93~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_68a0366f7f2147c7a0c63cd2c6d23a93~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_56f984f58d65458d92f6b73ee02d1cb8~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_56f984f58d65458d92f6b73ee02d1cb8~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_b195af11ac604ac9b9051d4295ff6cdd~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_b195af11ac604ac9b9051d4295ff6cdd~mv2.jpg |
| Apu Nena | 0 | 0 | https://static.wixstatic.com/media/57a016_60095639af3d4ed5a7ed20a61c688dfa~mv2.jpg/v1/fit/w_480,h_1373,q_90,enc_avif,quality_auto/57a016_60095639af3d4ed5a7ed20a61c688dfa~mv2.jpg |

## Sanitized queue - venues included

- Apu Nena: 22 image(s)
- El Preferido de Palermo: 4 image(s)
- Florería Atlántico: 3 image(s)
- Gran Bar Danzon: 3 image(s)
- La Biela: 2 image(s)
- Mishiguene: 7 image(s)
- Oporto Almacén: 3 image(s)
- Verne Club: 8 image(s)

## Verdict

READY FOR M3. Sanitized queue has 52 items. All have:
- allowed content type (jpeg/jpg/png/webp)
- non-logo/icon/map/payment/menu/avatar URLs
- present `source_url` and `resolved_image_url`
- confirmed resolution (>=1024 on at least one axis) OR unknown dimensions (flagged, kept)

- Output queue: `korantis_ba_batch_02_m27_final_vision_queue_sanitized.json`
- Full path: `/home/hermes/obsidian-vault/Hermes/companies/korantis/korantis_ba_batch_02_m27_final_vision_queue_sanitized.json`
