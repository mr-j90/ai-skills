# Zero to Hero — Examples

## Example 1: Trigger and course plan

**User:** `/zero-to-hero mlflow`

**Claude:**
> What tier would you like?
> - **Beginner** — install, log experiments, basic model registry
> - **Intermediate** — remote tracking, autologging, model serving, cloud storage
> - **Advanced** — custom plugins, multi-tenant, CI/CD pipelines, scaling

**User:** `intermediate`

**Claude:**
> Here's your course outline for **MLflow — Intermediate**:
>
> | # | Module | Theory | Lab |
> |---|--------|--------|-----|
> | 1 | Architecture & Components | Tracking server, model registry, artifact stores | Spin up a remote tracking server in Docker |
> | 2 | Autologging & Custom Metrics | autolog frameworks, manual logging tradeoffs | Compare autolog vs manual for an sklearn pipeline |
> | 3 | Model Registry Lifecycle | Stages, transitions, approval patterns | Promote a model through staging → production |
> | 4 | Model Serving | Built-in serving, REST API, batch scoring | Deploy a registered model as a local REST endpoint |
> | 5 | Cloud Artifact Storage | S3/Azure Blob config, artifact access patterns | Configure MLflow to store artifacts in Azure Blob |
>
> Ready to start Module 1?

## Example 2: Module delivery (theory + lab)

**Claude (Module 1):**

> ## Module 1: MLflow Architecture & Components
>
> ### Theory
>
> MLflow has four core components that work together...
> [3-6 paragraphs explaining tracking server, model registry, artifact store, projects]
>
> **Key takeaways:**
> - The tracking server is the brain — it stores run metadata in a backend store
> - Artifacts (models, plots, data) live separately from metadata
> - The model registry is a versioned catalog on top of the artifact store
>
> ### Lab: Stand Up a Remote Tracking Server
>
> **Objective:** Run MLflow tracking server backed by SQLite with a local artifact root, then log a run against it.
>
> **Prerequisites:** Python 3.10+, Docker (optional)
>
> **Steps:**
>
> 1. Install MLflow:
>    ```bash
>    pip install mlflow==2.16.0
>    ```
>
> 2. Start the tracking server:
>    ```bash
>    mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0 --port 5000
>    ```
>
> 3. In a new terminal, log a test run:
>    ```python
>    import mlflow
>    mlflow.set_tracking_uri("http://localhost:5000")
>    mlflow.set_experiment("hello-mlflow")
>    with mlflow.start_run():
>        mlflow.log_param("learning_rate", 0.01)
>        mlflow.log_metric("accuracy", 0.95)
>    ```
>
> 4. Open `http://localhost:5000` — you should see the `hello-mlflow` experiment with one run.
>
> **Expected output:** MLflow UI showing one experiment, one run, with `learning_rate=0.01` and `accuracy=0.95`.
>
> **Stretch goal:** Switch the backend store from SQLite to PostgreSQL using Docker Compose.
>
> ---
> Ready for Module 2, or want to dig deeper here?

## Example 3: User skips ahead

**User:** `skip module 3, I already know the registry`

**Claude:**
> Got it — skipping Module 3 (Model Registry Lifecycle). I'll note it in the wrap-up. Moving to Module 4: Model Serving.

## Example 4: User changes tier

**User:** `this feels too easy, can we switch to advanced?`

**Claude:**
> No problem. We've covered modules 1–2 at intermediate level. I'll re-scope the remaining modules at advanced depth:
>
> | # | Module | Theory | Lab |
> |---|--------|--------|-----|
> | 3 | Custom Flavors & Plugins | Building custom model flavors | Create a custom MLflow flavor |
> | 4 | CI/CD Integration | Train → register → deploy pipelines | GitHub Actions pipeline with MLflow |
> | 5 | Scaling MLflow | Kubernetes, Helm, multi-tenant auth | Deploy MLflow on K8s with Helm |
>
> Ready for Module 3?
