from article_service.database.mongo import db
from fastapi import FastAPI
async def lifespan(app: FastAPI):
    # --- Startup ---
    await db.article.create_index([("user_id", 1)])
