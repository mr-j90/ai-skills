---
name: harness-run
description: Orchestrate a full build harness — plan, contract, build, and QA — from a short product idea to a working application. Chains plan-spec, cycle-contract, build-cycle, and qa-eval into an automated pipeline. Use when user mentions "harness run", "build this app", "full build", "harness-run", or wants to go from idea to working product in one session.
---

# Harness Run

## Purpose

Orchestrate the full build pipeline from a short product idea to a working, QA-verified application. This skill chains the four harness skills in sequence, managing the flow between them.

## Quick start

User provides a 1–4 sentence product idea. You run the full pipeline:

```
plan-spec → for each cycle: cycle-contract → build-cycle → qa-eval → (fix loop) → next cycle
```

## Workflow

### Phase 1: Plan

1. Run the `plan-spec` workflow — expand the idea into `SPEC.md`.
2. Present the cycle breakdown to the user.
3. **Gate: get user approval before proceeding.** The spec is the most important document. A bad spec cascades into everything downstream.

### Phase 2: Build cycles

For each cycle in the spec (in order):

1. **Contract** — Run the `cycle-contract` workflow. Produce `CYCLE-CONTRACT.md`.
2. **Build** — Run the `build-cycle` workflow. Implement the cycle, produce `CYCLE-HANDOFF.md`.
3. **Evaluate** — Run the `qa-eval` workflow. Test the build, produce `QA-REPORT.md`.
4. **Fix loop** — If QA verdict is FAIL:
   - Read `QA-REPORT.md`.
   - Fix the reported issues (you are back in builder mode).
   - Update `CYCLE-HANDOFF.md`.
   - Re-run QA.
   - Max 3 fix iterations per cycle. If still failing after 3, note the remaining issues in `CYCLE-LOG.md` and move on.
5. **Log** — Append cycle results to `CYCLE-LOG.md`.
6. **Context check** — If the conversation is getting long and you feel context pressure, summarize state into the log files and suggest the user start a new session to continue. The file artifacts carry all necessary state.

### Phase 3: Wrap up

After all cycles complete:
1. Run the app end-to-end and verify cross-cycle integration.
2. Write a final `BUILD-SUMMARY.md`:
   - What was built (feature inventory).
   - What works well.
   - Known limitations or deferred items.
   - How to run the application.
3. Commit everything with a clean git history.

## Orchestration rules

- **Persona separation matters.** When you are in builder mode, build. When you switch to evaluator mode, be skeptical. Don't let builder-you influence evaluator-you. The article's key insight: models praise their own work. Fight that.
- **The spec is the source of truth.** If the builder wants to deviate from the spec, it must be a conscious decision noted in the handoff, not silent scope reduction.
- **Don't skip QA to save time.** The evaluator consistently catches issues the builder misses. This is the whole point.
- **File artifacts are the handoff mechanism.** Every agent reads files and writes files. This is how state flows between phases — not conversation memory.
- **Cycles are sequential.** Don't start cycle N+1 until cycle N passes QA (or is explicitly deferred).

## File manifest

The harness produces these files in the project root:

| File | Purpose | Written by |
|------|---------|------------|
| `SPEC.md` | Full product specification | plan-spec |
| `CYCLE-CONTRACT.md` | Current cycle's acceptance criteria | cycle-contract |
| `CYCLE-HANDOFF.md` | Builder's notes for the evaluator | build-cycle |
| `QA-REPORT.md` | Evaluator's test results and grade | qa-eval |
| `CYCLE-LOG.md` | Running log of completed cycles | cycle-contract (after each pass) |
| `BUILD-SUMMARY.md` | Final project summary | harness-run (at end) |

## When context gets long

The article's key finding: agents lose coherence as context fills up. If you notice this happening:
1. Write full state to the file artifacts.
2. Tell the user: "Context is getting heavy. Start a new chat and say 'continue the harness' — all state is in the project files."
3. On resume, read `SPEC.md`, `CYCLE-LOG.md`, and `CYCLE-CONTRACT.md` to reconstruct where you left off.
