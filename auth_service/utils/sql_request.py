from auth_service.database.base import SessionDep
from auth_service.database.models import User
from sqlalchemy import select
from auth_service.utils.password_val_hash import hash_password,verify_password

# нахождение п
async def get_user_login(session:SessionDep,login : str) -> bool:
    print(login)
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
