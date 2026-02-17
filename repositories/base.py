from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Holds the session and owns all database access.

    Services depend on repositories instead of touching the session or
    SQLAlchemy directly, keeping persistence concerns out of business logic.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
