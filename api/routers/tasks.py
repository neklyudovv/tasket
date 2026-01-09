from core.task_service import get_user_tasks, create_task, done_task, delete_task, get_single_task
from fastapi import APIRouter, Depends, HTTPException
from ..pydantic_models import TaskCreate, TaskRead
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db_session
from db.models.user import User
from ..deps import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/", response_model=list[TaskRead])
async def get_tasks(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session), limit: int = 50, offset: int = 0):
    return await get_user_tasks(user.id, session, limit, offset)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await get_single_task(task_id, user.id, session)


@router.post("/", response_model=TaskRead)
async def new_task(task: TaskCreate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await create_task(task.title, user.id, session, task.due_date)


@router.patch("/{task_id}/done", response_model=TaskRead)
async def mark_task_done(task_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await done_task(task_id, user.id, session)


@router.delete("/{task_id}")
async def delete_task_by_id(task_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await delete_task(task_id, user.id, session)
