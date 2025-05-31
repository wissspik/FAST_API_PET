from fastapi.responses import JSONResponse
from fastapi import APIRouter,status
from auth_service.shapes.shapes import Registration
from auth_service.database.base import SessionDep
from auth_service.database.models import User
from sqlalchemy import select
from auth_service.utils.password_val_hash import check_password,hash_password, check_login
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
    stmt = select(User).filter_by(login=data.login) # крут можно сделать
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    # 5. добавление пользователя в БД с hash паролем.
    if not found_user:
        rpg = User(login=data.login,password=hash_password(data.password),role = 'user')
        session.add(rpg)
        await session.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"detail":"Пользователь успешно создан"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Пользователь с таким логином уже существует, придумайте другой"}
        )
