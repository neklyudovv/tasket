from fastapi import APIRouter, Depends
from ..schemas.users import UserModel, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db_session
from core.user_service import new_user, login_user
from ..security import create_access_token


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserRead)
async def register(user: UserModel, session: AsyncSession = Depends(get_db_session)):
    return await new_user(user.username, user.password, session)


@router.post("/login")
async def login(user: UserModel, session: AsyncSession = Depends(get_db_session)):
    if await login_user(user.username, user.password, session):
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}