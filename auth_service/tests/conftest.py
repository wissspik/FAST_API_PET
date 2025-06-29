import os
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Set required environment variables before importing the application
os.environ.setdefault("DB_USER", "user")
os.environ.setdefault("DB_PASSWORD", "pass")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "db")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_DB", "0")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("SECRET_KEY", "TEST_SECRET")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")

from auth_service.database.models import Base
from auth_service.main import app
from auth_service.database.base import get_session

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")

@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest_asyncio.fixture
async def client(session, monkeypatch):
    class DummyRedis:
        def set(self, *a, **k):
            pass
        def delete(self, *a, **k):
            pass
        def exists(self, *a, **k):
            return False

    dummy = DummyRedis()
    import auth_service.database.redis as db_redis
    import auth_service.utils.sql_request as sql_req
    import auth_service.utils.JWT as jwt_utils
    import auth_service.routers.aut as aut_router

    monkeypatch.setattr(db_redis, "redis_client", dummy)
    monkeypatch.setattr(sql_req, "redis_client", dummy)
    monkeypatch.setattr(sql_req, "add_jti_redis", lambda *args, **kwargs: True)

    def sync_create_cookie_file(response, access_token, refresh_token):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15")),
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7")) * 86400,
        )
        return response

    monkeypatch.setattr(jwt_utils, "create_cookie_file", sync_create_cookie_file)
    monkeypatch.setattr(aut_router, "create_cookie_file", sync_create_cookie_file)

    app.dependency_overrides[get_session] = lambda: session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()