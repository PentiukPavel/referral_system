from datetime import datetime, timedelta, timezone
from uuid import uuid4, UUID

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, relationship

from core.database import Base, CommonMixin
from core.enums import Limit


class Token(CommonMixin, Base):
    code: Mapped[UUID] = Column(
        UUID, nullable=False, unique=True, default=uuid4, index=True
    )
    expired_at: Mapped[datetime] = Column(
        TIMESTAMP,
        default=datetime.now(timezone.utc)
        + timedelta(hours=Limit.CODE_LIFETIME),
        nullable=False,
    )
    owner = relationship("User", back_populates="tokens")
