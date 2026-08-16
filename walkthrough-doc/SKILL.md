---
name: walkthrough-doc
description: Generate end-user walkthrough documentation (login guides, feature how-tos, onboarding steps) with screenshots, resource links, and numbered steps. Produces PDF (default), Markdown, or Word output. Use when user mentions "walkthrough", "user guide", "how-to doc", "step-by-step guide", "end-user documentation", "login walkthrough", "onboarding doc", or provides screenshots and instructions that need to be packaged as end-user documentation.
---

# Walkthrough Document Generator

Generates polished end-user walkthrough documents from provided notes, screenshots, and resource links. Output formats: PDF (default), Markdown, Word — or all three.

## Quick start

1. Collect inputs from the user:
   - **Title** of the walkthrough (e.g., "Logging in to CrewClock")
   - **Screenshots** (from `/mnt/user-data/uploads/` — referenced by filename)
   - **Steps** the user wants covered
   - **Resources** (URLs, support contacts, credentials info)
   - **Output format(s)**: pdf (default), md, docx, or all

2. Assemble a single canonical markdown file following [TEMPLATE.md](TEMPLATE.md).

3. Render to requested format(s) using the scripts in `scripts/`.

4. Place all outputs in `/mnt/user-data/outputs/` and present via `present_files`.

## Inputs — flexible ingestion

Accept both structured and unstructured input:

- **Structured**: User provides sectioned content (title, steps, screenshots mapped to steps, resources). Use as-is.
- **Unstructured**: User dumps notes + screenshots. Organize into the template structure. Infer step order from screenshot names (e.g., `01-login.png`, `02-dashboard.png`) or from the order they're mentioned. Ask ONE clarifying question only if the title or primary goal is unclear.

Screenshots live in `/mnt/user-data/uploads/`. Copy each referenced screenshot to the working directory before rendering, so the rendered docs can embed them.

## Default sections (in order)

Include these sections by default. Omit any that have no content — never leave an empty section:

1. **Title + one-line purpose** — what this walkthrough accomplishes
2. **Overview** — 2–4 sentences of context (who it's for, prerequisites summary)
3. **Prerequisites** — accounts, access, URLs, software needed (bulleted)
4. **Steps** — numbered, each with:
   - A short action heading (imperative: "Navigate to the login page")
   - 1–3 sentences of instruction
   - Optional screenshot
   - Optional callout (tip/warning/note)
5. **Helpful Resources** — login URLs, support email/phone, doc links, related walkthroughs
6. **Troubleshooting** — common issues + resolutions (only if the user provided any)

See [TEMPLATE.md](TEMPLATE.md) for the exact markdown skeleton and callout syntax.

## Callouts

Three callout types, rendered consistently across all three output formats:

- `> [!TIP]` — helpful extras (e.g., "You can also access this via the mobile app")
- `> [!NOTE]` — neutral info (e.g., "Your session expires after 30 minutes")
- `> [!WARNING]` — things that can go wrong (e.g., "Do not share this URL externally")

Use sparingly — at most one callout per step.

## Rendering workflow

```
# 1. Write the canonical markdown to /home/claude/walkthrough.md
# 2. Copy referenced screenshots from /mnt/user-data/uploads/ → /home/claude/images/
# 3. Render based on user's format choice:

# PDF (default)
python3 scripts/render_pdf.py walkthrough.md /mnt/user-data/outputs/walkthrough.pdf

# Word
python3 scripts/render_docx.py walkthrough.md /mnt/user-data/outputs/walkthrough.docx

# Markdown — just copy the canonical file
cp walkthrough.md /mnt/user-data/outputs/walkthrough.md
```

When the user doesn't specify a format, produce **PDF by default** and mention that MD and DOCX versions are available on request.

When the user says "all formats" or similar, produce all three.

## Output file naming

Use a slugified version of the title:
- "Logging in to CrewClock" → `logging-in-to-crewclock.pdf`
- Strip punctuation, lowercase, replace spaces with hyphens

## Styling

The PDF renderer produces a clean professional look (neutral grays, single accent color, sans-serif body with serif headings). No custom branding by default — the renderer accepts `--accent-color` and `--logo` flags if the user wants to brand the output. See `scripts/render_pdf.py --help`.

## When screenshots are missing

If the user mentions a step needs a screenshot but hasn't uploaded one, insert a placeholder in the markdown:

```
> [!NOTE]
> Screenshot pending: [description of what the screenshot should show]
```

Do not fabricate or generate screenshot images.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for two complete worked examples (a simple login walkthrough and a multi-section feature guide).

## Review checklist

Before handing files to the user, verify:

- [ ] Every referenced screenshot file exists and is readable
- [ ] Steps are in logical order and imperatively phrased
- [ ] No empty sections in the output
- [ ] Output file(s) in `/mnt/user-data/outputs/`
- [ ] Called `present_files` with the output(s)
