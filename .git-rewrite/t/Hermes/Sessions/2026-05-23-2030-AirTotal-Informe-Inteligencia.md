# SESIÓN — 23 de mayo de 2026
## Tema: Informe Inteligencia Air Total SRL — Versión Ampliada

---

## Inicio de sesión
- **Hora:** ~20:30 UTC-3
- **Contexto:** Juan pidió ampliar el informe con información actual y scrapeo del Boletín Oficial de Catamarca. Quería un "verdadero informe de inteligencia". Mencionó patchright (github.com/Kaliiiiiiiiii-Vinyzu/patchright).

---

## Trabajo realizado

### 1. Instalación y configuración de patchright
- `pip install patchright` — exitoso
- Problema inicial: `EACCES: permission denied, mkdtemp '/tmp/playwright-artifacts-...'` — el entorno no tiene acceso a /tmp
- **Solución aplicada:**
  - `mkdir -p /home/hermes/tmp/playwright`
  - `PLAYWRIGHT_BROWSERS_PATH=/home/hermes/tmp/playwright playwright install chromium` → descargó Chrome Headless Shell 147.0.7727.15 (1217)
  - `TMPDIR=/home/hermes/tmp` en cada ejecución
  - `executable_path` explícito: `/home/hermes/tmp/playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell`
  - No usar `p.chromium.launch()` sin `executable_path` — busca en la ruta vieja (1208) y falla

### 2. Scraping airtotal.shop (patchright)
- `page.goto(url, timeout=30000)` + `page.wait_for_timeout(3000)` para JS
- `page.inner_text("body")` para texto, `page.content()` para HTML completo
- **Resultado:** Menos de 20 productos reales en el catálogo
- Productos encontrados: capacitores, cañería, motor forzador, kit eléctrico, mangueras, test 2, cinta aluminio, panel solar $20 (mal categorizado), refrigerantes (R134A, R22, R404A, R410A), garrafa MAP, bomba de condensado, varilla plata
- Número WhatsApp genérico: `wa.me/123456789` (no funciona — es de prueba)
- **Key finding:** La empresa opera como distribuidor minorista de climatización, NO como empresa de ingeniería civil pesada

### 3. Búsquedas web complementarias
- Niederle dejó Infraestructura en dic 2023 → pasó a Min. Agua, Energía y Medio Ambiente
- Nueva causa penal abril 2025 (vecinos Nueva Coneta, Capayán): Incumplimiento deberes + Estafa por 6 días sin agua
- Proyecto de resolución legislativa 2022 sobre Air Total: **EN TRÁMITE** en Cámara de Diputados Catamarca (sin resolver 3.5 años)
- LinkedIn: Jose Graffigna (contable 5+ años), Javier Gimenez (técnico), Sergio Mlacak (ex supervisor logística, solo 5 meses) → plantilla real: 5–15 personas
- Air Total NO aparece en cadenas de suministro de Sal de Vida, MARA, Arcadium, Lition Energy, YMAD
- Global Minera SÍ tiene contratos documentados con todas esas mineras

### 4. Generación del informe ampliado (v2.0)
- Scraping directo del sitio + web searches + extracción de Boletín Oficial
- Nueva sección 0 (Halloazgo crítico sobre naturaleza real de la empresa)
- Nueva sección 8 (Hallazgos inéditos: producto $20, WhatsApp genérico, categorías vacías)
- Matriz de riesgos ampliada
- Recomendación: NO formalizar consorcio sin due diligence legal + documentación financiera

### 5. PDF generado y enviado a Telegram
- Markdown → HTML (conversor propio en Python) → PDF via patchright `page.pdf()`
- Estilo: oscuro/gold (background #0d0d14, texto #e0e0e0, acentos #ffd700)
- Tamaño: 121.1 KB (123,985 bytes), formato A4
- Enviado a Juanchi777 (Telegram) — message_id 4513

---

## Herramientas configuradas exitosamente

### patchright (scraping con browser automation)
```
PLAYWRIGHT_BROWSERS_PATH=/home/hermes/tmp/playwright TMPDIR=/home/hermes/tmp python3 - <<'PYEOF'
from patchright.sync_api import sync_playwright
import os
os.environ['TMPDIR'] = '/home/hermes/tmp'
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/home/hermes/tmp/playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell"
    )
    page = browser.new_page()
    page.goto("URL", timeout=30000)
    page.wait_for_timeout(3000)
    text = page.inner_text("body")
    browser.close()
PYEOF
```
**Requiere:** `PLAYWRIGHT_BROWSERS_PATH`, `TMPDIR`, `executable_path` explícito
**Para instalar:** `PLAYWRIGHT_BROWSERS_PATH=/home/hermes/tmp/playwright playwright install chromium`
**Usar siempre:** `TMPDIR=/home/hermes/tmp` en el environment

### chromium-browser (generación de PDF desde HTML)
```
/usr/bin/chromium-browser --headless --disable-gpu --no-sandbox --print-to-pdf=output.pdf file://input.html
```
**Para qué:** HTML → PDF cuando patchright no está disponible o es lento

### Python pdf (pymupdf) — para extraer texto de PDFs descargados
```
import pymupdf
doc = pymupdf.open("archivo.pdf")
for page in doc:
    text = page.get_text()
```
**Instalar:** `pip install --break-system-packages pymupdf`

---

## Archivos generados
- `/home/hermes/obsidian-vault/Hermes/Intelligence/AirTotal_SRL_2026-05-23.md` — informe v2.0 (18,584 bytes)
- `/home/hermes/tmp/AirTotal_Informe_Inteligencia_2026-05-23.pdf` — PDF enviado (123,985 bytes)
- `/home/hermes/tmp/airtotal_report.html` — HTML intermedio (42,100 bytes)
- `/home/hermes/tmp/bulletin/` — directorio para boletines oficiales

---

## Decisiones tomadas
- Se priorizó patchright + chromium-browser sobre pyppeteer/scrapling (que requerían pyppeteer no disponible)
- Se usó conversor markdown→HTML propio en lugar de librerías externas (markdown no instalado)
- Se envió PDF por curl subprocess (la ruta MEDIA: no funcionó directamente)

---

## Pendientes
- MEMORY.md actualizar con nuevos tools instalados (patchright, pymupdf, chromium-browser)
- Due diligence legal sobre Air Total → queda para Juan
- Documentación financiera de Air Total → queda para Juan
- Evaluación de alternativa: Global Minera como socio en lugar de Air Total

---

*Sesión iniciada: 23/05/2026 ~20:30 | Hermes — Sistema Operativo de Juan Gomariz*