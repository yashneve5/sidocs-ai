from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas
from datetime import datetime
import os

# ── Brand colours ──────────────────────────────────────────
SIEMENS_TEAL   = colors.HexColor("#009999")
SIEMENS_DARK   = colors.HexColor("#000028")
SIEMENS_LIGHT  = colors.HexColor("#EBF7F7")
ACCENT_GREY    = colors.HexColor("#F5F5F5")
TEXT_GREY      = colors.HexColor("#555555")
DIVIDER_GREY   = colors.HexColor("#CCCCCC")

# ── Category badge colours ──────────────────────────────────
CAT_COLORS = {
    "Digital Industries":   colors.HexColor("#0066CC"),
    "Smart Infrastructure": colors.HexColor("#009999"),
    "Siemens Mobility":     colors.HexColor("#6600CC"),
    "Financial Services":   colors.HexColor("#CC6600"),
    "Siemens AG":           colors.HexColor("#333333"),
    "AI & Innovation":      colors.HexColor("#CC0066"),
    "Sustainability":       colors.HexColor("#006600"),
}

def get_cat_color(cat):
    return CAT_COLORS.get(cat, SIEMENS_TEAL)


# ── Page numbering ──────────────────────────────────────────
class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *args, **kwargs):
        rl_canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            rl_canvas.Canvas.showPage(self)
        rl_canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page = self._pageNumber
        if page <= 1:
            return  # skip cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_GREY)
        self.drawRightString(
            A4[0] - 1.5*cm,
            1.0*cm,
            f"Page {page} of {page_count}  |  Siemens Press Intelligence Report"
        )
        # footer line
        self.setStrokeColor(DIVIDER_GREY)
        self.line(1.5*cm, 1.3*cm, A4[0] - 1.5*cm, 1.3*cm)
        self.restoreState()


def build_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle("CoverTitle",
            fontSize=28, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=8),

        "cover_sub": ParagraphStyle("CoverSub",
            fontSize=13, textColor=colors.HexColor("#CCFFFF"),
            fontName="Helvetica", alignment=TA_CENTER, spaceAfter=6),

        "cover_meta": ParagraphStyle("CoverMeta",
            fontSize=10, textColor=colors.HexColor("#AADDDD"),
            fontName="Helvetica", alignment=TA_CENTER),

        "article_title": ParagraphStyle("ArticleTitle",
            fontSize=12, textColor=SIEMENS_DARK,
            fontName="Helvetica-Bold", spaceAfter=5, leading=16),

        "date_text": ParagraphStyle("DateText",
            fontSize=9, textColor=TEXT_GREY,
            fontName="Helvetica", spaceAfter=3),

        "url_text": ParagraphStyle("UrlText",
            fontSize=8, textColor=SIEMENS_TEAL,
            fontName="Helvetica", spaceAfter=6),

        "summary_label": ParagraphStyle("SummaryLabel",
            fontSize=9, textColor=SIEMENS_TEAL,
            fontName="Helvetica-Bold", spaceAfter=3),

        "summary_body": ParagraphStyle("SummaryBody",
            fontSize=10, textColor=SIEMENS_DARK,
            fontName="Helvetica", leading=15, spaceAfter=8),

        "toc_title": ParagraphStyle("TocTitle",
            fontSize=16, textColor=SIEMENS_DARK,
            fontName="Helvetica-Bold", spaceAfter=12),

        "toc_entry": ParagraphStyle("TocEntry",
            fontSize=9, textColor=SIEMENS_DARK,
            fontName="Helvetica", leading=14, spaceAfter=2),

        "section_header": ParagraphStyle("SectionHeader",
            fontSize=11, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_CENTER),
    }
    return styles


def clean(text):
    """Sanitise text for ReportLab"""
    if not text:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\u2019", "'")
            .replace("\u2018", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2013", "-")
            .replace("\u2014", "--"))


def make_cover(story, styles, articles, generated_on):
    """Dark branded cover page"""
    W, H = A4

    # Teal background block via a 1-row table spanning full width
    cover_table = Table(
        [[ Paragraph("", styles["cover_title"]) ]],
        colWidths=[W - 3*cm]
    )
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), SIEMENS_DARK),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [SIEMENS_DARK]),
    ]))

    story.append(Spacer(1, 2.5*cm))

    # Logo-style text header
    header_table = Table([[
        Paragraph("SIEMENS", ParagraphStyle("Logo",
            fontSize=11, textColor=SIEMENS_TEAL,
            fontName="Helvetica-Bold", alignment=TA_CENTER))
    ]], colWidths=[W - 3*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), SIEMENS_DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(header_table)

    # Main title block
    title_table = Table([[
        Paragraph("Press Intelligence<br/>Report", ParagraphStyle("MainTitle",
            fontSize=30, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=36))
    ]], colWidths=[W - 3*cm])
    title_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), SIEMENS_DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(title_table)

    # Teal accent bar
    accent = Table([[""]], colWidths=[W - 3*cm], rowHeights=[6])
    accent.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), SIEMENS_TEAL)]))
    story.append(accent)

    # Stats row
    stats_table = Table([[
        Paragraph(f"<b>{len(articles)}</b><br/>Articles", ParagraphStyle("Stat",
            fontSize=14, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18)),
        Paragraph(f"<b>{len(set(a.get('category','') for a in articles))}</b><br/>Categories", ParagraphStyle("Stat",
            fontSize=14, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18)),
        Paragraph(f"<b>{generated_on}</b><br/>Generated", ParagraphStyle("Stat",
            fontSize=12, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18)),
    ]], colWidths=[(W - 3*cm)/3]*3)
    stats_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), SIEMENS_DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
        ("LINEBEFORE",    (1,0), (2,-1),  0.5, colors.HexColor("#334455")),
    ]))
    story.append(stats_table)

    # Bottom dark footer
    footer_table = Table([[
        Paragraph("Confidential — For Internal Use Only", ParagraphStyle("Footer",
            fontSize=9, textColor=colors.HexColor("#AAAAAA"),
            fontName="Helvetica", alignment=TA_CENTER))
    ]], colWidths=[W - 3*cm])
    footer_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), SIEMENS_DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 30),
        ("BOTTOMPADDING", (0,0), (-1,-1), 30),
    ]))
    story.append(footer_table)
    story.append(PageBreak())


