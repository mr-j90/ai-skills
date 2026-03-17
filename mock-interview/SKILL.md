---
name: mock-interview
description: Conduct a realistic mock job interview tailored to a specific job description and company. Covers behavioral (STAR), technical, system design, and culture-fit rounds. Always researches the company via web search to tailor questions. Produces a scored feedback report with improved answer suggestions and study areas. Use when user mentions "mock interview", "interview prep", "practice interview", "interview me", provides a job description and asks to be interviewed, or wants to prepare for a specific role at a specific company.
---

# Mock Interview

## Quick start

Run a multi-round mock interview customized to a real job description and company.

## Inputs

The user must provide:
- **Job description** — pasted text, a URL, or an uploaded file.
- **Company name** — used for company research.

Optional:
- **Target round** — behavioral, technical, system design, culture fit, or "full loop" (default: full loop).
- **Resume or background context** — if provided, tailor behavioral questions to their experience.

If the user provides a URL for the job description, fetch it first. If they paste it or upload it, read it directly.

## Preparation workflow (before asking any questions)

### 1. Parse the job description

Extract:
- Role title and level (IC vs manager, seniority)
- Required skills and technologies
- Responsibilities and scope
- Team/org context if mentioned
- Soft skills and leadership signals

### 2. Research the company (required)

Use **web search** to gather:
- Company mission, values, and culture page
- Recent news (funding, launches, reorgs, earnings — last 6 months)
- Glassdoor or public interview-experience themes (general patterns only)
- Tech stack or engineering blog posts if role is technical
- Leadership and org structure if relevant to the level

Compile a brief internal dossier (do NOT show this to the user). Use it to:
- Inform culture-fit and values-based questions
- Add realism to behavioral scenarios
- Ground system design prompts in the company's actual domain

### 3. Build the question bank

Create an internal bank of 15–20 questions across four categories:

| Category | Count | Focus |
|---|---|---|
| Behavioral (STAR) | 4–5 | Leadership, conflict, failure, prioritization, influence |
| Technical / domain | 4–5 | Skills from the JD — coding, architecture, tools, domain knowledge |
| System design | 3–4 | Scaled to role level — high-level for managers, deeper for senior ICs |
| Culture fit / values | 3–4 | Mapped to company values and team dynamics from research |

Adjust weighting based on the role: manager roles get heavier behavioral/culture; IC roles get heavier technical/design.

## Interview workflow

### 4. Open the interview (1 turn)

Set the scene:
- Greet the user as the interviewer would.
- State the role and company naturally (e.g., "Thanks for coming in — we're excited to chat about the Senior Engineering Manager role here at Acme Corp.")
- Briefly describe the interview structure: "We'll go through a few rounds covering behavioral, technical, design, and culture-fit questions."
- Ask if they're ready.

### 5. Conduct the interview (12–16 questions)

Rules:
- **One question at a time.** Never batch.
- **Stay in character** as a professional interviewer. Don't break the fourth wall.
- **Follow-up naturally.** If an answer is vague, probe: "Can you be more specific about your role in that?" or "What was the measurable outcome?" — just like a real interviewer.
- **Use the STAR framework for behavioral Qs.** If the user gives a non-STAR answer, prompt for structure: "Walk me through the Situation and Task first."
- **For system design**, start with a prompt, let them drive, then push on tradeoffs, scaling, and failure modes.
- **Do NOT give feedback or corrections during the interview.** Simply acknowledge and move on, just like a real interview. Short reactions like "Interesting," "Got it," or "Thanks for walking me through that" are fine.
- **Track internally** (hidden from user):
  - Category (behavioral / technical / design / culture)
  - Rating: Strong / Adequate / Weak / Missed
  - Notes on what was good, what was missing, red flags
- **Adapt dynamically.** If the user is crushing behavioral, shift more weight to technical or design. If they struggle on technical, probe a second angle before moving on.
- **Respect time.** If the user says "let's wrap up" or "last question," honor it.

### 6. Close the interview (1 turn)

Stay in character:
- "That's all I had for today. Do you have any questions for me?"
- Answer 1–2 questions the user asks in character (as a hiring manager at that company).
- Then break character: "Great job — let me put together your feedback report."

## Report

### 7. Deliver the report

Produce a **markdown file** saved to `/mnt/user-data/outputs/mock-interview-{company-slug}-{YYYY-MM-DD}.md`.

#### Report sections

1. **Session overview** — role, company, date, number of questions, rounds covered.
2. **Scorecard** — table with columns: Question #, Category, Topic, Rating (🟢 Strong / 🟡 Adequate / 🔴 Weak), One-line note.
3. **Overall assessment** — 3–4 sentences: headline strengths, biggest gaps, hire/no-hire lean with rationale.
4. **Per-question feedback** — for each question:
   - The question asked
   - Summary of the user's answer
   - What was strong
   - What was missing or could improve
   - **Suggested improved answer** — a model answer or key bullet points the user could have hit
5. **Study & prep guide** — prioritized list of areas to work on:
   - For each gap area: what to study, why it matters for this role
   - Use **web search** to find 2–3 current, high-quality resources per area (official docs, blog posts, books, talks)
   - Format: `[Title](url) — one-line description`
6. **Company-specific tips** — based on the research, 3–5 tips for interviewing at this specific company (values to emphasize, culture signals to hit, topics likely to come up).

## Behavioral rules

- Never show the internal question bank or dossier to the user.
- Stay in interviewer character from step 4 through step 6. Only break character for the report.
- Be realistic but not adversarial — the goal is to simulate a real interview, not to trick the user.
- If the user provides a resume, weave their actual experience into behavioral question setups.
- If the user asks to focus on one category only, respect that and adjust question count accordingly.
- Keep questions concise. No multi-paragraph setups.
