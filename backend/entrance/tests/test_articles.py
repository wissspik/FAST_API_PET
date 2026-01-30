import pytest
from httpx import ASGITransport, AsyncClient

from backend.articles_service.main import app as articles_app
from backend.entrance.database.db import get_session
from backend.entrance.utils.sql import create_user
from backend.entrance.utils.tokens import create_access_token


@pytest.fixture
async def async_client(db_session):
    async def override_get_session():
        yield db_session
    articles_app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=articles_app),
        base_url="http://test",
    ) as client:
        yield client
    articles_app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(db_session):
    await create_user(db_session, "IvanCool321", "Abcdefg@")
    token = create_access_token("IvanCool321")
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_article_crud(async_client, auth_headers):
    payload = {
        "title": "My first article",
        "content": "Hello world",
        "interests": ["python", "fastapi"],
    }
    create_resp = await async_client.post("/articles", json=payload, headers=auth_headers)
    assert create_resp.status_code == 201
    body = create_resp.json()
    assert body["id"] > 0
    assert body["title"] == payload["title"]
    assert body["content"] == payload["content"]
    assert body["interests"] == payload["interests"]
    assert body["created_at"]

    list_resp = await async_client.get("/articles", headers=auth_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    article_id = body["id"]
    update_resp = await async_client.patch(
        f"/articles/{article_id}",
        json={"title": "Updated title"},
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated title"

    delete_resp = await async_client.delete(f"/articles/{article_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    list_resp_after = await async_client.get("/articles", headers=auth_headers)
    assert list_resp_after.status_code == 200
    assert list_resp_after.json() == []


@pytest.mark.asyncio
async def test_articles_require_auth(async_client):
    payload = {
        "title": "No auth article",
        "content": "Forbidden",
        "interests": ["noauth"],
    }
    response = await async_client.post("/articles", json=payload)
    assert response.status_code in (401, 403)
