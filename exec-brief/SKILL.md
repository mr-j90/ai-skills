---
name: exec-brief
description: Generate executive-level briefs for VPs, SVPs, and C-suite — distilling engineering portfolio status into strategic narrative, business risk, and investment decisions. Focuses on outcomes vs plan, ROI signals, organizational health, and board-ready framing. Use when user mentions "exec update", "executive brief", "VP update", "C-suite update", "board update", "leadership brief", "QBR prep", "quarterly business review", "report to VP", "steering committee", or needs to translate technical work into executive-level strategic communication.
---

# Executive Brief

## Quick start

Produce a tight executive brief that frames engineering work as strategic progress — answering the questions VPs and above actually ask: Are we on plan? What's the business risk? Where should we invest or cut?

## Inputs

The user should provide **at least one** of:
- **Status notes or director-level summaries** — raw bullets, prior briefs, or aggregated team updates.
- **Time period** — "this quarter", "H1", "YTD" (default: current quarter).

Optional:
- **Strategic context** — company OKRs, board priorities, annual plan themes.
- **Audience** — VP of Engineering, CTO, CFO, CEO, board (default: VP of Eng). This changes framing significantly.
- **Format** — email, executive summary doc, QBR slide script, one-pager (default: one-pager doc).
- **Recipient name and title** — for personalized addressing.

## Workflow

### 1. Identify the narrative

Before writing anything, determine the **one-sentence story** this brief tells. Executives don't read updates — they read narratives. Examples:

- "Engineering delivered ahead of plan on product velocity but is carrying unresolved platform debt that threatens H2 reliability targets."
- "The team shipped three revenue-impacting features on time; the primary risk is a widening hiring gap in infrastructure."
- "We're on track for the Q3 launch, but two cross-org dependencies need executive intervention this month."

If the user's notes don't suggest a clear narrative, ask: "If your VP could remember one thing from this update, what should it be?"

### 2. Structure the brief

Use this skeleton — **every section must earn its space**. If a section adds no signal, cut it.

**1. Bottom line (2–3 sentences max)**
- The narrative from Step 1, stated as a conclusion.
- Net assessment: on plan / ahead / behind / pivoting.
- The single most important thing the exec should know or act on.

**2. Outcomes vs plan**
A compact table or 3–5 bullet points:

| Initiative | Plan | Actual | Status | Note |
|---|---|---|---|---|
| Project Alpha launch | Q1 | On track for Mar 30 | 🟢 | Beta feedback positive |
| Platform migration | 60% by Q1 | 45% | 🟡 | Dep on Platform team; mitigation in place |

- Max 5 rows. If you have 12 workstreams, group them into 3–4 themes.
- Status must include a qualifier, not just a color.

**3. Business risk register (top 3 only)**
For each risk:
- **Risk**: One-line description.
- **Impact**: What happens if unmitigated (revenue, timeline, reliability, reputation).
- **Likelihood**: High / Medium / Low.
- **Mitigation**: What's being done. What needs executive help.

Executives track risk, not task lists. Three well-framed risks beat ten vague ones.

**4. Investment signals**
This is the section that separates exec briefs from status updates. Include when relevant:
- **Double down**: Where incremental investment would accelerate outcomes.
- **Watch**: Areas performing but with emerging risk.
- **Reconsider**: Efforts that may not justify continued investment.

Frame as options, not demands: "Adding 2 engineers to Platform would recover the migration timeline by 4 weeks."

**5. Organizational health (optional — include for VP+ audiences)**
- Headcount: plan vs actual, attrition, key hires.
- Team velocity or throughput trends (directional, not granular).
- Morale or culture signals if relevant (post-survey, post-reorg).

**6. Decisions or endorsements needed**
- Numbered, each with: the decision, why now, recommended path.
- Frame as: "Recommend [action]. This [unlocks/mitigates X]. Requesting endorsement by [date]."

### 3. Apply executive voice

Rules:
- **No engineering jargon.** "We migrated to event-driven architecture" → "We modernized the order processing system, improving reliability and reducing processing time by 40%."
- **Everything connects to business outcomes.** Revenue, cost, risk, speed, customer impact, or competitive position.
- **Confidence with intellectual honesty.** "We're on track" when you are. "We're behind, and here's the recovery plan" when you're not. Never "cautiously optimistic."
- **Brevity is respect.** Executives have 90 seconds for your update. One page max. 300–500 words.
- **Action-oriented closings.** End with what you need, not a summary of what you said.

### Audience-specific framing

| Audience | Emphasize | De-emphasize |
|---|---|---|
| VP of Engineering | Execution health, team capacity, technical risk | Revenue framing |
| CTO | Architecture decisions, platform bets, tech debt trajectory | Hiring details |
| CFO | Cost, ROI, headcount efficiency, burn rate | Technical details |
| CEO / Board | Strategic alignment, competitive position, milestone confidence | Everything granular |

### 4. Deliver

- **One-pager doc** (default): Save to `/mnt/user-data/outputs/exec-brief-{YYYY-MM-DD}.md`.
- **Email**: Use message_compose tool. Subject: `[Org] Executive Brief — [Period]`.
- **QBR slide script**: Output as speaker-notes-style markdown, one section per slide.
- **Slack DM**: Compress to 8–10 lines max with a link to the full doc.

## Behavioral rules

- Never pad. If the user has 3 things to report, the brief has 3 things. Don't manufacture a fourth.
- If the user provides granular engineering notes, your job is to **ruthlessly abstract up**. They shouldn't recognize their Jira tickets in the output.
- Always ask for the strategic context if the user doesn't provide it. An exec brief without OKR alignment is just a status update.
- If the user says "things are fine," push back: "What's the one thing that could go wrong in the next 30 days?"
- Default to one-pager doc format unless told otherwise.
- If the user asks for a QBR or board update, web-search for the company's recent public context (earnings, press, competitive moves) to ensure the brief is aligned with what leadership is hearing externally.
