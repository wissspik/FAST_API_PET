from auth_service.database.redis import redis_client

from fastapi.responses import JSONResponse
from fastapi import APIRouter,status,Depends,Cookie,Response,HTTPException

from auth_service.shapes.shapes import Registration,Authorization
from auth_service.database.base import SessionDep
from typing import Annotated

from auth_service.utils.JWT import create_access_token, get_current_user, create_refresh_token,set_logout_timestamp_for_user,delete_refresh_jti_from_redis,extract_jti_from_refresh_token
from auth_service.utils.password_val_hash import check_password,hash_password, check_login
from auth_service.utils.sql_request import get_user_login_password,get_user_login,create_user
from dotenv import load_dotenv
import os
import jwt
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


app = APIRouter()

@app.post("/registration")
async def registration(data: Registration,session:SessionDep):
    # 1. проверка на равенство паролей
    if data.confir_password != data.password:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Пароли не совпадают"}
        )
    # 2. проверка логина на правильность
    if not check_login(data.login):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Введите логин по правилам сайта"}
    )
    # 3. проверка пароля на правильность
    valid_password = check_password(data.confir_password)
    if not valid_password:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Введите пароль по правилам сайта"}
    )
    # 4. проверка на существование логина
    found_user = await get_user_login(session,data.login)

    # 5. добавление пользователя в БД с hash паролем.
    if not found_user:
        new_user = await create_user(session,data.login,data.password)
        # создаем access токен
        access_token = create_access_token(new_user.id)

        refresh_token = create_refresh_token(new_user.id)

        response = JSONResponse({"message":"Успешный логин"})
        response.set_cookie(
            key = "access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
        )
        response.set_cookie(
            key = "refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=int(REFRESH_TOKEN_EXPIRE_DAYS) * 86400,
        )
        return response
    else:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Пользователь с таким логином уже существует, придумайте другой"}
        )
@app.post("/entrance")
async def entrance(data:Authorization,session:SessionDep):
    # get_current_user = проверка.
    found_user = await get_user_login_password(session,data.login,data.password)
    if found_user:

        access_token = create_access_token(found_user.id)

        refresh_token = create_refresh_token(found_user.id)

        response = JSONResponse({"message": "Успешный логин"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
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
    else:
        return JSONResponse(

            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Неверный логин или пароль"}
    )

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    """
    Если get_current_user не вернул HTTPException, значит токен валиден,
    и current_user — это user_id из поля "sub".
    """
    return {"message": f"Привет, {current_user}! Вы авторизованы."}

@app.post("/logout")
async def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    access_token: Annotated[str | None, Cookie()] = None
):
    """
    1) Если передан refresh_token — извлекаем из него jti, удаляем ключ из Redis.
    2) Если передан access_token — извлекаем из него user_id и ставим метку logout в Redis.
    3) Удаляем оба куки на клиенте (делаем их «просроченными»).
    """
    # ─────────── 1. Обработка refresh_token ───────────
    if refresh_token is not None:
        try:
            jti, _ = extract_jti_from_refresh_token(refresh_token)
        except HTTPException as e:
            # Если RT совсем неверен или просрочен, всё равно чистим куку и возвращаем 401
            # (токен уже и так нельзя использовать)
            response.delete_cookie("refresh_token")
            raise e

        # Удаляем из Redis запись про этот RT
        delete_refresh_jti_from_redis(jti)

    # ─────────── 2. Обработка access_token ───────────
    if access_token is not None:
        try:
            payload_at = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            # AT уже просрочен — просто удаляем куку, нет смысла ставить метку
            response.delete_cookie("access_token")
        except jwt.InvalidTokenError:
            # Невалидный AT — удаляем куку и 401
            response.delete_cookie("access_token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный Access token"
            )
        else:
            # Если AT валиден, ставим метку logout:<user_id> = текущее время
            user_id = payload_at.get("sub")
            if user_id:
                set_logout_timestamp_for_user(user_id)
            # И затем всё равно удалим куку

    # ─────────── 3. Удаляем куки у клиента ───────────
    # Бывает, кто-то ещё передаёт куки без значений — всё равно удаляем
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")

    return {"message": "Успешный logout"}
    # или 204 код вернуть надо