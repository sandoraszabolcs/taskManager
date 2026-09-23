"""Data access for tasks and task events. No business rules here."""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task, TaskEvent
from app.domain.task import TaskEventType, TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task: Task) -> Task:
        raise NotImplementedError

    async def get(self, task_id: uuid.UUID, *, with_events: bool = False) -> Task | None:
        raise NotImplementedError

    async def list(
        self, *, status: TaskStatus | None, search: str | None, limit: int, offset: int
    ) -> tuple[list[Task], int]:
        raise NotImplementedError

    async def delete(self, task: Task) -> None:
        raise NotImplementedError

    async def add_event(
        self, task_id: uuid.UUID, event_type: TaskEventType, metadata: dict | None = None
    ) -> TaskEvent:
        raise NotImplementedError

    async def count_by_status(self) -> dict[TaskStatus, int]:
        raise NotImplementedError
