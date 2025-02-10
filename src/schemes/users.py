from datetime import datetime
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    registered_at: datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
