from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TokenCreate(BaseModel):
    expired_at: datetime = Field(..., description="Срок действия")


class TokenRetrieve(TokenCreate):
    code: UUID = Field(..., description="Реферальный код")

    class Config:
        from_attributes = True


class ErrorInfo(BaseModel):
    detail: str | None = None


class EmailData(BaseModel):
    email: EmailStr = Field(..., description="Адрес электронной почты")
