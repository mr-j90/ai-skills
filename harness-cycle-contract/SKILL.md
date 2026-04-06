---
name: cycle-contract
description: Generate a testable contract for a single build cycle — defining what will be built, acceptance criteria, and how the evaluator will verify completion. Use when user mentions "cycle contract", "define the cycle", "what does done look like", "acceptance criteria", or before starting a build cycle from a spec. Bridges the gap between product spec and verifiable implementation.
---

# Cycle Contract

## Purpose

Before building anything, define exactly what "done" means for this cycle. This contract is the agreement between the builder and the evaluator — the builder implements against it, the evaluator grades against it. No ambiguity, no scope creep, no "I thought that was working."

## Quick start

Read the `SPEC.md` and identify the next cycle to implement. Produce a `CYCLE-CONTRACT.md` that the builder will implement against and the evaluator will test against.

## Workflow

### 1. Identify the cycle

- Read `SPEC.md` for the cycle breakdown.
- Check the project state — what's already been built? Read `CYCLE-LOG.md` if it exists.
- Select the next unfinished cycle.

### 2. Write the contract

Create or overwrite `CYCLE-CONTRACT.md` with:

**Cycle name and number**

**Scope statement** (2–3 sentences)
- What this cycle delivers from the user's perspective.
- What it does NOT include (explicit exclusions prevent scope creep).

**Deliverables** (bulleted list)
- Concrete, observable things that will exist when this cycle is done.
- Example: "A level editor canvas that supports click-to-place tiles on a grid" — not "level editor functionality."

**Acceptance criteria** (numbered list, 10–30 items)
- Each criterion is a testable statement. It either passes or fails.
- Write them as "User can [action] and [expected result]" or "[Component] does [behavior] when [condition]."
- Cover the happy path, key edge cases, and integration with prior cycles.
- Group by feature area if the cycle touches multiple areas.

**Out of scope**
- Explicitly list things that might seem related but are deferred to later cycles.

### 3. Calibration rules

- **Criteria must be binary.** "The design looks good" is not a criterion. "The color palette uses no more than 5 colors and maintains AA contrast ratios" is.
- **Cover integration.** If this cycle builds on prior cycles, include criteria that verify the integration works (e.g., "Sprites created in the sprite editor appear in the level editor's asset picker").
- **Be specific about error states.** "Submitting an empty form shows a validation message" is a criterion. Don't just test the happy path.
- **15–25 criteria is the sweet spot.** Fewer than 10 means you're under-specifying. More than 30 means the cycle scope is too large — split it.
- **No implementation prescriptions.** Say what must be true, not how to make it true.

### 4. Deliver

Save to `CYCLE-CONTRACT.md` in the project root. Print the scope statement and criterion count to the user. Ask: "Ready to build, or want to adjust the contract?"

## Cycle log

After a cycle is completed and passes evaluation, append a summary to `CYCLE-LOG.md`:

```
## Cycle N: [Name]
- Status: PASS
- Criteria: X/Y passed
- Notes: [any deferred items or known issues]
- Date: [timestamp]
```

This gives future cycles (and the planner) context on what's been built.
