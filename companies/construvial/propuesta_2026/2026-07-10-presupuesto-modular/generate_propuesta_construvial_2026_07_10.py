#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.append('/home/hermes/scripts')
from wolfim_report_preset import WolfimReport  # noqa: E402

OUT = Path('/home/hermes/obsidian-vault/Hermes/Reports/propuesta-comercial-construvial-wolfim-2026-07-10.pdf')

WEB_SETUP = 850
WEB_MONTHLY = 49
ADS_SETUP = 250
ADS_MONTHLY = 180
LI_SETUP = 180
LI_MONTHLY = 160
IG_SETUP = 120
IG_MONTHLY = 220
SOCIAL_COMBO = 320
MEDIA_MIN = 300
MEDIA_MAX = 600

RECOMMENDED_SETUP = WEB_SETUP + ADS_SETUP + LI_SETUP
RECOMMENDED_MONTHLY = WEB_MONTHLY + ADS_MONTHLY + LI_MONTHLY
FULL_SETUP = WEB_SETUP + ADS_SETUP + LI_SETUP + IG_SETUP
FULL_MONTHLY_COMBO = WEB_MONTHLY + ADS_MONTHLY + SOCIAL_COMBO

assert RECOMMENDED_SETUP == 1280
assert RECOMMENDED_MONTHLY == 389
assert FULL_SETUP == 1400
assert FULL_MONTHLY_COMBO == 549


def usd(value: int) -> str:
    return f'USD {value:,}'.replace(',', '.')


class ProposalReport(WolfimReport):
    def add_proposal_cover(self, *, title: str, subtitle: str, client: str, validity: str, prepared_for: str, date_label: str):
        self.add_page()
        self.image(str(self.assets['logo_black']), x=16, y=18, w=43)
        self.set_xy(137, 20)
        self.set_draw_color(*self.color('black'))
        self.set_line_width(0.25)
        self.rect(137, 18, 57, 9, 'D')
        self.set_xy(137, 20.6)
        self.set_font('MONO', 'B', 7.0)
        self.set_text_color(*self.color('black'))
        self.cell(57, 4, 'PROPUESTA WOLFIM', align='C')

        self.set_xy(16, 52)
        self.set_font('DISPLAY', 'B', 27)
        self.set_text_color(*self.color('black'))
        self.multi_cell(155, 11.5, title)
        self.ln(2)
        self.set_x(16)
        self.set_font('BODY', '', 10.5)
        self.set_text_color(*self.color('gray_500'))
        self.multi_cell(148, 5.8, subtitle)

        self.ln(7)
        self.set_x(16)
        self.set_font('MONO', '', 7.0)
        self.set_text_color(*self.color('gray_400'))
        self.cell(0, 4, 'WEB  ·  GOOGLE ADS  ·  LINKEDIN  ·  INSTAGRAM')

        y = 126
        self.set_draw_color(*self.color('gray_200'))
        self.set_fill_color(*self.color('white'))
        self.rect(16, y, 178, 39, 'DF')
        self.set_xy(23, y + 7)
        self.meta_line('CLIENTE', client)
        self.meta_line('VIGENCIA', validity)
        self.meta_line('PREPARADO PARA', prepared_for)
        self.meta_line('FECHA', date_label)

        self.set_y(246)
        self.set_font('BODY', '', 8.5)
        self.set_text_color(*self.color('gray_400'))
        self.multi_cell(128, 5.0, 'Una propuesta modular para construir autoridad, captar demanda y medir oportunidades comerciales reales.')
        self.image(str(self.assets['logo_black']), x=151, y=247, w=43)
        self.set_y(270)
        self.set_x(16)
        self.set_font('MONO', '', 6.5)
        self.set_text_color(*self.color('gray_400'))
        self.cell(34, 4, 'B2B INDUSTRIAL')
        self.set_fill_color(*self.color('green'))
        self.ellipse(51.5, 271.2, 1.8, 1.8, 'F')
        self.set_x(56)
        self.cell(0, 4, 'OIL & GAS  ·  MINERÍA  ·  SERVICIOS')

    def module_label(self, number: str, title: str, tag: str):
        self.set_font('MONO', 'B', 7)
        self.set_text_color(*self.color('green'))
        self.cell(0, 5, f'MÓDULO {number} / {tag.upper()}', new_x='LMARGIN', new_y='NEXT')
        self.set_font('DISPLAY', 'B', 18)
        self.set_text_color(*self.color('black'))
        self.multi_cell(0, 8.5, title)
        y = self.get_y() + 1
        self.set_draw_color(*self.color('black'))
        self.line(16, y, 52, y)
        self.set_y(y + 5)


