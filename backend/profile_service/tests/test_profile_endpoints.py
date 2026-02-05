import asyncio

import pytest
from fastapi import HTTPException

from backend.entrance.database.models import Role, User
from backend.profile_service.routers.profile import get_profile_by_login


class DummySession:
    def __init__(self, user: User | None) -> None:
        self._user = user

    async def scalar(self, stmt):
        return self._user


def test_get_profile_by_login_found() -> None:
    target = User(
        id=1,
        login="alice",
        password="x",
        role=Role.user,
        email="alice@example.com",
        phone=None,
    )
    current = User(id=2, login="bob", password="x", role=Role.user)

    result = asyncio.run(get_profile_by_login("alice", DummySession(target), current))

    assert result.login == "alice"
    assert result.email == "alice@example.com"


def test_get_profile_by_login_missing() -> None:
    current = User(id=2, login="bob", password="x", role=Role.user)

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(get_profile_by_login("ghost", DummySession(None), current))

    assert excinfo.value.status_code == 404
