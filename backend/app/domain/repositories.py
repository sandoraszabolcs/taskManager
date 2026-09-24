from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from app.domain.task import (
    Task,
    TaskEvent,
    TaskEventType,
    TaskStatus,
)


class TaskRepository(Protocol):
    async def create(
        self,
        *,
        title: str,
        description: str | None,
    ) -> Task:
        ...

    async def get_by_id(
        self,
        task_id: UUID,
    ) -> Task | None:
        ...

    async def list(
        self,
        *,
        status: TaskStatus | None = None,
    ) -> Sequence[Task]:
        ...

    async def update(
        self,
        task: Task,
    ) -> None:
        ...


class TaskEventRepository(Protocol):
    async def create(
        self,
        *,
        task_id: UUID,
        event_type: TaskEventType,
        metadata: dict[str, object] | None = None,
    ) -> TaskEvent:
        ...

    async def list_for_task(
        self,
        task_id: UUID,
    ) -> Sequence[TaskEvent]:
        ...
