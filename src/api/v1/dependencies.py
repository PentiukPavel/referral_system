from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.auth import current_user
from core.database import get_async_session
from models import User
from utils.unit_of_work import BaseUnitOfWork, UnitOfWork


CurrentUserDep = Annotated[Optional[User], Depends(current_user)]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UOWDep = Annotated[BaseUnitOfWork, Depends(UnitOfWork)]
