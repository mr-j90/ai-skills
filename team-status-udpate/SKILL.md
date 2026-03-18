---
name: team-status-update
description: Generate concise team status updates for engineering managers to share with their direct team, peer managers, or skip-level leads. Covers sprint progress, blockers, shipped work, and upcoming priorities. Use when user mentions "team update", "status update", "standup summary", "sprint update", "weekly update", "team progress", "what shipped", or asks to summarize work for their team or engineering peers.
---

# Team Status Update

## Quick start

Produce a ready-to-send status update summarizing engineering team progress, blockers, and next steps — formatted for Slack, email, or a wiki post.

## Inputs

The user should provide **at least one** of:
- **Raw notes** — pasted bullet points, standup logs, Jira/Linear ticket summaries, or stream-of-consciousness dump.
- **Time period** — "this week", "last sprint", specific dates (default: current week).
- **Audience** — team channel, peer managers, skip-level lead (default: team channel).

Optional:
- **Team name or project name** — used in the header.
- **Format preference** — Slack message, email, wiki/Confluence snippet, markdown (default: Slack).
- **Tone** — casual (team channel), semi-formal (peer managers), crisp (skip-level) (default: inferred from audience).

If the user provides a Linear, Jira, or GitHub link, fetch it first. If they dump raw text, work from that directly.

## Workflow

### 1. Parse and categorize

Sort every item the user provides into buckets:

| Bucket | What goes here |
|---|---|
| Shipped / Completed | Merged PRs, deployed features, closed tickets, resolved incidents |
| In Progress | Active work with expected completion or status |
| Blocked / At Risk | Items waiting on external teams, decisions, or access |
| Upcoming / Next | Planned work for next period |
| Callouts | Wins worth celebrating, lessons learned, team shoutouts |

Drop anything trivial (routine meetings, admin). If a bucket is empty, omit it.

### 2. Write the update

Rules:
- **Lead with impact, not task names.** "Launched real-time notifications for 12K users" beats "Closed PROJ-412."
- **Keep each item to one line.** Two lines max if context is critical.
- **Quantify where possible.** Percentages, user counts, latency numbers, deploy dates.
- **Name blockers concretely.** Who/what is blocking, what's needed to unblock, and a proposed next step.
- **Use plain language.** Avoid jargon that doesn't add precision.
- **Bold the key noun or metric** in each line for scannability.

### 3. Format for channel

**Slack (default)**:
```
*🚀 [Team/Project] — Week of [date]*

*Shipped*
• Item one
• Item two

*In Progress*
• Item (ETA: date)

*Blocked*
• 🔴 Item — waiting on [who/what]. Next step: [action].

*Up Next*
• Item

*Callouts*
• 🎉 Shoutout or win
```

**Email**: Subject line + same structure, no emoji, slightly longer sentences.

**Wiki/Confluence**: Use headings instead of bold, add ticket links inline.

### 4. Deliver

- If the user asked for Slack format, output as a single copy-pasteable block.
- If email, use the message_compose tool.
- If markdown/wiki, save to `/mnt/user-data/outputs/team-update-{YYYY-MM-DD}.md`.

## Behavioral rules

- Never invent work the user didn't mention. If the input is thin, ask for more before guessing.
- If the user says "just clean this up," reshape their raw notes without adding substance.
- Default to concise. A good team update is 8–15 lines, not a novel.
- If blockers are present, always include a proposed next step — don't just list the problem.
- Adapt emoji and tone to audience: casual for team, minimal for skip-level.
