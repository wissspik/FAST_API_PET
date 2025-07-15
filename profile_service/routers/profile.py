import base64
from datetime import datetime

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
@app.post("/time_visit}")
async def time_visit(user_id: int = Depends(get_access_token)):
    user = await get_user_id_profile(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if await get_redis(user_id):
        await delete_redis(user_id)
        time_now = datetime.now()
        await add_redis(user_id,time_now)
    else:
        time_now = datetime.now()
        await add_redis(user_id,time_now)

# добавить к ручкам успешного логирования,к переходу на ленту,
# к переходу на профиль
# к замене данных из профиля и фотографии тоже
# с взаимодействием и функционала
# сделать design для статуса на странице
# прокинуть redis на другой микросервис