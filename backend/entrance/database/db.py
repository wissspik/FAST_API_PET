import os
from typing import Annotated
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

DATABASE_URL = "postgresql+asyncpg://appuser:strongpass@postgres:5432/full_db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]