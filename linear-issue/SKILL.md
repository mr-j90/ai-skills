---
name: linear-issue-creator
description: Create well-structured Linear issues with smart label recommendations, T-shirt size estimates, and proper team/project assignment. Use when user mentions "create issue", "new ticket", "file a ticket", "Linear issue", "log a bug", "feature request", or provides a task description and wants it tracked in Linear.
---

# Linear Issue Creator

## Quick start

When the user provides a task description (and optionally a team/project), create a Linear issue with:
1. A clear, actionable title
2. A structured description (context, acceptance criteria, notes)
3. Recommended labels based on content analysis
4. A T-shirt size estimate mapped to a numeric value
5. Appropriate priority

## Workflow

### Step 1 — Gather input

Required from user:
- **What**: A description of the work (can be a sentence, paragraph, or bullet list)
- **Team**: Linear team name (ask if not provided)
- **Project**: Linear project name (ask if not provided)

Optional (infer or ask):
- Priority override
- Assignee
- Due date
- Cycle

### Step 2 — Fetch workspace context

Before creating the issue, fetch existing labels and statuses:

```
Linear:list_issue_labels  → get available labels for the team
Linear:list_issue_statuses → get available statuses for the team
Linear:list_teams → confirm team exists (if ambiguous)
Linear:list_projects → confirm project exists (if ambiguous)
```

### Step 3 — Analyze and recommend

**Title**: Rewrite the user's input into a concise, imperative title (e.g., "Add pagination to users endpoint").

**Labels**: Recommend 1–3 labels from the workspace's existing labels based on:
- `bug` / `fix` → if describing broken behavior
- `feature` / `enhancement` → if describing new capability
- `improvement` → if describing a refinement to existing behavior
- `devops` / `infra` → if CI/CD, pipeline, cloud, or deployment related
- `frontend` / `backend` / `api` → if domain is clear
- `documentation` → if docs-related
- `security` → if auth, permissions, or vulnerability related
- `tech-debt` → if refactor, cleanup, migration
- Fall back to the closest match from the team's actual label list.
- **Never invent labels** — only use labels that exist in the workspace.

**T-shirt size estimate** (mapped to Linear estimate values):
| Size | Points | Heuristic |
|------|--------|-----------|
| S    | 1      | < 2 hours. Single file change, config tweak, copy update. |
| M    | 3      | Half-day to 1 day. A focused feature, bug with known root cause, straightforward integration. |
| L    | 5      | 2–3 days. Cross-cutting work, multiple files/services, needs testing strategy. |
| XL   | 8      | 3–5+ days. Large feature, significant refactor, unknowns, cross-team coordination. |

Assess size by considering: scope of code change, number of services/files touched, testing effort, risk/unknowns, and coordination overhead.

**Priority**: Infer from urgency cues in the description:
| Signal | Priority |
|--------|----------|
| "blocking", "P0", "production down" | 1 (Urgent) |
| "important", "P1", "customer-facing" | 2 (High) |
| Default / no signal | 3 (Normal) |
| "nice to have", "low", "backlog" | 4 (Low) |

### Step 4 — Present recommendation before creating

Show the user a summary before calling `Linear:save_issue`:

```
📋 Issue Summary
─────────────────
Title:    Add pagination to users endpoint
Team:     Engineering
Project:  API Platform
Size:     M (3 pts)
Priority: Normal
Labels:   backend, api, feature
State:    Backlog
───────────────────────────────
Description:
## Context
[Summarized context]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
- Estimate rationale: [why this size]
```

Ask: **"Ready to create this issue, or want to adjust anything?"**

### Step 5 — Create the issue

Call `Linear:save_issue` with all fields:

```
Linear:save_issue
  title: "<imperative title>"
  team: "<team name>"
  project: "<project name>"
  description: "<structured markdown>"
  estimate: <1|3|5|8>
  priority: <1-4>
  labels: ["label1", "label2"]
  state: "Backlog"
```

### Step 6 — Confirm

After creation, report back the issue identifier (e.g., `ENG-123`) and a link if available.

## Rules

- **Never create labels** that don't exist — only select from `list_issue_labels` results.
- **Always confirm** the issue summary with the user before calling `save_issue`.
- If the user provides multiple tasks in one message, create each as a separate issue.
- If team or project is ambiguous, list options and ask.
- Default state is `Backlog` unless user specifies otherwise.
