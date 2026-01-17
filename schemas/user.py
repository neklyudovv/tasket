from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)


class User(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
