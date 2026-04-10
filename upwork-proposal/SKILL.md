---
name: upwork-proposal
description: Generate tailored Upwork proposals from a job description and the user's resume/experience. Analyzes client needs, maps relevant experience, and outputs a ready-to-paste proposal with cover letter, key qualifications, and suggested questions. Use when user mentions "Upwork", "proposal", "freelance bid", "apply to this job", "write a proposal", pastes a job description from Upwork, or wants to respond to a freelance posting.
---

# Upwork Proposal Generator

## Inputs

| Input | Format | Required |
|-------|--------|----------|
| Job description | Pasted text or URL | Yes |
| Resume / experience | Uploaded file, pasted text, or `RESUME.md` in skill folder | Yes (first run) |
| Tone | `professional`, `conversational`, `technical` | No (default: `conversational`) |
| Rate info | Hourly rate or fixed bid | No (include if user provides) |

### Resume resolution order

1. User pastes or uploads resume in this conversation
2. `RESUME.md` bundled in this skill folder
3. User memories / context already in the conversation
4. **If none found → ask the user before proceeding**

## Workflow

### 1. Parse the job description

Extract and categorize:
- **Project type** — fixed-price vs hourly, one-off vs ongoing
- **Core deliverables** — what the client actually needs built/done
- **Required skills** — languages, frameworks, tools, platforms explicitly mentioned
- **Nice-to-have skills** — secondary mentions, "bonus if" items
- **Client pain signals** — urgency, frustration, past failed hires, complexity complaints
- **Budget signals** — posted budget, "expert" vs "intermediate" tag, expected timeline
- **Red flags** — unrealistic scope, vague requirements, test/scam indicators
- **Questions the client left unanswered** — gaps worth clarifying before starting

### 2. Map experience to requirements

For each required skill/deliverable:
- Find the **strongest match** from the resume (project, role, or bullet)
- Note the **proof point** — what was built, the outcome, or the metric
- Identify **gaps** — requirements with no resume match (be honest)
- Identify **adjacent strengths** — related experience that transfers

### 3. Draft the proposal

Use the structure in [REFERENCE.md](REFERENCE.md) to generate the proposal. Key principles:

- **Open with a hook** — reference the client's specific problem, not a generic greeting
- **Prove fit in 2–3 sentences** — map your strongest experience directly to their need
- **Show understanding** — restate what they need in your own words (proves you read the JD)
- **Propose an approach** — brief, concrete next steps (not a full project plan)
- **Close with a soft CTA** — invite conversation, suggest a quick call
- **Keep it under 200 words** — Upwork clients skim; density beats length

### 4. Generate supporting elements

- **3 clarifying questions** — smart questions that show expertise and uncover scope
- **Suggested rate/bid** — based on complexity, budget signals, and user's target rate
- **Match score** — honest 1–5 rating of how well the user fits this job
- **Red flag summary** — anything the user should watch out for

### 5. Output

Present as a single markdown block with clear sections:
```
## Proposal (ready to paste)
[the proposal text]

## Clarifying Questions
[3 questions to ask the client]

## Match Analysis
- Score: X/5
- Strongest fits: ...
- Gaps: ...
- Red flags: ...

## Suggested Bid
[rate or fixed-price recommendation with reasoning]
```

## Rules

- **Never fabricate experience.** Only reference what the resume supports.
- **Never use generic filler** like "I am a highly motivated professional" — every sentence must be specific.
- **Mirror the client's language.** If they say "webapp" don't say "web application." Match their formality level.
- **Front-load relevance.** The first two sentences determine whether the client keeps reading.
- **Be honest about gaps.** If the match is weak (<2/5), say so and suggest skipping the job.
- **No templates that read like templates.** Each proposal should feel hand-written for that specific job.
