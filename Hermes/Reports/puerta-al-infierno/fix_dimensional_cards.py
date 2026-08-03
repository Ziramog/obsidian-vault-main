from pathlib import Path
import fitz

SRC = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno/Puerta_al_Infierno_PROPUESTA_INSTITUCIONAL_Y_ANEXO_TECNICO.pdf')
OUT = Path('/home/hermes/obsidian-vault/Hermes/Reports/puerta-al-infierno/Puerta_al_Infierno_PROPUESTA_Y_ANEXO_DIMENSIONES_CORREGIDAS.pdf')
FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

RED = (200 / 255, 16 / 255, 46 / 255)
DARK_RED = (145 / 255, 0 / 255, 25 / 255)
DARK = (23 / 255, 23 / 255, 23 / 255)
GRID = (0.82, 0.82, 0.82)
GROUP_BG = (1.0, 0.93, 0.94)
NOTE_BG = (244 / 255, 242 / 255, 239 / 255)
WHITE = (1, 1, 1)

HORIZONTAL = [
    ('Desarrollo horizontal máximo superior', '14,033 m', 'Ancho máximo del coronamiento.'),
    ('Desarrollo horizontal superior secundario', '13,033 m', 'Ancho secundario del coronamiento.'),
    ('Ancho exterior total en base', '12,260 m', 'Distancia total entre caras exteriores de apoyos.'),
    ('Luz interior entre apoyos en base', '10,156 m', 'Distancia libre entre caras interiores.'),
    ('Ancho del núcleo inferior', '4,147 m', 'Desarrollo horizontal del núcleo inferior.'),
    ('Ancho del núcleo superior', '3,993 m', 'Desarrollo horizontal del núcleo superior.'),
]
VERTICAL = [
    ('Altura máxima general', '11,919 m', 'Cota vertical máxima del conjunto.'),
    ('Altura de referencia secundaria', '11,618 m', 'Segunda cota vertical general.'),
    ('Altura de referencia lateral superior', '9,160 m', 'Nivel vertical señalado en el plano.'),
    ('Altura de referencia interior', '7,901 m', 'Cota vertical interior repetida en el plano.'),
    ('Altura lateral inferior', '7,555 m', 'Nivel vertical del extremo lateral inferior.'),
    ('Altura parcial del coronamiento', '3,717 m', 'Diferencia vertical parcial del coronamiento.'),
]


def draw_cell_text(page, rect, text, fontname, fontsize, color=DARK, left_pad=7, top_pad=4):
    result = page.insert_textbox(
        fitz.Rect(rect.x0 + left_pad, rect.y0 + top_pad, rect.x1 - 5, rect.y1 - 2),
        text,
        fontname=fontname,
        fontsize=fontsize,
        lineheight=1.05,
        color=color,
        align=fitz.TEXT_ALIGN_LEFT,
        overlay=True,
    )
    if result < 0:
        raise RuntimeError(f'Text did not fit: {text!r} in {rect}')


def draw_full_table(page):
    # Cover only the old raster table; keep title, description, materiality, note and footer untouched.
    page.draw_rect(fitz.Rect(41, 190, 919, 452), color=None, fill=WHITE, overlay=True)
    page.insert_font(fontname='TableRegular', fontfile=FONT_REGULAR)
    page.insert_font(fontname='TableBold', fontfile=FONT_BOLD)

    x = [44, 324, 430, 916]
    y = 194
    header_h = 26
    group_h = 16
    row_h = 16

    # Main header.
    page.draw_rect(fitz.Rect(x[0], y, x[-1], y + header_h), color=RED, fill=RED, overlay=True)
    headers = ['Parámetro', 'Dato de plano', 'Lectura geométrica']
    for i, label in enumerate(headers):
        draw_cell_text(page, fitz.Rect(x[i], y, x[i + 1], y + header_h), label, 'TableRegular', 8.4, WHITE, 7, 7)
    y += header_h

    def draw_group(title, rows):
        nonlocal y
        page.draw_rect(fitz.Rect(x[0], y, x[-1], y + group_h), color=GRID, fill=GROUP_BG, width=0.5, overlay=True)
        draw_cell_text(page, fitz.Rect(x[0], y, x[-1], y + group_h), title, 'TableBold', 7.6, DARK_RED, 7, 4)
        y += group_h
        for parameter, value, observation in rows:
            rect = fitz.Rect(x[0], y, x[-1], y + row_h)
            page.draw_rect(rect, color=GRID, fill=WHITE, width=0.45, overlay=True)
            for vx in x[1:-1]:
                page.draw_line(fitz.Point(vx, y), fitz.Point(vx, y + row_h), color=GRID, width=0.45, overlay=True)
            draw_cell_text(page, fitz.Rect(x[0], y, x[1], y + row_h), parameter, 'TableRegular', 7.0, DARK, 7, 4)
            draw_cell_text(page, fitz.Rect(x[1], y, x[2], y + row_h), value, 'TableRegular', 7.1, DARK, 7, 4)
            draw_cell_text(page, fitz.Rect(x[2], y, x[3], y + row_h), observation, 'TableRegular', 6.85, DARK, 7, 4)
            y += row_h

    draw_group('COTAS HORIZONTALES', HORIZONTAL)
    draw_group('COTAS VERTICALES', VERTICAL)


