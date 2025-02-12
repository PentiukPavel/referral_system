from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class TokenCreate(BaseModel):
    expired_at: datetime


class TokenRetrieve(TokenCreate):
    code: UUID

    class Config:
        from_attributes = True


class ErrorInfo(BaseModel):
    detail: str | None = None


class EmailData(BaseModel):
    email: EmailStr
