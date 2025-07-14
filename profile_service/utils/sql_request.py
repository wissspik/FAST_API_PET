from sqlalchemy import select, update

from profile_service.database.base import SessionDep, new_session
from profile_service.database.models import Photo, Profile


async def get_user_id_profile(user_id: int) -> bool:
    async with new_session() as session:
        print("Получаем юзера")
        stml = select(Profile).filter_by(id=user_id)
        result = await session.execute(stml)
        found_user = result.scalar_one_or_none()
        return found_user


async def get_user_id_photo(user_id: int) -> bool:
    async with new_session() as session:
        stml = select(Photo).filter_by(profile_id=user_id)
        result = await session.execute(stml)
        found_user = result.scalar_one_or_none()
        return found_user


# создавать автоматическое создание топиков


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
    user = await get_user_id_profile(id)
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
    user = result.scalar_one_or_none()
    if user is not None:
        return True
    else:
        return False