today = date(2026, 7, 10)
valid_until = today + timedelta(days=15)

pdf = ProposalReport(
    report_title='Propuesta comercial modular',
    client_name='Construvial S.A.',
    footer_text='Wolfim Studio · Propuesta comercial · Web y adquisición digital',
)

pdf.add_proposal_cover(
    title='Ecosistema digital premium para Construvial',
    subtitle='Web corporativa B2B, captación mediante Google Ads y presencia institucional en LinkedIn e Instagram, organizadas como módulos independientes.',
    client='Construvial S.A.',
    validity=f'15 días · hasta {valid_until.strftime("%d/%m/%Y")}',
    prepared_for='Dirección de Construvial',
    date_label=today.strftime('%d/%m/%Y'),
)

# Page 2 — commercial logic
pdf.add_page()
pdf.section('Propuesta ejecutiva', 'Estrategia comercial')
pdf.body(
    'Construvial necesita una presencia digital que pueda sostener una conversación con compradores corporativos: explicar capacidades, demostrar experiencia, captar búsquedas con intención y facilitar el contacto. La propuesta evita mezclar todo en un paquete cerrado: cada módulo tiene alcance, inversión y continuidad propios.'
)
pdf.metric_cards([
    ('Web Premium', usd(WEB_SETUP), f'{usd(WEB_MONTHLY)}/mes'),
    ('Google Ads', usd(ADS_SETUP), f'{usd(ADS_MONTHLY)}/mes + medios'),
    ('LinkedIn Empresa', usd(LI_SETUP), f'{usd(LI_MONTHLY)}/mes opcional'),
    ('Instagram Empresa', usd(IG_SETUP), f'{usd(IG_MONTHLY)}/mes opcional'),
], columns=2)
pdf.callout(
    'Recomendación Wolfim',
    'Comenzar con Web Premium + Google Ads + LinkedIn. Ese núcleo cubre autoridad, demanda activa y validación corporativa. Instagram debe acompañar como canal visual en una segunda etapa; no reemplaza los tres activos principales.',
    tone='green',
)
pdf.section('Orden de implementación', 'Secuencia sugerida')
pdf.table(
    ['Etapa', 'Módulo', 'Objetivo', 'Momento'],
    [
        ['1', 'Web Premium', 'Base institucional y comercial', 'Inicio'],
        ['2', 'LinkedIn', 'Validación corporativa', 'En paralelo'],
        ['3', 'Google Ads', 'Captar búsquedas activas', 'Con web lista'],
        ['4', 'Instagram', 'Mostrar actividad y campo', 'Segunda etapa'],
    ],
    [18, 42, 76, 42],
    font_size=7.6,
    row_h=10,
)

