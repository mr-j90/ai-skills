"""
IES branded document component library.

Provides reusable styled flowables for building team-shareable PDFs:
- IES brand palette (PRIMARY, ACCENT, SUCCESS, WARN, etc.)
- Paragraph styles (title, h1, h2, h3, body, bullet, code)
- Component builders (callouts, comparison tables, step tables, flow diagrams,
  data tables, code blocks, horizontal rules)

All table builders use Paragraph cells (NOT raw strings) so text wraps cleanly
and HTML entities like &harr; and &mdash; render correctly.
"""
import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem,
    Image, KeepTogether
)

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
PRIMARY = colors.HexColor("#1f2937")       # slate-800 — body text, headers
ACCENT = colors.HexColor("#2563eb")        # blue-600 — H2, info accents
ACCENT_LIGHT = colors.HexColor("#dbeafe")  # blue-100 — info callout bg
SUCCESS = colors.HexColor("#059669")       # emerald-600 — good callouts
SUCCESS_LIGHT = colors.HexColor("#d1fae5")
WARN = colors.HexColor("#d97706")          # amber-600 — warn callouts
WARN_LIGHT = colors.HexColor("#fef3c7")
MUTED = colors.HexColor("#6b7280")         # gray-500 — captions, footer
LIGHT_BG = colors.HexColor("#f3f4f6")      # gray-100 — table header tint
BORDER = colors.HexColor("#e5e7eb")        # gray-200 — table grids, rules
ALT_ROW = colors.HexColor("#fafafa")       # alternating table rows
CODE_BG = colors.HexColor("#0f172a")       # slate-900 — code block bg
CODE_FG = colors.HexColor("#e2e8f0")       # slate-200 — code block fg

# Diagram box accent colors (used by flow_diagram)
DIAGRAM_COLORS = [
    colors.HexColor("#0ea5e9"),   # sky-500
    colors.HexColor("#2563eb"),   # blue-600
    colors.HexColor("#7c3aed"),   # violet-600
    colors.HexColor("#059669"),   # emerald-600
    colors.HexColor("#dc2626"),   # red-600
    colors.HexColor("#d97706"),   # amber-600
]


# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
def build_styles():
    """Return a dict of paragraph styles. Call once per document build."""
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "IESTitle", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=22, leading=28,
            textColor=PRIMARY, spaceAfter=6, alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "IESSubtitle", parent=base["Normal"],
            fontName="Helvetica", fontSize=11, leading=14,
            textColor=MUTED, spaceAfter=18, alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "IESH1", parent=base["Heading1"],
            fontName="Helvetica-Bold", fontSize=16, leading=20,
            textColor=PRIMARY, spaceBefore=10, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "IESH2", parent=base["Heading2"],
            fontName="Helvetica-Bold", fontSize=13, leading=16,
            textColor=ACCENT, spaceBefore=8, spaceAfter=4,
        ),
        "h3": ParagraphStyle(
            "IESH3", parent=base["Heading3"],
            fontName="Helvetica-Bold", fontSize=11, leading=14,
            textColor=PRIMARY, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "IESBody", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=PRIMARY, spaceAfter=6, alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "IESBullet", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=PRIMARY, leftIndent=14, bulletIndent=2, spaceAfter=3,
        ),
        "muted": ParagraphStyle(
            "IESMuted", parent=base["Normal"],
            fontName="Helvetica", fontSize=9, leading=12,
            textColor=MUTED, alignment=TA_LEFT,
        ),
        "callout": ParagraphStyle(
            "IESCallout", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=14, textColor=PRIMARY,
            leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "IESCode", parent=base["Code"],
            fontName="Courier", fontSize=8.5, leading=11,
            textColor=CODE_FG, backColor=CODE_BG,
            leftIndent=8, rightIndent=8,
            spaceBefore=6, spaceAfter=10, borderPadding=(8, 8, 8, 8),
        ),
    }


# ---------------------------------------------------------------------------
# Component builders
# ---------------------------------------------------------------------------
def cover_logo(logo_path, width_inches=1.4, aspect=1.786):
    """Branded logo for the cover page. aspect = width/height of the source."""
    img = Image(logo_path, width=width_inches * inch,
                height=(width_inches / aspect) * inch)
    img.hAlign = "LEFT"
    return img


def hr(width_inches=6.5, color=BORDER):
    """Thin horizontal rule."""
    t = Table([[""]], colWidths=[width_inches * inch], rowHeights=[1])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, color)]))
    return t


def callout(text, kind="info", styles=None, width_inches=6.3):
    """
    Colored callout box with a left accent bar.
    kind: "info" (blue), "good" (green), "warn" (amber).
    """
    color_map = {
        "info": (ACCENT, ACCENT_LIGHT),
        "good": (SUCCESS, SUCCESS_LIGHT),
        "warn": (WARN, WARN_LIGHT),
    }
    border, bg = color_map.get(kind, color_map["info"])
    p = Paragraph(text, styles["callout"])
    t = Table([[p]], colWidths=[width_inches * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, 0), 3, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def data_table(rows, col_widths_inches, styles, first_col_bold=True):
    """
    Generic data table with header row + body. All cells become Paragraphs
    so text wraps and HTML entities render. `rows[0]` is the header.

    rows: list[list[str]]
    col_widths_inches: list[float]
    """
    head_style = ParagraphStyle(
        "DTHead", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, alignment=TA_LEFT, textColor=colors.white,
    )
    cell_style = ParagraphStyle(
        "DTCell", parent=styles["body"], fontSize=9, leading=12, alignment=TA_LEFT,
    )
    label_style = ParagraphStyle(
        "DTLabel", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, alignment=TA_LEFT,
    )

    def cell(text, header=False, label=False):
        if header:
            return Paragraph(text, head_style)
        if label:
            return Paragraph(text, label_style)
        return Paragraph(text, cell_style)

    para_rows = [[cell(c, header=True) for c in rows[0]]]
    for row in rows[1:]:
        para_rows.append([
            cell(c, label=(first_col_bold and i == 0))
            for i, c in enumerate(row)
        ])

    t = Table(
        para_rows,
        colWidths=[w * inch for w in col_widths_inches],
        repeatRows=1,
    )
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
    ]
    if first_col_bold:
        style.append(("BACKGROUND", (0, 1), (0, -1), LIGHT_BG))
    t.setStyle(TableStyle(style))
    return t


