from sqlalchemy import select, update

from db.models.refresh_token import RefreshToken as RefreshTokenORM

from .base import BaseRepository


class RefreshTokenRepository(BaseRepository):
    async def add(self, token: RefreshTokenORM) -> RefreshTokenORM:
        self.session.add(token)
        await self.session.commit()
        return token

    async def get_by_jti(self, jti: str) -> RefreshTokenORM | None:
        result = await self.session.execute(
            select(RefreshTokenORM).where(RefreshTokenORM.jti == jti)
        )
        return result.scalars().first()

    async def revoke_all_for_user(self, user_id: int) -> None:
        await self.session.execute(
            update(RefreshTokenORM)
            .where(
                RefreshTokenORM.user_id == user_id,
                RefreshTokenORM.revoked == False,  # noqa: E712
            )
            .values(revoked=True)
        )
        await self.session.commit()

    async def rotate(self, old_jti: str, new_token: RefreshTokenORM) -> None:
        """Revoke the old token and persist its replacement atomically."""
        await self.session.execute(
            update(RefreshTokenORM)
            .where(RefreshTokenORM.jti == old_jti)
            .values(revoked=True, replaced_by=new_token.jti)
        )
        self.session.add(new_token)
        await self.session.commit()

    async def revoke(self, jti: str) -> None:
        await self.session.execute(
            update(RefreshTokenORM)
            .where(RefreshTokenORM.jti == jti)
            .values(revoked=True)
        )
        await self.session.commit()
