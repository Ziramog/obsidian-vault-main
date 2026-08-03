from io import BytesIO
from pathlib import Path
import fitz
from PIL import Image

SRC = Path('/home/hermes/.hermes/desktop-attachments/Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-2.pdf')
SHIELD_SRC = Path('/home/hermes/.hermes/desktop-attachments/Escudo_del_Club_Atlético_Independiente.svg-2.webp')
OUT_DIR = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno')
OUT_PDF = OUT_DIR / 'Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-CORREGIDA-v2.pdf'
SHIELD_PNG = OUT_DIR / 'escudo-independiente-recortado.png'
BACKGROUND_PATCH = OUT_DIR / 'portada-fondo-restaurado.png'

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Prepare the supplied official shield, preserving transparency and removing only empty margins.
shield = Image.open(SHIELD_SRC).convert('RGBA')
alpha_bbox = shield.getchannel('A').getbbox()
if alpha_bbox:
    shield = shield.crop(alpha_bbox)
shield.save(SHIELD_PNG, 'PNG', optimize=True)

doc = fitz.open(SRC)
if doc.page_count != 8:
    raise RuntimeError(f'Expected 8 pages in the supplied PDF, found {doc.page_count}')

cover = doc[0]

# Restore the photo under the old simplified C.A.I. mark before placing the supplied shield.
# The original page uses a full-page 1920x1080 image mapped to 960x540 pt and a 68% black overlay
# over the left 360 pt. Recreate that exact background in a small surgical patch.
image_info = cover.get_image_info(xrefs=True)
background = next(info for info in image_info if tuple(info['bbox']) == (0.0, 0.0, 960.0, 540.0))
raw = doc.extract_image(background['xref'])['image']
photo = Image.open(BytesIO(raw)).convert('RGB')
patch_rect = fitz.Rect(48, 118, 138, 220)
scale_x = photo.width / cover.rect.width
scale_y = photo.height / cover.rect.height
crop_box = (
    round(patch_rect.x0 * scale_x),
    round(patch_rect.y0 * scale_y),
    round(patch_rect.x1 * scale_x),
    round(patch_rect.y1 * scale_y),
)
patch = photo.crop(crop_box)
patch = Image.blend(patch, Image.new('RGB', patch.size, (0, 0, 0)), 0.68)
patch.save(BACKGROUND_PATCH, 'PNG', optimize=True)
cover.insert_image(patch_rect, filename=str(BACKGROUND_PATCH), overlay=True)

# Place the supplied official shield in the reserved cover space.
cover.insert_image(
    fitz.Rect(50.3, 124.0, 135.7, 214.0),
    filename=str(SHIELD_PNG),
    keep_proportion=True,
    overlay=True,
)

# Keep the reduced artist credit below the proposal.
cover.insert_font(fontname='DejaVuSansCredit', fontfile=FONT_REGULAR)
cover.insert_text(
    fitz.Point(50, 451),
    'Artista: José Landoni',
    fontname='DejaVuSansCredit',
    fontsize=8.0,
    color=(1, 1, 1),
    overlay=True,
)

# Every interior page that uses the institutional header must identify the work's author.
for page in doc[1:]:
    if 'PROPUESTA INSTITUCIONAL' not in page.get_text():
        continue
    page.insert_font(fontname='DejaVuSansHeaderBold', fontfile=FONT_BOLD)
    page.insert_text(
        fitz.Point(705, 25.1),
        'OBRA DE JOSÉ LANDONI',
        fontname='DejaVuSansHeaderBold',
        fontsize=8.0,
        color=(0.40, 0.40, 0.40),
        overlay=True,
    )

doc.set_metadata({**doc.metadata, 'title': 'Puerta al Infierno — Presentación institucional corregida v2'})
doc.save(OUT_PDF, garbage=4, deflate=True, clean=True)
doc.close()

print(OUT_PDF)
