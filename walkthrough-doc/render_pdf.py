#!/usr/bin/env python3
"""
Render a canonical walkthrough markdown file to a styled PDF.

Usage:
    python3 render_pdf.py INPUT.md OUTPUT.pdf [--accent-color #HEX] [--logo PATH]

Parses:
    - # Title
    - ## Section headings
    - ### Step headings (under ## Steps) and ### Troubleshooting entries
    - Paragraphs
    - Bulleted lists (- item)
    - Bolded inline text (**text**)
    - Images: ![alt](path) — path resolved relative to input file's parent directory
    - Callouts: > [!TIP] / > [!NOTE] / > [!WARNING] (first line) + continued > lines
"""

import argparse
import os
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# --- Styles ---------------------------------------------------------------

def build_styles(accent_hex: str):
    accent = colors.HexColor(accent_hex)
    ink = colors.HexColor("#1f2937")       # near-black
    muted = colors.HexColor("#6b7280")      # gray
    rule = colors.HexColor("#e5e7eb")       # light gray
    tip_bg = colors.HexColor("#ecfdf5")
    tip_border = colors.HexColor("#10b981")
    note_bg = colors.HexColor("#eff6ff")
    note_border = colors.HexColor("#3b82f6")
    warn_bg = colors.HexColor("#fef3c7")
    warn_border = colors.HexColor("#f59e0b")

    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "Title", parent=base["Title"],
            fontName="Times-Bold", fontSize=26, leading=32,
            textColor=ink, spaceAfter=6, alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=12, leading=16,
            textColor=muted, spaceAfter=18,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"],
            fontName="Times-Bold", fontSize=18, leading=22,
            textColor=accent, spaceBefore=18, spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"],
            fontName="Helvetica-Bold", fontSize=13, leading=16,
            textColor=ink, spaceBefore=12, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"],
            fontName="Helvetica", fontSize=10.5, leading=15,
            textColor=ink, spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"],
            fontName="Helvetica", fontSize=10.5, leading=15,
            textColor=ink, leftIndent=16, bulletIndent=4, spaceAfter=3,
        ),
        "callout_body": ParagraphStyle(
            "CalloutBody", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=ink,
        ),
        "callout_label": ParagraphStyle(
            "CalloutLabel", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=9, leading=12,
            textColor=ink, spaceAfter=2,
        ),
        "image_caption": ParagraphStyle(
            "ImageCaption", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=9, leading=12,
            textColor=muted, spaceAfter=10, spaceBefore=2,
        ),
    }

    palette = {
        "accent": accent, "ink": ink, "muted": muted, "rule": rule,
        "tip_bg": tip_bg, "tip_border": tip_border,
        "note_bg": note_bg, "note_border": note_border,
        "warn_bg": warn_bg, "warn_border": warn_border,
    }
    return styles, palette


# --- Inline markdown formatting -----------------------------------------

def inline_md(text: str) -> str:
    """Convert **bold** and `code` to reportlab-paragraph markup."""
    # escape ampersands and angle brackets that aren't already markup
    text = text.replace("&", "&amp;")
    text = re.sub(r"<(?![bui/])", "&lt;", text)
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # inline code
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    # links [label](url) -> label (url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    return text


# --- Parser -------------------------------------------------------------

def parse_markdown(md_text: str, base_dir: Path):
    """Return a list of block dicts in document order."""
    blocks = []
    lines = md_text.splitlines()
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line
        if not stripped:
            i += 1
            continue

        # Title
        if stripped.startswith("# ") and not stripped.startswith("## "):
            blocks.append({"type": "title", "text": stripped[2:].strip()})
            # check next non-blank line for subtitle (plain paragraph before first ##)
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and not lines[j].strip().startswith("#"):
                subtitle_lines = []
                while j < n and lines[j].strip() and not lines[j].strip().startswith("#"):
                    subtitle_lines.append(lines[j].strip())
                    j += 1
                blocks.append({"type": "subtitle", "text": " ".join(subtitle_lines)})
                i = j
                continue
            i += 1
            continue

        # H2
        if stripped.startswith("## "):
            blocks.append({"type": "h2", "text": stripped[3:].strip()})
            i += 1
            continue

        # H3
        if stripped.startswith("### "):
            blocks.append({"type": "h3", "text": stripped[4:].strip()})
            i += 1
            continue

        # Image: ![alt](path)
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if m:
            alt, path = m.group(1), m.group(2)
            # resolve path relative to markdown file
            img_path = (base_dir / path).resolve()
            blocks.append({"type": "image", "alt": alt, "path": str(img_path)})
            i += 1
            continue

        # Callout: > [!TIP] / > [!NOTE] / > [!WARNING]
        m = re.match(r">\s*\[!(TIP|NOTE|WARNING)\]\s*$", stripped)
        if m:
            kind = m.group(1)
            body_lines = []
            j = i + 1
            while j < n and lines[j].strip().startswith(">"):
                body_lines.append(lines[j].strip().lstrip(">").strip())
                j += 1
            blocks.append({
                "type": "callout",
                "kind": kind,
                "text": " ".join(l for l in body_lines if l),
            })
            i = j
            continue

        # Bulleted list
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue

        # Paragraph — collect contiguous non-empty non-special lines
        para_lines = [stripped]
        i += 1
        while i < n:
            l = lines[i].strip()
            if not l:
                break
            if l.startswith("#") or l.startswith(">") or l.startswith("- "):
                break
            if re.match(r"!\[([^\]]*)\]\(([^)]+)\)", l):
                break
            para_lines.append(l)
            i += 1
        blocks.append({"type": "paragraph", "text": " ".join(para_lines)})

    return blocks


# --- Flowable builders ---------------------------------------------------

