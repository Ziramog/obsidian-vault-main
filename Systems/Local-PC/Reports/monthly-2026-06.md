# Informe Mensual - 2026-06

> Equipo: DESKTOP-3V091DM
> Duracion: 7.5 segundos

## 1. Inventario de Hardware

- CPU: Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz (4 cores)
- RAM: 32 GB
- GPU: NVIDIA GeForce RTX 3070 Ti
- Motherboard: ASRock H110 Pro BTC+

## 2. Software principal

- Git: git version 2.54.0.windows.1
- GitHub CLI: gh version 2.95.0 (2026-06-17)
- Node.js: v22.23.0
- npm: 10.9.8
- Python: Python 3.11.15
- uv: uv 0.11.23 (3cdf50e09 2026-06-19 x86_64-pc-windows-msvc)
- Hermes: Hermes Agent v0.17.0 (2026.6.19) ┬╖ upstream 433db17c ┬╖ local bb7ff7dc (+1 carried commit)

## 3. Estado de Backups

- C:\Backups\Boot | 3 archivos | ultimo: 0 dias
- I:\Backups | NO EXISTE
- I:\roggero_backup | 1 archivos | ultimo: 3 dias

## 4. Almacenamiento

- C:: 114/476.9 GB usado, 362.9 GB libre (76.1%)
- D:: 219.8/495.8 GB usado, 276 GB libre (55.7%)
- E:: 0/0 GB usado, 0 GB libre (38.7%)
- F:: 145.7/146 GB usado, 0.3 GB libre (0.2%) *BAJO*
- G:: 57/86.4 GB usado, 29.4 GB libre (34.1%)
- H:: 439.9/488.3 GB usado, 48.4 GB libre (9.9%) *BAJO*
- I:: 676.7/878.9 GB usado, 202.2 GB libre (23%)

## 5. Cambios del mes

- | 2026-06-23 | 13:24 | config | CreaciÃ³n del workspace | 4 archivos, terminal.cwd, approvals.mode=manual | Revertir config |
- | 2026-06-23 | 18:36 | respaldo | BCD exportado, inventario pre-intervenciÃ³n | `C:\Backups\Boot\` | `bcdedit /import` |
- | 2026-06-23 | 18:42 | arranque | NVMe autÃ³nomo: bcdboot + bootsect Disco 2 | C: bootmgr + BCD + MBR NT60 | Revertir con diskpart |
- | 2026-06-23 | 19:00 | arranque | VerificaciÃ³n post-reinicio | Disco 2: IsSystem=True. Disco 0 liberado. | N/A |
- | 2026-06-23 | 19:10 | seguridad | Token ghp_ revocado y remote wolfim-web limpiado | `gh auth setup-git`. HTTPS limpia, ls-remote OK. | N/A |
- | 2026-06-23 | 19:15 | config | Teclado espaÃ±ol latino agregado | 3 layouts `0000080A` (es-AR, es-MX, es-419) + US English | Quitar con PowerShell |

## 6. Recomendaciones

- CRITICO: F: al 0.2% - requiere liberar espacio urgente
- ATENCION: H: al 9.9% - considerar liberar espacio

---
*Generado automaticamente. Solo lectura. Sin acciones realizadas.*
