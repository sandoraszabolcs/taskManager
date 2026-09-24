from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.task import (
    CreateTaskRequest,
    TaskResponse,
)
from app.domain.task import TaskStatus
from app.services.task_service import TaskService
from app.api.dependencies import get_task_service

router = APIRouter(
    tags=["tasks"],
)

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    request: CreateTaskRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = await service.create_task(
        title=request.title,
        description=request.description,
    )

    return TaskResponse.model_validate(task)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = await service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.model_validate(task)


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def list_tasks(
    status: TaskStatus | None = None,
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    tasks = await service.list_tasks(status=status)

    return [
        TaskResponse.model_validate(task)
        for task in tasks
    ]