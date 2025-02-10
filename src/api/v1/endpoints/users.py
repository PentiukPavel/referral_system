from fastapi import APIRouter

from api.v1.auth.auth import (
    auth_backend,
    fastapi_users,
)
from schemes import (
    UserCreate,
    UserRead,
)


v1_users_router = APIRouter(prefix="/api/clients", tags=["Users"])


v1_users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
)


v1_users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
)
