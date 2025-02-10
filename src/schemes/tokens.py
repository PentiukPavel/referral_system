from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenRetrieve(BaseModel):
    code: UUID
    expired_at: datetime

    class Config:
        from_attributes = True


class ErrorInfo(BaseModel):
    detail: str | None = None
