from fastapi import APIRouter,Depends,HTTPException

from article_service.shapes.shapes import Article

from datetime import datetime,timezone

from article_service.utils.JWT import get_access_token

from article_service.database.mongo import db


app = APIRouter()

@app.post("/profile/create_article")
async def create_article(article: Article,user_id : int = Depends(get_access_token)):
    article['timenow'] = datetime.now(timezone.utc)
    article['editing'] = 'False'
    await db[str(user_id)].insert_one(article)
    return {'message':'статья успешно создана'}
# сделать удаление и редактирования
# поднять и посмотреть что есть

@app.post("/profile/take_article")
async def take_article(user_id : int):
    cursor = db[str(user_id)].find({})
    articles = await cursor.to_list(length=None)
    if not articles:
        raise HTTPException(status_code=404, detail="Статей не найдено")
    return articles


'''
@app.post("/profile/update_article")
async def update_article(article: Article,user_id : int = Depends(get_access_token)):
'''


