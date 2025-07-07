from fastapi import APIRouter,HTTPException,Depends

from profile_service.database.base import SessionDep
from profile_service.utils.sql_request import get_user_id_profile, get_user_id_photo

app = APIRouter(tags=['profile_service'])

@app.get("/profile/{user_id}")
async def profile(user_id : int):
    user = await get_user_id_profile(user_id)
    user_photo = await get_user_id_photo(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = {
        'login': user.login,
        'name' : user.name,
        'surname': user.surname,
        'patronymic': user.patronymic,
        'gender': user.gender,
        'city': user.city,
        'age': user.age,
        'file': user_photo.file,
        "file_name": user_photo.file_name,
        "mime_type": user_photo.mime_type


    }
    return user_data
