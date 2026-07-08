"""
Wolfim report preset for client-facing PDF reports.

Style source: https://www.wolfim.com
- Display: Space Grotesk
- Body: Inter
- Mono labels: JetBrains Mono
- Palette: off-white paper, black ink, neutral borders, green primary accent.

Brand assets and fonts are read from the Obsidian vault.
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
FONT_DIR = BRAND_DIR / 'fonts'
CACHE_DIR = Path('/home/hermes/.cache/wolfim-report-assets')
TRANSFER_DIR = Path('/home/hermes/Transfer-files')

BRAND_ASSET_CANDIDATES = {
    'logo_black': [
        BRAND_DIR / 'wolfim_logo_black.png',
        BRAND_DIR / 'wolfim_logo_black.svg',
        BRAND_DIR / 'WOLFIM_logo.svg',
        BRAND_DIR / 'logo-wolfim-reference.jpg',
    ],
    'logo_white': [
        BRAND_DIR / 'wolfim_logo_white.png',
        BRAND_DIR / 'wolfim_logo_white.svg',
        BRAND_DIR / 'wolfim studio white.png',
    ],
    'isologo_black': [
        BRAND_DIR / 'wolfim_isologo_black.png',
        BRAND_DIR / 'wolfim_isologo_black.svg',
        BRAND_DIR / 'favicom.svg',
    ],
    'isologo_white': [
        BRAND_DIR / 'wolfim_isologo_white.png',
        BRAND_DIR / 'wolfim_isologo_white.svg',
    ],
}

# Wolfim.com CSS tokens observed 2026-07-08.
COLORS = {
    'black': (10, 10, 10),
    'white': (245, 245, 240),
    'paper': (250, 250, 248),
    'gray_100': (232, 232, 227),
    'gray_200': (208, 208, 203),
    'gray_300': (160, 160, 155),
    'gray_400': (112, 112, 104),
    'gray_500': (80, 80, 74),
    'green': (16, 185, 129),
    'whatsapp': (37, 211, 102),
    'red': (230, 30, 30),
    # Backward-compatible aliases for older report scripts.
    'ink': (10, 10, 10),
    'text': (80, 80, 74),
    'muted': (112, 112, 104),
    'line': (208, 208, 203),
    'soft': (245, 245, 240),
}

FONT_SPACE_REGULAR = FONT_DIR / 'SpaceGrotesk-Regular.ttf'
FONT_SPACE_MEDIUM = FONT_DIR / 'SpaceGrotesk-Medium.ttf'
FONT_SPACE_BOLD = FONT_DIR / 'SpaceGrotesk-Bold.ttf'
FONT_INTER_REGULAR = FONT_DIR / 'Inter-Regular.ttf'
FONT_INTER_MEDIUM = FONT_DIR / 'Inter-Medium.ttf'
FONT_INTER_SEMIBOLD = FONT_DIR / 'Inter-SemiBold.ttf'
FONT_MONO_REGULAR = FONT_DIR / 'JetBrainsMono-Regular.ttf'
FONT_MONO_MEDIUM = FONT_DIR / 'JetBrainsMono-Medium.ttf'

# Hard fallback if fonts have not been synced yet.
DEJAVU = Path('/usr/share/fonts/truetype/dejavu')


def _font(path: Path, fallback: str) -> str:
    return str(path if path.exists() else DEJAVU / fallback)


def _first_existing(candidates: Iterable[Path]) -> Path | None:
    for path in candidates:
        if path.exists():
            return path
    return None


def _convert_svg_to_png(src: Path, dst: Path, width: int | None = None) -> Path:
    """Render SVG to PNG preserving transparency when possible."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        import fitz  # PyMuPDF
        from PIL import Image

        doc = fitz.open(str(src))
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=True)
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


def _load_asset(key: str, cache_name: str, width: int) -> tuple[Path, str]:
    src = _first_existing(BRAND_ASSET_CANDIDATES[key])
    if not src:
        raise FileNotFoundError(f'No Wolfim brand asset found for {key} in {BRAND_DIR}')
    return _ensure_png(src, cache_name, width=width), str(src)


