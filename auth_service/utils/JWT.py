from datetime import datetime, timedelta, timezone
import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi.responses import JSONResponse
from auth_service.utils.sql_request import get_user_id
from auth_service.database.redis import redis_client
from dotenv import load_dotenv
from fastapi import HTTPException,Cookie,status,Depends
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

def create_access_token(user_id : int) -> str:
    jti = str(uuid4())
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": now,
        "exp": expire,
        "typ": "access",
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(user_id:int) -> str:
    jti = str(uuid4())
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": now,
        "exp": expire,
        "typ": "refresh",
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    expire_seconds = int(REFRESH_TOKEN_EXPIRE_DAYS) * 86400

    redis_client.set(jti,token,ex = expire_seconds)

    return token


async def get_current_user(access_token: str = Cookie(None, alias="access_token")):
    if not access_token:
        raise HTTPException(status_code=401, detail="Token is missing")

    #1)Декодируем
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Signature verification failed")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is malformed")
    except jwt.PyJWTError:
        # сюда попадут все остальные ошибки из PyJWT
        raise HTTPException(status_code=401, detail="Invalid token")
    # 2) Проверяем, не отозван ли jti
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="Token missing jti")

    if redis_client.exists(f"bl:{jti}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",

        )
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject",
        )
    # Возвращаем user_id из токена
    return int(user_id)

async def get_access_jti(access_token: str = Cookie(None,alias="access_token")) -> str:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет access_token в куки")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="В access-токене нет jti")
    return jti

async def get_refresh_jti(refresh_token: str = Cookie(None,alias="refresh_token")) -> str:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет refresh_token")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(401, "Refresh-токен истёк")
    except InvalidTokenError:
        raise HTTPException(400, "Неверный формат или подпись токена")
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="В access-токене нет jti")
    if not redis_client.exists(jti):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Срок жизни refresh токена истёк"
        )
    user_id = payload.get("sub")
    access_token = create_access_token(user_id)
    response = JSONResponse({"message": "Успешный логин"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
    )
    return response
