from fastapi.params import Depends

from auth_service.database.redis import redis_client

from fastapi.responses import JSONResponse
from fastapi import APIRouter,status

from auth_service.shapes.shapes import Registration,Authorization
from auth_service.database.base import SessionDep

from auth_service.utils.JWT import create_access_token, get_current_user, create_refresh_token,get_refresh_jti,get_access_jti
from auth_service.utils.password_val_hash import check_password, check_login
from auth_service.utils.sql_request import get_user_login_password,get_user_login,create_user
from dotenv import load_dotenv
import os

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
        access_token =  create_access_token(new_user.id)

        # создаем refresh токен
        refresh_token =  create_refresh_token(new_user.id)

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

        access_token =  create_access_token(found_user.id)

        refresh_token =  create_refresh_token(found_user.id)

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
@app.post("/logout",status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    jti_refresh: str = Depends(get_refresh_jti),
    jti_access: str = Depends(get_access_jti)):

    redis_client.detete(jti_refresh)

    redis_client.set(f"bl:{jti_access}", 1) # сделать время жизни

    response = JSONResponse({"message": "Logout seccessfully"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
@app.get("/protected")
async def protect(current_user = Depends(get_current_user)):
    """
    Проверяет аутентификацию пользователя через access_token из куки.
    Если токен валидный - возвращает информацию о пользователе, иначе 401.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Пользователь аутентифицирован", "user_id": current_user}
    )
@app.get("/refresh")
async def protect(current_user = Depends(get_refresh_jti)):
    return current_user


