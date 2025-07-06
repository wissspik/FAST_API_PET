from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime, timezone

from starlette.responses import JSONResponse

from profile.shapes.shapes import FileUpload, ChangeProfile
from profile.utils.sql_request import get_user_id
from profile.database.base import SessionDep
from profile.utils.sql_request import create_photo, put_data_profile
app = APIRouter(prefix='/profile', tags=['profile'])


@app.post('/upload_photo')
async def upload_file(session: SessionDep, user_id: int, file: UploadFile = File(...)):
    check_user = await  get_user_id(user_id)
    if not check_user:
        raise HTTPException(status_code=400, detail="Данного пользователя не существует")

    # Проверим тип файла(нужно только фото)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Можно загружать только изображения")

    contents = await file.read()
    file_size = len(contents)

    file_name = file.filename

    uploaded_at = datetime.now(timezone.utc)

    await create_photo(session, contents, file_name, file.content_type, uploaded_at, user_id, file_size)



    return {"status":"ok"}

@app.put('/change_profile')
async def change_profile(session: SessionDep, data: ChangeProfile):
    check_user = await get_user_id(data.user_id)
    if check_user:
        result = await put_data_profile(session, data.user_id, data.model_dump())
        if result:
            return {'comment':"Пользователь успешно поменял свои данные"}
        else:
            raise HTTPException(status_code=400, detail="Проблема с данными,который ввёл пользователь")
    else:
        raise HTTPException(status_code=400, detail="Данного id не существует")
