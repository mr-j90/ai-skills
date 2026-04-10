# Codebase Review — Reference

## Mermaid diagram templates

Use these as starting points. Adapt to the actual codebase — never force a template onto a codebase that doesn't fit.

---

### Architecture diagram

```mermaid
graph TB
    subgraph Client["🖥️ Client Layer"]
        Browser["Browser / Mobile"]
    end

    subgraph Frontend["📦 Frontend (NuxtJS 3)"]
        Pages["pages/"]
        Components["components/"]
        Composables["composables/"]
        Store["stores/ (Pinia)"]
        APIRoutes["server/api/"]
    end

    subgraph Backend["⚙️ Backend (FastAPI)"]
        Router["Routers"]
        Deps["Dependencies (Auth, DB)"]
        Services["Service Layer"]
        Models["Pydantic Models"]
    end

    subgraph Data["🗄️ Data Layer"]
        DB[(PostgreSQL)]
        Cache[(Redis)]
        Storage[("Blob Storage")]
    end

    subgraph External["🌐 External Services"]
        Auth0["Auth Provider"]
        Stripe["Stripe"]
        Email["SendGrid"]
    end

    Browser -->|HTTPS| Pages
    Pages --> Components
    Pages --> Composables
    Composables --> Store
    Pages --> APIRoutes
    APIRoutes -->|HTTP/REST| Router
    Router --> Deps
    Router --> Services
    Services --> Models
    Services --> DB
    Services --> Cache
    Services --> Storage
    Services --> Auth0
    Services --> Stripe
    Services --> Email
```

---

### Request lifecycle flowchart

```mermaid
flowchart TD
    A["Client sends request"] --> B{"Auth middleware"}
    B -->|No token| C["401 Unauthorized"]
    B -->|Valid token| D["Route handler"]
    D --> E{"Request validation"}
    E -->|Invalid| F["422 Validation Error"]
    E -->|Valid| G["Service layer"]
    G --> H{"Business logic"}
    H -->|DB read/write| I[(Database)]
    H -->|Cache check| J[(Redis)]
    I --> K["Serialize response"]
    J --> K
    K --> L{"Success?"}
    L -->|Yes| M["200 OK + JSON"]
    L -->|No| N["Error handler"]
    N --> O["4xx/5xx + error body"]

    style C fill:#ff6b6b,color:#fff
    style F fill:#ff6b6b,color:#fff
    style O fill:#ff6b6b,color:#fff
    style M fill:#51cf66,color:#fff
```

---

### Data model (ER diagram)

```mermaid
erDiagram
    USER ||--o{ PROJECT : owns
    USER ||--o{ TEAM_MEMBER : "belongs to"
    PROJECT ||--|{ TASK : contains
    PROJECT ||--o{ TEAM_MEMBER : "has members"
    TASK ||--o{ COMMENT : has
    TASK }o--|| USER : "assigned to"
    COMMENT }o--|| USER : "authored by"

    USER {
        uuid id PK
        string email UK
        string name
        string role
        datetime created_at
    }

    PROJECT {
        uuid id PK
        uuid owner_id FK
        string name
        string status
        datetime created_at
    }

    TASK {
        uuid id PK
        uuid project_id FK
        uuid assignee_id FK
        string title
        string status
        int priority
        datetime due_date
    }
```

---

### Module dependency graph

```mermaid
graph LR
    subgraph Core
        Config["config/"]
        DB["db/"]
        Auth["auth/"]
    end

    subgraph Features
        Users["users/"]
        Projects["projects/"]
        Tasks["tasks/"]
        Billing["billing/"]
    end

    subgraph Shared
        Utils["utils/"]
        Middleware["middleware/"]
    end

    Users --> Auth
    Users --> DB
    Projects --> DB
    Projects --> Users
    Tasks --> DB
    Tasks --> Projects
    Tasks --> Users
    Billing --> Users
    Billing --> Projects
    Auth --> Config
    Auth --> DB
    Middleware --> Auth
    Middleware --> Config
    Utils --> Config

    style Config fill:#74c0fc,color:#000
    style DB fill:#74c0fc,color:#000
    style Auth fill:#74c0fc,color:#000
```