def comparison_table(dimensions, option_a_label, option_b_label,
                     option_a_values, option_b_values, styles,
                     label_width=1.3, col_width=2.6):
    """
    Two-option side-by-side comparison table.
    dimensions: list[str] — left column labels (e.g. "Where it runs", "Cost")
    option_a_label / option_b_label: column headers
    option_a_values / option_b_values: list[str] aligned with dimensions
    """
    rows = [["Dimension", option_a_label, option_b_label]]
    for dim, a, b in zip(dimensions, option_a_values, option_b_values):
        rows.append([dim, a, b])
    return data_table(
        rows,
        col_widths_inches=[label_width, col_width, col_width],
        styles=styles,
        first_col_bold=True,
    )


def step_table(steps, styles, col_widths_inches=(0.35, 1.3, 4.85)):
    """
    Numbered step table with auto-incremented index.
    steps: list[(component_name, description)]
    """
    head_style = ParagraphStyle(
        "STHead", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=9, leading=11, alignment=TA_LEFT, textColor=colors.white,
    )
    num_style = ParagraphStyle(
        "STNum", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, alignment=TA_CENTER, textColor=ACCENT,
    )
    comp_style = ParagraphStyle(
        "STComp", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, alignment=TA_LEFT, textColor=PRIMARY,
    )
    cell_style = ParagraphStyle(
        "STCell", parent=styles["body"], fontSize=9, leading=12, alignment=TA_LEFT,
    )

    rows = [[
        Paragraph("#", head_style),
        Paragraph("Component", head_style),
        Paragraph("What happens", head_style),
    ]]
    for i, (component, what) in enumerate(steps, start=1):
        rows.append([
            Paragraph(str(i), num_style),
            Paragraph(component, comp_style),
            Paragraph(what, cell_style),
        ])

    t = Table(
        rows,
        colWidths=[w * inch for w in col_widths_inches],
        repeatRows=1,
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
    ]))
    return t


def flow_diagram(boxes, styles, box_width_inches=2.3):
    """
    Vertical flow diagram with colored boxes connected by arrows.
    boxes: list[(title, subtitle)] — colors auto-assigned from DIAGRAM_COLORS

    Example: [("UI", "Browser"), ("API", "FastAPI"), ("DB", "Postgres")]
    """
    box_title = ParagraphStyle(
        "FDTitle", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=10, leading=12, alignment=TA_CENTER, textColor=colors.white,
    )
    box_sub = ParagraphStyle(
        "FDSub", parent=styles["body"], fontName="Helvetica",
        fontSize=8, leading=10, alignment=TA_CENTER,
        textColor=colors.HexColor("#cbd5e1"),
    )
    arrow = ParagraphStyle(
        "FDArrow", parent=styles["body"], fontName="Helvetica-Bold",
        fontSize=14, leading=18, alignment=TA_CENTER, textColor=ACCENT,
    )

    def make_box(title, sub, color):
        cell = [[Paragraph(title, box_title)], [Paragraph(sub, box_sub)]]
        t = Table(cell, colWidths=[box_width_inches * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        return t

    arrow_down = Paragraph("&darr;", arrow)
    flowables = []
    for i, (title, sub) in enumerate(boxes):
        color = DIAGRAM_COLORS[i % len(DIAGRAM_COLORS)]
        flowables.append(make_box(title, sub, color))
        if i < len(boxes) - 1:
            flowables.append(arrow_down)

    rows = [[f] for f in flowables]
    container = Table(rows, colWidths=[box_width_inches * inch], hAlign="CENTER")
    container.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return container


def code_block(code_text, styles):
    """
    Dark-themed code block. Use <br/> for line breaks; escape < > & as
    HTML entities (&lt; &gt; &amp;).
    """
    wrapped = (
        f"<font face='Courier' color='{CODE_FG.hexval()}'>{code_text}</font>"
    )
    return Paragraph(wrapped, styles["code"])


def bullet_list(items, styles):
    """Standard bullet list. items: list[str] (HTML allowed)."""
    return ListFlowable(
        [ListItem(Paragraph(text, styles["bullet"])) for text in items],
        bulletType="bullet",
    )


def section(heading, body_text, styles, level="h1"):
    """Heading + body paragraph as a KeepTogether group (avoids orphans)."""
    return KeepTogether([
        Paragraph(heading, styles[level]),
        Paragraph(body_text, styles["body"]),
    ])


def keep_together(*flowables):
    """Wrap a sequence of flowables so they stay on the same page."""
    return KeepTogether(list(flowables))
