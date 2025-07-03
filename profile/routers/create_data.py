from fastapi import APIRouter,UploadFile,File,HTTPException
from datetime import datetime, timezone
from profile.shapes.shapes import FileUpload
from profile.utils.sql_request import get_user_id
from profile.database.base import SessionDep
from profile.utils.sql_request import create_photo

app = APIRouter(prefix='/profile', tags=['profile'])


@app.post('/data')
async def upload_file(user_id : int,file : UploadFile = File(...)):
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

    new_photo = await create_photo(contents,file_name,file.content_type,uploaded_at,user_id,file_size)



    return {"status":"ok"}