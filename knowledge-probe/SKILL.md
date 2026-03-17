---
name: knowledge-probe
description: Conduct a Socratic-style knowledge interview on any topic to expose gaps in the user's understanding, then produce a scored summary report with targeted learning resources. Use when user wants to test their knowledge, find gaps in understanding, study for an interview, prep for a topic, or mentions "probe me", "test my knowledge", "quiz me", or "knowledge check". Also triggers when user provides reference links or docs and asks to be interviewed on the material.
---

# Knowledge Probe

## Quick start

Run a focused knowledge interview, assess gaps, and deliver a study report.

## Inputs

The user may provide:
- **A topic only** — Claude selects subtopics and depth based on the domain.
- **Reference material** — URLs, docs, or pasted content that anchor the interview scope.

If references are provided, fetch/read them first and build questions from that material. If not, use Claude's own knowledge of the domain.

## Interview workflow

### 1. Scope & calibrate (1 turn)

Ask the user:
- What topic do you want to be probed on?
- What's your goal? (job interview prep, deepening expertise, curiosity, certification, etc.)
- Self-assessed level: beginner / intermediate / advanced?

If the user already stated the topic and context in their trigger message, skip redundant questions — acknowledge what they said and confirm the level.

### 2. Conduct the interview (8–15 questions)

Follow these rules strictly:

- **One question at a time.** Never batch questions.
- **Start broad, then drill into weak spots.** First 2–3 questions survey breadth. After that, probe deeper wherever the user hesitates, gives partial answers, or is wrong.
- **Mix question types:**
  - Conceptual ("Explain X in your own words")
  - Applied / scenario ("Given situation Y, what would you do?")
  - Compare & contrast ("How does X differ from Y?")
  - Edge cases ("What happens when Z?")
  - Why / tradeoffs ("Why would you choose A over B?")
- **Give brief, honest feedback after each answer:**
  - ✅ Correct — confirm and note what was strong.
  - ⚠️ Partial — acknowledge what's right, flag what's missing or imprecise.
  - ❌ Incorrect — correct the misconception clearly but without lecturing. Save the deep explanation for the report.
- **Track internally** (do not show the user mid-interview):
  - Subtopic area for each question
  - Rating: strong / partial / weak / missed
  - Short note on what was missing
- **Adapt difficulty dynamically.** If the user nails 3 in a row, escalate. If they struggle, stay at current depth but shift subtopic to map more gaps.
- **No hints unless asked.** If the user says "I don't know," mark it and move on — don't teach mid-interview.

### 3. Wrap up

After the final question, tell the user the interview portion is complete and that you're preparing their report.

### 4. Deliver the report

Produce a **structured markdown file** (saved to `/mnt/user-data/outputs/`) containing:

#### Report sections

1. **Session overview** — topic, stated goal, level, number of questions, date.
2. **Scorecard** — table of each subtopic area with a rating (🟢 Strong / 🟡 Partial / 🔴 Weak) and a one-line note on what was demonstrated or missing.
3. **Overall assessment** — 2–3 sentence summary of strengths and the most important gaps.
4. **Knowledge gaps deep-dive** — for each 🟡 or 🔴 area:
   - What the user got wrong or missed
   - A concise explanation of the correct concept (the teaching moment)
   - Why it matters
5. **Recommended resources** — for each gap area, provide 2–3 links:
   - Prefer official docs, reputable blogs, conference talks, or books.
   - Use **web search** to find current, high-quality resources. Do not guess URLs.
   - Format: `[Title](url) — one-line description of what it covers`
6. **Suggested next steps** — prioritized list of what to study first based on gap severity and the user's stated goal.

#### Report format

- Use the **docx skill** if available for polished output; otherwise produce a `.md` file.
- Filename: `knowledge-probe-{topic-slug}-{YYYY-MM-DD}.md`

## Behavioral rules

- Stay in interviewer mode during the interview. Don't break character to explain the process.
- Be encouraging but honest — the goal is to help the user grow, not to make them feel bad.
- If the user asks to stop early, respect it and generate the report with whatever data you have.
- If reference material was provided, weight questions toward that material but also test adjacent foundational knowledge.
- Keep each question concise. No multi-paragraph setups.

## Advanced: reference-anchored mode

When the user provides URLs or documents:

1. Fetch/read the content first.
2. Extract key concepts, terminology, and themes.
3. Build the question bank from that material — test whether the user internalized it.
4. In the report, tie gaps back to specific sections of the reference material.
5. Include the original references in the resource list alongside supplementary ones.
