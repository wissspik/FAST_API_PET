import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.entrance.database.db import get_session
from backend.entrance.database.models import Base
from backend.entrance.main import app
from backend.entrance.utils.tokens import create_access_token

transport = ASGITransport(app=app)


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        yield session
    await engine.dispose()
@pytest.fixture
async def async_client(db_session):
    async def override_get_session():
        yield db_session
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(async_client):
    user_payload = {
        "login": "IvanCool321",
        "first_password": "Abcdefg@",
        "second_password": "Abcdefg@",
    }
    await async_client.post("/registration", json=user_payload)
    token = create_access_token(user_payload["login"])
    return {"Authorization": f"Bearer {token}"}
