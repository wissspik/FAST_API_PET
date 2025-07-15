import base64
from datetime import datetime,timedelta

from fastapi import APIRouter, Depends, HTTPException



from profile_service.utils.sql_request import (get_user_id_photo,
                                               get_user_id_profile, add_redis, get_redis, delete_redis)
from profile_service.utils.JWT import  get_access_token


app = APIRouter(tags=["profile_service"])


@app.get("/profile/{user_id}")
async def profile(user_id: int, user_id_token: int = Depends(get_access_token)):
    if user_id_token != user_id:
        raise  HTTPException(status_code=401,detail="человек не имеет прав")
    user = await get_user_id_profile(user_id)
    user_photo = await get_user_id_photo(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = {
        "login": user.login,
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "gender": user.gender,
        "city": user.city,
        "age": user.age,
        "file": base64.b64encode(user_photo.file).decode() if user_photo else None,
        "file_name": user_photo.file_name if user_photo else None,
        "mime_type": user_photo.mime_type if user_photo else None,
        "file_size": user_photo.file_size if user_photo else None,
    }
    return user_data
@app.post("/visit_time")
async def time_visit(user_id: int = Depends(get_access_token)):
    user = await get_user_id_profile(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if await get_redis(user_id):
        await delete_redis(user_id)
    time_now = datetime.now()
    await add_redis(user_id, time_now.isoformat())

@app.post("/check_time")
async def check_time(user_id: int):
    time_now = datetime.now()
    client = await get_redis(user_id)
    if client is None:
        # Если записи нет — считаем, что пользователь заходит впервые
        # Можно сразу записать текущее время и возвращать успех
        await add_redis(user_id,time_now)

    last_visit_str = client.decode("utf-8")

    last_visit = datetime.fromisoformat(last_visit_str)

    delta = time_now - last_visit

    if delta > timedelta(minutes=5):
        # Если прошло больше 5 минут — пользователь не в сети
        return {"status":"unactivate"}
    else:
        return {"status":"activate"}
