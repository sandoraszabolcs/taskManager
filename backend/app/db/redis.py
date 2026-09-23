from redis.asyncio import Redis

from app.core.config import settings

redis = Redis.from_url(settings.redis_url, decode_responses=True)


async def enqueue_task(task_id: str) -> None:
    # TODO: push task id onto the processing queue
    raise NotImplementedError


async def dequeue_task(timeout: int = 5) -> str | None:
    # TODO: blocking pop from the processing queue
    raise NotImplementedError
