from db.models.user import User as UserORM
from schemas.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from core.exceptions import UserAlreadyExistsError, InvalidCredentialsError
import logging

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def new_user(self, username: str, password: str) -> User:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_orm = UserORM(username=username, password_hash=hashed_password)

        result = await self.session.execute(select(UserORM).where(UserORM.username == username))
        if result.scalars().first():
            raise UserAlreadyExistsError

        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        logger.info(f"User created: {username=} ")
        return User.model_validate(user_orm)

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(UserORM).where(UserORM.username == username))
        user = result.scalars().first()
        if user:
            return User.model_validate(user)
        return None

    async def login_user(self, username: str, password: str) -> User | None:
        result = await self.session.execute(select(UserORM).where(UserORM.username == username))
        user = result.scalars().first()
        
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            logger.warning(f"Invalid username or password: {username=}")
            raise InvalidCredentialsError
        logger.info(f"Logged in user: {username=}")
        return User.model_validate(user)
