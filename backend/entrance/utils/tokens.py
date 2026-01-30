import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from redis.asyncio import Redis


JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN", "15"))
REFRESH_TTL_SECONDS = int(os.getenv("REFRESH_TTL_SECONDS", "604800"))

_REFRESH_PREFIX = "refresh:"


def create_access_token(login: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=ACCESS_TTL_MIN)
    payload = {
        "sub": login,
        "iat": now,
        "exp": exp,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def verify_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])


def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)


async def store_refresh_token(redis: Redis, token: str, login: str) -> None:
    key = f"{_REFRESH_PREFIX}{token}"
    await redis.set(key, login, ex=REFRESH_TTL_SECONDS)


async def get_login_by_refresh_token(redis: Redis, token: str) -> str | None:
    key = f"{_REFRESH_PREFIX}{token}"
    return await redis.get(key)
