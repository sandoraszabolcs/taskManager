from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TaskModel
from app.domain.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = TaskRepository(session)

    async def create_task(
        self,
        *,
        title: str,
        description: str | None = None,
    ) -> Task:
        task_model = await self._repository.create(
            title=title,
            description=description,
        )

        await self._session.commit()
        await self._session.refresh(task_model)

        return self._to_domain(task_model)

    async def get_task(self, task_id: UUID) -> Task | None:
        task_model = await self._repository.get_by_id(task_id)

        if task_model is None:
            return None

        return self._to_domain(task_model)

    async def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        task_models = await self._repository.list(status=status)

        return [
            self._to_domain(task_model)
            for task_model in task_models
        ]

    async def start_processing(
        self,
        task_id: UUID,
    ) -> Task | None:
        task_model = await self._repository.get_by_id(task_id)

        if task_model is None:
            return None

        task = self._to_domain(task_model)

        # Business rule lives in the domain.
        task.start_processing()

        task_model.status = task.status
        task_model.error_message = task.error_message

        await self._session.commit()
        await self._session.refresh(task_model)

        return self._to_domain(task_model)

    async def complete_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        task_model = await self._repository.get_by_id(task_id)

        if task_model is None:
            return None

        task = self._to_domain(task_model)

        task.complete()

        task_model.status = task.status
        task_model.error_message = task.error_message

        await self._session.commit()
        await self._session.refresh(task_model)

        return self._to_domain(task_model)

    async def fail_task(
        self,
        task_id: UUID,
        error_message: str,
    ) -> Task | None:
        task_model = await self._repository.get_by_id(task_id)

        if task_model is None:
            return None

        task = self._to_domain(task_model)

        task.fail(error_message)

        task_model.status = task.status
        task_model.error_message = task.error_message

        await self._session.commit()
        await self._session.refresh(task_model)

        return self._to_domain(task_model)

    async def retry_task(
        self,
        task_id: UUID,
    ) -> Task | None:
        task_model = await self._repository.get_by_id(task_id)

        if task_model is None:
            return None

        task = self._to_domain(task_model)

        task.retry()

        task_model.status = task.status
        task_model.retry_count = task.retry_count
        task_model.error_message = task.error_message

        await self._session.commit()
        await self._session.refresh(task_model)

        return self._to_domain(task_model)

    @staticmethod
    def _to_domain(task_model: TaskModel) -> Task:
        return Task(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            status=task_model.status,
            retry_count=task_model.retry_count,
            error_message=task_model.error_message,
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
        )