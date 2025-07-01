from profile.database.base import SessionDep
from profile.database.models import Profile
from sqlalchemy import select
from profile.database.base import new_session

async def get_user_id(session:SessionDep,user_id:int) -> bool:
    stml = select(Profile).filter_by(id=user_id)
    result = await session.execute(stml)
    found_user = result.scalar_one_or_none()
    return found_user

# создавать автоматическое создание топиков

async def create_user_id(user_id : int,login : str):
    async with new_session() as session:
        stml = Profile(id = user_id,login = login)
        result = await session.execute(stml)
        user = result.scalar_one_or_none()
        if not user:
            return False
        else:
            return True

async def create_photo(session:SessionDep,file : bytes,file_name : str,mime_type : str,
                       uploaded_at,user_id : int,file_size : int) -> None:
    new_photo = Profile(id = user_id,
                   file_name = file_name,
                   mime_type = mime_type,
                   file_size = file_size,
                   file = file,
                   uploaded_at = uploaded_at)
    session.add(new_photo)
    await session.commit()

