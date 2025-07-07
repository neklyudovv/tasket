from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from tasket.db.session import get_db_session
from tasket.core.user_service import new_user, login_user
from tasket.core.exceptions import  UserAlreadyExistsError, InvalidCredentialsError
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
    try:
        created_user = await new_user(user.username, user.password, session)
    except UserAlreadyExistsError as e:
        raise HTTPException(409, e.message)
    return created_user


@router.post("/login")
async def login(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    try:
        if await login_user(user.username, user.password, session):
            token = create_access_token({"sub": user.username})
            return {"access_token": token, "token_type": "bearer"}
    except InvalidCredentialsError as e:
        raise HTTPException(401, e.message)