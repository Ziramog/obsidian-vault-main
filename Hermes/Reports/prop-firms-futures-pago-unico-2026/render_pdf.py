from pathlib import Path
import markdown

base = Path(__file__).resolve().parent
md = (base / 'reporte.md').read_text(encoding='utf-8')
# Strip Obsidian YAML frontmatter from the printable version.
if md.startswith('---\n'):
    _, _, md = md.split('---\n', 2)
body = markdown.markdown(md, extensions=['extra', 'tables', 'toc', 'sane_lists'])
css = r'''
@page {
  size: A4;
  margin: 17mm 16mm 18mm 16mm;
  @bottom-left { content: "Investigación independiente · 11 julio 2026"; font-size: 7.5pt; color: #777; }
  @bottom-right { content: "Página " counter(page) " de " counter(pages); font-size: 7.5pt; color: #777; }
}
* { box-sizing: border-box; }
body { font-family: Arial, "DejaVu Sans", sans-serif; color:#202124; font-size:9.2pt; line-height:1.48; margin:0; }
h1 { font-size:24pt; line-height:1.08; color:#102a43; margin:0 0 8mm; padding-bottom:4mm; border-bottom:3px solid #147d92; }
h2 { font-size:15pt; color:#102a43; margin:8mm 0 3mm; padding-bottom:1.5mm; border-bottom:1px solid #a7c9d1; break-after:avoid; }
h3 { font-size:11.5pt; color:#125d6b; margin:5mm 0 2mm; break-after:avoid; }
p { margin:0 0 3mm; }
strong { color:#102a43; }
a { color:#126b7b; text-decoration:none; overflow-wrap:anywhere; }
blockquote { margin:4mm 0; padding:3.5mm 4.5mm; background:#edf7f8; border-left:4px solid #147d92; color:#173f47; font-size:10pt; }
table { width:100%; border-collapse:collapse; margin:3mm 0 5mm; font-size:7.5pt; break-inside:auto; }
thead { display:table-header-group; }
tr { break-inside:avoid; }
th { background:#123b52; color:white; padding:2.2mm 1.7mm; text-align:left; vertical-align:top; }
td { border:0.4px solid #cbd5db; padding:2mm 1.7mm; vertical-align:top; }
tr:nth-child(even) td { background:#f4f8fa; }
ul,ol { margin:1.5mm 0 3mm 5.5mm; padding-left:3.5mm; }
li { margin:0 0 1.1mm; }
hr { border:0; border-top:1px solid #cbd5db; margin:7mm 0; }
code { background:#f0f3f5; padding:0.3mm 0.7mm; border-radius:2px; }
.cover { min-height:238mm; display:flex; flex-direction:column; justify-content:center; page-break-after:always; background:linear-gradient(145deg,#f8fbfc 0%,#edf7f8 100%); padding:18mm; border:1px solid #d7e7eb; }
.cover .eyebrow { color:#147d92; font-weight:bold; letter-spacing:1.4px; text-transform:uppercase; font-size:9pt; }
.cover h1 { font-size:31pt; border:none; margin:6mm 0; }
.cover .subtitle { font-size:15pt; color:#456; max-width:145mm; }
.cover .meta { margin-top:22mm; font-size:9.5pt; color:#5f6b73; }
.callout { background:#fff8e6; border:1px solid #e5c66d; padding:4mm; margin:4mm 0; }
.small { font-size:7.5pt; color:#667; }
.page-break { page-break-before:always; }
'''
# Remove first H1 from body because cover has title
body_no_h1 = body.replace('<h1>Prop firms de futuros con pago único</h1>', '', 1)
cover = '''<section class="cover"><div class="eyebrow">Research report · Futures</div><h1>Prop firms de futuros<br>con pago único</h1><div class="subtitle">Comparación profunda para un trader argentino con presupuesto limitado</div><div class="meta"><b>Fecha de corte:</b> 11 de julio de 2026<br><b>Alcance:</b> costos reales, drawdown, payouts, Argentina y riesgos contractuales<br><b>Conclusión:</b> elegir por costo total y dificultad real, no por saldo publicitario.</div></section>'''
html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Prop firms de futuros con pago único</title><style>{css}</style></head><body>{cover}{body_no_h1}</body></html>'''
(base / 'reporte.html').write_text(html, encoding='utf-8')
print(base / 'reporte.html')
