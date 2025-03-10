from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from api.v1.dependencies import CurrentUserDep, token_service_dep
import exceptions as custom_exc
from schemes import EmailData, ErrorInfo, TokenCreate, TokenRetrieve


v1_token_router = APIRouter(prefix="/api/v1/tokens", tags=["Tokens"])


@v1_token_router.post(
    "/code_create/",
    description="Создание реферального кода.",
    response_model=Union[ErrorInfo, TokenRetrieve],
)
async def create_code_endpoint(
    current_user: CurrentUserDep,
    token_service: token_service_dep,
    token_data: TokenCreate,
):
    try:
        token = await token_service.create_token(
            current_user=current_user,
            token_data=token_data,
        )
        return token
    except custom_exc.TokenAlreadyExists as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail=str(e)
        )


@v1_token_router.delete(
    "/code_delete/",
    description="Удаление активного реферального кода.",
)
async def delete_active_code_endpoint(
    current_user: CurrentUserDep,
    token_service: token_service_dep,
):
    try:
        await token_service.delete_token(current_user=current_user)
        return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content=None)
    except custom_exc.TokenDoesNotExist as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail=str(e)
        )


@v1_token_router.post(
    "/get_referral_code/",
    description="Получить реферальный код по email реферала.",
    response_model=Union[ErrorInfo, TokenRetrieve],
)
@cache(expire=90)
async def get_referral_code(
    token_service: token_service_dep, email_data: EmailData
):
    try:
        return await token_service.get_token_by_email(email_data=email_data)
    except custom_exc.NoActiveToken as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail=str(e)
        )
