from pathlib import Path
import re
from fpdf import FPDF

BASE = Path('/home/hermes/obsidian-vault/companies/construvial/propuesta_2026/2026-07-10-presupuesto-modular')
SRC = BASE / 'propuesta-ampliada-servicios-construvial-2026-07-10.md'
OUT = BASE / 'propuesta-ampliada-servicios-construvial-2026-07-10.pdf'

DARK = (10, 10, 10)
GOLD = (245, 197, 24)
GOLD_DARK = (200, 160, 16)
TEXT = (28, 28, 28)
MUTED = (105, 105, 105)
LINE = (226, 226, 226)
SOFT = (249, 247, 240)
BLUE = (24, 52, 92)


def strip_frontmatter(text: str) -> str:
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) == 3:
            return parts[2].lstrip('\n')
    return text


def clean_md(text: str) -> str:
    text = text.replace('**', '')
    text = text.replace('`', '')
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    text = re.sub(r'\s+$', '', text)
    return text.strip()


class ProposalPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=16)
        self.alias_nb_pages()
        self.add_font('DJS', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
        self.add_font('DJS', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
        self.add_font('DJS', 'I', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf')
        self.is_cover = False

    def header(self):
        if self.is_cover:
            return
        self.set_y(10)
        self.set_font('DJS', 'B', 9)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 5, 'WOLFIM  |  Propuesta modular Construvial', new_x='LMARGIN', new_y='NEXT', align='L')
        self.set_draw_color(*LINE)
        self.line(12, 17, 198, 17)
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*LINE)
        self.line(12, 285, 198, 285)
        self.set_font('DJS', 'I', 7)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, f'Borrador para revision interna  |  Pagina {self.page_no()}/{{nb}}', align='C')

    def cover_page(self):
        self.is_cover = True
        self.add_page()
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 297, 'F')

        self.set_text_color(*GOLD)
        self.set_font('DJS', 'B', 12)
        self.set_xy(18, 24)
        self.cell(0, 8, 'WOLFIM STUDIO', new_x='LMARGIN', new_y='NEXT')

        self.set_text_color(255, 255, 255)
        self.set_font('DJS', 'B', 28)
        self.set_x(18)
        self.multi_cell(150, 12, 'Propuesta modular de servicios digitales')
        self.ln(2)
        self.set_font('DJS', '', 16)
        self.set_text_color(210, 210, 210)
        self.set_x(18)
        self.cell(0, 8, 'Construvial S.A.  |  Julio 2026', new_x='LMARGIN', new_y='NEXT')

        self.ln(12)
        self.set_x(18)
        self.set_font('DJS', '', 11)
        self.set_text_color(222, 222, 222)
        self.multi_cell(170, 7, 'Sistema digital B2B compuesto por Web Premium, Google Ads, LinkedIn, Instagram y un motor de contenidos reutilizable, con modulos independientes y paquetes recomendados.')

        y = 102
        self.set_draw_color(60, 60, 60)
        self.set_fill_color(24, 24, 24)
        self.rounded_rect(18, y, 174, 48, 3, style='FD')
        self.set_xy(24, y + 6)
        self.set_text_color(*GOLD)
        self.set_font('DJS', 'B', 10)
        self.cell(0, 6, 'RECOMENDACION ACTUAL', new_x='LMARGIN', new_y='NEXT')
        self.set_x(24)
        self.set_text_color(255, 255, 255)
        self.set_font('DJS', 'B', 18)
        self.cell(0, 8, 'Plan B - B2B Comercial', new_x='LMARGIN', new_y='NEXT')
        self.set_x(24)
        self.set_font('DJS', '', 11)
        self.set_text_color(220, 220, 220)
        self.multi_cell(160, 6, 'Inicial: USD 1.370  |  Mensual Wolfim: USD 499  |  Pauta sugerida: USD 300-600/mes pagada directamente a Google')

        y2 = 170
        self.set_text_color(*GOLD)
        self.set_font('DJS', 'B', 10)
        self.set_xy(18, y2)
        self.cell(0, 6, 'MODULOS CUBIERTOS', new_x='LMARGIN', new_y='NEXT')
        modules = [
            'Web Premium B2B Industrial',
            'Mantenimiento Esencial / Growth',
            'Google Ads B2B',
            'LinkedIn Autoridad B2B',
            'Instagram Presencia Visual',
            'Motor de Contenidos B2B',
        ]
        self.set_font('DJS', '', 12)
        self.set_text_color(240, 240, 240)
        for mod in modules:
            self.set_x(24)
            self.cell(0, 8, f'- {mod}', new_x='LMARGIN', new_y='NEXT')

        self.set_xy(18, 258)
        self.set_font('DJS', 'I', 9)
        self.set_text_color(180, 180, 180)
        self.multi_cell(170, 5.5, 'Documento generado desde la propuesta ampliada archivada en Obsidian. Formato PDF preparado para revision y presentacion.')
        self.is_cover = False

    def rounded_rect(self, x, y, w, h, r, style=''):
        # FPDF built-in rounded_rect may not exist in all installs; emulate with regular rect.
        self.rect(x, y, w, h, style)

    def section(self, title: str):
        self.ln(3)
        if self.get_y() > 260:
            self.add_page()
        self.set_font('DJS', 'B', 15)
        self.set_text_color(*BLUE)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(*GOLD)
        self.set_line_width(0.8)
        self.line(12, self.get_y(), 80, self.get_y())
        self.set_line_width(0.2)
        self.ln(4)

    def subsection(self, title: str):
        if self.get_y() > 266:
            self.add_page()
        self.set_font('DJS', 'B', 11.5)
        self.set_text_color(*TEXT)
        self.cell(0, 7, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def paragraph(self, text: str):
        if not text:
            return
        self.set_font('DJS', '', 9.6)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.6, text)
        self.ln(1.2)

    def bullet(self, text: str, indent: int = 0):
        x = 16 + indent
        if self.get_y() > 270:
            self.add_page()
        self.set_x(x)
        self.set_font('DJS', 'B', 10)
        self.set_text_color(*GOLD_DARK)
        self.cell(4, 5.8, chr(8226))
        self.set_font('DJS', '', 9.5)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.8, text)
        self.ln(0.2)

    def numbered(self, n: str, text: str):
        if self.get_y() > 270:
            self.add_page()
        self.set_x(16)
        self.set_font('DJS', 'B', 9.8)
        self.set_text_color(*GOLD_DARK)
        self.cell(8, 5.8, f'{n}.')
        self.set_font('DJS', '', 9.5)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.8, text)
        self.ln(0.2)

    def callout(self, text: str):
        if self.get_y() > 264:
            self.add_page()
        self.set_fill_color(*SOFT)
        self.set_draw_color(232, 221, 188)
        start_x = 14
        start_y = self.get_y()
        self.rect(start_x, start_y, 182, 9, 'FD')
        self.set_xy(start_x + 3, start_y + 1.5)
        self.set_font('DJS', 'B', 9.3)
        self.set_text_color(*TEXT)
        self.cell(176, 5.5, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def divider(self):
        self.set_draw_color(*LINE)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(3)


def parse_and_render(pdf: ProposalPDF, text: str):
    lines = strip_frontmatter(text).splitlines()
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            pdf.ln(1.5)
            continue
        if stripped == '---':
            pdf.divider()
            continue
        if stripped.startswith('# '):
            # Cover already handles main title
            continue
        if stripped.startswith('## '):
            pdf.section(clean_md(stripped[3:]))
            continue
        if stripped.startswith('### '):
            pdf.subsection(clean_md(stripped[4:]))
            continue
        if re.match(r'^\d+\.\s+', stripped):
            n, txt = stripped.split('.', 1)
            pdf.numbered(n, clean_md(txt.strip()))
            continue
        if stripped.startswith('- '):
            pdf.bullet(clean_md(stripped[2:]))
            continue

        cleaned = clean_md(stripped)
        if cleaned.startswith(('Inversion:', 'Plazo:', 'Inicial:', 'Mensual:', 'Mensual Wolfim:', 'Pauta:', 'USD ', 'LinkedIn + Instagram:')):
            pdf.callout(cleaned)
        elif re.match(r'^(USD\s?[0-9]|\*?USD\s?[0-9])', cleaned):
            pdf.callout(cleaned.replace('*', ''))
        else:
            pdf.paragraph(cleaned)


def main():
    text = SRC.read_text(encoding='utf-8')
    pdf = ProposalPDF()
    pdf.set_title('Propuesta modular Construvial - Wolfim')
    pdf.set_author('Hermes Agent / Wolfim')
    pdf.set_creator('Hermes Agent')
    pdf.cover_page()
    pdf.add_page()
    parse_and_render(pdf, text)
    pdf.output(str(OUT))
    print(OUT)


if __name__ == '__main__':
    main()
