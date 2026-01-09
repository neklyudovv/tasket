from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    due_date: datetime | None = None


class TaskRead(BaseModel):
    id: str
    title: str
    due_date: datetime | None = None
    is_done: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
