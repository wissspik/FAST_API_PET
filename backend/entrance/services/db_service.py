from backend.entrance.database.db import engine
from backend.entrance.database.models import Base


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
