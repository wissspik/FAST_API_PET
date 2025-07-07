from datetime import datetime, timedelta, timezone
import os
import jwt
from pygments.lexer import default

from auth_service.utils.sql_request import add_jti_redis
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidIssuedAtError,
    InvalidSignatureError,
    InvalidAlgorithmError,
    DecodeError,
    MissingRequiredClaimError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidTokenError
)
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

async def create_access_token(user_id : int) -> str:
    jti = str(uuid4())
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=(int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60))
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": now,
        "exp": expire,
        "typ": "access",
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def create_refresh_token(user_id:int) -> str:
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

    add_jti_redis(jti,token,expire_seconds)

    return token


async def get_access_token(access_token: str = Cookie(None, alias="access_token")):
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
    exp = payload.get("exp")
    if exp is None:
        raise HTTPException(
            status_code=401, detail="Token missing jti"
        )
    # Возвращаем user_id из токена
    return {'user_id':int(user_id),'jti':jti,'exp':exp}

async def get_refresh_jti(refresh_token: str = Cookie(None,alias="refresh_token")) -> str:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет refresh_token")
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        # Токен просрочен
        raise HTTPException(status_code=401, detail="Refresh-токен истёк")
    except ImmatureSignatureError:
        # Токен активируется позже, чем сейчас
        raise HTTPException(status_code=401, detail="Токен ещё не действителен")
    except InvalidIssuedAtError:
        # Неверное поле iat
        raise HTTPException(status_code=400, detail="Некорректное время выпуска токена")
    except InvalidSignatureError:
        # Подпись не совпадает
        raise HTTPException(status_code=400, detail="Неверная подпись токена")
    except DecodeError:
        # Ошибка разбора (например, невалидная структура)
        raise HTTPException(status_code=400, detail="Не удалось декодировать токен")
    except MissingRequiredClaimError as e:
        # Отсутствует обязательное поле (например, exp, iat, sub и т.п.)
        raise HTTPException(status_code=400, detail=f"Отсутствует обязательное поле: {e.claim}")
    except InvalidAlgorithmError:
        # Если передан неподдерживаемый алгоритм
        raise HTTPException(status_code=400, detail="Неверный алгоритм токена")
    except InvalidTokenError:
        # Любая другая ошибка проверки токена
        raise HTTPException(status_code=400, detail="Неверный формат или подпись токена")
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="В access-токене нет jti")
    if not redis_client.exists(jti):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Срок жизни refresh токена истёк"
        )
    return jti
async def get_access_w_refresh(refresh_token: str = Cookie(None,alias="refresh_token")):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет refresh_token")
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        # Токен просрочен
        raise HTTPException(status_code=401, detail="Refresh-токен истёк")
    except ImmatureSignatureError:
        # Токен активируется позже, чем сейчас
        raise HTTPException(status_code=401, detail="Токен ещё не действителен")
    except InvalidIssuedAtError:
        # Неверное поле iat
        raise HTTPException(status_code=400, detail="Некорректное время выпуска токена")
    except InvalidSignatureError:
        # Подпись не совпадает
        raise HTTPException(status_code=400, detail="Неверная подпись токена")
    except DecodeError:
        # Ошибка разбора (например, невалидная структура)
        raise HTTPException(status_code=400, detail="Не удалось декодировать токен")
    except MissingRequiredClaimError as e:
        # Отсутствует обязательное поле (например, exp, iat, sub и т.п.)
        raise HTTPException(status_code=400, detail=f"Отсутствует обязательное поле: {e.claim}")
    except InvalidAlgorithmError:
        # Если передан неподдерживаемый алгоритм
        raise HTTPException(status_code=400, detail="Неверный алгоритм токена")
    except InvalidTokenError:
        # Любая другая ошибка проверки токена
        raise HTTPException(status_code=400, detail="Неверный формат или подпись токена")
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
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный Access токен")
    access_token = await create_access_token(user_id)
    response = JSONResponse({"message_service": "Успешный логин"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return response
def create_cookie_file(response : dict,access_token : str,refresh_token : str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(REFRESH_TOKEN_EXPIRE_DAYS) * 86400,
    )
    return response