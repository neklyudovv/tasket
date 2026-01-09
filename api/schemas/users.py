from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: int
    username: str
    
    model_config = ConfigDict(from_attributes=True)
