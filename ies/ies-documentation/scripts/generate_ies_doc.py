#!/usr/bin/env python3
"""
IES branded PDF document generator.

Renders the IES house style: branded cover with logo, slate-on-white body,
blue accent headers, callouts, comparison tables with wrapping cells,
numbered step tables, flow diagrams, and tightened spacing.

Input: a JSON config file describing the document and its sections.
Output: a PDF file at the path given by --output.

Run:
    python generate_ies_doc.py config.json --output report.pdf

See REFERENCE.md for the full config schema and section types.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

# ============================================================
# Brand palette — the IES house style.
# ============================================================
PRIMARY = colors.HexColor("#1f2937")        # slate-800 — body text & dark headers
ACCENT = colors.HexColor("#2563eb")          # blue-600 — H2 headers & info accents
ACCENT_LIGHT = colors.HexColor("#dbeafe")    # blue-100 — info callout bg
SUCCESS = colors.HexColor("#059669")         # emerald-600 — good callout border
SUCCESS_LIGHT = colors.HexColor("#d1fae5")   # emerald-100 — good callout bg
WARN = colors.HexColor("#d97706")            # amber-600 — warn callout border
WARN_LIGHT = colors.HexColor("#fef3c7")      # amber-100 — warn callout bg
MUTED = colors.HexColor("#6b7280")           # gray-500 — subtitles, footers
LIGHT_BG = colors.HexColor("#f3f4f6")        # gray-100 — table label column
BORDER = colors.HexColor("#e5e7eb")          # gray-200 — table borders, hr
ZEBRA = colors.HexColor("#fafafa")           # subtle alt row stripe
CODE_BG = colors.HexColor("#0f172a")         # slate-900 — code block bg
CODE_FG = colors.HexColor("#e2e8f0")         # slate-200 — code block fg

# Default flow-diagram box colors (used if a node doesn't specify one).
FLOW_DEFAULT_COLORS = [
    colors.HexColor("#0ea5e9"),   # sky-500
    colors.HexColor("#2563eb"),   # blue-600
    colors.HexColor("#7c3aed"),   # violet-600
    colors.HexColor("#059669"),   # emerald-600
    colors.HexColor("#dc2626"),   # red-600
]


# ============================================================
# Style sheet
# ============================================================
def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    s: dict[str, ParagraphStyle] = {}

    s["title"] = ParagraphStyle(
        "Title", parent=base["Title"], fontName="Helvetica-Bold",
        fontSize=22, leading=28, textColor=PRIMARY, spaceAfter=6, alignment=TA_LEFT,
    )
    s["subtitle"] = ParagraphStyle(
        "Subtitle", parent=base["Normal"], fontName="Helvetica",
        fontSize=11, leading=14, textColor=MUTED, spaceAfter=18, alignment=TA_LEFT,
    )
    s["h1"] = ParagraphStyle(
        "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
        fontSize=16, leading=20, textColor=PRIMARY, spaceBefore=10, spaceAfter=6,
    )
    s["h2"] = ParagraphStyle(
        "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=16, textColor=ACCENT, spaceBefore=8, spaceAfter=4,
    )
    s["h3"] = ParagraphStyle(
        "H3", parent=base["Heading3"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=PRIMARY, spaceBefore=8, spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "Body", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, leading=14, textColor=PRIMARY, spaceAfter=6, alignment=TA_JUSTIFY,
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", parent=s["body"], leftIndent=14, bulletIndent=2, spaceAfter=3,
    )
    s["muted"] = ParagraphStyle(
        "Muted", parent=s["body"], textColor=MUTED, fontSize=9, leading=12,
    )
    s["callout"] = ParagraphStyle(
        "Callout", parent=s["body"], fontSize=10, leading=14, textColor=PRIMARY,
        leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4,
    )
    s["code"] = ParagraphStyle(
        "Code", parent=base["Code"], fontName="Courier", fontSize=8.5, leading=11,
        textColor=CODE_FG, backColor=CODE_BG,
        leftIndent=8, rightIndent=8, spaceBefore=6, spaceAfter=10,
        borderPadding=(8, 8, 8, 8),
    )
    s["table_header"] = ParagraphStyle(
        "TableHeader", parent=s["body"], fontName="Helvetica-Bold",
        fontSize=10, leading=12, textColor=colors.white, alignment=TA_CENTER,
    )
    s["table_cell"] = ParagraphStyle(
        "TableCell", parent=s["body"], fontSize=9, leading=12, alignment=TA_LEFT, spaceAfter=0,
    )
    s["table_label"] = ParagraphStyle(
        "TableLabel", parent=s["table_cell"], fontName="Helvetica-Bold",
    )
    s["step_num"] = ParagraphStyle(
        "StepNum", parent=s["body"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=ACCENT, alignment=TA_CENTER,
    )
    s["flow_box_title"] = ParagraphStyle(
        "FlowBoxTitle", parent=s["body"], fontName="Helvetica-Bold",
        fontSize=10, leading=12, alignment=TA_CENTER, textColor=colors.white, spaceAfter=0,
    )
    s["flow_box_sub"] = ParagraphStyle(
        "FlowBoxSub", parent=s["body"], fontName="Helvetica",
        fontSize=8, leading=10, alignment=TA_CENTER,
        textColor=colors.HexColor("#cbd5e1"), spaceAfter=0,
    )
    s["flow_arrow"] = ParagraphStyle(
        "FlowArrow", parent=s["body"], fontName="Helvetica-Bold",
        fontSize=14, leading=18, alignment=TA_CENTER, textColor=ACCENT, spaceAfter=0,
    )
    return s


# ============================================================
# Helpers
# ============================================================
def hr(width: float = 6.5 * inch, color=BORDER) -> Table:
    """Thin horizontal rule."""
    t = Table([[""]], colWidths=[width], rowHeights=[1])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, color)]))
    return t


def callout(text: str, kind: str, styles: dict[str, ParagraphStyle]) -> Table:
    """Coloured left-bar callout. kind: info | good | warn."""
    palette = {
        "info": (ACCENT, ACCENT_LIGHT),
        "good": (SUCCESS, SUCCESS_LIGHT),
        "warn": (WARN, WARN_LIGHT),
    }
    border, bg = palette.get(kind, palette["info"])
    p = Paragraph(text, styles["callout"])
    t = Table([[p]], colWidths=[6.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, 0), 3, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def code_block(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Code block with terminal styling. Text may include <br/> for line breaks."""
    # Wrap raw text in a Courier/colour span for the dark background.
    safe = (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>"))
    return Paragraph(
        f"<font face='Courier' color='#e2e8f0'>{safe}</font>",
        styles["code"],
    )


def bullet_list(items: list[str], styles: dict[str, ParagraphStyle]) -> ListFlowable:
    """Bulleted list. Items support inline HTML (<b>, <i>, etc)."""
    return ListFlowable(
        [ListItem(Paragraph(item, styles["bullet"])) for item in items],
        bulletType="bullet",
    )


# ============================================================
# Section renderers — each takes a section dict and returns a list of flowables.
# ============================================================
def render_heading(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    level = section.get("level", 1)
    style = {1: "h1", 2: "h2", 3: "h3"}.get(level, "h1")
    return [Paragraph(section["text"], styles[style])]


def render_paragraph(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    return [Paragraph(section["text"], styles["body"])]


def render_bullets(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    return [bullet_list(section["items"], styles)]


def render_callout(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    return [callout(section["text"], section.get("kind", "info"), styles)]


def render_code(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    out: list = []
    if section.get("title"):
        out.append(Paragraph(section["title"], styles["h3"]))
    out.append(code_block(section["text"], styles))
    return out


def render_hr(_section: dict, _styles: dict[str, ParagraphStyle]) -> list:
    return [hr()]


def render_spacer(section: dict, _styles: dict[str, ParagraphStyle]) -> list:
    return [Spacer(1, section.get("height", 6))]


def render_pagebreak(_section: dict, _styles: dict[str, ParagraphStyle]) -> list:
    return [PageBreak()]


def render_table(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    """Generic table. Cells wrap; first row is the header."""
    rows = section["rows"]
    headers = rows[0]
    body_rows = rows[1:]

    paragraph_rows = [[Paragraph(str(c), styles["table_header"]) for c in headers]]
    for r in body_rows:
        paragraph_rows.append([Paragraph(str(c), styles["table_cell"]) for c in r])

    col_widths = section.get("col_widths")
    if col_widths:
        col_widths = [w * inch for w in col_widths]

    t = Table(paragraph_rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ZEBRA]),
    ]))
    return [t]


def render_comparison(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    """
    Side-by-side comparison table.
    section = {
      "type": "comparison",
      "headers": ["Dimension", "Option A", "Option B"],
      "rows": [
        ["Where it runs", "Cell A", "Cell B"],
        ...
      ],
      "col_widths": [1.3, 2.6, 2.6]   # optional, in inches
    }
    First column is rendered as bold labels with a light-grey background.
    """
    headers = section["headers"]
    rows = section["rows"]

    paragraph_rows = [[Paragraph(h, styles["table_header"]) for h in headers]]
    for r in rows:
        cells = [Paragraph(str(r[0]), styles["table_label"])]
        cells.extend(Paragraph(str(c), styles["table_cell"]) for c in r[1:])
        paragraph_rows.append(cells)

    col_widths = section.get("col_widths") or [1.3] + [
        (6.5 - 1.3) / max(1, len(headers) - 1)
    ] * (len(headers) - 1)
    col_widths = [w * inch for w in col_widths]

    t = Table(paragraph_rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BACKGROUND", (0, 1), (0, -1), LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (1, 1), (-1, -1), [colors.white, ZEBRA]),
    ]))
    return [t]


def render_steps(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    """
    Numbered step table. Three columns: #, component, what happens.
    section = {
      "type": "steps",
      "steps": [
        {"component": "UI", "what": "User submits ..."},
        ...
      ]
    }
    """
    rows: list = [[
        Paragraph("#", styles["table_header"]),
        Paragraph("Component", styles["table_header"]),
        Paragraph("What happens", styles["table_header"]),
    ]]
    for i, step in enumerate(section["steps"], start=1):
        rows.append([
            Paragraph(str(i), styles["step_num"]),
            Paragraph(step["component"], styles["table_label"]),
            Paragraph(step["what"], styles["table_cell"]),
        ])

    t = Table(rows, colWidths=[0.35 * inch, 1.3 * inch, 4.85 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ZEBRA]),
    ]))
    return [t]


