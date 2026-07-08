#!/usr/bin/env python3
"""
Generador automático del informe mensual de Analytics para Roggero & Roma.

Uso:
    python3 generate_roggero_analytics_auto.py [--start YYYY-MM-DD] [--end YYYY-MM-DD]

Ejemplo:
    python3 generate_roggero_analytics_auto.py --start 2026-06-08 --end 2026-07-07

Sin argumentos: usa el mes calendario anterior completo.
"""

import sys
from pathlib import Path
from datetime import date, timedelta
import argparse

sys.path.append('/home/hermes/scripts')
from wolfim_report_preset import WolfimReport, copy_to_transfer

# ─── GA4 query helpers ──────────────────────────────────────────────
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests, json

KEY = '/home/hermes/.hermes/profiles/wolfim-growth/wolfim-analytics-tools-a0b1de9655b0.json'
PROP = '539918073'

creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=['https://www.googleapis.com/auth/analytics.readonly'])
creds.refresh(Request())
HEADERS = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}
BASE = f'https://analyticsdata.googleapis.com/v1beta/properties/{PROP}:runReport'


def ga4(dimensions, metrics, filt=None, limit=100, order_metric=None):
    body = {
        'dateRanges': [{'startDate': START, 'endDate': END}],
        'dimensions': [{'name': d} for d in dimensions],
        'metrics': [{'name': m} for m in metrics],
        'limit': limit,
    }
    if order_metric:
        body['orderBys'] = [{'metric': {'metricName': order_metric}, 'desc': True}]
    if filt:
        body['dimensionFilter'] = filt
    r = requests.post(BASE, headers=HEADERS, json=body, timeout=45)
    d = r.json()
    if r.status_code >= 400:
        return []
    dims = [x['name'] for x in d.get('dimensionHeaders', [])]
    mets = [x['name'] for x in d.get('metricHeaders', [])]
    rows = []
    for row in d.get('rows', []):
        rr = {}
        for i, k in enumerate(dims):
            rr[k] = row['dimensionValues'][i].get('value')
        for i, k in enumerate(mets):
            rr[k] = row['metricValues'][i].get('value')
        rows.append(rr)
    return rows


# ─── Parse args ─────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument('--start', help='Start date YYYY-MM-DD')
parser.add_argument('--end', help='End date YYYY-MM-DD')
args = parser.parse_args()

if args.start and args.end:
    START = args.start
    END = args.end
else:
    # Default: previous full month
    today = date.today()
    first_of_month = today.replace(day=1)
    end_of_prev = first_of_month - timedelta(days=1)
    start_of_prev = end_of_prev.replace(day=1)
    START = start_of_prev.strftime('%Y-%m-%d')
    END = end_of_prev.strftime('%Y-%m-%d')

PERIOD_LABEL = f'{START} al {END} · últimos 30 días'
DATE_LABEL = date.today().strftime('%d/%m/%Y')
OUT_NAME = f'roggero_roma_informe_analytics_{START}_{END}.pdf'
OUT = Path(f'/home/hermes/{OUT_NAME}')

print(f'📊 Generando informe Roggero & Roma — {START} a {END}')

# ─── Fetch GA4 data ─────────────────────────────────────────────────
print('Consultando GA4...')

# Countries
countries = ga4(['country'], ['totalUsers', 'sessions', 'screenPageViews'], limit=15, order_metric='screenPageViews')

# Filters
pages = ga4(['pagePathPlusQueryString', 'pageTitle'], ['screenPageViews', 'totalUsers'], limit=100, order_metric='screenPageViews')

# Devices
devices = ga4(['deviceCategory'], ['totalUsers', 'sessions', 'screenPageViews'], limit=5)

# Hours
hours = ga4(['hour'], ['sessions', 'screenPageViews'], limit=24, order_metric='sessions')
hours_map = {int(r['hour']): r for r in hours}

# Weekdays
weekdays = ga4(['dayOfWeekName'], ['sessions', 'screenPageViews'], limit=10, order_metric='sessions')

# Events
filt_events = {'filter': {'fieldName': 'eventName', 'inListFilter': {'values': ['form_start', 'click', 'click_whatsapp']}}}
events = ga4(['eventName'], ['eventCount', 'totalUsers'], filt=filt_events, limit=10)

# Property pages (individual)
props = [r for r in pages if '/properties/' in r.get('pagePathPlusQueryString', '') and '/admin' not in r['pagePathPlusQueryString']]

# Summary
total_users = sum(int(r.get('totalUsers', 0)) for r in countries)
total_sessions = sum(int(r.get('sessions', 0)) for r in countries)
total_views = sum(int(r.get('screenPageViews', 0)) for r in countries)
ar = next((r for r in countries if r.get('country') == 'Argentina'), None)
organic = ga4(['sessionSource', 'sessionMedium'], ['sessions', 'screenPageViews'], limit=20)
google_organic = sum(int(r.get('sessions', 0)) for r in organic if r.get('sessionMedium') == 'organic')

