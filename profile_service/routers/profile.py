import base64

from fastapi import APIRouter, Depends, HTTPException

from profile_service.database.base import SessionDep
from profile_service.utils.sql_request import (get_user_id_photo,
                                               get_user_id_profile,)


app = APIRouter(tags=["profile_service"])


@app.get("/profile/{user_id}")
async def profile(user_id: int):
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
