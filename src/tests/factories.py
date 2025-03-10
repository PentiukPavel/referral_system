from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from models import User


class UserlFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    first_name = Faker("name")
    last_name = Faker("name")
    email = Sequence(lambda n: "user_{0}@example.example".format(n))
    hashed_password = "some_password"

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:
            await session.commit()
        return instance