---

### Deployment / infra diagram

```mermaid
graph TB
    subgraph CI["CI/CD Pipeline"]
        Push["Git Push"] --> Build["Build & Test"]
        Build --> Image["Container Image"]
        Image --> Registry["Container Registry"]
    end

    subgraph Prod["Production"]
        LB["Load Balancer"]
        App1["App Instance 1"]
        App2["App Instance 2"]
        DB[(PostgreSQL)]
        Cache[(Redis)]
    end

    Registry -->|Deploy| LB
    LB --> App1
    LB --> App2
    App1 --> DB
    App2 --> DB
    App1 --> Cache
    App2 --> Cache
```

---

### Feature implementation flowchart (example: "Add notifications")

```mermaid
flowchart TD
    A["User action triggers event"] --> B["Service emits NotificationEvent"]
    B --> C{"Notification type?"}
    C -->|In-app| D["Write to notifications table"]
    C -->|Email| E["Queue email job"]
    C -->|Push| F["Send via push service"]
    D --> G["SSE/WebSocket push to client"]
    E --> H["Worker picks up job"]
    H --> I["SendGrid API"]
    G --> J["Frontend toast + badge update"]

    style D fill:#74c0fc,color:#000
    style E fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style J fill:#51cf66,color:#000
```

---

## Health assessment rubric

| Area | Green | Yellow | Red |
|------|-------|--------|-----|
| **Test coverage** | Unit + integration tests, CI runs them | Some tests exist, not comprehensive | No tests or tests are all skipped/broken |
| **Error handling** | Centralized handler, typed errors, logging | Mix of try/catch and unhandled | Errors swallowed, no logging, crashes leak stack traces |
| **Code organization** | Consistent pattern, clear boundaries | Mostly consistent with a few outliers | No discernible pattern, god files, circular deps |
| **Security** | Secrets in env, auth middleware, CORS locked, input validated | Most secrets in env, auth exists but gaps | Hardcoded secrets, no auth on some routes, wide-open CORS |
| **Documentation** | README + inline docs on complex logic | README exists, sparse inline docs | No docs, misleading comments |
| **Dependencies** | Up to date, no known CVEs, minimal | Slightly behind, 1–2 advisories | Major versions behind, known vulnerabilities, bloated |

## Stack-specific reconnaissance hints

### NuxtJS / Vue
- Check `nuxt.config.ts` for modules, plugins, runtime config
- Scan `pages/` for route structure (file-based routing)
- Look at `composables/` and `stores/` for state management pattern
- Check `server/api/` for Nitro server routes
- Look for `middleware/` (route guards, auth)
- Check `.env` / `runtimeConfig` for environment handling

### FastAPI / Python
- Check `main.py` or `app.py` for app factory and router inclusion
- Scan `routers/` or `api/` for endpoint definitions
- Look at `models/` for SQLAlchemy/Pydantic models
- Check `dependencies.py` or `deps/` for DI pattern
- Look for `alembic/` for migration strategy
- Check `requirements.txt` / `pyproject.toml` for dependency versions

### .NET
- Check `Program.cs` for service registration and middleware pipeline
- Scan `Controllers/` for API surface
- Look at `Models/` or `Entities/` for EF Core models
- Check `Services/` for business logic layer
- Look for `Migrations/` for EF migration history
- Check `appsettings.json` for config structure

### General
- `docker-compose.yml` — what services exist, what ports, what volumes
- `.github/workflows/` or `azure-pipelines.yml` — CI/CD stages
- `.env.example` — what environment variables are expected
- `README.md` — does it exist? Is it accurate?
