---
name: resume-tailor
description: Tailor a resume to a specific job description by rewriting bullets, reordering sections, and injecting ATS-friendly keywords — outputting a polished .docx, .pdf, or .md file. Use when user mentions "tailor resume", "rewrite resume", "resume for this job", "optimize resume", provides a job description and resume, or wants to match a resume to a role.
---

# Resume Tailor

## Inputs

| Input | Format | Required |
|-------|--------|----------|
| Job description | Pasted text or uploaded file | Yes |
| Current resume | Uploaded .docx, .pdf, or pasted text | Yes |
| Output format | `docx`, `pdf`, or `markdown` | No (default: `docx`) |

**If the user does not specify an output format, ask them before generating.** Present the three options:
- **DOCX** — Best for submitting to job portals and ATS systems. Editable in Word/Google Docs.
- **PDF** — Best for emailing directly to a hiring manager. Locked formatting.
- **Markdown** — Best for quick review, further editing in any text editor, or pasting into online forms.

## Workflow

### 1. Parse inputs
- Extract text from the current resume (use `pandoc` for .docx, pdf-reading skill for .pdf)
- Extract text from the job description

### 2. Analyze the job description
Extract and categorize:
- **Hard skills** — languages, frameworks, tools, certifications (e.g. "Python", "AWS", "PMP")
- **Soft skills** — leadership, communication, collaboration patterns
- **Domain keywords** — industry terms, methodologies (e.g. "Agile", "CI/CD", "SaaS")
- **Seniority signals** — years of experience, scope of impact, team size
- **ATS-critical phrases** — exact phrases from the JD that applicant tracking systems will scan for

### 3. Audit the current resume
- Map which JD keywords already appear in the resume
- Identify **gaps** — JD keywords with no resume match
- Identify **buried strengths** — relevant experience that exists but is understated
- Flag **irrelevant filler** — bullets that add no value for this specific role

### 4. Rewrite the resume
Apply these rules in order:

**a) Professional summary (top of resume)**
- Write a 2–3 sentence summary that mirrors the JD's core requirements
- Front-load the most relevant title, years of experience, and domain
- Weave in 3–5 high-priority keywords naturally

**b) Experience bullets**
- Rewrite each bullet using the **XYZ formula**: "Accomplished [X] as measured by [Y], by doing [Z]"
- Inject missing JD keywords where the candidate has genuine experience — never fabricate
- Lead with strong action verbs matching the JD's tone (e.g. "Architected" for senior roles, "Implemented" for mid-level)
- Quantify impact wherever possible (%, $, time saved, users affected)
- Reorder bullets within each role: most JD-relevant first

**c) Skills section**
- Reorganize to lead with skills the JD prioritizes
- Add skills the candidate demonstrably has but omitted
- Group logically (Languages, Frameworks, Cloud/Infra, Tools, Methodologies)

**d) Section ordering**
- Place the most JD-relevant sections highest
- For senior roles: Summary → Experience → Skills → Education
- For technical roles: Summary → Skills → Experience → Education
- Remove or minimize sections that don't serve this application

**e) General polish**
- Eliminate first-person pronouns
- Keep to 1 page if <8 years experience, 2 pages max otherwise
- Use consistent date formatting (Mon YYYY)
- Ensure no orphan bullets (every role has 2–5 bullets)

### 5. Generate the output

**Ask the user which format they want if not already specified.** Then follow the appropriate path:

#### Option A: DOCX (default — best for ATS)

Use the `docx` skill (docx-js via Node.js) to produce a clean, ATS-friendly document:

- **Font**: Calibri or Arial, 10–11pt body, 12–14pt name
- **Margins**: 0.5–0.75 inches (tight but readable)
- **No tables for layout** — ATS parsers choke on tables; use paragraphs, tab stops, and spacing
- **No headers/footers for contact info** — some ATS systems skip header content
- **No images, icons, or graphics** — ATS can't read them
- **Section headings**: Bold, slightly larger, with a bottom border (Paragraph border, not a table)
- **Bullet style**: Use `LevelFormat.BULLET` from docx-js numbering config
- **File name**: `{FirstName}_{LastName}_Resume.docx`

#### Option B: PDF

Generate the resume as a `.docx` first using Option A rules, then convert:
```bash
python scripts/office/soffice.py --headless --convert-to pdf {FirstName}_{LastName}_Resume.docx
```
- **File name**: `{FirstName}_{LastName}_Resume.pdf`

#### Option C: Markdown

Output a clean `.md` file with:
- `#` for the candidate's name, `##` for section headings
- Standard markdown bullet lists for experience items
- `**Bold**` for company names and job titles
- A horizontal rule (`---`) between major sections
- Contact info on a single line at the top using pipes: `email | phone | location | LinkedIn`
- **File name**: `{FirstName}_{LastName}_Resume.md`

### 6. Present results
Output to the user:
1. The tailored resume file in their chosen format
2. A brief **changelog** summarizing key changes:
   - Keywords added
   - Bullets rewritten (before → after for top 3)
   - Sections reordered
   - Gaps that couldn't be addressed (honest about what's missing)

## Rules

- **Never fabricate experience.** Only surface and reframe what the candidate actually has.
- **Never copy JD language verbatim into bullets.** Paraphrase naturally.
- **Preserve the candidate's voice.** Match their existing tone and complexity level.
- **ATS first, human second.** The resume must pass automated screening before a human reads it.
- **If the resume is a poor match (<30% keyword overlap), say so.** Suggest which gaps to close before applying.
