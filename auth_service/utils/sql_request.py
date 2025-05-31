from auth_service.database.base import SessionDep
from auth_service.database.models import User
from sqlalchemy import select


# нахождение п
async def get_user_by_login(session:SessionDep,login : str) -> bool:
    stmt = select(User).filter_by(login=login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    return found_user