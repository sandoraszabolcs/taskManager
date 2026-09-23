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
  alembic/                      DB migrations
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
