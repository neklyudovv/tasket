import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import decode_token
from db.session import get_db_session
from schemas.user import User
from services.task_service import TaskService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(session)


def get_task_service(session: AsyncSession = Depends(get_db_session)) -> TaskService:
    return TaskService(session)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
