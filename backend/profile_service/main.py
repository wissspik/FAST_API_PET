from fastapi import FastAPI

from backend.profile_service.routers.profile import router as profile_router

app = FastAPI()
app.include_router(profile_router)
