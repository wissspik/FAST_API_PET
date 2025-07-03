from fastapi import APIRouter
from fastapi.responses import JSONResponse,Response

from dotenv import load_dotenv

from auth_service.utils.JWT import create_access_token, create_refresh_token,create_cookie_file
from auth_service.utils.sql_request import put_password,put_login,delete_user
from auth_service.utils.password_val_hash import check_password
from auth_service.shapes.shapes import DeleteAccount,ChangePassword,ChangeLogin
from auth_service.database.base import SessionDep

load_dotenv()

app = APIRouter(prefix="/profile")

@app.put("/change_password")
async def change_password(session:SessionDep,data:ChangePassword):
    if data.password_old != data.password_new:
        return JSONResponse(status_code=400, detail="Пароли не совпадают")  # type: ignore

    elif check_password(data.password_new):
        return JSONResponse(status_code=400, detail="Придумайте корректный пароль") # type: ignore

    if put_password(session,data.id,data.password_old,data.password_new):
        return JSONResponse(status_code=200, detail = "Пароль успешно изменён") # type: ignore
    else:
        return JSONResponse(status_code=400, detail = "Неправильный логин или пароль у пользователя") # type: ignore

@app.put("/change_login")
async def change_login(response : Response,session:SessionDep,data:ChangeLogin):
    result = put_login(session,data.old_login,data.new_login)
    if result:
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")
        access_token = create_access_token(result)
        refresh_token = create_refresh_token(result)
        response = JSONResponse({"message": "Успешная смена пароя"})
        return create_cookie_file(response, access_token, refresh_token)
    else:
        return JSONResponse(status_code=400,detail="Некорректный id у пользователя")

@app.delete("/delete_account")
async def delete_account(session:SessionDep,data:DeleteAccount):
    result = delete_user(session,data.login)
    if result:
        return JSONResponse(status_code=200, detail="Аккаунт успешно удалён")
    else:
        return JSONResponse(status_code=400,detail="Аккаунт не удалён")