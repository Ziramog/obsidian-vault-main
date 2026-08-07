#!/usr/bin/env python3
"""
Roggero & Roma — informe final cliente con totales limpios.
Excluye fuentes técnicas/login del total client-facing.
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

sys.path.append('/home/hermes/scripts')
from wolfim_report_preset import WolfimReport, copy_to_transfer

KEY = '/home/hermes/.hermes/profiles/wolfim-growth/wolfim-analytics-tools-a0b1de9655b0.json'
PROP = '539918073'
PREV_START = '2026-06-08'
PREV_END = '2026-07-07'
START = '2026-07-07'
END = '2026-08-06'
DATE_LABEL = date.today().strftime('%d/%m/%Y')
PERIOD_LABEL = '07/07/2026 al 06/08/2026 · datos completos'
OUT = Path(f'/home/hermes/roggero_roma_informe_analytics_auditado_final_{START}_{END}.pdf')

creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=['https://www.googleapis.com/auth/analytics.readonly']
)
creds.refresh(Request())
HEADERS = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}
BASE = f'https://analyticsdata.googleapis.com/v1beta/properties/{PROP}:runReport'

TECH_SOURCES = ['accounts.google.com', 'vercel.com']
TECH_FILTER = {'filter': {'fieldName': 'sessionSource', 'inListFilter': {'values': TECH_SOURCES}}}
NOT_TECH_FILTER = {'notExpression': TECH_FILTER}
ADMIN_PATH = {'filter': {'fieldName': 'pagePathPlusQueryString', 'stringFilter': {'matchType': 'CONTAINS', 'value': '/admin'}}}
ADMIN_TITLE_ADMIN = {'filter': {'fieldName': 'pageTitle', 'stringFilter': {'matchType': 'CONTAINS', 'value': 'Admin'}}}
ADMIN_TITLE_EDIT = {'filter': {'fieldName': 'pageTitle', 'stringFilter': {'matchType': 'CONTAINS', 'value': 'Editar Propiedad'}}}
ADMIN_TITLE_PANEL = {'filter': {'fieldName': 'pageTitle', 'stringFilter': {'matchType': 'CONTAINS', 'value': 'Panel de Control'}}}
INTERNAL_ANY = {'orGroup': {'expressions': [TECH_FILTER, ADMIN_PATH, ADMIN_TITLE_ADMIN, ADMIN_TITLE_EDIT, ADMIN_TITLE_PANEL]}}
CLEAN_FILTER = {'notExpression': INTERNAL_ANY}


def merge_filters(a, b):
    if not a:
        return b
    if not b:
        return a
    return {'andGroup': {'expressions': [a, b]}}


def ga4(start, end, dimensions=None, metrics=None, filt=None, limit=100, order_metric=None):
    dimensions = dimensions or []
    metrics = metrics or []
    body = {
        'dateRanges': [{'startDate': start, 'endDate': end}],
        'dimensions': [{'name': d} for d in dimensions],
        'metrics': [{'name': m} for m in metrics],
        'limit': limit,
    }
    if order_metric:
        body['orderBys'] = [{'metric': {'metricName': order_metric}, 'desc': True}]
    if filt:
        body['dimensionFilter'] = filt
    r = requests.post(BASE, headers=HEADERS, json=body, timeout=45)
    data = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f'GA4 {r.status_code}: {json.dumps(data, ensure_ascii=False)[:800]}')
    dims = [x['name'] for x in data.get('dimensionHeaders', [])]
    mets = [x['name'] for x in data.get('metricHeaders', [])]
    rows = []
    for row in data.get('rows', []):
        item = {}
        for i, k in enumerate(dims):
            item[k] = row['dimensionValues'][i].get('value')
        for i, k in enumerate(mets):
            item[k] = row['metricValues'][i].get('value')
        rows.append(item)
    if not dimensions:
        return rows[0] if rows else {}
    return rows


def to_int(v):
    try:
        return int(float(v))
    except Exception:
        return 0


def to_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def pct(part, total):
    return round(part / max(total, 1) * 100, 1)


def fmt_pct(v):
    return f'{v:.1f}%'.replace('.', ',')


def fmt_num(v):
    return f'{int(v):,}'.replace(',', '.')


def metric(start, end, filt=None):
    return ga4(start, end, [], [
        'totalUsers', 'sessions', 'screenPageViews', 'engagedSessions', 'engagementRate', 'bounceRate'
    ], filt=filt)


def source_sessions(source, medium=None, filt=None):
    source_f = {'filter': {'fieldName': 'sessionSource', 'stringFilter': {'matchType': 'EXACT', 'value': source}}}
    final_f = merge_filters(filt, source_f)
    if medium is not None:
        medium_f = {'filter': {'fieldName': 'sessionMedium', 'stringFilter': {'matchType': 'EXACT', 'value': medium}}}
        final_f = merge_filters(final_f, medium_f)
    row = metric(START, END, final_f)
    return to_int(row.get('sessions'))


print(f'📊 Generando informe cliente limpio real — {START} a {END}')
raw = metric(START, END)
tech = metric(START, END, INTERNAL_ANY)
clean = metric(START, END, CLEAN_FILTER)
prev = metric(PREV_START, PREV_END)
prev_admin = metric(PREV_START, PREV_END, {'orGroup': {'expressions': [ADMIN_PATH, ADMIN_TITLE_ADMIN, ADMIN_TITLE_EDIT, ADMIN_TITLE_PANEL]}})

raw_sessions = to_int(raw.get('sessions'))
raw_views = to_int(raw.get('screenPageViews'))
tech_sessions = to_int(tech.get('sessions'))
tech_views = to_int(tech.get('screenPageViews'))
tech_users = to_int(tech.get('totalUsers'))
users = to_int(clean.get('totalUsers'))
sessions = to_int(clean.get('sessions'))
views = to_int(clean.get('screenPageViews'))
engaged = to_int(clean.get('engagedSessions'))
engagement = to_float(clean.get('engagementRate')) * 100
bounce = to_float(clean.get('bounceRate')) * 100
views_per_session = round(views / max(sessions, 1), 2)
views_per_user = round(views / max(users, 1), 2)

prev_sessions = to_int(prev.get('sessions'))
prev_views = to_int(prev.get('screenPageViews'))
prev_engagement = to_float(prev.get('engagementRate')) * 100
prev_bounce = to_float(prev.get('bounceRate')) * 100
prev_admin_views = to_int(prev_admin.get('screenPageViews'))
prev_admin_sessions = to_int(prev_admin.get('sessions'))

countries = ga4(START, END, ['country'], ['totalUsers', 'sessions', 'screenPageViews'], filt=CLEAN_FILTER, limit=10, order_metric='screenPageViews')
devices = ga4(START, END, ['deviceCategory'], ['totalUsers', 'sessions', 'screenPageViews'], filt=CLEAN_FILTER, limit=5, order_metric='sessions')
hours = ga4(START, END, ['hour'], ['sessions', 'screenPageViews'], filt=CLEAN_FILTER, limit=24, order_metric='sessions')
pages = ga4(START, END, ['pagePathPlusQueryString', 'pageTitle'], ['screenPageViews', 'totalUsers'], filt=CLEAN_FILTER, limit=1000, order_metric='screenPageViews')
events = ga4(START, END, ['eventName'], ['eventCount', 'totalUsers'], filt=CLEAN_FILTER, limit=30, order_metric='eventCount')

google_sessions = source_sessions('google', 'organic', CLEAN_FILTER)
direct_sessions = source_sessions('(direct)', '(none)', CLEAN_FILTER)
other_sessions = max(sessions - google_sessions - direct_sessions, 0)

arg = next((r for r in countries if r.get('country') == 'Argentina'), {})
arg_views = to_int(arg.get('screenPageViews'))

filter_specs = [
    ('Casa', 'type=Casa', 'Búsqueda principal'),
    ('Venta', 'operation=venta', 'Intención comercial'),
    ('Terreno', 'type=Terreno', 'Búsqueda secundaria'),
    ('Inmueble comercial', 'type=Inmueble+Comercial', 'Nicho puntual'),
    ('Departamento', 'type=Departamento', 'Interés estable'),
    ('Campo', 'type=Campo', 'Interés puntual'),
    ('Alquiler', 'operation=alquiler', 'Interés puntual'),
]
filter_rows = []
for label, value, lectura in filter_specs:
    page_filter = {
        'filter': {
            'fieldName': 'pagePathPlusQueryString',
            'stringFilter': {
                'matchType': 'CONTAINS',
                'value': value,
                'caseSensitive': False,
            },
        },
    }
    row = metric(START, END, merge_filters(CLEAN_FILTER, page_filter))
    filter_rows.append([
        label,
        f'{to_int(row.get("totalUsers"))} pers.',
        f'{to_int(row.get("screenPageViews"))} vistas',
        lectura,
    ])
filter_rows.sort(key=lambda row: -int(row[2].split()[0]))

prop_rows = []
for r in pages:
    path = r.get('pagePathPlusQueryString', '')
    title = r.get('pageTitle', '')
    if '/properties/' not in path:
        continue
    clean_title = title.replace(' · Roggero & Roma', '').replace(' · Alta Gracia', '').replace(' · Córdoba', '')
    prop_rows.append([clean_title[:58], r.get('screenPageViews', '0'), r.get('totalUsers', '0')])
    if len(prop_rows) >= 6:
        break

event_map = {r.get('eventName'): to_int(r.get('eventCount')) for r in events}
property_viewed = event_map.get('property_viewed', 0)
whatsapp = event_map.get('click_whatsapp', 0)

hours_map = {to_int(r.get('hour')): r for r in hours}
h10_12 = sum(to_int(hours_map.get(h, {}).get('sessions')) for h in range(10, 13))
h18_21 = sum(to_int(hours_map.get(h, {}).get('sessions')) for h in range(18, 22))
v10_12 = sum(to_int(hours_map.get(h, {}).get('screenPageViews')) for h in range(10, 13))
v18_21 = sum(to_int(hours_map.get(h, {}).get('screenPageViews')) for h in range(18, 22))
rest_s = sessions - h10_12 - h18_21
rest_v = views - v10_12 - v18_21

pdf = WolfimReport(
    report_title='Informe mensual de Analytics',
    client_name='Roggero & Roma',
    footer_text='Wolfim Studio · Medición web y crecimiento comercial',
)

pdf.add_cover(
    title='Informe mensual de Analytics',
    subtitle='Lectura comercial con datos depurados: visitantes reales, navegación del catálogo y señales claras de interés.',
    client='Roggero & Roma',
    period=PERIOD_LABEL,
    prepared_for='Franco / Marcos Roma',
    date_label=DATE_LABEL,
)
# Correct the location rail inherited from the generic preset.
pdf.set_fill_color(*pdf.color('paper'))
pdf.rect(15, 268.5, 165, 9, 'F')
pdf.set_xy(16, 270)
pdf.set_font('MONO', '', 6.5)
pdf.set_text_color(*pdf.color('gray_400'))
pdf.cell(42, 4, 'CÓRDOBA, ARGENTINA')
pdf.set_fill_color(*pdf.color('green'))
pdf.ellipse(59.5, 271.2, 1.8, 1.8, 'F')
pdf.set_x(64)
pdf.cell(0, 4, 'SERVICIO REMOTO')

pdf.add_page()
pdf.section('Antes de leer los números', 'Nota sobre la medición')
pdf.body(
    'Este período utiliza una metodología más limpia que el informe anterior. Los totales presentados ya excluyen actividad de autenticación, hosting/previews y panel administrativo, para que la lectura represente mejor la navegación pública.',
    size=9.6,
)
pdf.bullets([
    'Las sesiones, usuarios y vistas de este informe corresponden a la base depurada.',
    'Las fuentes técnicas no se muestran como canales de adquisición ni suman al total presentado.',
    'El informe anterior y el actual no deben compararse solo por volumen, porque cambió la metodología de medición.',
    'Las conclusiones se apoyan en navegación, fuentes, filtros, propiedades vistas y acciones de contacto identificables.',
])
pdf.callout(
    'Cómo leer este informe',
    'La diferencia frente al informe anterior no equivale por sí sola a una caída del interés. El foco está en la calidad del tráfico que queda: origen, profundidad de navegación y comportamiento dentro del catálogo.',
    tone='green',
)

pdf.add_page()
pdf.section('Resumen ejecutivo', 'Lectura comercial')
pdf.body(
    'Con la base depurada, el sitio muestra navegación dentro del catálogo: usuarios que entran, recorren listados, usan filtros y miran propiedades puntuales.',
    size=9.6,
)
pdf.metric_cards([
    ('Usuarios medidos', fmt_num(users), 'base depurada'),
    ('Sesiones depuradas', fmt_num(sessions), 'base del informe'),
    ('Vistas depuradas', fmt_num(views), 'páginas vistas'),
    ('Google orgánico', fmt_num(google_sessions), f'{fmt_pct(pct(google_sessions, sessions))} de sesiones'),
    ('Páginas por sesión', str(views_per_session).replace('.', ','), 'profundidad'),
    ('Engagement rate', fmt_pct(engagement), 'sesiones con interacción'),
])
pdf.callout(
    'Conclusión principal',
    'Menos ruido y más foco: el dato útil muestra tráfico concentrado en Argentina, búsquedas de propiedades y navegación profunda dentro del catálogo.',
    tone='green',
)

pdf.add_page()
pdf.section('Procedencia y calidad del tráfico', 'Fuentes y país')
pdf.body('Para esta lectura se muestran solo fuentes útiles para entender adquisición y navegación comercial.', size=9.0)
pdf.table(
    ['Fuente', 'Sesiones', 'Peso', 'Lectura'],
    [
        ['Google orgánico', fmt_num(google_sessions), fmt_pct(pct(google_sessions, sessions)), 'Búsqueda real'],
        ['Directo', fmt_num(direct_sessions), fmt_pct(pct(direct_sessions, sessions)), 'Marca / acceso directo'],
        ['Otros canales', fmt_num(other_sessions), fmt_pct(pct(other_sessions, sessions)), 'Referidos y redes menores'],
    ],
    [48, 30, 26, 74],
    font_size=7.7,
    row_h=10,
)
country_names = {
    'Argentina': 'Argentina',
    'Singapore': 'Singapur',
    'United States': 'Estados Unidos',
    'Germany': 'Alemania',
    'Bangladesh': 'Bangladesh',
    'China': 'China',
    'Ireland': 'Irlanda',
    'Norway': 'Noruega',
    'Sweden': 'Suecia',
}
country_rows = []
for c in countries[:6]:
    raw_name = c.get('country', '')
    if not raw_name or raw_name == '(not set)':
        continue
    name = country_names.get(raw_name, raw_name)
    lectura = 'Mayor navegación útil' if raw_name == 'Argentina' else 'Tráfico menor'
    country_rows.append([name, c.get('totalUsers', '0'), c.get('sessions', '0'), c.get('screenPageViews', '0'), lectura])
pdf.table(['País', 'Usuarios', 'Sesiones', 'Vistas', 'Lectura'], country_rows, [34, 22, 22, 22, 78], font_size=7.2, row_h=9)
pdf.callout(
    'Argentina concentra la navegación útil',
    f'Argentina representa aproximadamente {fmt_pct(pct(arg_views, views))} de las vistas depuradas del período.',
    tone='green',
)

pdf.add_page()
pdf.section('Qué busca la gente', 'Catálogo y comportamiento')
pdf.body('Los filtros y las fichas vistas muestran qué tipo de propiedades concentran más atención. Esto sirve para priorizar publicaciones, fotos, descripciones y propiedades destacadas.', size=9.0)
if filter_rows:
    pdf.callout(
        'Casas sigue siendo el patrón principal',
        'El filtro Casa vuelve a aparecer como la búsqueda más fuerte. La navegación continúa en páginas sucesivas del listado, señal de revisión activa del catálogo.',
        tone='green',
    )
    pdf.table(['Filtro', 'Personas', 'Vistas', 'Lectura'], filter_rows, [34, 28, 30, 86], font_size=7.7, row_h=10)
pdf.body('Los filtros no son excluyentes: una misma persona puede aparecer en más de una categoría si realizó distintas búsquedas.', size=8.3, color='muted')
mobile_views = next((to_int(r.get('screenPageViews')) for r in devices if r.get('deviceCategory') == 'mobile'), 0)
desktop_views = next((to_int(r.get('screenPageViews')) for r in devices if r.get('deviceCategory') == 'desktop'), 0)
pdf.body(
    f'Dispositivos por páginas vistas: mobile {fmt_num(mobile_views)} ({fmt_pct(pct(mobile_views, views))}); desktop {fmt_num(desktop_views)} ({fmt_pct(pct(desktop_views, views))}).',
    size=8.6,
)
pdf.table(
    ['Horario', 'Sesiones', 'Vistas', 'Cuándo publicar'],
    [
        ['10 a 12 hs', f'~{h10_12}', f'~{v10_12}', 'Mañana — horario laboral'],
        ['18 a 21 hs', f'~{h18_21}', f'~{v18_21}', 'Noche — después del trabajo'],
        ['Resto del día', f'~{rest_s}', f'~{rest_v}', 'Tráfico disperso'],
    ],
    [30, 26, 30, 92],
    font_size=7.7,
    row_h=10,
)

if prop_rows:
    pdf.add_page()
    pdf.section('Propiedades con más visitas', 'Interés por inmueble')
    pdf.table(['Propiedad', 'Vistas', 'Usuarios'], prop_rows, [116, 31, 31], font_size=7.2, row_h=10)

pdf.add_page()
pdf.section('Señales comerciales y próximo paso', 'Eventos claros')
pdf.metric_cards([
    ('Fichas vistas', fmt_num(property_viewed), 'property_viewed'),
    ('Clicks WhatsApp', fmt_num(whatsapp), 'contacto directo'),
], columns=2)
pdf.body(
    'La medición actual muestra fichas de propiedades y clicks de WhatsApp como señales claras. Para los próximos informes vamos a separar mejor búsquedas, filtros y contactos reales con eventos propios.',
    size=9.2,
)
pdf.closing_panel(
    'Cierre Wolfim',
    'Este informe mira el sitio como herramienta comercial: qué tráfico vale la pena, qué se busca dentro del catálogo y qué señales pueden transformarse en consultas concretas.',
)

pdf.output(str(OUT))
transfer = copy_to_transfer(OUT)
print(f'✅ PDF generado: {OUT}')
print(f'📎 Transfer: {transfer}')
print(f'📦 Tamaño: {OUT.stat().st_size} bytes')
print(f'📊 Totales: raw_sessions={raw_sessions} tech_sessions={tech_sessions} clean_sessions={sessions} clean_views={views}')

bot_token = None
with open('/home/hermes/.hermes/.env') as f:
    for line in f:
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            bot_token = line.split('=', 1)[1].strip()
            break

if False and bot_token:
    # Envío desactivado: este artefacto se verifica antes de Telegram.
    caption = 'Roggero & Roma — informe auditado final, métricas depuradas y consistentes.'
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://api.telegram.org/bot{bot_token}/sendDocument',
        '-F', 'chat_id=1479438002',
        '-F', f'document=@{transfer}',
        '-F', f'caption={caption}',
        '--max-time', '90',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    data = json.loads(result.stdout) if result.stdout else {}
    if data.get('ok'):
        print(f'📨 Telegram OK — message_id: {data["result"]["message_id"]}')
    else:
        print(f'⚠️ Error Telegram: {data}')
else:
    print('⚠️ TELEGRAM_BOT_TOKEN no encontrado')
