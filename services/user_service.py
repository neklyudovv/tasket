import logging

from api.security import hash_password
from db.models.user import User as UserORM
from repositories import UserRepository
from schemas.user import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def new_user(self, username: str, password: str) -> User:
        user = await self.repository.add(
            UserORM(username=username, password_hash=hash_password(password))
        )

        logger.info(f"User created: {username=} ")
        return User.model_validate(user)

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.repository.get_by_username(username)
        if user:
            return User.model_validate(user)
        return None
