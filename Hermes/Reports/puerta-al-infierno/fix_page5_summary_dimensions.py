from io import BytesIO
from pathlib import Path
import fitz
from PIL import Image

SRC = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno/Puerta_al_Infierno_PROPUESTA_Y_ANEXO_DIMENSIONES_CORREGIDAS.pdf')
OUT = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno/Puerta_al_Infierno_PROPUESTA_Y_ANEXO_DIMENSIONES_CORREGIDAS_V2.pdf')
ASSET_DIR = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno')
BACKGROUND_PATH = ASSET_DIR / 'hoja-05-fondo-original.jpg'

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
WHITE = (1, 1, 1)
RED = (200 / 255, 16 / 255, 46 / 255)
PAGE_W, PAGE_H = 960, 540


def centered_x(font: fitz.Font, text: str, fontsize: float, x0: float, x1: float) -> float:
    width = font.text_length(text, fontsize=fontsize)
    if width > (x1 - x0):
        raise RuntimeError(f'Text too wide for block: {text} ({width:.1f} > {x1-x0:.1f})')
    return x0 + ((x1 - x0) - width) / 2


doc = fitz.open(SRC)
if doc.page_count != 15:
    raise RuntimeError(f'Expected 15 pages, found {doc.page_count}')

old_page = doc[4]
image_info = next(
    info for info in old_page.get_image_info(xrefs=True)
    if tuple(round(v, 2) for v in info['bbox']) == (0.0, 0.0, 960.0, 540.0)
)
raw = doc.extract_image(image_info['xref'])['image']
BACKGROUND_PATH.write_bytes(raw)

# Insert the corrected page before the old page 5, then delete the old one.
page = doc.new_page(pno=4, width=PAGE_W, height=PAGE_H)
page.insert_image(page.rect, filename=str(BACKGROUND_PATH), overlay=True)
page.draw_rect(
    fitz.Rect(0, 448, PAGE_W, PAGE_H),
    color=None,
    fill=(0, 0, 0),
    fill_opacity=0.68,
    overlay=True,
)
page.insert_font(fontname='Page5Regular', fontfile=FONT_REGULAR)
page.insert_font(fontname='Page5Bold', fontfile=FONT_BOLD)

# Original caption retained.
page.insert_text(
    fitz.Point(40, 482),
    'Vista aérea frontal - acceso exterior propuesto',
    fontname='Page5Regular', fontsize=15.5, color=WHITE,
)
page.insert_text(
    fitz.Point(42, 514),
    'Fotomontaje conceptual con forma escultórica ajustada a la maqueta original.',
    fontname='Page5Regular', fontsize=9.0, color=WHITE,
)

font_regular = fitz.Font(fontfile=FONT_REGULAR)
font_bold = fitz.Font(fontfile=FONT_BOLD)
blocks = [
    (688, 814, '11,919 m', 'ALTURA MÁXIMA'),
    (822, 950, '14,033 m', 'ANCHO MÁXIMO'),
]
for x0, x1, value, label in blocks:
    value_size = 23.0
    label_size = 8.7
    page.insert_text(
        fitz.Point(centered_x(font_bold, value, value_size, x0, x1), 491),
        value,
        fontname='Page5Bold', fontsize=value_size, color=RED,
    )
    page.insert_text(
        fitz.Point(centered_x(font_regular, label, label_size, x0, x1), 508),
        label,
        fontname='Page5Regular', fontsize=label_size, color=WHITE,
    )
    page.draw_line(fitz.Point(x0, 518), fitz.Point(x1, 518), color=WHITE, width=0.7)

# After insertion, the old page 5 moved to index 5.
doc.delete_page(5)
doc.set_metadata({**doc.metadata, 'title': 'Puerta al Infierno — Propuesta y anexo con dimensiones corregidas V2'})
doc.save(OUT, garbage=4, deflate=True, clean=True)
doc.close()
print(OUT)
