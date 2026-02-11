import logging
from datetime import UTC, datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_payload,
)
from core.exceptions import InvalidCredentialsError
from db.models.refresh_token import RefreshToken as RefreshTokenORM
from schemas.user import User

logger = logging.getLogger(__name__)


class TokenService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_entry(self, user_id: int, jti: str, expires_at: datetime):
        refresh_entry = RefreshTokenORM(
            jti=jti,
            user_id=user_id,
            expires_at=expires_at,
            created_at=datetime.now(UTC),
        )
        self.session.add(refresh_entry)
        await self.session.commit()

    async def create_tokens_for_user(self, user: User):
        username = user.username
        access_token = create_access_token({"sub": username})
        refresh_token, jti, expires_at = create_refresh_token({"sub": username})
        await self.create_refresh_entry(user.id, jti, expires_at)
        return access_token, refresh_token, "bearer"

    async def refresh(self, refresh_token_str: str):
        try:
            payload = decode_token(refresh_token_str)
            validated = verify_token_payload(payload, "refresh")
            username = validated.get("sub")
            jti = validated.get("jti")
        except Exception as exc:
            raise InvalidCredentialsError from exc

        if username is None or jti is None:
            raise InvalidCredentialsError

        result = await self.session.execute(select(RefreshTokenORM).where(RefreshTokenORM.jti == jti))
        db_token = result.scalars().first()
        if not db_token or db_token.revoked:
            if db_token:
                await self.session.execute(
                    update(RefreshTokenORM)
                    .where(RefreshTokenORM.user_id == db_token.user_id, RefreshTokenORM.revoked == False)
                    .values(revoked=True)
                )
                await self.session.commit()
            raise InvalidCredentialsError

        new_access = create_access_token({"sub": username})
        new_refresh, new_jti, new_expires_at = create_refresh_token({"sub": username})

        await self.session.execute(
            update(RefreshTokenORM)
            .where(RefreshTokenORM.jti == jti)
            .values(revoked=True, replaced_by=new_jti)
        )
        new_entry = RefreshTokenORM(
            jti=new_jti,
            user_id=db_token.user_id,
            expires_at=new_expires_at,
            created_at=datetime.now(UTC),
        )
        self.session.add(new_entry)
        await self.session.commit()

        return new_access, new_refresh, "bearer"

    async def logout(self, refresh_token_str: str):
        try:
            payload = decode_token(refresh_token_str)
            validated = verify_token_payload(payload, "refresh")
            jti = validated.get("jti")
        except Exception:
            return

        if jti:
            await self.session.execute(
                update(RefreshTokenORM).where(RefreshTokenORM.jti == jti).values(revoked=True)
            )
            await self.session.commit()

