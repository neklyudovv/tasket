from .setup import async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
