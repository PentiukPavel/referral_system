from uuid import UUID

from exceptions import AlreadyReferred, NotSelf, WrongToken
from models import User
from utils.unit_of_work import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def refer_to_user(
        self,
        code: UUID,
        current_user: User,
    ):
        async with self._uow as uow:
            user = await uow.users.get_user_by_code(code)
            if user is None:
                raise WrongToken()

            if user == current_user:
                raise NotSelf()

            if await uow.users.follow_up_check(user, current_user) is not None:
                raise AlreadyReferred()

            await uow.users.refer_to_user(user, current_user)
            await uow.commit()

    async def get_referrers(
        self,
        current_user: User,
    ):
        async with self._uow as uow:
            referrers = await uow.users.get_referrers_of_user(current_user)
            await uow.commit()
            return referrers
