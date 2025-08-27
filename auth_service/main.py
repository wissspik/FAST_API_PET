from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth_service.routers.aut import app as auth
from auth_service.routers.change_data import app as change_data
from auth_service.routers.db import app as db
from auth_service.utils.kafka import lifespan


app = FastAPI(lifespan=lifespan)

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
app.include_router(auth)
app.include_router(db)

app.include_router(change_data)
