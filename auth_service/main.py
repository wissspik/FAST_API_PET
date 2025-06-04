from fastapi import FastAPI
from auth_service.routees.aut import app as registration
from starlette.middleware.cors import CORSMiddleware
from auth_service.routees.db import app as db
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
app.include_router(registration)
app.include_router(db)

