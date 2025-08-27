from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from article_service.routers.article import app as article
from article_service.database.mongo import db
from auth_service.utils.kafka import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(article)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
async def lifespan(app: FastAPI):
    # --- Startup ---
    await db.article.create_index([("user_id", 1)])
