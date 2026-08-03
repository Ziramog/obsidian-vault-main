from pathlib import Path
import fitz
from PIL import Image, ImageDraw

PROPOSAL = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno/Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-CORREGIDA-v4.pdf')
ANNEX = Path('/home/hermes/.hermes/desktop-attachments/Puerta_al_Infierno_ANEXO_TECNICO_CORREGIDO_V5.pdf')
OUT_DIR = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno')
OUTPUT = OUT_DIR / 'Puerta_al_Infierno_PROPUESTA_INSTITUCIONAL_Y_ANEXO_TECNICO.pdf'

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PAGE_W, PAGE_H = 960, 540
RED = (200 / 255, 16 / 255, 46 / 255)
DARK = (23 / 255, 23 / 255, 23 / 255)
GRAY = (0.40, 0.40, 0.40)
LIGHT_LINE = (216 / 255, 213 / 255, 208 / 255)
CARD_BG = (244, 242, 239, 255)

OUT_DIR.mkdir(parents=True, exist_ok=True)
proposal = fitz.open(PROPOSAL)
annex = fitz.open(ANNEX)
if proposal.page_count != 8:
    raise RuntimeError(f'Expected 8 proposal pages, found {proposal.page_count}')
if annex.page_count != 7:
    raise RuntimeError(f'Expected 7 annex pages, found {annex.page_count}')

combined = fitz.open()

# Preserve the approved proposal exactly.
for i in range(proposal.page_count):
    target = combined.new_page(width=PAGE_W, height=PAGE_H)
    target.show_pdf_page(target.rect, proposal, i)

# Build page 09 as a narrative and visual bridge.
bridge = combined.new_page(width=PAGE_W, height=PAGE_H)
bridge.insert_font(fontname='BridgeRegular', fontfile=FONT_REGULAR)
bridge.insert_font(fontname='BridgeBold', fontfile=FONT_BOLD)

bridge.insert_text(
    fitz.Point(44, 25.1), 'OBRA DE JOSÉ LANDONI',
    fontname='BridgeBold', fontsize=8.6, color=GRAY,
)
bridge.draw_line(fitz.Point(44, 34), fitz.Point(916, 34), color=LIGHT_LINE, width=0.8)

bridge.insert_text(
    fitz.Point(44, 101), 'De la propuesta institucional al desarrollo técnico',
    fontname='BridgeBold', fontsize=27, color=RED,
)
bridge.insert_text(
    fitz.Point(44, 132), 'ANEXO TÉCNICO PRELIMINAR',
    fontname='BridgeBold', fontsize=12.5, color=RED,
)
intro = (
    'La propuesta institucional define el propósito, la experiencia y el valor simbólico de la obra. '
    'El anexo que sigue traduce esa visión en criterios iniciales de geometría, implantación, '
    'estructura, seguridad, durabilidad y documentación para la próxima etapa.'
)
intro_result = bridge.insert_textbox(
    fitz.Rect(44, 158, 916, 224), intro,
    fontname='BridgeRegular', fontsize=12.4, lineheight=1.28, color=DARK,
)
if intro_result < 0:
    raise RuntimeError('Bridge introduction did not fit')

# Rounded cards preserve the visual language used in the proposal.
card_w, card_h, card_y = 276, 132, 252
card_xs = [44, 342, 640]
card_scale = 4
card_image = Image.new('RGBA', (card_w * card_scale, card_h * card_scale), (255, 255, 255, 0))
draw = ImageDraw.Draw(card_image)
draw.rounded_rectangle(
    (0, 0, card_image.width - 1, card_image.height - 1),
    radius=12 * card_scale,
    fill=CARD_BG,
)
draw.rectangle((0, 0, 5 * card_scale, card_image.height), fill=(200, 16, 46, 255))
card_path = OUT_DIR / 'transicion-tarjeta.png'
card_image.save(card_path, 'PNG', optimize=True)

cards = [
    ('01', 'Definir', 'Geometría de referencia, dimensiones e implantación conceptual.'),
    ('02', 'Validar', 'Estructura, fundaciones, montaje, circulación, seguridad y durabilidad.'),
    ('03', 'Preparar', 'Relevamiento, prefactibilidad, presupuesto y proyecto ejecutivo.'),
]
for x, (number, title, description) in zip(card_xs, cards):
    bridge.insert_image(fitz.Rect(x, card_y, x + card_w, card_y + card_h), filename=str(card_path))
    bridge.insert_text(
        fitz.Point(x + 20, card_y + 37), number,
        fontname='BridgeBold', fontsize=22, color=RED,
    )
    bridge.insert_text(
        fitz.Point(x + 65, card_y + 34), title,
        fontname='BridgeBold', fontsize=12.5, color=DARK,
    )
    result = bridge.insert_textbox(
        fitz.Rect(x + 65, card_y + 51, x + card_w - 18, card_y + card_h - 15),
        description,
        fontname='BridgeRegular', fontsize=10.2, lineheight=1.25, color=DARK,
    )
    if result < 0:
        raise RuntimeError(f'Bridge card text did not fit: {title}')

bridge.insert_text(
    fitz.Point(44, 432), 'Alcance del anexo',
    fontname='BridgeBold', fontsize=12.5, color=RED,
)
bridge.insert_textbox(
    fitz.Rect(44, 444, 880, 485),
    'Documento de desarrollo preliminar. Las cotas y soluciones deberán verificarse mediante '
    'relevamiento, memoria de cálculo y documentación ejecutiva.',
    fontname='BridgeRegular', fontsize=10.5, lineheight=1.25, color=DARK,
)
bridge.insert_text(
    fitz.Point(808.03, 524.0), 'PUERTA AL INFIERNO | 09',
    fontname='BridgeRegular', fontsize=8.4, color=GRAY,
)

# Append annex content pages 10 onward, replacing its redundant/defective cover.
# Normalize page size and unify the headers with the approved proposal.
for annex_index in range(1, annex.page_count):
    target = combined.new_page(width=PAGE_W, height=PAGE_H)
    target.show_pdf_page(target.rect, annex, annex_index)
    # Cover the complete raster header, including antialiased remnants at the upper-right,
    # then rebuild the unified header and divider line.
    target.draw_rect(fitz.Rect(0, 0, PAGE_W, 38), color=None, fill=(1, 1, 1), overlay=True)
    target.draw_line(fitz.Point(44, 34), fitz.Point(916, 34), color=LIGHT_LINE, width=0.8, overlay=True)
    target.insert_font(fontname='AnnexHeaderBold', fontfile=FONT_BOLD)
    target.insert_text(
        fitz.Point(44, 25.1), 'OBRA DE JOSÉ LANDONI',
        fontname='AnnexHeaderBold', fontsize=8.6, color=GRAY, overlay=True,
    )

combined.set_metadata({
    'title': 'Puerta al Infierno — Propuesta institucional y anexo técnico',
    'author': 'José Landoni',
    'subject': 'Propuesta institucional integrada con anexo técnico preliminar',
})
combined.save(OUTPUT, garbage=4, deflate=True, clean=True)
combined.close()
proposal.close()
annex.close()

print(OUTPUT)
