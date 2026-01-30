import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.entrance.database.db import SessionDep
from backend.entrance.database.models import User
from backend.entrance.utils.sql import get_user_by_login
from backend.entrance.utils.tokens import verify_access_token

_security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
    session: SessionDep,
) -> User:
    token = credentials.credentials
    try:
        payload = verify_access_token(token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    login = payload.get("sub")
    if not login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    user = await get_user_by_login(session, login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
