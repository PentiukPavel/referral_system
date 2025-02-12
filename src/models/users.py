from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
)
from sqlalchemy.schema import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import backref, Mapped, relationship

from core.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String, nullable=False, unique=True)
    first_name: Mapped[str] = Column(String, nullable=False)
    last_name: Mapped[str] = Column(String, nullable=False)
    registered_at: Mapped[datetime] = Column(TIMESTAMP, default=datetime.now())
    hashed_password: Mapped[str] = Column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    referrers: Mapped[List["User"]] = relationship(
        secondary="referrals",
        backref=backref("referrals", lazy="dynamic"),
        lazy="dynamic",
        primaryjoin="Referral.referral_id == User.id",
        secondaryjoin="Referral.referrer_id == User.id",
    )

    tokens = relationship("Token", back_populates="owner", uselist=True)


class Referral(Base):
    __tablename__ = "referrals"
    __table_args__ = (
        UniqueConstraint("referral_id", "referrer_id", name="unique_referral"),
        CheckConstraint("referral_id != referrer_id", name="no_self_refer"),
    )

    referral_id: Mapped[int] = Column(
        Integer,
        ForeignKey(User.id, ondelete="CASCADE"),
        primary_key=True,
    )
    referrer_id: Mapped[int] = Column(
        Integer,
        ForeignKey(User.id, ondelete="CASCADE"),
        primary_key=True,
    )
