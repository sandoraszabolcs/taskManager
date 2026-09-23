from uuid import UUID

from app.domain.repositories import TaskRepository
from app.domain.task import Task, TaskStatus


class TaskService:
    def __init__(
        self,
        repository: TaskRepository,
    ) -> None:
        self._repository = repository

    async def create_task(
        self,
        *,
        title: str,
        description: str | None = None,
    ) -> Task:
        return await self._repository.create(
            title=title,
            description=description,
        )

    async def get_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        return await self._repository.get_by_id(task_id)

    async def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        return list(
            await self._repository.list(status=status)
        )

    async def start_processing(
        self,
        task_id: UUID,
    ) -> Task | None:
        task = await self._repository.get_by_id(task_id)

        if task is None:
            return None

        task.start_processing()

        await self._repository.update(task)

        return task

    async def complete_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        task = await self._repository.get_by_id(task_id)

        if task is None:
            return None

        task.complete()

        await self._repository.update(task)

        return task

    async def fail_task(
        self,
        task_id: UUID,
        error_message: str,
    ) -> Task | None:
        task = await self._repository.get_by_id(task_id)

        if task is None:
            return None

        task.fail(error_message)

        await self._repository.update(task)

        return task

    async def retry_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        task = await self._repository.get_by_id(task_id)

        if task is None:
            return None

        task.retry()

        await self._repository.update(task)

        return task

