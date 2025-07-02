from tasket.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def new_user(username: str, password: str, session: AsyncSession) -> User:
    hashed_password = pwd_context.hash(password)
    user = User(username=username, password_hash=hashed_password)

    if await session.execute(select(User).where(User.username == username)) is not None:
        raise ValueError

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def login_user(username: str, password: str, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise ValueError

    return user
