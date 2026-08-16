---
name: sow-generator
description: Generate branded PDF Statements of Work (SOWs) with logo, scope, deliverables, timeline, pricing, assumptions, acceptance criteria, and terms. Use when user mentions "SOW", "statement of work", "scope of work", "consulting proposal", "engagement letter", "project agreement", or wants to formalize a client engagement into a clean branded document.
---

# SOW Generator

## Quick Start

1. Gather engagement details from the user (or extract from conversation context)
2. Build a JSON config with `logo_path` set to `nova-research.png` (bundled in this skill directory)
3. Run `python generate_sow.py config.json --output <output_path>`

## Required Information

Collect these before generating. Use conversation context when available:

| Field | Example |
|-------|---------|
| `project_title` | "Claude AI Workflow Architecture" |
| `client_name` | "Client Name" |
| `client_company` | "Client Company" |
| `prepared_by` | "Jordan — Nova Research" |
| `date` | "April 14, 2026" |
| `overview` | 1-3 sentence engagement summary |
| `scope_items` | List of scope line items (what's included) |
| `deliverables` | List of concrete outputs the client receives |
| `timeline` | List of phases with duration |
| `pricing` | Rate, hours, total, payment terms |
| `assumptions` | What must be true for success |
| `acceptance_criteria` | How the client knows it's done |
| `terms` | Cancellation, IP, confidentiality |

## Workflow

1. **Extract from context** — scan the conversation for client name, scope, pricing discussed
2. **Fill gaps** — ask the user only for missing critical fields
3. **Generate JSON config** — build the config object, setting `logo_path` to the bundled `nova-research.png`
4. **Run script** — `python generate_sow.py config.json --output <output_path>`
5. **Deliver** — present the PDF to the user

## Config JSON Schema

```json
{
  "project_title": "string",
  "client_name": "string",
  "client_company": "string",
  "prepared_by": "string",
  "date": "string",
  "overview": "string",
  "scope_items": ["string"],
  "deliverables": [{"name": "string", "description": "string"}],
  "timeline": [{"phase": "string", "duration": "string", "description": "string"}],
  "pricing": {
    "rate_per_hour": 100,
    "estimated_hours": 12,
    "total": 1200,
    "payment_terms": "string"
  },
  "assumptions": ["string"],
  "acceptance_criteria": ["string"],
  "terms": ["string"],
  "logo_path": "path/to/logo.png"
}
```

## Design Notes

- Clean header with Nova Research logo + title (dark text, thin rule below)
- Clean section headers with left accent bar (#1a1a2e)
- Tables use alternating row shading
- Font: Helvetica throughout
- US Letter size, 0.75" margins
- Footer with page numbers and "Confidential" marker
