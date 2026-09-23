from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    return TaskService(TaskRepository(session))
