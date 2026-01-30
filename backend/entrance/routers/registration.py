from fastapi import APIRouter

from backend.entrance.database.db import SessionDep
from backend.entrance.models.models import Entrance, Refresh, Registration
from backend.entrance.services.auth_service import login_user, refresh_access, register_user
from backend.entrance.services.db_service import init_db as init_db_service
app = APIRouter(tags=["registration"])

@app.post("/registration")
async def registration(data: Registration,session: SessionDep)->dict:
    """
    Регистрация нового пользователя.
    :param data:JSON пользователя с данным:login, first_password, second_password
    :param session: сессия для работы с DB
    :return:None
    """
    return await register_user(data, session)
@app.post("/entrance")
async def login(data: Entrance,session: SessionDep)->dict:
    """
    Авторизация нового пользователя.
    :param data:JSON пользователя с данным:login, first_password, second_password
    :param session: сессия для работы с DB
    :return:None
    """
    return await login_user(data, session)


@app.post("/refresh")
async def refresh(data: Refresh) -> dict:
    """
    Обновление access-токена по refresh-токену.
    """
    return await refresh_access(data)

@app.post("/init-db")
async def init_db() -> dict:
    """
    Создание таблиц в БД (если их ещё нет).
    """
    await init_db_service()
    return {"message": "DB initialized"}
