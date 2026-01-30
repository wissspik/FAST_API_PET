from fastapi import FastAPI

from backend.articles_service.routers.articles import router as articles_router

app = FastAPI()
app.include_router(articles_router)
