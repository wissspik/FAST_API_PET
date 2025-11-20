from aiofiles.ospath import exists

from backend.entrance.database.models import User
from backend.entrance.models.models import Registration
from backend.entrance.database.db import SessionDep
from sqlalchemy import select

from backend.entrance.utils.correct_data import hash_password


async def get_user_login(session: SessionDep, login: str) ->bool:
    return session.scalar(exists().where(User.login==login))

async def get_user_login_password(session: SessionDep, login: str) ->bool:
    return session.scalar(exists().where(User.login==login))

async def create_user(session: SessionDep, login: str, password: str)->bool:
    hashes_password_user = hash_password(password)
    stml = User(login=login, password=hashes_password_user,role="user")
    session.add(stml)
    try:
        await session.commit()
        return True
    except Exception:
        session.rollback()
        return False


