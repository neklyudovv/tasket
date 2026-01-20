from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    due_date: datetime | None = None
    is_done: bool | None = None


class Task(BaseModel):
    id: str
    title: str
    description: str | None
    user_id: int
    due_date: datetime | None = None
    is_done: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
