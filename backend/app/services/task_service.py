"""Task business logic.

Each state change and its TaskEvent are written in the same transaction.
Concurrent updates are caught by the optimistic version check on Task.
"""
import uuid

from app.db.models import Task
from app.domain.task import TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.task import Metrics, TaskCreate, TaskList


class TaskNotFound(Exception):
    pass


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, data: TaskCreate) -> Task:
        # TODO: insert task + CREATED event
        raise NotImplementedError

    async def list_tasks(
        self, *, status: TaskStatus | None, search: str | None, limit: int, offset: int
    ) -> TaskList:
        raise NotImplementedError

    async def get_task(self, task_id: uuid.UUID) -> Task:
        # TODO: load with events, raise TaskNotFound if missing
        raise NotImplementedError

    async def delete_task(self, task_id: uuid.UUID) -> None:
        # TODO: decide whether PROCESSING tasks may be deleted
        raise NotImplementedError

    async def trigger_processing(self, task_id: uuid.UUID) -> Task:
        # TODO: only PENDING tasks; enqueue on Redis after commit
        raise NotImplementedError

    async def retry_task(self, task_id: uuid.UUID) -> Task:
        # TODO: FAILED -> PENDING, retry_count += 1, RETRIED event, enqueue
        raise NotImplementedError

    async def process(self, task_id: uuid.UUID) -> None:
        # Called by the worker: PENDING -> PROCESSING, call external API,
        # -> COMPLETED / FAILED (set error_message), with an event for each step
        raise NotImplementedError

    async def get_metrics(self) -> Metrics:
        raise NotImplementedError
