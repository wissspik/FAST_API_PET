from fastapi import APIRouter,Depends,HTTPException, Query

from article_service.shapes.shapes import Article

import uuid

from datetime import datetime,timezone

from article_service.utils.JWT import get_access_token

from article_service.database.mongo import db


app = APIRouter()

@app.post("/profile/create_article")
async def create_article(article: Article, user_id: int = Depends(get_access_token)):
    article_data = article.dict()
    article_data["article_id"] = uuid.uuid4()
    article_data["timenow"] = datetime.now(timezone.utc)
    article_data["editing"] = False
    article_data["user_id"] = user_id
    try:
        await db["articles"].insert_one(article_data)
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при создании статьи")
    return {"message": "статья успешно создана"}

@app.post("/profile/take_article")
async def take_article(
    user_id: int,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    try:
        cursor = (
            db["articles"].find({"user_id": user_id}).skip(offset).limit(limit)
        )
        articles = await cursor.to_list(length=None)
        total = await db["articles"].count_documents({"user_id": user_id})
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при получении статей")

    clean = []
    for doc in articles:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        clean.append(doc)

    return {"items": clean, "total": total}

@app.delete("/profile/delete_article")
async def delete_article(article: Article, user_id: int = Depends(get_access_token)):
    try:
        result = await db[str(user_id)].delete_many(article.dict())
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при удалении статьи")
    return {"deleted_count": result.deleted_count}

@app.put("/profile/update_article/{article_id}")
async def update_article(
    article_id: str,
    article: Article,
    user_id: int = Depends(get_access_token),
):
    """Update an existing article belonging to the current user."""
    update_data = {
        k: v
        for k, v in article.model_dump().items()
        if v is not None
    }

    try:
        result = await db["articles"].update_one(
            {"article_id": article_id, "user_id": user_id},
            {"$set": update_data},
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении статьи")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    return {"message": "статья успешно обновлена"}

