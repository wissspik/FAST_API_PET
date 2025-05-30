from fastapi.responses import JSONResponse
from fastapi import APIRouter,status
from auth_service.shapes.shapes import Registration
from auth_service.database.base import SessionDep
from auth_service.database.models import User
from sqlalchemy import select
app = APIRouter()

@app.post("/registration")
async def registration(data: Registration,session:SessionDep):
    stmt = select(User).filter_by(login=data.login)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()
    if not found_user:
        rpg = User(login=data.login,password=data.password,role = 'user')
        session.add(rpg)
        await session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail":"Пользователь успешно создан"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Пользователь с таким логином уже существует, придумайте другой"}
        )
