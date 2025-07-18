from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from article_service.routers.article import app as article
app = FastAPI()

app.include_router(article)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)