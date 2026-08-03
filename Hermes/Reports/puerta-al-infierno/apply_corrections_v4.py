from io import BytesIO
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

SRC = Path('/home/hermes/.hermes/desktop-attachments/Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-2.pdf')
SHIELD_SRC = Path('/home/hermes/.hermes/desktop-attachments/Escudo_del_Club_Atlético_Independiente.svg-2.webp')
OUT_DIR = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno')
OUT_PDF = OUT_DIR / 'Puerta_al_Infierno_PRESENTACION_INSTITUCIONAL-CORREGIDA-v4.pdf'
SHIELD_PNG = OUT_DIR / 'escudo-independiente-recortado.png'

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
DARK_TEXT = (23 / 255, 23 / 255, 23 / 255)
HEADER_GRAY = (0.40, 0.40, 0.40)
CARD_COLOR = (244, 242, 239, 255)

OUT_DIR.mkdir(parents=True, exist_ok=True)

shield = Image.open(SHIELD_SRC).convert('RGBA')
alpha_bbox = shield.getchannel('A').getbbox()
if alpha_bbox:
    shield = shield.crop(alpha_bbox)
shield.save(SHIELD_PNG, 'PNG', optimize=True)

doc = fitz.open(SRC)
if doc.page_count != 8:
    raise RuntimeError(f'Expected 8 pages, found {doc.page_count}')

# --- Cover corrections retained from v3 ---
cover = doc[0]
background = next(
    info for info in cover.get_image_info(xrefs=True)
    if tuple(info['bbox']) == (0.0, 0.0, 960.0, 540.0)
)
photo = Image.open(BytesIO(doc.extract_image(background['xref'])['image'])).convert('RGB')
scale_x = photo.width / cover.rect.width
scale_y = photo.height / cover.rect.height


def restore_dark_photo(rect: fitz.Rect, filename: str) -> None:
    crop_box = (
        round(rect.x0 * scale_x), round(rect.y0 * scale_y),
        round(rect.x1 * scale_x), round(rect.y1 * scale_y),
    )
    patch = photo.crop(crop_box)
    patch = Image.blend(patch, Image.new('RGB', patch.size, (0, 0, 0)), 0.68)
    path = OUT_DIR / filename
    patch.save(path, 'PNG', optimize=True)
    cover.insert_image(rect, filename=str(path), overlay=True)


restore_dark_photo(fitz.Rect(48, 118, 138, 220), 'portada-fondo-escudo-v4.png')
cover.insert_image(
    fitz.Rect(50.3, 124.0, 135.7, 214.0),
    filename=str(SHIELD_PNG), keep_proportion=True, overlay=True,
)
restore_dark_photo(fitz.Rect(44, 466, 326, 491), 'portada-fondo-caption-v4.png')
cover.insert_font(fontname='DejaVuSansCoverV4', fontfile=FONT_REGULAR)
cover.insert_text(
    fitz.Point(50, 478), 'Artista: José Landoni',
    fontname='DejaVuSansCoverV4', fontsize=11.5,
    color=(1, 1, 1), overlay=True,
)
cover.insert_text(
    fitz.Point(50, 507), 'Presentación institucional + anexo técnico preliminar',
    fontname='DejaVuSansCoverV4', fontsize=9.7,
    color=(1, 1, 1), overlay=True,
)

# --- Page 03: move the image/card down so it no longer invades the subtitle ---
page03 = doc[2]
# Preserve the original model image before covering its old position.
model_info = page03.get_image_info(xrefs=True)[0]
model_raw = doc.extract_image(model_info['xref'])['image']
model_image = Image.open(BytesIO(model_raw)).convert('RGB')
model_path = OUT_DIR / 'hoja-03-maqueta.png'
model_image.save(model_path, 'PNG', optimize=True)

# Hide the old card/image/caption and fully restore the subtitle strip.
page03.draw_rect(fitz.Rect(630, 118, 920, 470), color=None, fill=(1, 1, 1), overlay=True)
page03.draw_rect(fitz.Rect(40, 105, 900, 132), color=None, fill=(1, 1, 1), overlay=True)
page03.insert_font(fontname='DejaVuSansPage03V4', fontfile=FONT_REGULAR)
page03.insert_text(
    fitz.Point(44, 125.5),
    'Un arco de triunfo contemporáneo asociado a la mística del Diablo y al territorio de Avellaneda.',
    fontname='DejaVuSansPage03V4', fontsize=16.2, color=DARK_TEXT, overlay=True,
)

# Rounded card moved down with comfortable clearance below the subtitle.
card_w_pt, card_h_pt = 282, 336
card_scale = 4
card = Image.new('RGBA', (card_w_pt * card_scale, card_h_pt * card_scale), (255, 255, 255, 0))
ImageDraw.Draw(card).rounded_rectangle(
    (0, 0, card.width - 1, card.height - 1),
    radius=14 * card_scale,
    fill=CARD_COLOR,
)
card_path = OUT_DIR / 'hoja-03-tarjeta-v4.png'
card.save(card_path, 'PNG', optimize=True)
page03.insert_image(fitz.Rect(635, 142, 917, 478), filename=str(card_path), overlay=True)
page03.insert_image(fitz.Rect(655, 163.5, 897, 345), filename=str(model_path), overlay=True)

caption_lines = [
    'Lenguaje formal',
    'Dos soportes facetados sostienen el',
    'coronamiento estelar original. No se',
    'incorporan aletas, cuernos ni piezas',
    'adicionales respecto de la maqueta de',
    'referencia.',
]
for i, line in enumerate(caption_lines):
    page03.insert_text(
        fitz.Point(660, 365 + i * 12.6), line,
        fontname='DejaVuSansPage03V4', fontsize=9.7,
        color=DARK_TEXT, overlay=True,
    )

# --- Headers: author only, aligned to the left on every institutional-header page ---
for page in doc[1:]:
    if 'PROPUESTA INSTITUCIONAL' not in page.get_text():
        continue
    page.draw_rect(fitz.Rect(40, 10, 205, 31), color=None, fill=(1, 1, 1), overlay=True)
    page.insert_font(fontname='DejaVuSansHeaderBoldV4', fontfile=FONT_BOLD)
    page.insert_text(
        fitz.Point(44, 25.1), 'OBRA DE JOSÉ LANDONI',
        fontname='DejaVuSansHeaderBoldV4', fontsize=8.6,
        color=HEADER_GRAY, overlay=True,
    )

doc.set_metadata({**doc.metadata, 'title': 'Puerta al Infierno — Presentación institucional corregida v4'})
doc.save(OUT_PDF, garbage=4, deflate=True, clean=True)
doc.close()

print(OUT_PDF)
