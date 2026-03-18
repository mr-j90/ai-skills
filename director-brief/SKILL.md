---
name: director-brief
description: Generate polished status briefs for Directors and Senior Directors — translating engineering work into business outcomes, risk posture, and resource asks. Covers portfolio-level progress, cross-team dependencies, headcount/capacity, and strategic alignment. Use when user mentions "director update", "director brief", "leadership update", "portfolio status", "program update", "report to director", "monthly update for leadership", or needs to summarize multiple workstreams for a director-level audience.
---

# Director Brief

## Quick start

Produce a structured brief that translates granular engineering work into the language directors care about: business impact, timeline risk, resource needs, and strategic alignment.

## Inputs

The user should provide **at least one** of:
- **Raw status notes** — bullet points, sprint summaries, ticket dumps, or multiple team updates.
- **Time period** — "this month", "this quarter", "last 2 weeks" (default: current month).
- **Workstreams or projects** — names of initiatives being reported on.

Optional:
- **Business context** — OKRs, quarterly goals, or strategic priorities these workstreams ladder into.
- **Known risks or asks** — things the user already knows they need to escalate.
- **Format** — email, slide-ready bullets, one-pager doc, Slack DM (default: email).
- **Director's name** — for personalized addressing.

## Workflow

### 1. Reframe from tasks to outcomes

For every item the user provides, apply this translation:

| Engineering language | Director language |
|---|---|
| "Merged PR for auth refactor" | "Auth system hardened — reduces incident surface by X%" |
| "Migrated 3 services to container apps" | "Infrastructure modernization on track — 3 of 8 services migrated" |
| "Blocked on API access from Platform team" | "Cross-team dependency risk: Platform API access delayed, impacting Q2 milestone" |
| "Hired 2 new engineers" | "Team capacity ramping — 2 new hires onboarding, productive by [date]" |

If the user doesn't provide metrics, ask for them or flag the gap: "I'd strengthen this with a number — do you have one?"

### 2. Structure the brief

Use this skeleton (omit empty sections):

**1. Executive summary (2–3 sentences)**
- Net status: on track / at risk / off track.
- Biggest win this period.
- Biggest risk or ask.

**2. Portfolio status**
For each workstream:
- **Name** — one-line status. 🟢 On Track / 🟡 At Risk / 🔴 Off Track
- Key milestone hit or upcoming.
- If at risk or off track: root cause + mitigation plan.

**3. Cross-team dependencies**
- What's blocked or at risk due to other teams.
- Status of each dependency (resolved / in progress / escalation needed).

**4. Resource & capacity**
- Headcount: current vs plan.
- Capacity constraints or hiring pipeline updates.
- Any reallocation proposals.

**5. Asks / decisions needed**
- Numbered list of specific asks with context.
- Frame as: "I need [decision/resource/access] to [unblock/accelerate X] by [date]."

**6. Forward look (next 2–4 weeks)**
- Key milestones and expected outcomes.
- Risks on the horizon.

### 3. Apply tone and polish

Rules:
- **No jargon without payoff.** "Kubernetes migration" is fine; "refactored the DI container" is not.
- **Lead every paragraph with the conclusion.** Directors skim — put the headline first.
- **Quantify or qualify risk.** "At risk" alone is useless. "At risk — 2-week slip likely if Platform API not available by March 28" is actionable.
- **Be direct on asks.** Don't bury the request in paragraph 3. If you need something, say it clearly.
- **Confidence over hedging.** Replace "I think we might be able to" with "We expect to" or "Our plan is to."
- **Keep it to one page.** If it exceeds ~400 words, tighten.

### 4. Deliver

- **Email** (default): Use the message_compose tool. Subject format: `[Team/Org] Status — [Period]`.
- **Slide-ready bullets**: Output as a structured markdown block the user can paste into a deck.
- **One-pager doc**: Save to `/mnt/user-data/outputs/director-brief-{YYYY-MM-DD}.md`.
- **Slack DM**: Output as a single concise message block.

## Behavioral rules

- Never inflate status. If the user's notes say things are rough, reflect that honestly with a mitigation plan — don't sugarcoat.
- If the user provides no business context or OKRs, ask: "What's the strategic goal these workstreams ladder into?"
- Always propose at least one forward-looking action even if the user didn't mention one.
- If the user dumps raw notes from multiple teams, synthesize across them — don't just list them sequentially.
- Default to email format unless told otherwise.
