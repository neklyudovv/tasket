from tasket.core.task_service import get_user_tasks, create_task, done_task
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tasket.db.deps import get_db_session

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    due_to: datetime
    user_id: int


@router.get("/tasks/{user_id}", tags=["tasks"])
async def get_tasks(user_id: int, session: AsyncSession = Depends(get_db_session)):
    tasks = await get_user_tasks(user_id, session)
    if not tasks:
        raise HTTPException(404, "Tasks not found")
    return tasks


@router.post("/tasks/", tags=["tasks"])
async def new_task(task: TaskCreate, session: AsyncSession = Depends(get_db_session)):
    return await create_task(task.title, task.due_to, task.user_id, session)


@router.put("/tasks/{task_id}/done", tags=["tasks"])
async def mark_task_done(task_id: str, session: AsyncSession = Depends(get_db_session)):
    try:
        return await done_task(task_id, session)
    except ValueError:
        return HTTPException(404, "Task not found")