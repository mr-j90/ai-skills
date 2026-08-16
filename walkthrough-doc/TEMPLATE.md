# Walkthrough Template

This is the canonical structure. The markdown produced by the skill must follow this shape so the renderers (PDF / DOCX) produce consistent output.

## Skeleton

```markdown
# {Title}

{One-line purpose statement — what will the reader be able to do after this?}

## Overview

{2–4 sentences. Who is this for, when would they use it, what's the outcome.}

## Prerequisites

- {Account, access, or credential needed}
- {Software, browser, or device requirement}
- {Any URLs the user should have ready}

## Steps

### 1. {Imperative action heading}

{1–3 sentences describing what to do.}

![Alt text describing the screenshot](images/01-screenshot.png)

> [!TIP]
> {Optional helpful extra — keep short.}

### 2. {Next imperative action heading}

{Instructions.}

![Alt text](images/02-screenshot.png)

### 3. {...}

## Helpful Resources

- **Login URL**: https://example.com/login
- **Support**: support@example.com
- **Related guide**: {link or reference}

## Troubleshooting

### {Symptom or error message}

{Brief resolution. 1–2 sentences.}

### {Another symptom}

{Resolution.}
```

## Rules

**Step headings** are imperative verbs: "Click", "Enter", "Navigate to", "Select", "Confirm". Not "Clicking the button" or "You should click".

**Image paths** must be relative to the markdown file, living in an `images/` subdirectory. The renderers resolve them from the markdown file's parent directory.

**Callouts** use GitHub-flavored alert syntax:

```
> [!TIP]
> Text here.

> [!NOTE]
> Text here.

> [!WARNING]
> Text here.
```

The blockquote + `[!TYPE]` marker on the first line is required — the renderers look for this pattern.

**Resources** are a bulleted list with bolded labels. This renders cleanly in all three formats.

**Troubleshooting entries** use `###` sub-headings naming the symptom, followed by a short resolution. This keeps each entry scannable in the final doc.

## Omit, don't empty

If the user has no content for a section (e.g., no troubleshooting entries), **omit the section heading entirely**. Never leave "## Troubleshooting" with nothing under it.
