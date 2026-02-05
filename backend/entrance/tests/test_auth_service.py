import asyncio

import pytest
from fastapi import HTTPException

from backend.entrance.models.models import Entrance, Refresh, Registration
from backend.entrance.services import auth_service


class DummySession:
    pass


def test_register_user_conflict(monkeypatch) -> None:
    async def fake_get_user_login(session, login: str) -> bool:
        return True

    monkeypatch.setattr(auth_service, "check_login", lambda value: True)
    monkeypatch.setattr(auth_service, "check_password", lambda value: True)
    monkeypatch.setattr(auth_service, "get_user_login", fake_get_user_login)

    data = Registration(
        login="validlogin",
        first_password="Password",
        second_password="Password",
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(auth_service.register_user(data, DummySession()))

    assert excinfo.value.status_code == 409


def test_login_user_success(monkeypatch) -> None:
    async def fake_get_user_login_password(session, login: str, password: str) -> bool:
        return True

    calls = {}

    async def fake_store_refresh_token(redis, token: str, login: str) -> None:
        calls["token"] = token
        calls["login"] = login

    monkeypatch.setattr(auth_service, "get_user_login_password", fake_get_user_login_password)
    monkeypatch.setattr(auth_service, "create_access_token", lambda login: "access-token")
    monkeypatch.setattr(auth_service, "create_refresh_token", lambda: "refresh-token")
    monkeypatch.setattr(auth_service, "store_refresh_token", fake_store_refresh_token)

    data = Entrance(login="user", password="Password")
    result = asyncio.run(auth_service.login_user(data, DummySession()))

    assert result == {"access": "access-token", "refresh": "refresh-token"}
    assert calls == {"token": "refresh-token", "login": "user"}


def test_refresh_access_invalid(monkeypatch) -> None:
    async def fake_get_login_by_refresh_token(redis, token: str) -> str | None:
        return None

    monkeypatch.setattr(auth_service, "get_login_by_refresh_token", fake_get_login_by_refresh_token)

    data = Refresh(refresh="missing")

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(auth_service.refresh_access(data))

    assert excinfo.value.status_code == 401
