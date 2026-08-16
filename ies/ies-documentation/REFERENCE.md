# IES Document Generator — Reference

Full configuration schema and section reference for `generate_ies_doc.py`.

## Top-level config (JSON)

```json
{
  "title": "Document title (required)",
  "subtitle": "Optional subtitle shown under the title in muted grey",
  "author": "IES",
  "logo_path": "absolute or relative path; defaults to bundled IES logo",
  "page_footer_label": "Optional left-side footer label on every page",
  "footer_note": "Optional muted paragraph rendered after the last section",
  "sections": [ ...section objects... ]
}
```

If `logo_path` is omitted, the bundled `assets/IES_Logo.png` is used automatically.

## Section types

Every section object has a `type` field. Optional flags shared by all types:

- `keep_together: true` — wrap this section's flowables in a `KeepTogether` so they don't split across pages.

### `heading`

```json
{ "type": "heading", "level": 1, "text": "Section name" }
```

`level` is 1 (slate H1, biggest), 2 (blue H2), or 3 (slate H3, smallest).

### `paragraph`

```json
{ "type": "paragraph", "text": "Plain text. Supports <b>bold</b>, <i>italic</i>, &mdash; and other HTML entities." }
```

### `bullets`

```json
{
  "type": "bullets",
  "items": [
    "<b>First</b> item — supports inline HTML.",
    "Second item.",
    "Third item."
  ]
}
```

### `callout`

```json
{ "type": "callout", "kind": "info", "text": "<b>Note:</b> ..." }
```

`kind` is `info` (blue), `good` (green), or `warn` (amber).

### `code`

```json
{
  "type": "code",
  "title": "Optional H3 heading above the block",
  "text": "raw code text\nwith real newlines"
}
```

The text is HTML-escaped automatically and rendered on a dark slate background. Use real `\n` newlines; they're converted to `<br/>` for you.

### `hr`

```json
{ "type": "hr" }
```

A thin grey horizontal rule.

### `spacer`

```json
{ "type": "spacer", "height": 8 }
```

A vertical gap. `height` is in points; default 6.

### `pagebreak`

```json
{ "type": "pagebreak" }
```

Forces the next section onto a new page.

### `table`

Generic table. The first row of `rows` is the header.

```json
{
  "type": "table",
  "rows": [
    ["Path", "Data crossing", "Frequency", "Boundary"],
    ["UI &harr; FastAPI", "User prompts", "Per request", "Internet &rarr; Azure"]
  ],
  "col_widths": [1.45, 1.85, 1.35, 1.85]
}
```

