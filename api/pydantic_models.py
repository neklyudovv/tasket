from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    due_to: datetime

class UserModel(BaseModel):
    username: str
    password: str