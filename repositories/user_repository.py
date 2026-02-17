from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import UserAlreadyExistsError
from db.models.user import User as UserORM

from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get_by_username(self, username: str) -> UserORM | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username)
        )
        return result.scalars().first()

    async def add(self, user: UserORM) -> UserORM:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError

        await self.session.refresh(user)
        return user