# Page 3 — web
pdf.add_page()
pdf.module_label('01', 'Web Premium B2B Industrial', 'Activo comercial central')
pdf.body('Sitio corporativo diseñado para presentar a Construvial ante operadores, contratistas, responsables de compras y potenciales socios de oil & gas, minería e industria.')
pdf.metric_cards([
    ('Inversión inicial', usd(WEB_SETUP), 'pago único'),
    ('Hosting + mantenimiento', f'{usd(WEB_MONTHLY)}/mes', 'sin permanencia'),
    ('Plazo estimado', '4–6 semanas', 'con material completo'),
])
pdf.section('Alcance incluido', 'Diseño + estructura + medición')
pdf.bullets([
    'Diseño visual premium, responsive y alineado a una empresa industrial.',
    'Hasta 8 páginas o secciones: Inicio, Empresa, Servicios, Oil & Gas, Minería, Equipos/Capacidad, Proyectos/antecedentes y Contacto.',
    'Estructura comercial orientada a compradores B2B, no una web institucional genérica.',
    'Adaptación y edición del contenido técnico provisto por Construvial.',
    'WhatsApp, formularios y llamados a la acción visibles.',
    'SEO técnico inicial: títulos, descripciones, indexación, sitemap y estructura semántica.',
    'Integración base de GA4 y Google Tag Manager.',
    'Optimización de velocidad, SSL, seguridad y experiencia mobile.',
    'Carga inicial de imágenes, servicios y antecedentes; hasta 2 rondas de ajustes.',
])
pdf.callout(
    'Hosting y mantenimiento mensual',
    'Incluye hosting administrado, SSL, backups, monitoreo básico, actualizaciones de seguridad, soporte y hasta 60 minutos mensuales de cambios menores. Cuando exista volumen suficiente, se suma un reporte mensual simple de tráfico e interacciones.',
    tone='green',
)
pdf.body('No incluye dominio nuevo, producción fotográfica/audiovisual, traducciones, carga masiva, integraciones especiales ni sistemas internos. Esos alcances se cotizan por separado.', size=8.2, color='gray_400')

# Page 4 — Google Ads
pdf.add_page()
pdf.module_label('02', 'Google Ads B2B', 'Captación de demanda')
pdf.body('Campañas de búsqueda orientadas a personas y empresas que ya están buscando servicios vinculados con oil & gas, minería o soporte industrial en zonas de interés.')
pdf.metric_cards([
    ('Configuración inicial', usd(ADS_SETUP), 'pago único'),
    ('Gestión mensual', f'{usd(ADS_MONTHLY)}/mes', 'optimización + informe'),
    ('Inversión en Google', f'{usd(MEDIA_MIN)}–{usd(MEDIA_MAX)}/mes', 'pago directo a Google'),
])
pdf.section('Alcance incluido', 'Campañas + conversiones')
pdf.bullets([
    'Revisión o creación de la cuenta publicitaria.',
    'Investigación de búsquedas por servicio, industria y zona geográfica.',
    'Hasta 2 campañas iniciales: Oil & Gas y Minería/Servicios industriales.',
    'Grupos de anuncios, palabras clave, negativas y segmentación geográfica.',
    'Redacción y carga de anuncios responsivos.',
    'Configuración de conversiones disponibles: formularios, WhatsApp y llamadas.',
    'Parámetros UTM y conexión con GA4.',
    'Optimización semanal de términos de búsqueda, presupuesto, anuncios y ubicaciones.',
    'Informe mensual Wolfim: inversión, consultas, costo por contacto y acciones recomendadas.',
])
pdf.callout(
    'Separación clara de costos',
    'Los honorarios de Wolfim no incluyen el consumo publicitario. Google factura el presupuesto de medios directamente a Construvial. No se garantizan posiciones, consultas ni ventas; la gestión busca mejorar relevancia, medición y eficiencia con datos reales.',
    tone='green',
)
pdf.body('Lanzamiento estimado: 7 a 10 días hábiles después de contar con web, accesos, medios de pago y material aprobado.', size=8.4, color='gray_400')

# Page 5 — social modules
pdf.add_page()
pdf.module_label('03', 'LinkedIn Empresa', 'Autoridad corporativa')
pdf.body('Canal prioritario para una empresa B2B industrial: valida capacidades, experiencia, sectores atendidos y actividad frente a decisores corporativos.')
pdf.metric_cards([
    ('Creación / optimización', usd(LI_SETUP), 'pago único'),
    ('Gestión opcional', f'{usd(LI_MONTHLY)}/mes', '4 publicaciones'),
    ('Puesta en marcha', '5 días hábiles', 'con material completo'),
])
pdf.bullets([
    'Página empresa, portada, descripción institucional, especialidades, ubicación y contacto.',
    'Propuesta de valor B2B y palabras clave por sector.',
    'Plantilla visual y publicación inicial de presentación.',
    'Gestión opcional: calendario, redacción, diseño y 4 publicaciones mensuales.',
    'No incluye prospección uno a uno, inbox, perfiles personales ni LinkedIn Ads.',
])

