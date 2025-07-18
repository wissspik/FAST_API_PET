from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from starlette.responses import JSONResponse

from profile_service.database.base import SessionDep
from profile_service.shapes.shapes import ChangeProfile, FileUpload
from profile_service.utils.JWT import get_access_token
from profile_service.utils.sql_request import (create_photo,
                                               get_user_id_profile,
                                               put_data_profile,)


app = APIRouter(prefix="/profile", tags=["profile_service"])


@app.post("/upload_photo")
async def upload_file(
    session: SessionDep,
    user_id: int,
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_access_token)
):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Пользователь не смог поменять данные другого человека",
        )
    check_user = await get_user_id_profile(user_id)
    if not check_user:
        raise HTTPException(
            status_code=400, detail="Данного пользователя не существует"
        )

    # Проверим тип файла(нужно только фото)
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Можно загружать только изображения"
        )

    contents = await file.read()
    file_size = len(contents)

    file_name = file.filename

    new_photo = await create_photo(
        session, contents, file_name, file.content_type, user_id, file_size
    )

    return {"status": "ok"}


@app.put("/change_profile")
async def change_profile(
    session: SessionDep,
    data: ChangeProfile,
    current_user_id: int = Depends(get_access_token)):
    if current_user_id != data.user_id:
        raise HTTPException(
            status_code=400,
            detail="Данный пользователь не имеет права изменять данные другого id",
        )

    check_user = await get_user_id_profile(data.user_id)
    if not check_user:
        raise HTTPException(status_code=400, detail="Данного id не существует")

    result = await put_data_profile(session, data.user_id, data.dict())
    if not result:
        raise HTTPException(
            status_code=400, detail="Проблема с данными, который ввёл пользователь"
        )
    return {"comment": "Пользователь успешно поменял свои данные"}
