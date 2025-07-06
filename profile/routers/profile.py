from fastapi import APIRouter,HTTPException,Depends


from profile.utils.sql_request import get_user_id

app = APIRouter(tags=['profile'])

@app.get("/profile/{user_id}")
async def profile(user_id = Depends(get_user_id)):
    user = await get_user_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = {
        'login': user.login,
        'name' : user.name,
        'surname': user.surname,
        'patronymic': user.patronymic,
        'gender': user.gender,
        'city': user.city,
        'age': user.age
    }
    return {'user_data':user_data}