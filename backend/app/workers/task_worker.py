"""Worker: pops task ids from Redis and delegates to TaskService.process.

Run with: python -m app.workers.task_worker
"""
import asyncio


async def run() -> None:
    # TODO: loop on dequeue_task(); for each id open a session,
    # build TaskService(TaskRepository(session)) and call service.process(id)
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(run())
