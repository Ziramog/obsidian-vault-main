"""
Wolfim report preset for client-facing PDF reports.

Use from report scripts:

    from wolfim_report_preset import WolfimReport, copy_to_transfer

    pdf = WolfimReport(report_title='Informe mensual de Analytics')
    pdf.add_cover(...)
    pdf.add_page()
    pdf.section('Resumen')
    pdf.metric_cards([...])
    pdf.output('/home/hermes/report.pdf')
    copy_to_transfer('/home/hermes/report.pdf')

Brand assets are read from the Obsidian vault and converted into cache PNGs when needed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, Sequence

from fpdf import FPDF

VAULT = Path('/home/hermes/obsidian-vault')
BRAND_DIR = VAULT / 'companies/wolfim/brand'
CACHE_DIR = Path('/home/hermes/.cache/wolfim-report-assets')
TRANSFER_DIR = Path('/home/hermes/Transfer-files')

LOGO_CANDIDATES = [
    BRAND_DIR / 'WOLFIM_logo.svg',
    BRAND_DIR / 'logo-wolfim-reference.jpg',
    BRAND_DIR / 'wolfim studio white.png',
]

# Juan mentioned `wolfim_isologo (png)`. It is not present on this VPS yet, so the
# preset checks for it first and falls back to favicom.svg, which is the current
# square Wolfim mark available in the vault.
ISOLOGO_CANDIDATES = [
    BRAND_DIR / 'wolfim_isologo (png).png',
    BRAND_DIR / 'wolfim_isologo (png)',
    BRAND_DIR / 'wolfim_isologo.png',
    BRAND_DIR / 'favicom.svg',
]

COLORS = {
    'ink': (10, 10, 15),
    'text': (36, 39, 46),
    'muted': (93, 101, 116),
    'line': (222, 226, 234),
    'paper': (255, 255, 255),
    'soft': (247, 248, 250),
    'soft_red': (255, 244, 244),
    'red': (230, 30, 30),
    'red_dark': (166, 20, 20),
    'success': (24, 128, 91),
}

FONT_REGULAR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_ITALIC = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'


def _first_existing(candidates: Iterable[Path]) -> Path | None:
    for path in candidates:
        if path.exists():
            return path
    return None


def _convert_svg_to_png(src: Path, dst: Path, width: int | None = None) -> Path:
    """Render SVG to PNG.

    ImageMagick on this VPS can render some clipped SVGs as blank grayscale,
    so use PyMuPDF first and only fall back to `convert` if needed.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        import fitz  # PyMuPDF
        from PIL import Image

        doc = fitz.open(str(src))
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        tmp = dst.with_suffix('.tmp.png')
        pix.save(str(tmp))
        if width:
            img = Image.open(tmp)
            ratio = width / img.width
            height = max(1, int(img.height * ratio))
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(dst)
            tmp.unlink(missing_ok=True)
        else:
            tmp.replace(dst)
        return dst
    except Exception:
        cmd = ['convert']
        if width:
            cmd += ['-resize', f'{width}x']
        cmd += [str(src), str(dst)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise RuntimeError(f'ImageMagick convert failed for {src}: {result.stderr[:500]}')
        return dst


def _ensure_png(src: Path, out_name: str, width: int | None = None) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == '.svg':
        dst = CACHE_DIR / out_name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            _convert_svg_to_png(src, dst, width=width)
        return dst
    return src


def get_brand_assets() -> dict[str, Path | str]:
    logo_src = _first_existing(LOGO_CANDIDATES)
    iso_src = _first_existing(ISOLOGO_CANDIDATES)
    if not logo_src:
        raise FileNotFoundError(f'No Wolfim logo found in {BRAND_DIR}')
    if not iso_src:
        raise FileNotFoundError(f'No Wolfim isologo/favicom found in {BRAND_DIR}')

    logo = _ensure_png(logo_src, 'wolfim-logo-cache.png', width=1400)
    isologo = _ensure_png(iso_src, 'wolfim-isologo-cache.png', width=320)
    return {
        'logo': logo,
        'isologo': isologo,
        'logo_source': str(logo_src),
        'isologo_source': str(iso_src),
    }


def copy_to_transfer(pdf_path: str | Path) -> Path:
    src = Path(pdf_path)
    if not src.exists():
        raise FileNotFoundError(src)
    dst = TRANSFER_DIR / src.name
    try:
        TRANSFER_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        try:
            os.chown(dst, os.getuid(), os.getgid())
        except PermissionError:
            pass
    except PermissionError:
        # /home/hermes/Transfer-files is root-owned on the VPS. Fall back to sudo.
        subprocess.run(['sudo', 'mkdir', '-p', str(TRANSFER_DIR)], check=True, timeout=20)
        subprocess.run(['sudo', 'cp', str(src), str(dst)], check=True, timeout=30)
        subprocess.run(['sudo', 'chown', f'{os.getuid()}:{os.getgid()}', str(dst)], check=False, timeout=20)
    return dst


class WolfimReport(FPDF):
    """Professional Wolfim client-facing report preset."""

    def __init__(self, report_title: str, client_name: str = '', footer_text: str | None = None):
        super().__init__('P', 'mm', 'A4')
        self.report_title = report_title
        self.client_name = client_name
        self.footer_text = footer_text or 'Wolfim Studio · Diseño web, medición y crecimiento comercial'
        self.assets = get_brand_assets()
        self.set_margins(16, 16, 16)
        self.set_auto_page_break(auto=True, margin=20)
        self.add_font('WOLF', '', FONT_REGULAR)
        self.add_font('WOLF', 'B', FONT_BOLD)
        self.add_font('WOLF', 'I', FONT_ITALIC)
        self.alias_nb_pages()

    # ---------- helpers ----------
    def color(self, name: str) -> tuple[int, int, int]:
        return COLORS[name]

    def _set_text(self, color_name='text'):
        self.set_text_color(*self.color(color_name))

    # ---------- header/footer ----------
    def header(self):
        if self.page_no() <= 1:
            return
        # subtle top rule + small logo
        self.set_y(9)
        self.image(str(self.assets['logo']), x=16, y=7.5, w=31)
        self.set_xy(55, 8.5)
        self.set_font('WOLF', '', 7.2)
        self.set_text_color(*self.color('muted'))
        header = self.report_title
        if self.client_name:
            header = f'{self.client_name} · {self.report_title}'
        self.cell(0, 4, header, align='R')
        self.set_draw_color(*self.color('line'))
        self.line(16, 15.5, 194, 15.5)
        self.set_y(21)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*self.color('line'))
        self.line(16, self.get_y(), 194, self.get_y())
        y = self.get_y() + 2.4
        try:
            self.image(str(self.assets['isologo']), x=16, y=y - 1.5, w=5.5)
        except Exception:
            pass
        self.set_xy(24, y)
        self.set_font('WOLF', '', 6.8)
        self.set_text_color(*self.color('muted'))
        self.cell(120, 4, self.footer_text)
        self.set_xy(154, y)
        self.cell(40, 4, f'Página {self.page_no()}/{{nb}}', align='R')

    # ---------- cover ----------
    def add_cover(self, title: str, subtitle: str, client: str, period: str, prepared_for: str | None = None, date_label: str | None = None):
        self.add_page()
        # top logo
        self.image(str(self.assets['logo']), x=16, y=16, w=54)

        # right brand pill
        self.set_xy(142, 18)
        self.set_fill_color(*self.color('ink'))
        self.set_text_color(255, 255, 255)
        self.set_font('WOLF', 'B', 7.5)
        self.cell(52, 8, 'INFORME WOLFIM', border=0, align='C', fill=True)

        # title block
        self.set_xy(16, 52)
        self.set_font('WOLF', 'B', 22)
        self.set_text_color(*self.color('ink'))
        self.multi_cell(178, 10, title)
        self.ln(2)
        self.set_x(16)
        self.set_font('WOLF', '', 10.5)
        self.set_text_color(*self.color('muted'))
        self.multi_cell(160, 5.8, subtitle)

        # red accent line
        self.set_draw_color(*self.color('red'))
        self.set_line_width(1.0)
        self.line(16, self.get_y() + 6, 88, self.get_y() + 6)
        self.ln(16)

        # metadata card
        y = self.get_y()
        self.set_fill_color(*self.color('soft'))
        self.set_draw_color(*self.color('line'))
        self.rect(16, y, 178, 42, 'DF')
        self.set_xy(22, y + 7)
        self.meta_line('Cliente', client)
        self.meta_line('Período', period)
        if prepared_for:
            self.meta_line('Preparado para', prepared_for)
        if date_label:
            self.meta_line('Fecha', date_label)
        self.set_y(y + 55)

        # closing footer on cover
        self.set_y(254)
        self.set_font('WOLF', '', 8)
        self.set_text_color(*self.color('muted'))
        self.multi_cell(150, 5, 'Reporte preparado para convertir datos en decisiones comerciales concretas.')
        self.image(str(self.assets['isologo']), x=180, y=250, w=13)

    def meta_line(self, label: str, value: str):
        self.set_font('WOLF', 'B', 8)
        self.set_text_color(*self.color('ink'))
        self.cell(35, 5.5, label)
        self.set_font('WOLF', '', 8)
        self.set_text_color(*self.color('text'))
        self.cell(0, 5.5, value, new_x='LMARGIN', new_y='NEXT')
        self.set_x(22)

    # ---------- content blocks ----------
    def section(self, title: str, kicker: str | None = None):
        if self.get_y() > 248:
            self.add_page()
        if kicker:
            self.set_font('WOLF', 'B', 6.5)
            self.set_text_color(*self.color('red'))
            self.cell(0, 4, kicker.upper(), new_x='LMARGIN', new_y='NEXT')
        self.set_font('WOLF', 'B', 13.2)
        self.set_text_color(*self.color('ink'))
        self.cell(0, 7.5, title, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(*self.color('red'))
        self.set_line_width(0.35)
        self.line(16, self.get_y(), 47, self.get_y())
        self.set_draw_color(*self.color('line'))
        self.set_line_width(0.2)
        self.line(49, self.get_y(), 194, self.get_y())
        self.ln(4)

    def body(self, text: str, size: float = 8.7, color: str = 'text'):
        self.set_font('WOLF', '', size)
        self.set_text_color(*self.color(color))
        self.multi_cell(0, 4.9, text)
        self.ln(2)

    def callout(self, title: str, text: str, tone: str = 'red'):
        if self.get_y() > 236:
            self.add_page()
        if tone == 'green':
            fill, accent = (240, 253, 248), self.color('success')
        elif tone == 'soft':
            fill, accent = self.color('soft'), self.color('muted')
        else:
            fill, accent = self.color('soft_red'), self.color('red')
        x, y, w = 16, self.get_y(), 178
        self.set_fill_color(*fill)
        self.set_draw_color(*self.color('line'))
        self.rect(x, y, w, 25, 'DF')
        self.set_fill_color(*accent)
        self.rect(x, y, 2.2, 25, 'F')
        self.set_xy(x + 6, y + 4)
        self.set_font('WOLF', 'B', 8.5)
        self.set_text_color(*self.color('ink'))
        self.cell(0, 4.5, title, new_x='LMARGIN', new_y='NEXT')
        self.set_x(x + 6)
        self.set_font('WOLF', '', 7.7)
        self.set_text_color(*self.color('text'))
        self.multi_cell(w - 12, 4.2, text)
        self.set_y(y + 29)

    def metric_cards(self, items: Sequence[tuple[str, str, str]], columns: int = 3):
        x0 = 16
        gap = 5
        w = (178 - gap * (columns - 1)) / columns
        h = 24
        y0 = self.get_y()
        for i, (label, value, note) in enumerate(items):
            if self.get_y() > 245:
                self.add_page(); y0 = self.get_y()
            col = i % columns
            row = i // columns
            x = x0 + col * (w + gap)
            y = y0 + row * (h + 5)
            self.set_xy(x, y)
            self.set_fill_color(*self.color('soft'))
            self.set_draw_color(*self.color('line'))
            self.rect(x, y, w, h, 'DF')
            self.set_fill_color(*self.color('red'))
            self.rect(x, y, 1.7, h, 'F')
            self.set_xy(x + 5, y + 3.6)
            self.set_font('WOLF', 'B', 13.2)
            self.set_text_color(*self.color('ink'))
            self.cell(w - 9, 5.8, value, new_x='LMARGIN', new_y='NEXT')
            self.set_xy(x + 5, y + 10.8)
            self.set_font('WOLF', 'B', 7.1)
            self.set_text_color(*self.color('text'))
            self.multi_cell(w - 9, 3.25, label)
            if note:
                self.set_xy(x + 5, y + 18)
                self.set_font('WOLF', '', 6.2)
                self.set_text_color(*self.color('muted'))
                self.cell(w - 9, 3, note)
        rows = (len(items) + columns - 1) // columns
        self.set_y(y0 + rows * (h + 5) + 2)

    def table(self, headers: Sequence[str], rows: Sequence[Sequence[str]], widths: Sequence[float], font_size: float = 7.0, row_h: float = 9.0):
        if abs(sum(widths) - 178) > 0.5:
            raise ValueError(f'Table widths must sum to ~178mm, got {sum(widths)}')
        self.set_font('WOLF', 'B', font_size)
        self.set_fill_color(*self.color('ink'))
        self.set_text_color(255, 255, 255)
        self.set_draw_color(*self.color('ink'))
        for h, w in zip(headers, widths):
            self.cell(w, 6.5, h, border=0, fill=True)
        self.ln()
        fill = False
        for row in rows:
            if self.get_y() + row_h > 275:
                self.add_page()
                self.set_font('WOLF', 'B', font_size)
                self.set_fill_color(*self.color('ink'))
                self.set_text_color(255, 255, 255)
                for h, w in zip(headers, widths):
                    self.cell(w, 6.5, h, border=0, fill=True)
                self.ln()
            self.set_font('WOLF', '', font_size)
            self.set_text_color(*self.color('text'))
            self.set_fill_color(*(self.color('soft') if fill else self.color('paper')))
            y = self.get_y(); x = self.get_x()
            for i, (val, w) in enumerate(zip(row, widths)):
                self.set_xy(x + sum(widths[:i]), y)
                self.multi_cell(w, 4.2, str(val), border='B', fill=fill)
            self.set_y(y + row_h)
            self.set_draw_color(*self.color('line'))
            fill = not fill
        self.ln(3)

    def bullets(self, items: Sequence[str]):
        self.set_font('WOLF', '', 8.4)
        self.set_text_color(*self.color('text'))
        for item in items:
            self.set_x(18)
            self.multi_cell(174, 4.8, f'• {item}')
        self.ln(2)

    def closing_panel(self, title: str, text: str):
        if self.get_y() > 228:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*self.color('ink'))
        self.rect(16, y, 178, 34, 'F')
        self.image(str(self.assets['isologo']), x=176, y=y + 8, w=12)
        self.set_xy(22, y + 7)
        self.set_font('WOLF', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5.5, title, new_x='LMARGIN', new_y='NEXT')
        self.set_x(22)
        self.set_font('WOLF', '', 8)
        self.set_text_color(230, 232, 236)
        self.multi_cell(145, 4.5, text)
        self.set_y(y + 40)
