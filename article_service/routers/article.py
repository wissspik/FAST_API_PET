from fastapi import APIRouter,Depends,HTTPException

from article_service.shapes.shapes import Article

from datetime import datetime,timezone

from article_service.utils.JWT import get_access_token

from article_service.database.mongo import db


app = APIRouter()

@app.post("/profile/create_article")
async def create_article(article: Article, user_id: int = Depends(get_access_token)):
    article_data = article.dict()
    article_data["timenow"] = datetime.now(timezone.utc)
    article_data["editing"] = False
    article_data["user_id"] = user_id
    await db["articles"].insert_one(article_data)
    return {"message": "статья успешно создана"}
# сделать удаление и редактирования
# поднять и посмотреть что есть

@app.post("/profile/take_article")
async def take_article(user_id: int):
    cursor = db["articles"].find({"user_id" : user_id})
    articles = await cursor.to_list(length=None)
    if not articles:
        return []

    clean = []
    for doc in articles:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        clean.append(doc)

    return clean
@app.delete("/profile/delete_article")
async def delete_article(artcile : Article,user_id: int = Depends(get_access_token)):
        result = await db[str(user_id)].delete_many(artcile.dict())
        return {"deleted_count": result.deleted_count}
'''
@app.post("/profile/update_article")
async def update_article(article: Article,user_id : int = Depends(get_access_token)):
'''


