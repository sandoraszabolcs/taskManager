from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.api.routes import tasks
from app.core.config import settings

API_PREFIX = "/api"


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # TODO: exception handlers (TaskNotFound -> 404, InvalidTransition -> 409,
    # StaleDataError -> 409)
    app.include_router(health.router, prefix=API_PREFIX, tags=["health"])
    app.include_router(tasks.router, prefix=f"{API_PREFIX}/tasks", tags=["tasks"])
    return app


app = create_app()
