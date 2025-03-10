import http

import pytest
from sqlalchemy import select

from models import User


@pytest.mark.asyncio
async def test_registry(async_client, get_session):
    email = "string1@string.exmpl"
    request_data = {
        "email": email,
        "first_name": "name",
        "last_name": "name",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    }
    response = await async_client.post(
        "api/clients/register", json=request_data
    )
    assert response.status_code == http.HTTPStatus.CREATED
    user_query = select(User).filter_by(email=email)
    result = await get_session.execute(user_query)
    user = result.scalar_one_or_none()
    assert user is not None
