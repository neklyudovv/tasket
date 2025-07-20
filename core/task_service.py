from db.models import Task
from datetime import datetime, UTC
from typing import List
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import TaskNotFoundError, PermissionDeniedError
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


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
        created_at=datetime.now(UTC)
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    logger.info(f"Task created: {new_task.id=} {user_id=}")
    return new_task


async def done_task(task_id: str, user_id: int, session: AsyncSession) -> Task:
    task = await session.get(Task, task_id)

    if task is None:
        logger.warning(f"Task not found: {task_id=} for {user_id=}")
        raise TaskNotFoundError

    if task.user_id != user_id:
        logger.warning(f"Permission denied to modify task: {task_id=} {user_id=}")
        raise PermissionDeniedError

    task.is_done = True
    await session.commit()
    await session.refresh(task)
    logger.info(f"Task marked as done: {task_id=} {user_id=}")
    return task


async def delete_task(task_id: str, user_id: int, session: AsyncSession) -> None:
    task = await session.get(Task, task_id)

    if task is None:
        logger.warning(f"Task not found: {task_id=} for {user_id=}")
        raise TaskNotFoundError

    if task.user_id != user_id:
        logger.warning(f"Permission denied to delete task: {task_id=} {user_id=}")
        raise PermissionDeniedError

    await session.delete(task)
    await session.commit()
    logger.info(f"Task deleted: {task_id=} {user_id=}")
