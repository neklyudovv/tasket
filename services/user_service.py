import logging

import bcrypt
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from db.models.user import User as UserORM
from schemas.user import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def new_user(self, username: str, password: str) -> User:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        try:
            result = await self.session.execute(
                insert(UserORM)
                .values(username=username, password_hash=hashed_password)
                .returning(UserORM)
            )
            user = result.scalars().first()
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError

        logger.info(f"User created: {username=} ")
        return User.model_validate(user)

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username)
        )
        user = result.scalars().first()
        if user:
            return User.model_validate(user)
        return None

    async def login_user(self, username: str, password: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username)
        )
        user = result.scalars().first()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            logger.warning(f"Invalid username or password: {username=}")
            raise InvalidCredentialsError
        logger.info(f"Logged in user: {username=}")
        return User.model_validate(user)
