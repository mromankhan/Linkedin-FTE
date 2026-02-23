"""
Carousel Generator — Creates styled PDF slides from text content.
LinkedIn renders each PDF page as one swipeable carousel slide.

Usage:
    from carousel_generator import create_carousel_pdf
    pdf_path = create_carousel_pdf(
        title="5 AI Tools That Save 3 Hours Daily",
        slides=[
            {"heading": "The Problem", "body": "We waste hours on tasks AI can handle in minutes."},
            {"heading": "Tool #1: Cursor", "body": "AI code editor. Writes 60% of your boilerplate."},
            ...
        ],
        output_path="vault/Pending_Approval/CAROUSEL_my-topic.pdf"
    )
"""

from pathlib import Path
from fpdf import FPDF
import os


# ─── Color Palette ───────────────────────────────────────────────
BG_COLOR        = (15, 23, 42)      # Dark navy background
ACCENT_COLOR    = (99, 102, 241)    # Indigo accent
TEXT_WHITE      = (255, 255, 255)
TEXT_LIGHT      = (203, 213, 225)
TEXT_MUTED      = (148, 163, 184)
SLIDE_NUMBER_BG = (30, 41, 59)


WINDOWS_FONTS = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
]
WINDOWS_FONTS_BOLD = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
]


def _find_font(paths: list) -> str | None:
    for p in paths:
        if Path(p).exists():
            return p
    return None


class CarouselPDF(FPDF):
    """Custom PDF with LinkedIn carousel styling."""

    def __init__(self, brand_name: str = ""):
        super().__init__(orientation="L", unit="mm", format=(200, 200))  # Square format
        self.brand_name = brand_name
        self.set_auto_page_break(auto=False)

        # Load Unicode font if available (for special chars)
        regular = _find_font(WINDOWS_FONTS)
        bold = _find_font(WINDOWS_FONTS_BOLD)
        if regular and bold:
            self.add_font("UniFont", "", regular)
            self.add_font("UniFont", "B", bold)
            self._uni = True
        else:
            self._uni = False

    def _font(self, style: str = "", size: int = 12):
        if self._uni:
            self.set_font("UniFont", style, size)
        else:
            # Fallback: strip non-latin chars handled by fpdf
            self.set_font("Helvetica", style, size)

    def _set_bg(self):
        """Fill page with dark background."""
        self.set_fill_color(*BG_COLOR)
        self.rect(0, 0, 200, 200, "F")

    def _accent_bar(self, x: float, y: float, w: float = 8, h: float = 40):
        """Draw vertical accent bar."""
        self.set_fill_color(*ACCENT_COLOR)
        self.rect(x, y, w, h, "F")

    def _slide_number(self, current: int, total: int):
        """Draw slide number in bottom-right corner."""
        self.set_fill_color(*SLIDE_NUMBER_BG)
        self.rect(160, 178, 38, 20, "F")
        self._font("", 9)
        self.set_text_color(*TEXT_MUTED)
        self.set_xy(160, 183)
        self.cell(38, 10, f"{current} / {total}", align="C")

    def _brand_tag(self):
        """Draw brand name bottom-left."""
        if not self.brand_name:
            return
        self._font("B", 8)
        self.set_text_color(*ACCENT_COLOR)
        self.set_xy(10, 185)
        self.cell(80, 10, self.brand_name.upper())

    def cover_slide(self, title: str, subtitle: str, slide_num: int, total: int):
        """First slide — big title."""
        self.add_page()
        self._set_bg()

        # Accent bar left
        self._accent_bar(10, 40, 8, 120)

        # Title
        self._font("B", 28)
        self.set_text_color(*TEXT_WHITE)
        self.set_xy(28, 45)
        self.multi_cell(160, 16, title, align="L")

        # Subtitle
        self._font("", 14)
        self.set_text_color(*TEXT_LIGHT)
        y = self.get_y() + 8
        self.set_xy(28, y)
        self.multi_cell(160, 9, subtitle, align="L")

        # CTA at bottom
        self._font("", 10)
        self.set_text_color(*ACCENT_COLOR)
        self.set_xy(28, 168)
        self.cell(160, 8, "Swipe to learn more >>")

        self._slide_number(slide_num, total)
        self._brand_tag()

    def content_slide(self, heading: str, body: str, slide_num: int, total: int, number_label: str = ""):
        """Content slide with heading and body text."""
        self.add_page()
        self._set_bg()

        # Top accent line
        self.set_fill_color(*ACCENT_COLOR)
        self.rect(10, 10, 180, 3, "F")

        # Number label (e.g. "01", "02")
        if number_label:
            self._font("B", 48)
            self.set_text_color(30, 41, 59)
            self.set_xy(140, 18)
            self.cell(50, 40, number_label, align="R")

        # Heading
        self._font("B", 22)
        self.set_text_color(*TEXT_WHITE)
        self.set_xy(15, 22)
        self.multi_cell(140, 13, heading, align="L")

        # Divider
        y_after_heading = self.get_y() + 5
        self.set_fill_color(*ACCENT_COLOR)
        self.rect(15, y_after_heading, 40, 1.5, "F")

        # Body text — replace unicode arrows with ASCII
        body_clean = body.replace("\u2192", "->").replace("\u2190", "<-")
        self._font("", 13)
        self.set_text_color(*TEXT_LIGHT)
        self.set_xy(15, y_after_heading + 10)
        self.multi_cell(170, 8, body_clean, align="L")

        self._slide_number(slide_num, total)
        self._brand_tag()

    def cta_slide(self, cta_text: str, hashtags: str, slide_num: int, total: int):
        """Final CTA slide."""
        self.add_page()
        self._set_bg()

        # Big centered accent circle (decorative)
        self.set_fill_color(*ACCENT_COLOR)
        self.ellipse(80, 20, 40, 40, "F")

        # Star in circle
        self._font("B", 20)
        self.set_text_color(*TEXT_WHITE)
        self.set_xy(80, 26)
        self.cell(40, 28, "*", align="C")

        # CTA text — strip emoji
        cta_clean = cta_text.replace("\U0001f447", "").replace("\u2b07", "").strip()
        self._font("B", 18)
        self.set_text_color(*TEXT_WHITE)
        self.set_xy(15, 72)
        self.multi_cell(170, 11, cta_clean, align="C")

        # Hashtags
        self._font("", 10)
        self.set_text_color(*ACCENT_COLOR)
        y = self.get_y() + 8
        self.set_xy(15, y)
        self.multi_cell(170, 7, hashtags, align="C")

        # Follow line
        self._font("B", 12)
        self.set_text_color(*TEXT_MUTED)
        self.set_xy(15, 172)
        self.cell(170, 8, "Follow for more Tech & AI insights", align="C")

        self._slide_number(slide_num, total)
        self._brand_tag()


