from pathlib import Path
import fitz
from PIL import Image

SRC = Path('/home/hermes/.hermes/desktop-attachments/Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-2.pdf')
SHIELD_SRC = Path('/home/hermes/.hermes/desktop-attachments/Escudo_del_Club_Atlético_Independiente.svg-2.webp')
OUT_DIR = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno')
OUT_PDF = OUT_DIR / 'Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-CORREGIDA.pdf'
SHIELD_PNG = OUT_DIR / 'escudo-independiente-recortado.png'

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Preserve transparency and trim the tiny transparent margin of the supplied shield.
shield = Image.open(SHIELD_SRC).convert('RGBA')
alpha_bbox = shield.getchannel('A').getbbox()
if alpha_bbox:
    shield = shield.crop(alpha_bbox)
shield.save(SHIELD_PNG, 'PNG', optimize=True)

doc = fitz.open(SRC)
if doc.page_count != 8:
    raise RuntimeError(f'Expected the supplied file to have 8 pages, found {doc.page_count}')

# Cover: reduced artist credit directly below the four-line proposal.
cover = doc[0]
cover.insert_font(fontname='DejaVuSansCredit', fontfile=FONT_REGULAR)
cover.insert_text(
    fitz.Point(50, 451),
    'Artista: José Landoni',
    fontname='DejaVuSansCredit',
    fontsize=8.0,
    color=(1, 1, 1),
    overlay=True,
)

# First interior sheet: use the supplied shield and keep the artist credit only in the header.
page1 = doc[1]
page1.insert_font(fontname='DejaVuSansHeaderBold', fontfile=FONT_BOLD)
page1.insert_text(
    fitz.Point(705, 25.1),
    'OBRA DE JOSÉ LANDONI',
    fontname='DejaVuSansHeaderBold',
    fontsize=8.0,
    color=(0.40, 0.40, 0.40),
    overlay=True,
)
page1.insert_image(
    fitz.Rect(882, 5.0, 904, 28.2),
    filename=str(SHIELD_PNG),
    keep_proportion=True,
    overlay=True,
)

# The supplied file already ends at page 08; no page 09 exists to retain.
doc.set_metadata({**doc.metadata, 'title': 'Puerta al Infierno — Presentación institucional corregida'})
doc.save(OUT_PDF, garbage=4, deflate=True, clean=True)
doc.close()

print(OUT_PDF)
