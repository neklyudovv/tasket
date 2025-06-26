from http.client import HTTPException
from core.task_service import get_user_tasks, create_task
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    due_to: str
    user_id: int

@router.get("/tasks/{user_id}", tags=["tasks"])
async def get_tasks(user_id: int):
    tasks = await get_user_tasks(user_id)
    if not tasks:
        raise HTTPException(404, "Tasks not found")
    return tasks


@router.post("/tasks/", tags=["tasks"])
async def new_task(task: TaskCreate):
    return await create_task(task.title, task.due_to, task.user_id)
