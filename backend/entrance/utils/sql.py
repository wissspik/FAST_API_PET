from aiofiles.ospath import exists
from backend.entrance.database.models import Role, User
from backend.entrance.models.models import Registration
from backend.entrance.database.db import SessionDep
from sqlalchemy import select,and_

from backend.entrance.utils.correct_data import hash_password,verify_password


async def get_user_login(session: SessionDep, login: str) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.scalar(stmt)
    print(result)
    return result is not None

async def get_user_login_password(session: SessionDep, login: str, password: str) -> bool:
    stml = select(User).where(User.login==login)
    user = await session.scalar(stml)
    if user:
        if verify_password(password, user.password):
            return True
    return False

async def create_user(session: SessionDep,login: str, password: str)->bool:
    hashes_password_user = hash_password(password)
    stml = User(login=login, password=hashes_password_user, role=Role.user)
    session.add(stml)
    try:
        await session.commit()
        return True
    except Exception:
        await session.rollback()
        return False


