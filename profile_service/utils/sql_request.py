from sqlalchemy import select, update

from profile_service.database.redis import redis_client
from profile_service.database.base import SessionDep, new_session
from profile_service.database.models import Photo, Profile

from typing import Any


async def get_user_id_profile(user_id: int) -> Profile | None:
    async with new_session() as session:
        stml = select(Profile).filter_by(id=user_id)
        result = await session.execute(stml)
        return result.scalar_one_or_none()


async def get_user_id_photo(user_id: int) -> Photo | None:
    async with new_session() as session:
        stml = select(Photo).filter_by(profile_id=user_id)
        result = await session.execute(stml)
        return result.scalar_one_or_none()


async def create_user_id(user_id: int, login: str) -> Profile:
    async with new_session() as session:
        new_profile = Profile(id=user_id, login=login)
        session.add(new_profile)
        await session.commit()
        return new_profile


async def create_photo(
    session: SessionDep,
    file: bytes,
    file_name: str,
    mime_type: str,
    user_id: int,
    file_size: int,
) -> None:
    new_photo = Photo(
        profile_id=user_id,
        file_name=file_name,
        mime_type=mime_type,
        file_size=file_size,
        file=file,
    )
    session.add(new_photo)
    await session.commit()


async def put_data_profile(session: SessionDep, id: int, data: dict) -> bool:
    stml = (
        update(Profile)
        .where(Profile.id == id)
        .values(
            name=data["name"],
            surname=data["surname"],
            patronymic=data["patronymic"],
            city=data["city"],
            age=data["age"],
            gender=data["gender"],
        )
        .returning(Profile)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stml)
    await session.commit()
    return result.scalar_one_or_none() is not None


async def add_redis(key: Any, value: Any, exp: int | None = None) -> None:
    redis_client.set(key, value, ex=exp)


async def delete_redis(key: Any) -> None:
    redis_client.delete(key)


async def get_redis(key: Any):
    return redis_client.get(key)
