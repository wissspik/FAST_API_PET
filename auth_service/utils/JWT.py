from datetime import datetime, timedelta, timezone
import os
import jwt
from auth_service.database.redis import redis_client
from dotenv import load_dotenv
from fastapi import HTTPException,Cookie,Depends,status
from typing import Annotated
from uuid import uuid4
import time
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


def create_access_token(user_id : int,additional_claims: dict = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire,
    }
    if additional_claims:
        payload.update(additional_claims)

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id:int) -> str:
    jti = str(uuid4())
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    seconds_to_live = int((expire - now).total_seconds())

    redis_key = f"refresh_jti:{jti}"

    redis_client.set(redis_key, user_id, ex=seconds_to_live)

    return token




async def is_token_revoked(jti : str,token_iat : int) -> bool:

    logout_ts_raw = redis_client.get(f"refresh_jti:{jti}")
    if logout_ts_raw is None:
        return False
    try:
        logout_ts = int(logout_ts_raw)
    except ValueError:
        return True
    return token_iat < logout_ts

async def get_current_user(access_token:  str | None = Cookie(default=None)) -> str:

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token не найден в Cookie"
    )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token просрочен"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный access token"
    )
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Payload токена не содержит sub"
        )
    token_iat = payload.get("iat", 0)
    if is_token_revoked(user_id, token_iat):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отозван (пользователь вышел)"
        )
    return user_id
async def extract_jti_from_refresh_token(rt_token: str) -> str:
    """
    Декодируем Refresh-Token, чтобы достать из payload поле "jti".
    Если токен неверный или просрочен, можно выбросить HTTPException.
    """
    try:
        payload = jwt.decode(rt_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token просрочен"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный Refresh token"
        )

    jti = payload.get("jti")
    user_id = payload.get("sub")
    if jti is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="В Refresh token нет полей jti или sub"
        )
    return jti, user_id  # вернём и jti, и user_id


async def delete_refresh_jti_from_redis(jti: str) -> None:
    """
    Удаляем из Redis ключ, связанный с данным jti Refresh-Token'а
    (чтобы больше нельзя было обменять его на новый Access-Token).
    """
    redis_key = f"refresh_jti:{jti}"
    redis_client.delete(redis_key)
async def set_logout_timestamp_for_user(user_id: str) -> None:
    """
    Ставим в Redis метку «logout» для данного user_id,
    чтобы все Access-Token'ы до этого момента считались отозванными.
    """
    now_ts = int(time.time())
    redis_client.set(f"logout:{user_id}", now_ts)