def image_flowable(path: str, alt: str, styles, max_width: float, max_height: float):
    """Return an Image flowable sized to fit, with caption. Fallback to placeholder if missing."""
    if not os.path.exists(path):
        placeholder = Paragraph(
            f"<i>[Missing image: {os.path.basename(path)}]</i>",
            styles["image_caption"],
        )
        return [placeholder]

    try:
        img = Image(path)
        # Scale to fit
        iw, ih = img.imageWidth, img.imageHeight
        scale = min(max_width / iw, max_height / ih, 1.0)
        img.drawWidth = iw * scale
        img.drawHeight = ih * scale
        img.hAlign = "LEFT"
        flowables = [img]
        if alt:
            flowables.append(Paragraph(inline_md(alt), styles["image_caption"]))
        return [KeepTogether(flowables)]
    except Exception as e:
        return [Paragraph(f"<i>[Image error: {e}]</i>", styles["image_caption"])]


def callout_flowable(kind: str, text: str, styles, palette):
    """Render a callout as a single-cell bordered table with colored left bar."""
    bg_key = {"TIP": "tip_bg", "NOTE": "note_bg", "WARNING": "warn_bg"}[kind]
    border_key = {"TIP": "tip_border", "NOTE": "note_border", "WARNING": "warn_border"}[kind]
    label_text = {"TIP": "TIP", "NOTE": "NOTE", "WARNING": "WARNING"}[kind]

    label = Paragraph(label_text, styles["callout_label"])
    body = Paragraph(inline_md(text), styles["callout_body"])

    inner = Table(
        [[label], [body]],
        colWidths=[5.5 * inch],
    )
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, 1), (0, 1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), palette[bg_key]),
        ("LINEBEFORE", (0, 0), (0, -1), 3, palette[border_key]),
    ]))
    return KeepTogether([Spacer(1, 4), inner, Spacer(1, 10)])


# --- Page template --------------------------------------------------------

class WalkthroughDoc(BaseDocTemplate):
    def __init__(self, filename, title, palette, logo_path=None, **kwargs):
        super().__init__(
            filename,
            pagesize=LETTER,
            leftMargin=0.9 * inch,
            rightMargin=0.9 * inch,
            topMargin=0.9 * inch,
            bottomMargin=0.9 * inch,
            title=title,
            **kwargs,
        )
        self.doc_title = title
        self.palette = palette
        self.logo_path = logo_path

        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id="normal",
        )
        self.addPageTemplates([
            PageTemplate(id="default", frames=frame, onPage=self._draw_chrome),
        ])

    def _draw_chrome(self, canvas, doc):
        canvas.saveState()
        # Footer: title on left, page number on right
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(self.palette["muted"])
        canvas.drawString(
            self.leftMargin, 0.5 * inch,
            self.doc_title[:80],
        )
        canvas.drawRightString(
            LETTER[0] - self.rightMargin, 0.5 * inch,
            f"Page {doc.page}",
        )
        # Thin rule above footer
        canvas.setStrokeColor(self.palette["rule"])
        canvas.setLineWidth(0.5)
        canvas.line(
            self.leftMargin, 0.7 * inch,
            LETTER[0] - self.rightMargin, 0.7 * inch,
        )
        # Logo in header (if provided)
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                canvas.drawImage(
                    self.logo_path,
                    LETTER[0] - self.rightMargin - 0.8 * inch,
                    LETTER[1] - self.topMargin + 0.1 * inch,
                    width=0.8 * inch, height=0.4 * inch,
                    preserveAspectRatio=True, mask="auto",
                )
            except Exception:
                pass
        canvas.restoreState()


# --- Main ----------------------------------------------------------------

def render(md_path: Path, pdf_path: Path, accent: str, logo: str | None):
    md_text = md_path.read_text(encoding="utf-8")
    blocks = parse_markdown(md_text, md_path.parent)

    # Pull title for doc metadata
    title = next((b["text"] for b in blocks if b["type"] == "title"), "Walkthrough")

    styles, palette = build_styles(accent)
    doc = WalkthroughDoc(str(pdf_path), title, palette, logo_path=logo)

    story = []
    max_img_width = 6.5 * inch
    max_img_height = 4.5 * inch

    for b in blocks:
        t = b["type"]
        if t == "title":
            story.append(Paragraph(inline_md(b["text"]), styles["title"]))
        elif t == "subtitle":
            story.append(Paragraph(inline_md(b["text"]), styles["subtitle"]))
        elif t == "h2":
            story.append(Paragraph(inline_md(b["text"]), styles["h2"]))
        elif t == "h3":
            story.append(Paragraph(inline_md(b["text"]), styles["h3"]))
        elif t == "paragraph":
            story.append(Paragraph(inline_md(b["text"]), styles["body"]))
        elif t == "bullets":
            for item in b["items"]:
                story.append(Paragraph(f"• {inline_md(item)}", styles["bullet"]))
            story.append(Spacer(1, 4))
        elif t == "image":
            story.extend(image_flowable(
                b["path"], b["alt"], styles, max_img_width, max_img_height,
            ))
        elif t == "callout":
            story.append(callout_flowable(b["kind"], b["text"], styles, palette))

    doc.build(story)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="Input markdown file")
    p.add_argument("output", help="Output PDF file")
    p.add_argument("--accent-color", default="#2563eb",
                   help="Accent color hex (default #2563eb)")
    p.add_argument("--logo", default=None,
                   help="Optional logo image path (PNG/JPG)")
    args = p.parse_args()

    md_path = Path(args.input).resolve()
    pdf_path = Path(args.output).resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    if not md_path.exists():
        print(f"Input markdown not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    render(md_path, pdf_path, args.accent_color, args.logo)
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
