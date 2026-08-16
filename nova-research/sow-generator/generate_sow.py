#!/usr/bin/env python3
"""
SOW Generator — Produces branded PDF Statements of Work.
Usage: python generate_sow.py config.json [--output output.pdf]
"""

import json
import sys
import os
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.units import mm


# ── Brand Colors ──────────────────────────────────────────────
DARK_BG = HexColor("#1a1a2e")
ACCENT = HexColor("#16213e")
LIGHT_ACCENT = HexColor("#e8edf3")
MEDIUM_GRAY = HexColor("#f5f5f8")
TEXT_PRIMARY = HexColor("#1a1a2e")
TEXT_SECONDARY = HexColor("#555566")
BORDER_COLOR = HexColor("#d0d0d8")
WHITE = white


def build_styles():
    """Create all paragraph styles for the SOW."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="SOW_Title",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=WHITE,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name="SOW_Subtitle",
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=HexColor("#ccccdd"),
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name="SOW_SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=DARK_BG,
        spaceBefore=18,
        spaceAfter=8,
        borderPadding=(0, 0, 0, 8),
        leftIndent=12,
        borderWidth=3,
        borderColor=DARK_BG,
        borderRadius=0,
    ))

    styles.add(ParagraphStyle(
        name="SOW_Body",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_PRIMARY,
        spaceBefore=2,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="SOW_BodyBold",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=TEXT_PRIMARY,
        spaceBefore=2,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="SOW_BulletItem",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_PRIMARY,
        leftIndent=24,
        bulletIndent=12,
        spaceBefore=2,
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        name="SOW_TableHeader",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=WHITE,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name="SOW_TableCell",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=TEXT_PRIMARY,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name="SOW_Footer",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=TEXT_SECONDARY,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="SOW_MetaLabel",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=TEXT_SECONDARY,
    ))

    styles.add(ParagraphStyle(
        name="SOW_MetaValue",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_PRIMARY,
    ))

    return styles


def add_header_block(story, config, styles, logo_path):
    """Build a clean header — logo inline with title, thin rule below."""
    page_width = letter[0] - 1.5 * inch

    # Logo + Title side by side in a table (no background)
    title_parts = []
    title_parts.append(Paragraph(config["project_title"], ParagraphStyle(
        name="_hdr_title",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=DARK_BG,
    )))
    title_parts.append(Spacer(1, 2))
    title_parts.append(Paragraph("Statement of Work", ParagraphStyle(
        name="_hdr_sub",
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=TEXT_SECONDARY,
    )))

    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=50, height=50)
        header_data = [[logo, title_parts]]
        col_widths = [65, page_width - 65]
    else:
        header_data = [[title_parts]]
        col_widths = [page_width]

    header_table = Table(header_data, colWidths=col_widths, rowHeights=[70])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (-1, 0), (-1, 0), 8),
        ("RIGHTPADDING", (-1, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_BG, spaceAfter=12))


def add_meta_block(story, config, styles):
    """Add the prepared-for / prepared-by / date block."""
    page_width = letter[0] - 1.5 * inch
    meta_data = [
        [
            Paragraph("<b>Prepared For</b>", styles["SOW_MetaLabel"]),
            Paragraph("<b>Prepared By</b>", styles["SOW_MetaLabel"]),
            Paragraph("<b>Date</b>", styles["SOW_MetaLabel"]),
        ],
        [
            Paragraph(f"{config['client_name']}<br/>{config.get('client_company', '')}", styles["SOW_MetaValue"]),
            Paragraph(config["prepared_by"], styles["SOW_MetaValue"]),
            Paragraph(config["date"], styles["SOW_MetaValue"]),
        ],
    ]

    meta_table = Table(meta_data, colWidths=[page_width * 0.4, page_width * 0.35, page_width * 0.25])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MEDIUM_GRAY),
        ("BACKGROUND", (0, 1), (-1, 1), WHITE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDER_COLOR),
        ("LINEBELOW", (0, 1), (-1, 1), 0.5, BORDER_COLOR),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 16))


def section_header(text, styles):
    """Return a styled section header paragraph."""
    return Paragraph(text, styles["SOW_SectionHeader"])


def bullet_list(items, styles):
    """Return a list of bullet-pointed paragraphs."""
    elements = []
    for item in items:
        elements.append(Paragraph(f"•  {item}", styles["SOW_BulletItem"]))
    return elements


def add_overview(story, config, styles):
    """Add Overview section."""
    story.append(section_header("Overview", styles))
    story.append(Paragraph(config["overview"], styles["SOW_Body"]))
    story.append(Spacer(1, 8))


def add_scope(story, config, styles):
    """Add Scope of Work section."""
    story.append(section_header("Scope of Work", styles))
    story.extend(bullet_list(config["scope_items"], styles))
    story.append(Spacer(1, 8))


def add_deliverables(story, config, styles):
    """Add Deliverables table."""
    story.append(section_header("Deliverables", styles))

    page_width = letter[0] - 1.5 * inch
    header_row = [
        Paragraph("Deliverable", styles["SOW_TableHeader"]),
        Paragraph("Description", styles["SOW_TableHeader"]),
    ]
    table_data = [header_row]

    for d in config["deliverables"]:
        table_data.append([
            Paragraph(d["name"], styles["SOW_TableCell"]),
            Paragraph(d["description"], styles["SOW_TableCell"]),
        ])

    col_widths = [page_width * 0.32, page_width * 0.68]
    deliverables_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    table_style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]

    # Alternating row colors
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            table_style_commands.append(("BACKGROUND", (0, i), (-1, i), MEDIUM_GRAY))

    deliverables_table.setStyle(TableStyle(table_style_commands))
    story.append(deliverables_table)
    story.append(Spacer(1, 8))


def add_timeline(story, config, styles):
    """Add Timeline / Phases table."""
    story.append(section_header("Timeline", styles))

    page_width = letter[0] - 1.5 * inch
    header_row = [
        Paragraph("Phase", styles["SOW_TableHeader"]),
        Paragraph("Duration", styles["SOW_TableHeader"]),
        Paragraph("Description", styles["SOW_TableHeader"]),
    ]
    table_data = [header_row]

    for t in config["timeline"]:
        table_data.append([
            Paragraph(t["phase"], styles["SOW_TableCell"]),
            Paragraph(t["duration"], styles["SOW_TableCell"]),
            Paragraph(t["description"], styles["SOW_TableCell"]),
        ])

    col_widths = [page_width * 0.22, page_width * 0.18, page_width * 0.60]
    timeline_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    table_style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]

    for i in range(1, len(table_data)):
        if i % 2 == 0:
            table_style_commands.append(("BACKGROUND", (0, i), (-1, i), MEDIUM_GRAY))

    timeline_table.setStyle(TableStyle(table_style_commands))
    story.append(timeline_table)
    story.append(Spacer(1, 8))


def add_pricing(story, config, styles):
    """Add Pricing section."""
    story.append(section_header("Pricing", styles))

    pricing = config["pricing"]
    page_width = letter[0] - 1.5 * inch

    pricing_data = [
        [
            Paragraph("Hourly Rate", styles["SOW_TableHeader"]),
            Paragraph("Estimated Hours", styles["SOW_TableHeader"]),
            Paragraph("Total", styles["SOW_TableHeader"]),
        ],
        [
            Paragraph(f"${pricing['rate_per_hour']}/hr", styles["SOW_TableCell"]),
            Paragraph(str(pricing["estimated_hours"]), styles["SOW_TableCell"]),
            Paragraph(f"${pricing['total']:,.2f}", styles["SOW_BodyBold"]),
        ],
    ]

    col_widths = [page_width * 0.33, page_width * 0.34, page_width * 0.33]
    pricing_table = Table(pricing_data, colWidths=col_widths)
    pricing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_ACCENT),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, 1), (-1, 1), 1, DARK_BG),
        ("ALIGN", (0, 1), (-1, 1), "CENTER"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ]))
    story.append(pricing_table)
    story.append(Spacer(1, 4))

    if pricing.get("payment_terms"):
        story.append(Paragraph(
            f"<b>Payment Terms:</b> {pricing['payment_terms']}",
            styles["SOW_Body"]
        ))
    story.append(Spacer(1, 8))


def add_assumptions(story, config, styles):
    """Add Assumptions section."""
    story.append(section_header("Assumptions", styles))
    story.extend(bullet_list(config["assumptions"], styles))
    story.append(Spacer(1, 8))


def add_acceptance_criteria(story, config, styles):
    """Add Acceptance Criteria section."""
    story.append(section_header("Acceptance Criteria", styles))
    story.extend(bullet_list(config["acceptance_criteria"], styles))
    story.append(Spacer(1, 8))


def add_terms(story, config, styles):
    """Add Terms & Conditions section."""
    story.append(section_header("Terms & Conditions", styles))
    story.extend(bullet_list(config["terms"], styles))
    story.append(Spacer(1, 8))


def add_signature_block(story, config, styles):
    """Add signature lines."""
    story.append(section_header("Acceptance", styles))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "By signing below, both parties agree to the terms outlined in this Statement of Work.",
        styles["SOW_Body"]
    ))
    story.append(Spacer(1, 24))

    page_width = letter[0] - 1.5 * inch
    sig_data = [
        [
            Paragraph(f"<b>{config['prepared_by']}</b>", styles["SOW_Body"]),
            Paragraph("", styles["SOW_Body"]),
            Paragraph(f"<b>{config['client_name']}</b>", styles["SOW_Body"]),
        ],
        [
            Paragraph("_" * 35, styles["SOW_Body"]),
            Paragraph("", styles["SOW_Body"]),
            Paragraph("_" * 35, styles["SOW_Body"]),
        ],
        [
            Paragraph("Signature / Date", styles["SOW_MetaLabel"]),
            Paragraph("", styles["SOW_Body"]),
            Paragraph("Signature / Date", styles["SOW_MetaLabel"]),
        ],
    ]

    sig_table = Table(sig_data, colWidths=[page_width * 0.45, page_width * 0.10, page_width * 0.45])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sig_table)


def footer_handler(canvas_obj, doc):
    """Draw footer on each page."""
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(TEXT_SECONDARY)

    page_width = letter[0]
    canvas_obj.drawString(0.75 * inch, 0.5 * inch, "Confidential")
    canvas_obj.drawCentredString(page_width / 2, 0.5 * inch, f"Page {doc.page}")
    canvas_obj.drawRightString(page_width - 0.75 * inch, 0.5 * inch, "Nova Research")

    # Thin line above footer
    canvas_obj.setStrokeColor(BORDER_COLOR)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(0.75 * inch, 0.65 * inch, page_width - 0.75 * inch, 0.65 * inch)

    canvas_obj.restoreState()


def generate_sow(config, output_path):
    """Main generation function."""
    styles = build_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.85 * inch,
        title=f"SOW — {config['project_title']}",
        author=config["prepared_by"],
    )

    story = []

    logo_path = config.get("logo_path", "")
    add_header_block(story, config, styles, logo_path)
    add_meta_block(story, config, styles)
    add_overview(story, config, styles)
    add_scope(story, config, styles)
    add_deliverables(story, config, styles)
    add_timeline(story, config, styles)
    add_pricing(story, config, styles)
    add_assumptions(story, config, styles)
    add_acceptance_criteria(story, config, styles)
    add_terms(story, config, styles)
    add_signature_block(story, config, styles)

    doc.build(story, onFirstPage=footer_handler, onLaterPages=footer_handler)
    print(f"✓ SOW generated: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_sow.py config.json [--output output.pdf]")
        sys.exit(1)

    config_path = sys.argv[1]
    output_path = "sow_output.pdf"

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    with open(config_path, "r") as f:
        config = json.load(f)

    generate_sow(config, output_path)
