from datetime import datetime

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Token, User
from repositories.base import AbstrsctSQLAlcchemyRepository


class TokenRepository(AbstrsctSQLAlcchemyRepository):
    """
    SQLAlchemy репозиторий для CRUD операций с токенами в БД.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_token(self, user_id: int):
        """
        Получение активного токена по ID пользователя.

        :param user_id: ID пользователя
        :return: Активный токен
        """

        query = (
            select(Token)
            .filter_by(user_id=user_id)
            .filter(Token.expired_at > datetime.now())
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_token(self, data: dict):
        """
        Создание токена в БД.
        """

        stmt = insert(Token).values(data).returning(Token)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_token(self, token_id: int):
        stmt = delete(Token).where(Token.id == token_id)
        await self.session.execute(stmt)

    async def get_active_token_by_email(self, email):
        query = (
            select(Token)
            .join(User, Token.user_id == User.id)
            .where(User.email == email)
            .filter(Token.expired_at > datetime.now())
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