`col_widths` is in inches and optional. The total page content width is **6.5 inches** (US Letter, 0.6" margins). All cells are auto-wrapped — you can use HTML entities and inline `<b>`/`<i>` markup.

### `comparison`

Side-by-side option matrix. First column is rendered as bold labels with a light-grey background; remaining columns are content.

```json
{
  "type": "comparison",
  "headers": ["Dimension", "Option A", "Option B"],
  "rows": [
    ["Where it runs", "Managed SaaS in Azure region", "Dedicated server on-prem"],
    ["Latency", "5-10ms intra-Azure", "10-40ms Azure&harr;on-prem"]
  ],
  "col_widths": [1.3, 2.6, 2.6]
}
```

If `col_widths` is omitted, the first column is 1.3" and the rest split the remainder.

### `steps`

Numbered three-column step table (#, Component, What happens).

```json
{
  "type": "steps",
  "steps": [
    { "component": "UI", "what": "User submits a question..." },
    { "component": "FastAPI Gateway", "what": "Authenticates, applies rate limits..." },
    { "component": "LlamaIndex &rarr; DGX", "what": "Calls the embedding model. <b>[Cross-network hop #1]</b>" }
  ]
}
```

Use `<b>...</b>` to highlight key terms inside the `what` text.

### `flow_diagram`

Vertical stack of coloured boxes joined by down-arrows. Each box has a title, optional subtitle, and an optional hex color.

```json
{
  "type": "flow_diagram",
  "boxes": [
    { "title": "UI",              "subtitle": "Browser / Mobile",        "color": "#0ea5e9" },
    { "title": "FastAPI Gateway", "subtitle": "Azure Container Apps",    "color": "#2563eb" },
    { "title": "LlamaIndex",      "subtitle": "RAG orchestration",       "color": "#7c3aed" },
    { "title": "Qdrant",          "subtitle": "Cloud or local + NAS",    "color": "#059669" },
    { "title": "DGX Cluster",     "subtitle": "vLLM + embedding model",  "color": "#dc2626" }
  ],
  "box_width": 2.3
}
```

If `color` is omitted on a box, the script cycles through a default palette (sky / blue / violet / emerald / red).

### `group`

Container that bundles multiple child sections. Most useful with `keep_together: true` to keep a heading + its table or diagram on the same page.

```json
{
  "type": "group",
  "keep_together": true,
  "sections": [
    { "type": "heading", "level": 1, "text": "End-to-End RAG Flow" },
    { "type": "paragraph", "text": "Below is the full request lifecycle..." },
    { "type": "flow_diagram", "boxes": [ ... ] }
  ]
}
```

## HTML markup inside text

Inside any `text` or table cell, the following work:

| Markup | Renders as |
|---|---|
| `<b>...</b>` | **Bold** |
| `<i>...</i>` | *Italic* |
| `<font color="#hex">...</font>` | Coloured text |
| `<br/>` | Line break |
| `&rarr;` | → |
| `&larr;` | ← |
| `&harr;` | ↔ |
| `&darr;` | ↓ |
| `&mdash;` | — |
| `&ndash;` | – |
| `&ldquo;` `&rdquo;` | "smart quotes" |
| `&lsquo;` `&rsquo;` | 'smart quotes' |
| `&amp;` | & |

## Pagination patterns

**Force a section onto its own page**:

```json
[
  { "type": "pagebreak" },
  {
    "type": "group",
    "keep_together": true,
    "sections": [
      { "type": "heading", "level": 1, "text": "End-to-End Flow" },
      { "type": "paragraph", "text": "Full lifecycle..." },
      { "type": "flow_diagram", "boxes": [ ... ] }
    ]
  },
  { "type": "pagebreak" }
]
```

**Prevent an orphaned heading** (heading + table on different pages):

```json
{
  "type": "group",
  "keep_together": true,
  "sections": [
    { "type": "heading", "level": 1, "text": "What flows where" },
    { "type": "paragraph", "text": "Quick mental map..." },
    { "type": "table", "rows": [ ... ] }
  ]
}
```

## Markdown shortcuts

When writing prose-heavy docs, Markdown input is faster:

```markdown
# Document Title
Document subtitle on the line right after the title.

## Section heading

Body paragraph.

- bullet one
- bullet two

> [info] Info callout.
> [warn] Warn callout.
> [good] Good callout.

```python
print("code blocks too")
```

---

<pagebreak>

## Next section
```

Anything that needs a comparison/steps/flow diagram should be JSON instead — Markdown doesn't support those types.

## Page geometry

- **Page size**: US Letter (8.5" x 11")
- **Margins**: 0.6" left/right/top, 0.7" bottom
- **Content width**: 6.5"
- **Page numbers**: rendered in the footer at 0.4" from the bottom

## Color palette (hex)

| Token | Hex | Used for |
|---|---|---|
| PRIMARY | `#1f2937` | Body text, H1 headers, table header backgrounds |
| ACCENT | `#2563eb` | H2 headers, info callout border, page numbers labels |
| ACCENT_LIGHT | `#dbeafe` | Info callout background |
| SUCCESS | `#059669` | Good callout border |
| SUCCESS_LIGHT | `#d1fae5` | Good callout background |
| WARN | `#d97706` | Warn callout border |
| WARN_LIGHT | `#fef3c7` | Warn callout background |
| MUTED | `#6b7280` | Subtitles, footer notes, page numbers |
| LIGHT_BG | `#f3f4f6` | Comparison table label column |
| BORDER | `#e5e7eb` | Table borders, horizontal rules |
| ZEBRA | `#fafafa` | Alternating table row background |
| CODE_BG | `#0f172a` | Code block background |
| CODE_FG | `#e2e8f0` | Code block text |

To change the palette globally, edit the constants at the top of `scripts/generate_ies_doc.py`.
