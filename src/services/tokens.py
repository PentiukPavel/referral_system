from uuid import uuid4

from exceptions import TokenAlreadyExists, TokenDoesNotExist, NoActiveToken
from models import User
from utils.unit_of_work import UnitOfWork
from schemes import EmailData, TokenCreate


class TokenService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_token(self, current_user: User, token_data: TokenCreate):
        async with self.uow:
            token = await self.uow.tokens.get_active_token(current_user.id)
            if token is not None:
                raise TokenAlreadyExists()

            token_data = token_data.model_dump()
            data = {
                "code": uuid4(),
                "expired_at": token_data["expired_at"].replace(tzinfo=None),
                "user_id": current_user.id,
            }

            created_token = await self.uow.tokens.create_token(data)
            await self.uow.commit()
            return created_token

    async def delete_token(self, current_user: User):
        async with self.uow:
            token = await self.uow.tokens.get_active_token(current_user.id)
            if token is None:
                raise TokenDoesNotExist()

            await self.uow.tokens.delete_token(token.id)
            await self.uow.commit()

    async def get_token_by_email(self, email_data: EmailData):
        async with self.uow:
            email_data = email_data.model_dump()
            email = email_data["email"]
            token = await self.uow.tokens.get_active_token_by_email(email)
            if token is None:
                raise NoActiveToken()

            await self.uow.commit()
            return token
