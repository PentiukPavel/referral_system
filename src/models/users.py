from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
)
from sqlalchemy.orm import Mapped, relationship

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

    tokens = relationship("Token", back_populates="owner", uselist=True)
