import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from auth_service.database.models import Base
from auth_service.database.base import get_session
from auth_service.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield session_factory

    # удаляем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(test_session):
    async def override_get_session():
        async with test_session() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)
