from datetime import datetime, timedelta
import http

import pytest
from sqlalchemy import select

from main import app
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


@pytest.mark.asyncio
async def test_create_token(async_authorized_client, get_session):
    request_data = {
        "expired_at": (datetime.now() + timedelta(days=1)).isoformat(),
    }
    response = await async_authorized_client.post(
        app.url_path_for("create_code_endpoint"), json=request_data
    )
    assert response.status_code == http.HTTPStatus.CREATED
