from core.task_service import TaskService
from fastapi import APIRouter, Depends, HTTPException, Request
from ..limiter import limiter
from schemas.task import TaskCreate, Task
from schemas.user import User
from ..deps import get_current_user, get_task_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/", response_model=list[Task])
@limiter.limit("60/minute")
async def get_tasks(
    request: Request,
    user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
    limit: int = 50,
    offset: int = 0
):
    return await service.get_user_tasks(user.id, limit, offset)


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return await service.get_single_task(task_id, user.id)


@router.post("/", response_model=Task)
@limiter.limit("60/minute")
async def new_task(
    request: Request,
    task: TaskCreate,
    user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return await service.create_task(task.title, user.id, task.due_date)


@router.patch("/{task_id}/done", response_model=Task)
async def mark_task_done(
    task_id: str,
    user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return await service.done_task(task_id, user.id)


@router.delete("/{task_id}")
async def delete_task_by_id(
    task_id: str,
    user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    await service.delete_task(task_id, user.id)