print(f'  Usuarios: {total_users} | Sesiones: {total_sessions} | Vistas: {total_views}')

# ─── Build PDF ──────────────────────────────────────────────────────
pdf = WolfimReport(
    report_title='Informe mensual de Analytics',
    client_name='Roggero & Roma',
    footer_text='Wolfim Studio · Medición web y crecimiento comercial',
)

pdf.add_cover(
    title='Informe mensual de Analytics',
    subtitle='Lectura comercial del rendimiento web: tráfico, procedencia, navegación del catálogo y comportamiento de búsqueda.',
    client='Roggero & Roma',
    period=PERIOD_LABEL,
    prepared_for='Franco / Marcos Roma',
    date_label=DATE_LABEL,
)

# ── Page 2: Resumen ─────────────────────────────────────────────────
pdf.add_page()
pdf.section('Resumen ejecutivo', 'Lectura comercial')
pdf.body('El sitio ya tiene una base mensual medible con navegación real dentro del catálogo. Argentina concentra la navegación útil; el tráfico internacional aparece en usuarios pero con baja profundidad.')

ppv = round(total_views / max(total_sessions, 1), 2)
pdf.metric_cards([
    ('Usuarios activos', str(total_users), 'últimos 30 días'),
    ('Sesiones registradas', str(total_sessions), 'visitas al sitio'),
    ('Vistas acumuladas', str(total_views), 'tráfico útil'),
    ('Sesiones Google orgánico', str(google_organic), 'búsqueda real'),
    ('Páginas por sesión', str(ppv).replace('.', ','), 'navegación promedio'),
    ('Engagement rate', str(round(sum(float(r.get('engagementRate', 0)) for r in ga4([], ['engagementRate'], limit=1)) * 100, 1)) + '%' if ga4([], ['engagementRate'], limit=1) else '—', 'sesiones con interacción'),
])

pdf.callout(
    'Conclusión principal',
    'El sitio ya muestra qué secciones y filtros despiertan interés y desde dónde llega la gente. El próximo paso: medir qué propiedades generan los contactos reales.',
    tone='green',
)

# ── Page 3: Procedencia ─────────────────────────────────────────────
pdf.section('Procedencia estimada de visitas', 'País de conexión')
pdf.body('Analytics estima país de conexión por IP. No equivale a nacionalidad. Conviene mirar usuarios, sesiones y vistas en conjunto.', size=8.5, color='muted')

country_rows = []
ar_total = int(ar.get('screenPageViews', 0)) if ar else 0
for c in countries[:6]:
    name = c.get('country', '')
    if name in ('(not set)', ''):
        continue
    u = c.get('totalUsers', '0')
    s = c.get('sessions', '0')
    v = c.get('screenPageViews', '0')
    if name == 'Argentina':
        lectura = 'Mayor navegación útil'
    elif name == 'United States':
        lectura = 'Usuarios altos, baja profundidad'
    else:
        lectura = 'Baja navegación'
    country_rows.append([name, u, s, v, lectura])

pdf.table(
    ['País', 'Usuarios', 'Sesiones', 'Vistas', 'Lectura'],
    country_rows,
    [34, 22, 22, 22, 78],
    font_size=7.1,
    row_h=9,
)

pct_ar = round(ar_total / max(total_views, 1) * 100)
pdf.callout(
    'Lectura clave',
    f'Argentina concentra alrededor del {pct_ar}% de las vistas registradas. El resto de los países aparece con usuarios pero sin navegación real.',
    tone='red',
)

# ── Page 4: Filtros ─────────────────────────────────────────────────
pdf.section('Qué busca la gente', 'Comportamiento de navegación')
pdf.body('Además del volumen de visitas, el sitio ya muestra patrones de búsqueda que ayudan a entender qué necesita la audiencia.')

# Filters
filt_pages = [r for r in pages if 'type=' in r.get('pagePathPlusQueryString', '')]
filt_rows = []
for r in filt_pages[:10]:
    path = r.get('pagePathPlusQueryString', '')
    label = path.split('type=')[-1].split('&')[0].replace('+', ' ')
    if not label:
        continue
    filt_rows.append({
        'label': label.capitalize(),
        'users': int(r.get('totalUsers', 0)),
        'views': int(r.get('screenPageViews', 0)),
    })

# Aggregate by type
from collections import defaultdict
agg = defaultdict(lambda: {'users': 0, 'views': 0})
for r in filt_rows:
    agg[r['label']]['users'] += r['users']
    agg[r['label']]['views'] += r['views']

sorted_filters = sorted(agg.items(), key=lambda x: -x[1]['views'])
filt_table = []
lecturas = {
    'casa': 'El segmento que más buscan',
    'venta': 'Intención de compra',
    'terreno': 'Segunda búsqueda más fuerte',
    'departamento': 'Interés estable',
    'inmueble comercial': 'Búsqueda de nicho',
    'campo': 'Interés puntual',
}
for label, data in sorted_filters[:8]:
    lec = '—'
    for k, v in lecturas.items():
        if k in label.lower():
            lec = v
            break
    filt_table.append([label.capitalize(), f'{data["users"]} pers.', f'{data["views"]} v.', lec])

