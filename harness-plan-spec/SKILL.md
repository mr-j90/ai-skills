---
name: harness-plan-spec
description: Expand a short product idea (1–4 sentences) into a full product specification with features, user stories, technical direction, and a cycle breakdown for implementation. Use when user mentions "plan this", "spec this out", "write a spec", "product spec", "expand this idea", "harness-plan-spec", or provides a short app idea and wants it scoped into a buildable plan before coding begins.
---

# Plan Spec

## Purpose

Take a brief product idea and expand it into a comprehensive, opinionated product specification — the kind a strong PM would write before handing off to engineering. This is the first step in a multi-agent build harness. Do not start coding. Your output is a document, not an implementation.

## Quick start

User provides 1–4 sentences describing what they want to build. You produce a full spec saved to `SPEC.md` in the project root.

## Workflow

### 1. Research phase

Before writing anything:
- If the idea references an existing domain (e.g., "a DAW", "a CRM", "a retro game maker"), web-search for what best-in-class products in that space look like. Understand the feature landscape.
- If the project has an existing codebase, explore it to understand current state, stack, and constraints.
- Ask the user **at most 2 clarifying questions** if critical ambiguity exists. Prefer making opinionated decisions over asking.

### 2. Expand the spec

Write a `SPEC.md` with these sections:

**Product overview** (1 paragraph)
- What it is, who it's for, what makes it distinct.

**Tech stack** (brief)
- Recommend a stack based on the project's needs. Be specific (framework, DB, hosting). If user has a preferred stack, respect it. If not, pick the best fit and justify briefly.

**Features** (the bulk of the spec)
- 8–16 features, ordered by implementation dependency.
- Each feature gets:
  - A **description** (2–3 sentences of product context — why this exists, what it enables).
  - **User stories** (3–6 "As a user, I want to..." statements).
  - No implementation details — the builder decides how.

**AI integration opportunities**
- Identify 2–4 places where Claude or another LLM could add value to the product (natural language interfaces, content generation, intelligent defaults, etc.).
- Be specific — not "add AI" but "use an LLM to generate sprite assets from text descriptions in the sprite editor."

**Cycle breakdown**
- Group features into 4–10 **cycles** (a cycle = one feature or tightly coupled feature group).
- Order by dependency — earlier cycles are foundations, later cycles are enhancements.
- Each cycle gets a 1-line scope statement.

**Design direction** (3–5 sentences)
- Describe the visual identity, mood, and key UI principles. Not wireframes — vibes and constraints. Example: "Dark theme, dense information layout, keyboard-first navigation. Think Linear meets a Bloomberg terminal."

### 3. Calibration rules

- **Be ambitious about scope.** The planner's job is to imagine the best version of this product. The builder will negotiate what's realistic per cycle.
- **Stay at product level.** Don't specify API routes, database schemas, or component hierarchies. That's implementation. You describe *what* and *why*, never *how*.
- **Opinionated > vague.** "The dashboard shows a feed of recent activity" beats "the dashboard shows relevant information." Make concrete product decisions.
- **If in doubt, add the feature.** It's easier for the builder to cut scope than to invent features mid-build.

### 4. Deliver

Save the spec to `SPEC.md` in the project root. Print a summary of the cycle breakdown to the user and ask: "Want to adjust scope before we start building?"

## What this skill does NOT do

- Write code
- Create technical architecture documents
- Generate wireframes or mockups
- Make stack decisions that override explicit user preferences
