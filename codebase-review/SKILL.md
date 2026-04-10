---
name: codebase-review
description: Analyze an unfamiliar codebase to produce onboarding maps — architecture diagrams, request flow charts, dependency graphs, data model maps, and a guided feature implementation walkthrough. Use when user mentions "review this codebase", "onboard me", "map this repo", "codebase review", "code walkthrough", "how does this project work", "understand this code", or provides a repo path and wants to get up to speed fast. Also triggers for "add a feature walkthrough" or "show me how to implement X in this codebase".
---

# Codebase Review

## Purpose

Take an unfamiliar codebase and produce a comprehensive onboarding package — the kind a senior engineer would build for a new teammate. Outputs include architecture diagrams, request flow charts, data model maps, dependency graphs, and a concrete feature implementation walkthrough that proves you understand the codebase well enough to extend it.

## Quick start

User provides a path to a codebase (local directory or uploaded project). You produce a full review saved to `CODEBASE_REVIEW.md` in the project root, plus visual diagrams rendered inline.

## Workflow

### Phase 1 — Reconnaissance

Before producing anything, build a mental model:

1. **Directory scan** — `find` the project tree (2–3 levels deep), identify framework markers:
   - `package.json`, `nuxt.config.*`, `vue.config.*` → JS/TS frontend
   - `requirements.txt`, `pyproject.toml`, `main.py` → Python backend
   - `*.csproj`, `*.sln`, `Program.cs` → .NET
   - `docker-compose.*`, `Dockerfile` → containerized services
   - `terraform/`, `bicep/`, `infra/` → IaC layer

2. **Entry points** — identify:
   - Server bootstrap files (`main.py`, `Program.cs`, `server.ts`, `app.ts`)
   - Route/controller registrations
   - Frontend page directory (`pages/`, `views/`, `app/`)
   - Config files (env, settings, feature flags)

3. **Key abstractions** — read the top 5–10 most-imported modules to understand:
   - Data models / schemas / entities
   - Service layer patterns (repository, service, handler)
   - Middleware chain
   - Auth/identity approach

4. **Dependency audit** — parse lockfiles/manifests for:
   - Core framework + version
   - Database drivers (which DB?)
   - External service SDKs (Stripe, SendGrid, Azure, AWS)
   - Dev tooling (linters, test frameworks, CI config)

### Phase 2 — Architecture overview

Produce a **Mermaid architecture diagram** rendered via the Excalidraw or Visualizer tool showing:

- Major system boundaries (frontend, API, workers, database, external services)
- Communication protocols between them (REST, GraphQL, gRPC, queues, websockets)
- Data stores and their roles

Also produce a **tech stack summary table**:

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Frontend | NuxtJS | 3.x | SSR + API routes |
| Backend | FastAPI | 0.100+ | Async, Pydantic models |
| Database | PostgreSQL | 15 | Via SQLAlchemy |
| Cache | Redis | 7 | Session + job queue |
| Infra | Docker Compose | — | Local dev |

### Phase 3 — Flow diagrams

Produce **at minimum** these diagrams using Mermaid syntax rendered via the Visualizer tool:

1. **Request lifecycle flowchart** — trace a typical API request from client → middleware → route → service → DB → response. Include auth checks, validation, error handling branches.

2. **Data model relationship diagram** — ER-style diagram of core entities and their relationships (1:many, many:many, ownership).

3. **Dependency / module graph** — which internal modules depend on which. Highlight circular dependencies or god-modules.

4. **Deployment / infrastructure diagram** (if infra config exists) — containers, networking, CI/CD pipeline stages.

### Phase 4 — Codebase health assessment

Evaluate and report on:

- **Patterns used** — MVC, repository pattern, CQRS, event-driven, etc.
- **Testing coverage** — are there tests? what kind? what's untested?
- **Code organization** — flat vs nested, feature-sliced vs layer-sliced
- **Naming conventions** — consistent? framework-idiomatic?
- **Error handling** — centralized? per-route? swallowed?
- **Security posture** — env vars for secrets? auth middleware? CORS config?
- **Tech debt signals** — TODO comments, disabled tests, commented-out code, overly complex functions

### Phase 5 — Feature implementation walkthrough

This is the proof that the review is actionable. Pick a realistic feature (or use one the user provides) and produce:

1. **Feature description** — what it does, who it's for (1–2 sentences)
2. **Files you'd touch** — exact paths with what changes in each
3. **New files you'd create** — with purpose of each
4. **Step-by-step implementation plan**:
   - Data model changes (migrations, schemas)
   - Backend route / service / repository additions
   - Frontend page / component / store additions
   - Test additions
5. **Flowchart of the feature's request path** — Mermaid diagram showing how data flows through the new feature end-to-end
6. **Gotchas** — things in the existing code that would trip you up (naming inconsistencies, missing abstractions, tight coupling)

### Phase 6 — Deliver

Save the full review to `CODEBASE_REVIEW.md` in the project root. Render all diagrams inline in the conversation using the Visualizer tool. Print a summary to the user:

- Stack + architecture one-liner
- Top 3 things to understand first
- Top 3 risks / debt items
- Feature walkthrough summary

Ask: "Want me to dive deeper into any specific area, or walk through a different feature?"

## Diagram rendering rules

- Use Mermaid syntax for all diagrams
- Render via the Visualizer (`show_widget`) tool as inline HTML with embedded Mermaid JS
- Use the Mermaid CDN: `https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js`
- Keep diagrams focused — if an architecture has 20+ services, group them into bounded contexts
- Use color coding: green = healthy, yellow = needs attention, red = risk
- Label all edges (what data flows, what protocol)

## Calibration rules

- **Breadth first, depth on demand.** The initial review covers everything at survey depth. User can ask to drill into any area.
- **Diagrams are not optional.** Every review MUST include at least: architecture diagram, request flow, and data model diagram.
- **Be honest about what you see.** If the code is messy, say so constructively. If it's clean, acknowledge it.
- **Feature walkthrough must be concrete.** Not "you'd add a route" — give the exact file path, function signature, and integration point.
- **Adapt to stack.** A NuxtJS app gets composables/stores/pages analysis. A FastAPI app gets router/dependency-injection/Pydantic analysis. A .NET app gets controller/service/EF analysis. Don't force one framework's vocabulary onto another.

## What this skill does NOT do

- Refactor or modify the codebase
- Run the application or execute tests
- Make git commits or PRs
- Generate production code (the feature walkthrough is a plan, not an implementation)
- Security audit (surface-level posture only, not penetration testing)
