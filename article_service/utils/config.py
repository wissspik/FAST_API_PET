from article_service.database.mongo import db
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    await db.article.create_index([("user_id", 1)])
    yield
    # --- Shutdown (optional) ---
    # await db.client.close()