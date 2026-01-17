from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    due_date: datetime | None = None


class Task(BaseModel):
    id: str
    title: str
    user_id: int
    due_date: datetime | None = None
    is_done: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
