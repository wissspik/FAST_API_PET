from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from auth_service.database.base import SessionDep
from auth_service.shapes.shapes import (ChangeLogin, ChangePassword,
                                        DeleteAccount,)
from auth_service.utils.JWT import (create_access_token, create_cookie_file,
                                    create_refresh_token,)
from auth_service.utils.password_val_hash import check_password
from auth_service.utils.sql_request import (
    delete_user,
    get_user_login,
    put_login,
    put_password,
)


load_dotenv()

app = APIRouter(prefix="/profile_service")


@app.put("/change_password")
async def change_password(session: SessionDep, data: ChangePassword):
    if data.password_old != data.password_new:
        return JSONResponse(status_code=400, detail="Пароли не совпадают")  # type: ignore

    elif check_password(data.password_new):
        return JSONResponse(status_code=400, detail="Придумайте корректный пароль")  # type: ignore

    if await put_password(session, data.login, data.password_old, data.password_new):
        return JSONResponse(status_code=200, detail="Пароль успешно изменён")  # type: ignore
    else:
        return JSONResponse(status_code=400, detail="Неправильный логин или пароль у пользователя")  # type: ignore


@app.put("/change_login")
async def change_login(response: Response, session: SessionDep, data: ChangeLogin):
    if not await put_login(session, data.old_login, data.new_login):
        return JSONResponse(status_code=400, detail="Некорректный логин у пользователя")

    updated_user = await get_user_login(session, data.new_login)
    if updated_user is None:
        return JSONResponse(status_code=400, detail="Пользователь не найден")

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    access_token = await create_access_token(updated_user.id)
    refresh_token = await create_refresh_token(updated_user.id)
    response = JSONResponse({"message_service": "Успешная смена пароля"})
    return create_cookie_file(response, access_token, refresh_token)


@app.delete("/delete_account")
async def delete_account(session: SessionDep, data: DeleteAccount):
    result = await delete_user(session, data.login)
    if result:
        return JSONResponse(status_code=200, detail="Аккаунт успешно удалён")
    else:
        return JSONResponse(status_code=400, detail="Аккаунт не удалён")
