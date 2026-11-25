"""Widescreen maths review PDF layout for ReportLab and Matplotlib."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from matplotlib import get_data_path
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import MathTextParser
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


WIDTH, HEIGHT = 960, 540
LEFT, RIGHT = 54, WIDTH - 54
INK = HexColor("#17212B")
NAVY = HexColor("#173554")
SLATE = HexColor("#465C70")
RULE = HexColor("#B8C7D3")

MATH_PARSER = MathTextParser("path")


@dataclass(frozen=True)
class Math:
    """A LaTeX-style maths fragment for use alongside text."""

    tex: str


def register_fonts():
    bundled = Path(get_data_path()) / "fonts" / "ttf"
    liberation = Path("/usr/share/fonts/truetype/liberation")
    for name, preferred, fallback in (
        ("ReviewSans", "LiberationSans-Regular.ttf", "DejaVuSans.ttf"),
        ("ReviewSansBold", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"),
    ):
        preferred_path = liberation / preferred
        path = preferred_path if preferred_path.is_file() else bundled / fallback
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(path)))


@lru_cache(maxsize=256)
def parse_math(tex, size):
    properties = FontProperties(size=size, math_fontfamily="stix")
    return MATH_PARSER.parse(f"${tex}$", dpi=72, prop=properties)


class ReviewPDF:
    """One PDF page per original or practice question, plus compact bookends."""

    def __init__(self, output, year, assessment, *, pages):
        if pages < 1:
            raise ValueError("Specify a positive total page count.")
        register_fonts()
        self.canvas = Canvas(str(output), pagesize=(WIDTH, HEIGHT), pageCompression=1)
        self.strapline = f"{year} Maths  /  {assessment} Review"
        self.canvas.setTitle(f"{year} Maths {assessment} Review Lesson")
        self.pages = pages
        self.number = 0

    def _text(self, x, y, value, size, *, bold=False, right=False, colour=INK):
        self.canvas.setFont("ReviewSansBold" if bold else "ReviewSans", size)
        self.canvas.setFillColor(colour)
        draw = self.canvas.drawRightString if right else self.canvas.drawString
        draw(x, y, value)

    def page(self, title, status):
        """Start a page and add a bookmark. Draw content below y=415."""
        if self.number >= self.pages:
            raise ValueError("The page count exceeds the declared total.")
        title_width = pdfmetrics.stringWidth(title, "ReviewSansBold", 36)
        if not title_width or title_width * 28 / 36 > RIGHT - LEFT:
            raise ValueError("Use a shorter page title.")
        strip_width = pdfmetrics.stringWidth(self.strapline + status, "ReviewSansBold", 15)
        if strip_width + 20 > RIGHT - LEFT:
            raise ValueError("Use a shorter page label.")
        if self.number:
            self.canvas.showPage()
        self.number += 1
        self._text(LEFT, 503, self.strapline, 15, bold=True, colour=NAVY)
        self._text(RIGHT, 503, status, 15, bold=True, right=True, colour=NAVY)
        self._rule(LEFT, 487, RIGHT, 487)
        title_size = min(36, (RIGHT - LEFT) * 36 / title_width)
        self._text(LEFT, 443, title, title_size, bold=True, colour=NAVY)
        self._text(RIGHT, 24, f"{self.number} / {self.pages}", 12.5, right=True, colour=SLATE)
        key = f"page-{self.number}"
        self.canvas.bookmarkPage(key)
        self.canvas.addOutlineEntry(f"{status} · {title}", key)

    def _rule(self, x0, y0, x1, y1):
        self.canvas.setStrokeColor(RULE)
        self.canvas.setLineWidth(0.9)
        self.canvas.line(x0, y0, x1, y1)

    def divider(self, x=480, top=386, bottom=55):
        self._rule(x, top, x, bottom)

    def note(self, message, *, y=407, left=LEFT):
        self._text(left, y, message, 18, colour=SLATE)

    def _math(self, x, y, parsed):
        pdf = self.canvas
        pdf.setFillColor(INK)
        for face, glyph_size, code, dx, dy in parsed.glyphs:
            name = Path(face.fname).stem
            if name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(name, face.fname))
            pdf.setFont(name, glyph_size)
            pdf.drawString(x + dx, y + dy, chr(code))
        for dx, dy, w, h in parsed.rects:
            pdf.rect(x + dx, y + dy, w, h, fill=1, stroke=0)

    def line(self, y, *runs, left=LEFT, right=RIGHT, size=24, label=None, points=None):
        """Draw one line. Wrap longer prompts manually using several calls."""
        label_width = max(40, pdfmetrics.stringWidth(label, "ReviewSansBold", size - 2) + 12) if label else 0
        if points is None:
            marks_width = 0
        else:
            marks_width = pdfmetrics.stringWidth(f"({points})", "ReviewSansBold", 17) + 14
        formatted = []
        for run in runs:
            if isinstance(run, Math):
                content = parse_math(run.tex, size + 2)
                formatted.append((True, content, content.width))
            else:
                formatted.append((False, run, pdfmetrics.stringWidth(run, "ReviewSans", size)))
        x = left + label_width
        if x + sum(width for _, _, width in formatted) + marks_width > right + 0.1:
            raise ValueError(f"Line is too wide on page {self.number}: {runs!r}")
        if label:
            self._text(left, y, label, size - 2, bold=True, colour=NAVY)
        for is_math, content, width in formatted:
            if is_math:
                self._math(x, y, content)
            else:
                self._text(x, y, content, size)
            x += width
        if points is not None:
            self._text(right, y, f"({points})", 17, bold=True, right=True, colour=NAVY)

    def equation(self, y, tex, *, left=LEFT, right=RIGHT, size=29):
        """Centre a displayed equation in the given horizontal bounds."""
        parsed = parse_math(tex, size)
        if parsed.width > right - left:
            raise ValueError(f"Equation is too wide on page {self.number}: {tex}")
        self._math((left + right - parsed.width) / 2, y, parsed)

    def _prompt(self, number, question, *, left, right, top, height):
        if not question or 32 * len(question) + 25 > height:
            raise ValueError(f"Leave working space under question {number}, or lay out the page manually.")
        for i, content in enumerate(question):
            runs = (content,) if isinstance(content, (str, Math)) else content
            y = top - 32 * (i + 1)
            if i == 0:
                self.line(y, *runs, left=left, right=right, label=f"{number}.", size=22)
            else:
                self.line(y, *runs, left=left + 40, right=right, size=22)

    def starter(self, questions, *, instruction="Show your working."):
        """Lay out four short prompts in a two-by-two grid."""
        if len(questions) != 4:
            raise ValueError("The starter grid takes four questions.")
        self.page("Starter", "5 minutes")
        self.note(instruction)
        gap, height = 17, 160
        width = (RIGHT - LEFT - gap) / 2
        for i, question in enumerate(questions):
            row, col = divmod(i, 2)
            left = LEFT + col * (width + gap)
            top = 388 - row * (height + gap)
            self.canvas.setStrokeColor(RULE)
            self.canvas.setLineWidth(1)
            self.canvas.rect(left, top - height, width, height, fill=0)
            self._prompt(i + 1, question, left=left + 16, right=left + width - 16, top=top, height=height)

    def mixed_practice(self, questions, *, instruction="Show your working."):
        """Lay out short questions 1–3 on the left and 4–5 on the right."""
        if len(questions) != 5:
            raise ValueError("The closing practice page takes five questions.")
        self.page("Mixed practice", "Independent practice")
        self.note(instruction)
        self.divider()
        for start, end, left, right in ((0, 3, LEFT, 452), (3, 5, 508, RIGHT)):
            height = 334 / (end - start)
            for i in range(start, end):
                self._prompt(i + 1, questions[i], left=left, right=right,
                             top=389 - (i - start) * height, height=height)

    def save(self):
        if self.number != self.pages:
            raise ValueError(f"Declared {self.pages} pages but built {self.number}.")
        self.canvas.save()
