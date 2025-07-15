import logging

from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from sqlalchemy import delete, select, update

from auth_service.database.base import SessionDep
from auth_service.database.models import User
from auth_service.database.redis import redis_client
from auth_service.utils.password_val_hash import hash_password, verify_password


logger = logging.getLogger(__name__)


async def get_user_id(session: SessionDep, id: str) -> bool:
    stmt = select(User).filter_by(id=id)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    return found_user


async def get_user_login(session: SessionDep, login: str) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    return found_user


async def get_user_login_password(
    session: SessionDep, login: str, password: str
) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    if found_user is None:
        return None
    if not verify_password(password, found_user.password):
        return None
    return found_user


async def create_user(session: SessionDep, login: str, password: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(login=login, password=hashed_password, role="user")
    session.add(new_user)
    await session.commit()
    return new_user


async def put_password(
    session: SessionDep, login: str, password_old: str, password_new: str
) -> bool:
    user = get_user_login(session, login)
    if verify_password(password_old, user.password):
        stml = (
            update(User)
            .where(User.login == login)
            .values(password=password_new)
            .returning(User)
            .execution_options(synchronize_session="fetch")
        )
    result = await session.execute(stml)
    user = result.scalar_one_or_none()
    if user is not None:
        return True
    else:
        return False


async def put_login(session: SessionDep, login_old: str, login_new: str) -> bool:
    user = get_user_login(session, login_old)  #
    if get_user_id(session, login_old) is None:
        stml = (
            update(User)
            .where(User.login == login_old)
            .values(login=login_new)
            .returning(User)
            .execution_options(synchronize_session="fetch")
        )
    result = await session.execute(stml)
    user = result.scalar_one_or_none()
    if user is not None:
        return user.id
    else:
        return False


async def delete_user(session: SessionDep, login: str) -> bool:
    user = get_user_id(session, login)

    if user:
        stml = (
            delete(User)
            .where(User.login == login)
            .returning(User)
            .execution_options(synchronize_session="fetch")
        )

    result = await session.execute(stml)
    user = result.scalar_one_or_none()

    if user is not None:
        return True
    else:
        return False


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
