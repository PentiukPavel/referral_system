from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base import AbstrsctSQLAlcchemyRepository


class UserRepository(AbstrsctSQLAlcchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
