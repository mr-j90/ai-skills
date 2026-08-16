"""
IES Documentation Generator.

Generates a branded PDF from either:
  - a JSON config file (structured input)
  - a Markdown file (free-form sections with simple front-matter)

Usage:
  python generate_doc.py input.json --output report.pdf
  python generate_doc.py input.md   --output report.pdf

JSON schema: see schema.json bundled in templates/.
Markdown: front-matter (YAML) for title/subtitle, then standard markdown.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
)

# Make the components module importable regardless of cwd
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from ies_components import (  # noqa: E402
    build_styles, cover_logo, hr, callout, data_table, comparison_table,
    step_table, flow_diagram, code_block, bullet_list,
)

# Default bundled logo (relative to skill root)
DEFAULT_LOGO = SCRIPT_DIR.parent / "assets" / "IES_Logo_Black.png"


# ---------------------------------------------------------------------------
# Block dispatcher: each block type renders a list of flowables
# ---------------------------------------------------------------------------
def render_block(block, styles, logo_path):
    """
    Render a single content block to a list of flowables.

    Block types:
      - heading           {type, text, level: "h1"|"h2"|"h3"}
      - paragraph         {type, text}
      - bullets           {type, items: [str]}
      - callout           {type, kind: "info"|"good"|"warn", text}
      - code              {type, text}                        (use \\n for newlines)
      - hr                {type}
      - page_break        {type}
      - spacer            {type, height: int}
      - table             {type, rows: [[str]], col_widths: [float]}
      - comparison        {type, dimensions, option_a, option_b,
                                 option_a_values, option_b_values}
      - steps             {type, steps: [[component, description]]}
      - flow_diagram      {type, boxes: [[title, subtitle]]}
      - keep_together     {type, blocks: [...]}     (recursive — children stay together)
    """
    btype = block.get("type")

    if btype == "heading":
        level = block.get("level", "h1")
        return [Paragraph(block["text"], styles[level])]

    if btype == "paragraph":
        return [Paragraph(block["text"], styles["body"])]

    if btype == "bullets":
        return [bullet_list(block["items"], styles)]

    if btype == "callout":
        return [callout(block["text"], kind=block.get("kind", "info"), styles=styles)]

    if btype == "code":
        # Escape < > & for safe HTML rendering, then convert newlines to <br/>
        text = (block["text"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>"))
        return [code_block(text, styles)]

    if btype == "hr":
        return [hr()]

    if btype == "page_break":
        return [PageBreak()]

    if btype == "spacer":
        return [Spacer(1, int(block.get("height", 8)))]

    if btype == "table":
        return [data_table(
            rows=block["rows"],
            col_widths_inches=block["col_widths"],
            styles=styles,
            first_col_bold=block.get("first_col_bold", True),
        )]

    if btype == "comparison":
        return [comparison_table(
            dimensions=block["dimensions"],
            option_a_label=block["option_a"],
            option_b_label=block["option_b"],
            option_a_values=block["option_a_values"],
            option_b_values=block["option_b_values"],
            styles=styles,
        )]

    if btype == "steps":
        return [step_table(
            steps=[(c, d) for c, d in block["steps"]],
            styles=styles,
        )]

    if btype == "flow_diagram":
        return [flow_diagram(
            boxes=[(t, s) for t, s in block["boxes"]],
            styles=styles,
        )]

    if btype == "keep_together":
        children = []
        for child in block["blocks"]:
            children.extend(render_block(child, styles, logo_path))
        return [KeepTogether(children)]

    raise ValueError(f"Unknown block type: {btype!r}")


# ---------------------------------------------------------------------------
# Cover page builder
# ---------------------------------------------------------------------------
def build_cover(title, subtitle, logo_path, styles):
    """Standard IES cover: logo + title + subtitle + horizontal rule."""
    return [
        cover_logo(logo_path),
        Spacer(1, 8),
        Paragraph(title, styles["title"]),
        Paragraph(subtitle, styles["subtitle"]) if subtitle else Spacer(1, 0),
        hr(),
        Spacer(1, 6),
    ]


# ---------------------------------------------------------------------------
# JSON config -> document
# ---------------------------------------------------------------------------
def build_from_json(config, output_path, logo_path):
    """
    Config schema:
      {
        "title": "AI/ML Local Model Integration",
        "subtitle": "...",         # optional
        "logo_path": "/path/to/logo.png",  # optional, falls back to bundled
        "blocks": [ {block}, {block}, ... ]
      }
    """
    title = config.get("title", "Untitled Document")
    subtitle = config.get("subtitle", "")
    custom_logo = config.get("logo_path")
    if custom_logo and Path(custom_logo).exists():
        logo_path = custom_logo

    styles = build_styles()
    story = build_cover(title, subtitle, logo_path, styles)

    for block in config.get("blocks", []):
        story.extend(render_block(block, styles, logo_path))

    _build_pdf(story, output_path, title)


# ---------------------------------------------------------------------------
# Markdown -> document
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
CALLOUT_RE = re.compile(r"^>\s*\[!(info|good|warn)\]\s*(.*)$", re.IGNORECASE)
CODE_FENCE_RE = re.compile(r"^```")


def _parse_frontmatter(text):
    """Lightweight YAML-ish front-matter (title/subtitle/logo_path only)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = text[m.end():]
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def _markdown_to_blocks(md_text):
    """
    Convert a subset of Markdown to IES blocks.
    Supported:
      # / ## / ###            -> heading h1/h2/h3
      blank line              -> paragraph break
      - / *                   -> bullet list
      ```...```               -> code block
      > [!info|good|warn] ... -> callout
      ---                     -> hr
      <!-- pagebreak -->      -> page_break
      Plain text              -> paragraph
    Tables and complex blocks should use JSON input — Markdown is for prose.
    """
    blocks = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if line.strip() == "---":
            blocks.append({"type": "hr"})
            i += 1
            continue

        if "<!-- pagebreak -->" in line.lower():
            blocks.append({"type": "page_break"})
            i += 1
            continue

        if line.startswith("### "):
            blocks.append({"type": "heading", "level": "h3", "text": line[4:].strip()})
            i += 1
            continue
        if line.startswith("## "):
            blocks.append({"type": "heading", "level": "h2", "text": line[3:].strip()})
            i += 1
            continue
        if line.startswith("# "):
            blocks.append({"type": "heading", "level": "h1", "text": line[2:].strip()})
            i += 1
            continue

        m = CALLOUT_RE.match(line)
        if m:
            kind = m.group(1).lower()
            text = m.group(2).strip()
            # Continue if the next lines are also indented quotes
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                text += " " + lines[j].lstrip()[1:].strip()
                j += 1
            blocks.append({"type": "callout", "kind": kind, "text": _md_inline(text)})
            i = j
            continue

        if CODE_FENCE_RE.match(line):
            j = i + 1
            buf = []
            while j < len(lines) and not CODE_FENCE_RE.match(lines[j]):
                buf.append(lines[j])
                j += 1
            blocks.append({"type": "code", "text": "\n".join(buf)})
            i = j + 1
            continue

        if line.lstrip().startswith(("- ", "* ")):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith(("- ", "* ")):
                stripped = lines[i].lstrip()[2:].strip()
                items.append(_md_inline(stripped))
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue

        # Paragraph: gather contiguous non-blank, non-special lines
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_start(lines[i]):
            buf.append(lines[i].rstrip())
            i += 1
        blocks.append({"type": "paragraph", "text": _md_inline(" ".join(buf))})

    return blocks