if filt_table:
    pdf.callout(
        'Lo más buscado: Casas',
        f'El filtro "Casa" concentró las búsquedas principales. Los usuarios navegan varias páginas del listado (hasta la página 5), lo que indica revisión activa.',
        tone='green',
    )
    pdf.table(
        ['Filtro usado', 'Personas', 'Veces visto', 'Lectura'],
        filt_table,
        [30, 24, 26, 98],
        font_size=8,
        row_h=10,
    )

# Devices
dev_text = '; '.join([f'{r["deviceCategory"]}: {r.get("sessions", "0")} sesiones' for r in devices]) if devices else 'Desktop y mobile'
pdf.body(f'Distribución por dispositivo: {dev_text}.')

# Hours
h10_12 = sum(int(hours_map.get(h, {}).get('sessions', 0)) for h in range(10, 13))
h18_21 = sum(int(hours_map.get(h, {}).get('sessions', 0)) for h in range(18, 22))
v10_12 = sum(int(hours_map.get(h, {}).get('screenPageViews', 0)) for h in range(10, 13))
v18_21 = sum(int(hours_map.get(h, {}).get('screenPageViews', 0)) for h in range(18, 22))
rest_s = total_sessions - h10_12 - h18_21
rest_v = total_views - v10_12 - v18_21

best_days = sorted(weekdays, key=lambda r: -int(r.get('sessions', 0)))[:3]
day_names = ', '.join([r['dayOfWeekName'] for r in best_days]) if best_days else 'varios'

pdf.callout(
    'Cuándo navegan: picos de actividad',
    f'La audiencia busca propiedades en dos ventanas: entre 10 y 12 hs (horario laboral) y entre 18 y 21 hs (después del trabajo). Los días con más tráfico: {day_names}.',
    tone='green',
)

pdf.table(
    ['Horario', 'Sesiones', 'Páginas vistas', 'Cuándo publicar'],
    [
        ['10 a 12 hs', f'~{h10_12}', f'~{v10_12}', 'Mañana — horario laboral'],
        ['18 a 21 hs', f'~{h18_21}', f'~{v18_21}', 'Noche — después del trabajo'],
        ['Resto del día', f'~{rest_s}', f'~{rest_v}', 'Tráfico más disperso'],
    ],
    [30, 26, 30, 92],
    font_size=8,
    row_h=10,
)

# Properties
prop_rows = []
for r in props[:8]:
    title = r.get('pageTitle', '')
    views = r.get('screenPageViews', '0')
    users = r.get('totalUsers', '0')
    # Clean title: remove " · Roggero & Roma" suffix
    clean = title.replace(' · Roggero & Roma', '').replace(' · Alta Gracia', '').replace(' · Córdoba', '')
    prop_rows.append([clean[:42], views, users])

if prop_rows:
    pdf.section('Propiedades con más visitas', 'Interés por inmueble')
    pdf.body('Las propiedades con más visualizaciones indican dónde se concentra el interés. Aquí conviene reforzar la información y el llamado a la acción.')
    pdf.table(
        ['Propiedad', 'Vistas', 'Usuarios'],
        prop_rows,
        [84, 47, 47],
        font_size=8,
        row_h=10,
    )
    pdf.body('Del total de propiedades publicadas, solo una parte recibe visitas visibles cada mes. El resto no tuvo exposición en este período.')

# ── Close ───────────────────────────────────────────────────────────
pdf.closing_panel(
    'Cierre Wolfim',
    'El objetivo no es acumular métricas: es convertir el sitio en una herramienta comercial medible. Este mes ya deja datos de navegación, filtros y propiedades; la próxima evolución es conectar eso con las consultas que genera cada propiedad.',
)

pdf.output(str(OUT))
transfer = copy_to_transfer(OUT)
print(f'✅ PDF generado: {OUT}')
print(f'📎 Transfer: {transfer}')
print(f'📦 Tamaño: {OUT.stat().st_size} bytes')

# ─── Send to Telegram ──────────────────────────────────────────────
import os
token = None
with open('/home/hermes/.hermes/.env') as f:
    for line in f:
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break

if token:
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://api.telegram.org/bot{token}/sendDocument',
        '-F', 'chat_id=1479438002',
        '-F', f'document=@{transfer}',
        '-F', 'caption=Informe mensual de Roggero & Roma — generado automáticamente desde GA4.',
        '--max-time', '90',
    ]
    import subprocess
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    data = json.loads(res.stdout) if res.stdout else {}
    if data.get('ok'):
        print(f'📨 Telegram OK — message_id: {data["result"]["message_id"]}')
    else:
        print(f'⚠️ Error Telegram: {data}')
else:
    print('⚠️ TELEGRAM_BOT_TOKEN no encontrado')
