from http import HTTPStatus
from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.v1.auth.auth import (
    auth_backend,
    fastapi_users,
)
from api.v1.dependencies import CurrentUserDep, user_service_dep
from core.choices import APIMessages
import exceptions as custom_exc
from schemes import UserCreate, UserRead


v1_users_router = APIRouter(prefix="/api/clients", tags=["Users"])


v1_users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
)


v1_users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
)


@v1_users_router.post(
    "/refer/",
    description="Ввести реферальный код.",
)
async def refer_to_user_endpoint(
    current_user: CurrentUserDep,
    user_service: user_service_dep,
    code: UUID,
):
    try:
        await user_service.refer_to_user(code=code, current_user=current_user)
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=APIMessages.REFERRED_SUCCESSFULLY.value,
        )
    except (
        custom_exc.NotSelf,
        custom_exc.AlreadyReferred,
        custom_exc.WrongToken,
    ) as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail=str(e)
        )


@v1_users_router.get(
    "/referers/",
    description="Список референтов.",
    response_model=Optional[List[UserRead]],
)
async def get_referrers_endpoint(
    current_user: CurrentUserDep,
    user_service: user_service_dep,
):
    return await user_service.get_referrers(current_user=current_user)
