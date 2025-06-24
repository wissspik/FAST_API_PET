from auth_service.database.base import SessionDep
from fastapi.responses import JSONResponse
from auth_service.database.models import User
from sqlalchemy import select,update
from auth_service.utils.password_val_hash import hash_password,verify_password

async def get_user_id(session:SessionDep,id : str) -> bool:
    stmt = select(User).filter_by(id=id)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    return found_user

async def get_user_login(session:SessionDep,login : str) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    return found_user

async def get_user_login_password(session:SessionDep,login:str,password:str) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    if found_user is None:
        return None
    if not verify_password(password, found_user.password):
        return None
    return found_user

async def create_user(session:SessionDep,login:str,password:str) -> User:
    hashed_password = hash_password(password)
    new_user = User(login=login, password=hashed_password, role='user')
    session.add(new_user)
    await session.commit()
    return new_user
async def safe_person(session:SessionDep) -> User:
    return True

async def password_put(session : SessionDep,user_id : int,password_old : str,password_new : str) -> bool:
    user = get_user_login(session,str(user_id)) #
    if verify_password(password_old, user.password):
        stml = (
            update(User)
            .where(User.id == user_id)
            .values(password=password_new)
            .returning(User)
            .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stml)
    user = result.scalar_one_or_none()
    if user is not None:
        return  True
    else:
        return False

async def password_put(session : SessionDep,user_id : int) -> bool:
    user = get_user_login(session,str(user_id))
    if user:
        stml = (
            update(User)
            .where(User.id == user_id)
            .values(id=user_id)
            .returning(User)
            .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stml)
    user = result.scalar_one_or_none()
    if user is not None:
        return  True
    else:
        return False



