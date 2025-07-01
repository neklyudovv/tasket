from tasket.core.task_service import get_user_tasks, create_task, done_task, delete_task
from fastapi import APIRouter, Depends, HTTPException, Response, Header
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from tasket.db.session import get_db_session
from tasket.db.models.user import User
from ..deps import get_current_user

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    due_to: datetime


@router.get("/tasks/", tags=["tasks"])
async def get_tasks(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    tasks = await get_user_tasks(user.id, session)
    if not tasks:
        raise HTTPException(404, "Tasks not found")
    return tasks


@router.post("/tasks/", tags=["tasks"])
async def new_task(task: TaskCreate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await create_task(task.title, task.due_to, user.id, session)


@router.patch("/tasks/{task_id}/done", tags=["tasks"])
async def mark_task_done(task_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    try:
        return await done_task(task_id, user.id, session)
    except ValueError:
        raise HTTPException(404, "Task not found")


@router.delete("/tasks/{task_id}", tags=["tasks"])
async def delete_task_by_id(task_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    try:
        await delete_task(task_id, user.id, session)
    except ValueError:
        raise HTTPException(404, "Task not found")
    return Response(status_code=204)
