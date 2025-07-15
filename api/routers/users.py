from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db_session
from core.user_service import new_user, login_user
from ..security import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    created_user = await new_user(user.username, user.password, session)
    return created_user


@router.post("/login")
async def login(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    if await login_user(user.username, user.password, session):
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}