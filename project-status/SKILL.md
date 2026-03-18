---
name: project-status
description: Generate a focused status update for a single project — covering current state, completed work, in-progress items, blockers, and action items. Designed for quick project check-ins, not full team portfolio updates. Use when user mentions "project status", "project update", "where are we on [project]", "give me a status on", "project XYZ update", "what's the status of", or asks for a single-project progress snapshot with action items.
---

# Project Status

## Quick start

Produce a single-project status snapshot: where we are, what's done, what's left, and who owes what.

## Inputs

The user must provide:
- **Project name** — used in the header and throughout.

The user should provide **at least one** of:
- **Raw notes** — bullet points, ticket summaries, standup notes, or a brain dump of current state.
- **Ticket source** — Linear, Jira, or GitHub link to pull from.

Optional:
- **Audience** — team, peer managers, skip-level/director (default: inferred or asked).
- **Format** — Slack, email, markdown doc (default: Slack).
- **Milestone or deadline** — a target date the project is tracking toward.
- **Owner names** — for assigning action items to specific people.

If the user provides only a project name and no notes, **ask for the raw details before generating**. Never fabricate status.

## Workflow

### 1. Assess overall health

Determine a single project health indicator based on the user's notes:

- 🟢 **On Track** — hitting milestones, no major blockers.
- 🟡 **At Risk** — slipping or blocked but recoverable with action.
- 🔴 **Off Track** — behind plan, needs escalation or re-scoping.

If the notes are ambiguous, ask: "Would you say this project is on track, at risk, or off track right now?"

### 2. Categorize items

Sort everything into:

| Bucket | What goes here |
|---|---|
| Completed | Work that is done — shipped, merged, deployed, signed off |
| In Progress | Active work with current status and expected completion |
| Blocked / At Risk | Items stalled on dependencies, decisions, or access |
| Action Items | Specific next steps with an owner and a due date if known |

Rules:
- Every **action item** must have an **owner** (person or team). If the user didn't specify, leave a `[TBD]` placeholder and flag it.
- Every **blocked item** must have a **proposed unblock path**. If the user didn't provide one, suggest one or ask.
- **Completed** items should lead with the outcome, not the ticket number.
- **In Progress** items should include a rough ETA or % if available.

### 3. Write the update

**Tone by audience:**

| Audience | Tone | Detail level |
|---|---|---|
| Team | Casual, specific, ticket-level | High — names, ticket refs, technical detail OK |
| Peer managers | Semi-formal, outcome-focused | Medium — summarize themes, skip implementation detail |
| Skip-level / Director | Crisp, business-impact framing | Low — headlines, risks, asks only |

**General rules:**
- **Open with the health indicator and a one-line summary.** "Project XYZ is 🟢 on track — auth migration complete, API integration in progress, on target for April 15 launch."
- **Completed items: lead with impact.** Not "closed PROJ-412" but "Auth migration deployed to production — 12K users now on the new flow."
- **Action items: make them assignable.** Each one should be clear enough that someone could drop it into a ticket.
- **Keep it tight.** Target 10–20 lines total. If it's longer, you're writing a report, not a status.

### 4. Format and deliver

**Slack (default):**
```
*📊 [Project Name] Status — [Date]*
*Overall: 🟢 On Track*
[One-line summary]

*✅ Completed*
• Item one
• Item two

*🔧 In Progress*
• Item (ETA: date / ~X% complete)

*🔴 Blocked*
• Item — waiting on [who/what]. Proposed path: [action].

*📋 Action Items*
• [@owner] Action description (by [date])
• [@owner] Action description (by [date])
```

**Email:** Use the message_compose tool. Subject: `[Project Name] Status — [Date]`. Same structure, no emoji, slightly fuller sentences.

**Markdown doc:** Save to `/mnt/user-data/outputs/project-status-{project-slug}-{YYYY-MM-DD}.md`.

## Behavioral rules

- **Never invent status.** If the user gives you a project name and nothing else, ask for details.
- **Always include action items.** If the user's notes don't have explicit next steps, ask: "What are the immediate next steps and who owns them?"
- **Always assign owners to action items.** Use `[TBD]` if unknown, and flag it: "I've marked a few action items as TBD — want to assign owners?"
- **Always include the health indicator.** If you can't determine it from the notes, ask.
- **Don't duplicate between sections.** If something is completed, it shouldn't also appear in action items.
- **Adapt detail level to audience.** A skip-level update with ticket numbers is a smell. A team update without them might lack context.
