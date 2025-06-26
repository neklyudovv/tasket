from .models import Task
from datetime import datetime
from typing import List
from uuid import uuid4


async def get_user_tasks(user_id: int) -> List:
    return ['empty']


async def create_task(title: str, due: str, user_id: int) -> Task:
    new_task = Task(
        id=uuid4(),
        user_id=user_id,
        title=title,
        due_date=due,
        is_done=False,
        created_at=datetime.utcnow()
    )
    return new_task