pdf.module_label('04', 'Instagram Empresa', 'Presencia visual')
pdf.body('Canal complementario para mostrar obras, equipos, procesos, seguridad y cultura de trabajo. Debe apoyarse en material real de campo.')
pdf.metric_cards([
    ('Configuración inicial', usd(IG_SETUP), 'pago único'),
    ('Gestión opcional', f'{usd(IG_MONTHLY)}/mes', '8 piezas combinadas'),
    ('Puesta en marcha', '5 días hábiles', 'con material completo'),
])
pdf.bullets([
    'Perfil comercial, biografía, enlaces, destacados y estructura visual.',
    'Vinculación con Meta Business cuando corresponda.',
    'Plantillas base para publicaciones e historias.',
    'Gestión opcional: 8 piezas mensuales, redacción, diseño y programación.',
    'No incluye filmación, fotografía en obra, community management diario ni campañas pagas.',
])

# Page 6 — investment and close
pdf.add_page()
pdf.section('Inversión modular', 'Resumen comercial')
pdf.table(
    ['Módulo', 'Puesta en marcha', 'Mensual Wolfim', 'Medios'],
    [
        ['1. Web Premium', usd(WEB_SETUP), usd(WEB_MONTHLY), '—'],
        ['2. Google Ads', usd(ADS_SETUP), usd(ADS_MONTHLY), f'{usd(MEDIA_MIN)}–{usd(MEDIA_MAX)}'],
        ['3. LinkedIn', usd(LI_SETUP), f'{usd(LI_MONTHLY)} opcional', '—'],
        ['4. Instagram', usd(IG_SETUP), f'{usd(IG_MONTHLY)} opcional', '—'],
    ],
    [49, 43, 46, 40],
    font_size=7.5,
    row_h=10,
)
pdf.section('Plan recomendado', 'Web + Google Ads + LinkedIn')
pdf.metric_cards([
    ('Inversión inicial', usd(RECOMMENDED_SETUP), 'tres módulos'),
    ('Mensual Wolfim', f'{usd(RECOMMENDED_MONTHLY)}/mes', 'web + ads + LinkedIn'),
    ('Medios sugeridos', f'{usd(MEDIA_MIN)}–{usd(MEDIA_MAX)}/mes', 'pago directo a Google'),
])
pdf.callout(
    'Ecosistema completo',
    f'Los cuatro módulos suman {usd(FULL_SETUP)} de puesta en marcha. Contratando juntas las gestiones de LinkedIn e Instagram, el bloque de contenidos queda en {usd(SOCIAL_COMBO)}/mes y el total mensual Wolfim en {usd(FULL_MONTHLY_COMBO)}/mes, más la inversión publicitaria.',
    tone='green',
)
pdf.callout(
    'Condiciones de contratación',
    'Módulos separables. Puesta en marcha: 50% al iniciar y 50% antes de activar. Mensualidades por adelantado desde la activación. Valores en USD o ARS al tipo de cambio acordado. Construvial designará un responsable; cambios de alcance y producción adicional se cotizan aparte.',
    tone='black',
)
pdf.closing_panel(
    'Próximo paso',
    'Elegir los módulos de la primera etapa, confirmar responsables y materiales, aprobar la propuesta y coordinar la reunión de inicio. Wolfim recomienda comenzar por Web Premium + Google Ads + LinkedIn.',
)

pdf.output(str(OUT))
print(OUT)
print(f'pages={pdf.page_no()}')
print(f'bytes={OUT.stat().st_size}')
print(f'recommended_setup={RECOMMENDED_SETUP}')
print(f'recommended_monthly={RECOMMENDED_MONTHLY}')
print(f'full_setup={FULL_SETUP}')
print(f'full_monthly_combo={FULL_MONTHLY_COMBO}')
