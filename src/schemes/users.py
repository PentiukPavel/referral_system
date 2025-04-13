from datetime import datetime
from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    registered_at: datetime = Field(..., description="Время регистрации")


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
