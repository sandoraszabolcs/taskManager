from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TaskModel
from app.domain.task import TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        title: str,
        description: str | None,
    ) -> TaskModel:
        task = TaskModel(
            title=title,
            description=description,
            status=TaskStatus.PENDING,
        )

        self._session.add(task)
        await self._session.flush()

        return task

    async def get_by_id(
        self,
        task_id: UUID,
    ) -> TaskModel | None:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        status: TaskStatus | None = None,
    ) -> list[TaskModel]:
        query = select(TaskModel).order_by(
            TaskModel.created_at.desc()
        )

        if status is not None:
            query = query.where(TaskModel.status == status)

        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def update_status(
        self,
        task: TaskModel,
        status: TaskStatus,
    ) -> TaskModel:
        task.status = status

        await self._session.flush()

        return task

    async def increment_retry_count(
        self,
        task: TaskModel,
    ) -> TaskModel:
        task.retry_count += 1

        await self._session.flush()

        return task
