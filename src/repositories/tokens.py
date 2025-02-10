from datetime import datetime

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Token
from repositories.base import AbstrsctSQLAlcchemyRepository


class TokenRepository(AbstrsctSQLAlcchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_token(self, user_id: int):
        query = (
            select(Token)
            .filter_by(
                user_id=user_id,
            )
            .filter(Token.expired_at > datetime.now())
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_token(self, data: dict):
        stmt = insert(Token).values(data).returning(Token)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_token(self, token_id: int):
        stmt = delete(Token).where(Token.id == token_id)
        result = await self.session.execute(stmt)
