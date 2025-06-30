from tasket.db.models import Task
from datetime import datetime
from typing import List
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_user_tasks(user_id: int, session: AsyncSession) -> List[Task]:
    result = await session.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()


async def create_task(title: str, due: datetime, user_id: int, session: AsyncSession) -> Task:
    new_task = Task(
        id=str(uuid4()),
        user_id=user_id,
        title=title,
        due_date=due,
        is_done=False,
        created_at=datetime.utcnow()
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def done_task(task_id: str, user_id: int, session: AsyncSession) -> Task:
    task = await session.get(Task, task_id)

    if task is None or task.user_id != user_id:
        raise ValueError

    task.is_done = True
    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(task_id: str, user_id: int, session: AsyncSession) -> None:
    task = await session.get(Task, task_id)
    if task is None or task.user_id != user_id:
        raise ValueError

    await session.delete(task)
    await session.commit()