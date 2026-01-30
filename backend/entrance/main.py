from fastapi import FastAPI
from backend.entrance.routers.registration import app as registration_router
app = FastAPI()
app.include_router(registration_router)
