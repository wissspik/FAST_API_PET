from profile.database.base import SessionDep
from sqlalchemy import select
from profile.database.base import new_session
from profile.database.models import Profile
from sqlalchemy import update

async def get_user_id(user_id: int) -> bool:
    async with new_session() as session:
        stml = select(Profile).filter_by(id=user_id)
        result = await session.execute(stml)
        found_user = result.scalar_one_or_none()
        print(found_user)
        return found_user


# создавать автоматическое создание топиков


async def create_user_id(user_id: int, login: str) -> Profile:
    async with new_session() as session:
        new_profile = Profile(id=user_id, login=login)
        session.add(new_profile)
        await session.commit()
        return new_profile


async def create_photo(
    session: SessionDep, file: bytes, file_name: str, mime_type: str, uploaded_at, user_id: int, file_size: int
) -> None:
    new_photo = Profile(
        profile_id=user_id, file_name=file_name, mime_type=mime_type, file_size=file_size, file=file, uploaded_at=uploaded_at
    )
    session.add(new_photo)
    await session.commit()

async def put_data_profile(session : SessionDep,id : int,data : dict) -> bool:
    user = await get_user_id(id)
    stml = (
        update(Profile)
        .where(Profile.id == id)
        .values(name = data['name'],
                surname = data['surname'],
                patronymic = data['patronymic'],
                city = data['city'],
                age = data['age'],
                gender = data['gender'],)
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
