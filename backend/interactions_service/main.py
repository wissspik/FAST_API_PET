from fastapi import FastAPI

from backend.interactions_service.routers.comments import router as comments_router
from backend.interactions_service.routers.likes import router as likes_router
from backend.interactions_service.routers.views import router as views_router

app = FastAPI()
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(views_router)
