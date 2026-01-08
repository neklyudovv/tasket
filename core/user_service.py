from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from .exceptions import UserAlreadyExistsError, InvalidCredentialsError
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


async def new_user(username: str, password: str, session: AsyncSession) -> Dict[str, Any]:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(username=username, password_hash=hashed_password)

    result = await session.execute(select(User).where(User.username == username))
    if result.scalars().first():
        raise UserAlreadyExistsError

    session.add(user)
    await session.commit()
    await session.refresh(user)
    logger.info(f"User created: {username=} ")
    return {"id": user.id, "username": user.username}


async def login_user(username: str, password: str, session: AsyncSession) -> Dict[str, Any]:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        logger.warning(f"Invalid username or password: {username=}")
        raise InvalidCredentialsError
    logger.info(f"Logged in user: {username=}")
    return {"id": user.id, "username": user.username}
