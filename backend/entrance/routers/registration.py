from http.client import HTTPException
from fastapi import APIRouter
from backend.entrance.utils.correct_data import check_password,check_login
from backend.entrance.models.models import Registration
from backend.entrance.utils.sql import get_user_login,create_user
from backend.entrance.database.db import SessionDep
app = APIRouter(prefix="/reg", tags=["registration"])

@app.post("/")
async def registration(data: Registration,session: SessionDep)->None:
    """
    Регистрация нового пользователя.
    :param data:JSON пользователя с данным:login, first_password, second_password
    :param session: сессия для работы с DB
    :return:None
    """
    if check_login(data.login):
        raise HTTPException(status_code=400, detail="Login is bad,check roulse web-site")
    elif not check_password(data.first_password):
        raise HTTPException(status_code=400, detail="Password not satisfy rules web-site")
    elif data.first_password != data.second_password:
        raise HTTPException(status_code=400, detail="First password not equal second password")
    elif not get_user_login(session, data.login):
        raise HTTPException(status_code=400, detail="login is occupied")
    elif create_user(session, data.login,data.first_password):
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="bad error")

async def login(data: Registration,session: SessionDep)->None:
    """
    Регистрация нового пользователя.
    :param data:JSON пользователя с данным:login, first_password, second_password
    :param session: сессия для работы с DB
    :return:None
    """
    if check_login(data.login):
        raise HTTPException(status_code=400, detail="Login is bad,check roulse web-site")
    elif not check_password(data.first_password):
        raise HTTPException(status_code=400, detail="Password not satisfy rules web-site")
    elif data.first_password != data.second_password:
        raise HTTPException(status_code=400, detail="First password not equal second password")
    elif not get_user_login(session, data.login):
        raise HTTPException(status_code=400, detail="login is occupied")
    elif create_user(session, data.login,data.first_password):
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="bad error")