def _is_block_start(line):
    """True if `line` starts a non-paragraph markdown block."""
    s = line.lstrip()
    return (s.startswith(("# ", "## ", "### ", "- ", "* ", "> ", "```"))
            or s.strip() == "---")


def _md_inline(text):
    """Inline markdown -> reportlab HTML. Supports **bold**, *italic*, `code`."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", text)
    return text


def build_from_markdown(md_text, output_path, logo_path):
    fm, body = _parse_frontmatter(md_text)
    title = fm.get("title", "Untitled Document")
    subtitle = fm.get("subtitle", "")
    custom_logo = fm.get("logo_path")
    if custom_logo and Path(custom_logo).exists():
        logo_path = custom_logo

    styles = build_styles()
    story = build_cover(title, subtitle, logo_path, styles)

    for block in _markdown_to_blocks(body):
        story.extend(render_block(block, styles, logo_path))

    _build_pdf(story, output_path, title)


# ---------------------------------------------------------------------------
# PDF output
# ---------------------------------------------------------------------------
def _build_pdf(story, output_path, title):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.6 * inch, bottomMargin=0.7 * inch,
        title=title, author="IES",
    )
    doc.build(story)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate a branded IES PDF.")
    parser.add_argument("input", help="Path to .json or .md input file")
    parser.add_argument("--output", "-o", required=True, help="Output PDF path")
    parser.add_argument("--logo", help="Override logo path", default=None)
    args = parser.parse_args()

    logo_path = args.logo or str(DEFAULT_LOGO)
    if not Path(logo_path).exists():
        print(f"ERROR: logo not found at {logo_path}", file=sys.stderr)
        sys.exit(1)

    src = Path(args.input)
    if not src.exists():
        print(f"ERROR: input not found: {src}", file=sys.stderr)
        sys.exit(1)

    text = src.read_text(encoding="utf-8")
    if src.suffix.lower() == ".json":
        build_from_json(json.loads(text), args.output, logo_path)
    elif src.suffix.lower() in (".md", ".markdown"):
        build_from_markdown(text, args.output, logo_path)
    else:
        print(f"ERROR: unsupported input type: {src.suffix}", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
