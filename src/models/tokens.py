from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, relationship

from core.database import Base, CommonMixin


class Token(CommonMixin, Base):
    code: Mapped[UUID] = Column(UUID, nullable=False, unique=True, index=True)
    expired_at: Mapped[datetime] = Column(TIMESTAMP, nullable=False)
    user_id: Mapped[int] = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User", back_populates="tokens")
