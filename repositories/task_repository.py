from sqlalchemy import delete, select, update

from db.models import Task as TaskORM

from .base import BaseRepository


class TaskRepository(BaseRepository):
    async def list_by_user(
        self, user_id: int, limit: int = 50, offset: int = 0
    ) -> list[TaskORM]:
        result = await self.session.execute(
            select(TaskORM)
            .where(TaskORM.user_id == user_id)
            .order_by(TaskORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get(self, task_id: str, user_id: int) -> TaskORM | None:
        result = await self.session.execute(
            select(TaskORM).where(
                TaskORM.id == task_id,
                TaskORM.user_id == user_id,
            )
        )
        return result.scalars().first()

    async def add(self, task: TaskORM) -> TaskORM:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update(
        self, task_id: str, user_id: int, values: dict
    ) -> TaskORM | None:
        result = await self.session.execute(
            update(TaskORM)
            .where(
                TaskORM.id == task_id,
                TaskORM.user_id == user_id,
            )
            .values(**values)
            .returning(TaskORM)
        )
        task = result.scalars().first()
        if task is None:
            return None

        await self.session.commit()
        return task

    async def delete(self, task_id: str, user_id: int) -> int:
        result = await self.session.execute(
            delete(TaskORM).where(
                TaskORM.id == task_id,
                TaskORM.user_id == user_id,
            )
        )
        await self.session.commit()
        return result.rowcount
