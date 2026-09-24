from typing import Protocol

from app.domain.repositories import TaskEventRepository, TaskRepository


class UnitOfWork(Protocol):
    tasks: TaskRepository
    events: TaskEventRepository

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...

