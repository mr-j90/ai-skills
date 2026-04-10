# Zero to Hero — Reference

## Tier scoping rules

### Beginner
- **Assume:** User has never used the tool/framework. May know adjacent tech.
- **Theory focus:** What is it? Why does it exist? Where does it fit in the ecosystem? Core vocabulary.
- **Lab focus:** Install, configure, run hello-world, basic CRUD or core operation.
- **Modules:** 3–4
- **Example progression (MLflow):**
  1. What is experiment tracking & why MLflow? → Install MLflow, start UI
  2. Logging params, metrics, artifacts → Train a model, log everything
  3. Model registry basics → Register and load a model
  4. (Optional) Comparing runs → Use the UI to compare two experiments

### Intermediate
- **Assume:** User has done the basics. Wants real-world patterns and integration.
- **Theory focus:** Architecture, components, how things connect, tradeoffs, config options.
- **Lab focus:** Multi-step workflows, integration with other tools, realistic project structure.
- **Modules:** 4–5
- **Example progression (MLflow):**
  1. MLflow architecture deep dive → Set up remote tracking server (Docker)
  2. Custom metrics & autologging → Compare autolog vs manual for sklearn/pytorch
  3. Model registry lifecycle → Promote model through stages with CI checks
  4. Serving models → Deploy a registered model as a REST endpoint
  5. MLflow + cloud storage → Configure artifact store with Azure Blob / S3

### Advanced
- **Assume:** User is comfortable with standard usage. Wants internals, edge cases, production patterns.
- **Theory focus:** Internal mechanics, performance tuning, failure modes, scaling, security.
- **Lab focus:** Production deployment, custom plugins, debugging, performance benchmarking.
- **Modules:** 5–6
- **Example progression (MLflow):**
  1. MLflow internals & storage backends → Benchmark SQLite vs Postgres tracking store
  2. Custom flavors & plugins → Build a custom model flavor
  3. Multi-tenant MLflow → Deploy isolated tracking per team with auth
  4. CI/CD integration → GitHub Actions pipeline: train → register → deploy
  5. Monitoring & drift detection → Pair MLflow with Evidently or Whylogs
  6. Scaling MLflow → Kubernetes deployment with Helm chart

## Curriculum design rules

1. **Each module is self-contained but builds forward.** A user could stop after any module and have learned something useful. But the labs should ideally chain — module 3's lab might use the model registered in module 2.

2. **Theory before lab, always.** Never throw code at the user before explaining why it matters.

3. **The first module is always orientation.** What is this thing? Why should I care? How does it fit the landscape? This module's lab is always "install and verify."

4. **The last module is always forward-looking.** Point toward production patterns, ecosystem integration, or the next level of depth.

5. **Web search is mandatory for:**
   - Latest stable version numbers
   - Install commands (pip, npm, brew — these change)
   - API signatures if they've changed recently
   - Recommended companion tools

6. **Stack affinity.** When the user's stack is known, lean toward it:
   - Python/FastAPI examples over Node
   - Azure examples over AWS (unless topic is AWS-specific)
   - Vue/Nuxt examples for frontend topics
   - .NET examples when applicable

## Lab template

Every lab follows this structure:

```
### Lab: [Title]

**Objective:** [One sentence — what you'll build/do]

**Prerequisites:** [What must be installed or completed from prior modules]

**Steps:**

1. [Step with full command or code block]
2. [Next step]
   ...

**Expected output:** [What the user should see when done — terminal output, UI screenshot description, or API response]

**Stretch goal:** [Optional challenge that extends the lab — no solution provided, just the prompt]
```

## Handling user requests mid-course

- **"Skip this module"** → Acknowledge, move to next. Note what was skipped in the wrap-up summary.
- **"Go deeper on this"** → Expand the current module with an additional theory block or bonus lab. Don't break the flow — mark it as a detour and return to the outline.
- **"I'm lost"** → Back up. Re-explain the concept differently. Offer a simpler version of the lab.
- **"Change tier"** → Adjust remaining modules. Don't restart — honor what's been covered and re-scope forward.