def render_flow_diagram(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    """
    Vertical stack of coloured boxes joined by down-arrows.
    section = {
      "type": "flow_diagram",
      "boxes": [
        {"title": "UI", "subtitle": "Browser / Mobile", "color": "#0ea5e9"},
        ...
      ],
      "box_width": 2.3   # optional, inches
    }
    """
    boxes_data = section["boxes"]
    box_width = section.get("box_width", 2.3) * inch

    flowables: list = []
    arrow_para = Paragraph("&darr;", styles["flow_arrow"])

    for i, box in enumerate(boxes_data):
        color_str = box.get("color")
        if color_str:
            color = colors.HexColor(color_str)
        else:
            color = FLOW_DEFAULT_COLORS[i % len(FLOW_DEFAULT_COLORS)]

        cell_rows = [[Paragraph(box["title"], styles["flow_box_title"])]]
        if box.get("subtitle"):
            cell_rows.append([Paragraph(box["subtitle"], styles["flow_box_sub"])])

        box_table = Table(cell_rows, colWidths=[box_width])
        box_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        flowables.append(box_table)
        if i < len(boxes_data) - 1:
            flowables.append(arrow_para)

    rows = [[f] for f in flowables]
    t = Table(rows, colWidths=[box_width], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return [t]


# ============================================================
# Section dispatcher
# ============================================================
RENDERERS = {
    "heading": render_heading,
    "paragraph": render_paragraph,
    "bullets": render_bullets,
    "callout": render_callout,
    "code": render_code,
    "hr": render_hr,
    "spacer": render_spacer,
    "pagebreak": render_pagebreak,
    "table": render_table,
    "comparison": render_comparison,
    "steps": render_steps,
    "flow_diagram": render_flow_diagram,
}


def render_section(section: dict, styles: dict[str, ParagraphStyle]) -> list:
    """
    Render one section. Sections may be wrapped in a `keep_together` flag,
    in which case all the produced flowables are wrapped in a KeepTogether.
    """
    section_type = section["type"]
    if section_type == "group":
        # Container — render every child, optionally wrapped in KeepTogether.
        out: list = []
        for child in section.get("sections", []):
            out.extend(render_section(child, styles))
        if section.get("keep_together"):
            return [KeepTogether(out)]
        return out

    renderer = RENDERERS.get(section_type)
    if renderer is None:
        raise ValueError(f"Unknown section type: {section_type!r}")

    flowables = renderer(section, styles)
    if section.get("keep_together") and len(flowables) > 1:
        return [KeepTogether(flowables)]
    return flowables


# ============================================================
# Cover & top-matter
# ============================================================
def build_cover(config: dict, styles: dict[str, ParagraphStyle]) -> list:
    """Branded cover: logo + title + subtitle + thin rule."""
    out: list = []
    logo_path = config.get("logo_path")
    if logo_path and os.path.exists(logo_path):
        # Aspect ratio 2000:1120 ≈ 1.786:1 (matches the bundled IES logo).
        # If a different logo is supplied, we read its actual size to preserve ratio.
        try:
            from PIL import Image as PILImage
            with PILImage.open(logo_path) as img:
                w, h = img.size
                aspect = w / h if h else 1.786
        except Exception:
            aspect = 1.786
        logo = Image(logo_path, width=1.4 * inch, height=1.4 / aspect * inch)
        logo.hAlign = "LEFT"
        out.append(logo)
        out.append(Spacer(1, 8))

    out.append(Paragraph(config["title"], styles["title"]))
    if config.get("subtitle"):
        out.append(Paragraph(config["subtitle"], styles["subtitle"]))
    out.append(hr())
    out.append(Spacer(1, 6))
    return out


def build_footer_note(config: dict, styles: dict[str, ParagraphStyle]) -> list:
    note = config.get("footer_note")
    if not note:
        return []
    return [
        Spacer(1, 8),
        hr(),
        Spacer(1, 6),
        Paragraph(note, styles["muted"]),
    ]


# ============================================================
# Page decoration — page numbers in the footer
# ============================================================
def make_page_decorator(config: dict):
    """Returns a callback that draws "Page N of M" + an optional footer label."""
    label = config.get("page_footer_label", "")

    def decorator(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(letter[0] - 0.6 * inch, 0.4 * inch, text)
        if label:
            canvas.drawString(0.6 * inch, 0.4 * inch, label)
        canvas.restoreState()

    return decorator


# ============================================================
# Markdown → config converter (minimal, opinionated)
# ============================================================
def _md_inline(text: str) -> str:
    """Convert minimal inline Markdown to the inline HTML the renderer accepts."""
    import re
    # **bold** -> <b>bold</b>  (non-greedy, must contain non-* chars)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # __bold__ -> <b>bold</b>
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
    # *italic* -> <i>italic</i>  (avoid matching ** by requiring non-* on both sides)
    text = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<i>\1</i>", text)
    # `code` -> <font face="Courier">code</font>
    text = re.sub(r"`([^`\n]+?)`", r"<font face='Courier'>\1</font>", text)
    return text


def markdown_to_config(md_text: str, title: str | None = None,
                       subtitle: str | None = None,
                       logo_path: str | None = None) -> dict:
    """
    Convert simple Markdown into the section config.

    Supported syntax:
      # Title           -> document title (first #)
      ## Section        -> H1
      ### Subsection    -> H2
      #### Sub-sub      -> H3
      paragraph text    -> paragraph
      - item            -> bullets
      * item            -> bullets
      > [info] text     -> info callout
      > [warn] text     -> warn callout
      > [good] text     -> good callout
      ```                -> code block delimiter
      ---               -> horizontal rule
      <pagebreak>       -> page break

    Anything fancier (tables, comparisons, flow diagrams, steps) should
    be authored as JSON instead.
    """
    sections: list[dict] = []
    lines = md_text.splitlines()
    i = 0
    detected_title = title
    detected_subtitle = subtitle
    pending_bullets: list[str] = []
    pending_paragraph: list[str] = []

    def flush_bullets():
        if pending_bullets:
            sections.append({"type": "bullets",
                             "items": [_md_inline(b) for b in pending_bullets]})
            pending_bullets.clear()

    def flush_paragraph():
        if pending_paragraph:
            text = " ".join(pending_paragraph).strip()
            if text:
                sections.append({"type": "paragraph", "text": _md_inline(text)})
            pending_paragraph.clear()

    def flush_all():
        flush_bullets()
        flush_paragraph()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_all()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            sections.append({"type": "code", "text": "\n".join(code_lines)})
            i += 1
            continue

        if stripped == "---":
            flush_all()
            sections.append({"type": "hr"})
            i += 1
            continue

        if stripped == "<pagebreak>":
            flush_all()
            sections.append({"type": "pagebreak"})
            i += 1
            continue

        if stripped.startswith("# ") and detected_title is None:
            detected_title = stripped[2:].strip()
            i += 1
            # Optional subtitle on the very next non-empty line if it's plain text
            if (detected_subtitle is None and i < len(lines)
                    and lines[i].strip() and not lines[i].lstrip().startswith(("#", "-", "*", ">"))):
                detected_subtitle = lines[i].strip()
                i += 1
            continue

        if stripped.startswith("#### "):
            flush_all()
            sections.append({"type": "heading", "level": 3, "text": stripped[5:].strip()})
            i += 1
            continue

        if stripped.startswith("### "):
            flush_all()
            sections.append({"type": "heading", "level": 2, "text": stripped[4:].strip()})
            i += 1
            continue

        if stripped.startswith("## "):
            flush_all()
            sections.append({"type": "heading", "level": 1, "text": stripped[3:].strip()})
            i += 1
            continue

        if stripped.startswith(("- ", "* ")):
            flush_paragraph()
            pending_bullets.append(stripped[2:].strip())
            i += 1
            continue

        if stripped.startswith(">"):
            flush_all()
            content = stripped[1:].strip()
            kind = "info"
            for k in ("info", "warn", "good"):
                tag = f"[{k}]"
                if content.startswith(tag):
                    kind = k
                    content = content[len(tag):].strip()
                    break
            sections.append({"type": "callout", "kind": kind, "text": _md_inline(content)})
            i += 1
            continue

        if stripped == "":
            flush_all()
            i += 1
            continue

        # Default: accumulate into a paragraph.
        flush_bullets()
        pending_paragraph.append(stripped)
        i += 1

    flush_all()

    return {
        "title": detected_title or "Untitled Document",
        "subtitle": detected_subtitle,
        "logo_path": logo_path,
        "sections": sections,
    }


# ============================================================
# Main build
# ============================================================
def build_document(config: dict, output_path: str) -> None:
    """Build the PDF from a normalized config dict."""
    styles = build_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.6 * inch, bottomMargin=0.7 * inch,
        title=config.get("title", "IES Document"),
        author=config.get("author", "IES"),
    )

    story: list = []
    story.extend(build_cover(config, styles))
    for section in config.get("sections", []):
        story.extend(render_section(section, styles))
    story.extend(build_footer_note(config, styles))

    decorator = make_page_decorator(config)
    doc.build(story, onFirstPage=decorator, onLaterPages=decorator)


def load_config(input_path: str, logo_override: str | None = None,
                title_override: str | None = None) -> dict:
    """Load JSON or Markdown input and normalize to a config dict."""
    text = Path(input_path).read_text(encoding="utf-8")

    if input_path.endswith((".md", ".markdown")):
        config = markdown_to_config(text, title=title_override, logo_path=logo_override)
    else:
        config = json.loads(text)
        if logo_override:
            config["logo_path"] = logo_override
        if title_override:
            config["title"] = title_override

    # Default to bundled IES logo if no logo specified.
    if not config.get("logo_path"):
        bundled = Path(__file__).resolve().parent.parent / "assets" / "IES_Logo.png"
        if bundled.exists():
            config["logo_path"] = str(bundled)

    return config


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a branded IES PDF document.")
    ap.add_argument("input", help="Path to JSON config or Markdown source file.")
    ap.add_argument("--output", "-o", required=True, help="Output PDF path.")
    ap.add_argument("--logo", help="Optional path to a logo image (overrides config).")
    ap.add_argument("--title", help="Optional title (overrides config).")
    args = ap.parse_args()

    config = load_config(args.input, logo_override=args.logo, title_override=args.title)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    build_document(config, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
