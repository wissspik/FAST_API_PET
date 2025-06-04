from datetime import datetime, timedelta, timezone
import os
import jwt
from auth_service.database.redis import redis_client
from dotenv import load_dotenv
from fastapi import HTTPException,Cookie,Depends,status
from typing import Annotated
from uuid import uuid4
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
    expire = now + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS) * 86400)
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


def get_current_user(access_token: Annotated[str | None, Cookie()]) -> str:

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
    return user_id



'''
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse

app = FastAPI()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """
    Функция генерации JWT с полем exp, iat.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(access_token: Annotated[str | None, Cookie()]) -> str:
    """
    Зависимость (dependency) для извлечения и валидации JWT из cookie "access_token".
    Если токена нет или он невалиден/просрочен — кидает HTTPException 401.
    Если всё ок, возвращает user_id из поля "sub" payload-а.
    """
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

    return user_id


@app.post("/login")
def login_handler(response: JSONResponse, username: str, password: str):
    """
    Пример простого /login, который на основе username/password возвращает JWT в HttpOnly-cookie.
    """
    # 1) Здесь должна быть ваша проверка логина/пароля (DB, bcrypt и т.д.)
    #    Для примера примем, что любой непустой логин/пароль проходит:
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учётные данные")

    user_id = "user123"  # допустим, после проверки в БД мы получили такой ID

    # 2) Создаём access_token
    access_token = create_access_token({"sub": user_id})

    # 3) Кладём JWT в HttpOnly-cookie
    response = JSONResponse({"message": "Успешный логин"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,          # https-only
        samesite="strict",    # или "lax"
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response


@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    """
    Пример «защищённого» маршрута.
    Если get_current_user не вернул HTTPException, значит токен валиден,
    и current_user — это user_id из поля "sub".
    """
    return {"message": f"Привет, {current_user}! Вы авторизованы."}


@app.post("/logout")
def logout(response: JSONResponse, current_user: str = Depends(get_current_user)):
    """
    Для примера: при выходе мы просто затираем куку.
    (В реальном приложении стоит ещё «отозвать»/удалить Refresh-токен в базе.)
    """
    response = JSONResponse({"message": f"Пользователь {current_user} вышел"})
    response.delete_cookie("access_token", path="/")
    return response


'''