def get_brand_assets() -> dict[str, Path | str]:
    logo_black, logo_black_src = _load_asset('logo_black', 'wolfim-logo-black-cache.png', 1400)
    logo_white, logo_white_src = _load_asset('logo_white', 'wolfim-logo-white-cache.png', 1400)
    isologo_black, isologo_black_src = _load_asset('isologo_black', 'wolfim-isologo-black-cache.png', 420)
    isologo_white, isologo_white_src = _load_asset('isologo_white', 'wolfim-isologo-white-cache.png', 420)
    return {
        'logo_black': logo_black,
        'logo_white': logo_white,
        'isologo_black': isologo_black,
        'isologo_white': isologo_white,
        'logo_black_source': logo_black_src,
        'logo_white_source': logo_white_src,
        'isologo_black_source': isologo_black_src,
        'isologo_white_source': isologo_white_src,
        'logo': logo_black,
        'isologo': isologo_black,
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
        subprocess.run(['sudo', 'mkdir', '-p', str(TRANSFER_DIR)], check=True, timeout=20)
        subprocess.run(['sudo', 'cp', str(src), str(dst)], check=True, timeout=30)
        subprocess.run(['sudo', 'chown', f'{os.getuid()}:{os.getgid()}', str(dst)], check=False, timeout=20)
    return dst


class WolfimReport(FPDF):
    """Professional Wolfim report preset matching wolfim.com visual language."""

    def __init__(self, report_title: str, client_name: str = '', footer_text: str | None = None):
        super().__init__('P', 'mm', 'A4')
        self.report_title = report_title
        self.client_name = client_name
        self.footer_text = footer_text or 'Wolfim Studio · Web · Catálogo · SEO · Medición'
        self.assets = get_brand_assets()
        self.set_margins(16, 16, 16)
        self.set_auto_page_break(auto=True, margin=20)
        self._register_fonts()
        self.alias_nb_pages()

    def _register_fonts(self):
        self.add_font('DISPLAY', '', _font(FONT_SPACE_REGULAR, 'DejaVuSans.ttf'))
        self.add_font('DISPLAY', 'B', _font(FONT_SPACE_BOLD, 'DejaVuSans-Bold.ttf'))
        self.add_font('BODY', '', _font(FONT_INTER_REGULAR, 'DejaVuSans.ttf'))
        self.add_font('BODY', 'B', _font(FONT_INTER_SEMIBOLD, 'DejaVuSans-Bold.ttf'))
        self.add_font('MONO', '', _font(FONT_MONO_REGULAR, 'DejaVuSansMono.ttf'))
        self.add_font('MONO', 'B', _font(FONT_MONO_MEDIUM, 'DejaVuSansMono-Bold.ttf'))

    def color(self, name: str) -> tuple[int, int, int]:
        return COLORS[name]

    def _page_background(self):
        self.set_fill_color(*self.color('paper'))
        self.rect(0, 0, 210, 297, 'F')

    # ---------- header/footer ----------
    def header(self):
        self._page_background()
        if self.page_no() <= 1:
            return
        self.set_y(8)
        self.image(str(self.assets['logo_black']), x=16, y=7.4, w=30)
        self.set_xy(56, 8.4)
        self.set_font('MONO', '', 7.0)
        self.set_text_color(*self.color('gray_400'))
        header = self.report_title
        if self.client_name:
            header = f'{self.client_name.upper()} / {self.report_title.upper()}'
        self.cell(0, 4, header, align='R')
        self.set_draw_color(*self.color('gray_200'))
        self.set_line_width(0.18)
        self.line(16, 16, 194, 16)
        self.set_y(23)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*self.color('gray_200'))
        self.set_line_width(0.18)
        self.line(16, self.get_y(), 194, self.get_y())
        y = self.get_y() + 2.2
        try:
            self.image(str(self.assets['isologo_black']), x=16, y=y - 1.1, w=4.8)
        except Exception:
            pass
        self.set_xy(24, y)
        self.set_font('MONO', '', 6.5)
        self.set_text_color(*self.color('gray_400'))
        self.cell(116, 4, self.footer_text.upper())
        self.set_xy(154, y)
        self.cell(40, 4, f'PÁGINA {self.page_no()}/{{nb}}', align='R')

    # ---------- cover ----------
    def add_cover(self, title: str, subtitle: str, client: str, period: str, prepared_for: str | None = None, date_label: str | None = None):
        self.add_page()

        # Site-like minimal top rail.
        self.image(str(self.assets['logo_black']), x=16, y=18, w=43)
        self.set_xy(142, 20)
        self.set_draw_color(*self.color('black'))
        self.set_line_width(0.25)
        self.rect(142, 18, 52, 9, 'D')
        self.set_xy(142, 20.6)
        self.set_font('MONO', 'B', 7.0)
        self.set_text_color(*self.color('black'))
        self.cell(52, 4, 'INFORME WOLFIM', align='C')

        # Big editorial title, matching wolfim.com hero attitude.
        self.set_xy(16, 54)
        self.set_font('DISPLAY', 'B', 28)
        self.set_text_color(*self.color('black'))
        self.multi_cell(142, 11.5, title)
        self.ln(2)
        self.set_x(16)
        self.set_font('BODY', '', 10.5)
        self.set_text_color(*self.color('gray_500'))
        self.multi_cell(144, 5.8, subtitle)

        # Mono category strip.
        self.ln(7)
        self.set_x(16)
        self.set_font('MONO', '', 7.0)
        self.set_text_color(*self.color('gray_400'))
        self.cell(0, 4, 'WEB  ·  CATÁLOGO  ·  MEDICIÓN  ·  SEO')

        # Metadata as austere bordered card.
        y = 121
        self.set_draw_color(*self.color('gray_200'))
        self.set_fill_color(*self.color('white'))
        self.rect(16, y, 178, 39, 'DF')
        self.set_xy(23, y + 7)
        self.meta_line('CLIENTE', client)
        self.meta_line('PERÍODO', period)
        if prepared_for:
            self.meta_line('PREPARADO PARA', prepared_for)
        if date_label:
            self.meta_line('FECHA', date_label)

        # Bottom signature, inspired by the site hero.
        self.set_y(247)
        self.set_font('BODY', '', 8.5)
        self.set_text_color(*self.color('gray_400'))
        self.multi_cell(128, 5.0, 'Reporte preparado para convertir datos en decisiones comerciales concretas.')
        self.image(str(self.assets['logo_black']), x=151, y=247, w=43)
        self.set_y(270)
        self.set_x(16)
        self.set_font('MONO', '', 6.5)
        self.set_text_color(*self.color('gray_400'))
        self.cell(30, 4, 'BUENOS AIRES')
        self.set_fill_color(*self.color('green'))
        self.ellipse(47.5, 271.2, 1.8, 1.8, 'F')
        self.set_x(52)
        self.cell(0, 4, 'SERVICIO REMOTO MUNDIAL')

    def meta_line(self, label: str, value: str):
        self.set_font('MONO', 'B', 7.0)
        self.set_text_color(*self.color('black'))
        self.cell(43, 6.0, label)
        self.set_font('BODY', '', 8.5)
        self.set_text_color(*self.color('gray_500'))
        self.cell(0, 6.0, value, new_x='LMARGIN', new_y='NEXT')
        self.set_x(23)

    # ---------- content blocks ----------
    def section(self, title: str, kicker: str | None = None):
        if self.get_y() > 248:
            self.add_page()
        if kicker:
            self.set_font('MONO', 'B', 7.5)
            self.set_text_color(*self.color('black'))
            self.cell(0, 5, kicker.upper(), new_x='LMARGIN', new_y='NEXT')
            self.ln(1)
        self.set_font('DISPLAY', 'B', 16)
        self.set_text_color(*self.color('black'))
        self.cell(0, 8.5, title, new_x='LMARGIN', new_y='NEXT')
        y = self.get_y()
        # no vignette (green ball) — just a thin black line
        self.set_draw_color(*self.color('black'))
        self.set_line_width(0.25)
        self.line(16, y, 52, y)
        self.ln(5)

    def body(self, text: str, size: float = 9.8, color: str = 'gray_500'):
        self.set_font('BODY', '', size)
        self.set_text_color(*self.color(color))
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def callout(self, title: str, text: str, tone: str = 'green'):
        if self.get_y() > 236:
            self.add_page()
        accent = self.color('green') if tone == 'green' else self.color('black')
        fill = self.color('white')
        x, y, w = 16, self.get_y(), 178
        self.set_fill_color(*fill)
        self.set_draw_color(*self.color('gray_200'))
        self.rect(x, y, w, 28, 'DF')
        self.set_fill_color(*accent)
        self.rect(x, y, 1.7, 28, 'F')
        self.set_xy(x + 6, y + 5)
        self.set_font('DISPLAY', 'B', 9.8)
        self.set_text_color(*self.color('black'))
        self.cell(0, 5, title, new_x='LMARGIN', new_y='NEXT')
        self.set_x(x + 6)
        self.set_font('BODY', '', 8.5)
        self.set_text_color(*self.color('gray_500'))
        self.multi_cell(w - 12, 4.7, text)
        self.set_y(y + 32)

    def metric_cards(self, items: Sequence[tuple[str, str, str]], columns: int = 3):
        x0 = 16
        gap = 5
        w = (178 - gap * (columns - 1)) / columns
        h = 27
        y0 = self.get_y()
        for i, (label, value, note) in enumerate(items):
            if self.get_y() > 245:
                self.add_page(); y0 = self.get_y()
            col = i % columns
            row = i // columns
            x = x0 + col * (w + gap)
            y = y0 + row * (h + 5)
            self.set_fill_color(*self.color('white'))
            self.set_draw_color(*self.color('gray_200'))
            self.rect(x, y, w, h, 'DF')
            # black vignette
            self.set_fill_color(*self.color('black'))
            self.ellipse(x + 5, y + 5, 2.2, 2.2, 'F')
            self.set_xy(x + 5, y + 8.5)
            self.set_font('DISPLAY', 'B', 15)
            self.set_text_color(*self.color('black'))
            self.cell(w - 10, 6.5, value, new_x='LMARGIN', new_y='NEXT')
            self.set_xy(x + 5, y + 16)
            self.set_font('MONO', 'B', 6.5)
            self.set_text_color(*self.color('black'))
            self.multi_cell(w - 10, 3.5, label.upper())
            if note:
                self.set_xy(x + 5, y + 22.5)
                self.set_font('BODY', '', 6.5)
                self.set_text_color(*self.color('gray_400'))
                self.cell(w - 10, 3, note)
        rows = (len(items) + columns - 1) // columns
        self.set_y(y0 + rows * (h + 5) + 2)

    def table(self, headers: Sequence[str], rows: Sequence[Sequence[str]], widths: Sequence[float], font_size: float = 8.2, row_h: float = 10.5):
        if abs(sum(widths) - 178) > 0.5:
            raise ValueError(f'Table widths must sum to ~178mm, got {sum(widths)}')
        self.set_font('MONO', 'B', font_size - 0.5)
        self.set_fill_color(*self.color('black'))
        self.set_text_color(*self.color('white'))
        for h, w in zip(headers, widths):
            self.cell(w, 7.5, str(h).upper(), border=0, fill=True)
        self.ln()
        # add gap between header and first row
        self.ln(0.8)
        fill = False
        for row in rows:
            if self.get_y() + row_h > 275:
                self.add_page()
                self.set_font('MONO', 'B', font_size - 0.5)
                self.set_fill_color(*self.color('black'))
                self.set_text_color(*self.color('white'))
                for h, w in zip(headers, widths):
                    self.cell(w, 7.5, str(h).upper(), border=0, fill=True)
                self.ln()
                self.ln(0.8)
            self.set_font('BODY', '', font_size)
            self.set_text_color(*self.color('gray_500'))
            self.set_fill_color(*(self.color('white') if fill else self.color('paper')))
            y = self.get_y(); x = self.get_x()
            for i, (val, w) in enumerate(zip(row, widths)):
                self.set_xy(x + sum(widths[:i]), y)
                self.multi_cell(w, 4.7, str(val), border='B', fill=fill)
            self.set_y(y + row_h + 0.5)
            self.set_draw_color(*self.color('gray_200'))
            fill = not fill
        self.ln(3)

    def bullets(self, items: Sequence[str]):
        self.set_font('BODY', '', 9.5)
        self.set_text_color(*self.color('gray_500'))
        for item in items:
            y = self.get_y() + 1.5
            # black vignette
            self.set_fill_color(*self.color('black'))
            self.ellipse(18, y, 1.3, 1.3, 'F')
            self.set_x(22)
            self.multi_cell(170, 5.2, item)
        self.ln(2)

    def closing_panel(self, title: str, text: str):
        if self.get_y() > 228:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*self.color('black'))
        self.rect(16, y, 178, 38, 'F')
        self.image(str(self.assets['isologo_white']), x=176, y=y + 10, w=12)
        self.set_xy(22, y + 8)
        self.set_font('DISPLAY', 'B', 11.5)
        self.set_text_color(*self.color('white'))
        self.cell(0, 6, title, new_x='LMARGIN', new_y='NEXT')
        self.set_x(22)
        self.set_font('BODY', '', 8.8)
        self.set_text_color(220, 220, 216)
        self.multi_cell(145, 5.0, text)
        self.set_y(y + 44)
