---
name: ies-documentation
description: Generate branded IES PDF documents (architecture decisions, design briefs, technical reports, comparison docs, walkthroughs) with the IES logo, house color palette, comparison tables, numbered step tables, flow diagrams, and callouts. Use when user mentions "IES doc", "IES report", "IES PDF", "branded document", or wants to package technical content (architecture, decisions, comparisons, RAG/system flows, ML System design) into a polished, team-shareable PDF in the IES house style.
---

# IES Document Generator

## Quick Start

1. Decide on input format: JSON config (best for structured docs with tables/diagrams) or Markdown (best for prose-heavy docs).
2. Save the input file.
3. Run the generator:

```bash
python scripts/generate_ies_doc.py input.json --output /mnt/user-data/outputs/doc.pdf
```

The bundled IES logo (`assets/IES_Logo.png`) is used by default. Override with `--logo path/to/other.png` if needed.

## Input formats

**JSON** — full control. Every section is an object with a `type`. Supported types: `heading`, `paragraph`, `bullets`, `callout`, `code`, `hr`, `spacer`, `pagebreak`, `table`, `comparison`, `steps`, `flow_diagram`, `group`. See [REFERENCE.md](REFERENCE.md) for the schema.

**Markdown** — for prose-heavy docs without tables/diagrams. Supports `#`/`##`/`###`/`####` headings, paragraphs, `-`/`*` bullets, ` ``` ` code blocks, `---` rules, `<pagebreak>` markers, and `> [info|warn|good] text` callouts. Anything richer should be JSON.

## Workflow

1. **Understand the doc** — what's the audience, what sections does it need, are there tables/comparisons/flows?
2. **Pick the format** — JSON for structured (architecture decisions, comparisons, flow docs), Markdown for narrative (briefs, summaries, RFCs).
3. **Author the input** — write the JSON or Markdown file under `/tmp/` or the working dir.
4. **Generate** — run the script with `--output` pointing to `/mnt/user-data/outputs/`.
5. **Review** — render or open the PDF, check for:
   - Tables fitting on the page (no column overflow)
   - Section headers not stranded at the bottom of pages
   - Sections with diagrams kept on a single page (use `keep_together` or `pagebreak`)
6. **Iterate** — adjust column widths, group related sections under `keep_together`, or add `pagebreak` before major sections that deserve their own page.
7. **Present** — share the PDF via `present_files`.

## Patterns this skill bakes in

- **Branded cover**: IES logo (top-left) + bold title + muted subtitle + thin rule.
- **Color palette**: slate body text, blue accent headers, info/warn/good callouts in matching pastels, dark code blocks.
- **Wrapping table cells**: every table cell is rendered as a `Paragraph` so text wraps cleanly inside columns instead of overflowing — never pass raw strings as cells.
- **Comparison tables**: first column rendered as a bold label with a light-grey background; remaining columns are content cells. Use for option/A-B/vendor matrices.
- **Step tables**: numbered three-column tables (#, component, what happens) for query/ingestion/process flows.
- **Flow diagrams**: vertical stacks of coloured boxes joined by down-arrows, ideal for system architecture or RAG/data flows.
- **KeepTogether**: wrap a heading + its table/diagram in a `group` with `keep_together: true` to prevent the heading from being orphaned on a previous page.
- **PageBreak**: force a major section onto its own page with a `{"type": "pagebreak"}` section.
- **Tight spacing**: H1/H2 spacing and Spacer values tuned to avoid awkward whitespace.
- **Page numbers**: footer with "Page N" on every page (and an optional left-side label).

## Common gotchas

- **Don't pass raw strings as table cells in custom code** — the script wraps them in Paragraphs for you, but if you extend it, always use Paragraph cells or text won't wrap.
- **Use HTML entities for arrows in JSON**: `&rarr;` (→), `&harr;` (↔), `&ndash;` (–), `&mdash;` (—). They render correctly inside Paragraph cells.
- **Logo aspect ratio**: the bundled logo is ~1.79:1. The script auto-reads any logo's actual aspect ratio (via Pillow) so swapping logos preserves proportions.
- **Section ordering**: declare a `pagebreak` *before* the section heading you want on a new page, then wrap the heading + content in a `group` with `keep_together: true` so they all stay together.

## Reference

- Full config schema, every section type's options, and worked examples: [REFERENCE.md](REFERENCE.md)
- Example inputs: `templates/architecture-decision.json`, `templates/simple-brief.md`
