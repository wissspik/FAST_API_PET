from fastapi import APIRouter
from fastapi.responses import JSONResponse
from auth_service.utils.sql_request import password_put
from auth_service.utils.password_val_hash import check_password
from auth_service.shapes.shapes import DeleteAccount,ChangePassword,ChangeLogin
from auth_service.database.base import SessionDep

app = APIRouter(prefix="/profile")

@app.put("/change_password")
async def change_password(session:SessionDep,data:ChangePassword):
    if data.password_old == data.password_new:
        return JSONResponse(status_code=400, detail="Пароли не совпадают")  # type: ignore
    elif check_password(data.password_new):
        return JSONResponse(status_code=400, detail="Придумайте корректный пароль") # type: ignore
    if password_put(session,data.id,data.password_old,data.password_new):
        return JSONResponse(status_code=200, detail = "Пароль успешно изменён") # type: ignore
    else:
        return JSONResponse(status_code=400, detail = "Неправильный логин или пароль у пользователя") # type: ignore

@app.put("/change_login")
async def change_password(session:SessionDep,data:ChangeLogin):
    result = ChangeLogin(session,data.id)
    if result:
        JSONResponse(status_code=200,detail="Логин успешно изменён")
    else:
        return JSONResponse(status_code=400,detail="Некорректный id у пользователя")

@app.delete("/delete_account")
async def delete_account(session:SessionDep,data:DeleteAccount):
    return {'message':True}
# дописать удаление пользователя
