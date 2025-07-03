import time

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, HTTPException,Response
from fastapi.params import Depends

from auth_service.database.redis import redis_client
from auth_service.shapes.shapes import Registration,Authorization
from auth_service.database.base import SessionDep
from auth_service.utils.JWT import create_access_token, create_refresh_token, get_refresh_jti, \
get_access_token,get_access_w_refresh,create_cookie_file
from auth_service.utils.password_val_hash import check_password, check_login
from auth_service.utils.sql_request import get_user_login_password,get_user_login,create_user,add_jti_redis,delete_redis

from auth_service.utils.kafka import logger

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

        response = JSONResponse({})

        logger.info(f"A user has been created with the id: {new_user.id} and login: {new_user.login}")

        return await create_cookie_file(response,access_token,refresh_token)
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

        access_token =  await create_access_token(found_user.id)

        refresh_token = await create_refresh_token(found_user.id)

        response = JSONResponse({"message": "Успешный логин"})

        return await create_cookie_file(response,access_token,refresh_token)
    else:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Неверный логин или пароль"}
    )
@app.get("/protected")
async def protect(access_token = Depends(get_access_token)):
    """
    Проверяет аутентификацию пользователя через access_token из куки.
    Если токен валидный - возвращает информацию о пользователе, иначе 401.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Пользователь аутентифицирован", "user_id": access_token['user_id']}
    )

@app.get("/refresh")
async def refresh_token(Cookies:str = Depends(get_access_w_refresh)):
    """
    Обновляет access_token используя refresh_token из куки.
    Если refresh_token валидный - возвращает новый access_token, иначе 401.
    """
    return Cookies

@app.post("/logout")
async def logout(response:Response,Cookie_refresh:str = Depends(get_refresh_jti),Cookie_access: str = Depends(get_access_token)):
    delete_redis(Cookie_refresh)

    jti = Cookie_access['jti']
    exp = Cookie_access['exp']

    ttl = int(exp - time.time())
    if ttl > 0:
        add_jti_redis(f"bl:{jti}", "1", ttl)
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return {"detail": "Logged out successfully"}


#сделать форму ввода данных
#сделать api gateway