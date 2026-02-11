from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from . import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    jti = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    replaced_by = Column(String, nullable=True)

    user = relationship("User", back_populates="refresh_tokens")

