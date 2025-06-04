
from fastapi.responses import JSONResponse
from fastapi import APIRouter,status,Depends,Cookie

from auth_service.shapes.shapes import Registration,Authorization
from auth_service.database.base import SessionDep


from auth_service.utils.JWT import create_access_token, get_current_user, create_refresh_token
from auth_service.utils.password_val_hash import check_password,hash_password, check_login
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
        access_token = create_access_token({"sub": new_user.id})

        refresh_token = create_refresh_token(new_user.id)

        response = JSONResponse({"message":"Успешный логин"})
        response.set_cookie(
            key = "access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesitem="strict",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        response.set_cookie(
            key = "refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 86400,
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
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        print(response.headers)         # или response.raw_headers
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        )
        print(response.headers)         # или response.raw_headers
        return response
    else:
        return JSONResponse(

            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Неверный логин или пароль"}
    )

@app.get("/protected")
def protected_route(current_user: str | None = Cookie(default=None)):
    """
    Если get_current_user не вернул HTTPException, значит токен валиден,
    и current_user — это user_id из поля "sub".
    """
    return {"message": f"Привет, {current_user}! Вы авторизованы."}


