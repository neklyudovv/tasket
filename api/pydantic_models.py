from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    due_to: datetime


class UserModel(BaseModel):
    username: str
    password: str


class TaskRead(BaseModel):
    id: str
    title: str
    due_date: datetime
    is_done: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    username: str
    
    model_config = ConfigDict(from_attributes=True)