from io import BytesIO
from pathlib import Path
import fitz
from PIL import Image

SRC = Path('/home/hermes/.hermes/desktop-attachments/Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-2.pdf')
SHIELD_SRC = Path('/home/hermes/.hermes/desktop-attachments/Escudo_del_Club_Atlético_Independiente.svg-2.webp')
OUT_DIR = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno')
OUT_PDF = OUT_DIR / 'Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-CORREGIDA-v3.pdf'
SHIELD_PNG = OUT_DIR / 'escudo-independiente-recortado.png'

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

OUT_DIR.mkdir(parents=True, exist_ok=True)

shield = Image.open(SHIELD_SRC).convert('RGBA')
alpha_bbox = shield.getchannel('A').getbbox()
if alpha_bbox:
    shield = shield.crop(alpha_bbox)
shield.save(SHIELD_PNG, 'PNG', optimize=True)

doc = fitz.open(SRC)
if doc.page_count != 8:
    raise RuntimeError(f'Expected 8 pages in the supplied PDF, found {doc.page_count}')

cover = doc[0]
image_info = cover.get_image_info(xrefs=True)
background = next(info for info in image_info if tuple(info['bbox']) == (0.0, 0.0, 960.0, 540.0))
photo = Image.open(BytesIO(doc.extract_image(background['xref'])['image'])).convert('RGB')
scale_x = photo.width / cover.rect.width
scale_y = photo.height / cover.rect.height


def restore_dark_photo(rect: fitz.Rect, filename: str) -> Path:
    crop_box = (
        round(rect.x0 * scale_x),
        round(rect.y0 * scale_y),
        round(rect.x1 * scale_x),
        round(rect.y1 * scale_y),
    )
    patch = photo.crop(crop_box)
    patch = Image.blend(patch, Image.new('RGB', patch.size, (0, 0, 0)), 0.68)
    path = OUT_DIR / filename
    patch.save(path, 'PNG', optimize=True)
    cover.insert_image(rect, filename=str(path), overlay=True)
    return path

# Remove the old simplified mark and restore its photographic background.
restore_dark_photo(fitz.Rect(48, 118, 138, 220), 'portada-fondo-escudo-v3.png')
cover.insert_image(
    fitz.Rect(50.3, 124.0, 135.7, 214.0),
    filename=str(SHIELD_PNG),
    keep_proportion=True,
    overlay=True,
)

# Remove the original lower caption so it can be moved down and leave more air for the artist credit.
restore_dark_photo(fitz.Rect(44, 466, 326, 491), 'portada-fondo-caption-v3.png')

cover.insert_font(fontname='DejaVuSansCreditV3', fontfile=FONT_REGULAR)
cover.insert_text(
    fitz.Point(50, 478),
    'Artista: José Landoni',
    fontname='DejaVuSansCreditV3',
    fontsize=11.5,
    color=(1, 1, 1),
    overlay=True,
)
cover.insert_text(
    fitz.Point(50, 507),
    'Presentación institucional + anexo técnico preliminar',
    fontname='DejaVuSansCreditV3',
    fontsize=9.7,
    color=(1, 1, 1),
    overlay=True,
)

# Author credit on every existing institutional header; no shield in headers.
for page in doc[1:]:
    if 'PROPUESTA INSTITUCIONAL' not in page.get_text():
        continue
    page.insert_font(fontname='DejaVuSansHeaderBoldV3', fontfile=FONT_BOLD)
    page.insert_text(
        fitz.Point(705, 25.1),
        'OBRA DE JOSÉ LANDONI',
        fontname='DejaVuSansHeaderBoldV3',
        fontsize=8.0,
        color=(0.40, 0.40, 0.40),
        overlay=True,
    )

doc.set_metadata({**doc.metadata, 'title': 'Puerta al Infierno — Presentación institucional corregida v3'})
doc.save(OUT_PDF, garbage=4, deflate=True, clean=True)
doc.close()

print(OUT_PDF)