def draw_compact_table(page):
    # Cover the old right-hand table and note only. The dimensional drawing at left remains untouched.
    page.draw_rect(fitz.Rect(586, 143, 924, 502), color=None, fill=WHITE, overlay=True)
    page.insert_font(fontname='CompactRegular', fontfile=FONT_REGULAR)
    page.insert_font(fontname='CompactBold', fontfile=FONT_BOLD)

    x = [590, 818, 920]
    y = 150
    header_h = 27
    group_h = 16
    row_h = 17

    page.draw_rect(fitz.Rect(x[0], y, x[-1], y + header_h), color=RED, fill=RED, overlay=True)
    draw_cell_text(page, fitz.Rect(x[0], y, x[1], y + header_h), 'Parámetro', 'CompactRegular', 8.2, WHITE, 7, 7)
    draw_cell_text(page, fitz.Rect(x[1], y, x[2], y + header_h), 'Dato de plano', 'CompactRegular', 8.2, WHITE, 7, 7)
    y += header_h

    compact_horizontal = [
        ('Desarrollo horizontal máximo', '14,033 m'),
        ('Desarrollo horizontal secundario', '13,033 m'),
        ('Ancho exterior total en base', '12,260 m'),
        ('Luz interior entre apoyos', '10,156 m'),
        ('Ancho núcleo inferior', '4,147 m'),
        ('Ancho núcleo superior', '3,993 m'),
    ]
    compact_vertical = [
        ('Altura máxima general', '11,919 m'),
        ('Altura secundaria', '11,618 m'),
        ('Altura lateral superior', '9,160 m'),
        ('Altura interior', '7,901 m'),
        ('Altura lateral inferior', '7,555 m'),
        ('Altura parcial coronamiento', '3,717 m'),
    ]

    def draw_group(title, rows):
        nonlocal y
        page.draw_rect(fitz.Rect(x[0], y, x[-1], y + group_h), color=GRID, fill=GROUP_BG, width=0.5, overlay=True)
        draw_cell_text(page, fitz.Rect(x[0], y, x[-1], y + group_h), title, 'CompactBold', 7.4, DARK_RED, 7, 4)
        y += group_h
        for parameter, value in rows:
            rect = fitz.Rect(x[0], y, x[-1], y + row_h)
            page.draw_rect(rect, color=GRID, fill=WHITE, width=0.45, overlay=True)
            page.draw_line(fitz.Point(x[1], y), fitz.Point(x[1], y + row_h), color=GRID, width=0.45, overlay=True)
            draw_cell_text(page, fitz.Rect(x[0], y, x[1], y + row_h), parameter, 'CompactRegular', 6.8, DARK, 7, 4)
            draw_cell_text(page, fitz.Rect(x[1], y, x[2], y + row_h), value, 'CompactRegular', 7.0, DARK, 7, 4)
            y += row_h

    draw_group('COTAS HORIZONTALES', compact_horizontal)
    draw_group('COTAS VERTICALES', compact_vertical)

    note_rect = fitz.Rect(590, 426, 920, 493)
    page.draw_rect(note_rect, color=None, fill=NOTE_BG, overlay=True)
    note = (
        'Matriz reconstruida directamente del plano. Las cotas deberán verificarse y reconciliarse '
        'en modelo 3D, cálculo estructural y documentación ejecutiva.'
    )
    draw_cell_text(page, note_rect, note, 'CompactRegular', 7.1, GRAY if False else DARK, 10, 10)


doc = fitz.open(SRC)
if doc.page_count != 15:
    raise RuntimeError(f'Expected 15 pages, found {doc.page_count}')
draw_full_table(doc[10])
draw_compact_table(doc[11])
doc.set_metadata({**doc.metadata, 'title': 'Puerta al Infierno — Propuesta y anexo con dimensiones corregidas'})
doc.save(OUT, garbage=4, deflate=True, clean=True)
doc.close()
print(OUT)
