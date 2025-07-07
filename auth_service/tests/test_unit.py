import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from auth_service.main import app
from auth_service.database.models import User
from auth_service.utils.password_val_hash import hash_password
from auth_service.database.base import get_session


@pytest.mark.asyncio
async def test_registration_success(client, session):
    payload = {
        "login": "TestUser01",
        "password": "StrongPass1!",
        "confir_password": "StrongPass1!",
    }
    response = await client.post("/registration", json=payload)
    assert response.status_code == 200
    assert response.json()["message_service"] == "Успешный логин"
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    result = await session.execute(select(User).filter_by(login="TestUser01"))
    assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_registration_password_mismatch(client):
    payload = {
        "login": "MismatchUser",
        "password": "Password1!",
        "confir_password": "Password2!",
    }
    response = await client.post("/registration", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Пароли не совпадают"


@pytest.mark.asyncio
async def test_registration_existing_user(client, session):
    user = User(login="ExistingUser", password=hash_password("Password1!"), role="user")
    session.add(user)
    await session.commit()
    payload = {
        "login": "ExistingUser",
        "password": "Password1!",
        "confir_password": "Password1!",
    }
    response = await client.post("/registration", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Пользователь с таким логином уже существует, придумайте другой"