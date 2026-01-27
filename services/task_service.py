import logging
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import TaskNotFoundError
from db.models import Task as TaskORM
from schemas.task import Task, TaskUpdate

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_tasks(
        self, user_id: int, limit: int = 50, offset: int = 0
    ) -> list[Task]:
        result = await self.session.execute(
            select(TaskORM)
            .where(TaskORM.user_id == user_id)
            .order_by(TaskORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        tasks = result.scalars().all()
        return [Task.model_validate(t) for t in tasks]

    async def get_single_task(self, task_id: str, user_id: int) -> Task:
        result = await self.session.execute(
            select(TaskORM)
            .where(
                TaskORM.id == task_id,
                TaskORM.user_id == user_id
            )
        )
        task = result.scalars().first()

        if not task:
            logger.warning(f"Task not found: {task_id=} for {user_id=}")
            raise TaskNotFoundError

        return Task.model_validate(task)

    async def create_task(
        self,
        title: str,
        user_id: int,
        due_date: datetime | None = None,
        description: str | None = None,
    ) -> Task:
        result = await self.session.execute(
            insert(TaskORM)
            .values(
                id=str(uuid4()),
                user_id=user_id,
                title=title,
                description=description,
                due_date=due_date.replace(tzinfo=None) if due_date else None,
                is_done=False,
                created_at=datetime.now(UTC).replace(tzinfo=None),
            )
            .returning(TaskORM)
        )
        new_task = result.scalars().first()

        await self.session.commit()
        logger.info(f"Task created: {new_task.id=} {user_id=}")
        return Task.model_validate(new_task)

    async def update_task(
        self, task_id: str, user_id: int, update_data: TaskUpdate
    ) -> Task:
        update_dict = update_data.model_dump(exclude_unset=True)

        if not update_dict:
            return await self.get_single_task(task_id, user_id)

        result = await self.session.execute(
            update(TaskORM)
            .where(
                TaskORM.id == task_id,
                TaskORM.user_id == user_id
            )
            .values(**update_dict)
            .returning(TaskORM)
        )
        task = result.scalars().first()

        if not task:
            logger.warning(
                f"Task not found or permission denied: {task_id=} {user_id=}"
            )
            raise TaskNotFoundError

        await self.session.commit()
        logger.info(f"Task updated: {task_id=} {user_id=} {update_dict.keys()}")
        return Task.model_validate(task)

    async def delete_task(self, task_id: str, user_id: int) -> None:
        result = await self.session.execute(
            delete(TaskORM)
            .where(
                TaskORM.id == task_id,
                TaskORM.user_id == user_id
            )
        )

        if result.rowcount == 0:
            logger.warning(
                f"Task not found or permission denied: {task_id=} {user_id=}"
            )
            raise TaskNotFoundError

        await self.session.commit()
        logger.info(f"Task deleted: {task_id=} {user_id=}")
