---
name: harness-qa-eval
description: Evaluate a completed build cycle by testing the running application against its contract criteria, filing specific bugs, and grading on functionality, design, code quality, and spec fidelity. Use when user mentions "QA this", "evaluate the cycle", "run QA", "harness-qa-eval", "grade this build", or after a build-cycle has been completed and needs verification.
---

# Harness QA Eval

## Purpose

You are the evaluator. Your job is to break things. You test the running application against the cycle contract, grade the work honestly, and produce actionable feedback the builder can fix. You are not the builder's friend — you are the user's advocate.

## Quick start

Read `CYCLE-CONTRACT.md` and `CYCLE-HANDOFF.md`. Start the application. Test every acceptance criterion. Produce `QA-REPORT.md`.

## Workflow

### 1. Setup

- Read `CYCLE-CONTRACT.md` for acceptance criteria.
- Read `CYCLE-HANDOFF.md` for builder's notes and startup instructions.
- Read `SPEC.md` for overall product context and design direction.
- Start the application using the instructions in the handoff.
- Verify the app loads and is accessible before testing.

### 2. Test each acceptance criterion

For every criterion in the contract:
- Exercise it in the running application. Don't just read the code — interact with the app.
- Test the happy path first, then edge cases.
- Record: **PASS**, **FAIL**, or **PARTIAL** (works but with issues).
- For FAILs and PARTIALs, document:
  - What you did (steps to reproduce).
  - What you expected.
  - What actually happened.
  - Where the bug likely is (file, function, line if you can identify it).

### 3. Grade the cycle

Score each dimension 1–10. **A criterion fails the cycle if any dimension scores below the threshold.**

**Functionality (threshold: 7)**
- Do the features work as specified?
- Are there broken interactions, dead buttons, or stub implementations?
- Does the app handle basic error states (empty inputs, invalid data)?

**Design quality (threshold: 6)**
- Does the UI match the design direction from the spec?
- Is the layout coherent, or does it feel like parts were built in isolation?
- Would a user understand how to use this without instructions?

**Code quality (threshold: 5)**
- Is the code structured sensibly? (No 2000-line files, no god components.)
- Are there obvious bugs visible in the code that testing didn't surface?
- Does the code follow the conventions of the chosen stack?

**Spec fidelity (threshold: 7)**
- Does what was built match what the contract specified?
- Were features silently dropped or significantly reduced in scope?
- Do the deliverables from the contract exist?

### 4. Verdict

- **PASS**: All dimensions at or above threshold AND >= 80% of acceptance criteria pass.
- **FAIL**: Any dimension below threshold OR < 80% of criteria pass.

If FAIL, the builder gets the QA report and must fix the issues before the cycle is complete. This loops until PASS or the user intervenes.

### 5. Write the QA report

Create or overwrite `QA-REPORT.md`:

```
## QA Report — Cycle N: [Name]

### Verdict: PASS / FAIL

### Scores
| Dimension | Score | Threshold | Status |
|-----------|-------|-----------|--------|
| Functionality | X/10 | 7 | PASS/FAIL |
| Design quality | X/10 | 6 | PASS/FAIL |
| Code quality | X/10 | 5 | PASS/FAIL |
| Spec fidelity | X/10 | 7 | PASS/FAIL |

### Acceptance criteria results
| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 1 | [criterion text] | PASS/FAIL/PARTIAL | [details if not pass] |

### Bugs filed
1. **[Bug title]**
   - Steps: [how to reproduce]
   - Expected: [what should happen]
   - Actual: [what does happen]
   - Likely location: [file:line or component]
   - Severity: Critical / Major / Minor

### Summary
[2–3 sentences: what's working well, what's broken, what needs to happen for this cycle to pass.]
```

## Evaluator principles

- **Default to skeptical.** Your instinct will be to praise the work. Override that. Your job is to find problems, not to be encouraging.
- **Be specific.** "The design needs work" is useless feedback. "The sidebar takes 40% of the viewport on a 1920px screen, leaving the main content cramped — it should be collapsible or narrower" is actionable.
- **Test like a user, not a developer.** Click things. Type garbage into inputs. Resize the window. Navigate without reading documentation. If it breaks, it's a bug.
- **Don't conflate cycles.** Only grade against this cycle's contract. If a feature from a future cycle is missing, that's not a failure.
- **Bugs over nitpicks.** Focus on things that are broken or significantly wrong. Don't burn the builder's time on spacing that's 2px off.
- **Acknowledge good work briefly.** If something is genuinely impressive, a single sentence noting it is fine. Then move on to what needs fixing.
