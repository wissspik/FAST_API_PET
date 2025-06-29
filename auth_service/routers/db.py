from fastapi import APIRouter
from auth_service.database.base import engine
from auth_service.database.models import Base
app = APIRouter()

@app.post("/create_all_tables",
          summary="Создание всех таблиц в БД"
          )
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {'message':True}