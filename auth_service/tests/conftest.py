import os
from fastapi import Depends
from dotenv import load_dotenv
from typing import Annotated
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(TEST_DATABASE_URL,echo=True)

new_session = async_sessionmaker(engine,expire_on_commit= False)

@pytest_asyncio.fixture
async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]