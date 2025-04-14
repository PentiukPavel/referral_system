from datetime import datetime
from typing import List

from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Referral, Token, User
from repositories.base import AbstrsctSQLAlcchemyRepository


class UserRepository(AbstrsctSQLAlcchemyRepository):
    """
    SQLAlchemy репозиторий для CRUD операций с польщователями в БД.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_code(self, code) -> User | None:
        """
        Получение пользователя по реферальному коду из БД.

        :param code: реферальный код
        :return: пользователь
        """

        query = (
            select(User)
            .join(Token, Token.user_id == User.id)
            .where(
                and_(
                    Token.code == code,
                    Token.expired_at > datetime.now(),
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def refer_to_user(self, user: User, referrer: User) -> None:
        """
        Создание записи о подписке на пользователя в БД.

        :param user: реферал
        :param referrer: референт
        """

        stmt = insert(Referral).values(
            {"referral_id": user.id, "referrer_id": referrer.id}
        )
        await self.session.execute(stmt)

    async def follow_up_check(
        self, user: User, referrer: User
    ) -> Referral | None:
        """
        Проверка наличия записи о подписке в БД.

        :param user: реферал
        :param referrer: референт
        :return: подписка
        """

        query = select(Referral).where(
            and_(
                Referral.referral_id == user.id,
                Referral.referrer_id == referrer.id,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_referrers_of_user(self, user: User) -> List[User]:
        """
        Получение списка рефералов пользователя из БД.

        :param user: пользователь
        :return список рефералов пользователя:
        """

        query = user.referrers
        result = await self.session.execute(query)
        return result.scalars().all()
