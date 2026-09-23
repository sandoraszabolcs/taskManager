from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TaskModel
from app.domain.task import Task, TaskStatus


class SqlAlchemyTaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        title: str,
        description: str | None,
    ) -> Task:
        model = TaskModel(
            title=title,
            description=description,
            status=TaskStatus.PENDING,
        )

        self._session.add(model)
        await self._session.flush()

        return self._to_domain(model)

    async def get_by_id(
        self,
        task_id: UUID,
    ) -> Task | None:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def list(
        self,
        *,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        query = select(TaskModel).order_by(
            TaskModel.created_at.desc()
        )

        if status is not None:
            query = query.where(TaskModel.status == status)

        result = await self._session.execute(query)

        return [
            self._to_domain(model)
            for model in result.scalars().all()
        ]

    async def update(
        self,
        task: Task,
    ) -> None:
        model = await self._get_model(task.id)

        if model is None:
            raise ValueError(
                f"Task {task.id} does not exist"
            )

        model.title = task.title
        model.description = task.description
        model.status = task.status
        model.retry_count = task.retry_count
        model.error_message = task.error_message

        await self._session.flush()

    async def _get_model(
        self,
        task_id: UUID,
    ) -> TaskModel | None:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    def _to_domain(model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            retry_count=model.retry_count,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
