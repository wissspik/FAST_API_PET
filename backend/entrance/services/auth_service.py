from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.entrance.database.redis import redis_client
from backend.entrance.models.models import Entrance, Refresh, Registration
from backend.entrance.utils.correct_data import check_login, check_password
from backend.entrance.utils.sql import (
    create_user,
    get_user_login,
    get_user_login_password,
)
from backend.entrance.utils.tokens import (
    create_access_token,
    create_refresh_token,
    get_login_by_refresh_token,
    store_refresh_token,
)


async def register_user(data: Registration, session: AsyncSession) -> dict:
    if not check_login(data.login):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Login is bad,check roulse web-site",
        )
    if not check_password(data.first_password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password not satisfy rules web-site",
        )
    if data.first_password != data.second_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="First password not equal second password",
        )
    if await get_user_login(session, data.login):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="login is occupied",
        )
    if await create_user(session, data.login, data.first_password):
        return {"message": "User created successfully"}
    raise HTTPException(status_code=400, detail="bad error")


async def login_user(data: Entrance, session: AsyncSession) -> dict:
    if not await get_user_login_password(session, data.login, data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="uncorrect password or login",
        )
    access = create_access_token(data.login)
    refresh = create_refresh_token()
    await store_refresh_token(redis_client, refresh, data.login)
    return {"access": access, "refresh": refresh}


async def refresh_access(data: Refresh) -> dict:
    login = await get_login_by_refresh_token(redis_client, data.refresh)
    if not login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token is invalid",
        )
    access = create_access_token(login)
    return {"access": access}
