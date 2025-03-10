from uuid import UUID

from exceptions import AlreadyReferred, NotSelf, WrongToken
from models import User
from utils.unit_of_work import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def refer_to_user(
        self,
        code: UUID,
        current_user: User,
    ):
        async with self.uow:
            user = await self.uow.users.get_user_by_code(code)
            if user is None:
                raise WrongToken()

            if user.id == current_user.id:
                raise NotSelf()

            if (
                await self.uow.users.follow_up_check(
                    user=user,
                    referrer=current_user,
                )
                is not None
            ):
                raise AlreadyReferred()

            await self.uow.users.refer_to_user(user, current_user)
            await self.uow.commit()

    async def get_referrers(
        self,
        current_user: User,
    ):
        async with self.uow:
            referrers = await self.uow.users.get_referrers_of_user(
                user=current_user,
            )
            await self.uow.commit()
            return referrers
