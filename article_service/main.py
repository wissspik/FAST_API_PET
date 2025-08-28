from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from article_service.routers.article import app as article
from article_service.utils.config import lifespan
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