from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.v1.dependencies import CurrentUserDep, UOWDep
import exceptions as custom_exc
import services
from schemes import ErrorInfo, TokenCreate, TokenRetrieve

v1_token_router = APIRouter(prefix="/api/v1/tokens", tags=["Tokens"])


@v1_token_router.post(
    "/code_create/",
    description="Создание реферального кода.",
    response_model=Union[ErrorInfo, TokenRetrieve],
)
async def create_code_endpoint(
    current_user: CurrentUserDep, uow: UOWDep, token_data: TokenCreate
):
    try:
        token = await services.TokenService().create_token(
            uow, current_user, token_data
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
    uow: UOWDep,
):
    try:
        await services.TokenService().delete_token(uow, current_user)
        return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content=None)
    except custom_exc.TokenDoesNotExist as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail=str(e)
        )
