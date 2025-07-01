from fastapi import FastAPI
from profile.routers.create_data import app as create_data
from profile.routers.db import app as db
from starlette.middleware.cors import CORSMiddleware
from profile.utils.kafka import lifespan


app = FastAPI(lifespan = lifespan)
app.include_router(create_data)
app.include_router(db)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)