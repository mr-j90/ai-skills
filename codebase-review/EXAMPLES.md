# Codebase Review — Example Output

This is an example of what a completed `CODEBASE_REVIEW.md` looks like for a fictional task management SaaS built with NuxtJS + FastAPI.

---

# Codebase Review: TaskFlow

**Reviewed:** 2025-06-15
**Stack:** NuxtJS 3 (frontend) + FastAPI (backend) + PostgreSQL + Redis
**Repo root:** `/home/user/projects/taskflow`

---

## 1. Architecture overview

TaskFlow is a multi-tenant task management app. The frontend is a NuxtJS 3 SSR application that communicates with a FastAPI backend over REST. Data lives in PostgreSQL with Redis used for session caching and background job queuing.

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Frontend | NuxtJS | 3.11 | SSR mode, Pinia stores, Tailwind CSS |
| Backend | FastAPI | 0.109 | Async endpoints, Pydantic v2 |
| ORM | SQLAlchemy | 2.0 | Async engine, Alembic migrations |
| Database | PostgreSQL | 15.4 | Row-level security for multi-tenancy |
| Cache | Redis | 7.2 | Session store + Celery broker |
| Auth | Auth0 | — | OIDC flow, JWT validation in FastAPI |
| Infra | Docker Compose | — | Local dev; Azure Container Apps in prod |

---

## 2. Directory structure (key paths)

```
taskflow/
├── frontend/
│   ├── pages/
│   │   ├── index.vue              # Dashboard
│   │   ├── projects/[id].vue      # Project detail
│   │   └── settings.vue           # User settings
│   ├── components/
│   │   ├── TaskCard.vue
│   │   ├── ProjectSidebar.vue
│   │   └── NotificationBell.vue
│   ├── composables/
│   │   ├── useAuth.ts             # Auth0 integration
│   │   ├── useApi.ts              # Fetch wrapper with auth headers
│   │   └── useTasks.ts            # Task CRUD composable
│   ├── stores/
│   │   └── projects.ts            # Pinia store
│   └── nuxt.config.ts
├── backend/
│   ├── app/
│   │   ├── main.py                # App factory, router includes
│   │   ├── routers/
│   │   │   ├── projects.py
│   │   │   ├── tasks.py
│   │   │   └── users.py
│   │   ├── services/
│   │   │   ├── project_service.py
│   │   │   └── task_service.py
│   │   ├── models/
│   │   │   ├── project.py         # SQLAlchemy model
│   │   │   ├── task.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── project.py         # Pydantic schemas
│   │   │   └── task.py
│   │   └── deps.py                # DI: get_db, get_current_user
│   ├── alembic/
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 3. Health assessment

| Area | Rating | Notes |
|------|--------|-------|
| Test coverage | 🟡 Yellow | Backend has 40+ unit tests for services but zero integration tests. Frontend has no tests. |
| Error handling | 🟢 Green | Centralized `HTTPException` handler in FastAPI, frontend `useApi` catches and surfaces errors. |
| Code organization | 🟢 Green | Clean separation: routers → services → models. Frontend uses composables well. |
| Security | 🟢 Green | Secrets in `.env`, Auth0 JWT validation middleware, CORS locked to frontend origin. |
| Documentation | 🟡 Yellow | README covers setup but no architecture docs. Inline comments sparse. |
| Dependencies | 🟡 Yellow | FastAPI and SQLAlchemy are current. NuxtJS is one minor behind. No known CVEs. |

---

## 4. Top 3 things to understand first

1. **Auth flow** — Auth0 handles login on the frontend (`useAuth.ts`). The backend validates JWTs via `deps.py:get_current_user`. Every protected route depends on this.
2. **Multi-tenancy** — PostgreSQL RLS policies filter all queries by `tenant_id`. The tenant is extracted from the JWT claims in `deps.py`.
3. **Task state machine** — Tasks move through `draft → active → review → done`. The transitions are enforced in `task_service.py:transition_status()`.

---

## 5. Top 3 risks / tech debt

1. **No frontend tests** — The entire NuxtJS app has zero test coverage. A Vitest + Vue Testing Library setup would be the first investment.
2. **No integration tests** — Backend unit tests mock the DB. No tests verify actual SQL queries or migration compatibility.
3. **Celery worker has no retry logic** — Background jobs (email notifications) fail silently. Needs dead-letter queue or retry policy.

---

## 6. Feature implementation walkthrough: "Add due date reminders"

### What it does
Send users an in-app notification and optional email 24 hours before a task's due date.

### Files you'd touch

| File | Change |
|------|--------|
| `backend/app/models/task.py` | Already has `due_date` field — no change needed |
| `backend/app/models/notification.py` | **NEW** — Notification SQLAlchemy model |
| `backend/app/schemas/notification.py` | **NEW** — Pydantic schema for notification payloads |
| `backend/app/services/notification_service.py` | **NEW** — Logic to create + send notifications |
| `backend/app/routers/notifications.py` | **NEW** — GET /notifications, PATCH /notifications/{id}/read |
| `backend/app/main.py` | Register new notifications router |
| `backend/app/workers/reminder_worker.py` | **NEW** — Celery beat task that runs hourly, finds tasks due in 24h |
| `frontend/composables/useNotifications.ts` | **NEW** — Fetch + poll notifications |
| `frontend/components/NotificationBell.vue` | Add badge count, dropdown list |
| `alembic/versions/xxx_add_notifications.py` | **NEW** — Migration for notifications table |

### Step-by-step plan

1. **Create notification model + migration**
   - Add `Notification` model with fields: `id`, `user_id`, `task_id`, `type` (enum: reminder, mention, assignment), `message`, `read_at`, `created_at`
   - Generate Alembic migration, run it

2. **Build notification service**
   - `create_notification(user_id, task_id, type, message)` — writes to DB
   - `get_unread(user_id)` — returns unread notifications
   - `mark_read(notification_id)` — sets `read_at`

3. **Add API routes**
   - `GET /api/notifications` — paginated list for current user
   - `PATCH /api/notifications/{id}/read` — mark as read
   - Wire auth dependency so users only see their own

4. **Build Celery beat task**
   - Runs every hour via Celery Beat schedule
   - Query: `SELECT * FROM tasks WHERE due_date BETWEEN now() AND now() + interval '24 hours' AND reminder_sent = false`
   - For each result: call `notification_service.create_notification()`, set `reminder_sent = true`
   - Add `reminder_sent: bool` column to tasks (new migration)

5. **Frontend integration**
   - `useNotifications` composable: fetch on mount, poll every 60s
   - Update `NotificationBell.vue`: show count badge, dropdown with notification list, mark-read on click
   - Add toast on new notification arrival

### Gotchas

- **Celery Beat schedule** — The current `docker-compose.yml` runs a Celery worker but has no Beat scheduler. You'll need to add a `celery-beat` service.
- **Timezone handling** — `due_date` is stored as naive datetime. The reminder query needs to account for the user's timezone (stored in user profile) or default to UTC.
- **RLS impact** — The notification query in the worker runs outside a user request context, so it bypasses RLS. You'll need to query with a service-level DB connection that explicitly filters by tenant.
