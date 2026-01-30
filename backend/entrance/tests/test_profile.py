import pytest
from httpx import ASGITransport, AsyncClient

from backend.entrance.database.db import get_session
from backend.entrance.utils.sql import create_user
from backend.entrance.utils.tokens import create_access_token
from backend.profile_service.main import app as profile_app


@pytest.fixture
async def async_client(db_session):
    async def override_get_session():
        yield db_session
    profile_app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=profile_app),
        base_url="http://test",
    ) as client:
        yield client
    profile_app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(db_session):
    await create_user(db_session, "IvanCool321", "Abcdefg@")
    token = create_access_token("IvanCool321")
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_profile_update_and_clear(async_client, auth_headers):
    get_resp = await async_client.get("/profile", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] is None
    assert get_resp.json()["phone"] is None

    update_payload = {"email": "user@example.com", "phone": "79991234567"}
    update_resp = await async_client.patch("/profile", json=update_payload, headers=auth_headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["email"] == update_payload["email"]
    assert update_resp.json()["phone"] == update_payload["phone"]

    clear_resp = await async_client.patch("/profile", json={"email": None}, headers=auth_headers)
    assert clear_resp.status_code == 200
    assert clear_resp.json()["email"] is None
    assert clear_resp.json()["phone"] == update_payload["phone"]


@pytest.mark.asyncio
async def test_profile_requires_auth(async_client):
    response = await async_client.get("/profile")
    assert response.status_code in (401, 403)
