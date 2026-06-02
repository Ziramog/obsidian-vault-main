import os, json, re, base64
os.environ['TMPDIR'] = '/home/hermes/.tmp_chrome'

# Cargar reviews finales
with open('/home/hermes/.tmp_chrome/reviews.json') as f:
    raw_reviews = json.load(f)

# Deduplicar
seen = set()
unique_reviews = []
for r in raw_reviews:
    key = (r['name'], r['text'])
    if key not in seen:
        seen.add(key)
        unique_reviews.append(r)

photo_dir = '/home/hermes/obsidian-vault/companies/wolfim/clients/franco-roma/reviews-photos'

# Convertir fotos a data URIs (base64) para embeber en el HTML
def img_to_data_uri(filepath):
    if not os.path.exists(filepath):
        return None
    ext = os.path.splitext(filepath)[1].lstrip('.').lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'
    with open(filepath, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime};base64,{data}"

# Generar HTML
reviews_html = []
for r in unique_reviews:
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', r['name'])
    photo_path = os.path.join(photo_dir, f"{r['num']:02d}_{safe_name}.jpg")
    photo_uri = img_to_data_uri(photo_path)
    
    photo_html = f'<img src="{photo_uri}" alt="{r["name"]}" class="avatar">' if photo_uri else '<div class="avatar-placeholder">?</div>'
    
    # Estrellas visual
    try:
        stars_num = int(r['rating'].split()[0])
    except:
        stars_num = 5
    stars = '★' * stars_num + '☆' * (5 - stars_num)
    
    reviews_html.append(f'''
<div class="review">
    <div class="review-header">
        {photo_html}
        <div class="review-meta">
            <div class="review-name">{r['name']}</div>
            <div class="review-stars">{stars} <span class="rating-text">{r['rating']}</span></div>
            <div class="review-date">{r['date']}</div>
        </div>
    </div>
    <div class="review-text">{r['text']}</div>
</div>
''')

# Calcular distribución
dist = {'5': 28, '4': 2, '3': 0, '2': 0, '1': 0}
total = sum(dist.values())
pct = {k: int(v*100/total) for k, v in dist.items()}

