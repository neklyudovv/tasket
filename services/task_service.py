import logging
from datetime import UTC, datetime
from uuid import uuid4

from core.exceptions import TaskNotFoundError
from db.models import Task as TaskORM
from repositories import TaskRepository
from schemas.task import Task, TaskUpdate

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_user_tasks(
        self, user_id: int, limit: int = 50, offset: int = 0
    ) -> list[Task]:
        tasks = await self.repository.list_by_user(user_id, limit, offset)
        return [Task.model_validate(t) for t in tasks]

    async def get_single_task(self, task_id: str, user_id: int) -> Task:
        task = await self.repository.get(task_id, user_id)

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
        task = TaskORM(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date.replace(tzinfo=None) if due_date else None,
            is_done=False,
            created_at=datetime.now(UTC).replace(tzinfo=None),
        )
        new_task = await self.repository.add(task)

        logger.info(f"Task created: {new_task.id=} {user_id=}")
        return Task.model_validate(new_task)

    async def update_task(
        self, task_id: str, user_id: int, update_data: TaskUpdate
    ) -> Task:
        update_dict = update_data.model_dump(exclude_unset=True)

        if not update_dict:
            return await self.get_single_task(task_id, user_id)

        task = await self.repository.update(task_id, user_id, update_dict)

        if not task:
            logger.warning(
                f"Task not found or permission denied: {task_id=} {user_id=}"
            )
            raise TaskNotFoundError

        logger.info(f"Task updated: {task_id=} {user_id=} {update_dict.keys()}")
        return Task.model_validate(task)

    async def delete_task(self, task_id: str, user_id: int) -> None:
        deleted = await self.repository.delete(task_id, user_id)

        if deleted == 0:
            logger.warning(
                f"Task not found or permission denied: {task_id=} {user_id=}"
            )
            raise TaskNotFoundError

        logger.info(f"Task deleted: {task_id=} {user_id=}")