def make_toc(story, styles, articles):
    """Clean table of contents"""
    story.append(Paragraph("Table of Contents", styles["toc_title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=SIEMENS_TEAL))
    story.append(Spacer(1, 0.3*cm))

    for i, a in enumerate(articles, 1):
        cat   = a.get("category", "Siemens AG")
        date  = a.get("date", "")
        title = clean(a.get("title", "Untitled"))[:90]
        color = get_cat_color(cat)

        row = Table([[
            Paragraph(f"<b>{i:02d}</b>", ParagraphStyle("Num",
                fontSize=9, textColor=color, fontName="Helvetica-Bold")),
            Paragraph(title, styles["toc_entry"]),
            Paragraph(date,  ParagraphStyle("TocDate",
                fontSize=8, textColor=TEXT_GREY,
                fontName="Helvetica", alignment=TA_RIGHT)),
        ]], colWidths=[0.8*cm, 13.5*cm, 3*cm])
        row.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("ROWBACKGROUNDS",(0,0), (-1,-1),
             [ACCENT_GREY if i % 2 == 0 else colors.white]),
        ]))
        story.append(row)

    story.append(PageBreak())


def make_article_card(story, styles, i, article):
    """One article card with category badge + AI summary"""
    title    = clean(article.get("title",    "Untitled"))
    date     = clean(article.get("date",     "Unknown date"))
    url      =       article.get("url",      "")
    summary  = clean(article.get("summary",  "Summary not available."))
    category = clean(article.get("category", "Siemens AG"))
    cat_color = get_cat_color(article.get("category", "Siemens AG"))

    # ── Header bar: number + category badge ───────────────
    header = Table([[
        Paragraph(f"<b>{i:02d}</b>", ParagraphStyle("CardNum",
            fontSize=11, textColor=colors.white, fontName="Helvetica-Bold")),
        Paragraph(category, ParagraphStyle("CatBadge",
            fontSize=8, textColor=colors.white,
            fontName="Helvetica-Bold", alignment=TA_RIGHT)),
    ]], colWidths=[2*cm, 15.7*cm])
    header.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), cat_color),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (0,-1),  10),
        ("RIGHTPADDING",  (-1,0),(-1,-1), 10),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))

    # ── Body block ────────────────────────────────────────
    body_content = [
        Spacer(1, 0.2*cm),
        Paragraph(title, styles["article_title"]),
        Paragraph(f"📅 {date}", styles["date_text"]),
        Paragraph(f"🔗 {clean(url)}", styles["url_text"]),
        Paragraph("AI Summary", styles["summary_label"]),
    ]

    # Summary box with light background
    summary_table = Table([[
        Paragraph(summary, styles["summary_body"])
    ]], colWidths=[15.7*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), SIEMENS_LIGHT),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, SIEMENS_TEAL),
        ("ROUNDEDCORNERS",(0,0), (-1,-1), [4,4,4,4]),
    ]))

    body_content.append(summary_table)
    body_content.append(Spacer(1, 0.4*cm))

    card = KeepTogether([header] + body_content)
    story.append(card)
    story.append(HRFlowable(width="100%", thickness=0.5, color=DIVIDER_GREY))
    story.append(Spacer(1, 0.3*cm))


def save_to_pdf(articles, filename="output/siemens_press_releases.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    W, H = A4
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.8*cm,   bottomMargin=2*cm
    )

    styles      = build_styles()
    story       = []
    generated   = datetime.now().strftime("%d %b %Y")

    # 1 — Cover
    print("  🎨 Building cover page...")
    make_cover(story, styles, articles, generated)

    # 2 — Table of contents
    print("  📋 Building table of contents...")
    make_toc(story, styles, articles)

    # 3 — Articles
    print(f"  📰 Writing {len(articles)} article cards...")
    for i, article in enumerate(articles, 1):
        print(f"     [{i}/{len(articles)}] {article.get('title','')[:55]}...")
        make_article_card(story, styles, i, article)

    doc.build(story, canvasmaker=NumberedCanvas)
    size_kb = os.path.getsize(filename) // 1024
    print(f"\n✅ PDF saved → {filename}  ({size_kb} KB)")
    return filename
