from fastapi import HTTPException,Cookie,status
import jwt
from profile.database.redis import redis_client

from dotenv import load_dotenv
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

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
    return {'user_id':int(user_id)}
