import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from api.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
    verify_token_payload,
)
from core.exceptions import InvalidCredentialsError
from db.models.refresh_token import RefreshToken as RefreshTokenORM
from repositories import RefreshTokenRepository, UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.users = UserRepository(session)
        self.tokens = RefreshTokenRepository(session)

    async def authenticate(self, username: str, password: str):
        """Verify credentials and issue a fresh access/refresh token pair."""
        user = await self.users.get_by_username(username)

        if not user or not verify_password(password, user.password_hash):
            logger.warning(f"Invalid username or password: {username=}")
            raise InvalidCredentialsError

        logger.info(f"Logged in user: {username=}")
        return await self._issue_tokens(user.id, user.username)

    async def _issue_tokens(self, user_id: int, username: str):
        access_token = create_access_token({"sub": username})
        refresh_token, jti, expires_at = create_refresh_token({"sub": username})
        await self.tokens.add(
            RefreshTokenORM(
                jti=jti,
                user_id=user_id,
                expires_at=expires_at,
                created_at=datetime.now(UTC),
            )
        )
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

        db_token = await self.tokens.get_by_jti(jti)
        if not db_token or db_token.revoked:
            if db_token:
                # Reuse of a revoked token: revoke the whole family.
                await self.tokens.revoke_all_for_user(db_token.user_id)
            raise InvalidCredentialsError

        new_access = create_access_token({"sub": username})
        new_refresh, new_jti, new_expires_at = create_refresh_token({"sub": username})

        new_entry = RefreshTokenORM(
            jti=new_jti,
            user_id=db_token.user_id,
            expires_at=new_expires_at,
            created_at=datetime.now(UTC),
        )
        await self.tokens.rotate(jti, new_entry)

        return new_access, new_refresh, "bearer"

    async def logout(self, refresh_token_str: str):
        try:
            payload = decode_token(refresh_token_str)
            validated = verify_token_payload(payload, "refresh")
            jti = validated.get("jti")
        except Exception:
            return

        if jti:
            await self.tokens.revoke(jti)
