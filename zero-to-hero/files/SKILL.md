---
name: zero-to-hero
description: Deliver a structured, interactive learning course on any technical topic — combining theory explanations with hands-on labs in a progressive zero-to-hero format. Supports beginner, intermediate, and advanced tiers. Use when user mentions "zero to hero", "teach me", "walk me through", "learn about", "course on", "tutorial on", or wants a guided theory+lab breakdown of a topic.
---

# Zero to Hero

## Quick start

Deliver a progressive theory → lab learning experience on any topic the user names.

## Inputs

The user provides:
- **A topic** — e.g. "mlflow", "kubernetes", "fastapi", "docker networking"
- **A tier** (optional) — beginner / intermediate / advanced. If omitted, ask.

## Workflow

### 1. Scope & plan (1 turn)

Confirm the topic and tier. Then use **web search** to find the current state of the topic (latest version, key concepts, official docs). Build a **course outline** and present it:

- Course title
- Tier selected
- Number of modules (3–6 depending on tier)
- For each module: title, theory summary (1 line), lab summary (1 line)

Ask the user to confirm or adjust before starting.

### 2. Deliver modules (1 module per turn)

For each module, deliver **two sections in one message**:

#### Theory section
- Explain the concept clearly — what it is, why it matters, how it fits the bigger picture.
- Use analogies or comparisons the user would relate to (engineering manager, Python/Vue dev context).
- Keep it concise: 3–8 paragraphs. No filler.
- Include a "Key takeaways" summary (2–4 bullet points).

#### Lab section
- Present a **hands-on exercise** that reinforces the theory just taught.
- Provide full working code, commands, or config — not pseudocode.
- Use **web search** if you need to verify current CLI flags, API versions, or install steps.
- Structure every lab with: **Objective → Steps → Expected output → Stretch goal (optional)**.
- Labs should build on each other when possible (module 2 lab extends module 1's output).

After delivering the module, ask: **"Ready for the next module, or do you want to dig deeper here?"**

### 3. Wrap up

After the final module, deliver a **completion summary**:
- Recap of what was covered (one line per module)
- What to explore next (2–3 suggestions with links via web search)
- Save the full course outline + lab code to `/mnt/user-data/outputs/zero-to-hero-{topic-slug}.md`

## Tier definitions

See [REFERENCE.md](REFERENCE.md) for detailed tier scoping rules and lab complexity guidelines.

| Tier | Modules | Theory depth | Lab complexity |
|------|---------|-------------|----------------|
| Beginner | 3–4 | Concepts + "why" | Install, hello world, basic usage |
| Intermediate | 4–5 | Architecture + tradeoffs | Real-world patterns, integration, config |
| Advanced | 5–6 | Internals + edge cases | Production patterns, debugging, performance |

## Behavioral rules

- **One module at a time.** Never dump the whole course in one message.
- **Always verify versions.** Web search before giving install commands or API examples.
- **Labs must run.** Provide complete, copy-paste-ready code. Specify language, deps, and runtime.
- **Match the user's stack** when possible — Python, FastAPI, Vue/Nuxt, .NET, Azure examples preferred.
- **No fluff.** Every paragraph should teach something. Cut motivational padding.
- **If the user asks to skip ahead**, let them. Adjust remaining modules accordingly.
- **If the user is stuck on a lab**, help them debug before moving on.
