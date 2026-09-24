from uuid import UUID

from app.domain.unit_of_work import UnitOfWork
from app.domain.task import Task, TaskStatus, TaskEventType


class TaskService:
    """
    Service class for managing tasks and their events.
    """
    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self._uow = uow

    async def create_task(
        self,
        *,
        title: str,
        description: str | None = None,
    ) -> Task:
        task = await self._uow.tasks.create(
            title=title,
            description=description,
        )

        await self._uow.events.create(
            task_id=task.id,
            event_type=TaskEventType.CREATED,
        )

        await self._uow.commit()

        return task

    async def get_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        return await self._uow.tasks.get_by_id(task_id)

    async def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        return list(
            await self._uow.tasks.list(status=status)
        )

    async def start_processing(
            self,
            task_id: UUID,
    ) -> Task | None:
        task = await self._uow.tasks.get_by_id(task_id)

        if task is None:
            return None

        task.start_processing()

        await self._uow.tasks.update(task)

        await self._uow.events.create(
            task_id=task.id,
            event_type=TaskEventType.PROCESSING_STARTED,
        )

        await self._uow.commit()

        return task

    async def complete_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        task = await self._uow.tasks.get_by_id(task_id)

        if task is None:
            return None

        task.complete()

        await self._uow.tasks.update(task)

        await self._uow.events.create(
            task_id=task.id,
            event_type=TaskEventType.COMPLETED,
        )

        await self._uow.commit()

        return task

    async def fail_task(
        self,
        task_id: UUID,
        error_message: str,
    ) -> Task | None:
        task = await self._uow.tasks.get_by_id(task_id)

        if task is None:
            return None

        task.fail(error_message)

        await self._uow.tasks.update(task)

        await self._uow.events.create(
            task_id=task.id,
            event_type=TaskEventType.FAILED,
            metadata={"error_message": error_message},
        )

        await self._uow.commit()

        return task

    async def retry_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        task = await self._uow.tasks.get_by_id(task_id)

        if task is None:
            return None

        task.retry()

        await self._uow.tasks.update(task)

        await self._uow.events.create(
            task_id=task.id,
            event_type=TaskEventType.RETRYING,
            metadata={"retry_count": task.retry_count},
        )

        await self._uow.commit()

        return task