def create_carousel_pdf(
    title: str,
    subtitle: str,
    slides: list[dict],
    cta_text: str,
    hashtags: list[str],
    output_path: str,
    brand_name: str = "",
) -> Path:
    """
    Create a styled carousel PDF.

    Args:
        title:       Cover slide title
        subtitle:    Cover slide subtitle
        slides:      List of dicts with keys: heading (str), body (str)
        cta_text:    Final slide call-to-action text
        hashtags:    List of hashtag strings (without #)
        output_path: Where to save the PDF
        brand_name:  Optional brand/author name shown on each slide

    Returns:
        Path to the generated PDF
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    total_slides = 2 + len(slides)  # cover + content slides + CTA
    pdf = CarouselPDF(brand_name=brand_name)

    # Cover slide
    pdf.cover_slide(title, subtitle, slide_num=1, total=total_slides)

    # Content slides
    for i, slide in enumerate(slides, start=1):
        number_label = f"{i:02d}"
        pdf.content_slide(
            heading=slide.get("heading", ""),
            body=slide.get("body", ""),
            slide_num=i + 1,
            total=total_slides,
            number_label=number_label,
        )

    # CTA slide
    tags_str = "  ".join(f"#{h.lstrip('#')}" for h in hashtags)
    pdf.cta_slide(cta_text, tags_str, slide_num=total_slides, total=total_slides)

    pdf.output(str(output))
    print(f"[Carousel] PDF created: {output}  ({total_slides} slides)")
    return output


# ─── Quick test ───────────────────────────────────────────────────
if __name__ == "__main__":
    path = create_carousel_pdf(
        title="5 AI Tools That Replaced 3 Hours of My Day",
        subtitle="A practical guide for developers and founders",
        slides=[
            {
                "heading": "The Problem",
                "body": "Most developers spend 3+ hours daily on repetitive tasks.\n\nResearch. Boilerplate. Meeting notes. Follow-ups.\n\nAI can handle all of this — if you know which tools to use.",
            },
            {
                "heading": "Cursor",
                "body": "AI-native code editor.\n\n→ Writes 60% of my boilerplate automatically\n→ Understands full codebase context\n→ Suggests entire functions as you type\n\nTime saved: ~45 min/day",
            },
            {
                "heading": "Perplexity",
                "body": "AI search with cited sources.\n\n→ Research that took 30 min now takes 5\n→ Always shows source links\n→ Great for technical comparisons\n\nTime saved: ~30 min/day",
            },
            {
                "heading": "Claude",
                "body": "Complex reasoning & writing.\n\n→ Debugging logic errors\n→ Drafting technical docs\n→ Code reviews and refactoring\n\nTime saved: ~60 min/day",
            },
            {
                "heading": "The Real Unlock",
                "body": "It's not about individual tools.\n\nIt's about chaining them:\n\nPerplexity → Claude → Notion → Zapier\n\nWhen tools work together, hours disappear from your schedule.",
            },
        ],
        cta_text="Which AI tool has saved you the most time?\nDrop it in the comments 👇",
        hashtags=["AI", "Tech", "SoftwareDevelopment", "Automation", "Productivity"],
        output_path="test_carousel.pdf",
        brand_name="@YourLinkedIn",
    )
    print(f"Test carousel: {path}")
