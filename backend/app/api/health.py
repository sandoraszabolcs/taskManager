from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """Liveness: the process is up. No dependency checks."""
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    """Readiness: Postgres and Redis are reachable."""
    # TODO: SELECT 1 on Postgres, PING on Redis; return 503 if either fails
    raise NotImplementedError
