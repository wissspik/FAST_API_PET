import logging

from typing import Optional
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from sqlalchemy import delete, select, update

from auth_service.database.base import SessionDep
from auth_service.database.models import User
from auth_service.database.redis import redis_client
from auth_service.utils.password_val_hash import hash_password, verify_password


logger = logging.getLogger(__name__)


async def get_user_id(session: SessionDep, id: str) -> Optional[User]:
    stmt = select(User).filter_by(id=id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_login(session: SessionDep, login: str) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    return result.scalar_one_or_none()


async def get_user_login_password(
    session: SessionDep, login: str, password: str) -> Optional[User]:
    user = await get_user_login(session, login)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def create_user(session: SessionDep, login: str, password: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(login=login, password=hashed_password, role="user")
    session.add(new_user)
    await session.commit()
    return new_user


async def put_password(
    session: SessionDep, login: str, password_old: str, password_new: str
) -> bool:
    user = await get_user_login(session, login)
    if user is None:
        return False
    if not verify_password(password_old, user.password):
        return False
    hashed_password = hash_password(password_new)
    stmt = (
        update(User)
        .where(User.login == login)
        .values(password=hashed_password)
        .returning(User)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    updated_user = result.scalar_one_or_none()
    return updated_user is not None


async def put_login(session: SessionDep, login_old: str, login_new: str) -> bool:
    user = await get_user_login(session, login_old)
    if user is None:
        return False

    stmt = (
        update(User)
        .where(User.login == login_old)
        .values(login=login_new)
        .returning(User)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    updated_user = result.scalar_one_or_none()
    return updated_user is not None


async def delete_user(session: SessionDep, login: str) -> bool:
    user = await get_user_login(session, login)
    if user is None:
        return False

    stmt = (
        delete(User)
        .where(User.login == login)
        .returning(User)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    deleted_user = result.scalar_one_or_none()
    return deleted_user is not None


def add_jti_redis(jti, token, expire_seconds) -> bool:
    try:
        redis_client.set(jti, token, ex=expire_seconds)
    except RedisError as e:
        logger.error(f"Не удалось сохранить JTI {jti} в Redis: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при сохранении JTI {jti}: {e}", exc_info=True)
        return False

    return True

def delete_redis(key: str) -> None:
    redis_client.delete(key)
