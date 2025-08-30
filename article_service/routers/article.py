from fastapi import APIRouter,Depends,HTTPException, Query

from article_service.shapes.shapes import Article,ArticleUpdate

import uuid

from datetime import datetime,timezone

from article_service.utils.JWT import get_access_token

from article_service.database.mongo import db


app = APIRouter()

@app.post("/profile/create_article")
async def create_article(article: Article, user_id: int = Depends(get_access_token)):
    article_data = article.dict()
    article_data["article_id"] = str(uuid.uuid4())
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
        result = await db["articles"].delete_many(article.dict())
        print(db["articles"])
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при удалении статьи")
    return {"message": "Статья успешно удалена"}

@app.put("/profile/update_article")
async def update_article(
    article: ArticleUpdate,
    user_id: int = Depends(get_access_token)):
    try:
        result = await db["articles"].update_one(
            {"id": ArticleUpdate.id},  # фильтр
            {"$set": {"Editing": True, # изменения
                      "title" : ArticleUpdate.title,
                      "subtitle" : ArticleUpdate.subtitle,
                      "content" : ArticleUpdate.content,
                      "tags" : ArticleUpdate.tags
                      }
            }
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при изменение статьи")
    return {"message": "статья успешно обновлена"}

