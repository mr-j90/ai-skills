---
name: build-cycle
description: Implement a single build cycle against its contract — writing code, running it, and self-checking against acceptance criteria before handing off to QA. Use when user mentions "build this cycle", "implement the cycle", "start building", "build-cycle", or after a cycle-contract has been defined and the user is ready to code.
---

# Build Cycle

## Purpose

Implement one cycle of the product spec. You are the builder. You write code, run it, verify it works against the contract, and hand off to the evaluator. You do NOT evaluate your own work as a final judgment — that's the evaluator's job — but you do sanity-check before handoff.

## Quick start

Read `CYCLE-CONTRACT.md`. Build everything it specifies. Commit your work. Write a handoff note.

## Workflow

### 1. Pre-build setup

- Read `SPEC.md` for overall product context and design direction.
- Read `CYCLE-CONTRACT.md` for this cycle's scope and acceptance criteria.
- Read `CYCLE-LOG.md` if it exists to understand what's already been built.
- Explore the codebase to understand current state.
- If this is cycle 1, scaffold the project (install deps, set up the stack, create project structure).

### 2. Plan the implementation

Before writing code, think through:
- What files need to be created or modified?
- What's the dependency order? (Build data layer → API → UI, or whatever fits.)
- Are there any criteria that require specific technical approaches?

Do NOT write a detailed plan document. Just think, then start coding.

### 3. Build

- Implement one feature/criterion at a time. Don't try to do everything in one pass.
- **Run the code frequently.** After every meaningful change, verify it works. Don't write 500 lines and then discover a fundamental error.
- **Use version control.** Commit after each meaningful chunk of work with a descriptive message. This gives the evaluator (and you) rollback points.
- **Respect the design direction** from the spec. If it says "dark theme, keyboard-first," don't build a light theme with no keyboard shortcuts.
- **Wire things end-to-end.** A feature that has a UI but no backend, or a backend but no UI, is not done. Each criterion should be fully testable through the running application.

### 4. Self-check

Before handoff, walk through each acceptance criterion in `CYCLE-CONTRACT.md`:
- Run the app and manually verify each criterion.
- For each one, note PASS or FAIL.
- Fix any FAILs you can.
- If a criterion is genuinely blocked or out of scope, note it with an explanation.

**Be honest in self-assessment.** Your natural tendency is to convince yourself things work. Fight that. If something is flaky, it's a FAIL. The evaluator will find it anyway — better to fix it now.

### 5. Handoff

Create or overwrite `CYCLE-HANDOFF.md`:

```
## Cycle N: [Name] — Builder Handoff

### Self-check results
- Criteria passed: X/Y
- Known issues: [list any FAILs with explanation]

### What was built
- [Brief description of implementation approach]
- [Key files created/modified]

### How to test
- [Commands to start the app]
- [URL to access, if applicable]
- [Any setup steps the evaluator needs]

### Notes for evaluator
- [Anything tricky, areas of concern, or things to pay special attention to]
```

### Build principles

- **Features over polish.** Get all criteria passing before making anything pretty. Functionality first, refinement in response to evaluator feedback.
- **Don't gold-plate.** If the contract says "user can create a sprite," don't build an animation system. That's a later cycle.
- **When stuck for > 10 minutes, pivot.** Try a different approach. Don't tunnel-vision on one solution.
- **Leave the codebase better than you found it.** If you touch a file with obvious issues, fix them. But don't refactor the world — stay focused on the cycle.
