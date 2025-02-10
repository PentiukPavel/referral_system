from datetime import datetime, timedelta, timezone
from uuid import uuid4

from core.enums import Limit
from exceptions import TokenAlreadyExists, TokenDoesNotExist
from models import User
from utils.unit_of_work import UnitOfWork


class TokenService:
    async def create_token(
        self,
        uow: UnitOfWork,
        current_user: User,
    ):
        async with uow:
            token = await uow.tokens.get_active_token(current_user.id)
            if token is not None:
                raise TokenAlreadyExists()

            expired_at = datetime.now() + timedelta(hours=Limit.CODE_LIFETIME)
            data = {
                "code": uuid4(),
                "expired_at": expired_at,
                "user_id": current_user.id,
            }

            created_token = await uow.tokens.create_token(data)
            await uow.commit()
            return created_token

    async def delete_token(
        self,
        uow: UnitOfWork,
        current_user: User,
    ):
        async with uow:
            token = await uow.tokens.get_active_token(current_user.id)
            if token is None:
                raise TokenDoesNotExist()

            await uow.tokens.delete_token(token.id)
            await uow.commit()
