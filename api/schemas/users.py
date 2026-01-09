from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserModel(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    
    model_config = ConfigDict(from_attributes=True)
