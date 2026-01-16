from db.models import Task as TaskORM
from schemas.task import Task
from datetime import datetime, UTC
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import TaskNotFoundError, PermissionDeniedError
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_tasks(self, user_id: int, limit: int = 50, offset: int = 0) -> list[Task]:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.user_id == user_id).order_by(TaskORM.created_at.desc()).limit(limit).offset(offset))
        tasks_orm = result.scalars().all()
        return [Task.model_validate(t) for t in tasks_orm]

    async def get_single_task(self, task_id: str, user_id: int) -> Task:
        task = await self.session.get(TaskORM, task_id)

        if task is None:
            logger.warning(f"Task not found: {task_id=} for {user_id=}")
            raise TaskNotFoundError

        if task.user_id != user_id:
            logger.warning(f"Permission denied to modify task: {task_id=} {user_id=}")
            raise PermissionDeniedError

        logger.info(f"Task viewed: {task_id=} for {user_id=}")
        return Task.model_validate(task)

    async def create_task(self, title: str, user_id: int, due_date: datetime | None = None) -> Task:
        new_task = TaskORM(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            due_date=due_date.replace(tzinfo=None) if due_date else None,
            is_done=False,
            created_at=datetime.now(UTC).replace(tzinfo=None)
        )
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        logger.info(f"Task created: {new_task.id=} {user_id=}")
        return Task.model_validate(new_task)

    async def done_task(self, task_id: str, user_id: int) -> Task:
        task = await self.session.get(TaskORM, task_id)

        if task is None:
            logger.warning(f"Task not found: {task_id=} for {user_id=}")
            raise TaskNotFoundError

        if task.user_id != user_id:
            logger.warning(f"Permission denied to modify task: {task_id=} {user_id=}")
            raise PermissionDeniedError

        task.is_done = True
        await self.session.commit()
        await self.session.refresh(task)
        logger.info(f"Task marked as done: {task_id=} {user_id=}")
        return Task.model_validate(task)

    async def delete_task(self, task_id: str, user_id: int) -> None:
        task = await self.session.get(TaskORM, task_id)

        if task is None:
            logger.warning(f"Task not found: {task_id=} for {user_id=}")
            raise TaskNotFoundError

        if task.user_id != user_id:
            logger.warning(f"Permission denied to delete task: {task_id=} {user_id=}")
            raise PermissionDeniedError

        await self.session.delete(task)
        await self.session.commit()
        logger.info(f"Task deleted: {task_id=} {user_id=}")