# Distribución visual con barras
dist_html = ''
for star, count in dist.items():
    bar_width = pct[star]
    dist_html += f'''
<div class="dist-row">
    <div class="dist-label">{star} ★</div>
    <div class="dist-bar-bg">
        <div class="dist-bar" style="width: {bar_width}%;"></div>
    </div>
    <div class="dist-count">{count}</div>
</div>'''

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reseñas Google Maps — Roggero & Roma</title>
<style>
@page {{
    size: A4;
    margin: 1.5cm 1.5cm 2cm 1.5cm;
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: #0a0a0f;
    color: #ffffff;
    font-size: 10pt;
    line-height: 1.45;
    margin: 0;
    padding: 24px;
}}
.brand {{
    display: inline-block;
    background: linear-gradient(135deg, #1a1a25 0%, #2a2a35 100%);
    color: #f5c518;
    padding: 4px 14px;
    border-radius: 4px;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 8px;
}}
h1 {{
    font-size: 22pt;
    margin: 6px 0 4px 0;
    color: #ffffff;
    letter-spacing: -0.5px;
}}
h2 {{
    color: #f5c518;
    font-size: 13pt;
    margin: 18px 0 8px 0;
    border-bottom: 1px solid rgba(245, 197, 24, 0.2);
    padding-bottom: 4px;
}}
.subtitle {{
    color: #8a8a95;
    font-size: 9pt;
    margin-bottom: 14px;
}}
.summary {{
    background: rgba(245, 197, 24, 0.05);
    border: 1px solid rgba(245, 197, 24, 0.2);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.rating-big {{
    font-size: 36pt;
    font-weight: 800;
    color: #f5c518;
    line-height: 1;
}}
.rating-stars-big {{
    color: #f5c518;
    font-size: 14pt;
    letter-spacing: 2px;
}}
.rating-text-small {{
    color: #8a8a95;
    font-size: 9pt;
    margin-top: 4px;
}}
.dist {{
    flex: 1;
    margin-left: 24px;
}}
.dist-row {{
    display: flex;
    align-items: center;
    margin: 3px 0;
    font-size: 8.5pt;
}}
.dist-label {{
    width: 30px;
    color: #f5c518;
    font-weight: 600;
}}
.dist-bar-bg {{
    flex: 1;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    margin: 0 8px;
    overflow: hidden;
}}
.dist-bar {{
    height: 100%;
    background: #f5c518;
    border-radius: 3px;
}}
.dist-count {{
    width: 30px;
    text-align: right;
    color: #8a8a95;
}}
.review {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
    page-break-inside: avoid;
}}
.review-header {{
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}}
.avatar {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #f5c518;
    margin-right: 12px;
}}
.avatar-placeholder {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #2a2a35;
    color: #f5c518;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18pt;
    font-weight: 700;
    margin-right: 12px;
}}
.review-meta {{ flex: 1; }}
.review-name {{
    font-weight: 700;
    color: #ffffff;
    font-size: 10.5pt;
    margin-bottom: 2px;
}}
.review-stars {{
    color: #f5c518;
    font-size: 11pt;
    letter-spacing: 1px;
}}
.rating-text {{
    color: #8a8a95;
    font-size: 8.5pt;
    margin-left: 4px;
}}
.review-date {{
    color: #6a6a75;
    font-size: 8pt;
    margin-top: 1px;
}}
.review-text {{
    color: #d0d0d0;
    font-size: 9.5pt;
    line-height: 1.5;
    margin-left: 60px;
}}
.footer {{
    margin-top: 18px;
    padding-top: 10px;
    border-top: 1px solid rgba(245, 197, 24, 0.2);
    text-align: center;
    color: #6a6a75;
    font-size: 8pt;
}}
</style>
</head>
<body>

<div class="brand">WOLFIM</div>
<h1>Reseñas de Google Maps</h1>
<div class="subtitle">Silvia Roggero de Roma Negocios Inmobiliarios · Alta Gracia, Córdoba · 2 de junio de 2026</div>

<div class="summary">
    <div>
        <div class="rating-big">4.8</div>
        <div class="rating-stars-big">★★★★★</div>
        <div class="rating-text-small">30 reseñas</div>
    </div>
    <div class="dist">
        {dist_html}
    </div>
</div>

<h2>Reseñas individuales (10 más relevantes / recientes)</h2>
{''.join(reviews_html)}

<div class="footer">
    Recopilación preparada por Wolfim · WebAgency · 2 de junio de 2026<br>
    Fuente: Google Maps (https://www.google.com/maps/place/Silvia+Roggero+de+Roma+Negocios+Inmobiliarios)
</div>

</body>
</html>"""

html_path = "/home/hermes/obsidian-vault/companies/wolfim/clients/franco-roma/reviews-report.html"
with open(html_path, 'w') as f:
    f.write(html)
print(f"HTML generado: {os.path.getsize(html_path)} bytes")

# Generar PDF
from playwright.sync_api import sync_playwright
out_pdf = "/home/hermes/obsidian-vault/companies/wolfim/clients/franco-roma/reviews-google-maps.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'])
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"file://{html_path}", wait_until='networkidle')
    page.pdf(
        path=out_pdf,
        format='A4',
        margin={"top": "15mm", "right": "15mm", "bottom": "15mm", "left": "15mm"},
        print_background=True,
    )
    browser.close()

print(f"PDF: {out_pdf}")
print(f"Tamaño: {os.path.getsize(out_pdf)} bytes ({os.path.getsize(out_pdf)/1024:.1f} KB)")

# Limpiar HTML temporal
os.remove(html_path)
print("HTML temporal eliminado")
