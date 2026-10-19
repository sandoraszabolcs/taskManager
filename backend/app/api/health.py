from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.db.session import engine

router = APIRouter()


@router.get("/health")
async def health():
    """Liveness: the process is up. No dependency checks."""
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    """Readiness: Postgres and Redis are reachable."""
    # TODO: PING on Redis once the queue is wired up
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "unavailable", "postgres": "down"})
    return {"status": "ok", "postgres": "up"}
