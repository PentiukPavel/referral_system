from datetime import datetime

from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Referral, Token, User
from repositories.base import AbstrsctSQLAlcchemyRepository


class UserRepository(AbstrsctSQLAlcchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_code(self, code) -> User | None:
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
        stmt = insert(Referral).values({"referral_id": user.id, "referrer_id": referrer.id})
        await self.session.execute(stmt)

    async def follow_up_check(self, user: User, referrer: User):
        query = select(Referral).where(
            and_(
                Referral.referral_id == user.id,
                Referral.referrer_id == referrer.id,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_referrers_of_user(self, user: User):
        query = user.referrers
        result = await self.session.execute(query)
        return result.scalars().all()