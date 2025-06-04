from fastapi import FastAPI
from auth_service.routers.aut import app as auth
from starlette.middleware.cors import CORSMiddleware
from auth_service.routers.db import app as db
app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)
app.include_router(auth)
app.include_router(db)

