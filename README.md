# Task Manager

Task processing app: FastAPI + PostgreSQL + Redis (backend), React + TypeScript + Vite (frontend).

Task lifecycle: `PENDING → PROCESSING → COMPLETED | FAILED` (failed tasks can be retried).

## Layout

```
backend/
  app/
    main.py                     FastAPI app, router registration
    core/config.py              Settings (env vars)
    api/                        tasks, metrics, health endpoints + deps.py (DI wiring)
    domain/task.py              TaskStatus + allowed transitions (pure Python)
    schemas/task.py             Pydantic request/response schemas
    services/task_service.py    Business logic, uses repository + domain rules
    services/external_api.py    Simulated external API
    repositories/task_repository.py  Data access only
    db/                         models.py (ORM), session.py, redis.py (queue)
    workers/task_worker.py      Consumes Redis queue, calls TaskService.process
  migrations/                   Alembic migrations (alembic.ini points here)
  tests/
frontend/
  src/
    api/                 HTTP client + typed task API
    types/               Shared TS types
    pages/               Task list, task detail, metrics
    components/          Form, filters, status badge
    hooks/               Data-fetching hooks
```

## Run

```
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000/docs (all routes under /api)
- UI:  http://localhost:5173

## Connecting from the host (PyCharm, psql, redis-cli)

Host ports differ from container ports, because this machine already runs a local PostgreSQL on 5432 and Redis on 6379:

| Service  | Host               | Inside compose network |
|----------|--------------------|------------------------|
| Postgres | `localhost:5434`   | `postgres:5432`        |
| Redis    | `localhost:6380`   | `redis:6379`           |

DB credentials: user `tasks`, password `tasks`, database `tasks` (see `.env`).

## Deploying to Google Cloud

Runs on Cloud Run (project `taskmanagrger`, region `europe-west1`). The worker and Redis are not deployed yet.

| Piece | GCP resource |
|---|---|
| API | Cloud Run service `api`, runs as service account `taskmanager-api` |
| Frontend | Cloud Run service `frontend` (nginx, `prod` target of `frontend/Dockerfile`) |
| Migrations | Cloud Run job `migrate` (`alembic upgrade head`, same image as the API) |
| Database | Cloud SQL `taskmanager-db` (Postgres 16), database and user `tasks` |
| `DATABASE_URL` | Secret Manager secret `database-url` (connects via `/cloudsql/...` socket) |
| Images | Artifact Registry repo `taskmanager`, built by Cloud Build |

### Deploy

```powershell
.\deploy.ps1                  # build, migrate, deploy api + frontend
.\deploy.ps1 -SkipFrontend    # backend only
.\deploy.ps1 -SkipApi         # frontend only
```

Images are tagged with the git commit. Migrations run before the API is deployed, so keep them
backwards compatible. `VITE_API_URL` is baked in at build time (`frontend/cloudbuild.yaml`);
`CORS_ORIGINS` on the `api` service must equal the frontend URL.

### Day to day

```powershell
gcloud run services logs read api --region=europe-west1 --limit=50      # logs
gcloud run services update-traffic api --region=europe-west1 --to-revisions=REVISION=100   # rollback
gcloud sql instances patch taskmanager-db --activation-policy=NEVER     # stop DB (saves cost)
gcloud sql instances patch taskmanager-db --activation-policy=ALWAYS    # start DB
```

### Connecting from PyCharm / psql

```powershell
gcloud auth application-default login     # once
cloud-sql-proxy taskmanagrger:europe-west1:taskmanager-db --port 5435
```

Then connect to `localhost:5435`, database `tasks`, user `tasks`. Password:
`gcloud secrets versions access latest --secret=database-url` (the part between `tasks:` and `@`).
